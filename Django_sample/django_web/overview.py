from django_web.ms_data import *
from django_web.xs_data import *
from django_web.xz_data import *
import copy

allcase_info = {
    '民事案件': copy.deepcopy(mscase_info),
    '刑事案件': copy.deepcopy(xscase_info),
    '行政案件': copy.deepcopy(xzcase_info),
}
cate = ['民事案件', '刑事案件', '行政案件']

class OverView:
    def __init__(self):
        pass

    def get_ay_info(self):
        ay_info = []
        ay_info.append(msay_info[0])
        ay_info.append(xsay_info[0])
        ay_info.append(xzay_info[0])
        return ay_info

    def get_pie_case_number(self, cate, allcase_info):
        pie_case_number = []
        for i in cate:
            pie_meta_case_number = {}
            pie_meta_case_number['name'] = i
            pie_meta_case_number['y'] = allcase_info[i]['case_number']
            pie_case_number.append(pie_meta_case_number)
        return pie_case_number

    def get_pie_people_number(self, cate, allcase_info):
        pie_people_number = []
        for i in cate:
            pie_meta_people_number = {}
            pie_meta_people_number['name'] = i
            pie_meta_people_number['y'] = allcase_info[i]['people_number']
            pie_people_number.append(pie_meta_people_number)
        return pie_people_number

    def get_region_case_number(self, data):
        case_info = copy.deepcopy(data['民事案件']['region_case_number'])
        # case_info[0][0] = 0
        # print(case_info)
        # print(data['民事案件']['region_case_number'])
        # print(case_info is data['民事案件']['region_case_number'])
        for i in range(len(case_info[0])):
            for j in range(len(data['刑事案件']['region_case_number'][0])):
                if case_info[0][i] == data['刑事案件']['region_case_number'][0][j]:
                    case_info[1][i] = case_info[1][i] + data['刑事案件']['region_case_number'][1][j] + \
                                      data['行政案件']['region_case_number'][1][j]
        return case_info

    def get_map_data(self, data):
        map_data = []
        for i in range(len(data[0])):
            map_meta_data = {}
            map_meta_data['name'] = data[0][i]
            map_meta_data['value'] = data[1][i]
            map_data.append(map_meta_data)
        return map_data

    def get_line_data(self):
        date_case_data = copy.deepcopy(allcase_info['民事案件']['date_case_number'])
        line_data = []
        for i in cate:
            line_data.append(allcase_info[i]['date_case_number'][1][0])
        date_case_data[1] = line_data
        return date_case_data

    def get_case_detail(self):
        CASE = {
            'case_id': [],
            'case_title': [],
            'case_detail': [],
        }
        for i in MSAJ.objects.limit(10):
            # print(type(str(i.id)))
            CASE['case_id'].append(str(i.id))
            CASE['case_title'].append(i.标题)
            CASE['case_detail'].append(i.庭审过程)
        return CASE

    def get_case_info(self):
        case_info = {}
        pie_case_number = OverView().get_pie_case_number(cate, allcase_info)
        pie_people_number = OverView().get_pie_people_number(cate, allcase_info)
        ay_info = OverView().get_ay_info()
        region_case_number = OverView().get_region_case_number(allcase_info)
        map_data = OverView().get_map_data(region_case_number)
        line_data = OverView().get_line_data()
        case_info['pie_case_number'] = pie_case_number
        case_info['pie_people_number'] = pie_people_number
        case_info['ay_info'] = ay_info
        case_info['region_case_number'] = region_case_number
        case_info['map_data'] = map_data
        case_info['line_data'] = line_data
        return case_info


case_info = OverView().get_case_info()
CASE = OverView().get_case_detail()
print(case_info['map_data'])










