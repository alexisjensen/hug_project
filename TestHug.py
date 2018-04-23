import unittest
import random, string
from selenium import webdriver
from selenium.webdriver.support.ui import Select

def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def assertEquals(var1, var2):
    if var1 == var2:
        return True
    else:
        return False

#Simple Title Check
driver = webdriver.Firefox()
driver.get('http://cehermans.pythonanywhere.com/hug')
assert "Hug a Tree" in driver.title

#Register an Account || User Story 5 Defs of Done
driver.get('http://cehermans.pythonanywhere.com/hug/register')

fName = driver.find_element_by_name('first_name')
fName.send_keys("Stinky Farts")

lName = driver.find_element_by_name('last_name')
lName.send_keys("RIPKieran")

username = driver.find_element_by_name('username')
theUsername = randomword(5) + "TestAcc"

eAddress = driver.find_element_by_name('email')
eAddress.send_keys("cpsc310@gmail.com")

username.send_keys(theUsername)

password = driver.find_element_by_name('password')
password.send_keys("ttt")

button = driver.find_element_by_css_selector('.btn.btn-default.register')
button.click()

#Login Test
driver.get('http://cehermans.pythonanywhere.com/hug/login')
uName = driver.find_element_by_name('username')
uName.send_keys(theUsername)

pWord = driver.find_element_by_name('password')
pWord.send_keys("ttt")

button = driver.find_element_by_css_selector('.btn.btn-default')
button.click()

#Index Test, just filters

select = Select(driver.find_element_by_id('neighbourhood'))
select.select_by_visible_text('arbutus ridge')
select.select_by_visible_text('riley park')

#Tree Test
driver.get('http://cehermans.pythonanywhere.com/hug/tree/27951')
favButton = driver.find_element_by_css_selector('.btn.btn-sm.btn-default.tree')
favButton.click()

#Favorites Page Test
linkTree = driver.find_element_by_link_text('tree 27951')
linkTree.click()
unfavButton = driver.find_element_by_css_selector('.btn.btn-sm.btn-default.tree')
unfavButton.click()
html= driver.find_element_by_xpath(".//html")
print(html.text)
assert "You have not loved any trees yet :(" in html.text

#Delete the Username Created?

#Close the damn browser
driver.close()
