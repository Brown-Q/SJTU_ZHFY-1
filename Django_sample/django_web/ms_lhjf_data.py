#coding: utf-8
import re
from mongoengine import *
disconnect()
connect('TOPIC_data', host='202.121.180.66', port=7101)

class LHJF(Document):
    头部信息=StringField()
    当事人信息 = StringField()
    庭审过程 = StringField()
    尾部信息 = StringField()
    meta = {
        'collection': 'LHJF_data'
    }


class MsLhjfData:
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
        for i in LHJF.objects:
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
        court1 = [
            ('江津区人民法院', 4357), ('万州区人民法院', 4349), ('合川区人民法院', 3247), ('云阳县人民法院', 3210), ('綦江区人民法院', 3103), ('开州区人民法院', 3012), ('渝北区人民法院', 2925), ('沙坪坝区人民法院', 2716), ('巴南区人民法院', 2679), ('涪陵区人民法院', 2639), ('九龙坡区人民法院', 2580), ('彭水苗族土家族自治县人民法院', 2551), ('奉节县人民法院', 2507), ('永川区人民法院', 2454), ('大足区人民法院', 2223), ('北碚区人民法院', 2139), ('荣昌区人民法院', 2066), ('垫江县人民法院', 2063), ('巫山县人民法院', 1994), ('丰都县人民法院', 1981), ('铜梁区人民法院', 1868), ('梁平区人民法院', 1839), ('潼南区人民法院', 1803), ('南川区人民法院', 1748), ('长寿区人民法院', 1669), ('忠县人民法院', 1606), ('璧山区人民法院', 1590), ('南岸区人民法院', 1560), ('石柱土家族自治县人民法院', 1387), ('江北区人民法院', 1381), ('巫溪县人民法院', 1326), ('黔江区人民法院', 1246), ('渝中区人民法院', 1096), ('梁平县人民法院', 1014), ('酉阳土家族苗族自治县人民法院', 952), ('城口县人民法院', 943), ('秀山土家族苗族自治县人民法院', 941), ('大渡口区人民法院', 892), ('开县人民法院', 741), ('武隆区人民法院', 682), ('第一中级人民法院', 606), ('第五中级人民法院', 561), ('江津市人民法院', 555), ('武隆县人民法院', 460), ('第二中级人民法院', 342), ('荣昌县人民法院', 265), ('合川市人民法院', 231), ('第三中级人民法院', 177), ('人民法院', 169), ('璧山县人民法院', 161), ('第四中级人民法院', 113), ('高级人民法院', 97)]
        court = {}
        for i in court1:
            m = i[0].replace('区','')
            m = m.replace('人民法院', '')
            m = m.replace('自治县', '')
            m = m.replace('市', '')
            m = m.replace('苗族', '')
            m = m.replace('土家族', '')
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
        court = MsLhjfData().get_court_info()
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
        chart_age_data['PLAAGE'] = MsLhjfData().age_dict_get(age_info[1])#'原告年龄分布'
        chart_age_data['DEFAGE'] = MsLhjfData().age_dict_get(age_info[2])#'原告女性年龄分布'
        chart_age_data['PLAAGE_MALE'] = MsLhjfData().age_dict_get(age_info[3])#'原告男性年龄分布'
        chart_age_data['PLAAGE_FEMALE'] = MsLhjfData().age_dict_get(age_info[4])#'被告年龄分布'
        chart_age_data['DEFAGE_MALE'] = MsLhjfData().age_dict_get(age_info[5])#'被告男性年龄分布'
        chart_age_data['DEFAGE_FEMALE'] = MsLhjfData().age_dict_get(age_info[6])#'被告女性年龄分布'
        chart_age_data['plaintiff_sex'] = MsLhjfData().age_dict_get(age_info[7])#原告性别分布
        chart_age_data['defendant_sex'] = MsLhjfData().age_dict_get(age_info[8])#被告性别分布
        return chart_age_data


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
            '2018': 0,
            '2017': 0,
            '2016': 0
        }
        for i in LHJF.objects:
            for j in i.尾部信息.split('、'):
                if ('年' in j) and ('月' in j) and ('日' in j) and ('二' in j):
                    if ('二○一八' in j) or ('二〇一八' in j):
                        case_date_number['2018'] += 1
                    elif ('二○一七' in j) or ('二〇一七' in j):
                        case_date_number['2017'] += 1
                    elif ('二○一六' in j) or ('二〇一六' in j):
                        case_date_number['2016'] += 1
                    break
        return case_date_number

    # 婚姻存续时间
    def marriage_duration(self):
        marriage_duration={}
        for i in LHJF.objects():
            a=i.庭审过程
            b=a.split('、')
            for j in b:
                if '结婚' in j and '年' in j:
                    c=re.split('，|。',j)
                    for k in c:
                        if '结婚' in k and '年' in k:
                            marriage_date = re.findall(r'(\d{4})年', k)
                            if marriage_date:
                                marriage_time=2019-int(marriage_date[0])
                                if str(marriage_time) in marriage_duration:
                                    marriage_duration[str(marriage_time)]=marriage_duration[str(marriage_time)]+1
                                elif str(marriage_time) not in marriage_duration:
                                    marriage_duration[str(marriage_time)]=1
                        break
        marriage_duration=sorted(marriage_duration.items(), key=lambda e: int(e[0]), reverse=False)
        return(marriage_duration)

    #离婚原因
    def divorce_reason(self):
        divorce_reason={
                    '感情不和': 0,
                    '破裂': 0,
                    '家庭暴力': 0,
                    '家暴': 0,
                    '离家': 0,
                    '不归': 0,
                    '不良': 0,
                    '恶习': 0,
                    '重婚': 0,
                    '婚外情':0,
                    '生理缺陷': 0,
                    '缺陷': 0,

        }
        a=['感情不和','破裂','家庭暴力','家暴','离家','不归','不良','恶习','重婚','婚外情','生理缺陷','缺陷']
        for i in LHJF.objects():
            b = i.庭审过程
            for j in a:
                if j in b:
                    divorce_reason[j]=divorce_reason[j]+1
        return(divorce_reason)

    #判决结果
    def Divorce_result(self):
        divorce_result = {'解除婚姻关系': 0, '维持婚姻关系': 0}
        for i in LHJF.objects():
            a = i.庭审过程
            b = a.split('、')
            for j in b:
                if j.endswith('判决如下：'):
                    c = b.index(j)
                    k1 = b[c + 1]
                    k2 = b[c + 2]
                    k3 = b[c + 3]
                    if '离婚' in k1 or '离婚' in k2 or '离婚' in k3:
                        divorce_result['解除婚姻关系'] = divorce_result['解除婚姻关系'] + 1
                    elif '撤诉' in k1 or '驳回' in k1 or '撤诉' in k2 or '驳回' in k2:
                        divorce_result['维持婚姻关系'] = divorce_result['维持婚姻关系'] + 1
        return divorce_result



