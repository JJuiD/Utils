import random
import sys
import json
import os.path
import pprint
import re
import time
import csv

import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd

# ANIMAL_NAMES = [
#     '虎', '狼', '鼠', '鹿', '貂', '猴', '貘', '马', '狗', '狐', 
#     '熊', '象', '豹', '牛', '猫', '猪', '羊', '兽', '猩', '獭', 
#     '鱼', '蟒', '蜥', '鳄', '龟', '鳖', '蛙', 
#     '螈', '鹰', '鹭', '鹅', '鸟', '鸥', '鸡', 
#     '翁', '鹤', '雉', '燕', 
#     '雁', '鸽',
#     '雕', '鸭', '鲤', "虫"
# ]

# ffmap = {}
# fflist = []
# for s in ANIMAL_NAMES:
#     s = s[-1]
#     if ffmap.get(s) == None:
#         fflist.append(s)
#         ffmap[s] = True

# print(fflist)


# url_base = 'https://wiki.52poke.com/wiki/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89/%E7%AE%80%E5%8D%95%E7%89%88#.E7.AC.AC.E4.BA.8C.E4.B8.96.E4.BB.A3'
# resp = requests.get(url_base)
# resp_html = resp.text
# soup = BeautifulSoup(resp_html, features='lxml')
# all_data = soup.find('table', class_='a-c roundy eplist bgl-神奇宝贝百科 b-神奇宝贝百科 bw-2').find_all('tr')
# origin_data = []
# for tr in all_data[3:]:
#     td = tr.find_all('td')
#     if len(td) < 2:
#         continue
#     id_tmp = td[0].get_text()[:-1]
#     href_tmp = td[1].find('a').get('href')
#     name_tmp = td[1].find('a').get('title')
#     origin_data.append((id_tmp, href_tmp, name_tmp))


# """爬取900多只宝可梦"""
# if not os.path.exists('./image'):
#     os.makedirs('./image')
# Data_dict = {}
# for id, href, name in origin_data:
#     value_dict = {'id': id}
#     url = f'https://wiki.52poke.com/{href}'
#     resp = requests.get(url)
#     resp_html = resp.text
#     etree = html.etree
#     tree = etree.HTML(resp_html)
#     """爬取图片"""
#     image_url = tree.xpath(
#         '/html/body/div[3]/div[3]/div[5]/div/table[2]/tbody/tr[2]/td/table/tbody/tr/td/div[1]/a/img/@data-url')
#     if len(image_url) == 0:
#         print(id)
#         tmp = pd.read_html(url)
#         if len(tmp) > 209:
#             name_var = tmp[209].columns[0]
#             for t in range(1, len(name_var)):
#                 # 特别处理，多种形态的图片
#                 n = name_var[t]
#                 image_url = tree.xpath(
#                     f'/html/body/div[3]/div[3]/div[5]/div/table[2]/tbody/tr[{t}]/td/table/tbody/tr[2]/td/table/tbody/tr/td/a/img/@data-url')
#                 if len(image_url) == 0:
#                     image_url = tree.xpath(
#                         f'/html/body/div[3]/div[3]/div[5]/div/table[2]/tbody/tr[{t}]/td/table/tbody/tr[2]/td/table/tbody/tr/td/div[1]/a/img/@data-url')

#                 image_url = 'https:' + image_url[0]
#                 image_resp = requests.get(image_url)
#                 with open(f'./image/{n}.png', 'wb') as f:
#                     f.write(image_resp.content)
#                 print(f'{id}: {n}图片爬取成功')

#     else:
#         image_url = image_url[0]
#         image_url = 'https:' + image_url
#         image_resp = requests.get(image_url)
#         with open(f'./image/{name}.png', 'wb') as f:
#             f.write(image_resp.content)
#         print(f'{id}: {name}图片爬取成功')
#     time.sleep(0.5)
#     """爬取属性"""
#     attribute = re.findall('<table class="roundy (.*)fulltable">', resp_html)
#     attribute = attribute[2].split(' ')
#     att1 = attribute[0].split('-')[-1]
#     att2 = attribute[1].split('-')[-1]
#     if att1 == att2:
#         value_dict['属性'] = att1
#     else:
#         value_dict['属性'] = att1 + '-' + att2
#     """种族值"""
#     table_value = pd.read_html(resp_html)

#     for table in table_value:
#         if len(table.index) == 8 and len(table.columns) == 4 and table.columns[0][0] == '种族值':
#             table_target = table
#     table_value = table_target.values[:7, 0]

