from django.shortcuts import render
from django_web.models import *
from django_web.xs_wxjs_data import *
from django_web.xs_dqz_data import *
from django_web.xs_dpz_data import *
from django_web.ms_lhjf_data import *
from django_web.ms_jdjf_data import *
from django_web.ms_ldhtjf_data import *
from django_web.ms_cpzrjf_data import *
from django_web.ms_jcjf_data import *
from django_web.sjayc_data import *
from django_web.tsyp_data import *
from django_web.overview import *
# Create your views here.
def index(request):
    return render(request,'index.html')

def overview(request):

    context = {
        'case_info': case_info,
        'CASE': CASE,
        'CASE_CATE': '总体'
    }
    return render(request,'home/overview.html',context)
def chart1(request):
    context = {
        'CASE_INFO': mscase_info,
        'AY_INFO': msay_info,
        'MSCASE': mscase,
        'CASE_CATE': '民事'
    }
    return render(request,'home/chart1.html',context)
def chart2(request):
    context = {
        'CASE_INFO': xscase_info,
        'AY_INFO': xsay_info,
        'XSCASE': xscase,
        'CASE_CATE': '刑事'
    }
    return render(request,'home/chart2.html',context)
def chart3(request):
    context = {
        'CASE_INFO': xzcase_info,
        'AY_INFO': xzay_info,
        'XZCASE': xzcase,
        'CASE_CATE': '行政'
    }
    return render(request,'home/chart3.html',context)

def wxjsz(request):

    context = {
        'AY_INFO': xsay_info,
        'F_chart_data': F_chart_wxjs_data,
        'S_chart_data': S_chart_wxjs_data,
        'T_chart_data': T_chart_wxjs_data,
    }
    return render(request, 'XS_topic/WXJSZ.html',context)
def dqz(request):
    context = {
        'AY_INFO': xsay_info,
        'F_chart_data': F_chart_dqz_data,
        'S_chart_data': S_chart_dqz_data,
        'T_chart_data': T_chart_dqz_data,
    }
    return render(request, 'XS_topic/DQZ.html',context)

def dpz(request):
    context = {
        'AY_INFO': xsay_info,
        'F_chart_data': F_chart_dpz_data,
        'S_chart_data': S_chart_dpz_data,
        'T_chart_data': T_chart_dpz_data,
    }
    return render(request, 'XS_topic/DPZ.html',context)

def lhjf(request):
    context={
        'person_info': person_info_lhjf,
        'msay_info': msay_info,
        'overview_data':overview_data_lhjf,
        'analysis': analysis_lhjf,
    }
    return render(request, 'MS_topic/LHJF.html',context)

def jdjf(request):
    context={
        'person_info': person_info_jdjf,
        'msay_info': msay_info,
        'overview_data':overview_data_jdjf,
        'analysis': analysis_jdjf,
    }
    return render(request, 'MS_topic/JDJF.html',context)

def ldhtjf(request):
    context={
        'person_info': person_info_ldhtjf,
        'msay_info': msay_info,
        'overview_data':overview_data_ldhtjf,
        'analysis': analysis_ldhtjf,
    }
    return render(request, 'MS_topic/LDHTJF.html',context)

def cpzrjf(request):
    context={
        'person_info': person_info_cpzrjf,
        'msay_info': msay_info,
        'overview_data':overview_data_cpzrjf,
        'analysis': analysis_cpzrjf,
    }
    return render(request, 'MS_topic/CPZRJF.html',context)

def jcjf(request):
    context={
        'person_info': person_info_jcjf,
        'msay_info': msay_info,
        'overview_data':overview_data_jcjf,
        'analysis': analysis_jcjf,
    }
    return render(request, 'MS_topic/JCJF.html',context)

def sjayc(request):
    context = {
        'date_data': date_data,
        'region_data': region_data,
    }
    return render(request, 'sjayc/sjayc1.html', context)

def tsyp(request):

    context = {
        'range_data': [
            {
                'name': '总质效排名',
                'region': zzx_region,
                'score': zzx_score,
            },
            {
                'name': '立案管理排名',
                'region': lagl_region,
                'score': lagl_score,
            },
            {
                'name': '审判办理排名',
                'region': spbl_region,
                'score': spbl_score,
            },
            {
                'name': '结案管理排名',
                'region': jagl_region,
                'score': jagl_score,
            },
            {
                'name': 'XX管理排名',
                'region': XXgl_region,
                'score': XXgl_score,
            },

        ],
        'map': map_data,
        'pie_data': [
            {
                'name': '立案数量',
                'data': lasl_data,
            },
            {
                'name': '一审效果指数',
                'data': yszs_data,
            },
            {
                'name': '结案与执行指数',
                'data': jazx_data,
            },
        ],
        'histogram_data': [ysxg_hdata, jazx_hdata],
    }
    return render(request, 'tsyp/tsyp1.html', context)

def get_detail_page(request,case_id_cate):
    case_cate = case_id_cate.split('&&')[1]
    case_id = case_id_cate.split('&&')[0]
    if case_cate == '总体':
        for case in MSAJ.objects:
            # print(case_id)
            case_defendant = ''
            if case_id == str(case.id):
                if case.庭审过程 == '':
                    case_detail = '无庭审信息'
                else:
                    case_detail = case.庭审过程
                case_title = case.标题
                for case_defendant_list in case.当事人.split('、'):
                    if case_defendant == '':
                        case_defendant = case_defendant_list
                    else:
                        case_defendant = case_defendant + '\n' + case_defendant_list
                break
    elif case_cate == '民事':
        for case in MSAJ.objects:
            # print(case_id)
            case_defendant = ''
            if case_id == str(case.id):
                if case.庭审过程 == '':
                    case_detail = '无庭审信息'
                else:
                    case_detail = case.庭审过程
                case_title = case.标题
                for case_defendant_list in case.当事人.split('、'):
                    if case_defendant == '':
                        case_defendant = case_defendant_list
                    else:
                        case_defendant = case_defendant + '\n' + case_defendant_list
                break
    elif case_cate == '刑事':
        for case in XSAJ.objects:
            # print(case_id)
            case_defendant = ''
            if case_id == str(case.id):
                if case.庭审过程 == '':
                    case_detail = '无庭审信息'
                else:
                    case_detail = case.庭审过程
                case_title = case.标题
                for case_defendant_list in case.当事人.split('、'):
                    if case_defendant == '':
                        case_defendant = case_defendant_list
                    else:
                        case_defendant = case_defendant + '\n' + case_defendant_list
                break
    elif case_cate == '行政':
        for case in XZAJ.objects:
            # print(case_id)
            case_defendant = ''
            if case_id == str(case.id):
                if case.庭审过程 == '':
                    case_detail = '无庭审信息'
                else:
                    case_detail = case.庭审过程
                case_title = case.标题
                for case_defendant_list in case.当事人.split('、'):
                    if case_defendant == '':
                        case_defendant = case_defendant_list
                    else:
                        case_defendant = case_defendant + '\n' + case_defendant_list
                break
    return render(request, 'home/detail.html',
                  {
                      'case_detail': case_detail,
                      'case_title': case_title,
                      'case_defendant': case_defendant,
                      'case_category': case_cate,

                  }
                  )



