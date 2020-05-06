from selenium import webdriver
import time
import threading

url_backend = "http://172.16.224.248/login.php"
url_asm = "http://172.16.224.102/login.php"
username = 'admin'
password = 'password'

def login_bot(url, username, password):
    try:
        driver = webdriver.PhantomJS()
        driver.set_window_size(1120, 550)
        start = time.time()
        driver.get(url)
        driver.find_element_by_name('username').send_keys(username)
        driver.find_element_by_name('password').send_keys(password)
        driver.find_element_by_name('Login').click()
        duration = time.time() - start
        duration = round(duration, 2)
        print(f'\n\n{driver.current_url} done in {duration} seconds\n\n')
        driver.quit()
    except:
        print('\n\nConnection Failure\n\n')

def login_bot_no_thread(n_request, url, username, password):
    start = time.time()
    for i in range(n_request):
        login_bot(url, username, password)
    duration = time.time() - start
    duration = round(duration, 2)
    print(f'\n\n Login bot without thread finished in {duration} seconds')

def login_bot_thread(n_request, max_thread, url, username, password):
    threads = []
    start = time.time()
    for i in range(n_request):
        th = threading.Thread(target=login_bot, args=(url, username, password,))
        threads.append(th)
        th.start()
        while threading.active_count() > max_thread:
            time.sleep(.1)
    for th in threads:
        th.join()
    duration = time.time() - start
    duration = round(duration, 2)
    print(f'\n\n Login bot without thread finished in {duration} seconds')
    
url = url_backend
url = url_asm
# login_bot_no_thread(n_request=10, url=url, username=username, password=password)
login_bot_thread(n_request=10, max_thread=4, url=url, username=username, password=password)
