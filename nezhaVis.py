import csv

nickName = []
gender = []
cityName = []
content = ''


def read_csv():
    content = ''
    with open(r'nezha.csv', 'r', encoding='utf_8_sig', newline='') as file_test:
        reader = csv.reader(file_test)
        i = 0
        for row in reader:
            if i != 0:
                nickName.append(row[2])
                gender.append(row[5])
                cityName.append(row[1])
                content = content + row[6]
            i = i + 1
        print('一共有：' + str(i - 1) + '个')
        return content


import matplotlib.font_manager as fm
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']
from os import path

d = path.dirname(__file__)
stopwords_path = d + '/static/stopwords.txt'

from snapshot_phantomjs import snapshot
from pyecharts.render import make_snapshot


# 评论者性别分布可视化
def sex_distribution(gender):
    # print(gender)
    from pyecharts.charts import Pie
    from pyecharts import options as opts
    list_num = []
    list_num.append(gender.count('暂无'))  # 未知
    list_num.append(gender.count('1'))  # 男
    list_num.append(gender.count('2'))  # 女
    attr = ["其他", "男", "女"]
    data_pair = [list(z) for z in zip(attr, list_num)]
    pie = Pie().add(
        series_name="性别饼图",
        data_pair=data_pair,
        label_opts=opts.LabelOpts(is_show=False, position="center")
    )
    pie.render("sex_pie.html")
    make_snapshot(snapshot, "sex_pie.html", "sex_pie.png")


# 评论者所在城市分布可视化
def city_distribution(cityName):
    city_list = list(set(cityName))
    city_dict = {city_list[i]: 0 for i in range(len(city_list))}
    for i in range(len(city_list)):
        city_dict[city_list[i]] = cityName.count(city_list[i])
    # 根据数量(字典的键值)排序
    sort_dict = sorted(city_dict.items(), key=lambda d: d[1], reverse=True)
    city_name = []
    city_num = []
    for i in range(len(sort_dict)):
        city_name.append(sort_dict[i][0])
        city_num.append(sort_dict[i][1])

    import random
    from pyecharts.charts import Bar
    from pyecharts import options as opts
    bar = Bar().add_xaxis(city_name[0:20]).add_yaxis("城市人数", city_num[0:20]). \
        set_global_opts(title_opts=opts.TitleOpts(title="《哪吒之魔童降世》粉丝来源排行TOP20"),
                        visualmap_opts=opts.VisualMapOpts(min_=0,max_=1200))
    bar.render("city_bar.html")
    make_snapshot(snapshot, "city_bar.html", "city_bar.png")


content = read_csv()
sex_distribution(gender)
city_distribution(cityName)
