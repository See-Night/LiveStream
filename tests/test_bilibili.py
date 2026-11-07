"""Replay Bilibili quality negotiation through the real CLI, without network/video."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'livestream'


class BilibiliTests(unittest.TestCase):
    def run_cli(self, *, logged_in=True, scenario='live', url=False,
                source='file', cookie_after=False, extra_args=()):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            temp_dir = root / 'temporary cookies'
            temp_dir.mkdir()
            package = root / 'yt_dlp'
            package.mkdir()
            (package / '__init__.py').write_text('')
            (package / 'cookies.py').write_text('''
import http.cookiejar, os, time
from pathlib import Path
YoutubeDLCookieJar = http.cookiejar.MozillaCookieJar
def extract_cookies_from_browser(browser, logger=None):
    Path(os.environ['TEST_BROWSER_RECORD']).write_text(browser)
    if os.environ['TEST_SCENARIO'] == 'browser-error':
        raise RuntimeError('browser unavailable')
    jar = YoutubeDLCookieJar()
    if os.environ['TEST_SCENARIO'] == 'browser-empty':
        return jar
    for domain, name, expiry in [('.bilibili.com', 'SESSDATA', time.time() + 3600),
                                  ('.api.live.bilibili.com', 'session', None),
                                  ('.notbilibili.com', 'other', time.time() + 3600),
                                  ('.bilibili.com', 'old', 1)]:
        jar.set_cookie(http.cookiejar.Cookie(
            0, name, 'fake-secret', None, False, domain, True, True,
            '/', True, True, expiry, expiry is None, None, None, {}))
    return jar
''')
            curl = root / 'curl'
            curl.write_text('''#!/usr/bin/env python3
import json, os, stat, sys
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
args = sys.argv[1:]
url = next(a for a in reversed(args) if a.startswith('https://'))
query = parse_qs(urlsplit(url).query)
scenario = os.environ['TEST_SCENARIO']
record = {'cookie_file': None, 'cookie_names': []}
if '--cookie' in args:
    path = Path(args[args.index('--cookie') + 1])
    record.update(cookie_file=str(path), mode=stat.S_IMODE(path.stat().st_mode),
                  cookie_names=[line.split('\\t')[5] for line in path.read_text().splitlines()
                                if line and not line.startswith('#')])
with open(os.environ['TEST_RECORD'], 'a') as output:
    output.write(json.dumps(record) + '\\n')
if scenario == 'network-error':
    sys.exit(7)
if scenario == 'invalid-json':
    print('<html>upstream error</html>'); sys.exit()
if '/get_info?' in url:
    data = {'room_id': 7734200, 'live_status': 0 if scenario == 'offline' else 1}
    print(json.dumps({'code': 0, 'data': data})); sys.exit()
if '/playUrl?' in url:
    print(json.dumps({'code': 0, 'data': {'current_quality': 3, 'durl': [{'url': 'https://cdn.example/live.flv?qn=150'}]}})); sys.exit()
if scenario == 'api-error':
    print(json.dumps({'code': -101, 'message': 'not logged in', 'data': None})); sys.exit()
qn = int(query.get('qn', ['0'])[0])
if qn not in (10000, 15000):
    sys.exit('wrong requested quality')
authenticated = '--cookie' in args
actual = qn if authenticated and scenario != 'expired' else 250
def codec(name, quality):
    return {'codec_name': name, 'current_qn': quality, 'accept_qn': [15000, 10000, 400, 250, 150],
            'base_url': '/live.flv', 'url_info': [{'host': 'https://cdn.example', 'extra': f'?qn={quality}'}]}
streams = [] if scenario == 'empty' else [
    {'protocol_name': 'http_hls', 'format': [{'format_name': 'ts', 'codec': [codec('hevc', actual)]}]},
    {'protocol_name': 'http_stream', 'format': [{'format_name': 'flv', 'codec': [codec('hevc', actual), codec('avc', actual)]}]},
]
if scenario == 'mixed':
    streams[1]['format'][0]['codec'][1]['current_qn'] = 250
    streams[1]['format'][0]['codec'][1]['url_info'][0]['extra'] = '?qn=250'
data = {'live_status': 1, 'playurl_info': {'playurl': {'g_qn_desc': [
    {'qn': 30000, 'desc': 'Dolby'}, {'qn': 15000, 'desc': '2K'},
    {'qn': 10000, 'desc': 'Original'}, {'qn': 250, 'desc': 'HD'}], 'stream': streams}}}
print(json.dumps({'code': 0, 'data': data}))
''')
            player = root / 'player'
            player.write_text('#!/bin/sh\nprintf "PLAYED:%s\\n" "$1"\n')
            curl.chmod(0o755)
            player.chmod(0o755)
            config = root / 'config' / 'livestream'
            config.mkdir(parents=True)
            cookie_file = root / 'login cookies.txt'
            cookie_text = '# Netscape HTTP Cookie File\n.bilibili.com\tTRUE\t/\tTRUE\t2147483647\tSESSDATA\tfake-secret\n'
            cookie_file.write_text(cookie_text)
            # Legacy defaults must never implicitly opt into cookies.
            (config / 'cookies.txt').write_text(cookie_text)
            env = dict(os.environ, PATH=f'{tmp}:{os.environ["PATH"]}',
                       XDG_CONFIG_HOME=str(root / 'config'), TEST_SCENARIO=scenario,
                       BILIBILI_COOKIE_FILE=str(cookie_file), PYTHONPATH=str(root),
                       TMPDIR=str(temp_dir), TEST_RECORD=str(root / 'requests.jsonl'),
                       TEST_BROWSER_RECORD=str(root / 'browser.txt'))
            args = ['https://live.bilibili.com/6'] if url else ['bilibili', '6']
            cookie_args = ['--cookie-from', str(cookie_file) if source == 'file' else source] if logged_in else []
            args = args + cookie_args if cookie_after else cookie_args + args
            result = subprocess.run([str(SCRIPT), '-p', str(player), *args, *extra_args],
                                    env=env, capture_output=True, text=True, timeout=5)
            record = root / 'requests.jsonl'
            result.requests = [json.loads(line) for line in record.read_text().splitlines()] if record.exists() else []
            browser_record = root / 'browser.txt'
            result.browser = browser_record.read_text() if browser_record.exists() else None
            result.temporary_files = list(temp_dir.iterdir())
            result.cookie_file_unchanged = cookie_file.read_text() == cookie_text
            return result

    def test_highest_available_quality(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('PLAYED:https://cdn.example/live.flv?qn=15000', result.stdout)
        self.assertIn('15000', result.stderr)

    def test_url_invocation(self):
        result = self.run_cli(url=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('qn=15000', result.stdout)

    def test_anonymous_downgrade_is_visible(self):
        result = self.run_cli(logged_in=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('qn=250', result.stdout)
        self.assertIn('Warning', result.stderr)
        self.assertIn('Cookie', result.stderr)
        self.assertTrue(all(request['cookie_file'] is None for request in result.requests))
        self.assertIsNone(result.browser)

    def test_expired_cookie_downgrade_is_visible(self):
        result = self.run_cli(scenario='expired')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Warning', result.stderr)

    def test_quality_takes_priority_over_codec(self):
        result = self.run_cli(scenario='mixed')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('qn=15000', result.stdout)

    def test_failures_never_launch_player(self):
        for scenario in ('offline', 'empty', 'api-error', 'network-error', 'invalid-json'):
            with self.subTest(scenario=scenario):
                result = self.run_cli(scenario=scenario)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('PLAYED:', result.stdout)

    def test_cookie_file_with_spaces_is_used_without_modification(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(all(request['cookie_names'] == ['SESSDATA'] for request in result.requests))
        self.assertTrue(result.cookie_file_unchanged)
        self.assertIsNone(result.browser)

    def test_browser_cookies_are_filtered_private_and_temporary(self):
        for browser in ('firefox', 'chrome'):
            with self.subTest(browser=browser):
                result = self.run_cli(source=browser)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('qn=15000', result.stdout)
                self.assertEqual(result.browser, browser)
                self.assertTrue(all(set(request['cookie_names']) == {'SESSDATA', 'session'}
                                    for request in result.requests))
                self.assertTrue(all(request['mode'] == 0o600 for request in result.requests))
                self.assertEqual(result.temporary_files, [])
                self.assertNotIn('fake-secret', result.stdout + result.stderr)

    def test_browser_cookies_cleaned_up_on_failure(self):
        for scenario in ('api-error', 'network-error', 'browser-error', 'browser-empty'):
            with self.subTest(scenario=scenario):
                result = self.run_cli(source='firefox', scenario=scenario)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('PLAYED:', result.stdout)
                self.assertEqual(result.temporary_files, [])

    def test_options_after_room_are_supported(self):
        result = self.run_cli(cookie_after=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('qn=15000', result.stdout)

    def test_invalid_source_fails_before_requests(self):
        for source in ('unsupported-browser', '/missing/cookies.txt'):
            with self.subTest(source=source):
                result = self.run_cli(source=source)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.requests, [])
                self.assertNotIn('PLAYED:', result.stdout)

    def test_missing_cookie_source_is_an_error(self):
        result = self.run_cli(logged_in=False, extra_args=['--cookie-from'])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('--cookie-from requires a value', result.stderr)
        self.assertEqual(result.requests, [])


if __name__ == '__main__':
    unittest.main()
