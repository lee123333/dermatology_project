import csv
import sqlite3
from django.http import JsonResponse
import os
import pandas as pd
import time
def search_and_process_data():#用sql語法取對應值，跑很慢沒啥用
    # input_data_1 = input("Enter input_data_1: ")#DDX11L1
    # input_data_2 = input("Enter input_data_2: ")#ncRNA_exonic
    # result_data = []

    # 使用相對路徑
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)
    db_path = f"{parent_path}\db.sqlite3"
    
    
    numeric_cols = ["ExAC_ALL", "CADD_phred", "DANN_score", "SIFT_score", "MutationTaster_score"]
    thresholds = {}  # 用於存儲用戶輸入的閥值
    for col in numeric_cols:
        threshold = input(f"Enter threshold for {col} (leave blank if not needed): ")
        if threshold.strip():  # 如果輸入不是空白，則轉換為浮點數
            thresholds[col] = float(threshold)
        print(thresholds)


    threshold= thresholds["ExAC_ALL"]
    union_query = "SELECT *, 1 AS patient_number FROM `1_myanno` WHERE"

    # 将阈值条件添加到查询字符串中
    threshold_conditions = []
    parameter=[]
    if "ExAC_ALL" in thresholds:
        threshold_conditions.append("`ExAC_ALL` < ? OR `ExAC_ALL` IS NULL OR `ExAC_ALL` = '.'")
        parameter.append(thresholds["ExAC_ALL"])
    if "CADD_phred" in thresholds:
        threshold_conditions.append("`CADD_phred` > ? OR `CADD_phred` IS NULL OR `CADD_phred` = '.'")
        parameter.append(thresholds["CADD_phred"])
    if "DANN_score" in thresholds:
        threshold_conditions.append("`DANN_score` > ? OR `DANN_score` IS NULL OR `DANN_score` = '.'")
        parameter.append(thresholds["DANN_score"])
    if "SIFT_score" in thresholds:
        threshold_conditions.append("`SIFT_score` > ? OR `SIFT_score` IS NULL OR `SIFT_score` = '.'")
        parameter.append(thresholds["SIFT_score"])
    if "MutationTaster_score" in thresholds:
        threshold_conditions.append("`MutationTaster_score` > ? OR `MutationTaster_score` IS NULL OR `MutationTaster_score` = '.'")
        parameter.append(thresholds["MutationTaster_score"])
    parameter=tuple(parameter)

    # 将条件与 OR 连接
    if threshold_conditions:
        union_query += "(" + " ) AND (".join(threshold_conditions) + ")"
        print(union_query)

    # 使用循环添加 UNION ALL 子句
    for i in range(2,24):
        if i == 17 or i == 18:
            continue
        else:
            union_query += f" UNION ALL SELECT *, {i} AS patient_number FROM `{i}_myanno` WHERE"
            if threshold_conditions:
                union_query += "(" + " ) AND (".join(threshold_conditions) + ")"
    print(union_query)


    with sqlite3.connect(db_path, check_same_thread=False) as db_conn:
    
        db_cursor = db_conn.cursor()
        db_cursor.execute(union_query,parameter * 21)
        table_info = db_cursor.fetchall()
        column_names = [column[0] for column in db_cursor.description]
    column_names=[word.replace('.','_') for word in column_names]
    df = pd.DataFrame(table_info, columns=column_names)
    df.to_csv('123.csv')



    # 加入 Func.refGene 和 ExonicFunc.refGene 的篩選
    # func_ref_gene = input("Enter Func.refGene ('exonic', 'splicing' or comma-separated list, leave blank if not needed): ")
    # exonic_func_ref_gene = input("Enter ExonicFunc.refGene ('stopgain', 'nonsynonymous SNV', 'frameshift insertion', 'frameshift deletion', '.' or comma-separated list, leave blank if not needed): ")

    # if func_ref_gene.strip():
    #     filtered_df = filtered_df[filtered_df['Func.refGene'].isin(func_ref_gene.split(','))]

    # if exonic_func_ref_gene.strip():
    #     filtered_df = filtered_df[filtered_df['ExonicFunc.refGene'].isin(exonic_func_ref_gene.split(','))]

    # print(filtered_df)

