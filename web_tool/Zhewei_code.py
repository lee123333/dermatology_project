import csv
import sqlite3
from django.http import JsonResponse
import os
import pandas as pd

def search_and_process_data():
    input_data_1 = input("Enter input_data_1: ")
    input_data_2 = input("Enter input_data_2: ")
    result_data = []

    # 使用相對路徑
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)
    db_path = f"{parent_path}\db.sqlite3"
    
    with sqlite3.connect(db_path, check_same_thread=False) as db_conn:
        
        db_cursor = db_conn.cursor()
        union_query = "SELECT *, 1 AS patient_number FROM `1_myanno` WHERE `Gene.refGene` = ? AND `Func.refGene` = ? "
        for i in range(2, 24):
            if i==17 or i==18:
                continue
            else:
                union_query += f"UNION ALL SELECT *, {i} AS patient_number FROM `{i}_myanno` WHERE `Gene.refGene` = ? AND `Func.refGene`= ?"

        db_cursor.execute(union_query, (input_data_2, input_data_1) * 21)
        table_info = db_cursor.fetchall()
        column_names = [column[0] for column in db_cursor.description]
    column_names=[word.replace('.','_') for word in column_names]
    df = pd.DataFrame(table_info, columns=column_names)
    print(df)

    numeric_cols = ["ExAC_ALL", "CADD_phred", "DANN_score", "SIFT_score", "MutationTaster_score"]
    thresholds = {}  # 用於存儲用戶輸入的閥值
    for col in numeric_cols:
        threshold = input(f"Enter threshold for {col} (leave blank if not needed): ")
        if threshold.strip():  # 如果輸入不是空白，則轉換為浮點數
            thresholds[col] = float(threshold)

    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    filtered_df = df
  

    if "ExAC_ALL" in thresholds:
        filtered_df = filtered_df[(filtered_df['ExAC_ALL'] < thresholds["ExAC_ALL"]) |
                                   (filtered_df['ExAC_ALL'].isna()) |
                                   (filtered_df['ExAC_ALL'] == ".")]

    if "CADD_phred" in thresholds:
        filtered_df = filtered_df[(filtered_df['CADD_phred'] > thresholds["CADD_phred"]) |
                                   (filtered_df['CADD_phred'].isna()) |
                                   (filtered_df['CADD_phred'] == ".")]

    if "DANN_score" in thresholds:
        filtered_df = filtered_df[(filtered_df['DANN_score'] > thresholds["DANN_score"]) |
                                   (filtered_df['DANN_score'].isna()) |
                                   (filtered_df['DANN_score'] == ".")]

    if "SIFT_score" in thresholds:
        filtered_df = filtered_df[(filtered_df['SIFT_score'] > thresholds["SIFT_score"]) |
                                   (filtered_df['SIFT_score'].isna()) |
                                   (filtered_df['SIFT_score'] == ".")]

    if "MutationTaster_score" in thresholds:
        filtered_df = filtered_df[(filtered_df['MutationTaster_score'] > thresholds["MutationTaster_score"]) |
                                   (filtered_df['MutationTaster_score'].isna()) |
                                   (filtered_df['MutationTaster_score'] == ".")]
    print(filtered_df)
    # 加入 Func.refGene 和 ExonicFunc.refGene 的篩選
    func_ref_gene = input("Enter Func.refGene ('exonic', 'splicing' or comma-separated list, leave blank if not needed): ")
    exonic_func_ref_gene = input("Enter ExonicFunc.refGene ('stopgain', 'nonsynonymous SNV', 'frameshift insertion', 'frameshift deletion', '.' or comma-separated list, leave blank if not needed): ")

    if func_ref_gene.strip():
        filtered_df = filtered_df[filtered_df['Func_refGene'].isin(func_ref_gene.split(','))]

    if exonic_func_ref_gene.strip():
        filtered_df = filtered_df[filtered_df['ExonicFunc_refGene'].isin(exonic_func_ref_gene.split(','))]

    print(filtered_df)

if __name__ == "__main__":
    search_and_process_data()