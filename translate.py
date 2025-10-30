from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import collect as c
from googletrans import Translator
from collections import Counter
import re

def fourth(title,content,image,driver,browser):
    english_text=[]
    combined_string = ''
    translator = Translator()
    for i in range(len(title)):
        spanish_text = title[i]
        translated_text = translator.translate(spanish_text, src='es', dest='en')
        final = translated_text.text
        combined_string = combined_string+ str(final)+ ' '
        print('Spanish Title',i+1, spanish_text)
        print('English Title',i+1,final)
        english_text.append(final)


    words = []
    for item in english_text:
        words.extend(item.split())

    # Step 2: Clean each word (remove special chars & lowercase)
    cleaned_words = [
        re.sub(r'[^a-zA-Z0-9]', '', word).lower()
        for word in words
        if word.strip()
    ]

    # Step 3: Count and find duplicates
    word_counts = Counter(cleaned_words)
    duplicates = {word:count for word, count in word_counts.items() if count > 1}
    
    print("Duplicate words in English Title: ")
    for key,val in duplicates.items():
        print("Word: ",key,", Count: ",val,sep='')