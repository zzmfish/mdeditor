# encoding=utf-8

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
            test_dir = os.path.dirname(__file__)
            src_dir = os.path.join(test_dir, '..')
            os.chdir(src_dir)
            python_path = os.popen('which python').read().strip('\r\n\r ')
            python_srcs = []
            python_srcs.append('import config')
            python_srcs.append('config.port=%d' % TEST_PORT)
            python_srcs.append('config.md_dir="%s"' % os.path.join(test_dir, 'md_dir'))
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

        # 点击文件名输入框
        file_input = self.browser.find_element_by_id('FileNameInput')
        file_input.click()
        self.delay()
        self.browser.find_element_by_class_name('ui-autocomplete')
        self.browser.find_element_by_xpath('//li[@class="ui-menu-item" and text() = "test1"]')



if __name__ == '__main__':
    unittest.main(verbosity=2)