#     race_list = {}
#     for i in table_value:
#         race_list[i.split('：')[0]] = i.split('：')[1]
#     value_dict['种族值'] = race_list
#     """介绍"""
#     soup_tmp = BeautifulSoup(resp_html, features='lxml')
#     all_data_tmp = soup_tmp.find_all('div', class_='mw-parser-output')[0].find_all('p')
#     intro = ''
#     for m in all_data_tmp:
#         if m.string is not None:
#             intro += m.string
#     value_dict['介绍'] = intro
#     print(f'{id},{name}数据爬取完成...')
#     Data_dict[name] = value_dict


GrassType = {
    1: "Normal",         # 一般
    2: "Fire",           # 火
    3: "Fighting",       # 格斗
    4: "Water",          # 水
    5: "Flying",         # 飞行
    6: "Grass",          # 草
    7: "Poison",         # 毒
    8: "Electric",       # 电
    9: "Ground",         # 地面
    10: "Psychic",       # 超能力
    11: "Rock",          # 岩石
    12: "Ice",           # 冰
    13: "Bug",           # 虫
    14: "Dragon",        # 龙
    15: "Ghost",         # 幽灵
    16: "Dark",          # 恶
    17: "Steel",         # 钢
    18: "Fairy",         # 妖精
}


# 自动生成一些csv配置
if __name__ == '__main__':
    generate_type = "monster" #sys.argv[1]
    # 生成怪物设定
    if generate_type == "monster":
        #####################################
        # const 定义
        generate_id_begin = 100
        generate_grass_rate = [                                                     # 属性比例
            1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1
        ]    
        generate_evolution_rate = [                                                     # 阶段比例 1, 2, 3
            3, 1.5, 1.5
        ]    
        generate_count = 100                                                        # 个数
        generate_level_max = 100                                                    # 最大等级
        generate_attr_sum_min = 200                                                 # 属性综合最小
        generate_attr_sum_max = 300                                                 # 属性综合最大

        
        generate_attr_lv_distribution = [                                                         # 属性分布
            [10, 150], 
            [10, 150], [10, 150],
            [10, 150], [10, 150],
            [10, 50]
        ]
        generate_attr_evolution_reduce = 0.1
        #####################################
        cn_total_counter = {
            # "hp": 0, "dmg": 0, "def": 0, "sdmg": 0, "sdef": 0
            "id_counter": {}
        }

        desc_cache = {}

        def get_index(key, i, desc=""):
            index = key + str(i)
            if desc_cache.get(index) != None:
                return desc_cache.get(index)
            if desc != "":
                if type(desc) == dict:
                    desc_cache.update(desc)
                    return desc_cache[index]
                else:
                    return desc
            return index
                

        def total_counter(key, i, step, default=None, desc=""):
            index = get_index(key, i, desc=desc)

            if default != None:
                if cn_total_counter.get(index) == None:
                    cn_total_counter[index] = default
                cn_total_counter[index] = cn_total_counter[index] + step
            else:
                cn_total_counter[index] = step
                

        def id_counter(id, key, i, step, default=None, desc=""):
            if cn_total_counter["id_counter"].get(id) == None:
                cn_total_counter["id_counter"][id] = {}
            
            index = get_index(key, i, desc=desc)

            if default != None:
                if cn_total_counter["id_counter"][id].get(index) == None:
                    cn_total_counter["id_counter"][id][index] = default
                cn_total_counter["id_counter"][id][index] = cn_total_counter["id_counter"][id][index] + step
            else:
                cn_total_counter["id_counter"][id][index] = step
                

        #####################################
        evolution_num = []
        evolution_rate_sum = sum(generate_evolution_rate)
        temp_count = generate_count
        for rate in generate_evolution_rate:
            evolution_num.append(int(rate/evolution_rate_sum*generate_count))
            temp_count = temp_count - evolution_num[len(evolution_num) - 1]
        evolution_num[0] += temp_count
        evolution_num[0] += evolution_num[1]%2
        evolution_num[1] -= evolution_num[1]%2
        evolution_num[0] += evolution_num[2]%3
        evolution_num[2] -= evolution_num[2]%3

        grass_num = []
        grass_rate_sum = sum(generate_grass_rate)
        _generate_count = int(generate_count - evolution_num[1]/2  - evolution_num[2]/3*2)
        temp_count = _generate_count
        for rate in generate_grass_rate:
            grass_num.append(int(rate/grass_rate_sum*_generate_count))
            temp_count = temp_count - grass_num[len(grass_num) - 1]
        grass_num[0] += temp_count

        generate_attr_lv_min_sum = 0
        generate_attr_lv_distribution_sum = 0
        for item in generate_attr_lv_distribution:
            generate_attr_lv_min_sum += item[0]
            generate_attr_lv_distribution_sum += item[1]
        print(grass_num, evolution_num, generate_attr_lv_min_sum)

        evolution_temp_counter = 0
        data_total = []
        data_total.append([
            "ID",
            "name","desc","talent","grass","evolution",
            "hpMax","damage","defence","specialDamage","specialDefence","speed",
            "hpMaxLv","damageLv","defenceLv","specialDamageLv","specialDefenceLv","speedLv"
        ])

        def is_evolution_next(index):
            return (index == 1 or index == 2) and evolution_temp_counter != 0

        for i in range(1, generate_count+1):
            data = []
            id = generate_id_begin+i
            data.append(id)
            name_index = len(data)
            data.append("monster_"+str(id))
            data.append("this is desc")

            evolution_index = 0
            while True:
                if evolution_num[evolution_index] == 0:
                    evolution_index = evolution_index + 1
                    continue
                evolution_num[evolution_index] = evolution_num[evolution_index] - 1
                break
            # 天赋
            data.append("<0>")
            # grass
            if is_evolution_next(evolution_index):
                data.append(data_total[i-1][len(data)])
            else:
                grass_index = None
                while True:
                    grass_index = random.randrange(0,len(grass_num))
                    if grass_num[grass_index] == 0:
                        continue
                    grass_num[grass_index] = grass_num[grass_index] - 1
                    break
                data.append("<%d>" % (grass_index+1))
            # 进化链
            if evolution_index == 1 or evolution_index == 2:
                data[name_index] = "monster_%s_%s" % (id, evolution_temp_counter)
                if evolution_temp_counter == evolution_index:
                    data.append(id)
                else:
                    data.append(id+1)
            else:
                data.append(id)
            # 属性
            attr_index_list = [0,1,2,3,4,5]
            attr_base_list = []
            attr_lv_list = []
            # 基础属性
            for ii in attr_index_list:
                attr_base_list.append(1)
                attr_lv_list.append(0)
            data.extend(attr_base_list)
            # 属性成长
            temp_count = random.randrange(generate_attr_sum_min, generate_attr_sum_max)
            temp_min_sum = generate_attr_lv_min_sum
            temp_max_sum = generate_attr_lv_distribution_sum
            cn_index, cn_num = 0, 0
            random.shuffle(attr_index_list)
            for ii in attr_index_list:
                temp_min_sum -= generate_attr_lv_distribution[ii][0]
                temp_max_sum -= generate_attr_lv_distribution[ii][1]
                if is_evolution_next(evolution_index):
                    num = data_total[i-1][len(data)+ii]
                else:
                    range_l, range_r = generate_attr_lv_distribution[ii][0], min(temp_count-temp_min_sum, generate_attr_lv_distribution[ii][1])
                    if temp_max_sum < temp_count:
                        range_l = range_l + (temp_count - temp_max_sum)

                    if range_l == range_r:
                        num = range_l
                    else:
                        if range_l > range_r:
                            range_l, range_r = range_r, range_l
                        num = random.randrange(range_l, range_r)
                    temp_count = temp_count - num
                # CN: 统计属性成长
                if num > cn_num:
                    cn_num = num
                    cn_index = ii
                attr_lv_list[ii] = num
            data.extend(attr_lv_list)
            total_counter("attr_", cn_index, 1, default=0, desc={
                "attr_0": "hpMax",
                "attr_1": "damage",
                "attr_2": "defence",
                "attr_3": "specialDamage",
                "attr_4": "specialDefence",
                "attr_5": "speed",
            })
            id_counter(id, "attr_", cn_index, cn_num)
            id_counter(id, "id_", "", id)

            if evolution_index == 1 or evolution_index == 2:
                if evolution_index == evolution_temp_counter:
                    evolution_temp_counter = 0
                else:
                    evolution_temp_counter = evolution_temp_counter + 1

            data_total.append(data)

        for item in data_total:
            print(item)
        print("--------------------------------------")
        for k, v in cn_total_counter.items():
            if k == "id_counter":
                for kk in v:
                    print(v[kk])
            else:
                print(k, v)
            
        with open("generate_monster.csv", mode="w", encoding="utf-8",newline="") as f:
            # 基于打开的文件，创建csv.reader实例
            writer = csv.writer(f)
            writer.writerows(data_total)
            

        
        print(grass_num, evolution_num, sum(grass_num))
    elif generate_type == "monster_link":
        generate_count = 100                                                        # 个数
        generate_level_max = 100                                                    # 最大等级
        generate_attr_range = [200, 300]                                            # 属性范围
