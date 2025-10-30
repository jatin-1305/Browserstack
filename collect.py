from bs4 import BeautifulSoup
import os
import pandas as pd
import printData as prd


def second(driver,browser):
    print("Inside collect.py")
    d = {'Title': [], 'Content': []}

    title=[]
    content=[]
    image=[]

    #for article_0
    try: 
        with open (f"data/article_0_{browser}.html") as f:
            html_doc = f.read()
        soup = BeautifulSoup(html_doc,'html.parser')

        c = soup.findAll('p')
        t = soup.findAll('h2')
        for i,j in zip(t,c):
            title.append(i.get_text()), content.append(j.get_text())


        #for article_1
        with open (f"data/article_1_{browser}.html") as f:
            html_doc = f.read()
        soup = BeautifulSoup(html_doc,'html.parser')

        c = soup.find('p')
        t = soup.find('h2')
        img_tag = soup.find('img')
        img_src = img_tag['src']
        image.append(img_src)

        title.append(t.get_text())
        content.append(c.get_text())

        #for article_2
        with open (f"data/article_2_{browser}.html") as f:
            html_doc = f.read()
        soup = BeautifulSoup(html_doc,'html.parser')

        c = soup.find('p')
        t = soup.find('h2')
        title.append(t.get_text())
        content.append(c.get_text())

    except Exception as e:
        print(e)

    d['Title'] = title
    d['Content'] = content
    # d['Image_Link'] = image

    df = pd.DataFrame(data = d)
    df.to_csv('data.csv')

    prd.third(title,content,image,driver,browser)
