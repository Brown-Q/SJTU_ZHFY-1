#-*- coding:utf-8 -*-
import re
from mongoengine import *
disconnect()
connect('court', host='202.121.180.66', port=7101)

class HTJF(Document):
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


class MsHtjfData:
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
        for i in HTJF.objects(Q(案由='劳动合同纠纷')):
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
        court1 =[ ('万州区人民法院', 397), ('丰都县人民法院', 42), ('九龙坡区人民法院', 1537), ('云阳县人民法院', 27), ('北碚区人民法院', 514), ('南岸区人民法院', 1086), ('南川区人民法院', 287), ('合川区人民法院', 215), ('垫江县人民法院', 65), ('城口县人民法院', 9), ('大渡口区人民法院', 344), ('大足区人民法院', 205), ('奉节县人民法院', 212), ('巫山县人民法院', 192), ('巫溪县人民法院', 8), ('巴南区人民法院', 845), ('开州区人民法院', 68), ('彭水苗族土家族自治县人民法院', 214), ('忠县人民法院', 36), ('梁平区人民法院', 54), ('武隆区人民法院', 61), ('武隆县人民法院', 1), ('永川区人民法院', 161), ('江北区人民法院', 432), ('江津区人民法院', 331), ('沙坪坝区人民法院', 975), ('涪陵区人民法院', 185), ('渝中区人民法院', 1119), ('渝北区人民法院', 678), ('潼南区人民法院', 176), ('璧山区人民法院', 280), ('石柱土家族自治县人民法院', 271), ('秀山土家族苗族自治县人民法院', 122), ('第一中级人民法院', 797), ('第三中级人民法院', 139), ('第二中级人民法院', 137), ('第五中级人民法院', 1157), ('第四中级人民法院', 205), ('綦江区人民法院', 95), ('荣昌区人民法院', 244), ('酉阳土家族苗族自治县人民法院', 97), ('铜梁区人民法院', 184), ('长寿区人民法院', 208), ('高级人民法院', 374), ('黔江区人民法院', 22)]
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
        court = MsHtjfData().get_court_info()
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
        chart_age_data['PLAAGE'] = MsHtjfData().age_dict_get(age_info[1])#'原告年龄分布'
        chart_age_data['DEFAGE'] = MsHtjfData().age_dict_get(age_info[2])#'原告女性年龄分布'
        chart_age_data['PLAAGE_MALE'] = MsHtjfData().age_dict_get(age_info[3])#'原告男性年龄分布'
        chart_age_data['PLAAGE_FEMALE'] = MsHtjfData().age_dict_get(age_info[4])#'被告年龄分布'
        chart_age_data['DEFAGE_MALE'] = MsHtjfData().age_dict_get(age_info[5])#'被告男性年龄分布'
        chart_age_data['DEFAGE_FEMALE'] = MsHtjfData().age_dict_get(age_info[6])#'被告女性年龄分布'
        chart_age_data['plaintiff_sex'] = age_info[7]#原告性别分布
        chart_age_data['defendant_sex'] = age_info[8]#被告性别分布
        return chart_age_data

    def get_defendant_edujob(self):
        d = []
        f = {'无业游民': 0, '工人': 0, '自营业主': 0, '教师': 0, '医生': 0, '农民': 0}
        # print(str)
        for i in HTJF.objects(Q(案由='劳动合同纠纷')):
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
                            if '文化' in k and len(k) < 6:
                                c['edu'] = k
                            elif '文盲' in k and len(k) < 6:
                                c['edu'] = k
                            elif '无业' in k and len(k) < 6:
                                f['无业游民'] += 1
                            elif '工人' in k and len(k) < 6:
                                f['工人'] += 1
                            elif '公司' in k or '自营' in k and len(k) < 6:
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

    def get_case_date_number(self):
        case_date_number = {
            '2017': 0,
            '2018': 0,
            '2019': 0
        }
        for i in HTJF.objects(Q(案由='劳动合同纠纷')):
            for j in i.尾部信息.split('、'):
                if ('年' in j) and ('月' in j) and ('日' in j) and ('二' in j):
                    if ('二一九' in j) or ('二一九' in j):
                        case_date_number['2019'] += 1
                    elif ('二一八' in j) or ('二一八' in j):
                        case_date_number['2018'] += 1
                    elif ('二一七' in j) or ('二一七' in j):
                        case_date_number['2017'] += 1
                    break
        return case_date_number