marriage_time=[('1', 13), ('2', 67), ('3', 119), ('4', 133), ('5', 132), ('6', 131), ('7', 132), ('8', 145), ('9', 126), ('10', 108), ('11', 102), ('12', 103), ('13', 78), ('14', 54), ('15', 76), ('16', 62), ('17', 61), ('18', 53), ('19', 65), ('20', 61), ('21', 71), ('22', 74), ('23', 70), ('24', 64), ('25', 47), ('26', 50), ('27', 40), ('28', 36), ('29', 39), ('30', 39), ('31', 24), ('32', 38), ('33', 18), ('34', 12), ('35', 11), ('36', 9), ('37', 12), ('38', 11), ('39', 9), ('40', 4), ('41', 3), ('42', 3), ('43', 3), ('44', 1), ('45', 6), ('46', 3), ('50', 6), ('56', 3), ('57', 1)]
divorce_cause={'感情不和': 8307,'家庭暴力': 982,'离家不归': 917,'不良恶习': 481,'重婚或婚外情': 302,'生理缺陷': 18}
divorce_result = {'解除婚姻关系': 2348, '维持婚姻关系': 2081}
# court = MsLhjfData().get_court_info()#'各地区案件数量'
# age_info = MsLhjfData().get_pre_age_info()#获得未处的年龄数据
# chart_age_data = MsLhjfData().get_chart_age_data(age_info)#对未处理的年龄数据进行处理
# case_date_number = MsLhjfData().get_case_date_number()

#为了提高展示速度，将相关数据进行直接展示
court = {'江津': 5081, '万州': 4691, '合川': 3478, '云阳县': 3210, '綦江': 3103, '开州': 3012, '渝北': 3628, '沙坪坝': 2716, '巴南': 2679, '涪陵': 2816, '九龙坡': 2580, '彭水苗族土家族': 2551, '奉节县': 2507, '永川': 2454, '大足': 2223, '北碚': 2139, '荣昌': 2331, '垫江县': 2063, '巫山县': 1994, '丰都县': 1981, '铜梁': 1868, '梁平': 2853, '潼南': 1803, '南川': 1748, '长寿': 1669, '忠县': 1606, '璧山': 1751, '南岸': 1560, '石柱土家族': 1387, '江北': 1381, '巫溪县': 1326, '黔江': 1359, '渝中': 1096, '酉阳': 952, '城口县': 943, '秀山': 941, '大渡口': 892, '开县': 741, '武隆': 1142, '第五中级': 561}

