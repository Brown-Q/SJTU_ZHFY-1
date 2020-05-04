#-*- coding:utf-8 -*-
import re
from mongoengine import *
disconnect()
connect('court', host='202.121.180.66', port=7101)

class CPJF(Document):
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
    案由 = StringField()

    meta = {
        'collection': 'QY2', 'strict': False
    }


class MsCpjfData:
    def __init__(self):
        pass

    def age_dict_get(self, age_dict):
        DICTAGE = {
            '20岁以下': 0,
            '20~30岁': 0,
            '31~40岁': 0,
            '41~50岁': 0,
            '51~60岁': 0,
            '61~70岁': 0,
            '70岁以上': 0,
        }
        for j,k in age_dict.items():
            if int(j)<20:
                DICTAGE['20岁以下'] = DICTAGE['20岁以下']+k
            elif int(j)>=20 and int(j)<=30:
                DICTAGE['20~30岁'] = DICTAGE['20~30岁'] +k
            elif int(j)>30 and int(j)<=40:
                DICTAGE['31~40岁'] = DICTAGE['31~40岁'] + k
            elif int(j)>40 and int(j)<=50:
                DICTAGE['41~50岁'] = DICTAGE['41~50岁'] + k
            elif int(j)>50 and int(j)<=60:
                DICTAGE['51~60岁'] = DICTAGE['51~60岁'] + k
            elif int(j)>60 and int(j)<=70:
                DICTAGE['61~70岁'] = DICTAGE['61~70岁'] + k
            elif int(j) > 70:
                DICTAGE['70岁以上'] = DICTAGE['70岁以上'] + k
        return DICTAGE

    def get_pre_age_info(self):
        court = {}
        plaage_sta = {}
        defage_sta = {}
        plaage_sta_male = {}
        defage_sta_male = {}
        plaage_sta_female = {}
        defage_sta_female = {}
        plaintiff_sex = {
            '男': 0,
            '女': 0
        }
        defendant_sex = {
            '男': 0,
            '女': 0
        }
        for i in CPJF.objects(Q(案由='产品责任纠纷')):
            if i.头部信息:
                for j in i.头部信息.split('、'):
                    if '法院' in j and len(j)<25 and 'X' not in j and 'x' not in j:
                        # print(i.头部信息.split('、'))
                        a = j.replace('重庆市','')
                        a = a.replace('×','')
                        a = a.replace('-','')
                        a = a.replace('\t','')
                        a = a.replace('\\', '')
                        a = a.replace('\xa0', '')
                        if a not in court.keys():
                            court[a] = 1
                        elif a in court.keys():
                            court[a] = court[a] + 1
                        break
                # info1 = ''.join(i.当事人信息)
            info = i.当事人信息.split('、')
            plaintiff = ''
            defendant = ''
            # print(i.当事人信息)
            if info:
                for j in info:
                    if (('原告' in j) or ('申请人' in j) or ('上诉人' in j)) and (not plaintiff) and (len(j) > 15):
                        plaintiff = j
                    elif (('被告' in j) or ('被申请人' in j) or ('被上诉人' in j) or ('被申诉人' in j)) and (not defendant) and (
                            len(j) > 15):
                        defendant = j
                if plaintiff and defendant:
                    if '男' in plaintiff:
                        plaintiff_sex['男'] = plaintiff_sex['男'] + 1
                        m = re.split('[,，]', plaintiff)
                        for k in m:
                            if '年' in k and '月' in k:
                                plaintiff_date_male = re.findall(r'(\d{4})年', k)

                                if plaintiff_date_male:
                                    plaintiff_age_male = 2019 - int(plaintiff_date_male[0])
                                    # if plaintiff_age <20:
                                    #     print(i.当事人信息)
                                    # if plaintiff_age <0:
                                    #     print(i)
                                if (str(plaintiff_age_male) in plaage_sta_male):
                                    plaage_sta_male[str(plaintiff_age_male)] = plaage_sta_male[str(plaintiff_age_male)] + 1
                                elif (str(plaintiff_age_male) not in plaage_sta_male) and (plaintiff_age_male < 120) and (
                                        plaintiff_age_male > 10):
                                    plaage_sta_male[str(plaintiff_age_male)] = 1
                                break
                    elif '女' in plaintiff:
                        plaintiff_sex['女'] = plaintiff_sex['女'] + 1
                        m = re.split('[,，]', plaintiff)
                        for k in m:
                            if '年' in k and '月' in k:
                                plaintiff_date_female = re.findall(r'(\d{4})年', k)

                                if plaintiff_date_female:
                                    plaintiff_age_female = 2019 - int(plaintiff_date_female[0])
                                    # if plaintiff_age <20:
                                    #     print(i.当事人信息)
                                    # if plaintiff_age <0:
                                    #     print(i)
                                if (str(plaintiff_age_female) in plaage_sta_female):
                                    plaage_sta_female[str(plaintiff_age_female)] = plaage_sta_female[
                                                                                       str(plaintiff_age_female)] + 1
                                elif (str(plaintiff_age_female) not in plaage_sta_female) and (
                                        plaintiff_age_female < 120) and (plaintiff_age_female > 10):
                                    plaage_sta_female[str(plaintiff_age_female)] = 1
                                break
                    if '男' in defendant:
                        defendant_sex['男'] = defendant_sex['男'] + 1
                        m = re.split('[,，]', defendant)
                        for k in m:
                            if '年' in k and '月' in k:
                                defendant_date_male = re.findall(r'(\d{4})年', k)

                                if defendant_date_male:
                                    defendant_age_male = 2019 - int(defendant_date_male[0])
                                    # if defendant_age <20:
                                    #     print(i.当事人信息)
                                    # if defendant_age <0:
                                    #     print(i)
                                if (str(defendant_age_male) in defage_sta_male):
                                    defage_sta_male[str(defendant_age_male)] = defage_sta_male[str(defendant_age_male)] + 1
                                elif (str(defendant_age_male) not in defage_sta_male) and (defendant_age_male < 120) and (
                                        defendant_age_male > 10):
                                    defage_sta_male[str(defendant_age_male)] = 1
                                break
                    elif '女' in defendant:
                        defendant_sex['女'] = defendant_sex['女'] + 1
                        m = re.split('[,，]', defendant)
                        for k in m:
                            if '年' in k and '月' in k:
                                defendant_date_female = re.findall(r'(\d{4})年', k)

                                if defendant_date_female:
                                    defendant_age_female = 2019 - int(defendant_date_female[0])
                                    # if defendant_age <20:
                                    #     print(i.当事人信息)
                                    # if defendant_age <0:
                                    #     print(i)
                                if (str(defendant_age_female) in defage_sta_female):
                                    defage_sta_female[str(defendant_age_female)] = defage_sta_female[
                                                                                       str(defendant_age_female)] + 1
                                elif (str(defendant_age_female) not in defage_sta_female) and (
                                        defendant_age_female < 120) and (
                                        defendant_age_female > 10):
                                    defage_sta_female[str(defendant_age_female)] = 1
            if plaintiff and defendant:
                m = re.split('[,，]', plaintiff)
                n = re.split('[,，]', defendant)
                for k in m:
                    if '年' in k and '月' in k:
                        plaintiff_date = re.findall(r'(\d{4})年', k)

                        if plaintiff_date:
                            plaintiff_age = 2019 - int(plaintiff_date[0])
                            # if plaintiff_age <20:
                            #     print(i.当事人信息)
                            # if plaintiff_age <0:
                            #     print(i)
                        if (str(plaintiff_age) in plaage_sta):
                            plaage_sta[str(plaintiff_age)] = plaage_sta[str(plaintiff_age)] + 1
                        elif (str(plaintiff_age) not in plaage_sta) and (plaintiff_age < 120) and (plaintiff_age > 10):
                            plaage_sta[str(plaintiff_age)] = 1
                        break
                for k in n:
                    if '年' in k and '月' in k:
                        plaintiff_date = re.findall(r'(\d{4})年', k)

                        if plaintiff_date:
                            plaintiff_age = 2019 - int(plaintiff_date[0])
                            # if plaintiff_age <20:
                            #     print(i.当事人信息)
                            # if plaintiff_age <0:
                            #     print(i)
                        if (str(plaintiff_age) in defage_sta):
                            defage_sta[str(plaintiff_age)] = defage_sta[str(plaintiff_age)] + 1
                        elif (str(plaintiff_age) not in defage_sta) and (plaintiff_age < 120) and (plaintiff_age > 10):
                            defage_sta[str(plaintiff_age)] = 1
                        break
        return [court, plaage_sta, defage_sta, plaage_sta_male, plaage_sta_female, defage_sta_male, defage_sta_female, plaintiff_sex, defendant_sex]

    def get_court_info(self):
        # court = get_age_info()[0]
        court1 =[('万州区人民法院', 122), ('丰都县人民法院', 7), ('九龙坡区人民法院', 1157), ('云阳县人民法院', 40), ('北碚区人民法院', 506), ('南岸区人民法院', 641), ('南川区人民法院', 12), ('合川区人民法院', 226), ('垫江县人民法院', 7), ('城口县人民法院', 1), ('大渡口区人民法院', 292), ('大足区人民法院', 16), ('奉节县人民法院', 12), ('巫山县人民法院', 12), ('巫溪县人民法院', 4), ('巴南区人民法院', 536), ('开州区人民法院', 4), ('彭水苗族土家族自治县人民法院', 2), ('忠县人民法院', 4), ('梁平区人民法院', 4), ('武隆区人民法院', 1), ('永川区人民法院', 75), ('江北区人民法院', 2719), ('江津区人民法院', 135), ('江津区人民法院1', 2), ('沙坪坝区人民法院', 2605), ('涪陵区人民法院', 121), ('渝中区人民法院', 731), ('渝北区人民法院', 1835), ('潼南区人民法院', 6), ('璧山区人民法院', 83), ('石柱土家族自治县人民法院', 7), ('秀山土家族苗族自治县人民法院', 3), ('第一中级人民法院', 64), ('第三中级人民法院', 5), ('第二中级人民法院', 29), ('第五中级人民法院', 251), ('第四中级人民法院', 8), ('綦江区人民法院', 148), ('荣昌区人民法院', 11), ('酉阳土家族苗族自治县人民法院', 2), ('重庆铁路运输法院', 3), ('铜梁区人民法院', 88), ('长寿区人民法院', 2), ('高级人民法院', 67), ('黔江区人民法院', 49)]
        court = {}
        for i in court1:
            m = i[0].replace('区','')
            m = m.replace('人民法院', '')
            m = m.replace('自治县', '')
            m = m.replace('市', '')
            m = m.replace('苗族', '')
            m = m.replace('土家族', '')
            m = m.replace('中华人民共和国', '')

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
                m = '渝中'
            elif m == '高级':
                m = '渝北区'
            for j in court.keys():
                if m[:2] in j:
                    court[j] = court[j]+i[1]
                    m = ''
                    break
            if m:
                court[m] = i[1]
        return court

    def get_map_data(self):
        MAP = []
        court = MsCpjfData().get_court_info()
        for i, j in court.items():
            NOname = {}
            if i != '酉阳' and i != '秀山' and '县' not in i and len(i)<5:
                NOname['name'] = i+'区'
            else:
                NOname['name'] = i
            NOname['value'] = j
            # print(NOname)
            MAP.append(NOname)
        return MAP

    def get_bubble_data(self, plaage, defage):
        bubble = []
        bubble_b = []
        for i,j in plaage.items():
            if i == '20岁以下':
                bubble1 = []
                bubble1.append(15)
                bubble1.append(1)
                bubble1.append(j)
                bubble.append(bubble1)
            elif i == '20~30岁':
                bubble1 = []
                bubble1.append(25)
                bubble1.append(1)
                bubble1.append(j)
                bubble.append(bubble1)
            elif i == '31~40岁':
                bubble1 = []
                bubble1.append(35)
                bubble1.append(1)
                bubble1.append(j)
                bubble.append(bubble1)
            elif i == '41~50岁':
                bubble1 = []
                bubble1.append(45)
                bubble1.append(1)
                bubble1.append(j)
                bubble.append(bubble1)
            elif i == '51~60岁':
                bubble1 = []
                bubble1.append(55)
                bubble1.append(1)
                bubble1.append(j)
                bubble.append(bubble1)
            elif i == '61~70岁':
                bubble1 = []
                bubble1.append(65)
                bubble1.append(1)
                bubble1.append(j)
                bubble.append(bubble1)
            elif i == '70岁以上':
                bubble1 = []
                bubble1.append(75)
                bubble1.append(1)
                bubble1.append(j)
                bubble.append(bubble1)
        for i,j in defage.items():
            if i == '20岁以下':
                bubble1 = []
                bubble1.append(15)
                bubble1.append(0)
                bubble1.append(j)
                bubble_b.append(bubble1)
            elif i == '20~30岁':
                bubble1 = []
                bubble1.append(25)
                bubble1.append(0)
                bubble1.append(j)
                bubble_b.append(bubble1)
            elif i == '31~40岁':
                bubble1 = []
                bubble1.append(35)
                bubble1.append(0)
                bubble1.append(j)
                bubble_b.append(bubble1)
            elif i == '41~50岁':
                bubble1 = []
                bubble1.append(45)
                bubble1.append(0)
                bubble1.append(j)
                bubble_b.append(bubble1)
            elif i == '51~60岁':
                bubble1 = []
                bubble1.append(55)
                bubble1.append(0)
                bubble1.append(j)
                bubble_b.append(bubble1)
            elif i == '61~70岁':
                bubble1 = []
                bubble1.append(65)
                bubble1.append(0)
                bubble1.append(j)
                bubble_b.append(bubble1)
            elif i == '70岁以上':
                bubble1 = []
                bubble1.append(75)
                bubble1.append(0)
                bubble1.append(j)
                bubble_b.append(bubble1)
        return [bubble, bubble_b]

    def get_chart_age_data(self, age_info):
        chart_age_data = {}
        chart_age_data['PLAAGE'] = MsCpjfData().age_dict_get(age_info[1])#'原告年龄分布'
        chart_age_data['DEFAGE'] = MsCpjfData().age_dict_get(age_info[2])#'原告女性年龄分布'
        chart_age_data['PLAAGE_MALE'] = MsCpjfData().age_dict_get(age_info[3])#'原告男性年龄分布'
        chart_age_data['PLAAGE_FEMALE'] = MsCpjfData().age_dict_get(age_info[4])#'被告年龄分布'
        chart_age_data['DEFAGE_MALE'] = MsCpjfData().age_dict_get(age_info[5])#'被告男性年龄分布'
        chart_age_data['DEFAGE_FEMALE'] = MsCpjfData().age_dict_get(age_info[6])#'被告女性年龄分布'
        chart_age_data['plaintiff_sex'] = age_info[7]#原告性别分布
        chart_age_data['defendant_sex'] = age_info[8]#被告性别分布
        return chart_age_data

    def get_defendant_edujob(self):
        d = []
        f = {'无业游民': 0, '工人': 0, '自营业主': 0, '教师': 0, '医生': 0, '农民': 0}
        # print(str)
        for i in CPJF.objects(Q(案由='产品责任纠纷')):
            a = i.当事人信息.split('、')
            # print(a)
            for j in a:
                if ('被告人' in j or '被告' in j) and ('男' in j or '女' in j):
                    c = {'edu': '未知'}
                    # print(j)
                    if ',' in j or '，' in j:
                        e = j.split('，')
                        b = []
                        for i in e:
                            for w in i.split(','):
                                b.append(w)
                        for k in b:
                            if '文化' in k and len(k) < 6:
                                c['edu'] = k
                            elif '文盲' in k and len(k) < 6:
                                c['edu'] = k
                            elif '无业' in k and len(k) < 6:
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
                        d.append(c)
        return d,f

    def get_case_edu_number(self, DQdefendant_info):
        CPEDU = []
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
            CPEDU.append(d)
        return CPEDU

    def get_case_date_number(self):
        case_date_number = {
            '2016': 0,
            '2017': 0,
            '2018': 0,
            '2019': 0
        }
        for i in CPJF.objects(Q(案由='产品责任纠纷')):
            for j in i.尾部信息.split('、'):
                if ('年' in j) and ('月' in j) and ('日' in j) and ('二' in j):
                    if ('二一九' in j) or ('二一九' in j):
                        case_date_number['2019'] += 1
                    elif ('二一八' in j) or ('二一八' in j):
                        case_date_number['2018'] += 1
                    elif ('二一七' in j) or ('二一七' in j):
                        case_date_number['2017'] += 1
                    elif ('二一六' in j) or ('二一六' in j):
                        case_date_number['2016'] += 1
                    break
        return case_date_number

    # 涉诉商品
    def goods(self):
        goods = {
            '食品': 0,
            '药品': 0,
            '保健品': 0,
            '车': 0,
            '销售': 0,
            '其它': 0
        }
        for i in CPJF.objects(Q(案由='产品责任纠纷')):
            a = i.庭审过程
            if '食' in a or '超市' in a or '水' in a:
                goods['食品'] = goods['食品'] + 1
            elif '药' in a:
                goods['药品'] = goods['药品'] + 1
            elif '保健' in a:
                goods['保健品'] = goods['保健品'] + 1
            elif '车' in a:
                goods['车'] = goods['车'] + 1
            elif '销售' in a:
                goods['销售'] = goods['销售'] + 1
            else:
                goods['其它'] = goods['其它'] + 1
        return goods



    # 审理情况
    def verdict(self):
        verdict = {'撤诉': 0, '调解': 0, '移送': 0, '驳回起诉': 0, '判决': 0, '不予受理': 0}
        for i in CPJF.objects(Q(案由='产品责任纠纷')):
            a = i.庭审过程
            if '撤诉' in a:
                verdict['撤诉'] = verdict['撤诉'] + 1
            elif '调解' in a:
                verdict['调解'] = verdict['调解'] + 1
            elif '移送' in a:
                verdict['移送'] = verdict['移送'] + 1
            elif '驳回' in a:
                verdict['驳回起诉'] = verdict['驳回起诉'] + 1
            elif '判决' in a:
                verdict['判决'] = verdict['判决'] + 1
            elif '不予受理' in a:
                verdict['不予受理'] = verdict['不予受理'] + 1
        return verdict



    # 审理情况
    def get_case_money(self):
        money = []
        text = re.compile("[0-9].*")
        for i in CPJF.objects(Q(案由='产品责任纠纷')):
            a = i.庭审过程
            b = a.split('、')
            for j in b:
                if j.endswith('判决如下：'):
                    c = b.index(j)
                    k = b[c + 1]
                    if re.findall(r'(.*?)元', k):
                        str1 = str(re.findall(r'(.*?)元', k)[0]).replace('人民币', '')
                        str1 = str1.replace('人币', '')
                        d = str1.replace('元', '')
                        e = re.findall(r'\d+', d)
                        if e:
                            f = int(e[-1])
                            money.append(f)
        CPJFMON = []
        d = {
            '少于100元': 0,
            '101元~500元': 0,
            '501元~1500元': 0,
            '1501元~3500元': 0,
            '3500元以上': 0
        }
        for i in money:
            if i <= 100:
                d['少于100元'] = d['少于100元'] + 1
            elif i <= 500:
                d['101元~500元'] = d['101元~500元'] + 1
            elif i <= 1500:
                d['501元~1500元'] = d['501元~1500元'] + 1
            elif i <= 3500:
                d['1501元~3500元'] = d['1501元~3500元'] + 1
            elif i > 3500:
                d['3500元以上'] = d['3500元以上'] + 1
        for cl in d:
            # print(bl)
            c = {}
            c['name'] = cl
            c['y'] = d[cl]
            CPJFMON.append(c)
        return CPJFMON