def process_data_num():#用sql直接讀取整個表，這個也很慢用不了
    # file_path=os.path.dirname()
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)
    db_path = f"{parent_path}\db.sqlite3"
    with sqlite3.connect(db_path, check_same_thread=False) as db_conn:
        
        db_cursor = db_conn.cursor()
        union_query = "SELECT *, 1 AS patient_number FROM `1_myanno`"
        for i in range(2, 24):
            if i==17 or i==18:
                continue
            else:
                union_query += f"UNION ALL SELECT *, {i} AS patient_number FROM `{i}_myanno`"
        print(union_query)
        db_cursor.execute(union_query)
        table_info = db_cursor.fetchall()
        column_names = [column[0] for column in db_cursor.description]
    column_names=[word.replace('.','_') for word in column_names]
    df = pd.DataFrame(table_info, columns=column_names)
    print(df)

def process_func_data(list):#用sql讀取符合func的資料，有機會用到
    # file_path=os.path.dirname()
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)
    db_path = f"{parent_path}\db.sqlite3"
    with sqlite3.connect(db_path, check_same_thread=False) as db_conn:
        
        db_cursor = db_conn.cursor()
        union_query = "SELECT *, 1 AS patient_number FROM `1_myanno` WHERE  "
        if list != None:
            union_query += "`Func.refGene` = '"+ "' OR `Func.refGene` = '".join(list) +"'"
            
        for i in range(2,3):
            if i == 17 or i == 18:
                continue
            else:
                union_query += f" UNION ALL SELECT *, {i} AS patient_number FROM `{i}_myanno` WHERE"
                if list != None:
                    union_query += "`Func.refGene` = '"+ "' OR `Func.refGene` = '".join(list) +"'"
        print(union_query)
        db_cursor.execute(union_query)
        table_info = db_cursor.fetchall()
        column_names = [column[0] for column in db_cursor.description]
    column_names=[word.replace('.','_') for word in column_names]
    df = pd.DataFrame(table_info, columns=column_names)

  
    print(df)
    return df,column_names

def filter_divide(column_name,symbol,value,data):
    if value != '':
        data[column_name]= data[column_name].apply(pd.to_numeric, errors="coerce")
        if symbol == '<':
            data = data[(data[column_name] < float(value)) | (data[column_name].isna()) | (data[column_name] == '.')]
        elif symbol == '>':
            data = data[(data[column_name] > float(value)) | (data[column_name].isna()) | (data[column_name] == '.')]
    return data

def filter_for_condition(data,ExAC_ALL_symbol,ExAC_ALL_value,CADD_phred_symbol,CADD_phred_value,DANN_score_symbol,DANN_score_value,SIFT_score_symbol,SIFT_score_value,MutationTaster_score_symbol,MutationTaster_score_value):
    filtered_df=filter_divide('ExAC_ALL',ExAC_ALL_symbol,ExAC_ALL_value,data)
    filtered_df=filter_divide('CADD_phred',CADD_phred_symbol,CADD_phred_value,filtered_df)
    filtered_df=filter_divide('DANN_score',DANN_score_symbol,DANN_score_value,filtered_df)
    filtered_df=filter_divide('SIFT_score',SIFT_score_symbol,SIFT_score_value,filtered_df)
    filtered_df=filter_divide('MutationTaster_score',MutationTaster_score_symbol,MutationTaster_score_value,filtered_df)

    return filtered_df



