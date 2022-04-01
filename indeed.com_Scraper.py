# import module
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
# user define function
# Scrape the data
# and get in string
def getdata(url):
    r = requests.get(url)
    return r.text

# Get Html code using parse
def html_code(url):
    # pass the url
    # into getdata function
    htmldata = getdata(url)
    soup = BeautifulSoup(htmldata, 'html.parser')

    # return html code
    return (soup)

def find_next_page(soup):
    try:
        pagination = soup.find("a", {"aria-label": "Next"}).get("href")
        return "https://in.indeed.com" + pagination
    except AttributeError:
        return None

def company_data(soup):
    # find the Html tag
    # with find()
    # and convert into string

    job_title = []
    for item in (soup.find_all("div", class_="heading4 color-text-primary singleLineTitle tapItem-gutter")):
        job_title.append(item.find_all("span")[-1].get_text())



    comp_name = []
    for item in soup.find_all("div", class_="heading6 company_location tapItem-gutter companyInfo"):
        for i in item.find_all("span", class_ = "companyName"):

            comp_name.append(i.get_text())
    print(comp_name)




    location = []
    for item in soup.find_all("div", class_="heading6 company_location tapItem-gutter companyInfo"):
        for i in item.find_all("div", class_="companyLocation"):
            location.append((i.get_text()))

    print(location)

    job_des = []
    for item in soup.find_all("div", class_="job-snippet"):
        job_des.append(item.text.strip())

    print(job_des)



    salary = []
    c = 0
    for i in soup.find_all("td", class_ = "resultContent"):
        if len((i.find_all("div", class_ = "metadata salary-snippet-container"))) != 0:
            salary.append(i.find_all("div", class_ = "metadata salary-snippet-container")[0].get_text().strip())
        else:
            salary.append("Not Available")

    print(salary)


    links = []
    link = soup.find_all("div", id = "mosaic-provider-jobcards")
    for i in link:
        for j in (i.find_all('a')):
            links.append("https://in.indeed.com" + j.get("href"))
    print(links)



    df = pd.DataFrame(columns=["comp_name", "job_title", "location", "job_des", "salary", "link"])


    for i in range (len(job_title)):
        print("Company Name and Address : " + comp_name[i])
        print("Job : " + job_title[i])
        print(("Location: " + location[i]))
        print("Job Description: " + job_des[i])
        print("Salary: " + salary[i])
        print("Job Link: " + links[i])
        print("-----------------------------")
        row = [comp_name[i], job_title[i], location[i], job_des[i], salary[i],links[i]]
        df.loc[len(df)] = row
    df.to_csv('Indeed_Scraper1.csv', mode="a", header=False, index=False)



    return (comp_name)

if __name__ == "__main__":

    # Data for URL
    url = "https://in.indeed.com/jobs?q=freshers&fromage=1&sort=date"

    # Pass this URL into the soup
    # which will return
    # html string

    while True:
        print(url)
        soup = html_code(url)
        com_res = company_data(soup)
        url = find_next_page(soup)

file = pd.read_csv("Indeed_Scraper1.csv")
file.to_csv("Indeed_Scraper1.csv", header = ["Company Name", "Job Title", "Location", "Job Description", "Salary", "Link"], index = False)