goods_result = {'食品': 8979, '药品': 274, '保健品': 26, '车': 127, '销售': 1080, '其它': 21}
verdict_result = {'撤诉': 6465, '调解': 228, '移送': 80, '驳回起诉': 2400, '判决': 2010, '不予受理': 1}
CPJFMON_result = [{'name': '少于100元', 'y': 607}, {'name': '101元~500元', 'y': 25}, {'name': '501元~1500元', 'y': 1281},
                  {'name': '1501元~3500元', 'y': 19}, {'name': '3500元以上', 'y': 17}]


# d,f=MsCpjfData().get_defendant_edujob()
# CPEDU=MsCpjfData().get_case_edu_number(d)
# job=list(f.keys())
# job_number=list(f.values())
# job_all=[job,job_number]
# print(job_all)
# print(CPEDU)
# print(CPJF.objects(Q(案由='产品责任纠纷')).count())
# court = MsCpjfData().get_court_info()#'各地区案件数量'
# age_info = MsCpjfData().get_pre_age_info()#获得未处的年龄数据
# chart_age_data = MsCpjfData().get_chart_age_data(age_info)#对未处理的年龄数据进行处理
# case_date_number = MsCpjfData().get_case_date_number()
# print(chart_age_data)
# print(case_date_number)
#为了提高展示速度，将相关数据进行直接展示

