# -----------------------------------------------------------------------
# date_box.py
# release date visualization
# box visualization
# -----------------------------------------------------------------------
from pyecharts import options as opts
import pyecharts
import xlrd
from Douban import userAgents
import random
import requests
import re

numofMonth = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
boxofMonth = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def getBox():
    headers = {"User-Agent": random.choice(userAgents)}
    for num in range(10):
        url = f'http://www.mtime.com/boxoffice/?year=2019&area=china&type=MovieRankingYear&category=all&page={num}&display=list&timestamp=1604328420337&version=07bb781100018dd58eafc3b35d42686804c6df8d&dataType=json'
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise Exception(f"getBox() {r.status_code} errors! In the {num} pages!")
        text = r.json()["html"]

        pattern = re.compile('title=\\"(.*?)/', re.S)
        nameofMovie = pattern.findall(text)
        dateofMovie = []
        for i in range(len(nameofMovie)):
            if readDate(nameofMovie[i]) != 0:
                dateofMovie.append(readDate(nameofMovie[i]))
            else:
                print(nameofMovie[i])
        pattern = re.compile('<p class=\\"totalnum\\"><strong>(.*?)</strong>(亿|万)</p>', re.S)
        boxofMovie = pattern.findall(text)
        a = 1


def readDate(nameofMovie):
    workbook = xlrd.open_workbook("2019movies.xls")
    table = workbook.sheet_by_index(0)
    rowNum = table.nrows
    for i in range(rowNum):
        if nameofMovie == table.row(i)[0].value:
            return int(table.row(i)[3].value[5:7])
    return 0


# read month from 2019movies.xls
def readExcel():
    movieExcel = xlrd.open_workbook("2019movies.xls")
    table = movieExcel.sheet_by_index(0)
    dates = table.col_values(3)
    for i in range(0, len(dates)):
        if dates[i] == 0.0:
            dates[i] = "00"
            continue
        if dates[i] == "0":
            dates[i] = "00"
            continue
        if dates[i][0:4] == "2020":
            dates[i] = "00"
            continue
        if dates[i][4] == "(":
            dates[i] = "00"
            continue
        dates[i] = dates[i][5:7]
    for i in range(len(dates)):
        mon = int(dates[i])
        numofMonth[mon - 1] = numofMonth[mon - 1] + 1


def main():
    getBox()
    readExcel()
    xaxisMonth = ["Jan.", "Feb.", "Mar.", "Apr.", "May.", "June", "July,", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]
    bar = (
        pyecharts.charts.Bar()
            .add_xaxis(xaxisMonth)
            .add_yaxis("各月电影数量", numofMonth)
            .set_colors(['#FF6400'])
            .set_global_opts(title_opts=opts.TitleOpts(title="Correlation"))
    )
    bar.render()


if __name__ == "__main__":
    main()
