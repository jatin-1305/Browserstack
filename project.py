from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import collect as c

def first(driver,browser):

    # 1st col - b-d_a
    # 2nd col - b-d_b
    # 3rd col - b-d_c
    file = 0
    l=['a','b','c']
    title = 'article'
    for i in l:
        name = "b-d_"+i
        elems = driver.find_elements(By.CLASS_NAME, name)
        for elem in elems:
            data = elem.get_attribute("outerHTML")
            with open(f"data/{title}_{file}_{browser}.html","w",encoding="utf-8") as f:
                f.write(data)
                file+=1

    c.second(driver,browser)