PLAAGE = {'20岁以下': 1, '20~30岁': 2449, '31~40岁': 5937, '41~50岁': 1491, '51~60岁': 210, '61~70岁': 549, '70岁以上': 84}
PLAAGE_FEMALE = {'20岁以下': 0, '20~30岁': 487, '31~40岁': 377, '41~50岁': 65, '51~60岁': 33, '61~70岁': 185, '70岁以上': 13}
PLAAGE_MALE = {'20岁以下': 1, '20~30岁': 1962, '31~40岁': 5559, '41~50岁': 1424, '51~60岁': 177, '61~70岁': 364, '70岁以上': 71}
DEFAGE = {'20岁以下': 0, '20~30岁': 78, '31~40岁': 224, '41~50岁': 60, '51~60岁': 55, '61~70岁': 14, '70岁以上': 8}
DEFAGE_MALE = {'20岁以下': 0, '20~30岁': 67, '31~40岁': 196, '41~50岁': 48, '51~60岁': 51, '61~70岁': 11, '70岁以上': 8}
DEFAGE_FEMALE = {'20岁以下': 0, '20~30岁': 11, '31~40岁': 28, '41~50岁': 12, '51~60岁': 4, '61~70岁': 3, '70岁以上': 0}
plaintiff_sex = {'男': 10012, '女': 1213}
defendant_sex = {'男': 424, '女': 61}
aj_male = [plaintiff_sex['男'],defendant_sex['男']]
aj_female = [plaintiff_sex['女'],defendant_sex['女']]
case_date_number = {'2017': 2390, '2018': 7408, '2019': 2782}
bubble_data = MsCpjfData().get_bubble_data(PLAAGE, DEFAGE)


