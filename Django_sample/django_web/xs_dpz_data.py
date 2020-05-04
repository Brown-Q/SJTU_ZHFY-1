#coding:utf-8
from mongoengine import *
# Create your models here.
from mongoengine import connect
import re
from numpy import *
disconnect()
connect('court', host='202.121.180.66', port=7101)


class XSAJ(Document):
    年份 = StringField()
    日期 = StringField()
    省份 = StringField()
    法院名称 = StringField()
    案件类别 = StringField()
    案件数据 = StringField()
    头部信息 = StringField()
    当事人信息 = StringField()
    庭审过程 = StringField()
    尾部信息 = StringField()
    案由= StringField()

    meta = {
        'collection':'QY2','strict': False
    }

class XsDpzData:
    def __init__(self):
        CN_NUM = {
            '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '零': 0,
            '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '貮': 2, '两': 2,
        }
        CN_UNIT = {
            '十': 10,
            '拾': 10,
            '百': 100,
            '佰': 100,
            '千': 1000,
            '仠': 1000,
            '仟': 1000,
            '万': 10000,
            '萬': 10000,
            '亿': 100000000,
            '億': 100000000,
            '兆': 1000000000000,
        }
        self.CN_NUM = CN_NUM
        self.CN_UNIT = CN_UNIT

    def get_defendant_info(self, AY_str):
        d = []
        # print(str)
        for i in XSAJ.objects(Q(案由=AY_str)):
            a = i.当事人信息.split('、')
            # print(a)
            for j in a:
                if ('被告人' in j or '罪犯' in j or '被告' in j)and('男，' in j or '女，' in j):
                    c = {
                        'name':'未知','sex':'未知','birthdate':'未知','addr':'未知','age':'未知','nation':'未知','edu':'未知'
                    }
                    # print(j)
                    if ',' in j or '，' in j :
                        e = j.split('，')
                        b = []
                        for i in e:
                            for w in i.split(','):
                                b.append(w)
                        b[0] = b[0].replace('被告人','')
                        b[0] = b[0].replace('罪犯', '')
                        b[0] = b[0].replace('上诉人（原审）', '')
                        b[0] = b[0].replace('上诉人(原审)', '')
                        b[0] = b[0].replace('被告:', '')
                        b[0] = b[0].replace('被告', '')
                        c['name'] = b[0]
                        # print(b)
                        for k in b:
                            if '男'in k or '女' in k:
                                c['sex'] = k
                                # break
                            elif '出生' in k:
                                k1 = k.split('出生')
                                c['birthdate'] = k1[0]
                                if k1[1]:
                                    c['addr'] = re.sub('于','',k1[1])
                                if (c['birthdate'][:4].isdigit()) :
                                    c['age'] = str(2019 - int(c['birthdate'][:4]))
                                # break
                            elif '族' in k and len(k)<6:
                                c['nation'] = k
                                # break
                            elif '文化' in k and len(k)<6:
                                c['edu'] = k
                            elif '文盲' in k and len(k)<6:
                                c['edu'] = k
                                # break

                        d.append(c)
                        break
        return d

    def chinese_to_arabic(self, cn: str) -> int:
        unit = 0  # current
        ldig = []  # digest
        for cndig in reversed(cn):
            if cndig in self.CN_UNIT:
                unit = self.CN_UNIT.get(cndig)
                if unit == 10000 or unit == 100000000:
                    ldig.append(unit)
                    unit = 1
            else:
                dig = self.CN_NUM.get(cndig)
                if unit:
                    dig *= unit
                    unit = 0
                ldig.append(dig)
        if unit == 10:
            ldig.append(10)
        val, tmp = 0, 0
        for x in reversed(ldig):
            if x == 10000 or x == 100000000:
                val += tmp * x
                tmp = 0
            else:
                tmp += x
        val += tmp
        return val

    def prison_date(self, AY_str):
        prison = []
        for i in XSAJ.objects(Q(案由=AY_str)):
            for j in i.庭审过程.split('、'):
                if '被告人' in j:
                    for k in re.split('[,，；]', j):
                        if '判处' in k:
                            # print(k)
                            date = ''
                            if re.findall(r'判处(.*?)月',k):
                                date = re.findall(r'判处(.*?)月',k)[0]
                                date = date+'月'
                            elif re.findall(r'判处(.*?)年',k):
                                date = re.findall(r'判处(.*?)年', k)[0]
                                date = date + '年'
                            elif re.findall(r'判处(.*?)刑', k):
                                date1 = re.findall(r'判处(.*?)刑', k)[0]
                                if '死' in date1:
                                    date = '死刑'
                                elif '无期徒' in date1:
                                    date = '无期徒刑'
                            if len(date) <= 10 and date and ('�' not in date) and ('的' not in date) and (
                                    '被告人' not in date):
                                if date.startswith('拘') or date.startswith('有'):
                                    # print(date)
                                    prison.append(date)
        return prison

    def money_AJ(self, AY_str):
        money = []
        for i in XSAJ.objects(Q(案由='毒品罪')):
            for j in i.庭审过程.split('、'):
                if '被告人' in j:
                    for k in re.split('[,，；]', j):
                        # print(k)
                        if '罚金' in k and '�' not in k:
                            # print(k)
                            if re.findall(r'罚金(.*?)元', k):
                                # print(str(re.findall(r'罚金(.*?)元',k)[0]).replace('人民币',''))
                                str1 = str(re.findall(r'罚金(.*?)元', k)[0]).replace('人民币', '')
                                str1 = str1.replace('人币', '')
                                a = str1.replace('人民', '')
                                if 0 < len(a) <= 6:
                                    money.append(a)
                            elif bool(re.findall(r'处罚金(.*?)。', k)):
                                # print(str(re.findall(r'处罚金(.*?)。', k)[0]))
                                a = str(re.findall(r'处罚金(.*?)。', k)[0]).replace('人民币', '')
                                if 0 < len(a) <= 6:
                                    money.append(a)
        money_re = []
        for l in money:
            if l.isdigit():
                money_re.append(int(l))
            elif not re.compile(u'[^\u4e00-\u9fa5]').search(l):
                if '在' not in l and '各' not in l and '限' not in l and '的' not in l and '至' not in l and '已' not in l:
                    p = XsDpzData().chinese_to_arabic(l)
                    money_re.append(p)
        return money_re

    def get_case_sex_number(self, DPdefendant_info):
        count = 0
        b = {
            '男': 0,
            '女': 0,
            '未知': 0,
        }
        DPSEX = []

        for sex in DPdefendant_info:
            # print(sex['sex'])
            if sex['sex'] == '男':
                b['男'] = b['男'] + 1
            elif sex['sex'] == '女':
                b['女'] = b['女'] + 1
            else:
                b['未知'] = b['未知'] + 1
        # print(b)
        for bl in b:
            # print(bl)
            c = {}
            c['name'] = bl
            c['y'] = b[bl]
            DPSEX.append(c)
        return DPSEX

    def get_case_age_number(self, DPdefendant_info):
        DPAGE = []
        c = {
            '未知': 0,
            '20岁以下': 0,
            '21岁~30岁': 0,
            '31岁~40岁': 0,
            '41岁~50岁': 0,
            '51岁~60岁': 0,
            '60岁以上': 0,
        }
        for i in DPdefendant_info:
            if i['age'] == '未知':
                c['未知'] = c['未知'] + 1
            elif i['age'] <= '20':
                c['20岁以下'] = c['20岁以下'] + 1
            elif i['age'] <= '30':
                c['21岁~30岁'] = c['21岁~30岁'] + 1
            elif i['age'] <= '40':
                c['31岁~40岁'] = c['31岁~40岁'] + 1
            elif i['age'] <= '50':
                c['41岁~50岁'] = c['41岁~50岁'] + 1
            elif i['age'] <= '60':
                c['51岁~60岁'] = c['51岁~60岁'] + 1
            else:
                c['60岁以上'] = c['60岁以上'] + 1
        # print(c)
        DPAGE = []
        DPAGE.append(list(c.keys()))
        DPAGE.append(list(c.values()))
        return DPAGE

    def get_defendant_job(self):
        f = {'无业游民': 0, '工人': 0, '自营业主': 0, '教师': 0, '医生': 0, '农民': 0}
        # print(str)
        for i in XSAJ.objects(Q(案由='毒品罪')):
            a = i.当事人信息.split('、')
            # print(a)
            for j in a:
                if ('被告人' in j or '被告' in j) and ('男，' in j or '女，' in j):
                    c = {'edu': '未知'}
                    # print(j)
                    if ',' in j or '，' in j:
                        e = j.split('，')
                        b = []
                        for i in e:
                            for w in i.split(','):
                                b.append(w)
                        for k in b:
                            if '无业' in k and len(k) < 6:
                                f['无业游民'] += 1
                            elif '工人' in k and len(k) < 6:
                                f['工人'] += 1
                            elif '公司' in k and len(k) < 6:
                                f['自营业主'] += 1
                            elif '教师' in k and len(k) < 6:
                                f['教师'] += 1
                            elif '医生' in k and len(k) < 6:
                                f['医生'] += 1
                            elif '农民' in k and len(k) < 6:
                                f['农民'] += 1
                                # break
        return f

    def get_case_edu_number(self, DPdefendant_info):
        DPEDU = []
        c = {
            '未知': 0,
            '文盲': 0,
            '小学文化': 0,
            '中学文化': 0,
            '高中文化': 0,
            '大专文化': 0,
            '本科文化': 0,
            '研究生文化': 0,
        }

        for i in DPdefendant_info:
            if i['edu'] == '未知':
                c['未知'] = c['未知'] + 1
            elif i['edu'] == '文盲':
                c['文盲'] = c['文盲'] + 1
            elif i['edu'] in ['小学文化。', '小学文化']:
                c['小学文化'] = c['小学文化'] + 1
            elif i['edu'] in ['初中文化。', '初中文化', '中学文化', '中技文化']:
                c['中学文化'] = c['中学文化'] + 1
            elif i['edu'] in ['高中文化', '中专文化', '中专文化。', '高中文化。', '职高文化']:
                c['高中文化'] = c['高中文化'] + 1
            elif i['edu'] in ['大专文化', '专科文化', '大专文化。']:
                c['大专文化'] = c['大专文化'] + 1
            elif i['edu'] in ['大学文化', '本科文化', '本科文化。', '大学文化。', '大学本科文化']:
                c['本科文化'] = c['本科文化'] + 1
            elif i['edu'] in ['研究生文化']:
                c['研究生文化'] = c['研究生文化'] + 1
        for cl in c:
            # print(bl)
            d = {}
            d['name'] = cl
            d['y'] = c[cl]
            DPEDU.append(d)
        return DPEDU

    def get_case_sentence_date_number(self, DPprison_date_info):
        DPPDATE = []
        d = {}
        for i in DPprison_date_info:
            if i not in DPPDATE:
                DPPDATE.append(i)
                d[i] = 1
            else:
                d[i] = d[i] + 1
        # d= sorted(d.items(),key=lambda x:x[1],reverse=True)

        DPPDATE = []
        for cl in d:
            # print(bl)
            c = {}
            c['name'] = cl
            c['y'] = d[cl]
            DPPDATE.append(c)
        return DPPDATE

    def get_case_money(self, DPajmoney):
        DPAJMON = []
        d = {
            '少于1000元': 0,
            '1001元~5000元': 0,
            '5001元~10000元': 0,
            '10001元~20000元': 0,
            '20001元~30000元': 0,
            '30000元以上': 0,
        }
        for i in DPajmoney:
            if i <= 1000:
                d['少于1000元'] = d['少于1000元'] + 1
            elif i <= 5000:
                d['1001元~5000元'] = d['1001元~5000元'] + 1
            elif i <= 10000:
                d['5001元~10000元'] = d['5001元~10000元'] + 1
            elif i <= 20000:
                d['10001元~20000元'] = d['10001元~20000元'] + 1
            elif i <= 30000:
                d['20001元~30000元'] = d['20001元~30000元'] + 1
            elif i > 30000:
                d['30000元以上'] = d['30000元以上'] + 1

        for cl in d:
            # print(bl)
            c = {}
            c['name'] = cl
            c['y'] = d[cl]
            DPAJMON.append(c)
        return DPAJMON

    def get_court_pre_info(self):
        court = {}
        for i in XSAJ.objects(Q(案由='毒品罪')):
            if i.法院名称 in list(court.keys()):
                court[i.法院名称] += 1
            else:
                court[i.法院名称] = 1
        court_pre = sorted(court.items(), key=lambda k: k[1], reverse=True)
        return court_pre

    def get_court_info(self):
        # court = get_age_info()[0]
        court_pre = XsDpzData().get_court_pre_info()
        # [('重庆市北碚区人民法院', 707), ('重庆市万州区人民法院', 664), ('重庆市渝中区人民法院', 646), ('重庆市涪陵区人民法院', 444), ('重庆市高级人民法院', 6)]
        court = {}
        for i in court_pre:
            m = i[0].replace('人民法院', '')
            m = m.replace('重庆市', '')
            # print(court)
            if m == '第一中级':
                m = '渝北区'
            elif m == '第二中级':
                m = '万州区'
            elif m == '第三中级':
                m = '涪陵区'
            elif m == '第四中级':
                m = '黔江区'
            elif m == '第五中级':
                m='渝中区'
            elif m == '高级':
                m = '渝北区'
            for j in court.keys():
                if m[:2] in j:
                    court[j] = court[j] + i[1]
                    m = ''
                    break
            if m:
                court[m] = i[1]
        return court

    def get_map_data(self, court_l_data):
        map_data = []
        for i in court_l_data.keys():
            map_meta_data = {}
            map_meta_data['name'] = i
            map_meta_data['value'] = court_l_data[i]
            map_data.append(map_meta_data)
        return map_data

    def get_his_row_data(self, map_data):
        his_row_data = []
        his_region_data = []
        his_number_data = []
        for i in map_data:
            his_region_data.append(i['name'])
            his_number_data.append(i['value'])
        his_row_data = [his_region_data[0:5], his_number_data[0:5]]
        return his_row_data

    def get_case_date_number(self):
        case_date_number = {
            '2019': 0,
            '2018': 0,
            '2017': 0
        }
        for i in XSAJ.objects(Q(案由='毒品罪')):
            for j in i.尾部信息.split('、'):
                if ('年' in j) and ('月' in j) and ('日' in j) and ('二' in j):
                    if ('二○一九' in j) or ('二〇一九' in j):
                        case_date_number['2019'] += 1
                    elif ('二○一八' in j) or ('二〇一八' in j):
                        case_date_number['2018'] += 1
                    elif ('二○一七' in j) or ('二〇一七' in j):
                        case_date_number['2017'] += 1
                    break
        return case_date_number

    def get_line_data(self):
        line_data_dict = {}
        for i in XSAJ.objects(Q(案由='毒品罪')):
            a=i.头部信息.split('、')
            for j in a:
                if '（20' in j:
                    date = str(j.split('）')[0].replace('（', '')) + '年'
            if (date not in line_data_dict.keys()) and (len(date) < 7):
                line_data_dict[date] = 1
            elif date in line_data_dict.keys():
                line_data_dict[date] += 1
        line_data_tuple = sorted(line_data_dict.items(), key=lambda k: k[0])
        line_data = [[], []]
        for i in line_data_tuple:
            line_data[0].append(i[0])
            line_data[1].append(i[1])
        return line_data


