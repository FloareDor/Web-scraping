#this is the code that just gets all the reviews of each item in the form of rating-heading-comment

import requests
import openpyxl
from bs4 import BeautifulSoup

url1_indi = "https://www.flipkart.com/dinine-craft-wooden-2-pocket-key-holder-wall-home-decor-decorative-showpiece-6-cm/product-reviews/itmb6135a09b4d7d?pid=SHIGG8J7VQ7BHUYK&lid=LSTSHIGG8J7VQ7BHUYKODYETT&marketplace=FLIPKART"
#the link is the same as the product page only the key word "/product-reviews/" needs to be added in between
page_01 = requests.get(url1_indi)
doc_01 = page_01.text
soup_01 = BeautifulSoup(doc_01,'html.parser')

string = "https://www.flipkart.com"
pages = soup_01.find_all(["a"],class_="ge-49M") # this finds the links of all the possible pages the comment section can have

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'Page 1'

insert = [] #this is used to append to the excel sheet

for i in pages:
    url = string+i['href']
    page = requests.get(url)
    doc = page.text
    soup = BeautifulSoup(doc,'html.parser')

    for temp in (soup.find_all("div",{ "class" : "col _2wzgFH K0kLPL"})) :
        rating = temp.find("div",{ "class" : "_3LWZlK _1BLPMq"}) #positive rating
        heading = temp.find("p",{ "class" : "_2-N8zT"}).get_text() #Heading 
        comments = temp.find("div",{"class" : "t-ZTKy"}).get_text() #Comments
        comments = comments.removesuffix('READ MORE')
        update = ""
        if rating == None: #the negative rating is stored in the below class
            bad_rating = temp.find("div",{ "class" : "_3LWZlK _1rdVr6 _1BLPMq"})
            if bad_rating == None:
                bad_rating = "NULL"
            else:
                bad_rating = bad_rating.get_text()


            update = update + (bad_rating) +"-"
        else: #the positive rating gets fixed here
            update = update + (rating.get_text()) +"-"
        
        update = update + (heading) +"-" #merging all the attributes to a single string
        update = update + (comments)
        insert.append(update) #inseting into the list



sheet.append(insert)

sheet_name = input("Enter the excel sheet file name(No Spaces): ")
excel.save(sheet_name+".xlsx") #change the excel sheet name

