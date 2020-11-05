from pyecharts import options as opts
from pyecharts.charts import Scatter
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot
import xlrd

rateAna = []

movieExcel = xlrd.open_workbook("cmtsAnalysis.xlsx")
table = movieExcel.sheet_by_index(0)
rateMovies = table.col_values(6)
posNeg = table.col_values(8)
gay = table.col_values(9)
data = []

for i in range(1, 20000):
    if posNeg[i] == "negative":
        gay[i] = -1 * float(gay[i])
    data.append([float(rateMovies[i]), gay[i]])

data.sort(key=lambda x: x[0])
x_data = [d[0] for d in data]
y_data = [d[1] for d in data]
sct = (
    Scatter()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(series_name="", y_axis=y_data, symbol_size=2, label_opts=opts.LabelOpts(is_show=False))
        .set_series_opts()
        .set_global_opts(title_opts=opts.TitleOpts(title='评分-情感置信度'),
                         xaxis_opts=opts.AxisOpts(
                             type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
                         ),
                         yaxis_opts=opts.AxisOpts(
                             type_="value",
                             axistick_opts=opts.AxisTickOpts(is_show=True),
                             splitline_opts=opts.SplitLineOpts(is_show=True),
                         ),
                         tooltip_opts=opts.TooltipOpts(is_show=False),
                         )
)
sct.render("rate_emo.html")
make_snapshot(snapshot, "rate_emo.html", "rate_emo.png")
