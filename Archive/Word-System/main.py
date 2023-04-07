'''
预提供的
youdao-appid: 15f45a64cbf74042
appsecret: iS0Mz8CxDJcgIKkxNdCfMDxITvliKO5e
文件夹根目录下有已做好的相关db，修改文件名或复制副本即可使用

Author>>Word Automatic translation and testing System
Author>>Written by Kid-Ocelot
Author>>Requires Verificated Youdao-app to have best experience
'''

import sqlite3
import sys
import uuid
import requests
import hashlib
import time
from importlib import reload
import json
import time
import random

def connect_db(db_input):
    if db_input == "empty":
        db=sqlite3.connect("Words.db")
        db.execute("CREATE TABLE youdao (appID TEXT,appSECRET TEXT,access INTEGER)")
        db.execute("CREATE TABLE new (CN TEXT,EN TEXT,value INTEGER DEFAULT(0))")
        db.execute("CREATE TABLE prob (CN TEXT,EN TEXT,value INTEGER DEFAULT(0))")
        db.execute("CREATE TABLE fin (CN TEXT,EN TEXT)")
        #db.execute("INSERT INTO youdao (id,appID,appSECRET) values (1,'" + appID + "','" + appSECRET + "')")
        #db.execute("INSERT INTO youdao (id,appID,appSECRET) values (1,'text','text2')")
        db.execute("INSERT into youdao(access) values(0)")
    else:
        db=sqlite3.connect(db_input)
    return db

def db_verification(db):
    #Only Verify Colomns
    errors=0
    try:
        db.execute("SELECT appID,appSECRET,access from youdao")
    except sqlite3.OperationalError:
        print("Veri>>Table youdao error")
        errors=errors+1
    try:
        db.execute("SELECT CN,EN,value from new")
    except sqlite3.OperationalError:
        print("Veri>>Table new error")
        errors=errors+1
    try:
        db.execute("SELECT CN,EN,value from prob")
    except sqlite3.OperationalError:
        print("Veri>>Table prob error")
        errors=errors+1
    try:
        db.execute("SELECT CN,EN from fin")
    except sqlite3.OperationalError:
        print("Veri>>Table fin error")
        errors=errors+1
    print("Veri>>Found",errors,"error(s).")
    if errors>0:
        print("Veri>>",errors,"found,consider creating a new database.",end="\n\n")
    else:
        print("Veri>>Verification passed.",end="\n\n")

def mainChoice():
    print("Main>>Choose operation.")
    print("Main>>1:Configure youdao-id")
    print("Main>>2:Translate a given word")
    print("Main>>3:Words Management")
    print("Main>>4:Words Testment")
    print("Main>>5:Words Migration")
    print("Main>>6")
    print("Main>>7")
    print("Main>>8")
    print("Main>>9:Help")
    print("Main>>10:Close the DB")
    sel=str(input("Main>>Operation id:"))
    return sel

def youdaoGlobalinfoRefresh():
    youdao_appID=db.execute("Select appID from youdao").fetchone()[0]
    youdao_appSECRET=db.execute("Select appSECRET from youdao").fetchone()[0]
    return youdao_appID,youdao_appSECRET

def fetchlist(database,table):#Usage(db,new) Return(Indexs count,Selection)
    list_=database.execute("SELECT * from "+str(table)).fetchall()
    recur=0
    while True:
            try:
                list_[recur]
                recur=recur+1
            except:
                break
    return recur,list_

