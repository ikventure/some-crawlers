"""
该版本为使用线程池优化后的版本，速度相对较快。

根据晋江小说的novelid和需要爬取的起始和终止章节，保存这些章节的评论信息
评论信息包括：评论id、评论楼层、评论用户名、发表时间、章节id、评论内容

访问晋江评论库不需要购买章节，可以随机找一本
以该链接为例， http://www.jjwxc.net/onebook.php?novelid=2697774
novelid = 2697774
获取 1-88章评论

"""
import time

import requests
import re
import csv
from concurrent.futures import ThreadPoolExecutor


# http://www.jjwxc.net/onebook.php?novelid=2697774
novelid = int(input("请输入novelid：")) # 2697774

chapter_start = int(input("请输入起始章节：")) # 1
chapter_end = int(input("请输入终止章节：")) # 88

headers_dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}


# 获取html页面代码
def getHTMLpage(url):
    page = requests.get(url, headers=headers_dict)
    page.close()
    page.encoding = "gb18030"
    return page


# 获取某一章的评论页数
def get_summary(page):
    pattern1 = re.compile(r"共有<span class='redtext'>(?P<comment_count>\d+)</span>条评论，"
                          r"分<span class='redtext'>(?P<page_count>\d+)</span>页", re.S)
    result = pattern1.search(page.text)
    return int(result.group("page_count"))


# 获取评论相关信息
def get_re_result(page):
    pattern2 = re.compile(r'data-commentid="(?P<comment_id>.*?)"'
                          r'.*?<span class="coltext">.*?№(?P<comment_floor>\d+).*?网友'
                          r'.*?target="_blank">(?P<user_name>.*?)</a></span>'
                          r'.*?发表时间：(?P<comment_time>.*?)&nbsp'
                          r'.*?所评章节：.*?data-chapterid="(?P<chapter_id>.*?)">'
                          r'.*?mormalcomment_.*?>(?P<content>.*?)</span>', re.S)
    result = pattern2.finditer(page.text)
    return result


# 将一章评论写入一个csv文件中
def data_to_csv(chapter_id, page_id=1):
    url_chap = f"https://www.jjwxc.net/comment.php?novelid={novelid}&chapterid={chapter_id}&page=1"
    page1 = getHTMLpage(url_chap)
    # 跳过被锁定章节
    try:
        page_count = get_summary(page1)
    except AttributeError:
        print(f'chapter {chapter_id:03} is locked.')
        return
    # 章节不存在或者评论数为0时，跳过
    if page_count == 0:
        print(f'chapter {chapter_id:03} does not exists.')
        return

    with open(f'.\\comments\\{novelid}_chapter{chapter_id:03}_comments.csv', 'w', encoding="utf-8", newline='') as f:
        fieldnames = ["comment_id", "comment_floor", "user_name", "comment_time", "chapter_id", "content"]
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writeheader()

        while page_id <= page_count:
            page_url = f"https://www.jjwxc.net/comment.php?novelid={novelid}&chapterid={chapter_id}&page={page_id}"
            page2 = getHTMLpage(page_url)
            comments = get_re_result(page2)
            for comment in comments:
                dic = comment.groupdict()
                csv_writer.writerow(dic)
            page_id += 1
        print(f'chapter {chapter_id:03} comments have been saved.')


if __name__ == '__main__':
    start_time = time.perf_counter()
    with ThreadPoolExecutor(50) as t:
        for chapter in range(chapter_start, chapter_end + 1):
            t.submit(data_to_csv, chapter)
    end_time = time.perf_counter()
    print(f"All comments have been saved. Time Used: {end_time - start_time}s")


'''
测试输出用
for comment in comments:
    dic = comment.groupdict()
    comment_id = dic["comment_id"]
    comment_floor = dic["comment_floor"]
    user_name = dic["user_name"]
    comment_time = dic["comment_time"]
    chapter_id = dic["chapter_id"]
    content = dic["content"]
    print(comment_id, comment_floor, user_name, comment_time, chapter_id, content)
'''

