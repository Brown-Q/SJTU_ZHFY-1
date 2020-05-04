#-*- coding:utf-8 -*-
import re
from mongoengine import *
disconnect()
connect('court', host='202.121.180.66', port=7101)

class JDJF(Document):
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


class MsJdjfData:
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
        for i in JDJF.objects(Q(案由='借贷纠纷')):
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
        court1 = [('万州区人民法院', 1735), ('中华人民共和国渝中区人民法院', 1), ('丰都县人民法院', 591), ('九龙坡区人民法院', 2198), ('云阳县人民法院', 960), ('八归档的九龙坡区人民法院', 1), ('北碚区人民法院', 932), ('南岸区人民法院', 1896), ('南川区人民法院', 551), ('合川区人民法院', 1436), ('垫江县人民法院', 1321), ('城口县人民法院', 311), ('大渡口区人民法院', 316), ('大渡口区人民法院1', 5), ('大足区人民法院', 876), ('奉节县人民法院', 1513), ('巫山县人民法院', 794), ('巫溪县人民法院', 778), ('巴南区人民法院', 1517), ('庆市大渡口区人民法院', 1), ('开县人民法院', 29), ('开州区人民法院', 1302), ('彭水苗族土家族自治县人民法院', 533), ('彭水苗族土彭水苗族土家族自治县人民法院', 1), ('忠县人民法院', 519), ('梁平区人民法院', 690), ('梁平县人民法院', 2), ('武隆区人民法院', 346), ('武隆县人民法院', 3), ('永川区人民法院', 871), ('江北区人民法院', 2240), ('江津区人民法院', 2084), ('沙坪坝区人民法院', 2073), ('涪陵区人民法院', 1864), ('渝中区人民法院', 1828), ('渝北区人民法院', 4583), ('潼南区人民法院', 572), ('潼南县人民法院', 2), ('璧山区人民法院', 1138), ('石柱土家族自治县人民法院', 347), ('秀山土家族苗族自治县人民法院', 393), ('第一中级人民法院', 1074), ('第三中级人民法院', 357), ('第丰都县人民法院', 1), ('第二中级人民法院', 633), ('第五中级人民法院', 1050), ('第四中级人民法院', 132), ('綦江区人民法院', 853), ('荣昌区人民法院', 767), ('荣昌县人民法院', 1), ('酉阳土家族苗族自治县人民法院', 230), ('重庆万州区人民法院', 1), ('重庆垫江县人民法院', 1), ('重庆大渡口区人民法院', 1), ('重庆巫溪县人民法院', 1), ('重庆自由贸易试验区人民法院', 4), ('铜梁区人民法院', 734), ('长寿区人民法院', 1100), ('高级人民法院', 528), ('黔江区人民法院', 574)]
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
        court = MsJdjfData().get_court_info()
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
        chart_age_data['PLAAGE'] = MsJdjfData().age_dict_get(age_info[1])#'原告年龄分布'
        chart_age_data['DEFAGE'] = MsJdjfData().age_dict_get(age_info[2])#'原告女性年龄分布'
        chart_age_data['PLAAGE_MALE'] = MsJdjfData().age_dict_get(age_info[3])#'原告男性年龄分布'
        chart_age_data['PLAAGE_FEMALE'] = MsJdjfData().age_dict_get(age_info[4])#'被告年龄分布'
        chart_age_data['DEFAGE_MALE'] = MsJdjfData().age_dict_get(age_info[5])#'被告男性年龄分布'
        chart_age_data['DEFAGE_FEMALE'] = MsJdjfData().age_dict_get(age_info[6])#'被告女性年龄分布'
        chart_age_data['plaintiff_sex'] = age_info[7]#原告性别分布
        chart_age_data['defendant_sex'] = age_info[8]#被告性别分布
        return chart_age_data

    def get_defendant_edujob(self):
        d = []
        f = {'无业游民': 0, '工人': 0, '自营业主': 0, '教师': 0, '医生': 0, '农民': 0}
        # print(str)
        for i in JDJF.objects(Q(案由='借贷纠纷')):
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
        return d, f

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
        for i in JDJF.objects(Q(案由='借贷纠纷')):
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

    # 证据分析  案件中并没有绝对必要的证据，只要原告能证明双方存在借贷关系，法院一般会支持全部诉讼请求。
    def evidence(self):
        evidence = {
            '借条': 0,
            '借款合同': 0,
            '转账凭证': 0,
        }
        a = ['借条', '借款合同', '转账凭证']
        for i in JDJF.objects(Q(案由='借贷纠纷')):
            b = i.庭审过程
            for j in a:
                if j in b:
                    evidence[j] = evidence[j] + 1
        return evidence


    def get_case_money(self):
        money = []
        text = re.compile("[0-9].*")
        for i in JDJF.objects(Q(案由='借贷纠纷')):
            for j in i.庭审过程.split('、'):
                if j.startswith('原告'):
                    if re.findall(r'本金(.*?)元', j):
                        str1 = str(re.findall(r'本金(.*?)元', j)[0]).replace('人民币', '')
                        str1 = str1.replace('人币', '')
                        a = str1.replace('元', '')
                        if 0 < len(a) <= 6 and text.match(a):
                            money.append(a)
                    elif bool(re.findall(r'借款(.*?)。', j)):
                        a = str(re.findall(r'借款(.*?)。', j)[0]).replace('人民币', '')
                        a = a.replace('元', '')
                        if 0 < len(a) <= 6 and text.match(a):
                            money.append(a)
        money_re = []
        for l in money:
            if l.isdigit():
                money_re.append(int(l))
            elif not re.compile(u'[^\u4e00-\u9fa5]').search(l):
                if '在' not in l and '各' not in l and '限' not in l and '的' not in l and '至' not in l and '已' not in l:
                    p = MsJdjfData().chinese_to_arabic(l)
                    money_re.append(p)
        JDJFMON = []
        d = {
            '少于15000元': 0,
            '15001元~35000元': 0,
            '35001元~55000元': 0,
            '55001元~75000元': 0,
            '75001元~95000元': 0,
            '95000元以上': 0
        }
        for i in money_re:
            if i <= 15000:
                d['少于15000元'] = d['少于15000元'] + 1
            elif i <= 35000:
                d['15001元~35000元'] = d['15001元~35000元'] + 1
            elif i <= 55000:
                d['35001元~55000元'] = d['35001元~55000元'] + 1
            elif i <= 75000:
                d['55001元~75000元'] = d['55001元~75000元'] + 1
            elif i <= 95000:
                d['75001元~95000元'] = d['75001元~95000元'] + 1
            elif i > 95000:
                d['95000元以上'] = d['95000元以上'] + 1
        for cl in d:
            # print(bl)
            c = {}
            c['name'] = cl
            c['y'] = d[cl]
            JDJFMON.append(c)
        return JDJFMON



    # 结案方式 饼图
    def settlement_method(self):
        settlement_method = {
            '判决': 0,
            '撤诉': 0,
            '调解': 0,
            '其他': 0
        }
        a = ['判决', '撤诉', '调解']
        for i in JDJF.objects(Q(案由='借贷纠纷')):
            b = i.庭审过程
            for j in a:
                if j in b:
                    settlement_method[j] = settlement_method[j] + 1
                else:
                    settlement_method['其他'] = settlement_method['其他'] + 1
        return settlement_method



