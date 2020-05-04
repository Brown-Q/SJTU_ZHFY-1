from django_web.models import XZAJ



class XzData:
    def __init__(self):
        pass

    #获得数据库中各地区法院的案件数量
    def get_court_case_number(self):
        court_case_number = []
        court_list = []
        for i in XZAJ.objects:
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
        case_number = XZAJ.objects.count()
        people_number = 2 * case_number
        map = [{'name': '万州区', 'value': 511}, {'name': '北碚区', 'value': 331}, {'name': '涪陵区', 'value': 989}, {'name': '渝中区', 'value': 816}, {'name': '渝北区', 'value': 2913}]
        date = ['2005年', '2006年', '2007年', '2008年', '2010年', '2011年', '2012年', '2013年', '2014年', '2015年', '2016年', '2017年', '2018年', '2019年']
        date_number = [0, 0, 0, 1, 7, 19, 18, 95, 614, 977, 1453, 1192, 1126, 50]
        region = []
        region_number = []
        date_case_number = [{
            'name': '行政案件',
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
        XZCASE = {
            'xzcase_id': [],
            'xzcase_title': [],
            'xzcase_detail': [],
        }
        for i in XZAJ.objects.limit(10):
            # print(type(str(i.id)))
            XZCASE['xzcase_id'].append(str(i.id))
            XZCASE['xzcase_title'].append(i.标题)
            XZCASE['xzcase_detail'].append(i.庭审过程)
        return XZCASE

    def get_ay_info(self):
        xzcase_info = {
            '信息电讯行政管理(信息、电讯)': 460, '民政行政管理(民政)、行政登记': 1, '民政行政管理(民政)': 1205, '其他(公安)': 249, '道路交通管理(道路)': 28, '公安行政管理:其他(公安)': 118, '公安行政管理:消防管理(消防)': 1, '治安管理(治安)': 59, '公安行政管理:道路交通管理(道路)': 13, '土地行政管理(土地)': 754, '其他(资源)': 664, '林业行政管理(林业)': 107, '资源行政管理:其他(资源)': 474, '资源行政管理:林业行政管理(林业)': 107, '资源行政管理:土地行政管理(土地)': 488, '公安行政管理:治安管理(治安)': 73, '城乡建设行政管理:房屋登记管理(房屋登记)': 110, '房屋拆迁管理(拆迁)': 325, '城市规划管理(规划)': 56, '房屋登记管理(房屋登记)': 62, '城乡建设行政管理:城市规划管理(规划)': 48, '其他(城建)': 11, '城乡建设行政管理:房屋拆迁管理(拆迁)': 114, '消防管理(消防)': 6, '城乡建设行政管理:其他(城建)': 14, '城乡建设行政管理': 1, '地质矿产行政管理(地矿)': 4, '资源行政管理:地质矿产行政管理(地矿)': 6,  '资源行政管理:能源行政管理(能源管理)': 2, }
        ay_info = []
        ay_meta_info = {}
        name = []
        num = []
        for i in sorted(xzcase_info.items(), key=lambda x: x[1], reverse=True):
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
        ay_meta_info['name'] = '行政案由'
        ay_meta_info['data'] = data
        ay_info.append(ay_meta_info)
        return ay_info

    def get_defendant_name(self):
        defendant_name_list = []
        for i in XZAJ.objects:
            for j in i.被告.split('、'):
                if j[:2] in defendant_name_list:
                    continue
                else:
                    defendant_name_list.append(j[:3])
                    # print(j[:3])
        name_list = list(set(defendant_name_list))
        return name_list


xzcase_info = XzData().get_case_info()
xzcase = XzData().get_detail_info()
xzay_info = XzData().get_ay_info()