class OverviewInfo:
    def __init__(self):
        pass

    def get_his_row_data(self, map_data):
        region_case_pre_number = sorted(map_data, key=lambda y: y['value'], reverse=True)
        region = []
        number = []
        region_case_number = []
        for i in region_case_pre_number:
            if region_case_pre_number.index(i) > 6:
                break
            else:
                region.append(i['name'])
                number.append(i['value'])
        region_case_number.append(region)
        region_case_number.append(number)
        return region_case_number

    def get_line_data(self, data):
        date_list = list(data.keys())
        date_number = list(data.values())
        line_data = [date_list, date_number, '产品责任纠纷案件']
        return line_data

    def get_overview_data(self):
        map_jdjf_data = MsCpjfData().get_map_data()
        jdjf_ajnumber = 12666#LHJF.objects.count()  #
        jdjf_pnumber = plaintiff_sex['男'] + plaintiff_sex['女'] + defendant_sex['男'] + defendant_sex['女']
        region_case_number = OverviewInfo().get_his_row_data(map_jdjf_data)
        line_data = OverviewInfo().get_line_data(case_date_number)
        overview_data = {
            'ajnumber': jdjf_ajnumber,
            'pnumber': jdjf_pnumber,
            'map': map_jdjf_data,
            'region_case_number': region_case_number,
            'line_data': line_data,
        }
        return overview_data

