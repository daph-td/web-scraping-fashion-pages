from bs4 import BeautifulSoup
import requests
import csv 

# to find the content that we wanna scrape in one page
url = "https://scrapingclub.com/exercise/list_basic/?page=1"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
items = soup.find_all('div', class_= 'col-lg-4 col-md-6 mb-4')
# print(items)
# print('------')

# to write the output in a file
with open('fashion_web_scrap0.csv', 'w',  newline = '') as file_output:
    headers = ['Count', 'Item Price', 'Item Name']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    
    count = 1
    for i in items:
        itemName = i.find('h4', class_= 'card-title').text.strip('\n')
        itemPrice = i.find('h5').text
        print('%s ) Price: %s, Item Name: %s' % (count, itemPrice, itemName))
        #writer.writerow({headers[0]:count, headers[1]:itemPrice, headers[2]:itemName})
        count = count + 1

    # to replicate the scrape for multiple pages
    pages = soup.find('ul', class_ = 'pagination')

    # create a list of all pages
    urls = []
    links = pages.find_all('a', class_='page-link')
    for link in links:
        pageNum = int(link.text) if link.text.isdigit() else None
        if pageNum != None:
            x = link.get('href')
            urls.append(x)
    print(urls)
    count = 1
    for i in urls:
        newURL = url + i
        response = requests.get(newURL)
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all('div', class_= 'col-lg-4 col-md-6 mb-4')
        for i in items:
            itemName = i.find('h4', class_= 'card-title').text.strip('\n')
            itemPrice = i.find('h5').text
            print('%s ) Price: %s, Item Name: %s' % (count, itemPrice, itemName))
            writer.writerow({headers[0]:count, headers[1]:itemPrice, headers[2]:itemName})
            count = count + 1 

print('done')