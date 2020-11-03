import requests
from bs4 import BeautifulSoup


# movie class
class movieInfo:
    name = ""
    rate = 0.0
    releaseTime = ""
    length = 0
    boxOffice = 0.0
    star = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


moviesInfo = []


# Download html from "https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=2019"
# return string of html text
def downloadHTML():
    url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=20&year_range=2019,2019"
    print("crawl html : " + url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise Exception(f"downloadHTML() {r.status_code} errors!")
    print(r.text)
    return r.text


# parse single html text from "https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=2019"
# return movieInfo class
def parseHTML(html):
    soup = BeautifulSoup(html, "html.parser")
    movieList = soup.find("div", attrs={"class", "list-wp"})
    for movie in movieList.find_all('a'):
        name = movie.find("span", attrs={"class", "title"})
        rate = movie.find("span", attrs={"class", "rate"})


downloadHTML()
