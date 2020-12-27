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


def mlink_process_new(mlinklist):
    global body
    temptuple=list_split(mlinklist)
    mlinklist=temptuple[0]
    msizelist_temp=temptuple[1]
    msizelist=size_format(msizelist_temp)
    # print(type(msizelist[0]))
    mlinklist_sorted = [x for y, x in sorted(zip(msizelist,mlinklist))]
    msizelist_sorted=sorted(msizelist,key = float)
    
    # X = ["159", "mp4", "159"]
    # Y = [ 5.72,   5.64,   5.64]
    # Z = [x for y,x in sorted(zip(Y,X))]

    # print(linklist,'and ',sizelist)
    multple_CD_string=''
    mlinkmark=''
    msize_mp4_index=0
    flagA=False
    flagB=False
    flag1=False # multiple CD
    flag2=False # mp4 flag


    for i in mlinklist_sorted:
        if i.upper().endswith('A'):
            flagA=True
            multple_CD_string+=i+','
        if i.upper().endswith('B'):
            flagB=True
            multple_CD_string+=i+','
        flag1=(flagA and flagB)

    for i in mlinklist_sorted:
        if i.upper().endswith('MP4'):
            flag2=True
            msize_mp4_index=mlinklist_sorted.index(i)
            mlinkmark=i

    if (not flag1) and flag2: 

        # mp4 is the largest one, direct get it
        if mlinklist_sorted[-1]==mlinkmark:
            return True, mlinkmark
        else:
            # if not the same, compare the difference between mp4 and the largest one 
            delta=msizelist_sorted[-1]-msizelist_sorted[msize_mp4_index]
            # delta<0.2, then get mp4, else get the largest one
            if delta<=0.2:
                return True, mlinkmark
            else:
                return True, mlinklist_sorted[-1]
    elif (not flag1) and (not flag2): 
        # get the largest one
        return True, mlinklist_sorted[-1]
    # if multiple CD exists, need to check
    else: 
    # flag1 is true: mutiple CDs
        print("need to check mutiple CDs mlink:",multple_CD_string)
        body+='\n'+"need to check mutiple CDs mlink:"+ multple_CD_string+'\n'
        return False,  'NA'


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



def download_new(DB_Name,table_name):
# Create a SQL connection to our SQLite database
    # conn = sqlite3.connect("TestDB.db")
    conn = sqlite3.connect(DB_Name)
    cur = conn.cursor()
    
    aria2=login_aria2()
    global body

    # The result of a "cursor.execute" can be iterated over by row
    count=1
    for row in cur.execute('SELECT * FROM '+table_name):
        ID=row[1]
        print(ID,': ')
        mlinkstring=row[10]
        if len(mlinkstring)>0:
            mlinklist=mlink_seperate(mlinkstring)
            mlink=mlink_process_new(mlinklist)
            # mlink=mlink_process(mlinklist)
            if mlink[0]:
                magnet_uri=mlink[1]
                print(count,':', ID, magnet_uri)
                add_download_task(aria2,magnet_uri)
                remove_record(ID,table_name,conn)
                count+=1
                if count>100:
                    time.sleep(360)
        else:
            body+=ID+': There is no magnet link found under it'+'\n'+'\n'
            print(ID,': There is no magnet link found under it')
        
    # Be sure to close the connection
    conn.close()


# main_previous()
body=''
DB_Name="javbus.sqlite3.db"
# DB_Name="TestDB.db"
table_name='JAVBUS_DATA'
# table_name='JAVBUS_DATA_dummy'


download_new(DB_Name,table_name)
subject="Today Download Exceptional Result"
send_notification(subject,body)