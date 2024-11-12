import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
word = input("enter the firm category in arabic: ")
def extract(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    html_content = response.content       # html_content is the page content (el doc )
    soup = BeautifulSoup(html_content, "lxml")
    company_divs = soup.find_all('div',{'class':'row-fluid tablcom0'})
    return company_divs    # return all the page divs(components) so the output will be input in transform method
    # print(len(company_divs))   -> each page has 20 company_div
main_list = []
def transform(company_divs):
    domain_name= 'https://www.140online.com/'
    for div in company_divs:
        company_name_href_link = div.find("h3",{"class":"tith3"}).a['href']
        company_full_path = domain_name + company_name_href_link
        company_page_response = requests.get(company_full_path)
        company_page_html_content = company_page_response.content
        company_page_soup = BeautifulSoup(company_page_html_content,'lxml')
        name = company_page_soup.find('h3',{'class':'tithenamcomp'}).text.strip()
        co_info = company_page_soup.find('div',{"class":"span12"}).find_all('table',{"class":"tabrcom"})[1] # get the second table in that list which represent the co_info 
        address_span = co_info.find_all('tr')[0].find_all('td')[1].find('span',{"id":"ctl09_lblAddress"})   
        if address_span:
            address = address_span.text.strip()
        else:
            address = ''
        phone_row = co_info.find('tr',{"id":"ctl09_BranchSec"})
        if phone_row:
            phone = phone_row.find_all('td')[1].text.strip()
        else:
            phone = ''
        company_info = {
            'company_name':name,
            'company_phone': phone,
            'company_address': address
        } 
        main_list.append(company_info)
    """the last update is i finally got the name,phone and address, and compacted them into dictionary
        so the remaining is to make a function to get info and make a loop on this function by the page numbers"""
def load():
    df = pd.DataFrame(main_list)
    df.to_csv('E:/Python/140_Online/قطع-غيار_word_extracted_data.csv', index=False,encoding='utf-8-sig')

for pageNum in range(1,6):   # till 10 pages only each page has 20 divs
    url_pattern = f"https://www.140online.com/result.aspx?c=0&a=0&txt={word}&Page={pageNum}" # this is a pattern for the organization categories[مصنع ,مدرسة ,صالات رياضية]
    extra_urls = {
            'fright_url' : f"https://www.140online.com/class/pages/111/{word}/{pageNum}",
            'furniture_url' : f"https://www.140online.com/class/pages/{word}/{pageNum}",
            'gym_url' : f"https://www.140online.com/Class/125/{word}/{pageNum}",
            'pipeline_url' : f'https://www.140online.com/class/pages/224/{word}/{pageNum}',
            "paper_url" : f"https://www.140online.com/Class/pages/603/{word}/{pageNum}"
    }
    print(f"Extracting Data Now From page_{pageNum}")
    divs = extract(url_pattern)    
    transform(divs)
load()
print(f"Total Rows {len(main_list)} are Extracted Successfully and Saved In CSV.\nGOOD JOB")
# We used here real practice on ETL Tool 
# 1- Extracting data from website
# 2- Transforming data into structured format
# 3- Loading data into CSV file
# we are in need for logical error handling!!!!!!!!!!!!!!!!