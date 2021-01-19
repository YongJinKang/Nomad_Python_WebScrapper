import requests
from bs4 import BeautifulSoup


#  페이지 가져오기
def get_last_page(url):
    try:
        result = requests.get(url)
        soup = BeautifulSoup(result.text,"html.parser")

        pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
        
        last_page= pages[-2].get_text(strip=True)
        
        return int(last_page)
    except:
        print('Error: get_last_page_num')
        return 0

# 직무, 회사, 지역, 구인링크 가져오기

def extract_job(html):
    title = html.find("div", {"class": "grid--cell fl1 "}).find("h2").find("a")["title"]
    company, location = html.find("div", {"class": "grid--cell fl1 "}).find("h3").find_all("span",recursive=False)
    company = company.get_text(strip=True).strip("\n")
    location = location.get_text(strip=True).strip("-").strip("\n").strip("\r")
    
    job_id = html["data-jobid"]
    link = f"https://stackoverflow.com/jobs/{job_id}"
    return {'title' : title, 'company' : company, 'location' : location, 'link' : link}


# 모든 페이지의 모든 항목의 데이터(직무, 회사 지역, 구인링크) 모으기

def extract_jobs(last_page, url):
    jobs = []
#     result = requests.get(f"{URL}&pg={0+1}")
    
    
    for page in range(last_page):
        print(f"Scrapping SO page {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class" : "-job"})   
        
        for result in results:
#           print(result["data-jobid"])
            job = extract_job(result)
            jobs.append(job)
        
    return jobs


        
    

#word를 받아야겠지 ?
def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}&sort=i"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs

# 마지막 페이지 출력
# last_page = get_last_page()

# 데이터 뽑기
# extract_jobs(last_page)

#다 합친 함수
# get_jobs()