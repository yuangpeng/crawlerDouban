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
boxofMonth = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


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
            dateofMovie.append(readDate(nameofMovie[i]))
        pattern = re.compile('<p class=\\"totalnum\\"><strong>(.*?)</strong>(亿|万)</p>', re.S)
        boxofMovie = pattern.findall(text)
        for i in range(len(dateofMovie)):
            money = float(boxofMovie[i][0])
            if boxofMovie[i][1] == "亿":
                money = money * 10000
            boxofMonth[dateofMovie[i]] = boxofMonth[dateofMovie[i]] + money


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
    xaxisMonth = ["Jan.", "Feb.", "Mar.", "Apr.", "May.", "June", "July", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]
    del boxofMonth[0]
    bar = (
        pyecharts.charts.Bar()
            .add_xaxis(xaxisMonth)
            .add_yaxis("各月电影数量", numofMonth, yaxis_index=1)
            .extend_axis(yaxis=opts.AxisOpts(name="各月电影数量", type_="value", min_=0, max_=150, position="right",
                                             axislabel_opts=opts.LabelOpts(formatter="{value} 部")))
            .extend_axis(yaxis=opts.AxisOpts(type_="value", name="各月电影票房", min_=0.0, max_=1200000.0, position="left",
                                             axislabel_opts=opts.LabelOpts(formatter="{value} 万元"),
                                             splitline_opts=opts.SplitLineOpts(
                                                 is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                                             )))
            .set_global_opts(tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"))
    )
    barBox = (
        pyecharts.charts.Bar()
            .add_xaxis(xaxisMonth)
            .add_yaxis(
            "各月电影票房",
            boxofMonth,
            yaxis_index=2,
            label_opts=opts.LabelOpts(is_show=False),
        )
    )
    bar.overlap(barBox)
    grid = pyecharts.charts.Grid()
    grid.add(bar, opts.GridOpts(pos_left="20%", pos_right="20%"), is_control_axis_index=True)
    grid.render("date_box.html")


if __name__ == "__main__":
    main()
