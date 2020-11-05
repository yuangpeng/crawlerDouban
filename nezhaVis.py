import csv

time = []
nickName = []
gender = []
cityName = []
userLevel = []
score = []
content = ''


def read_csv():
    content = ''
    # 读取文件内容
    with open(r'G:\maoyan\maoyan.csv', 'r', encoding='utf_8_sig', newline='') as file_test:
        # 读文件
        reader = csv.reader(file_test)
        i = 0
        for row in reader:
            if i != 0:
                time.append(row[0])
                nickName.append(row[1])
                gender.append(row[2])
                cityName.append(row[3])
                userLevel.append(row[4])
                score.append(row[5])
                content = content + row[6]
            # print(row)
            i = i + 1
        print('一共有：' + str(i - 1) + '个')
        return content
