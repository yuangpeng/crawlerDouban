import xlrd
import pyecharts
from snapshot_phantomjs import snapshot
from pyecharts.render import make_snapshot
from pyecharts import options as opts

names = ["哪吒之魔童降世", "流浪地球", "复仇者联盟4：终局之战", "我和我的祖国", "中国机长", "疯狂的外星人", "飞驰人生", "烈火英雄", "少年的你", "速度与激情：特别行动"]
box = [49.19, 46.40, 41.91, 30.24, 28.52, 21.92, 17.09, 16.76, 15.42, 14.07]

bar = (
    pyecharts.charts.Bar()
        .add_xaxis(names)
        .add_yaxis("票房", box)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 20}))
)

bar.render("10box.html")

make_snapshot(snapshot, "10box.html", "10box.png")