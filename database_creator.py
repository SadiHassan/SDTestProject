# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 17:54:05 2020

@author: mhassan
"""
import pandas as pd
import os
import sqlalchemy as db
import time

def read_this_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df

def db_connect():
    config = {
            'host': 'localhost',
            'port': 3308,
            'user': 'root',
            'password': '12345',
            'database': 'test_db'
            }
    db_user = config.get('user')
    db_pwd = config.get('password')
    db_host = config.get('host')
    db_port = config.get('port')
    db_name = config.get('database')
    
    # specify connection string
    connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
    # connect to database
    engine = db.create_engine(connection_str)
    connection = engine.connect()
    
    return connection, engine
    
def get_all_tables(connection, engine):
    query_result = engine.execute("show tables;");
    df = pd.DataFrame(query_result.fetchall())
    table_list = []
    for index, row in df.iterrows():
        table_list.append(row[0])
    return table_list

def create_table(table_name, df, engine):
    create_table_str = "CREATE TABLE " + table_name + " ( "
    index = 0
    
    for col_name in df.columns:
        create_table_str += col_name + "_ " + "TEXT" #added _ because there is a column named group in gender_age_train which conflicts with "group" keyword of sql
        if index < len(df.columns) - 1:
            create_table_str += ","
        index += 1    
    create_table_str += ");"
    engine.execute(create_table_str)

def insert_data_by_chunk(table_name, df, engine):
    total_rows = len(df.index)
    cur_total = 0;
    insert_str = "INSERT INTO " + table_name + " VALUES ";
    value_str = "("
    chunk_size = 100000
    start_time = time.time();
    
    for index, row in df.iterrows():
        cur_total += 1    
        for i in range(0, len(df.columns)):
            value_str += "\'" + str(row[i]).replace("\'", "") + "\'"
            if i < len(df.columns) - 1:
                value_str += ","
        value_str += ")"    
        if cur_total < chunk_size and index < total_rows - 1:
            value_str += ", ("
        else:
            
            insert_str += value_str
            insert_str += ";"
            #print(insert_str)
            engine.execute(insert_str)
            print("Inserted total ", cur_total, " rows\n")
            cur_total = 0
            value_str = "("
            insert_str = "INSERT INTO " + table_name + " VALUES ";
            print("Time taken: ", time.time() - start_time)
            start_time = time.time()
    if cur_total > 0:
        insert_str += value_str
        insert_str += ";"
        #print(insert_str)
        engine.execute(insert_str)
        print("Finally... Inserted total ", cur_total, " rows")
        print("Time taken: ", time.time() - start_time)
    
    
    
    
def insert_data(table_name, df, engine):
    
    for index, row in df.iterrows():
        value_str = ""
        for i in range(0, len(df.columns)):
            value_str += str(row[i])
            if i < len(df.columns) - 1:
                value_str += ","
        insert_str = "INSERT INTO " + table_name + " VALUES (" + value_str + ");"
        engine.execute(insert_str)
    
def main():
    connection, engine = db_connect()
    table_list = get_all_tables(connection, engine)
    
    folder_name = "china-mobile-user-gemographics"
    #folder_name = "small_data"
    
    for f in os.listdir(folder_name):
        table_name, ext = f.split(".")
        if table_name in table_list:
            engine.execute("drop table " + table_name + ";")
            print("dropped table..." + table_name)
        
        df = pd.read_csv(folder_name + "/" + f)
        print(f, " ------ ")
        print(df.head(5))
        print("creating table: ", table_name)
        create_table(table_name, df, engine)
        print("SUCCESS!")
        print("Inserting data into table: ", table_name)
        #insert_data(table_name, df, engine)
        start_time = time.time()
        insert_data_by_chunk(table_name, df, engine)
        print("Insertion Done for table ==> ", table_name, " ! ")
        print("Time taken: ", (time.time() - start_time), " sec")
        print("-------------------------------------------")
        #break
        
    
    
if __name__ == "__main__":
    main()