overview_data_cpzrjf = OverviewInfo().get_overview_data()





class ChartData:
    def __init__(self):
        pass

    def get_pie_sex_data(self, name):
        pie_data = {}
        pie_data['name'] = name
        pie_data['data'] = []

        pie_meta_data = {}
        pie_meta_data['name'] = '男性'
        pie_meta_data['y'] = plaintiff_sex['男'] + defendant_sex['男']
        pie_data['data'].append(pie_meta_data)
        pie_meta_data = {}
        pie_meta_data['name'] = '女性'
        pie_meta_data['y'] = plaintiff_sex['女'] + defendant_sex['女']
        pie_data['data'].append(pie_meta_data)
        return pie_data

    def get_his_age_data(self):
        cate = list(PLAAGE.keys())
        data = []
        for i in cate:
            data.append(PLAAGE[i] + DEFAGE[i])
        return [cate, data]

    def get_person_info(self):
        person_info = {}
        pie_age_data = ChartData().get_pie_sex_data('当事人性别')
        pie_edu_data = {
            'name': '当事人学历',
            'data':[{'name': '未知', 'y': 430}, {'name': '文盲', 'y': 8}, {'name': '小学文化', 'y': 62}, {'name': '中学文化', 'y': 73}, {'name': '高中文化', 'y': 16}, {'name': '大专文化', 'y': 0}, {'name': '本科文化', 'y': 0}, {'name': '研究生文化', 'y': 0}]
        }
        his_age_data = ChartData().get_his_age_data()
        his_job_data = [['无业游民', '工人', '自营业主', '教师', '医生', '农民'], [360, 150, 330, 200, 250, 870]]
        person_info['pie_age_data'] = pie_age_data
        person_info['pie_edu_data'] = pie_edu_data
        person_info['his_age_data'] = his_age_data
        person_info['his_job_data'] = his_job_data
        return person_info
person_info_cpzrjf = ChartData().get_person_info()


class case_analysis:
    def __init__(self):
        pass

    def get_pie_data(self, data):
        pie=[]
        for i in data:
            # print(bl)
            a = {}
            a['name'] = i
            a['y'] = data[i]
            pie.append(a)
        return pie

    def special_case_analysis(self):
        analysis={}
        pie_goods_data = {
            'name': '涉诉商品',
            'data': case_analysis().get_pie_data(goods_result)
        }
        pie_verdict_data = {
            'name': '审理情况',
            'data': case_analysis().get_pie_data(verdict_result)
        }
        pie_CPJFMON_data = {
            'name': '罚款分析',
            'data': CPJFMON_result
        }
        analysis['pie_goods_data']=pie_goods_data
        analysis['pie_verdict_data'] = pie_verdict_data
        analysis['pie_CPJFMON_data']=pie_CPJFMON_data
        return analysis
analysis_cpzrjf=case_analysis().special_case_analysis

