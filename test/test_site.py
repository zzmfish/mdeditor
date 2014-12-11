__author__ = 'zhouzhiming'


import sys
import os
import os.path
import time
import signal
import unittest
import selenium.webdriver as webdriver

TEST_PORT = 19168

class GoogleTestCase(unittest.TestCase):

    def get_url(self, path):
        return 'http://127.0.0.1:%d/%s' % (TEST_PORT, path)

    def init_server(self):
        pid = os.fork()
        if pid == 0:
            src_dir = os.path.join(os.path.dirname(__file__), '..')
            os.chdir(src_dir)
            python_path = os.popen('which python').read().strip('\r\n\r ')
            python_srcs = []
            python_srcs.append('import config')
            python_srcs.append('config.port=%d' % TEST_PORT)
            python_srcs.append('import main')
            python_srcs.append('main.main()')
            os.execv(python_path, [python_path, '-c', ';'.join(python_srcs)])
        self.addCleanup(self.stop_setver, pid)
        time.sleep(1)

    def stop_setver(self, server_pid):
        os.kill(server_pid, signal.SIGINT)

    def init_browser(self):
        self.browser = webdriver.Firefox()
        self.addCleanup(self.browser.quit)

    def delay(self):
        time.sleep(1)

    def setUp(self):
        self.init_server()
        self.init_browser()

    def test_case1(self):
        self.browser.get(self.get_url(''))
        self.delay()

        self.browser.find_element_by_id('Editor')

if __name__ == '__main__':
    unittest.main(verbosity=2)