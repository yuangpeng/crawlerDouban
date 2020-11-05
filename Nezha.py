import time
import random
import requests
from Douban import userAgents
import csv, os
import pandas as pd


class Spidermaoyan():
    headers = {"User-Agent": random.choice(userAgents)}

    def __init__(self, url, time):
        self.url = url
        self.time = time

    def get_json(self):
        response = requests.get(self.url, headers=self.headers)
        a = response.text
        js = response.json()["cmts"]
        return js

    def get_data(self, json_response):
        print(len(json_response))
        list_info = []
        for data in json_response:
            cityName = data["cityName"]
            content = data["content"]
            if "gender" in data:
                gender = data["gender"]
            else:
                gender = 0
            nickName = data["nickName"]
            userLevel = data["userLevel"]
            score = data["score"]
            list_one = [self.time, nickName, gender, cityName, userLevel, score, content]
            list_info.append(list_one)
        print(list_info)
        self.file_do(list_info)

    def file_do(self, list_info):
        file_size = os.path.getsize(r'nezha.csv')
        if file_size == 0:
            name = ['评论日期', '评论者昵称', '性别', '所在城市', '猫眼等级', '评分', '评论内容']
            file_test = pd.DataFrame(columns=name, data=list_info)
            file_test.to_csv(r'nezha', encoding='utf_8_sig', index=False)
        else:
            with open(r'nezha.csv', 'a+', encoding='utf_8_sig', newline='') as file_test:
                writer = csv.writer(file_test)
                writer.writerows(list_info)


def spider_maoyan():
    offset = 0
    startTime = '2019-07-26'
    day = [26, 27, 28, 29, 30, 31, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
           24, 25, 26]
    j = 0
    page_num = int(20000 / 15)
    for i in range(page_num):
        comment_api = 'http://m.maoyan.com/mmdb/comments/movie/1211270.json?_v_=yes&offset={0}&startTime={1}' \
            .format(offset, startTime)
        s0 = Spidermaoyan(comment_api, startTime)
        json_comment = s0.get_json()
        if json_comment["total"] == 0:
            if j < 6:
                startTime = '2019-07-%d' % day[j]
            elif j >= 6 and j < 32:
                startTime = '2019-08-%d' % day[j]
            else:
                break
            offset = 0
            j = j + 1
            continue
        s0.get_data(json_comment)
        offset = offset + 15
        time.sleep(1)


if __name__ == '__main__':
    spider_maoyan()
