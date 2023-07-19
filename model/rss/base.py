import json
import os
from datetime import datetime
from threading import Thread
from time import sleep

import feedparser

from easy.idler import IdlerList
from easy.user_default import UserDefault
from model.base import Model
from view.rss import RSSView


# "http://www.zhihu.com/rss"
# NewsFeed = feedparser.parse("http://www.gcores.com/rss")
#
# entry = NewsFeed.entries[1]
#
# print(entry)

GMT0800_FORMAT = '%a, %d %b %Y %H:%M:%S +0800'
UPDATE_TIME = "Thu, 13 Jul 2023 02:16:42 +0800"

class RSSUrl:
	def __init__(self, key, url, seconds):
		self._key = key
		self._url = url
		self._seconds = seconds
		self._over = False
		self._updateTimeStr = UserDefault.value("rss/updatetime")
		if self._updateTimeStr is None:
			self._updateTimeStr = UPDATE_TIME
		self._nowTimeStruct = datetime.strptime(self._updateTimeStr, GMT0800_FORMAT)
	# def setting(self):
	# 	UserDefault.setValue("rss/" + self._key, self._updateTimeStr)
	def calcLerpTime(self, strptime):
		return (strptime - self._nowTimeStruct).total_seconds()
	def parse(self):
		feed = feedparser.parse(self._url)
		if feed.bozo == 0:
			entries = []
			published = None
			for entry in feed.entries:
				seconds = self.calcLerpTime(datetime.strptime(entry.published, GMT0800_FORMAT))
				if seconds > 0:
					entries.append({
						"web_title": feed.feed.title,
						"title": entry.title,
						"link": entry.link,
						"summary": entry.summary,
						"published": entry.published,
					})
					if published is None:
						published = entry.published
				else:
					break

			if published is not None:
				self._updateTimeStr = published
				self._nowTimeStruct = datetime.strptime(self._updateTimeStr, GMT0800_FORMAT)
				# self.setting()
			return entries
		return None

urls = [
	["gcores", "http://www.gcores.com/rss", 60*60*24]
]

HistoryFile = "rss_history"
RssTimeLerp = 5

def RSSGet(self):
	while self.threadRun:
		self.refresh()
		sleep(RssTimeLerp)

def rssSort(item):
	dateStr = item["published"]
	date = datetime.strptime(dateStr, GMT0800_FORMAT)
	return -date.timestamp()
	# return  (date, item["id"]) 相同使用id进行排序
	# return (-date.timestamp(), item["id"]) 降序

class RSS_(Model):
	Name = "rss"
	ViewClass = RSSView
	def init(self):
		global urls
		self.urlGet = []

		for url in urls:
			self.urlGet.append(RSSUrl(url[0], url[1], url[2]))

		urlArticles = []
		if os.path.exists(HistoryFile):
			with open(HistoryFile, 'r', encoding='utf-8') as file:
				urlArticles = json.load(file)
		self.urlArticles = IdlerList(urlArticles, sort=rssSort)

		self.thread = Thread(target=RSSGet, args=[self], name="RSSGet")
		self.threadRun = True
		self.thread.start()
	def refresh(self):
		articles = []
		for p in self.urlGet:
			info = None
			try:
				info = p.parse()
			except Exception as e:
				print("rss get parse error ", str(e))

			if info is not None:
				articles.extend(info)

		# 将新的提要内容写入本地文件
		if len(articles) > 0:
			self.urlArticles.extend(articles)
			self.urlArticles.sort()
			with open(HistoryFile, 'w+', encoding='utf-8') as file:
				json.dump(self.urlArticles.json(), file, indent=4)
				UserDefault.setValue("rss/updatetime", datetime.now().strftime(GMT0800_FORMAT))
			print(f"RSS提要已保存到 {HistoryFile}, 拉取时间 {datetime.now().strftime(GMT0800_FORMAT)}")
	def exit(self):
		self.threadRun = False

		# feedList = []
		# for url in urls:
		# 	newsFeed = feedparser.parse(url)
		# 	feedList.append(newsFeed)
		# return feedList

# RSS2.0 image的子元素列表
# url     图片的url      必备
# title     图片的标题，用于http的alt属性      必备
# link     网站的url(实际中常以频道的url代替)      必备
# width     图片的宽度(象素为单位) 最大144,默认88     可选
# height     图片的高度(象素为单位) 最大400，默认31     可选
# description     用于link的title属性      可选
#
# RSS2.0  cloud的子元素列表
#
# domain     Cloud程序所在机器的域名或IP地址   radio.xmlstoragesystem.com
# port     访问clound程序所通过的端口   80
# path     程序所在路径（不一定是真实路径）   /RPC2
# registerProcedure     注册的可提供的服务或过程   xmlStorageSystem.rssPleaseNotify
# protocol     协议 xml-rpc, soap , http-post 之一  xml-rpc
#
# RSS2.0元素channel的子元素textInput的子元素列表
# title     Submit按钮的标签      必备
# description     解释text输入区      必备
# name     Text area对象的名字      必备
# link     处理提交的请求的cgi程序      必备