###################################youdao-request copied from ai.youdao.com (modified)
def youdaoRequest(q,APP_KEY,APP_SECRET,destni_lang="en"):
    import sys
    import uuid
    import requests
    import hashlib
    import time
    from importlib import reload
    import json
    import time

    reload(sys)

    YOUDAO_URL = 'https://openapi.youdao.com/api'
    
    def encrypt(signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()


    def truncate(q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


    def do_request(data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(YOUDAO_URL, data=data, headers=headers)


    def connect(q):
    #    q = "有道智云控制台"

        data = {}
        data['from'] = 'auto'
        data['to'] = destni_lang
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
        sign = encrypt(signStr)
        data['appKey'] = APP_KEY
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign
        data['vocabId'] = "9E47A57AA8B348B789AD6C59B94AFA79"

        response = do_request(data)
        return response.content

    youdao_return=connect(q)
    youdao_return=youdao_return.decode()
    youdao_return=json.loads(youdao_return)
    return youdao_return["translation"][0],youdao_return["errorCode"],youdao_return
#################################################youdao-request########Define part ends
print("""
Author>>Word Automatic translation and testing System
Author>>Written by Kid-Ocelot
Author>>Requires Verificated Youdao-app to have best experience
""")

db_int_sel=str(input("Conn>>1:Connect;2.Create:"))
if db_int_sel=="1":
    db=connect_db(str(input("Name of db:")))
    #db=connect_db("Words.db")#Fast testment,Changing later
else:
    db=connect_db("empty")
    print("Conn>>Created Words.db",end="\n\n")
print("Veri>>Database connected,verificating it.")
db_verification(db)

#During the main Program, Don't forget to db.commit()!

while True:
    youdao_veri=0
    youdao_res_veri1=db.execute("Select appID from youdao").fetchone()[0]
    youdao_res_veri2=db.execute("Select appSECRET from youdao").fetchone()[0]
    if youdao_res_veri1 == None or youdao_res_veri2 == None:
        print("Main>>Appid/Appsecret not found.",end="\n\n")
        youdao_veri=1
    else:
        #Refresh app algorithm
        youdao_appID=youdaoGlobalinfoRefresh()[0]
        youdao_appSECRET=youdaoGlobalinfoRefresh()[1]
        if db.execute("SELECT access from youdao").fetchone()[0]!=1:
            print("Main>>Youdao Info found but not verificated.",end="\n\n")
    sel=mainChoice()
    print()#\n
    if sel=="1":#Youdao id Config
        youdao_sel_main=str(input("Youdao>>1:Input new info.2:Show current info.3.Verificate current info. Choice:"))
        if youdao_sel_main=="1":
            print("Youdao>>Now inputing new info.")
            youdao_res_appID=str(input("Youdao>>appID:"))
            youdao_res_appSECRET=str(input("Youdao>>appSECRET:"))
            if youdao_veri!=1:
                print("Youdao>>Cleared current info.")
                db.execute("Delete from youdao")

            db.execute("Update youdao Set appID='"+youdao_res_appID+"',appSECRET='"+youdao_res_appSECRET+"'")
            #db.execute("Insert into youdao (appID,appSECRET) values ('"+youdao_res_appID+"','"+youdao_res_appSECRET+"')")
            #db.execute("UPDATE youdao SET access=0")
            print("Youdao>>Sucessfully inserted the new info.",end="\n\n")
            db.commit()
        if youdao_sel_main=="2":
            print("Youdao>>Now checking info.")
            if youdao_veri==1:
                print("Youdao>>Infomation missing.")
            youdao_check_appid=db.execute("Select appID from youdao").fetchone()
            youdao_check_appsec=db.execute("Select appSECRET from youdao").fetchone()
            youdao_check_appaccess=db.execute("SELECT access from youdao").fetchone()
            if youdao_check_appaccess[0]==1:
                youdao_check_appaccess="True"
            else:
                youdao_check_appaccess="False"
            print("Youdao>>appID:",youdao_check_appid[0])
            print("Youdao>>appSECRET:",youdao_check_appsec[0])
            print("Youdao>>Accessbility:",youdao_check_appaccess)
            print("Youdao>>Sucessfully shown the current info.",end="\n\n")
        if youdao_sel_main=="3":
            print("Youdao>>Now verificating app accessbility.")
            if youdao_veri==1:
                print("Youdao>>Appid/Appsecret missing.")
            if youdao_veri==0:
                try:
                    youdao_accessbility=youdaoRequest("apple",youdao_appID,youdao_appSECRET,"zh-CHS")#zh-CHS/en
                except:
                    print("Youdao>>Accessbility test not passed.",end="\n\n")
                    youdao_accessbility=("error")
                if youdao_accessbility[1]=="0":
                    print("Youdao>>Accessbility test passed.",end="\n\n")
                    db.execute("UPDATE youdao SET access=1")
                    db.commit()
    if sel=="2":#Translation
        trans_veri_access=db.execute("Select access from youdao").fetchone()[0]
        if trans_veri_access!=1:
            print("Trans>>Please first pass the accessbility check in the Youdao-id>>Verificate")
        else:
            trans_type_sel=str(input("Trans>>Select destination language: 1:English 2:Chinese:"))
            trans_query=str(input("Trans>>Input Beginning String:"))
            if trans_type_sel != "2":
                trans_type_sel="en"
            else:
                trans_type_sel="zh-CHS"
            print("Trans>>",str(youdaoRequest(trans_query,youdao_appID,youdao_appSECRET,trans_type_sel)[0]),end="\n\n")
    if sel=="3":#Manage Words
        mana_sel_main=str(input("Manage>>1:Input New Word 2:View current tables :"))
        if mana_sel_main=="1":
            print("Manage>>Input Method only allows Table new,for further management use SQliteStudio.")
            #mana>>inp>>Selecion matrix

            #Check accessbility
            if db.execute("SELECT access from youdao").fetchone()[0]==1:
                mana_sel_Input_youdao=str(input("Manage>>Input>>Select youdao auto-fill requirement 1:Automatic 2:Manual:"))
            else:
                mana_sel_Input_youdao="2"
            mana_sel_Input_method=str(input("Manage>>Input>>Select Input Method 1:Single 2:Multple(Insert Nothing/ENTER to exit)"))
            #Once AutoYoudao isn't chosen,Input Preference==CN
            #a.k.a "212" & "222" choices can't be chosen
            #Down there "122" "222" can't be chosen
            #Down there "212"&"222" are the same

            if mana_sel_Input_youdao=="1":
                mana_sel_Input_preference=str(input("Manage>>Input>>Select First Insert Character 1:CN 2:EN:"))
            else:
                mana_sel_Input_preference="1"

            mana_char_en=""
            mana_char_cn=""
            mana_count=0
            if mana_sel_Input_method=="1" and mana_sel_Input_preference=="1" and mana_sel_Input_youdao=="1":
                mana_char_cn=str(input("Manage>>Input>>Insert CN character"))
                mana_char_en=str(youdaoRequest(mana_char_cn,youdao_appID,youdao_appSECRET,"en")[0])
                db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en)
            if mana_sel_Input_method=="1" and mana_sel_Input_preference=="1" and mana_sel_Input_youdao=="2": #same as 222
                mana_char_cn=str(input("Manage>>Input>>Insert CN character"))
                mana_char_en=str(input("Manage>>Input>>Insert EN character"))
                db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
            if mana_sel_Input_method=="1" and mana_sel_Input_preference=="2" and mana_sel_Input_youdao=="1":
                mana_char_en=str(input("Manage>>Input>>Insert EN character"))
                mana_char_cn=str(youdaoRequest(mana_char_en,youdao_appID,youdao_appSECRET,"zh-CHS")[0])
                db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
            if mana_sel_Input_method=="1" and mana_sel_Input_preference=="2" and mana_sel_Input_youdao=="2": #same as 212 #Can't be chosen
                mana_char_cn=str(input("Manage>>Input>>Insert CN character"))
                mana_char_en=str(input("Manage>>Input>>Insert EN character"))
                db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
            if mana_sel_Input_method=="2" and mana_sel_Input_preference=="1" and mana_sel_Input_youdao=="1":#cn2en
                mana_count=0
                while True:
                    mana_char_cn=str(input("Manage>>Input>>Insert CN character"))
                    if mana_char_cn=="":
                        print("Manage>>Input>>Exited inputing mode with "+str(mana_count)+" word(s) inserted.",end="\n\n")
                        break
                    else:
                        mana_char_en=str(youdaoRequest(mana_char_cn,youdao_appID,youdao_appSECRET,"en")[0])
                        db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                        print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
                        mana_count=mana_count+1
            if mana_sel_Input_method=="2" and mana_sel_Input_preference=="1" and mana_sel_Input_youdao=="2":#Same as 122
                mana_count=0
                while True:
                    mana_char_cn=str(input("Manage>>Input>>Insert CN character"))
                    mana_char_en=str(input("Manage>>Input>>Insert EN character"))
                    if mana_char_cn=="" or mana_char_en=="":
                        print("Manage>>Input>>Exited inputing mode with "+str(mana_count)+" word(s) inserted.",end="\n\n")
                        break
                    else:
                        db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                        print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
                        mana_count=mana_count+1
            if mana_sel_Input_method=="2" and mana_sel_Input_preference=="2" and mana_sel_Input_youdao=="1":#e
                mana_count=0
                while True:
                    mana_char_en=str(input("Manage>>Input>>Insert EN character"))
                    if mana_char_en=="":
                        print("Manage>>Input>>Exited inputing mode with "+str(mana_count)+" word(s) inserted.",end="\n\n")
                        break
                    else:
                        mana_char_cn=str(youdaoRequest(mana_char_en,youdao_appID,youdao_appSECRET,"zh-CHS")[0])
                        db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                        print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
                        mana_count=mana_count+1
                if mana_sel_Input_method=="2" and mana_sel_Input_preference=="2" and mana_sel_Input_youdao=="2":#Same as 112 Can't be chosen
                    mana_count=0
                    while True:
                        mana_char_cn=str(input("Manage>>Input>>Insert CN character"))
                        mana_char_en=str(input("Manage>>Input>>Insert EN character"))
                        if mana_char_cn=="" or mana_char_en=="":
                            print("Manage>>Input>>Exited inputing mode with "+str(mana_count)+" word(s) inserted.",end="\n\n")
                            break
                        else:
                            db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                            print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
                            mana_count=mana_count+1
            db.commit()
        if mana_sel_main=="2":#View tables
            mana_view_tuple=fetchlist(db,"new")[1]
            mana_recur_int=fetchlist(db,"new")[0]
            print("Manage>>View>>",mana_recur_int,"word(s) found in Table new.")
            for i in range(0,mana_recur_int,1):
                print("Manage>>View>>Table new: CN:",mana_view_tuple[i][0],", EN:",mana_view_tuple[i][1],", Rank:",mana_view_tuple[i][2])
            print()#\n
            
            mana_view_tuple=fetchlist(db,"prob")[1]
            mana_recur_int=fetchlist(db,"prob")[0]
            print("Manage>>View>>",mana_recur_int,"word(s) found in Table prob.")
            for i in range(0,mana_recur_int,1):
                print("Manage>>View>>Table new: CN:",mana_view_tuple[i][0],", EN:",mana_view_tuple[i][1],", Rank:",mana_view_tuple[i][2])
            print()#\n
            
            mana_view_tuple=fetchlist(db,"fin")[1]
            mana_recur_int=fetchlist(db,"fin")[0]
            print("Manage>>View>>",mana_recur_int,"word(s) found in Table fin.")
            for i in range(0,mana_recur_int,1):
                print("Manage>>View>>Table new: CN:",mana_view_tuple[i][0],", EN:",mana_view_tuple[i][1])
            print()#\n
    if sel=="4":#Do tests
        print("Tests>>Entered Testment Mode,Input nothing/ENTER to exit.")
        test_sel_main=str(input("Tests>>Decide lists: 1:Only table New 2:Only Table Prob:"))
        test_success=0#Init
        test_failure=0#Init
        if test_sel_main!="2":#New
            test_count=fetchlist(db,"new")[0]
            if test_count>0:
                while True:
                    test_list=fetchlist(db,"new")[1]
                    test_random_1=int(random.randint(0,test_count-1))
                    test_req=""
                    try:
                        test_req=test_list[test_random_1]
                    except:
                        print("Tests>>An error occurred.",end="\n\n")
                        break
                    test_answer_EN=str(input("Tests>>Translate "+str(test_req[0])+" to English."))
                    if test_answer_EN=="":
                        print("Tests>>Exited with "+str(test_success)+" success(s) and "+str(test_failure)+" failure(s).")
                        break
                    if test_answer_EN==str(test_req[1]):
                        test_success=test_success+1
                        db.execute("UPDATE new SET value="+str(test_req[2]+1)+" WHERE CN='"+test_req[0]+"'")#Success=>+1
                        db.commit()
                        print("Test>>Success.",end="\n\n")
                    else:
                        test_failure=test_failure+1
                        db.execute("UPDATE new SET value="+str(test_req[2]-1)+" WHERE CN='"+test_req[0]+"'")#Fail=>-1
                        db.commit()
                        print("Test>>Failure. The correct answer is "+str(test_req[1])+" .",end="\n\n")
                    db.commit()
            else:
                print("Tests>>Exited for no words in Table new",end="\n\n")

                
        if test_sel_main=="2":#Prob
            test_count=fetchlist(db,"prob")[0]
            if test_count>0:
                while True:
                    test_list=fetchlist(db,"prob")[1]
                    test_random_1=int(random.randint(0,test_count-1))
                    test_req=""
                    try:
                        test_req=test_list[test_random_1]
                    except:
                        print("Tests>>An error occurred.",end="\n\n")
                        break
                    test_answer_EN=str(input("Tests>>Translate "+str(test_req[0])+" to English."))
                    if test_answer_EN=="":
                        print("Tests>>Exited with "+str(test_success)+" success(s) and "+str(test_failure)+" failure(s).")
                        break
                    if test_answer_EN==str(test_req[1]):
                        test_success=test_success+1
                        db.execute("UPDATE prob SET value="+str(test_req[2]+1)+" WHERE CN='"+test_req[0]+"'")#Success=>+1
                        db.commit()
                        print("Test>>Success.",end="\n\n")
                    else:
                        test_failure=test_failure+1
                        db.execute("UPDATE prob SET value="+str(test_req[2]-1)+" WHERE CN='"+test_req[0]+"'")#Fail=>-1
                        db.commit()
                        print("Test>>Failure. The correct answer is "+str(test_req[1])+" .",end="\n\n")
                    db.commit()
            else:
                print("Tests>>Exited for no words in Table prob",end="\n\n")
    if sel=="5":#Migration
        mig_count=0
        mig_list_new=fetchlist(db,"new")
        mig_list_prob=fetchlist(db,"prob")
        mig_list_fin=fetchlist(db,"fin")
        mig_sel=str(input("Mig>>Select 'from'. 1:new>prob 2.new>fin 3:prob>new:"))##Guideline
        if mig_sel=="1":#new>>prob
            #Copied from View
            mig_mana_view_tuple=fetchlist(db,"new")[1]
            mig_mana_recur_int=fetchlist(db,"new")[0]
            print("Mig>>View>>",mig_mana_recur_int,"word(s) found in Table new.")
            for i in range(0,mig_mana_recur_int,1):
                print("Mig>>View>>Table new: CN:",mig_mana_view_tuple[i][0],", EN:",mig_mana_view_tuple[i][1],"Count:",mig_mana_view_tuple[i][2])
            print()#\n
            
            mig_mana_view_tuple=fetchlist(db,"prob")[1]
            mig_mana_recur_int=fetchlist(db,"prob")[0]
            print("Mig>>View>>",mig_mana_recur_int,"word(s) found in Table prob.")
            for i in range(0,mig_mana_recur_int,1):
                print("Mig>>View>>Table prob: CN:",mig_mana_view_tuple[i][0],", EN:",mig_mana_view_tuple[i][1],"Count:",mig_mana_view_tuple[i][2])
            print()#\n
            
            mig_1_sel=int(input("Mig>>Select 'Count' max value. Eg:Select 3 => Any Entries with 'Count' <=3 will be chosen."))
            for i in range(0,mig_list_new[0],1):
                if mig_list_new[1][i][2]<=mig_1_sel:
                    db.execute("DELETE FROM new WHERE en = '"+mig_list_new[1][i][1]+"'")
                    db.execute("INSERT INTO prob (cn,en,value) values ('"+mig_list_new[1][i][0]+"','"+mig_list_new[1][i][1]+"',"+str(mig_list_new[1][i][2])+")")
                    print("Mig>>Migrated ",mig_list_new[1][i])
                    mig_count=mig_count+1
            print("Mig>>Migrated ",mig_count,"word(s).",end="\n\n")

        
        if mig_sel=="2":#new>>fin
            mig_mana_view_tuple=fetchlist(db,"new")[1]
            mig_mana_recur_int=fetchlist(db,"new")[0]
            print("Mig>>View>>",mig_mana_recur_int,"word(s) found in Table new.")
            for i in range(0,mig_mana_recur_int,1):
                print("Mig>>View>>Table new: CN:",mig_mana_view_tuple[i][0],", EN:",mig_mana_view_tuple[i][1],"Count:",mig_mana_view_tuple[i][2])
            print()#\n
            
            mig_mana_view_tuple=fetchlist(db,"fin")[1]
            mig_mana_recur_int=fetchlist(db,"fin")[0]
            print("Mig>>View>>",mig_mana_recur_int,"word(s) found in Table fin.")
            for i in range(0,mig_mana_recur_int,1):
                print("Mig>>View>>Table fin: CN:",mig_mana_view_tuple[i][0],", EN:",mig_mana_view_tuple[i][1])
            print()#\n
            
            mig_2_sel=int(input("Mig>>Select 'Count' min value. Eg:Select 3 => Any Entries with 'Count' >=3 will be chosen."))
            for i in range(0,mig_list_new[0],1):
                if mig_list_new[1][i][2]>=mig_2_sel:
                    db.execute("DELETE FROM new WHERE en = '"+mig_list_new[1][i][1]+"'")
                    db.execute("INSERT INTO fin (cn,en) values ('"+mig_list_new[1][i][0]+"','"+mig_list_new[1][i][1]+"')")
                    print("Mig>>Migrated ",mig_list_new[1][i])
                    mig_count=mig_count+1
            print("Mig>>Migrated ",mig_count,"word(s).",end="\n\n")

        if mig_sel=="3":#prob>>new
            #Copied from View
            mig_mana_view_tuple=fetchlist(db,"prob")[1]
            mig_mana_recur_int=fetchlist(db,"prob")[0]
            print("Mig>>View>>",mig_mana_recur_int,"word(s) found in Table prob.")
            for i in range(0,mig_mana_recur_int,1):
                print("Mig>>View>>Table prob: CN:",mig_mana_view_tuple[i][0],", EN:",mig_mana_view_tuple[i][1],"Count:",mig_mana_view_tuple[i][2])
            print()#\n
            
            mig_mana_view_tuple=fetchlist(db,"new")[1]
            mig_mana_recur_int=fetchlist(db,"new")[0]
            print("Mig>>View>>",mig_mana_recur_int,"word(s) found in Table new.")
            for i in range(0,mig_mana_recur_int,1):
                print("Mig>>View>>Table new: CN:",mig_mana_view_tuple[i][0],", EN:",mig_mana_view_tuple[i][1],"Count:",mig_mana_view_tuple[i][2])
            print()#\n
            
            mig_3_sel=int(input("Mig>>Select 'Count' min value. Eg:Select 3 => Any Entries with 'Count' >=3 will be chosen."))
            for i in range(0,mig_list_prob[0],1):
                if mig_list_prob[1][i][2]>=mig_3_sel:
                    db.execute("DELETE FROM prob WHERE en = '"+mig_list_prob[1][i][1]+"'")
                    db.execute("INSERT INTO new (cn,en,value) values ('"+mig_list_prob[1][i][0]+"','"+mig_list_prob[1][i][1]+"',"+str(mig_list_prob[1][i][2])+")")
                    print("Mig>>Migrated ",mig_list_prob[1][i])
                    mig_count=mig_count+1
            print("Mig>>Migrated ",mig_count,"word(s).",end="\n\n")

    if sel=="9":#Help
        print("Help>>1:关于Youdao-id与翻译")
        print("Help>>2:关于数据库")
        help_sel_main=str(input("Help>>选择捏:"))
        if help_sel_main=="1":
            print("Help>>有道id是去ai.youdao.com进行一个带文本翻译api的app的申请")
            print("Help>>并且将其中的appid与appsecret进行一个Main>>Youdao>>New>>那边的输入")
            print("Help>>然后主界面的Appid/secMissing就会变成Not verified")
            print("Help>>然后再到Main>>Youdao>>3:Verificate>>那边进行一个验证可用性")
            print("Help>>这样之后 Words management>>Add中的有道自动填充就可用了")
            print("Help>>并且同时main>>2的翻译也可用了")
            print("Help>>芜湖芜湖！！",end="\n\n")
        if help_sel_main=="2":
            print("Help>>数据库嘛，有4个表")
            print("Help>>分别是youdao,new,prob,fin")
            print("Help>>youdao表里存了1 entry的appid与appsec")
            print("Help>>new和prob表里存了若干entries的CN,EN,value")
            print("Help>>CN代表了中文解释，EN代表英文词条，value代表在Main>>Test>里的成绩")
            print("Help>>这个value基准为0，text每错一次-1,对一次+1")
            print("Help>>fin表里存了Cn,en")
            print("Help>>为什么没有Value？ 你都背熟了还考什么试")
            print("Help>>通过Main>>Migrate也可以发现 fin表只进不出")
            print("Help>>然后在一开始导入数据库的时候 我在下面def了一个db_verification")
            print("Help>>校验表的列是不是足够 符合标准")
            print("Help>>虽然校验的有点草率 但是至少校验了（（（")
            print("Help>>主要依靠数据库提供的功能就是单词存取，测试与迁移")
            print("Help>>看心情再做一个csv导入？")
            print("Help>>这个不一定做，可能会咕咕（",end="\n\n")
            
    if sel=="10":
        db.commit()
        db.close()
        input("Shut>>Thanks for using! Press ENTER to exit.")
        break
