# -*- coding:utf-8 -*-
# get facebook landingpage videos list
class FbSpider(object):
    """docstring for FbSpilder"""
    email = 'user name'
    password = 'passwords'
    driver_path = '/path/to/chromedriver'
    target_url = 'https://www.facebook.com/pg/wordcalm/ads/?country=1&ref=page_internal'
    video_base_url = 'https://www.facebook.com/wordcalm/videos/{video_id}/'
    videos = []
    file_path = '/tmp/facebook/{create_time}/videos.xlsx'

    def __init__(self):
        super(FbSpider, self).__init__()

    def get_cookies(self):
        print("==============================")
        print("       Geting Cookies!        ")
        print("==============================")
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        import time
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        #选择浏览器
        # option = webdriver.FirefoxOptions()
        # option.add_argument('headless')
        # browser = webdriver.Firefox()   
        # browser.implicitly_wait(10)
        # browser.set_window_size(0,0)
        #访问facebook网页
        browser = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)
        browser.get('https://www.facebook.com/')    
        #输入账户密码
        browser.find_element_by_id('email').clear() 
        browser.find_element_by_id('email').send_keys(self.email)
        browser.find_element_by_id('pass').clear()
        browser.find_element_by_id('pass').send_keys(self.password)
        #模拟点击登录按钮，两种不同的点击方法。。。
        try:    
            #browser.find_element_by_xpath('//button[@id="loginbutton"]').send_keys(Keys.ENTER)
            browser.find_element_by_id('u_0_2').send_keys(Keys.ENTER)
        except Exception as e:
            browser.find_element_by_xpath('//input[@value="Log In"]').send_keys(Keys.ENTER)
            # time.sleep(10)
        except Exception as e:
            print(e)
            browser.find_element_by_xpath('//input[@value="登录"]').send_keys(Keys.ENTER)
        # browser.find_element_by_xpath('//a[@href="https://www.facebook.com/?ref=logo"]').send_keys(Keys.ENTER)
        # browser.file_detector_context('Facebook').send_keys(Keys.ENTER)
        #获取cookie
        cookies = browser.get_cookies()
        time.sleep(5)
        browser.get(self.target_url)
        self.cookies = cookies
        self.html = browser.page_source

        print("================= cookies ================")
        print(cookies)
        #关闭浏览器
        browser.close()

    def get_video_ids(self):
        import re
        str_html = str(self.html)
        match_str = r'"video_id":"[0-9]+"'
        results = re.findall(match_str, str_html)
        video_list = []
        print(results)
        for result in results:
            # result = '"video_id":"363141437878223"'
            video_list.append(self.video_base_url.format(video_id=result[12:-1]))
        self.videos = list(set(video_list))

    def write_df_data_to_file(self, df, file_path):
        # from pandas import ExcelWriter
        # writer = ExcelWriter()
        df.to_excel(file_path, index=False)

    def store_videos_list(self, video_list):
        import datetime as dt
        import pandas as pd
        time_now = dt.datetime.now()
        create_time = '-'.join([str(time_now.year), str(time_now.month), str(time_now.day), str(time_now.hour)])
        path = self.file_path.format(create_time=create_time)
        video_list = [{
            create_time: ','.join([str(tmp) for tmp in video_list])
        }]
        try:
            df = pd.read_excel(path)
        except Exception as e:
            print('no such file')
            df = None
        if not df or df.empty:
            df = pd.DataFrame(video_list)
        else:
            df_list = df.to_dict(orient='records')
            df_list.append(video_list)
            df = pd.DataFrame(df_list)
        self.write_df_data_to_file(df, path)

    def main(self):
        self.get_cookies()
        self.get_video_ids()
        self.store_videos_list(self.videos)


fbspider = FbSpider()
fbspider.main()
