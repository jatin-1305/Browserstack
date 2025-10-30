from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import pandas as pd
import requests
import translate as t

def third(title,content,image,driver,browser):
    print('Here are the top 5 topics and contents in Spanish:')
    for i in range(len(title)):
        print('Title',i+1,": ", title[i])
        print('Content',i+1,": ", content[i])

    response = requests.get(image[0])
    with open(f"data/images/image_{browser}.jpg", 'wb') as f:
        f.write(response.content)
    print('Image downloaded')

    t.fourth(title,content,image,driver,browser)