from base64 import decode
from encodings import utf_8
import requests
from pandas import *
import pandas as pd
from bs4 import BeautifulSoup
import random

reviewlist=[]
reqdf = read_csv('amazon_url.csv')
tempdata=reqdf["product_URL"].tolist()
orgdata=set(tempdata)
newdata=list(orgdata)
df = pd.DataFrame(newdata)
df.to_csv('amazon_set_url.csv',mode='a', index=False)

def extractReviews(reviewUrl, pageNumber,x,revlist):
    # revlist=[]
    resp = requests.get(reviewUrl)
    soup = BeautifulSoup(resp.text, 'html.parser')
    reviews = soup.findAll('div', {'data-hook':"review"})
    # print(reviews)
    for item in reviews:
        with open('outputs/file.html', 'w', encoding='utf-8') as f:
            f.write(str(item))
        try:
            review = {
                'productTitle': soup.title.text.replace("Amazon.in:Customer reviews: ", "").strip(),
                'Review Title': item.find('a', {'data-hook':"review-title"}).text.strip(),
                'Rating': item.find('i', {'data-hook': 'review-star-rating'}).text.strip(),
                'Review Body': item.find('span', {'data-hook': 'review-body'}).text.strip() ,
            }
        # print(review)
            revlist.append(review)
        except:
            return -1
    print("appendeded for xth item of ith page",x,pageNumber)
    return revlist

def totalPages(productUrl):
    resp = requests.get(productUrl)
    soup = BeautifulSoup(resp.text, 'html.parser')
    reviews = soup.find('div', {'data-hook':"cr-filter-info-review-rating-count"})
    return(int(reviews.text.strip().split(', ')[1].split(" ")[0]))

def main():
    # productUrl = "https://www.amazon.in/Its-Trending-Wood-handcrafts-Beautiful/dp/B07VLT3V1G/ref=sr_1_4"
    print("newdata",newdata[0],"newdata1",newdata[1])
    print("len",len(newdata))
    # len(newdata)//100
    for x in range(len(newdata)):
        productUrl=newdata[x]
        revlist=[]
        # print(productUrl)
        # productUrl = "https://www.amazon.in/Xtore-African-Beautiful-Uniquely-Crafted/dp/B08WL2RDBD/ref=sr_1_1"   
        reviewUrl = productUrl.replace("dp", "product-reviews") + "?pageNumber=" + str(1)
        try:
            totalPg = totalPages(reviewUrl)
            print("totalpg",totalPg)
        except:
            totalPg=0

        for i in range(1,totalPg):
            print(f"Running for page {i}")      
            try: 
                reviewUrl = productUrl.replace("dp", "product-reviews") + "?pageNumber=" + str(i)
                print(reviewUrl)
                x = extractReviews(reviewUrl, i,x,revlist)
                if x!=-1:
                    revlist = x
                else:
                    break
                print("revlist",len(revlist))
                print("x",x,"i",i)
            except Exception as e:
                print(e)
            
        print("x",x)
        
        df = pd.DataFrame(revlist)
        revlist=revlist.clear
        df.to_csv('amazon_Reviews.csv',mode='a', index=False)
        # print(x)

main()
#print(totalPages("https://www.amazon.in/JH-Gallery-Hangings-Decoration-showpiece/product-reviews/B0B7XQJ8TQ/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"))
# totalPages("https://www.amazon.in/Xtore-African-Beautiful-Uniquely-Crafted/product-reviews/B08WL2RDBD/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")