from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup as bs
res=requests.get('http://www.themelock.com')
reptxt = res.text
soup = bs(reptxt, "lxml")
lin = []
tit = []
posts = []
images =[]
print("Enter User Name:")
username = input()

print("Enter Passwd:")
password = input()

print("Enter site domain:")

site = input()

print("Do you have Default login Page")
print("If yes Type 'y' else type 'n'")
yn=input()
if(yn =='y'):
    loginpage = '/wp-login.php'
elif(yn == 'n'):
    print("Enter login page last path")
    loginpage = '/'+input()
else:
    print("Please type Write input")

def Collect():
  for link in soup.find_all('div',{'class':'news-title'}):
    x = str(link)
    l=x.split('"')[3]
    lin.append(l)
    t=x.split('"')[5]
    tit.append(t)

Collect()

def Postgen():
 for url in lin:
   req = requests.post(url)
   urlres = req.text
   soupp = bs(urlres, "lxml")
   post = str(soupp.find_all('div',{'class':'description'})).split('<!--QuoteBegin--><div class="quote"><!--QuoteEBegin-->')[0].split('<div class="description">')[1]
   dlink = str(soupp.find_all('div',{'class':'description'})).split('<!--QuoteBegin--><div class="quote"><!--QuoteEBegin-->')[1].split('<script src="http://www.themelock.com/advertisement.js" type="text/javascript"></script>')[0].split('<!--QuoteEnd--></div><!--QuoteEEnd-->')[0]
   img = str(soupp.find_all('div', {'class': 'full-news img'})).split('src="')[1].split('"/></div>')[0]
   posts.append(post+dlink)
   images.append(img)


Postgen()


try:
  option = Options()
  # Pass the argument 1 to allow and 2 to block
  option.add_experimental_option("prefs", {
      "profile.default_content_setting_values.notifications": 1
  })

  browser = webdriver.Chrome(chrome_options=option, executable_path="chromedriver.exe")
  # To maximize the browser window
  browser.maximize_window()
except DeprecationWarning:
    pass
# goto link setlarry
browser.get('https://'+site+loginpage)

# Enter your user name and password here.


def login():
    browser.find_elements_by_xpath('//*[@id="user_login"]')[0].send_keys(username)
    browser.find_elements_by_xpath('//*[@id="user_pass"]')[0].send_keys(password)
    browser.find_elements_by_xpath('//*[@id="wp-submit"]')[0].click()
    print('Login Successful')


login()

def Post():
    for x in range(len(lin)):
       browser.get('https://'+site+'/wp-admin/post-new.php')
       browser.find_element(By.XPATH, '//*[@id="title"]').send_keys(tit[x])
       browser.find_element(By.XPATH, '//*[@id="content-html"]').click()
       browser.find_element(By.XPATH, '//*[@id="content"]').send_keys(posts[x])
       browser.find_element(By.XPATH, '//*[@id="fifu_input_url"]').send_keys(images[x])
       time.sleep(1)
       browser.find_element(By.XPATH, '//*[@id="fifu_button"]').click()
       browser.execute_script("window.scrollTo(0,0)")
       time.sleep(1)
       browser.find_element(By.XPATH, '//*[@id="publish"]').click()
       print("Post created successful")
       time.sleep(2)

Post()


