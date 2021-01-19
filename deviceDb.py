import webbrowser
# import urllib.request
#
# with urllib.request.urlopen('https://rconfig01.ptu.sphaera.ru/devices.php') as response:
#     html = response.read()
#
#     print(html.decode('utf-8'))

from selenium import webdriver

driver = webdriver.Firefox()
driver.get(url='https://rconfig01.ptu.sphaera.ru/devices.php')
element = driver.find_element_by_css_selector('button.show_hide')
element.click()
