import hashlib
from typing import Final
import feedparser
from flask import request
from module.base import DataConfig, DictConfig, ListConfig, ModuleBase
from datetime import datetime

from module.net import AppNet

GMT0800_FORMAT: Final = "%a, %d %b %Y %H:%M:%S +0800"
ISO8601_FORMAT: Final = "%Y-%m-%dT%H:%M:%SZ"
UPDATE_TIME: Final = "Thu, 18 Sep 2024 16:33:40 +0800"

# _now_time: datetime = None

# def calc_lerptime(strptime: datetime):
#     global _now_time
#     return (strptime - _now_time).total_seconds()

def rss_sort(item):
    dateStr = item["published"]
    date = datetime.strptime(dateStr, GMT0800_FORMAT)
    # return (False, -date.timestamp())
    return -date.timestamp()

def string_to_md5(input_string: str):
    # 创建一个 md5 哈希对象
    md5_hash = hashlib.md5()

    # 更新哈希对象，必须将字符串编码为字节
    md5_hash.update(input_string.encode('utf-8'))

    # 获取十六进制表示的哈希值
    return md5_hash.hexdigest()

class _RSSParse:
    def __init__(self, module, data):
        self._module = module
        # self._url = url
        self._data = data
        # self._over = False

    @property
    def url(self):
        return self._data["url"]

    @property
    def time_format(self):
        return self._data["time_format"]

    @property
    def content_get(self):
        return self._data["content"]

    def check_parse(self):
        pass

    def calc_lerptime(self, strptime: datetime):
        feed_time = datetime.strptime(self._module.feeds[self.url], GMT0800_FORMAT)
        return (strptime - feed_time).total_seconds()

    def parse(self) -> list:
        pass

class _FeedParser(_RSSParse):
    def parse(self):
        entries = []
        feed = feedparser.parse(self.url)
        if feed.bozo == 0 or feed.bozo is False:
            # published = None
            for entry in feed.entries:
                published_datetime = datetime.strptime(entry.published, self.time_format)
                seconds = self.calc_lerptime(published_datetime)
                if seconds > 0:
                    md5 = string_to_md5(entry.link)

                    rss_item = {
                        "web_title": feed.feed.title,
                        "title": entry.title,
                        "link": entry.link,
                        "published": published_datetime.strftime("%Y年%m月%d日 %H:%M:%S"),
                        "id": md5,
                        "is_read": 0,
                        # "summary": entry.summary,
                    }
                    rss_item["comment"] = self.content_get(entry)

                    # if hasattr(entry, "comments"):
                    #     rss_item["comment"] = entry.comments

                    entries.append(rss_item)
                else:
                    break

            # if published is not None:
            #     self._updateTimeStr = published
            #     self._nowTimeStruct = datetime.strptime(self._updateTimeStr, GMT0800_FORMAT)
                # self.setting()
        return entries


RSSLimit: Final = 50
RSSFeedUrls: Final = [
    {
        # "cls": _FeedParser,
        "url": "http://www.gcores.com/rss",
        "lerp_time": 60*60*24,
        "time_format": GMT0800_FORMAT,
        "content": lambda entry: entry.summary
    },
    {
        # "cls": _FeedParser,
        "url": "https://indienova.com/feed/",
        "lerp_time": 60*60*24,
        "time_format": GMT0800_FORMAT,
        "content": lambda entry: entry.content[0]['value'] if len(entry.content) > 0 else None
    },
    {
        # "cls": _FeedParser,
        "url": "http://www.ruanyifeng.com/blog/atom.xml",
        "lerp_time": 60*60*24,
        "time_format": ISO8601_FORMAT,
        "content": lambda entry: entry.content[0]['value'] if len(entry.content) > 0 else None
    }
]

RSSFeedTime: Final = {}

for data in RSSFeedUrls:
    RSSFeedTime[data["url"]] = UPDATE_TIME

class RSSModule(ModuleBase):
    _nowTimeStruct: datetime
    _urls: list[_RSSParse]

    _setting: DataConfig
    _history: ListConfig
    # _summary: DictConfig

    def init(self):
        self._urls = []
        for data in RSSFeedUrls:
            self._urls.append(_FeedParser(self, data))
        # self._urls.append(_FeedParser(self, "https://indienova.com/feed/", 60*60*24))
        # self._urls.append(_FeedBurner(self, "http://feeds.feedburner.com/ruanyifeng", 60*60*24))
        self._setting = DataConfig("setting", self.name, {
            "feeds": RSSFeedTime,
            "updatetime": UPDATE_TIME,
            "count": 0,
            "delete_read": 1
        })

        self._history = ListConfig("history", self.name, True)

        # self._summary = DictConfig("summary", self.name, False)

        # test
        # self._setting.load()
        # self._history.load()
        # self._summary.load()

        # self.refresh_item()

    def open(self):
        if self.is_first:
            self._setting.load()
            self._history.load()
            # self._summary.load()
        self.refresh_item()
        return

    def get_history(self, index):
        return self._history.items

    def close(self):
        pass

    @property
    def feeds(self):
        return self._setting.value("feeds")

    @property
    def updatetime(self):
        return self._setting.value("updatetime")

    @updatetime.setter
    def updatetime(self, value):
        self._setting.value("updatetime", value)

    # def calc_lerptime(self, strptime: datetime):
    #     now_time = datetime.strptime(self.updatetime, GMT0800_FORMAT)
    #     return (strptime - now_time).total_seconds()

    def delete_item(self, key: str | int):
        # self._history.earse_filter(lambda item: item["md5"] != key)
        self._history.earse_filter(lambda item: item["id"] != key)
        self._history.save()

    def get_item(self, key: str | int):
        first_item = self._history.next_filter(lambda item: item["id"] == key)
        if first_item is not None:
            first_item["is_read"] = 1
            self._history.save()
        # item = self._history.get(key)
        # if item is not None:
        #     item["is_read"] = 1
        return first_item

    def on_app_quit(self):
        self._setting.save()
        self._history.save()

    def prune_history(self):
        if len(self._history) < RSSLimit:
            return

        # 优先删除已读的内容
        read_items = [item for item in self._history if item["is_read"] == 1]

        # 删除已读内容
        while len(self._history) > RSSLimit and len(read_items) > 0:
            oldest_read = min(read_items, key=lambda item: item["published"])
            self._history.remove(oldest_read)
            # self._history.earse_key(oldest_read["md5"])
            read_items.remove(oldest_read)

        # 如果仍然超过最大长度，按时间远到近删除
        while len(self._history) > RSSLimit:
            oldest_item = min(self._history, key=lambda item: item["published"])
            self._history.remove(oldest_item)
            # self._history.earse_key(oldest_item["md5"])

    def refresh_item(self):
        articles = []
        now_time = datetime.now().strftime(GMT0800_FORMAT)
        for p in self._urls:
            info = p.parse()
            if len(info) > 0:
                articles.append(info)
                self.feeds[p.url] = now_time

        # 将新的提要内容写入本地文件
        if len(articles) > 0:
            for items in articles:
                self._history.extend(items)

            self.prune_history()
            self._setting.value("count", len(self._history))
            # self._history.sort(rss_sort)
            self.updatetime = now_time

            self._setting.save()
            self._history.save()
            print(f"RSS提要已保存, 拉取时间 {now_time}")

