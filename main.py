from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
#import cv2
#import numpy as np
import os
import time
import shutil
import hashlib
#import imagehash
#import PIL.Image
#from PIL import Image
#from PIL import ImageTk
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="product_bc"

)

#from store import *


app = Flask(__name__)
app.secret_key = 'abcdef'


@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""
    act=""
    show=""
    ms1=""
    ms2=""
    ms3=""
    data2=[]
    data3=[]
    mdata=[]
    sdata=[]
    rdata=[]
    pdata=[]
    scnt=0
    company=""
    supplier=""
    shop=""
    sact=""
    pid=0
    pcode=""
    if request.method=='POST':
        pcode=request.form['pcode']
        show="yes"

        #pp=pcode.split("P")
        #pcode2=pp[0]
        
        cursor = mydb.cursor()

        cursor.execute("SELECT count(*) FROM pr_productcode where product_code=%s",(pcode, ))
        cnt = cursor.fetchone()[0]
        if cnt>0:
            act="1"
            cursor.execute("SELECT * FROM pr_productcode where product_code=%s",(pcode, ))
            dd = cursor.fetchone()
            pid=dd[1]
            company=dd[2]
            suplier=dd[5]
            shop=dd[6]
            cursor.execute('SELECT * FROM pr_blockchain where block_id=%s && ptype=%s',(pid, 'PID'))
            data2 = cursor.fetchall()

            ####Find Manufacture###
            #code=int(pp[1])
            ms1="1"
            cursor.execute("SELECT * FROM pr_manufacture where uname=%s",(company, ))
            mdata = cursor.fetchone()

            cursor.execute("SELECT * FROM pr_product where id=%s",(pid, ))
            pdata = cursor.fetchone()

            ####Find Distributor###
            
            if supplier=="":
                ms2="2"
                print("none")
            else:
                ms2="1"
                

                cursor.execute("SELECT * FROM pr_supplier where uname=%s",(supplier, ))
                sdata = cursor.fetchone()
            
                
            ####Find Retailer###
            if shop=="":
                ms3="2"
                print("none")
            else:
                ms3="1"
                

                cursor.execute("SELECT * FROM pr_shop where uname=%s",(shop, ))
                rdata = cursor.fetchone()
            
            ####SOLD##
            cursor.execute("SELECT count(*) FROM pr_sale where pcode=%s",(pcode, ))
            scnt = cursor.fetchone()[0]
            if scnt>0:
                sact="1"
            else:
                sact=""
            ######


            
        else:
            act="2"





        
        '''cursor.execute("SELECT count(*) FROM pr_product where pcode=%s",(pcode2, ))
        cnt = cursor.fetchone()[0]
        if cnt>0:
            act="1"
            cursor.execute("SELECT * FROM pr_product where pcode=%s",(pcode2, ))
            dd = cursor.fetchone()
            pid=dd[0]
            company=dd[3]
            cursor.execute('SELECT * FROM pr_blockchain where block_id=%s && ptype=%s',(pid, 'PID'))
            data2 = cursor.fetchall()
            #for ss in data:
            #    ss1=ss[4].split(",")
            #    data1.append()
            cursor.execute("SELECT * FROM pr_shop")
            data3 = cursor.fetchall()
            ####Find Manufacture###
            code=int(pp[1])
            ms1="1"
            cursor.execute("SELECT * FROM pr_manufacture where uname=%s",(company, ))
            mdata = cursor.fetchone()

            cursor.execute("SELECT * FROM pr_product where id=%s",(pid, ))
            pdata = cursor.fetchone()
            
            ####Find Distributor###
            cursor.execute("SELECT count(*) FROM pr_send where pid=%s && prd1<=%s && prd2>=%s",(pid, code,code))
            dss1 = cursor.fetchone()[0]
            if dss1>0:
                ms2="1"
                cursor.execute("SELECT * FROM pr_send where pid=%s && prd1<=%s && prd2>=%s",(pid, code,code))
                dss2 = cursor.fetchone()
                supplier=dss2[8]

                cursor.execute("SELECT * FROM pr_supplier where uname=%s",(supplier, ))
                sdata = cursor.fetchone()
            else:
                ms2="2"
                print("none")
            ####Find Retailer###
            cursor.execute("SELECT count(*) FROM pr_send2 where pid=%s && prd1<=%s && prd2>=%s",(pid, code,code))
            dss2 = cursor.fetchone()[0]
            if dss2>0:
                ms3="1"
                cursor.execute("SELECT * FROM pr_send2 where pid=%s && prd1<=%s && prd2>=%s",(pid, code,code))
                dss2 = cursor.fetchone()
                shop=dss2[12]

                cursor.execute("SELECT * FROM pr_shop where uname=%s",(shop, ))
                rdata = cursor.fetchone()
            else:
                ms3="2"
                print("none")
            ####SOLD##
            cursor.execute("SELECT count(*) FROM pr_sale where pcode=%s",(pcode, ))
            scnt = cursor.fetchone()[0]
            if scnt>0:
                sact="1"
            else:
                sact=""
            ######
            
        
        else:
            act="2"'''
        
        
    return render_template('index.html',ms1=ms1,ms2=ms2,ms3=ms3,act=act,msg=msg,show=show,data2=data2,data3=data3,sact=sact,mdata=mdata,sdata=sdata,rdata=rdata,pdata=pdata,pcode=pcode)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    act = request.args.get('act')
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM pr_manufacture WHERE uname = %s AND pass = %s AND status=1', (uname, pwd))
        account = cursor.fetchone()
        if account:
            ff1=open("log.txt","w")
            ff1.write(uname)
            ff1.close()
            session['username'] = uname
            return redirect(url_for('product'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password! or Not Approved'
            return redirect(url_for('mess'))
        
        
    return render_template('index.html',msg=msg,act=act)

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    msg=""
    act = request.args.get('act')
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM pr_admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            ff1=open("log.txt","w")
            ff1.write(uname)
            ff1.close()
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
        
        
    return render_template('index.html',msg=msg,act=act)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    act = request.args.get('act')

    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM pr_manufacture')
    data = cursor.fetchall()

    if act=="ok":
        mid = request.args.get('mid')
        cursor.execute('update pr_manufacture set status=1 where id=%s',(mid,))
        mydb.commit()
        return redirect(url_for('admin'))
       

    return render_template('admin.html',msg=msg,act=act,data=data)

@app.route('/index_dist', methods=['GET', 'POST'])
def index_dist():
    msg=""
    act = request.args.get('act')
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM pr_supplier WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            ff1=open("log2.txt","w")
            ff1.write(uname)
            ff1.close()
            session['username'] = uname
            return redirect(url_for('dist_home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('index_dist.html',msg=msg,act=act)

@app.route('/index_shop', methods=['GET', 'POST'])
def index_shop():
    msg=""
    act = request.args.get('act')
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM pr_shop WHERE uname = %s AND pass = %s AND status=1', (uname, pwd))
        account = cursor.fetchone()
        if account:
            ff1=open("log3.txt","w")
            ff1.write(uname)
            ff1.close()
            session['username'] = uname
            return redirect(url_for('shop_home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('index_shop.html',msg=msg,act=act)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    msg=""
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM pr_manufacture")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO pr_manufacture(id,name,mobile,email,address,uname,pass) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,name,mobile,email,address,uname,pass1)
        mycursor.execute(sql, val)
        mydb.commit()            
        print(mycursor.rowcount, "Added Success")
        ##BC##
        sdata="MID:"+str(maxid)+", Company:"+name+", Mobile:"+mobile+",Location:"+address+", RegDate:"+rdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=maxid1-1
            mycursor1.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
            pp = mycursor1.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
        val2 = (maxid1,maxid,pkey,key,sdata,'MID')
        mycursor1.execute(sql2, val2)
        mydb.commit()   
        ####
        return redirect(url_for('message'))
       
    
    return render_template('index.html')


@app.route('/complaint', methods=['GET', 'POST'])
def complaint():
    msg=""
    act = request.args.get('act')
    pcode = request.args.get('pcode')

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM pr_productcode where product_code=%s",(pcode,))
    pdd = mycursor.fetchone()
    company=pdd[2]
    pid=pdd[1]

    mycursor.execute("SELECT * FROM pr_product where id=%s",(pid,))
    pdd1 = mycursor.fetchone()
    product=pdd1[2]
        
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        message=request.form['message']
      

        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM pr_complaint")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO pr_complaint(id,company,pid,pcode,name,email,message,rdate,product) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)"
        val = (maxid,company,pid,pcode,name,email,message,rdate,product)
        mycursor.execute(sql, val)
        mydb.commit()            
        return redirect(url_for('complaint',pcode=pcode,act='1'))

    return render_template('complaint.html',act=act,pcode=pcode)


@app.route('/message', methods=['GET', 'POST'])
def message():
    
    return render_template('message.html')

@app.route('/mess', methods=['GET', 'POST'])
def mess():
    
    return render_template('mess.html')

@app.route('/code1', methods=['GET', 'POST'])
def code1():
    pid = request.args.get('pid')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM pr_productcode where pid=%s",(pid,))
    data = mycursor.fetchall()

        
    return render_template('code1.html',data=data)


@app.route('/code2', methods=['GET', 'POST'])
def code2():
    pid = request.args.get('pid')
    k1 = request.args.get('k1')
    k2 = request.args.get('k2')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM pr_productcode where pid=%s && pcount between %s and %s",(pid,k1,k2))
    data = mycursor.fetchall()

        
    return render_template('code2.html',data=data)

@app.route('/view_comp', methods=['GET', 'POST'])
def view_comp():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    print(uname)
    cursor = mydb.cursor()
    ff1=open("log.txt","r")
    company=ff1.read()
    ff1.close()

    
    
    cursor.execute('SELECT * FROM pr_complaint where company=%s order by id desc',(company, ))
    data = cursor.fetchall()

    return render_template('view_comp.html',data=data)


@app.route('/product', methods=['GET', 'POST'])
def product():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    print(uname)
    cursor = mydb.cursor()
    ff1=open("log.txt","r")
    company=ff1.read()
    ff1.close()

    cursor.execute('SELECT count(*) FROM pr_product where company=%s',(company, ))
    cnpr = cursor.fetchone()[0]
    
    cursor.execute('SELECT * FROM pr_product where company=%s order by id desc',(company, ))
    data = cursor.fetchall()
    
    cursor.execute('SELECT * FROM pr_category')
    catt = cursor.fetchall()
    if request.method=='POST':
        cat=request.form['category']
        prd=request.form['product']
        price=request.form['price']
        description=request.form['description']
        location=request.form['location']
        mdate=request.form['mdate']
        num_piece=request.form['num_piece']

        num_start="1"
        plen=len(num_piece)
        numStr1 = num_start.zfill(plen)
        numStr2 = num_piece.zfill(plen)
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM pr_product")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        numStr = str(maxid)
        numStr = numStr.zfill(4)
        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        my=now.strftime("%y%m")

        xn=randint(1000, 9999)
        pcode="K"+numStr
        code1=pcode+"P"+numStr1
        code2=pcode+"P"+numStr2

        i=1
        nmm=int(num_piece)
        while i<=nmm:
            
            mycursor.execute("SELECT max(id)+1 FROM pr_productcode")
            maxid2 = mycursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1

            xn1=randint(100, 999)
            xn2=randint(1, 9)
            kycode="K"+str(xn2)+str(maxid)+"0"+str(maxid2)+str(xn1)
            
            sql = "INSERT INTO pr_productcode(id,pid,company,product_code,pcount) VALUES (%s, %s, %s, %s,%s)"
            val = (maxid2,maxid,company,kycode,i)
            cursor.execute(sql, val)
            mydb.commit()     
            
            i+=1
        

        
        sql = "INSERT INTO pr_product(id,category,product,company,price,description,location,mdate,pcode,rdate,num_piece,code1,code2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,cat,prd,company,price,description,location,mdate,pcode,rdate,num_piece,code1,code2)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Added Success")
        result="sucess"
        ##BC##
        sdata="PID:"+str(maxid)+", Product:"+prd+", Company:"+company+", Manufacture:"+mdate+",KYP Code:"+code1+" to "+code2+", RegDate:"+rdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=maxid1-1
            cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
            pp = cursor.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
        val2 = (maxid1,maxid,pkey,key,sdata,'PID')
        cursor.execute(sql2, val2)
        mydb.commit()   
        ####
        
        if cursor.rowcount==1:
            msg="success"
            return redirect(url_for('product',msg=msg))
        else:
            msg="fail"
            return redirect(url_for('product',msg=msg))
            #msg='Already Exist'

    
    return render_template('product.html',catt=catt,data=data,cnpr=cnpr)


@app.route('/dist', methods=['GET', 'POST'])
def dist():
    msg=""
    owner=""
    if 'username' in session:
        owner = session['username']
    ff1=open("log.txt","r")
    company=ff1.read()
    ff1.close()
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_supplier where owner=%s order by id desc',(company, ))
    data = cursor.fetchall()

    cursor.execute('SELECT * FROM pr_send where company=%s',(company,))
    data2 = cursor.fetchall()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        name2=request.form['name2']
        gst_number=request.form['gst_number']
        

        cursor.execute('SELECT * FROM pr_supplier')
        result = cursor.fetchall()
        j=0
        for i in result:
            print(i[0])
            j+=1
        id2=j+1

        
        cursor.execute("SELECT max(id)+1 FROM pr_supplier")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid=1
        #rd=str(rdate).split("-")
        #rdd=rd[2]+"-"+rd[1]+"-"+rd[0]
        sql = "INSERT INTO pr_supplier(id,owner,name,mobile,email,city,uname,pass,rdate,name2,gst_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,company,name,mobile,email,city,uname,pass1,rdate,name2,gst_number)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        ##BC##
        sdata="DID:"+str(maxid)+", Distributor:"+name+", Company:"+company+", Mobile:"+mobile+", City:"+city+", RegDate:"+rdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=maxid1-1
            cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
            pp = cursor.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
        val2 = (maxid1,maxid,pkey,key,sdata,'DID')
        cursor.execute(sql2, val2)
        mydb.commit()   
        ####
        link="http://localhost:5000/index_dist"
        message="Dear "+name+", Distributed Account created, Username:"+uname+", Password"+pass1+", Link:"+link
        url="http://iotcloud.co.in/testmail/sendmail.php?email="+email+"&message="+message
        webbrowser.open_new(url)
            
        if cursor.rowcount==1:
            return redirect(url_for('dist',act='1'))
        else:
            return redirect(url_for('dist',act='2'))
            #msg='Already Exist' 
    return render_template('dist.html',msg=msg,data=data,data2=data2)




@app.route('/view_prd', methods=['GET', 'POST'])
def view_prd():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']
    print(uname)
    ff1=open("log.txt","r")
    company=ff1.read()
    ff1.close()
    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where owner=%s',(company, ))
    catt = cursor.fetchall()
    # where status=0
    cursor.execute('SELECT * FROM pr_product where company=%s',(company, ))
    data = cursor.fetchall()

    '''if request.method=='POST':
        prd_from=request.form['prd_from']
        prd_to=request.form['prd_to']
        supplier=request.form['supplier']
        p1=int(prd_from)
        p2=int(prd_to)
        #cursor.execute("SELECT count(*) FROM pr_product where id=%s && status=0",(prd_from, ))
        #cnt = cursor.fetchone()[0]
        #cursor.execute("SELECT count(*) FROM pr_product where id=%s && status=0",(prd_to, ))
        #cnt2 = cursor.fetchone()[0]
        if cnt>0 and cnt2>0 and p1<=p2:
            i=p1

            
            cursor.execute("SELECT max(id)+1 FROM pr_send")
            maxid2 = cursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1
            sql3 = "INSERT INTO pr_send(id,prd_from,prd_to,supplier,rdate) VALUES (%s, %s, %s, %s, %s)"
            val3 = (maxid2,prd_from,prd_to,supplier,rdate)
            cursor.execute(sql3, val3)
                
                    
            while i<=p2:
                cursor.execute('update pr_product set supplier=%s,status=1 WHERE id = %s', (supplier, i))
                mydb.commit()
                ##BC##
                sdata="PID:"+str(i)+", Distribute to:"+supplier+", RegDate:"+rdate
                result = hashlib.md5(sdata.encode())
                key=result.hexdigest()

                mycursor1 = mydb.cursor()
                mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
                maxid1 = mycursor1.fetchone()[0]
                if maxid1 is None:
                    maxid1=1
                    pkey="00000000000000000000000000000000"
                else:
                    mid=maxid1-1
                    cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
                    pp = cursor.fetchone()
                    pkey=pp[3]
                sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
                val2 = (maxid1,i,pkey,key,sdata,'PID')
                cursor.execute(sql2, val2)
                mydb.commit()   
                ####
                i+=1
            act="1"
            msg="Distributed Success"
            return redirect(url_for('view_prd'))
            
        else:
            act="2"
            msg="Product ID not available!"'''

    return render_template('view_prd.html',data=data,catt=catt,act=act,msg=msg)

@app.route('/prd_send', methods=['GET', 'POST'])
def prd_send():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']
    print(uname)
    ff1=open("log.txt","r")
    company=ff1.read()
    ff1.close()

    pid = request.args.get('pid')
    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where owner=%s',(company, ))
    catt = cursor.fetchall()
    # where status=0
    cursor.execute('SELECT * FROM pr_product where id=%s',(pid, ))
    dd1 = cursor.fetchone()
    tot=dd1[21]
    pcode=dd1[9]
    tot1=str(tot)

    if request.method=='POST':
        num_prd=request.form['num_prd']
        supp=request.form['supplier']
        pid=request.form['pid']

        num=int(num_prd)
        cursor.execute('SELECT sum(num_prd) FROM pr_send where pid=%s',(pid, ))
        sn1 = cursor.fetchone()[0]
        if sn1 is None:
            sn1=0
        bal=tot-sn1

        
        
        
        if bal>=num:

            num_start=sn1+1
            num_end=sn1+num
            num_s=str(num_start)
            num_e=str(num_end)
            plen=len(tot1)
            numStr1 = num_s.zfill(plen)
            numStr2 = num_e.zfill(plen)
            code1=pcode+"P"+numStr1
            code2=pcode+"P"+numStr2

            balance=tot-num_end
            
            cursor.execute("SELECT max(id)+1 FROM pr_send")
            maxid2 = cursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1
            sql3 = "INSERT INTO pr_send(id,pid,num_prd,prd_from,prd_to,prd1,prd2,company,supplier,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val3 = (maxid2,pid,num_prd,code1,code2,num_start,num_end,company,supp,rdate)
            cursor.execute(sql3, val3)
            mydb.commit()
                    
            
            cursor.execute('update pr_product set distribute=%s,balance=%s WHERE id = %s', (num_end,balance, pid))
            mydb.commit()

            cursor.execute('update pr_productcode set supplier=%s WHERE pid = %s && pcount between %s and %s', (supp, pid, num_start, num_end))
            mydb.commit()
            ##BC##
            sdata="PID:"+pid+", Distribute to:"+supp+", Company:"+company+", Pcode:"+num_s+" to "+num_e+", RegDate:"+rdate
            result = hashlib.md5(sdata.encode())
            key=result.hexdigest()

            mycursor1 = mydb.cursor()
            mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
            maxid1 = mycursor1.fetchone()[0]
            if maxid1 is None:
                maxid1=1
                pkey="00000000000000000000000000000000"
            else:
                mid=maxid1-1
                cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
                pp = cursor.fetchone()
                pkey=pp[3]
            sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
            val2 = (maxid1,pid,pkey,key,sdata,'PID')
            cursor.execute(sql2, val2)
            mydb.commit()   
            ####
                
            act="1"
            msg="Distributed Success"
            return redirect(url_for('view_prd'))
            
        else:
            act="2"
            msg="Product not available!"

    return render_template('prd_send.html',catt=catt,act=act,msg=msg,pid=pid)

@app.route('/view_req', methods=['GET', 'POST'])
def view_req():
    ff1=open("log.txt","r")
    company=ff1.read()
    ff1.close()
    data=[]
    
    cursor = mydb.cursor()

    #cursor.execute('SELECT * FROM pr_supplier where owner=%s',(company, ))
    #dd1 = cursor.fetchone()
    #company=dd1[1]

    cursor.execute('SELECT * FROM pr_request where company=%s',(company, ))
    data1 = cursor.fetchall()
    for ss in data1:
        data3=[]
        cursor.execute('SELECT * FROM pr_product where id=%s',(ss[1], ))
        dd2 = cursor.fetchone()
        data3.append(ss[1])
        data3.append(dd2[2])
        data3.append(dd2[5])
        data3.append(ss[2])
        data3.append(ss[3])
        data.append(data3)

    return render_template('view_req.html',data=data)

@app.route('/dist_home', methods=['GET', 'POST'])
def dist_home():
    msg=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where distributor=%s',(supplier, ))
    data = cursor.fetchall()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    data1 = cursor.fetchone()
    company=data1[1]

    #cursor.execute('SELECT * FROM pr_send')
    #data2 = cursor.fetchall()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        name2=request.form['name2']
        

        
        cursor.execute("SELECT max(id)+1 FROM pr_shop")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO pr_shop(id,owner,distributor,name,mobile,email,city,uname,pass,name2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,company,supplier,name,mobile,email,city,uname,pass1,name2)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        ##BC##
        sdata="RID:"+str(maxid)+", Retailer:"+name+", Distributor:"+supplier+", Company:"+company+", City:"+city+", RegDate:"+rdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=maxid1-1
            cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
            pp = cursor.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
        val2 = (maxid1,maxid,pkey,key,sdata,'RID')
        cursor.execute(sql2, val2)
        mydb.commit()   
        ####
        link="http://localhost:5000/index_shop"
        message="Dear "+name+", Retailer Account created, Username:"+uname+", Password"+pass1+", Link:"+link
        url="http://iotcloud.co.in/testmail/sendmail.php?email="+email+"&message="+message
        webbrowser.open_new(url)
            
        if cursor.rowcount==1:
            return redirect(url_for('dist_home',act='1'))
        else:
            return redirect(url_for('dist_home',act='2'))
            #msg='Already Exist' 
    return render_template('dist_home.html',msg=msg,data=data,data1=data1)


@app.route('/shop_req', methods=['GET', 'POST'])
def shop_req():
    msg=""
    act=""
    sid=""
    supplier=""
    if 'username' in session:
        supplier = session['username']

    ff1=open("log.txt","r")
    company=ff1.read()
    ff1.close()
    cursor = mydb.cursor()

    ###Retailer approval
    cursor.execute('SELECT * FROM pr_shop where owner=%s', (company, ))
    data = cursor.fetchall()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    data1 = cursor.fetchone()

    if request.method=='GET':
        sid = request.args.get('sid')
        if sid is None:
            print("sid")
        else:
            cursor.execute('update pr_shop set status=1 WHERE id = %s', (sid, ))
            mydb.commit()
            return redirect(url_for('shop_req',act='1'))

    return render_template('shop_req.html',msg=msg,data=data,data1=data1,act=act)

@app.route('/dist_prd', methods=['GET', 'POST'])
def dist_prd():
    msg=""
    act=""
    #uname=""
    #if 'username' in session:
    #    uname = session['username']
    #print(uname)
    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    dd1 = cursor.fetchone()
    company=dd1[1]

    cursor.execute('SELECT * FROM pr_shop where status=1')
    catt = cursor.fetchall()
    
    cursor.execute('SELECT * FROM pr_product where company=%s',(company, ))
    data = cursor.fetchall()

    if request.method=='POST':
        prd_from=request.form['prd_from']
        prd_to=request.form['prd_to']
        shop=request.form['shop']
        p1=int(prd_from)
        p2=int(prd_to)
        cursor.execute("SELECT count(*) FROM pr_product where id=%s && supplier=%s && status=1",(prd_from, uname ))
        cnt = cursor.fetchone()[0]
        cursor.execute("SELECT count(*) FROM pr_product where id=%s && supplier=%s && status=1",(prd_to, uname))
        cnt2 = cursor.fetchone()[0]
        if cnt>0 and cnt2>0 and p1<=p2:
            i=p1

            
            cursor.execute("SELECT max(id)+1 FROM pr_send2")
            maxid2 = cursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1
            sql3 = "INSERT INTO pr_send(id,prd_from,prd_to,supplier,shop,rdate) VALUES (%s, %s, %s, %s, %s, %s)"
            val3 = (maxid2,prd_from,prd_to,uname,shop,rdate)
            cursor.execute(sql3, val3)
                
                    
            while i<=p2:
                cursor.execute('update pr_product set shop=%s,status=1 WHERE id = %s', (shop, i))
                mydb.commit()
                ##BC##
                sdata="PID:"+str(i)+", Retailer:"+shop+", RegDate:"+rdate
                result = hashlib.md5(sdata.encode())
                key=result.hexdigest()

                mycursor1 = mydb.cursor()
                mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
                maxid1 = mycursor1.fetchone()[0]
                if maxid1 is None:
                    maxid1=1
                    pkey="00000000000000000000000000000000"
                else:
                    mid=maxid1-1
                    cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
                    pp = cursor.fetchone()
                    pkey=pp[3]
                sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
                val2 = (maxid1,i,pkey,key,sdata,'PID')
                cursor.execute(sql2, val2)
                mydb.commit()   
                ####
                i+=1
            act="1"
            msg="Distributed Success"
            return redirect(url_for('view_prd'))
            
        else:
            act="2"
            msg="Product ID not available!"

    return render_template('dist_prd.html',data=data,catt=catt,act=act,msg=msg)

@app.route('/dist_send', methods=['GET', 'POST'])
def dist_send():
    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    dd1 = cursor.fetchone()
    company=dd1[1]
    
    pid = request.args.get('pid')
    if request.method=='POST':
        num_prd=request.form['num_prd']
        pid=request.form['pid']

        cursor.execute("SELECT max(id)+1 FROM pr_request")
        maxid2 = cursor.fetchone()[0]
        if maxid2 is None:
            maxid2=1
        sql3 = "INSERT INTO pr_request(id,pid,num_prd,supplier,company,rdate) VALUES (%s, %s, %s, %s, %s, %s)"
        val3 = (maxid2,pid,num_prd,supplier,company,rdate)
        cursor.execute(sql3, val3)
            
                
        
        #cursor.execute('update pr_product set supplier=%s,status=1 WHERE id = %s', (supplier, i))
        #mydb.commit()
        ##BC##
        sdata="PID:"+pid+",Distributor:"+supplier+", Request to "+company+", Required Products:"+num_prd+", RegDate:"+rdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=maxid1-1
            cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
            pp = cursor.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
        val2 = (maxid1,pid,pkey,key,sdata,'Req')
        cursor.execute(sql2, val2)
        mydb.commit()   
        ####
            
        act="1"
        msg="Distributed Success"
        return redirect(url_for('dist_sent'))
    
    return render_template('dist_send.html',pid=pid)
    
@app.route('/dist_sent', methods=['GET', 'POST'])
def dist_sent():
    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    data=[]
    
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    dd1 = cursor.fetchone()
    company=dd1[1]

    cursor.execute('SELECT * FROM pr_request where supplier=%s',(supplier, ))
    data1 = cursor.fetchall()
    for ss in data1:
        data3=[]
        cursor.execute('SELECT * FROM pr_product where id=%s',(ss[1], ))
        dd2 = cursor.fetchone()
        data3.append(ss[1])
        data3.append(dd2[2])
        data3.append(dd2[5])
        data3.append(ss[2])
        data3.append(ss[5])
        data.append(data3)
    
    return render_template('dist_sent.html',data=data)

@app.route('/dist_view', methods=['GET', 'POST'])
def dist_view():
    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    data=[]
    
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    dd1 = cursor.fetchone()
    company=dd1[1]

    cursor.execute('SELECT * FROM pr_send where supplier=%s',(supplier, ))
    data1 = cursor.fetchall()
    
    for ss in data1:
        data3=[]
        cursor.execute('SELECT * FROM pr_product where id=%s',(ss[1], ))
        dd2 = cursor.fetchone()
        data3.append(ss[1])
        data3.append(dd2[2])
        data3.append(dd2[5])
        data3.append(dd2[4])
        data3.append(ss[2])
        data3.append(ss[3])
        data3.append(ss[4])
        data3.append(ss[10])
        data3.append(ss[11])
        data3.append(ss[0])
        
        data3.append(ss[5])
        data3.append(ss[6])
        
        data.append(data3)
    
    return render_template('dist_view.html',data=data)

@app.route('/dist_sendprd', methods=['GET', 'POST'])
def dist_sendprd():
    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    data=[]
    data3=[]
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    dd1 = cursor.fetchone()
    company=dd1[1]

    pid = request.args.get('pid')
    rid = request.args.get('rid')
    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    

    cursor.execute('SELECT * FROM pr_shop where distributor=%s',(supplier, ))
    catt = cursor.fetchall()
    # where status=0
    
    cursor.execute('SELECT * FROM pr_send where id=%s',(rid, ))
    sg1 = cursor.fetchone()
    tot=sg1[2]
    

    cursor.execute('SELECT * FROM pr_product where id=%s',(pid, ))
    dd2 = cursor.fetchone()
    pcode=dd2[9]
    print(pcode)
    tot1=str(tot)

    if request.method=='POST':
        num_prd=request.form['num_prd']
        shopp=request.form['shopp']
        pid=request.form['pid']

        num=int(num_prd)
        cursor.execute('SELECT sum(num_prd) FROM pr_send2 where rid=%s',(rid, ))
        sn1 = cursor.fetchone()[0]
        if sn1 is None:
            sn1=0
        bal=tot-sn1

        
        
        
        if bal>=num:

            num_start=sn1+1
            num_end=sn1+num
            num_s=str(num_start)
            num_e=str(num_end)
            plen=len(tot1)
            numStr1 = num_s.zfill(plen)
            numStr2 = num_e.zfill(plen)
            code1=pcode+"P"+numStr1
            code2=pcode+"P"+numStr2

            balance=tot-num_end
            cursor.execute('update pr_send set distribute=%s,balance=%s WHERE id = %s', (num_end, balance, rid))
            mydb.commit()

            cursor.execute('update pr_productcode set shop=%s WHERE pid = %s && pcount between %s and %s', (shopp, pid, num_start, num_end))
            mydb.commit()
            
            cursor.execute("SELECT max(id)+1 FROM pr_send2")
            maxid2 = cursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1
            sql3 = "INSERT INTO pr_send2(id,pid,num_prd,prd_from,prd_to,prd1,prd2,company,supplier,shop,rdate,rid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val3 = (maxid2,pid,num_prd,code1,code2,num_start,num_end,company,supplier,shopp,rdate,rid)
            cursor.execute(sql3, val3)
            mydb.commit()
                    
            
            
            ##BC##
            sdata="PID:"+pid+", Distribute to:"+shopp+", Supplier:"+supplier+", Company:"+company+", Pcode:"+num_s+" to "+num_e+", RegDate:"+rdate
            result = hashlib.md5(sdata.encode())
            key=result.hexdigest()

            mycursor1 = mydb.cursor()
            mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
            maxid1 = mycursor1.fetchone()[0]
            if maxid1 is None:
                maxid1=1
                pkey="00000000000000000000000000000000"
            else:
                mid=maxid1-1
                mycursor1.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
                pp = mycursor1.fetchone()
                pkey=pp[3]
            sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
            val2 = (maxid1,pid,pkey,key,sdata,'PID')
            mycursor1.execute(sql2, val2)
            mydb.commit()   
            ####
                
            act="1"
            msg="Distributed Success"
            return redirect(url_for('dist_view'))
            
        else:
            act="2"
            msg="Product not available!"
    
    return render_template('dist_sendprd.html',catt=catt,pid=pid,rid=rid)

@app.route('/dist_req', methods=['GET', 'POST'])
def dist_req():
    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    data=[]
    
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    dd1 = cursor.fetchone()
    company=dd1[1]

    cursor.execute('SELECT * FROM pr_request2 where supplier=%s',(supplier, ))
    data1 = cursor.fetchall()
    for ss in data1:
        data3=[]
        cursor.execute('SELECT * FROM pr_product where id=%s',(ss[1], ))
        dd2 = cursor.fetchone()
        data3.append(ss[1])
        data3.append(dd2[2])
        data3.append(dd2[5])
        data3.append(ss[2])
        data3.append(ss[6])
        data3.append(ss[3])
        data.append(data3)
    
    return render_template('dist_req.html',data=data)

@app.route('/dist_deliver', methods=['GET', 'POST'])
def dist_deliver():
    ff1=open("log2.txt","r")
    supplier=ff1.read()
    ff1.close()
    data=[]
    
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    dd1 = cursor.fetchone()
    company=dd1[1]

    cursor.execute('SELECT * FROM pr_send2 where supplier=%s',(supplier, ))
    data1 = cursor.fetchall()
    for ss in data1:
        data3=[]
        cursor.execute('SELECT * FROM pr_product where id=%s',(ss[1], ))
        dd2 = cursor.fetchone()
        data3.append(ss[1])
        data3.append(ss[3])
        data3.append(ss[4])
        data3.append(ss[2])
        data3.append(ss[9])
        data3.append(ss[12])
        data.append(data3)
    
    return render_template('dist_deliver.html',data=data)

@app.route('/shop_home', methods=['GET', 'POST'])
def shop_home():
    msg=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log3.txt","r")
    shop=ff1.read()
    ff1.close()
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
    data1 = cursor.fetchone()
    company=data1[1]
    supplier=data1[2]

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    data = cursor.fetchone()
    cursor.execute('SELECT * FROM pr_manufacture where uname=%s',(company, ))
    data2 = cursor.fetchone()
    

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    return render_template('shop_home.html',msg=msg,data=data,data1=data1,data2=data2)

@app.route('/shop_distprd', methods=['GET', 'POST'])
def shop_distprd():
    msg=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log3.txt","r")
    shop=ff1.read()
    ff1.close()
    data4=[]
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
    data1 = cursor.fetchone()
    company=data1[1]
    supplier=data1[2]

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    data = cursor.fetchone()
    cursor.execute('SELECT * FROM pr_manufacture where uname=%s',(company, ))
    data2 = cursor.fetchone()
    
    cursor.execute('SELECT * FROM pr_send where supplier=%s',(supplier, ))
    data3 = cursor.fetchall()
    for ss in data3:
        dat=[]
        pid=ss[1]
        cursor.execute('SELECT * FROM pr_product where id=%s',(pid, ))
        dd2 = cursor.fetchone()
        dat.append(ss[1])
        dat.append(dd2[2])
        dat.append(dd2[5])
        dat.append(dd2[4])
        dat.append(ss[2])
        dat.append(ss[3])
        dat.append(ss[4])
        data4.append(dat)
        
    
    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    return render_template('shop_distprd.html',msg=msg,data=data,data1=data1,data2=data2,data4=data4)

@app.route('/shop_send', methods=['GET', 'POST'])
def shop_send():
    msg=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log3.txt","r")
    shop=ff1.read()
    ff1.close()
    data4=[]
    dat=[]
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
    data1 = cursor.fetchone()
    company=data1[1]
    supplier=data1[2]

    cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
    data = cursor.fetchone()
    cursor.execute('SELECT * FROM pr_manufacture where uname=%s',(company, ))
    data2 = cursor.fetchone()
    
    
    
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    pid = request.args.get('pid')
    if request.method=='POST':
        num_prd=request.form['num_prd']
        pid=request.form['pid']

        cursor.execute("SELECT max(id)+1 FROM pr_request2")
        maxid2 = cursor.fetchone()[0]
        if maxid2 is None:
            maxid2=1
        sql3 = "INSERT INTO pr_request2(id,pid,num_prd,shop,supplier,company,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val3 = (maxid2,pid,num_prd,shop,supplier,company,rdate)
        cursor.execute(sql3, val3)
            
                
        
        #cursor.execute('update pr_product set supplier=%s,status=1 WHERE id = %s', (supplier, i))
        #mydb.commit()
        ##BC##
        sdata="PID:"+pid+",:Retailer"+shop+", Request to "+supplier+", Required Products:"+num_prd+", RegDate:"+rdate
        result = hashlib.md5(sdata.encode())
        key=result.hexdigest()

        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
        maxid1 = mycursor1.fetchone()[0]
        if maxid1 is None:
            maxid1=1
            pkey="00000000000000000000000000000000"
        else:
            mid=maxid1-1
            cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
            pp = cursor.fetchone()
            pkey=pp[3]
        sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
        val2 = (maxid1,pid,pkey,key,sdata,'Req2')
        cursor.execute(sql2, val2)
        mydb.commit()   
        ####
            
        act="1"
        msg="Request Sent"
        return redirect(url_for('shop_sent'))
        
    return render_template('shop_send.html',msg=msg,data=data,data1=data1,data2=data2,pid=pid)

@app.route('/shop_sent', methods=['GET', 'POST'])
def shop_sent():
    msg=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log3.txt","r")
    shop=ff1.read()
    ff1.close()
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
    data1 = cursor.fetchone()
    company=data1[1]
    supplier=data1[2]

    
    data=[]

    cursor.execute('SELECT * FROM pr_request2 where shop=%s',(shop, ))
    data11 = cursor.fetchall()
    for ss in data11:
        data3=[]
        cursor.execute('SELECT * FROM pr_product where id=%s',(ss[1], ))
        dd2 = cursor.fetchone()
        data3.append(ss[1])
        data3.append(dd2[2])
        data3.append(dd2[5])
        data3.append(ss[2])
        data3.append(ss[6])
        data.append(data3)
        
    return render_template('shop_sent.html',msg=msg,data=data,data1=data1)

@app.route('/shop_product', methods=['GET', 'POST'])
def shop_product():
    msg=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log3.txt","r")
    shop=ff1.read()
    ff1.close()
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
    data1 = cursor.fetchone()
    company=data1[1]
    supplier=data1[2]

    
    data=[]

    cursor.execute('SELECT * FROM pr_send2 where supplier=%s',(supplier, ))
    data11 = cursor.fetchall()
    for ss in data11:
        data3=[]
        cursor.execute('SELECT * FROM pr_product where id=%s',(ss[1], ))
        dd2 = cursor.fetchone()
        data3.append(ss[1])
        data3.append(ss[3])
        data3.append(ss[4])
        data3.append(ss[2])
        data3.append(ss[9])
        data3.append(ss[12])
        data3.append(ss[0])
        data.append(data3)
        
    return render_template('shop_product.html',msg=msg,data=data,data1=data1)

@app.route('/shop_sale', methods=['GET', 'POST'])
def shop_sale():
    msg=""
    act=""
    kid=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log3.txt","r")
    shop=ff1.read()
    ff1.close()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    pid = request.args.get('pid')
    rid = request.args.get('rid')
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
    data1 = cursor.fetchone()
    company=data1[1]
    supplier=data1[2]

    
    data=[]

    cursor.execute('SELECT * FROM pr_product where id=%s',(pid, ))
    data2 = cursor.fetchone()
    pcode=data2[9]
    tot=data2[21]
    tot1=str(tot)
    plen=len(tot1)

    

    cursor.execute('SELECT * FROM pr_send2 where id=%s',(rid, ))
    data11 = cursor.fetchone()

    p1=data11[5]
    p2=data11[6]
    print(p1)
    print(" ")
    print(p2)

    cursor.execute('SELECT * FROM pr_productcode where pid=%s && pcount between %s and %s',(pid, p1,p2))
    data22 = cursor.fetchall()


    
    i=p1
    s="0"
    while i<p2:
        dat=[]

        num_start=i
        num_s=str(num_start)
        numStr1 = num_s.zfill(plen)
        code1=pcode+"P"+numStr1

        cursor.execute('SELECT count(*) FROM pr_sale where pcode=%s',(code1, ))
        dt = cursor.fetchone()[0]
        if dt>0:
            s="1"
        else:
            s="0"
            
        dat.append(i)
        dat.append(code1)
        dat.append(s)
        data.append(dat)
        i+=1

    #######
    
    if request.method=='GET':
        act=request.args.get('act')
        kid=request.args.get('kid')
        pcode2=request.args.get('pcode2')
        if act=="1":
            
            cursor.execute("SELECT max(id)+1 FROM pr_sale")
            maxid2 = cursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1
            sql3 = "INSERT INTO pr_sale(id,shop,pid,rid,kid,pcode,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val3 = (maxid2,shop,pid,rid,kid,pcode2,rdate)
            cursor.execute(sql3, val3)
            
                
            cursor.execute('update pr_productcode set sale=1 WHERE pid = %s && product_code=%s', (pid, pcode2))
            mydb.commit()
            
            #cursor.execute('update pr_send2 set supplier=%s,status=1 WHERE id = %s', (supplier, i))
            #mydb.commit()
            ##BC##
            sdata="PID:"+pid+",:Retailer"+shop+", Product:"+pcode2+", RegDate:"+rdate
            result = hashlib.md5(sdata.encode())
            key=result.hexdigest()

            mycursor1 = mydb.cursor()
            mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
            maxid1 = mycursor1.fetchone()[0]
            if maxid1 is None:
                maxid1=1
                pkey="00000000000000000000000000000000"
            else:
                mid=maxid1-1
                cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
                pp = cursor.fetchone()
                pkey=pp[3]
            sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype) VALUES (%s, %s, %s, %s, %s,%s)"
            val2 = (maxid1,pid,pkey,key,sdata,'Sale')
            cursor.execute(sql2, val2)
            mydb.commit()   
            ####
                
            act="1"
            msg="Request Sent"
            return redirect(url_for('shop_sale',pid=pid,rid=rid))
        
    return render_template('shop_sale.html',msg=msg,data=data,data1=data1,data2=data2,pid=pid,rid=rid,data22=data22)

@app.route('/shop_sold', methods=['GET', 'POST'])
def shop_sold():
    msg=""
    act=""
    kid=""
    #supplier=""
    #if 'username' in session:
    #    supplier = session['username']

    ff1=open("log3.txt","r")
    shop=ff1.read()
    ff1.close()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
    data1 = cursor.fetchone()
    company=data1[1]
    supplier=data1[2]

    
    

    cursor.execute('SELECT * FROM pr_sale where shop=%s',(shop, ))
    data = cursor.fetchall()

    return render_template('shop_sold.html',msg=msg,data=data,data1=data1)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
