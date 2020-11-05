import xlrd
import pyecharts
from snapshot_phantomjs import snapshot
from pyecharts.render import make_snapshot
from pyecharts import options as opts

rate = []
rateNum = []
for i in range(0, 101):
    rate.append(1.0 * i / 10)
    rateNum.append(0)

movieExcel = xlrd.open_workbook("2019movies.xls")
table = movieExcel.sheet_by_index(0)
rateMovies = table.col_values(2)
for i in range(len(rateMovies)):
    rateMovies[i] = float(rateMovies[i])
    rateMovies[i] = int(rateMovies[i] * 10)
    rateNum[rateMovies[i]] = rateNum[rateMovies[i]] + 1

bar = (
    pyecharts.charts.Bar()
        .add_xaxis(rate)
        .add_yaxis("各评分电影数量", rateNum)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(visualmap_opts=opts.VisualMapOpts(min_=0, max_=60))
)

bar.render("Rate.html")
make_snapshot(snapshot, "Rate.html", "Rate.png")

make_snapshot(snapshot, "date_box.html", "date_box.png")
