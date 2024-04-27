import pandas as pd
import time
import json 
import os
import re
import sqlite3
# with open ("/home/thomas/Desktop/safetrader/saferTrader/stock_project/config/table_config_monitor.json", 'r')as f:
#     db_info = json.load(f)

# Connect to PostgreSQL server

# def get_sql_data(input,input_func):

#     db_conn = pymysql.connect(host = "localhost",
#                         port= 3306 ,
#                         user = 'leehaohsiang',
#                         passwd = 'mypassword',
#                         db = 'dermatology',
#                         charset='utf8')
#     print("Connect successful!")
#     db_cursor = db_conn.cursor()
#     column_names = None
#     df=pd.DataFrame()
#     for i in range(1,11):
#         table_name=f'`{i}_myanno_hg38_multianno`'
#         columns_name="`Gene.refGene`"
#         query=f"SELECT *,{i} AS patient_number FROM {table_name} WHERE `Gene.refGene` = '{input}' AND `Func.refGene`='{input_func}'"
#         db_cursor.execute(query)
#         if column_names is None:
#             column_names = [column[0] for column in db_cursor.description]
#         table_info = db_cursor.fetchall()
#         df_table_info = pd.DataFrame(table_info)

#         # df_table_info['patient number']=i
#         df=pd.concat([df_table_info,df])

#     # column_names = [column[0] for column in db_cursor.description]
#     db_conn.commit()
#     db_conn.close()
#     print("connect terminated")
#     print(df)

#     return df,column_names
def read_data_csv(func,gene):
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)
    data=pd.read_csv(f'{parent_path}/final1.csv')
    if func != '':
        data=data[(data['Func.refGene'] == func) & (data['Gene.refGene'] == gene)]
    elif func=='':
        data=data[data['Gene.refGene'] == gene]
    data = data.drop(columns=['Unnamed: 0'])
    data = data.rename(columns=lambda x: x.replace('.', '_'))
    columns_name=data.columns.to_list()

    return data,columns_name
def run_alldata(form_number,gene_name,func):
    df=pd.DataFrame()
    # if form_number=='count_values':
    #     for i in range(1,12):
    #         try:
    #            data=pd.read_csv(f'/root/skin/{i}_myanno.hg38_multianno.csv') 
    #            data=data[(data['Func.refGene'] == func) & (data['Gene.refGene'] == gene_name)]
    #            data['patient_number']=i
    #            df=pd.concat([data,df])

    #         except:
    #             continue
    #     data=df
    # elif 'patient' in form_number:
    numbers = re.findall(r'\d+', form_number)
    if numbers:
        result = int(numbers[0])
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)
    db_path = f"{parent_path}\db.sqlite3"
    print(db_path)

    with sqlite3.connect(db_path, check_same_thread=False) as db_conn:
        
        db_cursor = db_conn.cursor()
        union_query = f"SELECT *,{result} AS patient_number FROM `{result}_myanno` WHERE `Gene.refGene` = ? AND `Func.refGene` = ? "
        db_cursor.execute(union_query, (gene_name, func) * 1)
        table_info = db_cursor.fetchall()
        column_names = [column[0] for column in db_cursor.description]
    print(1)
    column_names=[word.replace('.','_') for word in column_names]
    df = pd.DataFrame(table_info, columns=column_names)
    print(df)
    column_to_move = 'patient_number'
    moved_column=df.pop(column_to_move)
    new_position=0
    df.insert(new_position,column_to_move,moved_column)
    columns_name=df.columns.to_list()

    # data=pd.read_csv(f'/root/skin/{result}_myanno.hg38_multianno.csv')
    # data=data[(data['Func.refGene'] == func) & (data['Gene.refGene'] == gene_name)]
    # data['patient_number']=result
    # column_to_move = 'patient_number'
    # moved_column=data.pop(column_to_move)
    # new_position=0
    # data.insert(new_position,column_to_move,moved_column)
    # data = data.rename(columns=lambda x: x.replace('.', '_'))
    # columns_name=data.columns.to_list()
    return df,columns_name
def sql_func_prove(func,gene):

    current_path = os.path.dirname(__file__)
    print(current_path)
    parent_path = os.path.dirname(current_path)
    print(parent_path)
    db_path = f"{parent_path}\db.sqlite3"
    print(db_path)

    # https://nkust.gitbook.io/python/sqlite-liao-cao-zuo-jie
    with sqlite3.connect(db_path, check_same_thread=False) as db_conn:
        
        db_cursor = db_conn.cursor()
        union_query = "SELECT *, 1 AS patient_number FROM `1_myanno` WHERE `Gene.refGene` = ? AND `Func.refGene` = ? "
        for i in range(2, 24):
            if i==17 or i==18:
                continue
            else:
                union_query += f"UNION ALL SELECT *, {i} AS patient_number FROM `{i}_myanno` WHERE `Gene.refGene` = ? AND `Func.refGene`= ?"
        print(union_query)
        db_cursor.execute(union_query, (gene, func) * 21)
        table_info = db_cursor.fetchall()
        column_names = [column[0] for column in db_cursor.description]
    column_names=[word.replace('.','_') for word in column_names]
    df = pd.DataFrame(table_info, columns=column_names)
    column_to_move = 'patient_number'
    moved_column=df.pop(column_to_move)
    new_position=0
    df.insert(new_position,column_to_move,moved_column)
    columns_name=df.columns.to_list()
   
    return df,columns_name

def process_detail_one_sig(form_number,gene_name):
    df=pd.DataFrame()
    numbers = re.findall(r'\d+', form_number)
    if numbers:
        result = int(numbers[0])
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)
    db_path = f"{parent_path}\db.sqlite3"
    print(db_path)

    with sqlite3.connect(db_path, check_same_thread=False) as db_conn:
        
        db_cursor = db_conn.cursor()
        if 'patient' in form_number:
            union_query = f"SELECT *,{result} AS patient_number FROM `{result}_myanno` WHERE `Gene.refGene` = '{gene_name}'"
            print(union_query)
            db_cursor.execute(union_query)
        elif form_number=='count_values':
            union_query = f"SELECT *, 1 AS patient_number FROM `1_myanno` WHERE `Gene.refGene` = '{gene_name}'"
            for i in range(2, 24):
                if i==17 or i==18:
                    continue
                else:
                    union_query += f"UNION ALL SELECT *, {i} AS patient_number FROM `{i}_myanno` WHERE `Gene.refGene` = '{gene_name}'"
            print(union_query)
            db_cursor.execute(union_query)
        
        table_info = db_cursor.fetchall()
        column_names = [column[0] for column in db_cursor.description]
    print(1)
    column_names=[word.replace('.','_') for word in column_names]
    df = pd.DataFrame(table_info, columns=column_names)
    
    column_to_move = 'patient_number'
    moved_column=df.pop(column_to_move)
    new_position=0
    df.insert(new_position,column_to_move,moved_column)
    columns_name=df.columns.to_list()

    return df,columns_name


if __name__=='__main__':
    start_time= time.time()
    input='A1BG'
    func='ncRNA_exonic'
    gene='DDX11L1'
    # df,col=sql_func_prove(func,gene)
    df,col=read_data_csv(func,gene)
    # df,col=run_alldata('patient_1',gene,func)
    df,col=process_detail_one_sig('patient_1',gene)
    print(df)
    # df =get_sql_data(input)
    # df.to_csv('output.csv')
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"執行時間：{execution_time} 秒")
