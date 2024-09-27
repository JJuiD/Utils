import hashlib
from typing import Final
import feedparser
from flask import request
from module.base import DataConfig, DictConfig, ListConfig, ModuleBase
from datetime import datetime

from module.net import AppNet

GMT0800_FORMAT = "%a, %d %b %Y %H:%M:%S +0800"
UPDATE_TIME = "Thu, 18 Sep 2024 16:33:40 +0800"

_now_time: datetime = None

def calc_lerptime(strptime: datetime):
    global _now_time
    return (strptime - _now_time).total_seconds()

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

class _RSSUrl:
    def __init__(self, module, url: str, seconds: int):
        self._module = module
        self._url = url
        self._seconds = seconds
        self._over = False

    def parse(self):
        feed = feedparser.parse(self._url)
        if feed.bozo == 0 or feed.bozo is False:
            entries = []
            # published = None
            for entry in feed.entries:
                seconds = self._module.calc_lerptime(datetime.strptime(entry.published, GMT0800_FORMAT))
                if seconds > 0:
                    md5 = string_to_md5(entry.link)

                    rss_item = {
                        "web_title": feed.feed.title,
                        "title": entry.title,
                        "link": entry.link,
                        "published": entry.published,
                        "md5": md5,
                        "is_read": 0,
                        "summary": entry.summary,
                    }

                    if hasattr(entry, "comments"):
                        rss_item["comment"] = entry.comments

                    entries.append(rss_item)
                else:
                    break

            # if published is not None:
            #     self._updateTimeStr = published
            #     self._nowTimeStruct = datetime.strptime(self._updateTimeStr, GMT0800_FORMAT)
                # self.setting()
            return entries
        return None

RSSLimit: Final = 10


class RSSModule(ModuleBase):
    _nowTimeStruct: datetime
    _urls: list[_RSSUrl]

    _setting: DataConfig
    _history: ListConfig
    # _summary: DictConfig

    def init(self):
        self._urls = []
        self._urls.append(_RSSUrl(self, "http://www.gcores.com/rss", 60*60*24))
        self._urls.append(_RSSUrl(self, "https://indienova.com/feed/", 60*60*24))
        self._setting = DataConfig("setting", self.name, {
            "updatetime": UPDATE_TIME,
            "count": 0,
            "delete_read": 1
        })
        self._history = ListConfig("history", self.name, False, sort_f=rss_sort)

        AppNet.app.add_url_rule('/rss_page', self.get_history)
        # self._summary = DictConfig("summary", self.name, False)

        # test
        # self._setting.load()
        # self._history.load()
        # self._summary.load()

        # self.refresh_item()

    def open(self):
        print("open(self)", self.is_first)
        if self.is_first:
            self._setting.load()
            self._history.load()
            # self._summary.load()
        self.refresh_item()
        return

    def get_history(self):
        index = request.args.get('index', type=int)
        return self._history.load_part(index)

    def close(self):
        pass

    @property
    def updatetime(self):
        return self._setting.value("updatetime")

    @updatetime.setter
    def updatetime(self, value):
        self._setting.value("updatetime", value)

    def calc_lerptime(self, strptime: datetime):
        now_time = datetime.strptime(self.updatetime, GMT0800_FORMAT)
        return (strptime - now_time).total_seconds()

    def delete_item(self, key: str | int):
        # self._history.earse_filter(lambda item: item["md5"] != key)
        self._history.earse_filter(lambda item: item["md5"] != key)

    def get_item(self, key: str | int):
        first_item = self._history.next_filter(lambda item: item["md5"] == key)
        if first_item is not None:
            first_item["is_read"] = 1
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
        read_items = [item for item in self._history if item["is_read"]]

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
        for p in self._urls:
            info = p.parse()
            if info is not None:
                articles.append(info)

        # 将新的提要内容写入本地文件
        if len(articles) > 0:
            for items in articles:
                self._history.extend(items)

            self.prune_history()
            self._setting.value("count", len(self._history))
            # self._history.sort(rss_sort)
            self.updatetime = datetime.now().strftime(GMT0800_FORMAT)
            print(f"RSS提要已保存, 拉取时间 {datetime.now().strftime(GMT0800_FORMAT)}")