PLAAGE = {'20岁以下': 27, '20~30岁': 12081, '31~40岁': 31720, '41~50岁': 27133, '51~60岁': 9857, '61~70岁': 2964, '70岁以上': 1011}
PLAAGE_FEMALE = {'20岁以下': 16, '20~30岁': 10464, '31~40岁': 23925, '41~50岁': 18828, '51~60岁': 6413, '61~70岁': 1275, '70岁以上': 227}
PLAAGE_MALE = {'20岁以下': 10, '20~30岁': 1611, '31~40岁': 7768, '41~50岁': 8291, '51~60岁': 3435, '61~70岁': 1687, '70岁以上': 781}
DEFAGE = {'20岁以下': 3, '20~30岁': 7616, '31~40岁': 29196, '41~50岁': 30471, '51~60岁': 12635, '61~70岁': 3798, '70岁以上': 903}
DEFAGE_MALE = {'20岁以下': 1, '20~30岁': 4281, '31~40岁': 21046, '41~50岁': 23250, '51~60岁': 9431, '61~70岁': 2585, '70岁以上': 535}
DEFAGE_FEMALE = {'20岁以下': 1, '20~30岁': 3331, '31~40岁': 8132, '41~50岁': 7190, '51~60岁': 3193, '61~70岁': 1217, '70岁以上': 366}
plaintiff_sex = {'男': 23608, '女': 61221}
defendant_sex = {'男': 61336, '女': 23486}
aj_male = [plaintiff_sex['男'],defendant_sex['男']]
aj_female = [plaintiff_sex['女'],defendant_sex['女']]
case_date_number = {'2016': 20149, '2017': 29843, '2018': 27419}

bubble_data = MsLhjfData().get_bubble_data(PLAAGE, DEFAGE)


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
        line_data = [date_list, date_number, '离婚纠纷案件']
        return line_data

    def get_overview_data(self):
        map_lhjf_data = MsLhjfData().get_map_data()
        lhjf_ajnumber = 85696#LHJF.objects.count()  #
        lhjf_pnumber = plaintiff_sex['男'] + plaintiff_sex['女'] + defendant_sex['男'] + defendant_sex['女']
        region_case_number = OverviewInfo().get_his_row_data(map_lhjf_data)
        line_data = OverviewInfo().get_line_data(case_date_number)
        overview_data_lhjf = {
            'ajnumber': lhjf_ajnumber,
            'pnumber': lhjf_pnumber,
            'map': map_lhjf_data,
            'region_case_number': region_case_number,
            'line_data': line_data,
        }
        return overview_data_lhjf

overview_data_lhjf = OverviewInfo().get_overview_data()



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
        person_info_lhjf = {}
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
        person_info_lhjf['pie_age_data'] = pie_age_data
        person_info_lhjf['pie_edu_data'] = pie_edu_data
        person_info_lhjf['his_age_data'] = his_age_data
        person_info_lhjf['his_job_data'] = his_job_data
        return person_info_lhjf

person_info_lhjf = ChartData().get_person_info()

class case_analysis:
    def __init__(self):
        pass

    def get_line_data(self, data):
        date_list = []
        date_number = []
        for i in data:
            date_list.append(i[0])
            date_number.append(i[1])
        line_data = [date_list, date_number, '离婚纠纷案件']
        return line_data

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
        line_data = case_analysis().get_line_data(marriage_time)
        pie_cause_data = {
            'name': '离婚原因',
            'data': case_analysis().get_pie_data(divorce_cause)
        }
        pie_result_data = {
            'name': '判决结果',
            'data': case_analysis().get_pie_data(divorce_result)
        }
        analysis['line_data']=line_data
        analysis['pie_cause_data']=pie_cause_data
        analysis['pie_result_data'] = pie_result_data
        return analysis
analysis_lhjf=case_analysis().special_case_analysis
# female_num1 = []
# male_num1 = []
# for i,j in PLAAGE_FEMALE.items():
#     female_num1.append(j)
# for i,j in PLAAGE_MALE.items():
#     male_num1.append(-j)
# female_num2 = []
# male_num2 = []
# for i,j in DEFAGE_FEMALE.items():
#     female_num2.append(j)
# for i,j in DEFAGE_MALE.items():
#     male_num2.append(-j)
# print(female_num2)