# {
# 	'title': '试译：异世界诞生2006',
# 	 'title_detail': {'type': 'text/plain', 'language': None, 'base': 'https://www.gcores.com/rss',
# 					  'value': '试译：异世界诞生2006'},
# 	 'links': [{'rel': 'alternate', 'type': 'text/html', 'href': 'https://www.gcores.com/articles/167389'}],
# 	 'link': 'https://www.gcores.com/articles/167389',
# 	 'summary': '<img src="https://image.gcores.com/11d3111336dcf3e0f180f1b429eca028-1305-734.jpg?x-oss-process=image/resize,limit_1,m_fill,w_626,h_292/quality,q_90" /><p>  </p><div>\n<div>\n<figure><img alt="岛田文惠：“那孩子能做这样的吗？”岛田千佳：“啊？你在说什么呀？”片山吉方：“有那么严重吗……？”" src="https://image.gcores.com/0bfd969900c74a557a56923a7f900a76-2724-1922.jpg?x-oss-process=image/resize,limit_1,m_lfit,w_700,h_2000/quality,q_90/watermark,image_d2F0ZXJtYXJrLnBuZw,g_se,x_10,y_10" /><figcaption>(岛田文惠：“那孩子能做这样的吗？”岛田千佳：“啊？你在说什么呀？”片山吉方：“有那么严重吗……？”)</figcaption></figure><figure><img alt="随着烟雾散去，怪物一下子就被吹飞了出去。骑士夏露娜：““勇者贵史，刚才那招究竟是什么？”勇者贵史：“刚才那是火药。我自己做的。”在这个没发明出火药的异世界里，火药可是十分强大的武器。" src="https://image.gcores.com/add4106ea5face59083a1aebb3ec5efc-2724-1922.jpg?x-oss-process=image/resize,limit_1,m_lfit,w_700,h_2000/quality,q_90/watermark,image_d2F0ZXJtYXJrLnBuZw,g_se,x_10,y_10" /><figcaption>(随着烟雾散去，怪物一下子就被吹飞了出去。骑士夏露娜：““勇者贵史，刚才那招究竟是什么？”勇者贵史：“刚才那是火药。我自己做的。”在这个没发明出火药的异世界里，火药可是十分强大的武器。)</figcaption></figure><figure><img alt="“勇者贵史啊，你就到此为止了。你难道以为魔炮沾了水就用不了了吗？”“不不不，不是水，而是热水哦。你知道受热膨胀吗？”——魔佣兵阿姆斯特朗一开魔炮，魔炮便爆炸了。勇者贵史凭借着取得模拟考试县内第二十一位好成绩的头脑打败了他。大魔术师兰斯洛特公主：“不愧是贵史！真聪明！”" src="https://image.gcores.com/9047441d126f1a654b514b1a6dab441e-2724-1922.jpg?x-oss-process=image/resize,limit_1,m_lfit,w_700,h_2000/quality,q_90/watermark,image_d2F0ZXJtYXJrLnBuZw,g_se,x_10,y_10" /><figcaption>(“勇者贵史啊，你就到此为止了。你难道以为魔炮沾了水就用不了了吗？”“不不不，不是水，而是热水哦。你知道受热膨胀吗？”——魔佣兵阿姆斯特朗一开魔炮，魔炮便爆炸了。勇者贵史凭借着取得模拟考试县内第二十一位好成绩的头脑打败了他。大魔术师兰斯洛特公主：“不愧是贵史！真聪明！”)</figcaption></figure>\n</div></div><p>作者：伊藤ヒロ</p><p>插图：やすも</p><h1>序章</h1><p>亲爱的儿子：</p><p>我是妈妈。最近身体还好吗？</p><p>自从你去往异世界，已经过去很久了。</p><p>在那里住的还舒服吗？还在冒险的旅途中吗？还是说，你已经打败了魔王，和大家一起快乐地生活？果然还是开了后宫了？</p><p>你一向喜欢小巧的女孩子，所以妈妈才担心你会不会被小女孩欺负，像是摆出师傅架子的萝莉BBA啦，奴隶市场买来的兽人女孩啦。一定要和同龄的正宫女主角也好好相处呀。</p><p>这边的大家都过得很好。</p><p>你妹妹明年要升初中了。初中的时候你成绩很好，所以我常常想，如果你还在家的话，就能辅导妹妹学习了。</p><p>还记得吗？全国模拟考试的时候你在县里是第二十一名。亲戚们都说，我家的儿子头脑比谁都好。</p><p>如今你一定也借着这股聪明，在那边的世界参加民主选举，或者发明蛋黄酱和黑火药之类的东西吧。毕竟，你是我最骄傲的儿子。</p><p>昨天，片山先生（或许是个你不想听见的名字）又来家里拜访了。</p><p>片山先生他每个月都来家里向你道歉。他也和我约好了，以后会一直把工资的一部分交给我作为补偿。</p><p>你一直是个温柔的孩子，所以，你说不定早就原谅他了。</p><p>但我是个没用的母亲。直到今天，那天发生的事我都不能接受。</p><p>尽管我其实不想要他的钱，也不想再看到他带来的标着银行记号的信封，因为这些根本弥补不了什么，但是害死我儿子的卡车司机就这样一直辛苦下去吧、总之想要他在佛坛前磕头，这样的想法也渐渐消失了。</p><p>现在我只在乎你在异世界过的好不好。</p><p>但是你一定是因为忙于冒险和内政，这次也没法回信吧。虽然很遗憾，但是没办法。</p><p>等到异世界变得和平，你闲下来的时候，一定要记得写信给妈妈呀。</p><p>最后，一定要注意身体，千万不要逞强。也一定要注意车辆。</p><p>你的妈妈</p><p>附：我已经和你爸爸离婚了。</p><p>  </p><h1>第一话 母亲文惠，和异世界转生</h1><p>公元2006年4月下旬——。距离那天已过去一年。</p><p>此处为某县地N市，是个小城市。急行列车在此处铁道停留。因此即便没有家用汽车，也能借助公交网络方便地出行。最近便利店和家庭餐厅也多了起来。在郊外，佳世客（大型商场）也挨着电影院开办了起来。</p><p>手机也是各个运营商的都能用。虽然据说在县内还有不少地方只能用docomo这家运营商的电话。总而言之，此处虽然称不上大都市，倒也可算作一个生活方便的地方。</p><p>在这样一座城市中的一隅，建着一座不起眼的商品房。其中传来这样的声音。</p><p>“妈妈，晚饭不要再做三人份的了！”</p><p>晚上七点，正上小学六年级的、十一岁的岛田千佳在吃晚饭时向母亲说着这样的话。</p><p>我们家的晚饭应该是两人份的。只要有我和妈妈的就足够了。</p><p>这几个月来，父亲都没怎么回过家，和母亲几乎是分居的状态。母亲尽管想要隐瞒，女儿千佳却还是知道了父母私底下办理的离婚。</p><p>——不过话说回来，从很久以前开始，父亲就一直很晚才回家。从小时候开始，一家人在平日里一起吃晚饭在记忆中就一次也没有过。</p><p>这么看来，母亲准备的第三份晚餐并不是为了爸爸。</p><p>那么就是为哥哥准备的了。</p><p>是为一年前去世的哥哥岛田贵史准备的。</p><p>“不是说好了要省钱吗？晚餐做三人份地也太浪费了吧！”</p><p>一如既往的话。少女每天都重复着同样的话。特别是知道了父母离婚的事后，少女的语气变得更加尖锐。</p><p>当她一如既往地责备母亲后，母亲文惠也果然一如既往地回答道：</p><p>“对不起……但是我感觉那孩子说不定就会突然回来。”</p><p>今天的晚饭是炸鸡块和番茄沙拉。</p><p>千佳最近有些在意起体重来。话虽如此，她和平均水平比起来还要偏瘦些。这只是这个年纪的女孩特有的过度节食的倾向。因此她昨天刚刚说过，她不想吃这样的油炸食品和碳水化合物。</p><p>但是，这份菜单是哥哥的最爱。</p><p>即便是挑食的哥哥，面对这份菜单也会难得地大加赞赏、要求再来一份。</p><p>“——也就是说，妈妈不是为了自己，而是为了不在的哥哥准备的晚饭。”</p><p>千佳这么想着，渐渐有些生气，表情也变得严峻起来。</p><p>“千佳，生气了吗……？”</p><p>“……没有。”</p><p>这是谎言。并不是“没有”。千佳正生气。</p><p>“对不起啊，千佳。对不起啊……我今天早上梦到那孩子了……然后，过了白天，去买东西的时候，天空一下子就变蓝了——我就想起来以前，那孩子还小的时候，看到了这样的天空我就会和他一起去散步……我以为这一定是预示着他就要回家了。”</p><p>“你是笨蛋吗？”</p><p>千佳可以理解母亲看到同样的景色就想起哥哥的事。虽然还在读小学六年级，千佳却有着大人般的性格。因此她并没有幼稚到不能理解母亲的伤感。</p><p>但是，千佳还是不明白为什么这是“回家的预兆”。</p><p>因此，千佳生气的原因又多了一个。</p><p>“我说啊，妈妈真的希望哥哥回来吗？明明是那样的哥哥！明明是那样的哥哥！”</p><p>听到女儿的话，母亲只是低着头，沉默着。</p><p>虽然因为角度的原因看不清楚，母亲大概在哭泣。千佳也有些后悔自己的发言，不管怎么说都讲得太过分了。</p><p>毕竟，岛田文惠，虽然是母亲，却仍是个脆弱的女人。</p><p>这就是所谓的“演歌系”吧。世间所谓男人们，一直被女性的脆弱和梦幻感所吸引。这也就意味着，她会如那饱受风吹日晒的柔弱花朵一般，激发起男人们强烈的保护欲。</p><p>可是如今，文惠业已遭丈夫抛弃，身心却还是脆弱如故。无论何事何物，总该有个限度吧。</p><p>这样的女人在同性之中总是遭人厌恶，文惠也不例外。千佳虽然身为女儿，面对母亲时，无论她做了什么说了什么，也总是陷入一种无可奈何的焦躁情绪。</p><p>“——居然为了那样的哥哥，每天这副样子。”。</p><p>千佳紧皱眉头，一言不发地吃着晚饭，还没吃完一半就匆匆回到自己的房间。当然，这也是一如既往。</p><p>不知花了多少时间，文惠一个人把剩下的晚餐吃完了。</p><p>十一岁的少女千佳仰面躺在儿童房的床上，向着天花板吐露心中的不满。</p><p>“啊啊，真是的！受不了了！”</p><p>虽然多少有些令人意外，但千佳并不怨恨自己的父亲。</p><p>在常人看来，舍弃了这样的妻子可谓不人道，将这样的母亲丢给女儿照顾更称得上是恶行。</p><p>但是，千佳已经是六年级的学生了。她多少理解，所谓夫妻，终究还是男女关系的延申。</p><p>因此，千佳能理解父亲的心情。如果自己是丈夫，恐怕也不想回到这样忧郁的女人的身边。</p><p>千佳暗自想到，聪明得不彻底，不如彻底不聪明。或许自己身为孩子便不该表示出对父母的理解，反倒是表现得更加任性一些会更好。</p><p>像班上的男生们那样，做一个能对着“便便”“秃子”这样的词哈哈大笑的孩子的话，就没有这些烦恼了吧。</p><p>（……关于妈妈的事情，我得做点什么才行啊。）</p><p>千佳有些瞧不起自己的母亲。虽说如此，倒也不是真的厌恶她。</p><p>果然这就是母女间感情的体现吧。</p><p>“正因为是孩子才不能逃离父母”，千佳如此开导自己。她是个聪明的少女，能在头脑中快速转变情绪。总之——</p><p>（非得做点什么才行……。首先就这样做吧。）</p><p>对于千佳而言，虽然母亲在做的事无论哪件都让她难以接受，但都还是勉强忍受下来了。</p><p>唯独一件事是例外。</p><p>唯独母亲最近在夜里做的那件事是例外。</p><p>在月光也显得如此耀眼的深夜零点。</p><p>岛田文惠最近开始产生了一个兴趣。主要是在去世的儿子的房间里啪嗒啪嗒地敲响键盘。</p><p>……啪嗒、啪嗒、啪嗒……。</p><p>“——我的erzi，rujin在异世界快乐生huo。”</p><p>她正在写着业余小说。</p><p>这是一本关于少年在幻想世界里旅行的轻小说。</p><p>深夜，当现实世界已陷入沉寂后，文惠用着儿子遗留下的台式电脑，一个字一个字地，啪嗒啪嗒地敲打着键盘……。</p><div>\n<figure><img alt="" src="https://image.gcores.com/2c6bf18da60aea679f66bfbbfb1da7b8-1299-1824.jpg?x-oss-process=image/resize,limit_1,m_lfit,w_700,h_2000/quality,q_90/watermark,image_d2F0ZXJtYXJrLnBuZw,g_se,x_10,y_10" /></figure></div><p></p><p><span style="font-weight: bold;">连载小说《我的儿子，如今在异世界快乐生活》</span></p><p><span style="font-style: italic;">“贵史呀，你还没有死。你会作为异世界的勇者活下去。”</span></p><p><span style="font-style: italic;">女神温柔的声音直接传入贵史的脑海。</span></p><p><span style="font-style: italic;">被卡车撞倒后的贵史一醒来便发现自己在一个陌生的地方。</span></p><p><span style="font-style: italic;">“这里是……？我明明被卡车撞了呀。”</span></p><p><span style="font-style: italic;">眼前都是贵史没见过的风景。可是，他还是不知道这里是哪里。</span></p><p><span style="font-style: italic;">“这里难道是幻想世界吗？”</span></p><p><span style="font-style: italic;">这不是在做梦。就像那位女神说的那样。</span></p><p><span style="font-style: italic;">待续</span></p><p>  </p><h1>第二话 母亲文惠，和原卡车司机</h1><p>西历2006年。世界迈入新世纪已过去了五年。</p><p>这是一个总觉得有些空虚的时代。新世纪的风景，既不是幻想中的“梦中的未来社会”，也不是“核战争后的废土世界”。——可以说，人们是以一种逃避的姿态生活在这个所谓的“零零年代”（西历2000年到2010年的十年间）。</p><p>话虽如此，科技从九十年代开始便稳步向前发展。得益于此，像N市这样的小城市里，因特网、个人电脑和移动电话也普及开来。世界确确实实地发生了变化。</p><p>在这个不平衡的时代里，某个春日午后，以下的故事发生了。</p><p>岛田千佳正走在从小学回家的路上。在家附近，她看到一个熟悉的身影。</p><p>“欸，那不是片山先生吗？”</p><p>那人的名叫片山吉方。</p><p>他还是位二十岁出头、气质有些柔弱的青年。听到背后传来的声音后，他发出“哇！”的一声，明显吃惊的有些过头，直跳起来，几乎就要从原地飞走了。</p><p>面对这样一个做出漫画中才会出现的反应的男人，千佳一时手足无措，愣在原地。</p><p>“吓了我一跳。你，你好啊，千佳。”</p><p>“才不是你好吧！你在这里干嘛？在我家附近鬼鬼祟祟的。”</p><p>这位青年简直就像间谍或是小偷那样，躲在电线杆后的阴影里偷看千佳她们家，活脱脱一个可疑分子形象。</p><p>“你这下总算要被警察抓走了吧？这次要被送进看守所了吧？上次是缓刑来着。”</p><p>“你也太严厉了吧……其实，我想着去一趟你家来着。”</p><p>“来我家？为什么？前几天不是才来过？”</p><p>“该怎么说呢……”不知为何，片山开始吞吞吐吐起来。</p><p>“其实我从之前的公司辞职了。毕竟发生了那样的事。以后我会在一家电脑公司工作。这次是想来报告一下这件事。”</p><p>“这也没什么必要吧。我妈妈对这种事情没什么兴趣。”千佳虽然这么回答着，却也明白这位青年是出于诚意才辞职的。还是不要说“别来”这种话为好，她暗自想到。</p><p>“片山先生，你最好还是别说新工作是有关电脑的工作。像我妈妈这个年纪的人，总是会就觉得那是一种轻松的活。还是和她说是要做一些更辛苦的工作更好哦。”</p><p>“啊，我明白了。那个，还有一件事——”</p><p>“还有什么事？”</p><p>看他这说话吞吞吐吐的样子，恐怕报告要换工作这事只是个借口，其实他还另有所图。</p><p>片山用比之前更加吞吞吐吐的语气，认真地说出了所谓的“另一件事”：</p><p>“那个、之前见面的时候，你妈妈的脸色看起来不太好啊……”</p><p>“啊？”</p><p>这位名叫片山吉方的青年，是一个极为善良而认真的人。这次特意过来也是出于他的这份善良和认真吧。这种事千佳还是明白的。</p><p>只是，对于如今的情况，千佳只能做出这样的回答：</p><p>“这不都是你的错吗？还不都怪你害死了哥哥。”</p><p>对此，片山只能保持沉默。</p><p>他也没什么可回应。千佳所说的都是不可否定的事实。</p><p>“我妈妈最近确实很不好过就是了。虽然是因为爸爸不回家了她的情况才恶化的，但是整件事情说到底还是你的错吧。都是因为你撞死了哥哥。事情都这样了，你干嘛还来我们家？”</p><p>“嗯……确实啊。对不起啊。就像你说的那样，我不该过来的。”</p><p>“我也这么觉得。”</p><p>正好是距今一年前的事了。当时还是卡车司机的片山，在出勤时发生了事故。</p><p>人身事故，准确来说是死亡事故。他把千佳的哥哥撞死了。</p><p>虽然身为小孩的千佳并不清楚事故的详细情况，但根据警察的调查和法院的判决来看，这次事故似乎是“半夜还在路上晃荡的哥哥”的过失。</p><p>无论如何，这位青年每次领到工资后，都会取出一万元送到岛田家。事故发生后的这一年里，他从没有拖欠过一次。</p><p>“说实话，妈妈的脸色越来越不好，有一部分原因就是每个月都要和你见面。但是我倒不会不让你来，毕竟还需要你带来的那些钱。”</p><p>“啊、嗯，我会好好给钱的”</p><p>“这不是当然的吗。你不会以为撞了人家的哥哥还能不用负责吧？但是这也不是因为我贪心哦。现在爸爸也不在了，家里面很需要你给的钱。我们家因为你才变成了这样，所以，一直到我读完大学的费用都要麻烦你喽。”</p><p>“我明白……”</p><p>这个女孩实在聪明，她看清了现实，也活在现实之中。</p><p>片山沉默着低着头，脑海中满是对千佳的愧疚之情。自己造成的事故给他人带了不幸。一个好好的家庭就这么破碎了。他感到自己没法再看千佳的脸。</p><p>“对不起。我，我就先回去了。今天不该过来的，实在是抱歉。”</p><p>“能在见我妈妈之前明白这点就好。”</p><p>青年片山满面愁容，正准备离开。</p><p>“啊，对了，你等一下。”</p><p>千佳急忙叫住转身离去的他。</p><p>“你有没有什么想和别人商量一下的事啊？”</p><p>“商量？我吗？”</p><p>“嗯嗯。虽然说是商量，但更像发牢骚吧。毕竟也是因为你才这样的，要好好听我说的话哦。你在这等一下，我回家去把那个拿过来。”</p><p>十五分钟后，两个人来到附近的家庭餐厅。</p><p>“我要饮料吧台和炸薯条，还有芝士蛋糕。”</p><p>“我只要水就好。”</p><p>对于每月给岛田家交钱的片山而言，来家庭餐厅实在是有些奢侈了。</p><p>千佳也是因为知道这点才特意到这来谈话的。她是在故意惹片山生气。但这也已经算是手下留情了，否则千佳会要求去更贵的店吧。</p><p>“先说好了，我也一点都不喜欢你。都怪你我现在才有这么多麻烦。这点任性的权利我还是有的吧。”</p><p>“嗯嗯，对不起，我明白。”</p><p>“但是啊，我和妈妈比起来，只有她一半，不不，是十分之一的生气。这也是真的哦。”</p><p>即便同为家人，母亲和妹妹也有所不同。相比起母亲，千佳一直在用一种冷静而客观的方式看待哥哥。</p><p>“我哥哥是一个没工作的家里蹲。除了吃饭都不出房间的。他就是最近说的那种尼特吧（最近开始被广泛使用的词）。虽然他和你年纪差不多，连班都不上，成天游手好闲的。一开始听到他出车祸的时候，说实话，我其实有点高兴的。”</p><p>“怎么能这么说呢。千佳，这种话你可不该说啊。”</p><p>“毕竟这是事实呀。但是我没想到妈妈居然这么溺爱哥哥，更没想到我们家会变成这样子。”</p><p>如此看来，岛田家或许从一开始就并不和睦。</p><p>岛田家有这么一个没出息的儿子，还有这么一个溺爱他的母亲，早已是千疮百孔。片山引发的交通事故也只是戳穿了表面的和谐。</p><p>“哥哥的事情都无所谓了。现在最重要的事情是那个呀！”</p><p>千佳一边这么说着，一边突然抽出薄薄的一叠纸放在桌上。</p><p>这叠不到十张的A4纸上用明朝体不知打印了些什么。</p><p>“千佳，这是？”</p><p>“是小说哦，幻想小说。前阵子妈妈用哥哥的电脑的时候，发现电脑一直放着张软盘，接着又发现软盘里存着一份还没写完的小说。然后，妈妈就开始接着写下去了。”</p><p>现如今，软盘虽然渐渐被废用了，但是由于其他的存储媒介价格仍旧居高不下，不少家庭和办公室还在接着用它。</p><p>虽然说是“未完成”，哥哥留下的不过是数十行笔记般的故事梗概而已。还有就是一些过于繁复庞大的设定资料。不过，不管是哪个后面都郑重地署上了过于正式的笔名。</p><p>母亲明明打字都打不利索，想要写完这部小说无异于痴人说梦。</p><p>“那还真是挺厉害的呀。”</p><p>“哪里厉害了？！你给我好好回答！如果是你的话，自己的妈妈有这样的爱好，你不会不好意思吗？！”</p><p>“那个，怎么说好呢……”</p><p>“是吧？我妈妈一点也不觉得不好意思，写完一页就给我看。再这样下去，她岂不是要给附近的人也看看？啊啊，真是的，光是想想我都觉得不好意思。”</p><p>千佳怒火中烧，连吸管都顾不上用，把从饮料吧台接来的杯里的哈密瓜苏打水一饮而尽。</p><p>接着，她又粗暴地将空杯子扣在桌上，接着抱怨起来：</p><p>“所以我今天才找你商量。到底要怎么做才能让妈妈不要再做那个了！这个让人丢脸的兴趣！这么没品味的垃圾小说！”</p><p>“这可真是……”</p><p>此刻，接受着千佳地商量的片山，正与她思考着完全相反的事。他也能理解千佳的心情，毕竟只是个六年级的小学生，对母亲地爱好感到不好意思也是理所当然的。但是，他的注意力全在面前放着的这些纸上。</p><p>（这些莫非是……）</p><p>纸上写的内容很短，片山仅仅花了几分钟就读完了。这些文字确实显得缺乏技巧，却洋溢着一种喜悦感，一种初次创作故事的兴奋感，以及更为引人注目的、一股近乎于执念的热情。</p><p>不，恐怕这股情感就是执念本身吧。文中的登场人物们所作所为无不透露出一股对与被赋予生命这件事本身而散发出的由衷的感谢之情。</p><p>（……这部小说不是挺有有意思的吗？）</p><p>至少片山还想读到后续。这个故事，究竟会走向何处呢？</p><p>“千佳，能不能试试看，让你妈妈继续写下去呢？”</p><p>“啊？你个杀人犯说什么呢？”</p><p>“不是……”</p><p>多么辛辣的一句话。面对少女的威吓，片山哑口无言。</p><p>但此时此刻，在片山的心中——自事故发生以来，一直仿佛行尸走肉般活着、毫无生活目的的片山的心中，点燃了一盏燃烧着热情之炎的明灯。</p><p>（我要让这部小说继续写下去。虽然对不起千佳，但是为了文惠女士和死去的贵史先生……）</p><p>即便只是一点点也好，这也许能算作对那两位的补偿吧。</p><p>多么微弱的一盏希望之灯啊。</p><div>\n<figure><img alt="" src="https://image.gcores.com/87cafce7eb1620e2e4be26c4a7fb417c-1301-1830.jpg?x-oss-process=image/resize,limit_1,m_lfit,w_700,h_2000/quality,q_90/watermark,image_d2F0ZXJtYXJrLnBuZw,g_se,x_10,y_10" /></figure></div><p></p><p><span style="font-weight: bold;">连载小说《我的儿子，如今在异世界快乐生活》</span></p><p><span style="font-style: italic;">随着烟雾散去，怪物一下子就被吹飞了出去。</span></p><p><span style="font-style: italic;">“勇者贵史，刚才那招究竟是什么？”</span></p><p><span style="font-style: italic;">“刚才那是火药。我自己做的。”</span></p><p><span style="font-style: italic;">在这个没发明出火药的异世界里，火药可是十分强大的武器。</span></p><p><span style="font-style: italic;">把骑士夏露娜从危机中救出来后，勇者贵史又用日本料理来招待她。</span></p><p><span style="font-style: italic;">虽然这些对贵史来说都是普通的食物，可在第一次见到这些的夏露娜看来却是十足的稀罕东西。她的内心一点点动摇起来。</span></p><p><span style="font-style: italic;">“来，快多吃一点。怎么样，好吃吧？”</span></p><p><span style="font-style: italic;">待续</span></p>',
# 	 'summary_detail': {'type': 'text/html', 'language': None, 'base': 'https://www.gcores.com/rss',
# 						'value': '<img src="https://image.gcores.com/11d3111336dcf3e0f180f1b429eca028-1305-734.jpg?x-oss-process=image/resize,limit_1,m_fill,w_626,h_292/quality,q_90" /><p>  </p><div>\n<div>\n<figure><img alt="岛田文惠：“那孩子能做这样的吗？”岛田千佳：“啊？你在说什么呀？”片山吉方：“有那么严重吗……？”" src="https://image.gcores.com/0bfd969900c74a557a56923a7f900a76-2724-1922.jpg?x-oss-process=image/resize,limit_1,m_lfit,w_700,h_2000/quality,q_90/watermark,image_d2F0ZXJtYXJrLnBuZw,g_se,x_10,y_10" /><figcaption>(岛田文惠：“那孩子能做这样的吗？”岛田千佳：“啊？你在说什么呀？”片山吉方：“有那么严重吗……？”)</figcaption></figure><figure><img alt="随着烟雾散去，怪物一下子就被吹飞了出去。骑士夏露娜：““勇者贵史，刚才那招究竟是什么？”勇者贵史：“刚才那是火药。我自己做的。”在这个没发明出火药的异世界里，火药可是十分强大的武器。" src="https://image.gcores.com/add4106ea5face59083a1aebb3ec5efc-2724-1922.jpg?x-oss-process=image/resize,limit_1,m_lfit,w_700,h_2000/quality,q_90/watermark,image_d2F0ZXJtYXJrLnBuZw,g_se,x_10,y_10" /><figcaption>(随着烟雾散去，怪物一下子就被吹飞了出去。骑士夏露娜：““勇者贵史，刚才那招究竟是什么？”勇者贵史：“刚才那是火药。我自己做的。”在这个没发明出火药的异世界里，火药可是十分强大的武器。)</figcaption></figure><figure><img alt="“勇者贵史啊，你就到此为止了。你难道以为魔炮沾了水就用不了了吗？”“不不不，不是水，而是热水哦。你知道受热膨胀吗？”——魔佣兵阿姆斯特朗一开魔炮，魔炮便爆炸了。勇者贵史凭借着取得模拟考试县内第二十一位好成绩的头脑打败了他。大魔术师兰斯洛特公主：“不愧是贵史！真聪明！”" src="https://image.gcores.com/9047441d126f1a654b514b1a6dab441e-2724-1922.jpg?x-oss-process=image/resize,limit_1,m_lfit,w_700,h_2000/quality,q_90/watermark,image_d2F0ZXJtYXJrLnBuZw,g_se,x_10,y_10" /><figcaption>(“勇者贵史啊，你就到此为止了。你难道以为魔炮沾了水就用不了了吗？”“不不不，不是水，而是热水哦。你知道受热膨胀吗？”——魔佣兵阿姆斯特朗一开魔炮，魔炮便爆炸了。勇者贵史凭借着取得模拟考试县内第二十一位好成绩的头脑打败了他。大魔术师兰斯洛特公主：“不愧是贵史！真聪明！”)</figcaption></figure>\n</div></div><p>作者：伊藤ヒロ</p><p>插图：やすも</p><h1>序章</h1><p>亲爱的儿子：</p><p>我是妈妈。最近身体还好吗？</p><p>自从你去往异世界，已经过去很久了。</p><p>在那里住的还舒服吗？还在冒险的旅途中吗？还是说，你已经打败了魔王，和大家一起快乐地生活？果然还是开了后宫了？</p><p>你一向喜欢小巧的女孩子，所以妈妈才担心你会不会被小女孩欺负，像是摆出师傅架子的萝莉BBA啦，奴隶市场买来的兽人女孩啦。一定要和同龄的正宫女主角也好好相处呀。</p><p>这边的大家都过得很好。</p><p>你妹妹明年要升初中了。初中的时候你成绩很好，所以我常常想，如果你还在家的话，就能辅导妹妹学习了。</p><p>还记得吗？全国模拟考试的时候你在县里是第二十一名。亲戚们都说，我家的儿子头脑比谁都好。</p><p>如今你一定也借着这股聪明，在那边的世界参加民主选举，或者发明蛋黄酱和黑火药之类的东西吧。毕竟，你是我最骄傲的儿子。</p><p>昨天，片山先生（或许是个你不想听见的名字）又来家里拜访了。</p><p>片山先生他每个月都来家里向你道歉。他也和我约好了，以后会一直把工资的一部分交给我作为补偿。</p><p>你一直是个温柔的孩子，所以，你说不定早就原谅他了。</p><p>但我是个没用的母亲。直到今天，那天发生的事我都不能接受。</p><p>尽管我其实不想要他的钱，也不想再看到他带来的标着银行记号的信封，因为这些根本弥补不了什么，但是害死我儿子的卡车司机就这样一直辛苦下去吧、总之想要他在佛坛前磕头，这样的想法也渐渐消失了。</p><p>现在我只在乎你在异世界过的好不好。</p><p>但是你一定是因为忙于冒险和内政，这次也没法回信吧。虽然很遗憾，但是没办法。</p><p>等到异世界变得和平，你闲下来的时候，一定要记得写信给妈妈呀。</p><p>最后，一定要注意身体，千万不要逞强。也一定要注意车辆。</p><p>你的妈妈</p><p>附：我已经和你爸爸离婚了。</p><p>  </p><h1>第一话 母亲文惠，和异世界转生</h1><p>公元2006年4月下旬——。距离那天已过去一年。</p><p>此处为某县地N市，是个小城市。急行列车在此处铁道停留。因此即便没有家用汽车，也能借助公交网络方便地出行。最近便利店和家庭餐厅也多了起来。在郊外，佳世客（大型商场）也挨着电影院开办了起来。</p><p>手机也是各个运营商的都能用。虽然据说在县内还有不少地方只能用docomo这家运营商的电话。总而言之，此处虽然称不上大都市，倒也可算作一个生活方便的地方。</p><p>在这样一座城市中的一隅，建着一座不起眼的商品房。其中传来这样的声音。</p><p>“妈妈，晚饭不要再做三人份的了！”</p><p>晚上七点，正上小学六年级的、十一岁的岛田千佳在吃晚饭时向母亲说着这样的话。</p><p>我们家的晚饭应该是两人份的。只要有我和妈妈的就足够了。</p><p>这几个月来，父亲都没怎么回过家，和母亲几乎是分居的状态。母亲尽管想要隐瞒，女儿千佳却还是知道了父母私底下办理的离婚。</p><p>——不过话说回来，从很久以前开始，父亲就一直很晚才回家。从小时候开始，一家人在平日里一起吃晚饭在记忆中就一次也没有过。</p><p>这么看来，母亲准备的第三份晚餐并不是为了爸爸。</p><p>那么就是为哥哥准备的了。</p><p>是为一年前去世的哥哥岛田贵史准备的。</p><p>“不是说好了要省钱吗？晚餐做三人份地也太浪费了吧！”</p><p>一如既往的话。少女每天都重复着同样的话。特别是知道了父母离婚的事后，少女的语气变得更加尖锐。</p><p>当她一如既往地责备母亲后，母亲文惠也果然一如既往地回答道：</p><p>“对不起……但是我感觉那孩子说不定就会突然回来。”</p><p>今天的晚饭是炸鸡块和番茄沙拉。</p><p>千佳最近有些在意起体重来。话虽如此，她和平均水平比起来还要偏瘦些。这只是这个年纪的女孩特有的过度节食的倾向。因此她昨天刚刚说过，她不想吃这样的油炸食品和碳水化合物。</p><p>但是，这份菜单是哥哥的最爱。</p><p>即便是挑食的哥哥，面对这份菜单也会难得地大加赞赏、要求再来一份。</p><p>“——也就是说，妈妈不是为了自己，而是为了不在的哥哥准备的晚饭。”</p><p>千佳这么想着，渐渐有些生气，表情也变得严峻起来。</p><p>“千佳，生气了吗……？”</p><p>“……没有。”</p><p>这是谎言。并不是“没有”。千佳正生气。</p><p>“对不起啊，千佳。对不起啊……我今天早上梦到那孩子了……然后，过了白天，去买东西的时候，天空一下子就变蓝了——我就想起来以前，那孩子还小的时候，看到了这样的天空我就会和他一起去散步……我以为这一定是预示着他就要回家了。”</p><p>“你是笨蛋吗？”</p><p>千佳可以理解母亲看到同样的景色就想起哥哥的事。虽然还在读小学六年级，千佳却有着大人般的性格。因此她并没有幼稚到不能理解母亲的伤感。</p><p>但是，千佳还是不明白为什么这是“回家的预兆”。</p><p>因此，千佳生气的原因又多了一个。</p><p>“我说啊，妈妈真的希望哥哥回来吗？明明是那样的哥哥！明明是那样的哥哥！”</p><p>听到女儿的话，母亲只是低着头，沉默着。</p><p>虽然因为角度的原因看不清楚，母亲大概在哭泣。千佳也有些后悔自己的发言，不管怎么说都讲得太过分了。</p><p>毕竟，岛田文惠，虽然是母亲，却仍是个脆弱的女人。</p><p>这就是所谓的“演歌系”吧。世间所谓男人们，一直被女性的脆弱和梦幻感所吸引。这也就意味着，她会如那饱受风吹日晒的柔弱花朵一般，激发起男人们强烈的保护欲。</p><p>可是如今，文惠业已遭丈夫抛弃，身心却还是脆弱如故。无论何事何物，总该有个限度吧。</p><p>这样的女人在同性之中总是遭人厌恶，文惠也不例外。千佳虽然身为女儿，面对母亲时，无论她做了什么说了什么，也总是陷入一种无可奈何的焦躁情绪。</p><p>“——居然为了那样的哥哥，每天这副样子。”。</p><p>千佳紧皱眉头，一言不发地吃着晚饭，还没吃完一半就匆匆回到自己的房间。当然，这也是一如既往。</p><p>不知花了多少时间，文惠一个人把剩下的晚餐吃完了。</p><p>十一岁的少女千佳仰面躺在儿童房的床上，向着天花板吐露心中的不满。</p><p>“啊啊，真是的！受不了了！”</p><p>虽然多少有些令人意外，但千佳并不怨恨自己的父亲。</p><p>在常人看来，舍弃了这样的妻子可谓不人道，将这样的母亲丢给女儿照顾更称得上是恶行。</p><p>但是，千佳已经是六年级的学生了。她多少理解，所谓夫妻，终究还是男女关系的延申。</p><p>因此，千佳能理解父亲的心情。如果自己是丈夫，恐怕也不想回到这样忧郁的女人的身边。</p><p>千佳暗自想到，聪明得不彻底，不如彻底不聪明。或许自己身为孩子便不该表示出对父母的理解，反倒是表现得更加任性一些会更好。</p><p>像班上的男生们那样，做一个能对着“便便”“秃子”这样的词哈哈大笑的孩子的话，就没有这些烦恼了吧。</p><p>（……关于妈妈的事情，我得做点什么才行啊。）</p><p>千佳有些瞧不起自己的母亲。虽说如此，倒也不是真的厌恶她。</p><p>果然这就是母女间感情的体现吧。</p><p>“正因为是孩子才不能逃离父母”，千佳如此开导自己。她是个聪明的少女，能在头脑中快速转变情绪。总之——</p><p>（非得做点什么才行……。首先就这样做吧。）</p><p>对于千佳而言，虽然母亲在做的事无论哪件都让她难以接受，但都还是勉强忍受下来了。</p><p>唯独一件事是例外。</p><p>唯独母亲最近在夜里做的那件事是例外。</p><p>在月光也显得如此耀眼的深夜零点。</p><p>岛田文惠最近开始产生了一个兴趣。主要是在去世的儿子的房间里啪嗒啪嗒地敲响键盘。</p><p>……啪嗒、啪嗒、啪嗒……。</p><p>“——我的erzi，rujin在异世界快乐生huo。”</p><p>她正在写着业余小说。</p><p>这是一本关于少年在幻想世界里旅行的轻小说。</p><p>深夜，当现实世界已陷入沉寂后，文惠用着儿子遗留下的台式电脑，一个字一个字地，啪嗒啪嗒地敲打着键盘……。</p><div>\n<figure><img alt="" src="https://image.gcores.com/2c6bf18da60aea679f66bfbbfb1da7b8-1299-1824.jpg?x-oss-process=image/resize,limit_1,m_lfit,w_700,h_2000/quality,q_90/watermark,image_d2F0ZXJtYXJrLnBuZw,g_se,x_10,y_10" /></figure></div><p></p><p><span style="font-weight: bold;">连载小说《我的儿子，如今在异世界快乐生活》</span></p><p><span style="font-style: italic;">“贵史呀，你还没有死。你会作为异世界的勇者活下去。”</span></p><p><span style="font-style: italic;">女神温柔的声音直接传入贵史的脑海。</span></p><p><span style="font-style: italic;">被卡车撞倒后的贵史一醒来便发现自己在一个陌生的地方。</span></p><p><span style="font-style: italic;">“这里是……？我明明被卡车撞了呀。”</span></p><p><span style="font-style: italic;">眼前都是贵史没见过的风景。可是，他还是不知道这里是哪里。</span></p><p><span style="font-style: italic;">“这里难道是幻想世界吗？”</span></p><p><span style="font-style: italic;">这不是在做梦。就像那位女神说的那样。</span></p><p><span style="font-style: italic;">待续</span></p><p>  </p><h1>第二话 母亲文惠，和原卡车司机</h1><p>西历2006年。世界迈入新世纪已过去了五年。</p><p>这是一个总觉得有些空虚的时代。新世纪的风景，既不是幻想中的“梦中的未来社会”，也不是“核战争后的废土世界”。——可以说，人们是以一种逃避的姿态生活在这个所谓的“零零年代”（西历2000年到2010年的十年间）。</p><p>话虽如此，科技从九十年代开始便稳步向前发展。得益于此，像N市这样的小城市里，因特网、个人电脑和移动电话也普及开来。世界确确实实地发生了变化。</p><p>在这个不平衡的时代里，某个春日午后，以下的故事发生了。</p><p>岛田千佳正走在从小学回家的路上。在家附近，她看到一个熟悉的身影。</p><p>“欸，那不是片山先生吗？”</p><p>那人的名叫片山吉方。</p><p>他还是位二十岁出头、气质有些柔弱的青年。听到背后传来的声音后，他发出“哇！”的一声，明显吃惊的有些过头，直跳起来，几乎就要从原地飞走了。</p><p>面对这样一个做出漫画中才会出现的反应的男人，千佳一时手足无措，愣在原地。</p><p>“吓了我一跳。你，你好啊，千佳。”</p><p>“才不是你好吧！你在这里干嘛？在我家附近鬼鬼祟祟的。”</p><p>这位青年简直就像间谍或是小偷那样，躲在电线杆后的阴影里偷看千佳她们家，活脱脱一个可疑分子形象。</p><p>“你这下总算要被警察抓走了吧？这次要被送进看守所了吧？上次是缓刑来着。”</p><p>“你也太严厉了吧……其实，我想着去一趟你家来着。”</p><p>“来我家？为什么？前几天不是才来过？”</p><p>“该怎么说呢……”不知为何，片山开始吞吞吐吐起来。</p><p>“其实我从之前的公司辞职了。毕竟发生了那样的事。以后我会在一家电脑公司工作。这次是想来报告一下这件事。”</p><p>“这也没什么必要吧。我妈妈对这种事情没什么兴趣。”千佳虽然这么回答着，却也明白这位青年是出于诚意才辞职的。还是不要说“别来”这种话为好，她暗自想到。</p><p>“片山先生，你最好还是别说新工作是有关电脑的工作。像我妈妈这个年纪的人，总是会就觉得那是一种轻松的活。还是和她说是要做一些更辛苦的工作更好哦。”</p><p>“啊，我明白了。那个，还有一件事——”</p><p>“还有什么事？”</p><p>看他这说话吞吞吐吐的样子，恐怕报告要换工作这事只是个借口，其实他还另有所图。</p><p>片山用比之前更加吞吞吐吐的语气，认真地说出了所谓的“另一件事”：</p><p>“那个、之前见面的时候，你妈妈的脸色看起来不太好啊……”</p><p>“啊？”</p><p>这位名叫片山吉方的青年，是一个极为善良而认真的人。这次特意过来也是出于他的这份善良和认真吧。这种事千佳还是明白的。</p><p>只是，对于如今的情况，千佳只能做出这样的回答：</p><p>“这不都是你的错吗？还不都怪你害死了哥哥。”</p><p>对此，片山只能保持沉默。</p><p>他也没什么可回应。千佳所说的都是不可否定的事实。</p><p>“我妈妈最近确实很不好过就是了。虽然是因为爸爸不回家了她的情况才恶化的，但是整件事情说到底还是你的错吧。都是因为你撞死了哥哥。事情都这样了，你干嘛还来我们家？”</p><p>“嗯……确实啊。对不起啊。就像你说的那样，我不该过来的。”</p><p>“我也这么觉得。”</p><p>正好是距今一年前的事了。当时还是卡车司机的片山，在出勤时发生了事故。</p><p>人身事故，准确来说是死亡事故。他把千佳的哥哥撞死了。</p><p>虽然身为小孩的千佳并不清楚事故的详细情况，但根据警察的调查和法院的判决来看，这次事故似乎是“半夜还在路上晃荡的哥哥”的过失。</p><p>无论如何，这位青年每次领到工资后，都会取出一万元送到岛田家。事故发生后的这一年里，他从没有拖欠过一次。</p><p>“说实话，妈妈的脸色越来越不好，有一部分原因就是每个月都要和你见面。但是我倒不会不让你来，毕竟还需要你带来的那些钱。”</p><p>“啊、嗯，我会好好给钱的”</p><p>“这不是当然的吗。你不会以为撞了人家的哥哥还能不用负责吧？但是这也不是因为我贪心哦。现在爸爸也不在了，家里面很需要你给的钱。我们家因为你才变成了这样，所以，一直到我读完大学的费用都要麻烦你喽。”</p><p>“我明白……”</p><p>这个女孩实在聪明，她看清了现实，也活在现实之中。</p><p>片山沉默着低着头，脑海中满是对千佳的愧疚之情。自己造成的事故给他人带了不幸。一个好好的家庭就这么破碎了。他感到自己没法再看千佳的脸。</p><p>“对不起。我，我就先回去了。今天不该过来的，实在是抱歉。”</p><p>“能在见我妈妈之前明白这点就好。”</p><p>青年片山满面愁容，正准备离开。</p><p>“啊，对了，你等一下。”</p><p>千佳急忙叫住转身离去的他。</p><p>“你有没有什么想和别人商量一下的事啊？”</p><p>“商量？我吗？”</p><p>“嗯嗯。虽然说是商量，但更像发牢骚吧。毕竟也是因为你才这样的，要好好听我说的话哦。你在这等一下，我回家去把那个拿过来。”</p><p>十五分钟后，两个人来到附近的家庭餐厅。</p><p>“我要饮料吧台和炸薯条，还有芝士蛋糕。”</p><p>“我只要水就好。”</p><p>对于每月给岛田家交钱的片山而言，来家庭餐厅实在是有些奢侈了。</p><p>千佳也是因为知道这点才特意到这来谈话的。她是在故意惹片山生气。但这也已经算是手下留情了，否则千佳会要求去更贵的店吧。</p><p>“先说好了，我也一点都不喜欢你。都怪你我现在才有这么多麻烦。这点任性的权利我还是有的吧。”</p><p>“嗯嗯，对不起，我明白。”</p><p>“但是啊，我和妈妈比起来，只有她一半，不不，是十分之一的生气。这也是真的哦。”</p><p>即便同为家人，母亲和妹妹也有所不同。相比起母亲，千佳一直在用一种冷静而客观的方式看待哥哥。</p><p>“我哥哥是一个没工作的家里蹲。除了吃饭都不出房间的。他就是最近说的那种尼特吧（最近开始被广泛使用的词）。虽然他和你年纪差不多，连班都不上，成天游手好闲的。一开始听到他出车祸的时候，说实话，我其实有点高兴的。”</p><p>“怎么能这么说呢。千佳，这种话你可不该说啊。”</p><p>“毕竟这是事实呀。但是我没想到妈妈居然这么溺爱哥哥，更没想到我们家会变成这样子。”</p><p>如此看来，岛田家或许从一开始就并不和睦。</p><p>岛田家有这么一个没出息的儿子，还有这么一个溺爱他的母亲，早已是千疮百孔。片山引发的交通事故也只是戳穿了表面的和谐。</p><p>“哥哥的事情都无所谓了。现在最重要的事情是那个呀！”</p><p>千佳一边这么说着，一边突然抽出薄薄的一叠纸放在桌上。</p><p>这叠不到十张的A4纸上用明朝体不知打印了些什么。</p><p>“千佳，这是？”</p><p>“是小说哦，幻想小说。前阵子妈妈用哥哥的电脑的时候，发现电脑一直放着张软盘，接着又发现软盘里存着一份还没写完的小说。然后，妈妈就开始接着写下去了。”</p><p>现如今，软盘虽然渐渐被废用了，但是由于其他的存储媒介价格仍旧居高不下，不少家庭和办公室还在接着用它。</p><p>虽然说是“未完成”，哥哥留下的不过是数十行笔记般的故事梗概而已。还有就是一些过于繁复庞大的设定资料。不过，不管是哪个后面都郑重地署上了过于正式的笔名。</p><p>母亲明明打字都打不利索，想要写完这部小说无异于痴人说梦。</p><p>“那还真是挺厉害的呀。”</p><p>“哪里厉害了？！你给我好好回答！如果是你的话，自己的妈妈有这样的爱好，你不会不好意思吗？！”</p><p>“那个，怎么说好呢……”</p><p>“是吧？我妈妈一点也不觉得不好意思，写完一页就给我看。再这样下去，她岂不是要给附近的人也看看？啊啊，真是的，光是想想我都觉得不好意思。”</p><p>千佳怒火中烧，连吸管都顾不上用，把从饮料吧台接来的杯里的哈密瓜苏打水一饮而尽。</p><p>接着，她又粗暴地将空杯子扣在桌上，接着抱怨起来：</p><p>“所以我今天才找你商量。到底要怎么做才能让妈妈不要再做那个了！这个让人丢脸的兴趣！这么没品味的垃圾小说！”</p><p>“这可真是……”</p><p>此刻，接受着千佳地商量的片山，正与她思考着完全相反的事。他也能理解千佳的心情，毕竟只是个六年级的小学生，对母亲地爱好感到不好意思也是理所当然的。但是，他的注意力全在面前放着的这些纸上。</p><p>（这些莫非是……）</p><p>纸上写的内容很短，片山仅仅花了几分钟就读完了。这些文字确实显得缺乏技巧，却洋溢着一种喜悦感，一种初次创作故事的兴奋感，以及更为引人注目的、一股近乎于执念的热情。</p><p>不，恐怕这股情感就是执念本身吧。文中的登场人物们所作所为无不透露出一股对与被赋予生命这件事本身而散发出的由衷的感谢之情。</p><p>（……这部小说不是挺有有意思的吗？）</p><p>至少片山还想读到后续。这个故事，究竟会走向何处呢？</p><p>“千佳，能不能试试看，让你妈妈继续写下去呢？”</p><p>“啊？你个杀人犯说什么呢？”</p><p>“不是……”</p><p>多么辛辣的一句话。面对少女的威吓，片山哑口无言。</p><p>但此时此刻，在片山的心中——自事故发生以来，一直仿佛行尸走肉般活着、毫无生活目的的片山的心中，点燃了一盏燃烧着热情之炎的明灯。</p><p>（我要让这部小说继续写下去。虽然对不起千佳，但是为了文惠女士和死去的贵史先生……）</p><p>即便只是一点点也好，这也许能算作对那两位的补偿吧。</p><p>多么微弱的一盏希望之灯啊。</p><div>\n<figure><img alt="" src="https://image.gcores.com/87cafce7eb1620e2e4be26c4a7fb417c-1301-1830.jpg?x-oss-process=image/resize,limit_1,m_lfit,w_700,h_2000/quality,q_90/watermark,image_d2F0ZXJtYXJrLnBuZw,g_se,x_10,y_10" /></figure></div><p></p><p><span style="font-weight: bold;">连载小说《我的儿子，如今在异世界快乐生活》</span></p><p><span style="font-style: italic;">随着烟雾散去，怪物一下子就被吹飞了出去。</span></p><p><span style="font-style: italic;">“勇者贵史，刚才那招究竟是什么？”</span></p><p><span style="font-style: italic;">“刚才那是火药。我自己做的。”</span></p><p><span style="font-style: italic;">在这个没发明出火药的异世界里，火药可是十分强大的武器。</span></p><p><span style="font-style: italic;">把骑士夏露娜从危机中救出来后，勇者贵史又用日本料理来招待她。</span></p><p><span style="font-style: italic;">虽然这些对贵史来说都是普通的食物，可在第一次见到这些的夏露娜看来却是十足的稀罕东西。她的内心一点点动摇起来。</span></p><p><span style="font-style: italic;">“来，快多吃一点。怎么样，好吃吧？”</span></p><p><span style="font-style: italic;">待续</span></p>'},
# 	 'authors': [{'name': '阳光之星'}], 'author': '阳光之星', 'author_detail': {'name': '阳光之星'},
# 	 'id': 'https://www.gcores.com/articles/167389', 'guidislink': False,
# 	 'published': 'Wed, 21 Jun 2023 14:00:20 +0800',
# 	 'published_parsed': time.struct_time(tm_year=2023, tm_mon=6, tm_mday=21, tm_hour=6, tm_min=0, tm_sec=20,
# 										  tm_wday=2, tm_yday=172, tm_isdst=0),
# 	 'thumb': 'https://image.gcores.com/11d3111336dcf3e0f180f1b429eca028-1305-734.jpg?x-oss-process=image/resize,limit_1,m_fill,w_626,h_292/quality,q_90'
# }

