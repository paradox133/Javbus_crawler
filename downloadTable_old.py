# -*- coding:utf-8 -*-
# import pandas as pd
import sqlite3 
from aria2download import add_download_task, login_aria2,print_download_task
import time
from Notification import send_notification

def mlink_seperate(mlinkstring):
    mlinklist=[]
    mlinklist=mlinkstring.split("\n")
    mlinklist.pop()
    return mlinklist


def mlink_process(mlinklist):
    global body
    mlinkmark=''
    flag1=False # multiple CD
    flag2=False
    flagA=False
    flagB=False
    for i in mlinklist:
        if i.upper().endswith('A'):
            flagA=True
        if i.upper().endswith('B'):
            flagB=True
        flag1=flagA and flagB

    for i in mlinklist:
        if i.upper().endswith('MP4'):
            flag2=True
            mlinkmark=i

    if (not flag1) and flag2:
        return True, mlinkmark
    elif flag1:
        print("need to check mutiple CDs mlink")
        body+='\n'+"need to check mutiple CDs mlink:"+'\n'
        for i in mlinklist:
            body+=i+'\n'
        return False,  'NA'
    else:
        return True, mlinklist[0]


def list_split(test_list):
    odd_i = [] 
    even_i = [] 
    for i in range(0, len(test_list)): 
        if i % 2: #residual is 1: 1,3,5,7,...
            even_i.append(test_list[i]) 
        else :  #residual is 0: 0,2,4,8,...
            odd_i.append(test_list[i]) 
    return odd_i, even_i

def size_format(msizelist):
    temp_list=[]
    for i in range(0, len(msizelist)): 
        s=msizelist[i]
        if s.upper().endswith('GB'):
            temp_list.append(float(s[:len(s)-2]))
        elif s.upper().endswith('MB'):
            temp_list.append(float(s[:len(s)-2])/1024)
        else:
            temp_list.append(0)
    return temp_list



def remove_record(ID,table_name,conn):
    sqlcommand="DELETE FROM "+ table_name +" WHERE 識別碼="+ "'"+ ID+"'"
    #print("sqlcommand is ", sqlcommand)
    cursor = conn.cursor()
    cursor.execute(sqlcommand)
    conn.commit()
    print('record ', ID, ' is removed from Table',table_name)
    return True


def download_previous(DB_Name):
# Create a SQL connection to our SQLite database
    global body
    conn = sqlite3.connect(DB_Name)
    cur = conn.cursor()
    table_name='JAVBUS_DATA'
    aria2=login_aria2()

    # The result of a "cursor.execute" can be iterated over by row
    count=0
    for row in cur.execute('SELECT * FROM '+table_name):
        ID=row[1]
        print(ID,': ')
        mlinkstring=row[10]
        if len(mlinkstring)>0:
            mlinklist=mlink_seperate(mlinkstring)
            mlink=mlink_process(mlinklist)
            if mlink[0]:
                magnet_uri=mlink[1]
                # break
                print(ID, magnet_uri)
                add_download_task(aria2,magnet_uri)
                remove_record(ID,table_name,conn)
                count+=1
                if count>30:
                    time.sleep(3600)
        else:
            body+=ID+': There is no magnet link found under it'+'\n'+'\n'
            print(ID,': There is no magnet link found under it')
        
    # Be sure to close the connection
    conn.close()



body=''
download_previous("TestDB.db")
# main_new()
subject="Download Exceptional Result"
send_notification(subject,body)