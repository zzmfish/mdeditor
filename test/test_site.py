# encoding=utf-8

import sys
import os
import os.path
import time
import signal
import unittest
import selenium.webdriver as webdriver

TEST_PORT = 19168

class TestSiteBase(unittest.TestCase):

    server_pid = 0
    browser = None

    def get_url(self, path=''):
        return 'http://127.0.0.1:%d/%s' % (TEST_PORT, path)

    @classmethod
    def init_server(cls):
        pid = os.fork()
        if pid == 0:
            test_dir = os.path.dirname(__file__)
            src_dir = os.path.join(test_dir, '..')
            os.chdir(src_dir)
            python_path = os.popen('which python').read().strip('\r\n\r ')
            python_srcs = list()
            python_srcs.append('import config')
            python_srcs.append('config.port=%d' % TEST_PORT)
            python_srcs.append('config.md_dir="%s"' % os.path.join(test_dir, 'md_dir'))
            python_srcs.append('import main')
            python_srcs.append('main.main()')
            os.execv(python_path, [python_path, '-c', ';'.join(python_srcs)])
        cls.server_pid = pid
        time.sleep(1)

    def delay(self):
        time.sleep(1)

    @classmethod
    def setUpClass(cls):
        cls.init_server()
        cls.browser = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        if cls.server_pid:
            os.kill(cls.server_pid, signal.SIGINT)
        if cls.browser:
            cls.browser.quit()


class TestSite(TestSiteBase):

    def test_editor(self):
        self.browser.get(self.get_url())
        self.browser.find_element_by_id('Editor')

    def test_file_input(self):
        # 点击文件名输入框
        self.browser.get(self.get_url())
        file_input = self.browser.find_element_by_id('FileNameInput')
        file_input.click()
        self.delay()
        self.browser.find_element_by_class_name('ui-autocomplete')
        self.browser.find_element_by_xpath('//li[@class="ui-menu-item" and text() = "test1"]')


if __name__ == '__main__':
    unittest.main(verbosity=2)