#This code will get the url links of all the pages
import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.flipkart.com/search?q=handicraft&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

page = requests.get(url) 
doc = page.content  
soup = BeautifulSoup(doc,'html.parser')

got_links = []
string = "www.flipkart.com"

max_page = soup.find(["div","span"],class_="_2MImiq").get_text() # gets the main body text

max_page = max_page.removesuffix('12345678910Next')  
max_page = max_page.removeprefix("Page 1 of ")
max_page = int(max_page.replace(',', '')) # the variable max_page has the total number of pages


for i in range(1,3): # replace 3 with max_page+1 
    try:
        url = "https://www.flipkart.com/search?q=handicraft&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="+str(i)
        page = requests.get(url) 
        doc = page.content  
        got_links=[]
        soup = BeautifulSoup(doc,'html.parser')
        string = "https://www.flipkart.com" 
        links = soup.find_all(["a"],class_="s1Q9rs") 
        for j in links:
            got_links.append([string+j['href']])  
        print("done "+str(i))
    except:
        print("")

    if (i== 26):
        break



fields = ['URL'] 
filename = "flipkart_url.csv"

with open(filename, 'w') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(fields) 
    csvwriter.writerows(got_links)





