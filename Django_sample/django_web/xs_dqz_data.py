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



class XsDqaData:
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
                            if len(date)<=10 and date and ('�' not in date) and ('的' not in date) and ('被告人' not in date):
                                if date.startswith('拘') or date.startswith('有'):
                                    # print(date)
                                    prison.append(date)
        return prison

    def money_AJ(self, AY_str):
        money = []
        for i in XSAJ.objects(Q(案由=AY_str)):
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
        # print(money)
        money.remove('二千并罚')
        # money.remove('限被告人赖')
        # money.remove('限被告人赖')
        money_re = []
        for l in money:
            if l.isdigit():
                money_re.append(int(l))
            elif not re.compile(u'[^\u4e00-\u9fa5]').search(l):
                if '在' not in l and '各' not in l and '限' not in l and '的' not in l and '至' not in l and '已' not in l:
                    p = XsDqaData().chinese_to_arabic(l)
                    # print(p)
                    money_re.append(p)
        return money_re

    def get_case_sex_number(self, DQdefendant_info):
        count = 0
        b = {
            '男': 0,
            '女': 0,
            '未知': 0,
        }
        DQSEX = []

        for sex in DQdefendant_info:
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
            DQSEX.append(c)
        return DQSEX

    def get_case_age_number(self, DQdefendant_info):
        DQAGE = []
        c = {
            '未知': 0,
            '20岁以下': 0,
            '21岁~30岁': 0,
            '31岁~40岁': 0,
            '41岁~50岁': 0,
            '51岁~60岁': 0,
            '60岁以上': 0,
        }
        for i in DQdefendant_info:
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
        DQAGE = []
        DQAGE.append(list(c.keys()))
        DQAGE.append(list(c.values()))
        return DQAGE

    def get_defendant_job(self):
        f = {'无业游民': 0, '工人': 0, '自营业主': 0, '教师': 0, '医生': 0, '农民': 0}
        # print(str)
        for i in XSAJ.objects(Q(案由='盗窃罪')):
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

    def get_case_edu_number(self, DQdefendant_info):
        DQEDU = []
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

        for i in DQdefendant_info:
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
            DQEDU.append(d)
        return DQEDU

    def get_case_sentence_date_number(self, DQprison_date_info):
        DQPDATE = []
        d = {}
        for i in DQprison_date_info:
            if i not in DQPDATE:
                DQPDATE.append(i)
                d[i] = 1
            else:
                d[i] = d[i] + 1
        # d= sorted(d.items(),key=lambda x:x[1],reverse=True)

        DQPDATE = []
        for cl in d:
            # print(bl)
            c = {}
            c['name'] = cl
            c['y'] = d[cl]
            DQPDATE.append(c)
        return DQPDATE

    def get_case_money(self, DQajmoney):
        DQAJMON = []
        d = {
            '少于1000元': 0,
            '1001元~5000元': 0,
            '5001元~10000元': 0,
            '10001元~20000元': 0,
            '20001元~30000元': 0,
            '30000元以上': 0,
        }
        for i in DQajmoney:
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
            DQAJMON.append(c)
        return DQAJMON

    def get_court_pre_info(self):
        court = {}
        for i in XSAJ.objects(Q(案由='盗窃罪')):
            if i.法院名称 in list(court.keys()):
                court[i.法院名称] += 1
            else:
                court[i.法院名称] = 1
        court_pre = sorted(court.items(), key=lambda k: k[1], reverse=True)
        return court_pre

    def get_court_info(self):
        # court = get_age_info()[0]
        court_pre = XsDqaData().get_court_pre_info()
        court = {}
        for i in court_pre:
            m = i[0].replace('区', '')
            m = m.replace('重庆市', '')
            m = m.replace('人民法院', '')
            m = m.replace('自治县', '')
            m = m.replace('市', '')
            m = m.replace('苗族', '')
            m = m.replace('土家族', '')
            m = m.replace('中华人民共和国', '')
            # print(court)
            if m == '第一中级':
                m = '渝北'
            elif m == '第二中级':
                m = '万州'
            elif m == '第三中级':
                m = '涪陵'
            elif m == '第四中级':
                m = '黔江'
            elif m == '第五中级':
                m = '渝中'
            elif m == '高级':
                m = '渝北'
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
        court_l_data.pop('重庆铁路运输法院')
        for i,j in court_l_data.items():
                NOname = {}
                if i != '酉阳' and i != '秀山' and '县' not in i and len(i) < 5:
                    NOname['name'] = i + '区'
                else:
                    NOname['name'] = i
                NOname['value'] = j
                # print(NOname)
                map_data.append(NOname)
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
            '2017': 0,
            '2016': 0
        }
        for i in XSAJ.objects(Q(案由='盗窃罪')):
            for j in i.尾部信息.split('、'):
                if ('年' in j) and ('月' in j) and ('日' in j) and ('二' in j):
                    if ('二一九' in j) or ('二一九' in j):
                        case_date_number['2019'] += 1
                    if ('二一八' in j) or ('二一八' in j):
                        case_date_number['2018'] += 1
                    elif ('二一七' in j) or ('二一七' in j):
                        case_date_number['2017'] += 1
                    elif ('二一六' in j) or ('二一六' in j):
                        case_date_number['2016'] += 1
                    break
        return case_date_number

    def get_line_data(self):
        line_data_dict = {}
        for i in XSAJ.objects(Q(案由='盗窃罪')):
            a = i.头部信息.split('、')
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
        DQpnumber = len(self.defendant_info)
        DQcasenum = XSAJ.objects(Q(案由='盗窃罪')).count()
        court_data = XsDqaData().get_court_info()
        map_data = XsDqaData().get_map_data(court_data)
        his_row_data = XsDqaData().get_his_row_data(map_data)
        line_data = XsDqaData().get_line_data()
        Fchart_data = {
            'DQpnumber': DQpnumber,
            'DQcasenum': DQcasenum,
            'map_data': map_data,
            'his_row_data': his_row_data,
            'line_data': line_data,
        }
        return Fchart_data

    def get_Schart_data(self):
        DQsex = XsDqaData().get_case_sex_number(self.defendant_info)
        DQage = XsDqaData().get_case_age_number(self.defendant_info)
        DQedu = XsDqaData().get_case_edu_number(self.defendant_info)
        DQjob = [['无业游民', '工人', '自营业主', '教师', '医生', '农民'], [3118, 47, 19, 1, 0, 1141]]
        Schart_data = {
            'DQSEX': DQsex,  # 当事人性别信息
            'DQJOB': DQjob,# 职业分布
            'DQEDU': DQedu,  # 教育程度
            'DQAGE': DQage,  # 年龄信息
        }
        return Schart_data

    def get_Tchart_data(self):
        DQajmoney = XsDqaData().money_AJ('盗窃罪')
        DQprison_date_info = XsDqaData().prison_date('盗窃罪')
        DQsentence = XsDqaData().get_case_sentence_date_number(DQprison_date_info)
        DQcasemoney = XsDqaData().get_case_money(DQajmoney)
        Tchart_data = {
            'DQsentence': DQsentence,
            'DQcasemoney': DQcasemoney,
        }
        return Tchart_data


