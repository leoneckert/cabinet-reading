from selenium import webdriver
import time, os
import random
import ConfigParser 
from bs4 import BeautifulSoup
import urllib
#  from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0

config = ConfigParser.ConfigParser()
try:
    config.read('settings.cfg')
    print "[+] Read settings"
except:
    print "[-] Could not read settings"

configUname = config.get('twitter','uname')
configPassword = config.get('twitter','password')



def get_cabinet():
    cabinet_url = "https://en.wikipedia.org/wiki/Cabinet_of_the_United_States"
    html = urllib.urlopen(cabinet_url).read()
    soup = BeautifulSoup(html, 'html.parser')

    politicians = list()

    tables = soup.select('.wikitable')
    for table in tables:
        if table.th.text == "Cabinet":
            entries = table.findAll('tr')
            for entry in entries:
                entry_contents = entry.findAll('td')
                if len(entry_contents) == 3:
                    name = entry_contents[1].findAll('div')[0].select('a')[0].text
                    if name != "TBD":
                        politicians.append(name)

    return politicians

politicians = get_cabinet()
#  print politicians



driver = webdriver.Firefox()
url = "https://twitter.com"
driver.get(url)


driver.find_element_by_css_selector('a.js-login').click()
email_box = driver.find_element_by_css_selector('.js-signin-email')
for letter in configUname:
    email_box.send_keys(letter)
    #  time.sleep(random.uniform(0.5,0.9))

password_wrapper = driver.find_element_by_css_selector('.LoginForm-password')
password_box = password_wrapper.find_element_by_css_selector('.text-input')
for letter in configPassword:
    password_box.send_keys(letter)
    #  time.sleep(random.uniform(0.5,0.9))

login_button = driver.find_element_by_css_selector('.js-submit')
login_button.click()

time.sleep(3)
search_box = driver.find_element_by_css_selector('.search-input')
#  print search_box

for letter in random.choice(politicians):
    search_box.send_keys(letter)
    #  time.sleep(random.uniform(0.5,0.9))
driver.find_element_by_css_selector('.Icon--search').click()

time.sleep(6)
driver.get(driver.current_url + "&f=tweets&vertical")
time.sleep(5)
scrollTo = None
previousScroll = 0
for i in range(random.choice(range(5,12))):
    try:
        scrollTo =  random.choice([150, 250, 400, 600])
        driver.execute_script("window.scrollTo(" + str(previousScroll) + ", " + str(previousScroll + scrollTo) +  ");")
        #  time.sleep(random.uniform(0.1,0.4))
        previousScroll = (previousScroll + scrollTo)
    except:
        print "can'tscroll"

tweets = driver.find_elements_by_css_selector('.tweet')
#  print tweets
tweet = random.choice(tweets)
tweet.click()
#
#  print tweet.text
time.sleep(2)
t = driver.find_element_by_css_selector('p.TweetTextSize--26px')
#  print t
print t.text

import unicodedata, re

all_chars = (unichr(i) for i in xrange(0x110000))
control_chars = ''.join(c for c in all_chars if unicodedata.category(c) == 'Cc')
# or equivalently and much more efficiently
control_chars = ''.join(map(unichr, range(0,32) + range(127,160)))

control_char_re = re.compile('[%s]' % re.escape(control_chars))

def remove_control_chars(s):
    return control_char_re.sub('', s)

os.system("say '" + str(remove_control_chars(t.text)) + "'") 

#  text = driver.find_element_by_css_selector(".permalink-container").find_element_by_css_selector('.tweet-text').text
#  print text

#  #  titles = driver.find_elements_by_css_selector('h2.title')
#
#  for title in titles:
#      print title
#
#  driver.quit()