case_evidence = {'借条': 23598, '借款合同': 10492, '转账凭证': 3378,'其它':1210}
JDJFMON_result = [{'name': '少于15000元', 'y': 798}, {'name': '15001元~35000元', 'y': 710},
                  {'name': '35001元~55000元', 'y': 599}, {'name': '55001元~75000元', 'y': 299},
                  {'name': '75001元~95000元', 'y': 169}, {'name': '95000元以上', 'y': 1571}]
settlement_result = {'判决': 33025, '撤诉': 10384, '调解': 1289, '其他': 920}

# d,f=MsJdjfData().get_defendant_edujob()
# JDEDU=MsJdjfData().get_case_edu_number(d)
# job=list(f.keys())
# job_number=list(f.values())
# job_all=[job,job_number]
# print(job_all)
# print(JDEDU)
# print(JDJF.objects(Q(案由='借贷纠纷')).count())
# court = MsJdjfData().get_court_info()#'各地区案件数量'
# age_info = MsJdjfData().get_pre_age_info()#获得未处的年龄数据
# print(age_info)
# chart_age_data = MsJdjfData().get_chart_age_data(age_info)#对未处理的年龄数据进行处理
# case_date_number = MsJdjfData().get_case_date_number()
# print(chart_age_data)
# print(case_date_number)
#为了提高展示速度，将相关数据进行直接展示

