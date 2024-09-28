import feedparser


# feed = feedparser.parse("http://www.ruanyifeng.com/blog/atom.xml")
feed = feedparser.parse("http://www.gcores.com/rss")

if feed.bozo == 0 or feed.bozo is False:
    # published = None
    for entry in feed.entries:
        if hasattr(entry, "comments"):
            pass

data = []

print(data[0]["value"] if len(data) > 0 else "11111111")

# import requests

# # 替换为你的 FeedBurner URL
# feedburner_url = 'http://www.ruanyifeng.com/blog/atom.xml'

# try:
#     response = requests.get(feedburner_url)
#     response.raise_for_status()  # 检查请求是否成功
#     # 输出 feed 内容
#     print(response.text)

# except requests.exceptions.RequestException as e:
#     print(f'请求错误: {e}')
