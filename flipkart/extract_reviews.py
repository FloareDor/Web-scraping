from base64 import decode
from encodings import utf_8
import requests
from pandas import *
import pandas as pd
from bs4 import BeautifulSoup
import random

reviewslist=[]
reqdf = read_csv('flipkart_url.csv')
tempdata=reqdf["URL"].tolist()
orgdata=set(tempdata)
newdata=list(orgdata)
df = pd.DataFrame(newdata)
df.to_csv('flipkart_set_url.csv',mode='a', index=False)


def extractReviews(reviewUrl, pageNumber,x):
    # revlist=[]
    resp = requests.get(reviewUrl)
    soup = BeautifulSoup(resp.text, 'html.parser')
    reviews = soup.findAll(('div', {'class':"col _2wzgFH K0kLPL"}))
    #print(reviews)
    #prevtitle=soup.find(('a', {'class':"_2rpwqI"}))
    #print(prevtitle)
    #print(req_titile)
    #print(reviews)

    for item in reviews:
        with open('outputs/file.html', 'w', encoding='utf-8') as f:
            f.write(str(item))
            # title=item['title']

        review = {
            'productTitle': (str(reviewUrl).split(".com/")[1]).split("product-reviews")[0],
            'Review Title': item.find('p', {'class':"_2-N8zT"}).text.strip(),
            'Rating': item.find('div', {'class': '_3LWZlK _1BLPMq'}).text.strip(),
            'Review Body': item.find('div', {'class': 't-ZTKy'}).find().text.strip() ,
        }
        
        print(len(review))
        reviewslist.append(review)  
    print("REVIEWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
    # print(f"appendeded for {x}th item of {pageNumber}th page")
    # return revlist

def totalPages(productUrl):
    resp = requests.get(productUrl)
    soup = BeautifulSoup(resp.text, 'html.parser')
    reviews = soup.find('div', {'class':"col"})
    counts = str(reviews.select("span"))
    return int(counts.strip().split(', ')[1].split(" ")[0].replace("<span>", ""))
    # review_count = 0
    # try:
    #     review_count = int(counts.strip().split(', ')[1].split(" ")[0].replace("<span>", ""))
    # except:
    #     pass
    # return review_count
    #for size in reviews:
    #    pagesize=size['span']
    #print(pagesize)
    

def main():
    #print("hi")
    # productUrl = "https://www.flipkart.com/crafts-world-welcome-our-home-wall-hanging-board-plaque-sign-room-decoration-decorative-showpiece/product-reviews/itm73e7a2d4bc678?pid=WDCG339E7HVAQHMH&lid=LSTWDCG339E7HVAQHMHGXUU7G&marketplace=FLIPKART"
    # print(totalPages(productUrl))
    # print("newdata",newdata[0],"newdata1",newdata[1])
    print("len",len(newdata))
    # len(newdata)//100
    for x in range(len(newdata)//10):
        productUrl=newdata[x]
        revlist=[]
        # print(productUrl)
        # productUrl = "https://www.amazon.in/Xtore-African-Beautiful-Uniquely-Crafted/dp/B08WL2RDBD/ref=sr_1_1"   
        reviewUrl = productUrl.replace("/p/", "/product-reviews/") + "&page=" + str(1)
        #print(reviewUrl)
        
        try:
            totalPg = totalPages(reviewUrl)
            print("totalpg",totalPg)
        except:
            totalPg=0
        # if totalPg > 0:
        for i in range(1,4):
            print(f"Running for REVIEW {i}")    
            try:
                reviewUrl = productUrl.replace("/p/", "/product-reviews/") + "&page=" + str(i)
                    # print(reviewUrl)
                extractReviews(reviewUrl, i)
                print("revlist",len(revlist))
                print("x",x,"i",i)
            except Exception as e:
                pass
                    #print("hiiiiiiiiiiiiiiiiiiiiiii",e)
                    # else:
                    #     pass
            
        print("xPAGEE",x)
        #print(revlist)
        df = pd.DataFrame(reviewslist)
        # revlist=revlist.clear
        
        df.to_csv('flipkart_Reviews.csv',mode='a', index=False)
        #print(x)

main()
# # totalPages("https://www.amazon.in/Xtore-African-Beautiful-Uniquely-Crafted/product-reviews/B08WL2RDBD/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")