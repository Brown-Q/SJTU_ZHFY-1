import xlrd


class RangeChartData:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    #得到地区的排名信息，输入需要得到的排名名称
    def get_region_score(self):
        #立案管理排名，审判办理排名，结案管理排名
        data = xlrd.open_workbook(self.url)
        table = data.sheet_by_name(self.name)
        region = table.col_values(0,1)
        score = table.col_values(2,1)
        region = [x+'区' for x in region]
        score = {
            'name': self.name,
            'data': score,
        }
        return region, score

    #得到总的排名，由于展示地区进行数量限制，单写一个函数
    def get_region_score1(self):
        #总排名
        data = xlrd.open_workbook(self.url)
        table = data.sheet_by_name(self.name)
        region = table.col_values(0,1,8)
        score = table.col_values(2,1,8)
        score = [float(format(x, '.3f')) for x in score]
        region = [x+'区' for x in region]
        score = {
            'name': self.name,
            'data': score,
        }
        return region, score

    #得到地图排名数据，数据格式[{'name':$$$, 'value':%% },{},{}]
    def get_map_data(self):
        map_data = []

        data = xlrd.open_workbook(self.url)
        table = data.sheet_by_name(self.name)
        region = table.col_values(0, 1)
        score = table.col_values(2, 1)
        score = [float(format(x, '.3f')) for x in score]
        for i in range(len(region)):
            map_meta_data = {}
            map_meta_data['name'] = region[i] + '区'
            map_meta_data['value'] = score[i]
            map_data.append(map_meta_data)
        return map_data

    #得到饼状图数据
    def get_pie_data(self):
        name = self.name
        pie_data = []
        data = xlrd.open_workbook(self.url)
        table = data.sheet_by_name(name)
        region = table.col_values(0, 2)
        score = table.col_values(7, 2)
        for i in range(len(region)):
            pie_meta_data = {}
            pie_meta_data['name'] = region[i] + '区'
            pie_meta_data['y'] = score[i]
            pie_data.append(pie_meta_data)
        return pie_data

    #得到柱状图数据，输入为指标在数据表的位置和图表名称
    def get_his_data(self, start, end, his_name):
        pie_data = []
        data = xlrd.open_workbook(self.url)
        table = data.sheet_by_name(self.name)
        region = table.col_values(0, 2)
        index = []
        for i in range(start, end+1):
            index.append(table.col_values(i))
        region = [x + '区' for x in region]
        h_data = []
        for i in index:
            h_meta_data = {}
            meta_data = {}
            h_meta_data['name'] = i[0]
            meta_data['name'] = i[0]
            meta_data['y'] = i[1]
            i[2:] = [float(format(x, '.3f')) for x in i[2:]]
            h_meta_data['data'] = i[2:]
            h_data.append(h_meta_data)
            pie_data.append(meta_data)
        hdata = {
            'name': his_name,
            'region': region,
            'data': h_data,
        }
        return hdata, pie_data

#排名数据
url_result = 'D:\\Django\\data\\tsyp\\result.xls'
url_data = 'D:\\Django\\data\\tsyp\\data.xls'
zzx_region, zzx_score = RangeChartData('总排名', url_result).get_region_score1()
lagl_region, lagl_score = RangeChartData('立案管理排名', url_result).get_region_score()
spbl_region, spbl_score = RangeChartData('审判办理排名', url_result).get_region_score()
jagl_region, jagl_score = RangeChartData('结案管理排名', url_result).get_region_score()
XXgl_region, XXgl_score = [0,0]
map_data = RangeChartData('总排名', url_result).get_map_data()
#饼图数据
lasl_data = RangeChartData('全部地区', url_data).get_pie_data()
#柱状图数据
ysxg_hdata, yszs_data = RangeChartData('全部地区', url_data).get_his_data(14, 15, '一审效果指数')
jazx_hdata, jazx_data = RangeChartData('全部地区', url_data).get_his_data(21, 24, '结案与执行指数')
