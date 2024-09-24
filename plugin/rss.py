import feedparser
from plugin.base import Plugin
from datetime import datetime

GMT0800_FORMAT = "%a, %d %b %Y %H:%M:%S +0800"
UPDATE_TIME = "Thu, 18 Sep 2024 16:33:40 +0800"

_now_time: datetime = None

def calc_lerptime(strptime: datetime):
    global _now_time
    return (strptime - _now_time).total_seconds()

def rss_sort(item):
    dateStr = item["published"]
    date = datetime.strptime(dateStr, GMT0800_FORMAT)
    return (False, -date.timestamp())

class _RSSUrl:
    def __init__(self, plugin, url: str, seconds: int):
        self._plugin = plugin
        self._url = url
        self._seconds = seconds
        self._over = False

    def parse(self):
        feed = feedparser.parse(self._url)
        if feed.bozo == 0 or feed.bozo is False:
            entries = []
            # published = None
            for entry in feed.entries:
                seconds = self._plugin.calc_lerptime(datetime.strptime(entry.published, GMT0800_FORMAT))
                if seconds > 0:
                    entries.append({
                        "web_title": feed.feed.title,
                        "title": entry.title,
                        "link": entry.link,
                        "summary": entry.summary,
                        "published": entry.published
                    })
                else:
                    break

            # if published is not None:
            #     self._updateTimeStr = published
            #     self._nowTimeStruct = datetime.strptime(self._updateTimeStr, GMT0800_FORMAT)
                # self.setting()
            return entries
        return None

class RSSPlugin(Plugin):
    _nowTimeStruct: datetime
    _urls: list[_RSSUrl]

    def init(self):
        for i in range(len(self.history)):
            self.history[i]["id"] = i

        self._urls = []
        self._urls.append(_RSSUrl(self, "http://www.gcores.com/rss", 60*60*24))
        self._urls.append(_RSSUrl(self, "https://indienova.com/feed/", 60*60*24))
        self.refresh_item()

    def open(self):
        self.refresh_item()
        return self.config

    def close(self):
        pass

    @property
    def updatetime(self):
        return self.config["updatetime"]

    @property
    def history(self):
        return self.config["history"]

    @updatetime.setter
    def updatetime(self, value):
        self.config["updatetime"] = value

    def calc_lerptime(self, strptime: datetime):
        now_time = datetime.strptime(self.updatetime, GMT0800_FORMAT)
        return (strptime - now_time).total_seconds()

    def refresh_item(self):
        articles = []
        for p in self._urls:
            info = p.parse()
            if info is not None:
                articles.extend(info)

        # 将新的提要内容写入本地文件
        if len(articles) > 0:
            for item in articles:
                self.history.append(item)
                item["id"] = len(self.history)
            self.updatetime = datetime.now().strftime(GMT0800_FORMAT)
            self.save_config()
            print(f"RSS提要已保存, 拉取时间 {datetime.now().strftime(GMT0800_FORMAT)}")

    def config_default(self):
        return {
            "updatetime": UPDATE_TIME,
            "history": []
        }
