# coding:utf-8
from django_web.models import XSAJ


class XsData:
    def __init__(self):
        pass

    #获得数据库中各地区法院的案件数量
    def get_court_case_number(self):
        court_case_number = []
        court_list = []
        for i in XSAJ.objects:
            meta_court_case_number = {}
            region_demo = i.法院.split('市')[1].split('区')[0]
            if len(region_demo) > 3:
                region = region_demo
            else:
                region = region_demo + '区'
            # print(region)
            if region not in court_list:
                meta_court_case_number['name'] = region
                meta_court_case_number['value'] = 1
                court_list.append(region)
                court_case_number.append(meta_court_case_number)
            else:
                for j in court_case_number:
                    if j['name'] == region:
                        j['value'] = j['value'] + 1

    def get_case_info(self):
        case_info = {}
        case_number = XSAJ.objects.count()
        people_number = 2 * case_number
        map = [{'name': '万州区', 'value': 3064}, {'name': '北碚区', 'value': 1456}, {'name': '涪陵区', 'value': 2238},
                {'name': '渝中区', 'value': 2558}, {'name': '渝北区', 'value': 2704}]
        date = ['2005年', '2006年', '2007年', '2008年', '2009年', '2010年', '2011年', '2012年', '2013年', '2014年', '2015年', '2016年', '2017年', '2018年', '2019年']
        date_number = [7, 1, 4, 6, 5, 67, 72, 226, 1743, 2134, 2347, 2507, 2614, 269]
        region = []
        region_number = []
        date_case_number = [{
            'name': '刑事案件',
            'data': date_number,
        }]
        for i in map:
            region.append(i['name'])
            region_number.append(i['value'])
        case_info['case_number'] = case_number
        case_info['people_number'] = people_number
        case_info['map'] = map
        case_info['region_case_number'] = [region, region_number]
        case_info['date_case_number'] = [date, date_case_number]
        return case_info

    def get_detail_info(self):
        XSCASE = {
            'xscase_id': [],
            'xscase_title': [],
            'xscase_detail': [],
        }
        for i in XSAJ.objects.limit(10):
            # print(type(str(i.id)))
            XSCASE['xscase_id'].append(str(i.id))
            XSCASE['xscase_title'].append(i.标题)
            XSCASE['xscase_detail'].append(i.庭审过程)
        return XSCASE

    def get_ay_info(self):
        xscase_info = {
    '交通肇事罪': 344, '危险驾驶罪': 1415, '非法制造、买卖、运输、邮寄、储存枪支、弹药、爆炸物罪': 1161, '以危险方法危害公共安全罪': 13, '重大责任事故罪': 5, '危险驾驶罪、危害公共安全罪': 2, '非法持有、私藏枪支、弹药罪': 21, '过失以危险方法危害公共安全罪': 6, '投放危险物质罪': 1, '放火罪': 17, '非法制造、买卖、运输、邮寄、储存枪支、弹药、爆炸物罪、交通肇事罪': 1, '破坏电力设备罪': 6, '失火罪': 6, '过失投放危险物质罪': 1, '生产、销售假药罪、非法制造、买卖、运输、邮寄、储存枪支、弹药、爆炸物罪': 1, '破坏广播电视设施、公用电信设施罪': 2, '故意伤害罪': 663, '非法拘禁罪': 89, '过失致人死亡罪': 61, '强奸罪': 57, '重婚罪': 75, '出售、非法提供公民个人信息罪': 11, '故意杀人罪': 761, '拐卖妇女、儿童罪': 3, '非法获取公民个人信息罪': 20, '过失致人重伤罪': 4, '遗弃罪': 1, '强制猥亵、侮辱妇女罪': 6, '诈骗罪': 339, '盗窃罪': 2526, '抢劫罪': 244, '抢夺罪': 44, '盗窃罪、抢劫罪': 1, '故意毁坏财物罪': 25, '敲诈勒索罪': 17, '挪用资金罪': 12, '破坏生产经营罪': 2, '侵占罪': 8, '盗窃罪、抢劫罪、抢夺罪': 2, '赌博罪、盗窃罪、强奸罪、抢劫罪': 1, '盗窃罪、抢夺罪': 2, '职务侵占罪': 41, '滥伐林木罪': 176, '非法捕捞水产品罪': 288, '容留他人吸毒罪': 610, '非法持有毒品罪': 264, '开设赌场罪': 100, '引诱、容留、介绍卖淫罪': 78, '走私、贩卖、运输、制造毒品罪': 1664, '组织、利用会道门、邪教组织、利用迷信破坏法律实施罪': 6, '聚众斗殴罪': 44, '伪造、变造、买卖国家机关公文、证件、印章罪': 12, '寻衅滋事罪': 176, '制作、复制、出版、贩卖、传播淫秽物品牟利罪': 7, '非法收购、运输、加工、出售国家重点保护植物、国家重点保护植物制品罪': 3, '妨害公务罪': 53, '招摇撞骗罪': 8, '盗伐林木罪': 38, '非法收购、运输盗伐、滥伐的林木罪': 8, '走私、贩卖、运输、制造毒品罪、容留他人吸毒罪': 3, '非法猎捕、杀害珍贵、濒危野生动物罪': 16, '组织卖淫罪': 3, '非法占用农用地罪': 19, '走私、贩卖、运输、制造毒品罪、非法持有毒品罪': 2, '偷越国（边）境罪': 7, '传播淫秽物品罪': 3, '非法狩猎罪': 12, '非法获取计算机信息系统数据、非法控制计算机信息系统罪': 3, '非法行医罪': 4, '非法处置查封、扣押、冻结的财产罪': 4, '盗掘古文化遗址、古墓葬罪': 1, '伪造公司、企业、事业单位、人民团体印章罪': 9, '非法采矿罪': 10, '窝藏、转移、隐瞒毒品、毒赃罪': 3, '掩饰、隐瞒犯罪': 43, '赌博罪': 14, '非法采伐、毁坏国家重点保护植物罪': 8, '妨害动植物防疫、检疫罪': 2, '故意伤害罪、故意毁坏财物罪、寻衅滋事罪、非法持有毒品罪': 1, '脱逃罪': 1, '非法种植毒品原植物罪': 1, '使用虚假身份证件、盗用身份证件罪': 2, '受贿罪': 125, '行贿罪': 22, '贪污罪': 26, '单位行贿罪': 5, '挪用公款罪': 11, '介绍贿赂罪': 1, '单位受贿罪': 1, '拒不支付劳动报酬罪': 4, '盗窃罪、抢劫罪、脱逃罪、抢夺罪': 1, '危险驾驶罪、抢劫罪': 1, '非法侵入住宅罪': 4, '诽谤罪': 4, '信用卡诈骗罪、诈骗罪': 1, '危险驾驶罪、非法制造、买卖、运输、邮寄、储存枪支、弹药、爆炸物罪': 2, '猥亵儿童罪': 4, '扰乱无线电通讯管理秩序罪': 1, '拒不执行判决、裁定罪': 5, '非法收购、运输、出售珍贵、濒危野生动物、珍贵、濒危野生动物制品罪': 1, '伪造、变造居民身份证罪': 1, '重大劳动安全事故罪': 1, '爆炸罪、非法制造、买卖、运输、邮寄、储存枪支、弹药、爆炸物罪、非法持有、私藏枪支、弹药罪': 3, '诈骗罪、非法制造、买卖、运输、邮寄、储存枪支、弹药、爆炸物罪': 1, '打击报复证人罪': 1, '盗窃罪、走私、贩卖、运输、制造毒品罪': 2, '窝藏、包庇罪': 3, '破坏计算机信息系统罪': 1, '传播性病罪': 1, '组织他人偷越国（边）境罪': 1, '破坏监管秩序罪': 2, '侮辱罪': 7, '绑架罪': 3, '私分国有资产罪': 2, '抢劫罪、非法拘禁罪': 1, '刑讯逼供罪': 2, '组织、领导、参加恐怖组织罪': 1, '组织、领导、参加黑社会性质组织罪': 38, '非法制造、买卖、运输、邮寄、储存枪支、弹药、爆炸物罪、走私、贩卖、运输、制造毒品罪': 1, '强迫卖淫罪': 1, '帮助毁灭、伪造证据罪': 1, '盗窃、侮辱尸体罪': 1, '故意伤害罪、妨害公务罪': 1, '单位行贿罪、行贿罪': 1, '侵占罪、职务侵占罪': 1
        }
        ay_info = []
        ay_meta_info = {}
        name = []
        num = []
        for i in sorted(xscase_info.items(), key=lambda x: x[1], reverse=True):
            name.append(i[0])
            num.append(i[1])
        name = name[:50]
        num = num[:50]
        data = []
        for i in range(6):
            meta_data = {}
            meta_data['name'] = name[i]
            meta_data['value'] = num[i]
            data.append(meta_data)
        ay_meta_info['name'] = '刑事案由'
        ay_meta_info['data'] = data
        ay_info.append(ay_meta_info)
        return ay_info

    def get_defendant_name(self):
        defendant_name_list = []
        for i in XSAJ.objects:
            for j in i.被告.split('、'):
                if j[:2] in defendant_name_list:
                    continue
                else:
                    defendant_name_list.append(j[:3])
                    # print(j[:3])
        name_list = list(set(defendant_name_list))
        return name_list


xscase_info = XsData().get_case_info()
xscase = XsData().get_detail_info()
xsay_info = XsData().get_ay_info()


# XSFYSORT = {'万州区': 3064, '北碚区': 1456, '涪陵区': 2238, '渝中区': 2558, '高级人民法院': 2704}
# XSFY = [{'name': '万州区', 'value': 3064}, {'name': '北碚区', 'value': 1456}, {'name': '涪陵区', 'value': 2238}, {'name': '渝中区', 'value': 2558}, {'name': '渝北区', 'value': 2704}]
# XSAJSJ = ['1970年', '2000年', '2002年', '2004年', '2005年', '2006年', '2007年', '2008年', '2009年', '2011年', '2012年', '2013年', '2014年', '2015年', '2016年', '2017年', '2018年', '2019年']
# XSAJSL = [13, 2, 1, 1, 7, 1, 4, 6, 5, 67, 72, 226, 1743, 2134, 2347, 2507, 2614, 269]


