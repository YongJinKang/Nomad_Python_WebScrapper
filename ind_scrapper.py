import requests
from bs4 import BeautifulSoup

LIMIT = 50

def get_last_page(url):
    try:
        result = requests.get(url)
        
        soup = BeautifulSoup(result.text,'html.parser')
        
        pagination = soup.find("div",{"class":"pagination"})

        links = pagination.find_all('a')
        
        pages=[]
        for page in links[:-1]:
            pages.append(int(page.find("span").string))   
        
        max_page = pages[-1]
        
        return max_page
    except:
        print('Error: get_last_page_num')
        return 0


def extract_job(html):
    
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span",{"class": "company"})

    try:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
        company = company.strip()
    except:
        print("there is no company name")

    location = html.find("span",{"class": "location accessible-contrast-color-location"})
    if location is not None :
        location = str(location.string)
        location = location.strip()
    else:
        None


    job_id = html["data-jk"]
            
    return {'title': title, 'company' : company, 'location' : location, 'link' : f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}"}

        



def extract_jobs(last_page,url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed page {page}")
        result = requests.get(f"{url}&start={page*LIMIT}")
#     result = requests.get(f"{URL}&pg={0+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class" : "jobsearch-SerpJobCard"})   
        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs

def get_jobs(word):
    url = f"https://kr.indeed.com/jobs?q={word}&limit={LIMIT}&radius=25"
    last_page = get_last_page(url)
    jobs=extract_jobs(last_page,url)

    return jobs

    
# last_page = get_last_page()

# extract_jobs(last_page)

# get_jobs()


    




    