#先用sql找出對應gene_name的值，再用filter分類，做出統計表
def process_data_genename(gene_name,func,ExAC_ALL_select,ExAC_ALL_value,CADD_phred_select,CADD_phred_value,DANN_score_select,DANN_score_value,SIFT_score_select,SIFT_score_value,MutationTaster_score_select,MutationTaster_score_value):
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)
    db_path = f"{parent_path}\db.sqlite3"
    #從資料庫讀取資料，搜尋符合的基因名稱
    with sqlite3.connect(db_path, check_same_thread=False) as db_conn:
        
        db_cursor = db_conn.cursor()
        union_query = f"SELECT *, 'patient_number1' AS patient_number FROM `1_myanno` WHERE  `Gene.refGene` = '{gene_name}'"

            
        for i in range(2,24):
            if i == 17 or i == 18:
                continue
            else:
                union_query += f"UNION ALL SELECT *, 'patient_number{i}' AS patient_number FROM `{i}_myanno` WHERE `Gene.refGene` = '{gene_name}' "
        print(union_query)
        db_cursor.execute(union_query)
        table_info = db_cursor.fetchall()
        column_names = [column[0] for column in db_cursor.description]
    column_names=[word.replace('.','_') for word in column_names]
    df = pd.DataFrame(table_info, columns=column_names)

    #塞選符合條件的資料
    df=df[df['Func_refGene'].isin(func)]
    data=filter_for_condition(df,ExAC_ALL_select,ExAC_ALL_value,CADD_phred_select,
                              CADD_phred_value,DANN_score_select,DANN_score_value,
                              SIFT_score_select,SIFT_score_value,MutationTaster_score_select,MutationTaster_score_value)
    data.to_csv('4.csv')
    # print(data)
    df=data.copy()
    df['combine']=df['Func_refGene']+df['Gene_refGene']
    data_two_signal = df.groupby(['combine', 'patient_number']).size().reset_index(name='count')
    gene_one_signal = df.groupby(['Gene_refGene', 'patient_number']).size().reset_index(name='count')
    data['combine']=data['Chr']+data['Start'].astype(str)+data['End'].astype(str)+data['Ref']+data['Alt']+data['Func_refGene']+data['Gene_refGene']
    data_all_signal = data.groupby(['combine', 'patient_number']).size().reset_index(name='count')


    pivot_df_one = gene_one_signal.pivot_table(index='Gene_refGene', columns='patient_number', values='count', aggfunc='sum')
    pivot_df_two = data_two_signal.pivot_table(index='combine', columns='patient_number', values='count', aggfunc='sum')
    pivot_df_all = data_all_signal.pivot_table(index='combine', columns='patient_number', values='count', aggfunc='sum')
    # print(pivot_df_all)

    # data_one_signal_name=df[['Gene_refGene']].drop_duplicates(subset='Gene_refGene')
    data_two_signal_name=df[['Func_refGene','Gene_refGene','combine']].drop_duplicates(subset='combine')
    # print(data_two_signal_name)
    data_all_signal_name=data[['Chr','Start','End','Ref','Alt','Func_refGene','Gene_refGene','combine']].drop_duplicates(subset='combine')
    data_for_all_sig=pd.merge(left=data_all_signal_name,right=pivot_df_all,on=['combine'],how='right').drop('combine',axis=1)
    data_for_two_sig=pd.merge(left=data_two_signal_name,right=pivot_df_two,on=['combine'],how='right').drop('combine',axis=1)
    data_for_one_sig=pivot_df_one.reset_index()
    data_for_one_sig['count_values'] = data_for_one_sig.iloc[:, 1:].apply(lambda x: x.map(lambda y: not pd.isna(y))).sum(axis=1)
    data_for_two_sig['count_values'] = data_for_two_sig.iloc[:, 2:].apply(lambda x: x.map(lambda y: not pd.isna(y))).sum(axis=1)
    data_for_all_sig['count_values'] = data_for_all_sig.iloc[:, 7:].apply(lambda x: x.map(lambda y: not pd.isna(y))).sum(axis=1)
    column_names_order=[]
    for i in range(1,24):
            if i == 17 or i == 18:
                continue
            else:
                column_names_order.append(f'patient_number{i}')  
    column_names_order_one=['Gene_refGene','count_values']+column_names_order
    column_names_order_two=['Func_refGene','Gene_refGene','count_values']+column_names_order
    column_names_order_all=['Chr','Start','End','Ref','Alt','Func_refGene','Gene_refGene','count_values']+column_names_order



    # 重新排列 DataFrame 的列
    data_for_one_sig = data_for_one_sig.reindex(columns=column_names_order_one).fillna(0)
    data_for_two_sig = data_for_two_sig.reindex(columns=column_names_order_two).fillna(0)
    data_for_all_sig = data_for_all_sig.reindex(columns=column_names_order_all).fillna(0)
    column_names_for_one_sig = data_for_one_sig.columns.tolist()
    column_names_for_two_sig = data_for_two_sig.columns.tolist()
    column_names_for_all_sig = data_for_all_sig.columns.tolist()
    print(data_for_one_sig)
    # data_for_two_sig=pd.merge(left=data_two_signal_name,right=pivot_df_two,on=['combine'],how='right').drop('combine',axis=1).fillna(0)

    # data_for_one_sig.to_csv('1.csv')
    # data_for_two_sig.to_csv('2.csv')
    # data_for_all_sig.to_csv('3.csv')
    return data_for_one_sig,data_for_two_sig,data_for_all_sig,column_names_for_one_sig,column_names_for_two_sig,column_names_for_all_sig


if __name__ == "__main__":
    start_time= time.time()
    # process_func_data(['ncRNA_exonic'])
    column_names_order=[]
    func=['ncRNA_exonic','ncRNA_intronic']
    # print(column_names_order)
    process_data_genename('WASH7P',func,'<','0.5','','','','','','','','')

    # print(df)
    end_time= time.time()
    print(end_time-start_time)