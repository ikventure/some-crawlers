"""
获取豆瓣电影top250的相关信息保存到csv文件中。
电影信息包括：电影名称、年份、评分、评价人数

"""


import requests
import re
import csv

# url = "https://movie.douban.com/top250"
ua = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}


def get_page(url):
    page = requests.get(url, headers=ua)
    page_source = page.text
    pat = re.compile(r'<div class="item">.*?<span class="title">(?P<name>.*?)</span>'
                     r'.*?<p class="">.*?<br>(?P<year>.*?)&nbsp'
                     r'.*?<span class="rating_num" property="v:average">(?P<rate>.*?)</span>'
                     r'.*?<span>(?P<number>.*?)人评价</span>', re.S)
    res = pat.finditer(page_source)
    page.close()
    return res


with open('db_movie_250.csv', 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    for start in range(0, 250, 25):
        douban_url = f'https://movie.douban.com/top250?start={start}&filter='
        result = get_page(douban_url)
        for item in result:
            dic = item.groupdict()
            dic['year'] = dic['year'].strip()
            csv_writer.writerow(dic.values())

print("over!")