# d,f=MsHtjfData().get_defendant_edujob()
# LHEDU=MsHtjfData().get_case_edu_number(d)
# job=list(f.keys())
# job_number=list(f.values())
# job_all=[job,job_number]
# print(job_all)
# print(LHEDU)
# print(HTJF.objects(Q(案由='劳动合同纠纷')).count())
# court = MsHtjfData().get_court_info()#'各地区案件数量'
# age_info = MsHtjfData().get_pre_age_info()#获得未处的年龄数据
# chart_age_data = MsHtjfData().get_chart_age_data(age_info)#对未处理的年龄数据进行处理
# case_date_number = MsHtjfData().get_case_date_number()
# print(chart_age_data)
# print(case_date_number)
#为了提高展示速度，将相关数据进行直接展示
# court = {'江津': 5081, '万州': 4691, '合川': 3478, '云阳县': 3210, '綦江': 3103, '开州': 3012, '渝北': 3628, '沙坪坝': 2716, '巴南': 2679, '涪陵': 2816, '九龙坡': 2580, '彭水苗族土家族': 2551, '奉节县': 2507, '永川': 2454, '大足': 2223, '北碚': 2139, '荣昌': 2331, '垫江县': 2063, '巫山县': 1994, '丰都县': 1981, '铜梁': 1868, '梁平': 2853, '潼南': 1803, '南川': 1748, '长寿': 1669, '忠县': 1606, '璧山': 1751, '南岸': 1560, '石柱土家族': 1387, '江北': 1381, '巫溪县': 1326, '黔江': 1359, '渝中': 1096, '酉阳': 952, '城口县': 943, '秀山': 941, '大渡口': 892, '开县': 741, '武隆': 1142, '第五中级': 561}

PLAAGE = {'20岁以下': 15, '20~30岁': 1351, '31~40岁': 2224, '41~50岁': 3718, '51~60岁': 3007, '61~70岁': 1146, '70岁以上': 143}
PLAAGE_FEMALE = {'20岁以下': 7, '20~30岁': 581, '31~40岁': 887, '41~50岁': 1347, '51~60岁': 1073, '61~70岁': 275, '70岁以上': 53}
PLAAGE_MALE = {'20岁以下': 8, '20~30岁': 762, '31~40岁': 1339, '41~50岁': 2373, '51~60岁': 1925, '61~70岁': 869, '70岁以上': 90}
DEFAGE = {'20岁以下': 3, '20~30岁': 183, '31~40岁': 585, '41~50岁': 962, '51~60岁': 726, '61~70岁': 125, '70岁以上': 18}
DEFAGE_MALE = {'20岁以下': 0, '20~30岁': 59, '31~40岁': 178, '41~50岁': 285, '51~60岁': 157, '61~70岁': 14, '70岁以上': 0}
DEFAGE_FEMALE = {'20岁以下': 1, '20~30岁': 84, '31~40岁': 286, '41~50岁': 344, '51~60岁': 79, '61~70岁': 7, '70岁以上': 0}
plaintiff_sex = {'男': 7508, '女': 4282}
defendant_sex = {'男': 2685, '女': 832}
aj_male = [plaintiff_sex['男'],defendant_sex['男']]
aj_female = [plaintiff_sex['女'],defendant_sex['女']]
case_date_number = {'2017': 5651, '2018': 8720, '2019': 9950}
bubble_data = MsHtjfData().get_bubble_data(PLAAGE, DEFAGE)


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
        line_data = [date_list, date_number, '劳动合同纠纷案件']
        return line_data

    def get_overview_data(self):
        map_jdjf_data = MsHtjfData().get_map_data()
        jdjf_ajnumber = 14826#LHJF.objects.count()  #
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

overview_data_ldhtjf = OverviewInfo().get_overview_data()





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
            'data': [{
                'name': '文盲',
                'y': 12144
            }, {
                'name': '小学',
                'y': 8243
            }, {
                'name': '初中',
                'y': 3424
            }, {
                'name': '高中',
                'y': 3054
            }, {
                'name': '本科',
                'y': 6424
            }, {
                'name': '硕士',
                'y': 1054
            }, {
                'name': '博士及以上',
                'y': 200
            }]
        }
        his_age_data = ChartData().get_his_age_data()
        his_job_data = [['无业游民', '工人', '自营业主', '教师', '医生', '农民'], [420, 330, 340, 390, 520, 750]]
        person_info['pie_age_data'] = pie_age_data
        person_info['pie_edu_data'] = pie_edu_data
        person_info['his_age_data'] = his_age_data
        person_info['his_job_data'] = his_job_data
        return person_info
person_info_ldhtjf = ChartData().get_person_info()