import pandas as pd
import numpy as np
import xlrd


class ChartData:
    def __init__(self):
        pass

    #处理表格文件数据得到收结案和地区信息，收结案可以看做矩阵
    def get_sja_data(self):
        sa_number = []
        ja_number = []
        region = []
        for i in range(1, 10):
            url = 'D:\\Django\\data\\sjayc\\df0' + str(i) + '.xlsx'
            excel = xlrd.open_workbook(url)
            sheet = excel.sheet_by_name('Sheet1')
            sa_data = sheet.col_values(3, 1)
            ja_data = sheet.col_values(2, 1)
            region = sheet.col_values(1, 1)
            region = [x+'区' for x in region]
            sa_number.append(sa_data)
            ja_number.append(ja_data)
        for i in range(10, 41):
            url = 'D:\\Django\\data\\sjayc\\df' + str(i) + '.xlsx'
            excel = xlrd.open_workbook(url)
            sheet = excel.sheet_by_name('Sheet1')
            sa_data = sheet.col_values(3, 1)
            ja_data = sheet.col_values(2, 1)
            sa_number.append(sa_data)
            ja_number.append(ja_data)
        return sa_number, ja_number, region

    #将收结案数据处理，得到2016-2019年的年数据
    def get_sjayear_data(self, sja_data):
        year_data = []
        for i in range(3):
            year_meta_data = [0 for x in range(len(sja_data[0]))]
            for j in range(12):
                k = j + 12 * i
                for l in range(len(sja_data[0])):
                    year_meta_data[l] = year_meta_data[l] + sja_data[k][l]
            year_data.append(year_meta_data)
        year_meta_data = [0 for x in range(len(sja_data[0]))]
        for j in range(36, 40):
            for l in range(len(sja_data[0])):
                year_meta_data[l] = year_meta_data[l] + sja_data[j][l]
        year_data.append(year_meta_data)
        return year_data

    #得到地图数据
    def get_map_data(self, region, sa_number):
        map_data = []
        for i in range(len(region)):
            map_meta_data = {}
            map_meta_data['name'] = region[i]
            map_meta_data['value'] = sa_number[i]
            map_data.append(map_meta_data)
        return map_data

    #得到柱状图和地图年份数据，直接传回view
    def get_his_data(self):
        sa_number, ja_number, region = ChartData().get_sja_data()
        sa_data = ChartData().get_sjayear_data(sa_number)
        ja_data = ChartData().get_sjayear_data(ja_number)
        data = []
        for x in range(4):
            meta_data = {}
            meta_data['date'] = str(x+2016)
            meta_data['chart_region'] = region
            meta_data['chart_sa_number'] = sa_data[x]
            meta_data['chart_ja_number'] = ja_data[x]
            meta_data['map'] = ChartData().get_map_data(region, sa_data[x])
            data.append(meta_data)
        return data

    #得到地区分类的40个月数据
    def get_region_data(self):
        chart_date = [
            '2016-01-31', '2016-02-29', '2016-03-31', '2016-04-30',
            '2016-05-31', '2016-06-30', '2016-07-31', '2016-08-31',
            '2016-09-30', '2016-10-31', '2016-11-30', '2016-12-31',
            '2017-01-31', '2017-02-28', '2017-03-31', '2017-04-30',
            '2017-05-31', '2017-06-30', '2017-07-31', '2017-08-31',
            '2017-09-30', '2017-10-31', '2017-11-30', '2017-12-31',
            '2018-01-31', '2018-02-28', '2018-03-31', '2018-04-30',
            '2018-05-31', '2018-06-30', '2018-07-31', '2018-08-31',
            '2018-09-30', '2018-10-31', '2018-11-30', '2018-12-31',
            '2019-01-31', '2019-02-28', '2019-03-31'
        ]
        sa_number, ja_number, region = ChartData().get_sja_data()
        region_data = []
        for i in range(len(region)):
            region_meta_data = {}
            region_sa_number = []
            region_ja_number = []
            for j in range(len(sa_number)):
                region_sa_number.append(sa_number[j][i])
                region_ja_number.append(ja_number[j][i])
            region_meta_data['region'] = region[i]
            region_meta_data['chart_date'] = chart_date
            region_meta_data['chart_sa_number'] = region_sa_number
            region_meta_data['chart_ja_number'] = region_ja_number
            region_data.append(region_meta_data)
        return region_data

#返回日期数据和地区数据
date_data = ChartData().get_his_data()
region_data = ChartData().get_region_data()



