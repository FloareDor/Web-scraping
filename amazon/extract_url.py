from itertools import product
from time import sleep
import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
from requests_html import HTMLSession



reviewlist = []
productlist=[]

pTitle=[]
stringw="https://www.amazon.in"
numberofpages="s-pagination-item s-pagination-disabled"

producturl_string="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"


def extractitems(page_url,pagenumber,prodlist):
    resp=requests.get(page_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    products = soup.findAll('a', {'class':producturl_string})
    print(soup)
    # productRating=soup.findAll('span', {'class':"a-icon-alt"})
    # print(resp,"\n")
    # print(soup,"\n")
    # print(products,"\n")
    # print(page_url)
    print("length",len(products))
    # for items in productRating:
    #     ratingtext=items.getText()
    #     Rating.append(ratingtext)
    # print("length",type(products))
    for item in products:
        with open('outputs/file.html', 'w', encoding='utf-8') as f:
            f.write(str(item))
        # productUrl = item['href']
        inter_product_Url = item['href']
        productUrl = "".join((stringw, inter_product_Url))

        product={
            # 'product_Title': product_Title,
            # 'product_Rating':productRating,
            'product_URL':productUrl
        }
        prodlist.append(product)  
    return prodlist
        # print(productlist)


def totalPages(productUrl):
    resp = requests.get(productUrl)
    soup = BeautifulSoup(resp.text, 'html.parser')
	# reviews = soup.find('div', {'data-hook':"cr-filter-info-review-rating-count"})
    # return int(reviews.text.strip().split(', ')[1].split(" ")[0])
    counter=soup.find('span',{'class':numberofpages})
    value = 0
    try:
        value=counter.text.strip()
    except:
        pass
    return(int(value))

def main():
    productUrl = "https://www.amazon.in/s?k=handicraft&i=kitchen&rh=n%3A976442031&dc"
    products_Url = productUrl + "&page=" +str(1) 
    # itemdetails("https://www.amazon.in/eCraftIndia-Gemstone-Studded-Brass-Handicraft/dp/B076473RYB/ref=sr_1_1_sspa?keywords=handicraft&qid=1665765334&qu=eyJxc2MiOiI4LjQ1IiwicXNhIjoiNy43MyIsInFzcCI6IjQuNTcifQ%3D%3D&s=kitchen&sr=1-1-spons&psc=1")
    prodlist=[]
    # Rating=[]

    totalPg = totalPages(products_Url)
    # totalPg=400
    print(totalPg)

    for i in range(15):
    # for i in range(10):
        print(f"Running for page {i}")

        
        sleep(3)
        
        try: 
            products_Url = productUrl.replace("dp", "product-reviews") + "&page=" + str(i)
            # print(products_Url)
            prodlist=extractitems(products_Url, i,prodlist)
            # print(len(prodlist))
        except Exception as e:
            print(e)        

    df = pd.DataFrame(prodlist)
    df.to_csv('amazon_url.csv',index=False)
    



main()
# totalPages("https://www.amazon.in/s?k=handicraft&i=kitchen&rh=n%3A976442031&dc&page=2&qid=1665765334&ref=sr_pg_1")


 