#
# f=XsDqaData().get_defendant_job()
# job=list(f.keys())
# job_number=list(f.values())
# job_all=[job,job_number]
# print(job_all)
# DQdefendant_info = XsDqaData().get_defendant_info('盗窃罪')
# F_chart_dqz_data = ChartRegion(DQdefendant_info).get_Fchart_data()
# S_chart_dqz_data = ChartRegion(DQdefendant_info).get_Schart_data()
# T_chart_dqz_data = ChartRegion(DQdefendant_info).get_Tchart_data()
# print(F_chart_dqz_data)
# print(S_chart_dqz_data)
# print(T_chart_dqz_data)
F_chart_dqz_data ={'DQpnumber': 8501, 'DQcasenum': 8830, 'map_data': [{'name': '沙坪坝区', 'value': 638}, {'name': '渝中区', 'value': 1089}, {'name': '渝北区', 'value': 793}, {'name': '九龙坡区', 'value': 535}, {'name': '南岸区', 'value': 532}, {'name': '涪陵区', 'value': 550}, {'name': '江津区', 'value': 332}, {'name': '江北区', 'value': 330}, {'name': '万州区', 'value': 326}, {'name': '合川区', 'value': 295}, {'name': '北碚区', 'value': 257}, {'name': '綦江区', 'value': 232}, {'name': '永川区', 'value': 230}, {'name': '璧山区', 'value': 202}, {'name': '荣昌县', 'value': 191}, {'name': '长寿区', 'value': 186}, {'name': '大足区', 'value': 171}, {'name': '开州区', 'value': 165}, {'name': '潼南县', 'value': 162}, {'name': '巴南区', 'value': 149}, {'name': '铜梁县', 'value': 129}, {'name': '奉节县', 'value': 128}, {'name': '梁平区', 'value': 122}, {'name': '垫江县', 'value': 122}, {'name': '云阳县', 'value': 117}, {'name': '南川区', 'value': 106}, {'name': '丰都县', 'value': 98}, {'name': '忠县', 'value': 79}, {'name': '秀山', 'value': 76}, {'name': '黔江区', 'value': 80}, {'name': '大渡口区', 'value': 67}, {'name': '石柱区', 'value': 66}, {'name': '彭水区', 'value': 56}, {'name': '巫山县', 'value': 54}, {'name': '酉阳', 'value': 52}, {'name': '巫溪县', 'value': 37}, {'name': '城口县', 'value': 32}, {'name': '武隆区', 'value': 13}], 'his_row_data': [['沙坪坝区', '渝中区', '渝北区', '九龙坡区', '南岸区'], [638, 1089, 793, 535, 532]], 'line_data': [['2017年', '2018年', '2019年'], [1394, 5896, 1400]]}
S_chart_dqz_data ={'DQSEX': [{'name': '男', 'y': 7939}, {'name': '女', 'y': 429}, {'name': '未知', 'y': 133}], 'DQJOB': [['无业游民', '工人', '自营业主', '教师', '医生', '农民'], [3118, 47, 19, 1, 0, 1141]], 'DQEDU': [{'name': '未知', 'y': 3203}, {'name': '文盲', 'y': 456}, {'name': '小学文化', 'y': 1854}, {'name': '中学文化', 'y': 2306}, {'name': '高中文化', 'y': 565}, {'name': '大专文化', 'y': 84}, {'name': '本科文化', 'y': 27}, {'name': '研究生文化', 'y': 0}], 'DQAGE': [['未知', '20岁以下', '21岁~30岁', '31岁~40岁', '41岁~50岁', '51岁~60岁', '60岁以上'], [869, 224, 2370, 1924, 1910, 941, 263]]}
T_chart_dqz_data ={'DQsentence': [{'name': '有期徒刑十一年', 'y': 53}, {'name': '有期徒刑十三年', 'y': 36}, {'name': '有期徒刑一年六个月', 'y': 247}, {'name': '拘役四个月', 'y': 1614}, {'name': '有期徒刑十个月', 'y': 836}, {'name': '有期徒刑七年六个月', 'y': 13}, {'name': '有期徒刑八个月', 'y': 1590}, {'name': '有期徒刑七个月', 'y': 2010}, {'name': '有期徒刑一年四个月', 'y': 101}, {'name': '有期徒刑五年六个月', 'y': 26}, {'name': '有期徒刑四年六个月', 'y': 66}, {'name': '有期徒刑六个月', 'y': 2589}, {'name': '有期徒刑十一个月', 'y': 311}, {'name': '有期徒刑十四年', 'y': 18}, {'name': '有期徒刑五年三个月', 'y': 1}, {'name': '拘役三个月', 'y': 1221}, {'name': '有期徒刑十年', 'y': 64}, {'name': '有期徒刑十二年八个月', 'y': 2}, {'name': '有期徒刑一年', 'y': 617}, {'name': '有期徒刑三年六个月', 'y': 107}, {'name': '拘役五个月', 'y': 1168}, {'name': '有期徒刑九个月', 'y': 809}, {'name': '有期徒刑一年二个月', 'y': 221}, {'name': '有期徒刑一年三个月', 'y': 130}, {'name': '有期徒刑十年六个月', 'y': 32}, {'name': '有期徒刑三年', 'y': 186}, {'name': '有期徒刑六年', 'y': 59}, {'name': '有期徒刑一年七个月', 'y': 31}, {'name': '有期徒刑四年', 'y': 89}, {'name': '有期徒刑二年四个月', 'y': 27}, {'name': '有期徒刑三年八个月', 'y': 16}, {'name': '有期徒刑十一年六个月', 'y': 11}, {'name': '拘役二个月', 'y': 330}, {'name': '有期徒刑五年八个月', 'y': 1}, {'name': '有期徒刑八年', 'y': 17}, {'name': '有期徒刑三年三个月', 'y': 13}, {'name': '有期徒刑一年一个月', 'y': 107}, {'name': '拘役一个月', 'y': 43}, {'name': '有期徒刑二年六个月', 'y': 87}, {'name': '有期徒刑九年', 'y': 16}, {'name': '有期徒刑十二年六个月', 'y': 18}, {'name': '有期徒刑二年', 'y': 146}, {'name': '有期徒刑十二年', 'y': 57}, {'name': '有期徒刑一年八个月', 'y': 73}, {'name': '拘役八个月', 'y': 1}, {'name': '拘役六个月', 'y': 275}, {'name': '有期徒刑一年五个月', 'y': 60}, {'name': '有期徒刑五年', 'y': 64}, {'name': '有期徒刑二年二个月', 'y': 16}, {'name': '有期徒刑三年十个月', 'y': 23}, {'name': '有期徒刑四年二个月', 'y': 2}, {'name': '拘役二至四个月', 'y': 4}, {'name': '拘役三至五个月', 'y': 3}, {'name': '拘役四至六个月', 'y': 7}, {'name': '有期徒刑一年十个月', 'y': 67}, {'name': '有期徒刑四年八个月', 'y': 10}, {'name': '有期徒刑三年九个月', 'y': 7}, {'name': '有期徒刑7个月', 'y': 2}, {'name': '有期徒刑二年一个月', 'y': 10}, {'name': '有期徒刑十一月', 'y': 1}, {'name': '有期徒刑八年四个月', 'y': 1}, {'name': '有期徒刑七至九个月', 'y': 4}, {'name': '有期徒刑六至八个月', 'y': 5}, {'name': '有期徒刑七年', 'y': 29}, {'name': '有期徒刑六年六个月', 'y': 8}, {'name': '有期徒刑三年七个月', 'y': 11}, {'name': '拘役三至四个月', 'y': 3}, {'name': '有期徒六个月', 'y': 4}, {'name': '有期徒刑十一年七个月', 'y': 3}, {'name': '有期徒刑三年一个月', 'y': 8}, {'name': '有期徒刑十三年六个月', 'y': 13}, {'name': '有期徒刑五年九个月', 'y': 2}, {'name': '有期徒刑十四年六个月', 'y': 9}, {'name': '有期徒刑四年三个月', 'y': 11}, {'name': '有期徒刑六年八个月', 'y': 2}, {'name': '有期徒刑三年四个月', 'y': 24}, {'name': '有期徒刑三年五个月', 'y': 4}, {'name': '有期徒刑二年十个月', 'y': 21}, {'name': '有期徒刑三年二个月', 'y': 18}, {'name': '有期徒刑二年三个月', 'y': 21}, {'name': '有期徒刑二年九个月', 'y': 4}, {'name': '有期徒刑二年五个月', 'y': 12}, {'name': '有期徒刑八年六个月', 'y': 3}, {'name': '有期徒刑一年九个月', 'y': 25}, {'name': '有期徒刑十七年', 'y': 1}, {'name': '有期徒刑九至十个月', 'y': 2}, {'name': '有期徒刑一年十一个月', 'y': 4}, {'name': '拘役3个月', 'y': 1}, {'name': '有期徒刑六个六个月', 'y': 1}, {'name': '有期徒刑十六年', 'y': 1}, {'name': '有期徒刑十三年八个月', 'y': 1}, {'name': '有期徒刑十年三个月', 'y': 6}, {'name': '有期徒刑二年八个月', 'y': 13}, {'name': '有期徒刑十年十个月', 'y': 2}, {'name': '有拘役二个月', 'y': 2}, {'name': '有期徒刑六年四个月', 'y': 1}, {'name': '有期徒刑八至十个月', 'y': 3}, {'name': '有期徒刑一年零三个月', 'y': 3}, {'name': '有期徒刑二年零四个月', 'y': 1}, {'name': '有期徒刑十二年二个月', 'y': 1}, {'name': '有期有期徒刑十二年', 'y': 1}, {'name': '有期拘役四个月', 'y': 2}, {'name': '有期徒刑二年七个月', 'y': 5}, {'name': '拘役一年', 'y': 1}, {'name': '有期徒刑十年九个月', 'y': 1}, {'name': '有期徒刑徒刑六个月', 'y': 1}, {'name': '有期徒刑十一年八个月', 'y': 2}, {'name': '有期徒九年四个月', 'y': 1}, {'name': '拘投五个月', 'y': 1}, {'name': '有期徒刑十一年四个月', 'y': 2}, {'name': '有期徒刑十年八个月', 'y': 2}, {'name': '有期徒刑十年十一个月', 'y': 1}, {'name': '有期徒刑六年十个月', 'y': 2}, {'name': '有期徒刑十五年', 'y': 12}, {'name': '有拘役五个月', 'y': 3}, {'name': '有有期徒刑六个月', 'y': 1}, {'name': '有期徒刑四年九个月', 'y': 3}, {'name': '有拘役六个月', 'y': 2}, {'name': '有期徒刑一年零七个月', 'y': 1}, {'name': '有期徒刑一年零四个月', 'y': 1}, {'name': '有期徒刑四年四个月', 'y': 5}, {'name': '有期徒刑4年', 'y': 2}, {'name': '有期徒刑1年', 'y': 1}, {'name': '拘役二至三个月', 'y': 5}, {'name': '有期徒刑六年九个月', 'y': 1}, {'name': '有期徒刑四年十个月', 'y': 6}, {'name': '有期徒刑九年六个月', 'y': 3}, {'name': '有期限徒刑六个月', 'y': 1}, {'name': '有期徒三年', 'y': 1}, {'name': '有期徒刑2年', 'y': 1}, {'name': '有期徒刑七至八个月', 'y': 2}, {'name': '拘四个月', 'y': 1}, {'name': '有期徒刑有期徒刑一年', 'y': 1}, {'name': '有期徒刑八月', 'y': 10}, {'name': '拘役七个月', 'y': 1}, {'name': '拘役一至二个月', 'y': 1}, {'name': '有期徒刑十一年九个月', 'y': 2}, {'name': '有期徒刑五年四个月', 'y': 1}, {'name': '拘役四月', 'y': 1}, {'name': '有期徒刑一年零二个月', 'y': 1}, {'name': '有期徒刑九年八个月', 'y': 1}, {'name': '有期徒刑六年三个月', 'y': 1}, {'name': '有期徒刑十三年二个月', 'y': 2}, {'name': '有期徒刑十七年六个月', 'y': 1}, {'name': '有期徒刑十年四个月', 'y': 1}, {'name': '有期徒刑七年二个月', 'y': 1}, {'name': '有期徒刑十年七个月', 'y': 1}, {'name': '有期徒刑十年二个月', 'y': 2}, {'name': '有期徒刑四年十一个月', 'y': 2}, {'name': '有期徒刑十一年三个月', 'y': 1}, {'name': '有期徒刑五年十个月', 'y': 1}, {'name': '有期徒刑五年一个月', 'y': 1}, {'name': '有期徒刑十四年二个月', 'y': 1}, {'name': '有期徒刑六年七个月', 'y': 1}, {'name': '有期徒刑十一年五个月', 'y': 1}, {'name': '有期徒刑五年二个月', 'y': 2}, {'name': '拘役13个月', 'y': 1}, {'name': '拘役十个月', 'y': 2}, {'name': '有期徒刑二年十一个月', 'y': 1}, {'name': '有期徒刑1年6个月', 'y': 1}, {'name': '有期徒刑10年', 'y': 1}, {'name': '有期徒刑七年零六个月', 'y': 1}, {'name': '有期徒刑十一年十个月', 'y': 2}, {'name': '有期徒刑三年十一个月', 'y': 2}, {'name': '拘役十一个月', 'y': 1}, {'name': '有期徒刑6年', 'y': 1}, {'name': '有期徒刑8个月', 'y': 1}, {'name': '有其徒刑三年六个月', 'y': 1}, {'name': '有期徒刑9年', 'y': 1}, {'name': '拘役五至六个月', 'y': 1}, {'name': '有期徒刑四年五个月', 'y': 2}, {'name': '有拘役三个月', 'y': 4}, {'name': '有期徒刑三个月', 'y': 1}, {'name': '有期徒刑十二年九个月', 'y': 1}, {'name': '有期徒刑十三年七个月', 'y': 1}, {'name': '有期徒刑五年七个月', 'y': 1}, {'name': '拘役有期徒刑六个月', 'y': 1}, {'name': '有期徒刑十五年三个月', 'y': 1}, {'name': '有期徒十一年四个月', 'y': 1}, {'name': '拘役6个月', 'y': 1}, {'name': '有期徒刑6个月', 'y': 2}, {'name': '拘拘役三个月', 'y': 1}, {'name': '有期徒刑一年零六个月', 'y': 1}, {'name': '有拘役四个月', 'y': 3}, {'name': '有期徒十年六个月', 'y': 1}, {'name': '有期徒刑四年一个月', 'y': 1}], 'DQcasemoney': [{'name': '少于1000元', 'y': 4309}, {'name': '1001元~5000元', 'y': 10209}, {'name': '5001元~10000元', 'y': 1756}, {'name': '10001元~20000元', 'y': 666}, {'name': '20001元~30000元', 'y': 208}, {'name': '30000元以上', 'y': 218}]}











