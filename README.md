# some-crawlers
some small crawlers for personal use

### douban_movie_top250.py
获取豆瓣电影top250的相关信息保存到csv文件中。
电影信息包括：电影名称、年份、评分、评价人数

### jjwxc_comments.py(单线程)
根据晋江小说的novelid和需要爬取的起始和终止章节，保存这些章节的评论信息
评论信息包括：评论id、评论楼层、评论用户名、发表时间、章节id、评论内容

### jjwxc_comments_ThreadPool.py(多线程)
根据晋江小说的novelid和需要爬取的起始和终止章节，保存这些章节的评论信息
评论信息包括：评论id、评论楼层、评论用户名、发表时间、章节id、评论内容

### pearvideo_downloader.py
输入梨视频网页地址，下载该地址视频