# {
# 	'title': '新能源汽车时代技术更重要还是品牌更重要？',
# 	'title_detail': {'type': 'text/plain',
# 					 'language': None,
# 					 'base': 'https://www.zhihu.com/rss',
# 					 'value': '新能源汽车时代技术更重要还是品牌更重要？'},
# 	'links': [{'rel': 'alternate',
# 			   'type': 'text/html',
# 			   'href': 'http://www.zhihu.com/question/598593472/answer/3020473909?utm_campaign=rss&utm_medium=rss&utm_source=rss&utm_content=title'}],
# 	'link': 'http://www.zhihu.com/question/598593472/answer/3020473909?utm_campaign=rss&utm_medium=rss&utm_source=rss&utm_content=title',
# 	'summary': '<blockquote><b>技术应对产品，品牌应对体验！</b></blockquote><p>对于汽车行业，一提到“技术”和“品牌”这两个哪个重要，大家都会异口同声的说：技术重要，技术才是永远的王道。而品牌，多数人认为这是虚的，没有人只是为买个牌子。这样的观点也没错，毕竟我国的汽车工业就是这么走过来的，但处在21世纪的今天，这样的观点应该改变，技术和品牌应该是相辅相成的！</p><p><img src="https://picx.zhimg.com/v2-d7ec8dcd7536ea7cf5ebc2679457fef3_720w.jpeg?source=b1748391?rss" /></p><p>多少年来，提到技术，对于我国汽车行业来讲，那就是核心，就是全部。曾几何时，中国的汽车工业发展之初，汽车从业者最渴望的就是技术，那个年代没有技术，一切都未从谈起。这么多年以来，我国靠着<b>庞大的汽车消费市场来换取汽车技术</b>，这也让中国的汽车工业迈出了发展的一大步。但对于传统汽车真正的核心技术，我们仍然没有完全掌握，还有着向国外企业、品牌学习的空间。</p><p>这样的历史时期支撑了我国汽车工业的发展。而如今，我们处在一个移动互联网、智能电动汽车发展、开放的时代，技术已经不再是汽车行业的唯一了，在这个时期，消费者才是唯一的，<b>汽车行业开始将“以人为本”作为发展的重点。</b></p><p><b>技术再好，它也是为人服务的，没有了消费者，再好的技术也没有落脚之地。</b>况且，再向消费者介绍新款车型时，销售人员或者品牌公司不可能只把话语的重点放在技术上吧，与其给客户讲这款车搭载的技术如何如何先进、产品功能如何如何丰富，还不如着眼于新车体验上，让乘客切身感受新技术带来的全新的体验。<b>真实的体验是一切的开始</b>，只有实实在在的体验，消费者才会认同这项技术，才会判断这项技术是不是真正的好技术，至于技术如何如何开发出来的、技术原理是什么，消费者没有兴趣对其做更深的了解。</p><p><img src="https://picx.zhimg.com/v2-46450f9352c7fcccc60480f2fc455aba_720w.jpeg?source=b1748391?rss" /></p><p><b>品牌是什么，品牌就意味着市场，没有市场就没有品牌。</b>最需要重视的一点：品牌做大意味着更大的销售量、更持久的销售周期。对于品牌来说，技术只是构成品牌利益点的众多因素中较重要的那个。</p><p>之前的传统燃油车时代，经过上百年的发展，<b>品牌就意味着销量、就意味着高品质</b>，因为燃油车时代能留到现在的品牌都是在上百年的激烈竞争中存活下来的，他们也是有着强大的燃油汽车技术来支撑的，所以为什么之前买车，大众、BBA、本田、丰田那么吃香，一大部分的用户都是冲着这样屹立百年的品牌才购车的，尤其是进入到“新能源汽车时代”的今天，我国新能源汽车市场已经如此火爆，但一些坚挺的传统品牌仍然具备着强有力的销量，这就是品牌的力量，它的确带来了持久的销售周期。</p><p><img src="https://picx.zhimg.com/v2-18bce1e5614b0391b5f028651c46cd51_720w.jpeg?source=b1748391?rss" /></p><p>新能源汽车时代，越来越多的科技汽车企业、造车新势力如雨后春笋般爆发出来，，一些是鼓吹品牌理念的，一些是鼓吹技术的，亮一些则是讲品牌定位与产品技术两手抓的。经过四五年的发展，我们能够发现，之前的众多新能源汽车品牌都走向了消亡，在新能源汽车的地位争夺赛中沦为了垫脚石，这样的企业大都是前两种，只专注一方面的企业。</p><p><img src="https://picx.zhimg.com/v2-d3a65efdfb1db49a04f97422280cc2d6_720w.jpeg?source=b1748391?rss" /></p><p><b>新能源汽车时代，需要既能踏踏实实做好技术，又能讲好品牌故事、品牌理念的车企</b>，毕竟软件定义汽车的时代，汽车更新换代的速度是越来越快，单纯的讲技术会让消费者眼花缭乱。<b>车企应该通过讲好品牌故事的方式将技术与体验完美的呈现出来</b>，才能让用户对品牌和技术有更深的印象。举个例子：特斯拉，<b>马斯克将特斯拉的品牌故事用“特斯拉秘密宏图”来呈现。“秘密宏图第一篇章”</b>为我们带来了Model S/X以及Model 3/Y等产品；<b>“秘密宏图第二篇章”</b>带来了屋顶光伏、Powerwall、FSD以及Semi等；<b>“秘密宏图第三篇章”</b>带来了储能、电动车、可再生能源生产设施、一体化压铸、自动驾驶、Cybertruck问世以及人形机器人等关键内容。通过这样的方式将技术一一带出，会让消费者更有兴趣去探究这个品牌的故事与理念，才会有助于企业的发展。</p>\n<br /><br />\n来源：知乎 www.zhihu.com<br />\n    \n作者：<a href="http://www.zhihu.com/people/18833271729?utm_campaign=rss&amp;utm_medium=rss&amp;utm_source=rss&amp;utm_content=author">汽车人高工</a><br />\n            \n<br />\n【知乎日报】千万用户的选择，做朋友圈里的新鲜事分享大牛。\n        <a href="http://daily.zhihu.com?utm_source=rssyanwenzi&amp;utm_campaign=tuijian&amp;utm_medium=rssnormal" target="_blank">点击下载</a><br />\n<br />\n此问题还有 <a href="http://www.zhihu.com/question/598593472/answer/3020473909?utm_campaign=rss&amp;utm_medium=rss&amp;utm_source=rss&amp;utm_content=title" target="_blank">103 个回答，查看全部。</a><br />\n                延伸阅读：<br />\n<a href="http://www.zhihu.com/question/577936218?utm_campaign=rss&amp;utm_medium=rss&amp;utm_source=rss&amp;utm_content=title" target="_blank">新能源汽车制造与传统汽车有什么不同？</a><br />\n            \n<a href="http://www.zhihu.com/question/601957162?utm_campaign=rss&amp;utm_medium=rss&amp;utm_source=rss&amp;utm_content=title" target="_blank">我们的新能源汽车技术在国际上具有怎样的优势？</a><br />',
# 	'summary_detail': {'type': 'text/html',
# 					   'language': None,
# 					   'base': 'https://www.zhihu.com/rss',
# 					   'value': '<blockquote><b>技术应对产品，品牌应对体验！</b></blockquote><p>对于汽车行业，一提到“技术”和“品牌”这两个哪个重要，大家都会异口同声的说：技术重要，技术才是永远的王道。而品牌，多数人认为这是虚的，没有人只是为买个牌子。这样的观点也没错，毕竟我国的汽车工业就是这么走过来的，但处在21世纪的今天，这样的观点应该改变，技术和品牌应该是相辅相成的！</p><p><img src="https://picx.zhimg.com/v2-d7ec8dcd7536ea7cf5ebc2679457fef3_720w.jpeg?source=b1748391?rss" /></p><p>多少年来，提到技术，对于我国汽车行业来讲，那就是核心，就是全部。曾几何时，中国的汽车工业发展之初，汽车从业者最渴望的就是技术，那个年代没有技术，一切都未从谈起。这么多年以来，我国靠着<b>庞大的汽车消费市场来换取汽车技术</b>，这也让中国的汽车工业迈出了发展的一大步。但对于传统汽车真正的核心技术，我们仍然没有完全掌握，还有着向国外企业、品牌学习的空间。</p><p>这样的历史时期支撑了我国汽车工业的发展。而如今，我们处在一个移动互联网、智能电动汽车发展、开放的时代，技术已经不再是汽车行业的唯一了，在这个时期，消费者才是唯一的，<b>汽车行业开始将“以人为本”作为发展的重点。</b></p><p><b>技术再好，它也是为人服务的，没有了消费者，再好的技术也没有落脚之地。</b>况且，再向消费者介绍新款车型时，销售人员或者品牌公司不可能只把话语的重点放在技术上吧，与其给客户讲这款车搭载的技术如何如何先进、产品功能如何如何丰富，还不如着眼于新车体验上，让乘客切身感受新技术带来的全新的体验。<b>真实的体验是一切的开始</b>，只有实实在在的体验，消费者才会认同这项技术，才会判断这项技术是不是真正的好技术，至于技术如何如何开发出来的、技术原理是什么，消费者没有兴趣对其做更深的了解。</p><p><img src="https://picx.zhimg.com/v2-46450f9352c7fcccc60480f2fc455aba_720w.jpeg?source=b1748391?rss" /></p><p><b>品牌是什么，品牌就意味着市场，没有市场就没有品牌。</b>最需要重视的一点：品牌做大意味着更大的销售量、更持久的销售周期。对于品牌来说，技术只是构成品牌利益点的众多因素中较重要的那个。</p><p>之前的传统燃油车时代，经过上百年的发展，<b>品牌就意味着销量、就意味着高品质</b>，因为燃油车时代能留到现在的品牌都是在上百年的激烈竞争中存活下来的，他们也是有着强大的燃油汽车技术来支撑的，所以为什么之前买车，大众、BBA、本田、丰田那么吃香，一大部分的用户都是冲着这样屹立百年的品牌才购车的，尤其是进入到“新能源汽车时代”的今天，我国新能源汽车市场已经如此火爆，但一些坚挺的传统品牌仍然具备着强有力的销量，这就是品牌的力量，它的确带来了持久的销售周期。</p><p><img src="https://picx.zhimg.com/v2-18bce1e5614b0391b5f028651c46cd51_720w.jpeg?source=b1748391?rss" /></p><p>新能源汽车时代，越来越多的科技汽车企业、造车新势力如雨后春笋般爆发出来，，一些是鼓吹品牌理念的，一些是鼓吹技术的，亮一些则是讲品牌定位与产品技术两手抓的。经过四五年的发展，我们能够发现，之前的众多新能源汽车品牌都走向了消亡，在新能源汽车的地位争夺赛中沦为了垫脚石，这样的企业大都是前两种，只专注一方面的企业。</p><p><img src="https://picx.zhimg.com/v2-d3a65efdfb1db49a04f97422280cc2d6_720w.jpeg?source=b1748391?rss" /></p><p><b>新能源汽车时代，需要既能踏踏实实做好技术，又能讲好品牌故事、品牌理念的车企</b>，毕竟软件定义汽车的时代，汽车更新换代的速度是越来越快，单纯的讲技术会让消费者眼花缭乱。<b>车企应该通过讲好品牌故事的方式将技术与体验完美的呈现出来</b>，才能让用户对品牌和技术有更深的印象。举个例子：特斯拉，<b>马斯克将特斯拉的品牌故事用“特斯拉秘密宏图”来呈现。“秘密宏图第一篇章”</b>为我们带来了Model S/X以及Model 3/Y等产品；<b>“秘密宏图第二篇章”</b>带来了屋顶光伏、Powerwall、FSD以及Semi等；<b>“秘密宏图第三篇章”</b>带来了储能、电动车、可再生能源生产设施、一体化压铸、自动驾驶、Cybertruck问世以及人形机器人等关键内容。通过这样的方式将技术一一带出，会让消费者更有兴趣去探究这个品牌的故事与理念，才会有助于企业的发展。</p>\n<br /><br />\n来源：知乎 www.zhihu.com<br />\n    \n作者：<a href="http://www.zhihu.com/people/18833271729?utm_campaign=rss&amp;utm_medium=rss&amp;utm_source=rss&amp;utm_content=author">汽车人高工</a><br />\n            \n<br />\n【知乎日报】千万用户的选择，做朋友圈里的新鲜事分享大牛。\n        <a href="http://daily.zhihu.com?utm_source=rssyanwenzi&amp;utm_campaign=tuijian&amp;utm_medium=rssnormal" target="_blank">点击下载</a><br />\n<br />\n此问题还有 <a href="http://www.zhihu.com/question/598593472/answer/3020473909?utm_campaign=rss&amp;utm_medium=rss&amp;utm_source=rss&amp;utm_content=title" target="_blank">103 个回答，查看全部。</a><br />\n                延伸阅读：<br />\n<a href="http://www.zhihu.com/question/577936218?utm_campaign=rss&amp;utm_medium=rss&amp;utm_source=rss&amp;utm_content=title" target="_blank">新能源汽车制造与传统汽车有什么不同？</a><br />\n            \n<a href="http://www.zhihu.com/question/601957162?utm_campaign=rss&amp;utm_medium=rss&amp;utm_source=rss&amp;utm_content=title" target="_blank">我们的新能源汽车技术在国际上具有怎样的优势？</a><br />'},
# 	'authors': [{'name': '汽车人高工'}],
# 	'author': '汽车人高工',
# 	'author_detail': {'name': '汽车人高工'},
# 	'published': 'Wed, '
# 				 '14 Jun 2023 18:39:59 +0800',
# 	'published_parsed': time.struct_time(tm_year=2023,
# 										 tm_mon=6,
# 										 tm_mday=14,
# 										 tm_hour=10,
# 										 tm_min=39,
# 										 tm_sec=59,
# 										 tm_wday=2,
# 										 tm_yday=165,
# 										 tm_isdst=0),
# 	'id': 'http://www.zhihu.com/question/598593472/answer/3020473909',
# 	'guidislink': False
# }

RSS = RSS_()