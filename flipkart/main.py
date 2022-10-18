import requests
import openpyxl
from bs4 import BeautifulSoup



excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'Page 1'


page_url = "https://www.flipkart.com/search?q=handicraft&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1"

page2 = requests.get(page_url) #this gets all the data from the url
doc2 = page2.content  #doc stores all the content of the page
soup2 = BeautifulSoup(doc2,'html.parser')  # soup now has all the html code of the file

got_links=[] #a list to store all the links


string = "https://www.flipkart.com" #the links we get only store after the flipkart.com so need this as to call the link

links = soup2.find_all(["a"],class_="s1Q9rs")  #this goes to the class and finds all the 'a' tags
for i in links:
    got_links.append(string+i['href']) 


for url in got_links: #iterates for each item
    page = requests.get(url)
    doc = page.text
    soup = BeautifulSoup(doc,'html.parser')



    title = soup.find(["span"],class_="B_NuCI").get_text()
    over_all_rating = soup.find(["div"],class_="_3LWZlK")
    if over_all_rating == None:
        over_all_rating = "NULL"
    else:
        over_all_rating = over_all_rating.get_text() #gives a list as ['851', 'Ratings', '&', '100', 'Reviews']



    number_reviews = soup.find(["span"],class_="col-12-12")
    if number_reviews == None:
        number_reviews = 0
    else:
        number_reviews = (number_reviews.get_text())
        #gives a list as ['851', 'Ratings', '&', '100', 'Reviews']

    insert = []

    new_url = url.replace("/p/", "/product-reviews/" ) #to shift to the reviews page


    page1 = requests.get(new_url) 
    doc1 = page1.text  
    soup1 = BeautifulSoup(doc1,'html.parser')  

    temp=soup1.find_all("div",{ "class" : "col _2wzgFH K0kLPL"})

    insert=[url, title, over_all_rating,]

    for temp in (soup1.find_all("div",{ "class" : "col _2wzgFH K0kLPL"})) :

        # just add the indi_comment page here to get all the comments instead of ones on the first page
        
        rating = temp.find("div",{ "class" : "_3LWZlK _1BLPMq"}) #rating
        heading = temp.find("p",{ "class" : "_2-N8zT"}).get_text() #Heading 
        comments = temp.find("div",{"class" : "t-ZTKy"}).get_text() #Comments
        comments = comments.removesuffix('READ MORE')
        update = ""
        if rating == None:
            bad_rating = temp.find("div",{ "class" : "_3LWZlK _1rdVr6 _1BLPMq"})
            if bad_rating == None:
                bad_rating = "NULL"
            else:
                bad_rating = bad_rating.get_text()
            update = update + (bad_rating) +"-"
        else:
            update = update + (rating.get_text()) +"-"
        
        update = update + (heading) +"-"
        update = update + (comments)
        insert.append(update)

    sheet.append(insert)


Excel_page_name = input("Enter the name of the excel sheet here: ")
excel.save(Excel_page_name+".xlsx") 