class ChartRegion:
    def __init__(self, defendant_info):
        self.defendant_info = defendant_info

    def get_Fchart_data(self):
        DPpnumber = len(self.defendant_info)
        DPcasenum = XSAJ.objects(Q(案由='毒品罪')).count()
        court_data = XsDpzData().get_court_info()
        map_data = XsDpzData().get_map_data(court_data)
        his_row_data = XsDpzData().get_his_row_data(map_data)
        line_data = XsDpzData().get_line_data()
        Fchart_data = {
            'DPpnumber': DPpnumber,
            'DPcasenum': DPcasenum,
            'map_data': map_data,
            'his_row_data': his_row_data,
            'line_data': line_data,
        }
        return Fchart_data

    def get_Schart_data(self):
        DPsex = XsDpzData().get_case_sex_number(self.defendant_info)
        DPage = XsDpzData().get_case_age_number(self.defendant_info)
        DPedu = XsDpzData().get_case_edu_number(self.defendant_info)
        DPjob = [['无业游民', '工人', '自营业主', '教师', '医生', '农民'], [1985, 14, 9, 5, 5, 461]]
        Schart_data = {
            'DPSEX': DPsex,  # 当事人性别信息
            'DPJOB': DPjob,# 职业分布
            'DPEDU': DPedu,  # 教育程度
            'DPAGE': DPage,  # 年龄信息
        }
        return Schart_data

    def get_Tchart_data(self):
        DPajmoney = XsDpzData().money_AJ('毒品罪')
        DPprison_date_info = XsDpzData().prison_date('毒品罪')
        DPsentence = XsDpzData().get_case_sentence_date_number(DPprison_date_info)
        DPcasemoney = XsDpzData().get_case_money(DPajmoney)
        Tchart_data = {
            'DPsentence': DPsentence,
            'DPcasemoney': DPcasemoney,
        }
        return Tchart_data


