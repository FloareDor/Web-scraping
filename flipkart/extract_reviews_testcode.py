from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests as rq
import pandas as pd
from time import sleep
import re
from pandas import *
from base64 import decode
from encodings import utf_8
import random

reviewlist=[]
reqdf = read_csv('flipkart_url.csv')
tempdata=reqdf["URL"].tolist()
orgdata=set(tempdata)
newdata=list(orgdata)
# df = pd.DataFrame(newdata)
# df.to_csv('flipkart_set_url.csv',mode='a', index=False)


def extract_reviews(review_url):
    resp = rq.get(review_url)
    soup = bs(resp.text, 'html.parser')
    reviews = soup.findAll('div', {'class':"_1AtVbE col-12-12"})

    for single_review in reviews:
        print(single_review)
        with open('outputs/file.html', 'w', encoding='utf-8') as f:
            f.write(str(single_review))
    
    # print(single_review.find('p', {'class':"_2-N8zT"}).text.strip())
    # print(single_review.find('div', {'class': '_3LWZlK _1BLPMq'}).text.strip())
    # print(single_review.find('div', {'class': 't-ZTKy'}).find().text.strip())
    # dict_review = {
    #         'productTitle': (str(review_url).split(".com/")[1]).split("product-reviews")[0],
    #         'Review Title': single_review.find('p', {'class':"_2-N8zT"}).text.strip(),
    #         'Rating': single_review.find('div', {'class': '_3LWZlK _1BLPMq'}).text.strip(),
    #         'Review Body': single_review.find('div', {'class': 't-ZTKy'}).find().text.strip() ,
    #     }
    
    # reviewlist.append(dict_review)

def totalreviews(product_url):
    resp = rq.get(product_url)
    soup = bs(resp.text, 'html.parser')
    reviews = soup.find('span', {'class':"_2_R_DZ"})
    temp = reviews.text.split('\xa0')

    temp_list = temp[-1].split(" ")
    print(temp_list[0])
    return int(temp_list[0])

    #needs to return number of reviews count

def totalpages(review_url):
    resp = rq.get(review_url)
    soup = bs(resp.text, 'html.parser')
    pages = soup.find('div', {'class':"_2MImiq _1Qnn1K"}).find('span')
    temp = pages.text.split(" ")
    # return pages.text
    return(int(temp[-1]))
    #needs to return number of pages

def main():
    product_url="https://www.flipkart.com/ryme-combo-ying-yang-dream-catcher-five-rings-multi-attract-positive-dreams-decorative-showpiece-55-cm/p/itm160b7e33e0fd4?pid=SHIF96HSGQEKNDX8&fm=organic&ppt=dynamic&ppn=dynamic&ssid=t989af0e740000001666083668826"
    # totalreviews(product_url)
    revlist=[] #empty revlist
    for url in range(1): #ideally should be newdata
        # product_url=newdata[url]
        review_url = product_url.replace("/p/", "/product-reviews/") + "&page=" + str(1)
        page_count=totalpages(review_url)
        print(page_count)
        try:
            print(review_url)
            review_count = totalreviews(review_url)
            print("totalreviews",review_count)
        except:
            review_count = 0

    for page_id in range(1,page_count):
        print(f'Running for page{page_id}')
        try:
            review_url=product_url.replace("/p/", "/product-reviews/") + "&page=" + str(page_id)
            print(review_url)
            extract_reviews(review_url)
        except Exception as e:
            print(e)
            pass

    df=pd.DataFrame(reviewlist)
    df.to_csv('flipkart_reviews.csv',mode='a',index=False)

# product_url="https://www.flipkart.com/ryme-combo-ying-yang-dream-catcher-five-rings-multi-attract-positive-dreams-decorative-showpiece-55-cm/p/itm160b7e33e0fd4?pid=SHIF96HSGQEKNDX8&fm=organic&ppt=dynamic&ppn=dynamic&ssid=t989af0e740000001666083668826"
review_url="https://www.flipkart.com/ryme-combo-ying-yang-dream-catcher-five-rings-multi-attract-positive-dreams-decorative-showpiece-55-cm/product-reviews/itm160b7e33e0fd4?pid=SHIF96HSGQEKNDX8&lid=LSTSHIF96HSGQEKNDX8EZZTDR&marketplace=FLIPKART"
# totalpages(review_url)
extract_reviews(review_url)