PLAAGE = {'20岁以下': 12, '20~30岁': 3036, '31~40岁': 8232, '41~50岁': 14476, '51~60岁': 9977, '61~70岁': 4084, '70岁以上': 1218}
PLAAGE_FEMALE = {'20岁以下': 2, '20~30岁': 650, '31~40岁': 2069, '41~50岁': 3453, '51~60岁': 2429, '61~70岁': 933, '70岁以上': 220}
PLAAGE_MALE = {'20岁以下': 7, '20~30岁': 2000, '31~40岁': 5257, '41~50岁': 9463, '51~60岁': 6543, '61~70岁': 2765, '70岁以上': 892}
DEFAGE = {'20岁以下': 11, '20~30岁': 4021, '31~40岁': 10765, '41~50岁': 14892, '51~60岁': 10247, '61~70岁': 2200, '70岁以上': 324}
DEFAGE_MALE = {'20岁以下': 9, '20~30岁': 3069, '31~40岁': 8413, '41~50岁': 11840, '51~60岁': 7903, '61~70岁': 1594, '70岁以上': 232}
DEFAGE_FEMALE = {'20岁以下': 2, '20~30岁': 933, '31~40岁': 2347, '41~50岁': 3036, '51~60岁': 2318, '61~70岁': 597, '70岁以上': 90}
plaintiff_sex = {'男': 27304, '女': 14257}
defendant_sex = {'男': 33677, '女': 9513}
aj_male = [plaintiff_sex['男'],defendant_sex['男']]
aj_female = [plaintiff_sex['女'],defendant_sex['女']]
case_date_number = {'2017': 12318, '2018': 28544, '2019': 5416}
bubble_data = MsJdjfData().get_bubble_data(PLAAGE, DEFAGE)


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
        line_data = [date_list, date_number, '借贷纠纷案件']
        return line_data

    def get_overview_data(self):
        map_jdjf_data = MsJdjfData().get_map_data()
        jdjf_ajnumber = 47206#LHJF.objects.count()  #
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

overview_data_jdjf = OverviewInfo().get_overview_data()





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
        his_job_data = [['无业游民', '工人', '自营业主', '教师', '医生', '农民'], [1550, 760, 130, 20, 15, 410]]
        person_info['pie_age_data'] = pie_age_data
        person_info['pie_edu_data'] = pie_edu_data
        person_info['his_age_data'] = his_age_data
        person_info['his_job_data'] = his_job_data
        return person_info
person_info_jdjf = ChartData().get_person_info()

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
        pie_evidence_data = {
            'name': '证据分析',
            'data': case_analysis().get_pie_data(case_evidence)
        }
        pie_JDJFMON_data = {
            'name': '借贷数额分析 ',
            'data': JDJFMON_result
        }
        pie_settlement_data = {
            'name': '结案方式分析 ',
            'data': case_analysis().get_pie_data(settlement_result)
        }
        analysis['pie_evidence_data']=pie_evidence_data
        analysis['pie_JDJFMON_data'] = pie_JDJFMON_data
        analysis['pie_settlement_data']=pie_settlement_data
        return analysis
analysis_jdjf=case_analysis().special_case_analysis