# f=XsDpzData().get_defendant_job()
# job=list(f.keys())
# job_number=list(f.values())
# job_all=[job,job_number]
# print(job_all)
# DPdefendant_info = XsDpzData().get_defendant_info('毒品罪')
# F_chart_dpz_data = ChartRegion(DPdefendant_info).get_Fchart_data()
# S_chart_dpz_data = ChartRegion(DPdefendant_info).get_Schart_data()
# T_chart_dpz_data = ChartRegion(DPdefendant_info).get_Tchart_data()
# print(F_chart_dpz_data)
# print(S_chart_dpz_data)
# print(T_chart_dpz_data)
F_chart_dpz_data ={'DPpnumber': 6345, 'DPcasenum': 6566, 'map_data': [{'name': '渝中区', 'value': 1785}, {'name': '涪陵区', 'value': 988}, {'name': '渝北区', 'value': 1099}, {'name': '沙坪坝区', 'value': 340}, {'name': '九龙坡区', 'value': 331}, {'name': '江北区', 'value': 226}, {'name': '南岸区', 'value': 221}, {'name': '江津区', 'value': 131}, {'name': '合川区', 'value': 123}, {'name': '綦江区', 'value': 116}, {'name': '长寿区', 'value': 94}, {'name': '北碚区', 'value': 90}, {'name': '巴南区', 'value': 84}, {'name': '万州区', 'value': 106}, {'name': '永川区', 'value': 75}, {'name': '梁平区', 'value': 73}, {'name': '开州区', 'value': 55}, {'name': '奉节县', 'value': 48}, {'name': '大足区', 'value': 48}, {'name': '荣昌县', 'value': 47}, {'name': '南川区', 'value': 46}, {'name': '丰都县', 'value': 45}, {'name': '铜梁县', 'value': 45}, {'name': '璧山区', 'value': 42}, {'name': '石柱土家族自治县', 'value': 38}, {'name': '垫江县', 'value': 36}, {'name': '大渡口区', 'value': 36}, {'name': '潼南县', 'value': 27}, {'name': '忠县', 'value': 25}, {'name': '巫山县', 'value': 24}, {'name': '黔江区', 'value': 40}, {'name': '云阳县', 'value': 23}, {'name': '秀山土家族苗族自治县', 'value': 21}, {'name': '彭水苗族土家族自治县', 'value': 11}, {'name': '巫溪县', 'value': 9}, {'name': '武隆区', 'value': 9}, {'name': '酉阳土家族苗族自治县', 'value': 6}, {'name': '重庆铁路运输法院', 'value': 2}, {'name': '城口县', 'value': 1}], 'his_row_data': [['渝中区', '涪陵区', '渝北区', '沙坪坝区', '九龙坡区'], [1785, 988, 1099, 340, 331]], 'line_data': [['2017年', '2018年', '2019年'], [1215, 4216, 999]]}
S_chart_dpz_data ={'DPSEX': [{'name': '男', 'y': 5477}, {'name': '女', 'y': 492}, {'name': '未知', 'y': 376}], 'DPJOB': [['无业游民', '工人', '自营业主', '教师', '医生', '农民'], [1985, 14, 9, 5, 5, 461]], 'DPEDU': [{'name': '未知', 'y': 3239}, {'name': '文盲', 'y': 68}, {'name': '小学文化', 'y': 665}, {'name': '中学文化', 'y': 1702}, {'name': '高中文化', 'y': 599}, {'name': '大专文化', 'y': 55}, {'name': '本科文化', 'y': 14}, {'name': '研究生文化', 'y': 0}], 'DPAGE': [['未知', '20岁以下', '21岁~30岁', '31岁~40岁', '41岁~50岁', '51岁~60岁', '60岁以上'], [421, 25, 1106, 1925, 1803, 902, 163]]}
T_chart_dpz_data ={'DPsentence': [{'name': '有期徒刑七年', 'y': 156}, {'name': '有期徒刑一年七个月', 'y': 27}, {'name': '有期徒刑十五年', 'y': 465}, {'name': '有期徒刑一年一个月', 'y': 117}, {'name': '有期徒刑八年六个月', 'y': 47}, {'name': '有期徒刑八个月', 'y': 702}, {'name': '有期徒刑七个月', 'y': 741}, {'name': '有期徒刑六个月', 'y': 1120}, {'name': '有期徒刑七年二个月', 'y': 25}, {'name': '有期徒刑五年', 'y': 29}, {'name': '拘役六个月', 'y': 52}, {'name': '有期徒刑二年', 'y': 139}, {'name': '有期徒刑十年', 'y': 76}, {'name': '有期徒刑七年六个月', 'y': 139}, {'name': '有期徒刑二年二个月', 'y': 23}, {'name': '有期徒刑九个月', 'y': 461}, {'name': '有期徒刑七年五个月', 'y': 2}, {'name': '有期徒刑八年', 'y': 124}, {'name': '有期徒刑一年', 'y': 395}, {'name': '有期徒刑十个月', 'y': 393}, {'name': '有期徒刑七年十个月', 'y': 21}, {'name': '有期徒刑十四年', 'y': 28}, {'name': '有期徒刑七年七个月', 'y': 4}, {'name': '有期徒刑二年六个月', 'y': 72}, {'name': '有期徒刑八年九个月', 'y': 4}, {'name': '有期徒刑三年', 'y': 131}, {'name': '有期徒刑十二年', 'y': 53}, {'name': '有期徒刑五年六个月', 'y': 20}, {'name': '有期徒刑九年', 'y': 72}, {'name': '有期徒刑一年二个月', 'y': 170}, {'name': '有期徒刑十一个月', 'y': 190}, {'name': '有期徒刑二年四个月', 'y': 17}, {'name': '拘役五个月', 'y': 205}, {'name': '有期徒刑一年六个月', 'y': 165}, {'name': '有期徒刑一年四个月', 'y': 107}, {'name': '有期徒刑一年五个月', 'y': 53}, {'name': '有期徒刑一年三个月', 'y': 91}, {'name': '有期徒刑一年十一个月', 'y': 11}, {'name': '有期徒刑一年八个月', 'y': 62}, {'name': '拘役四个月', 'y': 105}, {'name': '有期徒刑六年', 'y': 26}, {'name': '有期徒刑二年五个月', 'y': 9}, {'name': '有期徒刑二年八个月', 'y': 13}, {'name': '有期徒刑二年十个月', 'y': 25}, {'name': '有期徒刑三年六个月', 'y': 67}, {'name': '拘役三个月', 'y': 29}, {'name': '有期徒刑三年九个月', 'y': 4}, {'name': '有期徒刑六年十个月', 'y': 1}, {'name': '有期徒刑二年三个月', 'y': 27}, {'name': '有期徒刑十一年', 'y': 40}, {'name': '有期徒刑四年六个月', 'y': 21}, {'name': '有期徒刑七年八个月', 'y': 11}, {'name': '有期徒刑四年', 'y': 38}, {'name': '有期徒刑一年十个月', 'y': 47}, {'name': '有期徒刑七年四个月', 'y': 5}, {'name': '有期徒刑八年四个月', 'y': 5}, {'name': '有期徒刑四年八个月', 'y': 3}, {'name': '有期徒刑十一年八个月', 'y': 1}, {'name': '有期徒刑七年九个月', 'y': 3}, {'name': '拘役二个月', 'y': 12}, {'name': '有期徒刑十年十个月', 'y': 1}, {'name': '有期徒刑七年三个月', 'y': 22}, {'name': '有期徒刑二年九个月', 'y': 5}, {'name': '有期徒刑十年六个月', 'y': 13}, {'name': '有期徒刑三年四个月', 'y': 7}, {'name': '有期徒刑三年十个月', 'y': 4}, {'name': '有期徒刑十三年', 'y': 41}, {'name': '有期徒刑九年六个月', 'y': 13}, {'name': '有期徒一年四个月', 'y': 2}, {'name': '有期徒刑十一年三个月', 'y': 2}, {'name': '有期徒刑十一年六个月', 'y': 7}, {'name': '有期徒刑六年四个月', 'y': 1}, {'name': '有期徒刑六年九个月', 'y': 1}, {'name': '有期徒刑八年八个月', 'y': 4}, {'name': '有期徒刑三年五个月', 'y': 4}, {'name': '有期徒刑十三年六个月', 'y': 15}, {'name': '有期徒刑九年八个月', 'y': 2}, {'name': '有期徒刑三年八个月', 'y': 4}, {'name': '有期徒刑二年一个月', 'y': 6}, {'name': '有期徒刑三年三个月', 'y': 19}, {'name': '有期徒刑六年六个月', 'y': 11}, {'name': '有期徒刑十一年九个月', 'y': 1}, {'name': '有期徒刑八年三个月', 'y': 6}, {'name': '有期徒刑七月', 'y': 1}, {'name': '有期徒刑八年二个月', 'y': 2}, {'name': '有期徒刑七至八年', 'y': 1}, {'name': '有期徒刑一年九个月', 'y': 22}, {'name': '有期徒刑十三年四个月', 'y': 1}, {'name': '有期徒刑九年四个月', 'y': 2}, {'name': '有期徒刑七年零十个月', 'y': 1}, {'name': '有期徒刑年六个月', 'y': 1}, {'name': '有期徒刑十六年', 'y': 1}, {'name': '有期徒刑一年两个月', 'y': 1}, {'name': '有期徒刑二年七个月', 'y': 3}, {'name': '有期徒刑二个月', 'y': 1}, {'name': '有期徒刑一年零六个月', 'y': 6}, {'name': '有期徒刑十四年二个月', 'y': 1}, {'name': '有期徒八年六个月', 'y': 1}, {'name': '有期徒刑七年一个月', 'y': 2}, {'name': '有期徒刑十四年六个月', 'y': 4}, {'name': '有期徒刑五年十个月', 'y': 1}, {'name': '有期徒刑五年九个月', 'y': 1}, {'name': '有期徒刑十二年六个月', 'y': 10}, {'name': '有期徒刑八年十个月', 'y': 3}, {'name': '有期徒刑五年二个月', 'y': 2}, {'name': '有期徒刑三年二个月', 'y': 7}, {'name': '有期徒七年六个月', 'y': 1}, {'name': '有期徒刑四年四个月', 'y': 2}, {'name': '有期徒刑十年八个月', 'y': 1}, {'name': '有期徒刑十五年四个月', 'y': 1}, {'name': '有期徒刑八年五个月', 'y': 2}, {'name': '有期徒刑六年五个月', 'y': 1}, {'name': '有期徒刑四年三个月', 'y': 3}, {'name': '有期徒刑十五个年', 'y': 1}, {'name': '拘役一个月', 'y': 3}, {'name': '有期徒刑六月', 'y': 1}, {'name': '有期徒九个月', 'y': 1}, {'name': '有期徒刑两年', 'y': 1}, {'name': '有期徒刑十三年三个月', 'y': 1}, {'name': '有期徒七年', 'y': 1}, {'name': '有期徒刑四年七个月', 'y': 1}, {'name': '有期徒刑十五年六个月', 'y': 1}, {'name': '有期徒刑十二年三个月', 'y': 1}, {'name': '有期徒刑八月', 'y': 1}, {'name': '有期徒刑二年十一个月', 'y': 6}, {'name': '有期徒刑七年十一个月', 'y': 1}, {'name': '有期徒刑五年三个月', 'y': 1}, {'name': '有期徒刑九年九个月', 'y': 1}, {'name': '有期徒刑四年五个月', 'y': 1}, {'name': '有期徒刑九年三个月', 'y': 2}, {'name': '有期徒刑六年八个月', 'y': 1}, {'name': '有期徒刑十二年八个月', 'y': 1}, {'name': '有期徒刑二年零六个月', 'y': 1}, {'name': '有期徒刑五年五个月', 'y': 1}, {'name': '有期徒刑四年十个月', 'y': 1}, {'name': '有期徒刑两年十个月', 'y': 1}, {'name': '有期徒八年', 'y': 1}, {'name': '有期徒刑四年九个月', 'y': 2}, {'name': '拘役一年', 'y': 1}, {'name': '有期刑八个月', 'y': 1}, {'name': '有期徒刑十五年二个月', 'y': 1}, {'name': '有期徒刑6个月', 'y': 1}, {'name': '有期徒刑7个月', 'y': 1}, {'name': '有期徒刑11个月', 'y': 1}, {'name': '有期徒刑1年4个月', 'y': 1}, {'name': '拘役十个月', 'y': 1}], 'DPcasemoney': [{'name': '少于1000元', 'y': 1102}, {'name': '1001元~5000元', 'y': 4511}, {'name': '5001元~10000元', 'y': 747}, {'name': '10001元~20000元', 'y': 201}, {'name': '20001元~30000元', 'y': 45}, {'name': '30000元以上', 'y': 67}]}
