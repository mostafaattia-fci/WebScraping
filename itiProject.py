import bs4
import requests
import xlsxwriter
from itertools import zip_longest
import csv

# url = 'https://forasna.com/a/%D9%88%D8%B8%D8%A7%D8%A6%D9%81-%D8%AA%D8%B3%D9%88%D9%8A%D9%82-%D9%88%D9%85%D8%A8%D9%8A%D8%B9%D8%A7%D8%AA-%D9%81%D9%89-%D9%85%D8%B5%D8%B1?a%5Bref%5D=bpnav'
url= "https://forasna.com/a/%D9%88%D8%B8%D8%A7%D8%A6%D9%81-%D8%AA%D9%83%D9%86%D9%88%D9%84%D9%88%D8%AC%D9%8A%D8%A7-%D9%85%D8%B9%D9%84%D9%88%D9%85%D8%A7%D8%AA-%D9%88%D8%A7%D8%AA%D8%B5%D8%A7%D9%84%D8%A7%D8%AA-%D9%81%D9%89-%D9%85%D8%B5%D8%B1?"
s = requests.Session()
r = s.get(url)
soup = bs4.BeautifulSoup(r.content, "html.parser")
# collect data
jobTitle = soup.findAll("h2", {"class": "job-title"})
companyName = soup.findAll("span", {"class": "company-name"})
location = soup.findAll("span", {"class": "location"})
# jobDetails = soup.findAll("div", {"class": "job-details"})
date = soup.findAll("span", {"class": "date date-desktop"})
page = soup.findAll("li", {"class": "hidden-xs"})


# lists for store data
tittleList = []
# requirementsList = []
companyList = []
locationList = []
dateList = []
links = []
pages = []
bsalaryList = []
links1 = []
for t in range(len(jobTitle)):
    tittleList.append(jobTitle[t].text.strip())
    links.append(jobTitle[t].find("a").attrs['href'])
    companyList.append(companyName[t].text.strip())
    locationList.append(location[t].text.strip())
    dateList.append(date[t].text.strip())



# collect data from other page
for link in links:
    results = requests.get(link)
    srcs = results.content
    soups = bs4.BeautifulSoup(srcs, "html.parser")
    baseSalary = soups.find("span", {"itemprop": "baseSalary"}).parent
    bsalaryList.append(baseSalary.get_text(strip=True))

for p in range(len(page)-1):
    pages.append(page[p].find("a").attrs['href'])
# loops for multiple pages
for pg in range(len(pages)):
    s = requests.Session()
    r = s.get(pages[pg])
    soups = bs4.BeautifulSoup(r.content, "html.parser")
    # collect data
    jobTitle1 = soups.findAll("h2", {"class": "job-title"})
    companyName1 = soups.findAll("span", {"class": "company-name"})
    location1 = soups.findAll("span", {"class": "location"})
    date1 = soups.findAll("span", {"class": "date date-desktop"})
    # store data
    for t in range(len(jobTitle1)):
        tittleList.append(jobTitle1[t].text.strip())
        links1.append(jobTitle1[t].find("a").attrs['href'])
        companyList.append(companyName1[t].text.strip())
        locationList.append(location1[t].text.strip())
        dateList.append(date1[t].text.strip())
# collect salary
for linkk in range(len(links1)):
    results = requests.get(links1[linkk])
    srcs1 = results.content
    soups = bs4.BeautifulSoup(srcs1, "html.parser")
    baseSalary1 = soups.find("span", {"itemprop": "baseSalary"}).parent
    bsalaryList.append(baseSalary1.get_text(strip=True))


workbook = xlsxwriter.Workbook('projectiti.xlsx')
worksheet = workbook.add_worksheet()

my_dict = {'Job Title': tittleList,
           'Company Name': companyList,
           'Location': locationList,
           'Date': dateList,
           'Base Salary': bsalaryList

           }

col_num = 0
for key, value in my_dict.items():
    worksheet.write(0, col_num, key)
    worksheet.write_column(1, col_num, value)
    col_num += 1

workbook.close()
