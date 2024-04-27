from django.shortcuts import render
from django.http import JsonResponse
from .sql import *
from .test import *
import json
import pandas as pd
import os
def test(request):
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)
    data=pd.read_csv(f'{parent_path}/gene_list1.csv')
    # data=pd.read_csv('/root/skin/gene_list1.csv')
    func_list=data['Func.refGene'].drop_duplicates().to_list()
    gene_list=data['Gene.refGene'].drop_duplicates().to_list()
    return render(request, 'test.html', locals())
def ajax_test(request):
    func=request.POST.get('func')
    genes_name=request.POST.get('genes')
    print(func)
    # df,columns_name=get_sql_data(genes_name)
    data,columns_name=read_data_csv(func,genes_name)
    json_string1 = data.to_json(orient='records')
    data = json.loads(json_string1)  

    response={
            'data':data,
            'columns_name':columns_name
       
    }
    
    return JsonResponse(response)
def ajax_find_alldata(request):
    func=request.POST.get('Func_refGene')
    genes_name=request.POST.get('Gene_refGene')
    patient_number=request.POST.get('patient_number')
    print(type(genes_name),type(func),(patient_number))
    if 'patient' in patient_number:
        data,columns_name=run_alldata(patient_number,genes_name,func)
    elif patient_number=='count_values':
        data,columns_name=sql_func_prove(func,genes_name)
    # df,columns_name=get_sql_data(genes_name)
    # data,columns_name=read_data_csv(func,genes_name)
    json_string1 = data.to_json(orient='records')
    data = json.loads(json_string1)  

    response={
            'data':data,
            'columns_name':columns_name
       
    }
    
    return JsonResponse(response)
def filter_web(request):

    return render(request, 'filter_web.html', locals())
def ajax_filter_web(request):
    gene_name=request.POST.get('genes')
    CADD_phred_select=request.POST.get('CADD_phred_select')
    CADD_phred_value=request.POST.get('CADD_phred_value')
    checkbox_value=request.POST.getlist('checkbox_value[]')
    ExAC_ALL_select=request.POST.get('ExAC_ALL_select')
    ExAC_ALL_value=request.POST.get('ExAC_ALL_value')
    DANN_score_select=request.POST.get('DANN_score_select')
    DANN_score_value=request.POST.get('DANN_score_value')
    SIFT_score_select=request.POST.get('SIFT_score_select')
    SIFT_score_value=request.POST.get('SIFT_score_value')
    MutationTaster_score_select=request.POST.get('MutationTaster_score_select')
    MutationTaster_score_value=request.POST.get('MutationTaster_score_value')
    # print(gene_name)
    data_for_one_sig,data_for_two_sig,data_for_all_sig,column_names_for_one_sig,column_names_for_two_sig,column_names_for_all_sig=process_data_genename(gene_name,checkbox_value,ExAC_ALL_select,ExAC_ALL_value,CADD_phred_select,
                                                                                                                                                        CADD_phred_value,DANN_score_select,DANN_score_value,
                                                                                                                                                        SIFT_score_select,SIFT_score_value,MutationTaster_score_select,MutationTaster_score_value )

    json_string1 = data_for_one_sig.to_json(orient='records')
    data_for_one_sig = json.loads(json_string1)  
    json_string2 = data_for_two_sig.to_json(orient='records')
    data_for_two_sig = json.loads(json_string2)  
    json_string_all = data_for_all_sig.to_json(orient='records')
    data_for_all_sig = json.loads(json_string_all)  
    response={
            'data_for_one_sig':data_for_one_sig,
            'data_for_two_sig':data_for_two_sig,
            'data_for_all_sig':data_for_all_sig,
            'columns_name_for_one_sig':column_names_for_one_sig,
            'columns_name_for_two_sig':column_names_for_two_sig,
            'columns_name_for_all_sig':column_names_for_all_sig
            
       
    }
    
    return JsonResponse(response)
def ajax_for_two_sig_detail(request):
    func=request.POST.get('Func_refGene')
    genes_name=request.POST.get('Gene_refGene')
    patient_number=request.POST.get('patient_number')
    CADD_phred_select=request.POST.get('CADD_phred_select')
    CADD_phred_value=request.POST.get('CADD_phred_value')
    checkbox_value=request.POST.getlist('checkbox_value[]')
    ExAC_ALL_select=request.POST.get('ExAC_ALL_select')
    ExAC_ALL_value=request.POST.get('ExAC_ALL_value')
    DANN_score_select=request.POST.get('DANN_score_select')
    DANN_score_value=request.POST.get('DANN_score_value')
    SIFT_score_select=request.POST.get('SIFT_score_select')
    SIFT_score_value=request.POST.get('SIFT_score_value')
    MutationTaster_score_select=request.POST.get('MutationTaster_score_select')
    MutationTaster_score_value=request.POST.get('MutationTaster_score_value')
    print(func)
    data,columns_name=process_detail_one_sig(patient_number,genes_name)
    data=data[data['Func_refGene'].isin([func])]
    data=filter_for_condition(data,ExAC_ALL_select,ExAC_ALL_value,CADD_phred_select,
                              CADD_phred_value,DANN_score_select,DANN_score_value,
                              SIFT_score_select,SIFT_score_value,MutationTaster_score_select,MutationTaster_score_value).fillna('.')
    json_string1 = data.to_json(orient='records')
    data = json.loads(json_string1)
    print(columns_name)

    response={
            'data':data,
            'columns_name':columns_name
       
    }
    
    return JsonResponse(response)
def ajax_for_one_sig_detail(request):
    genes_name=request.POST.get('Gene_refGene')
    patient_number=request.POST.get('patient_number')
    CADD_phred_select=request.POST.get('CADD_phred_select')
    CADD_phred_value=request.POST.get('CADD_phred_value')
    checkbox_value=request.POST.getlist('checkbox_value[]')
    ExAC_ALL_select=request.POST.get('ExAC_ALL_select')
    ExAC_ALL_value=request.POST.get('ExAC_ALL_value')
    DANN_score_select=request.POST.get('DANN_score_select')
    DANN_score_value=request.POST.get('DANN_score_value')
    SIFT_score_select=request.POST.get('SIFT_score_select')
    SIFT_score_value=request.POST.get('SIFT_score_value')
    MutationTaster_score_select=request.POST.get('MutationTaster_score_select')
    MutationTaster_score_value=request.POST.get('MutationTaster_score_value')
    data,columns_name=process_detail_one_sig(patient_number,genes_name)
    data=data[data['Func_refGene'].isin(checkbox_value)]
    data=filter_for_condition(data,ExAC_ALL_select,ExAC_ALL_value,CADD_phred_select,
                              CADD_phred_value,DANN_score_select,DANN_score_value,
                              SIFT_score_select,SIFT_score_value,MutationTaster_score_select,MutationTaster_score_value).fillna('.')
    json_string1 = data.to_json(orient='records')
    data = json.loads(json_string1)
    print(columns_name)

    response={
            'data':data,
            'columns_name':columns_name
       
    }
    
    return JsonResponse(response)
# Create your views here.
