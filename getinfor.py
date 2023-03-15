import time
from appium import webdriver
from appium.webdriver.common import mobileby
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

desired_caps = {'platformName': 'Android',
                'platformVersion': '7.1.2',
                'appPackage': 'com.sina.weibo',  # 新浪微博
                'appActivity': '.MainTabActivity',  # 打开微博APP首页
                'unicodeKeyboard': True,
                'resetKeyboard': True,
                'noReset': True,
                'deviceName': '127.0.0.1:62001'
                }  # 和启动命令保持一致

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
time.sleep(8)
x = driver.get_window_size()['width']  # 获取屏幕的高
y = driver.get_window_size()['height']  # 获取屏幕的宽
driver.find_element_by_xpath('//android.widget.FrameLayout[@content-desc="我"]').click()
time.sleep(8)
driver.find_element_by_xpath(
    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.TabHost/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.FrameLayout[2]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]').click()
time.sleep(8)
driver.find_element_by_xpath('//*[@text="关注的人"]').click()
time.sleep(8)
for i in range(4, 10):
    txt1 = driver.find_element_by_xpath(
        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.RelativeLayout[{}]/android.widget.LinearLayout/android.view.ViewGroup/android.widget.TextView[1]'.format(
            i)).text
    txt2 = driver.find_element_by_xpath(
        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.RelativeLayout[{}]/android.widget.LinearLayout/android.view.ViewGroup/android.widget.TextView[2]'.format(
            i)).text
    print(txt1 + ' ' + txt2)
for j in range(2):
    driver.swipe(1 / 2 * x, 4 / 5 * y, 1 / 2 * x, 0, 600)
    time.sleep(8)
    for i in range(1, 9):
        txt1 = driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.RelativeLayout[{}]/android.widget.LinearLayout/android.view.ViewGroup/android.widget.TextView[1]'.format(
                i)).text
        txt2 = driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.RelativeLayout[{}]/android.widget.LinearLayout/android.view.ViewGroup/android.widget.TextView[2]'.format(
                i)).text
        print(txt1 + ' ' + txt2)
