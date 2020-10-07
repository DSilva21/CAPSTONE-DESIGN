#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import urllib.request
import json
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
import pymysql
#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("0.ui")[0]
form_class1 = uic.loadUiType("1.ui")[0]
form_class2 = uic.loadUiType("2.ui")[0]
#선호도 1,2위의 상위 상품의 주소가 저장
qw=[]
#선호도 1,2위의 상위 상품 3개의  상품명이 저장
s=[]
#유저 정보가 저장되는 배열
user_info=[]
rogin_user=[]
cri={}
from math import sqrt
import time
from multiprocessing import Pool #pool import


# In[2]:


#네이버 데이터랩에 존재하는 모든 상품들의 카테고리이다.
item=['여성의류','여성언더웨어/잠옷','남성의류','남성언더웨어/잠옷',
     '여성신발','남성신발','신발용품','여성가방','남성가방','여행용가방/소품','지갑',
     '벨트','모자','장갑','양말','선글라스/안경테','헤어액세사리','시계','순금','주얼리',
     '노트북','스킨케어','베이스메이크업','색조메이크업','클렌징','마스크/팩','선케어','남성화장품','향수','바디케어','헤어케어','헤어스타일링','네일케어','뷰티소품',
     '음향가전','휴대폰','휴대폰액세서리','카메라/캠코터용품','광학기기/용품',
     '주방가전','침실가구','거실가구','주방가구','수납가구',
     '출산/육아','인테리어소품','주변기기','스포츠/레저','생활/건강','여가/생활편의']
item1=item[:]
random.shuffle(item)
#선호도 비교를 위해 만들어진 배열
item2=[[0,'노트북'],[0,'여성의류'],[0,'여성언더웨어/잠옷'],[0,'남성의류'],[0,'남성언더웨어/잠옷'],
      [0,'음향가전'],[0,'여성신발'],[0,'남성신발'],[0,'신발용품'],[0,'여성가방'],[0,'남성가방'],[0,'여행용가방/소품'],[0,'지갑'],
     [0,'벨트'],[0,'모자'],[0,'장갑'],[0,'양말'],[0,'선글라스/안경테'],[0,'헤어액세사리'],[0,'시계'],[0,'순금'],[0,'주얼리'],
     [0,'주방가전'],[0,'스킨케어'],[0,'베이스메이크업'],[0,'색조메이크업'],[0,'클렌징'],[0,'마스크/팩'],[0,'선케어'],[0,'남성화장품'],[0,'향수'],[0,'바디케어'],[0,'헤어케어'],[0,'헤어스타일링'],[0,'네일케어'],[0,'뷰티소품'],
     [0,'인테리어소품'],[0,'휴대폰'],[0,'휴대폰액세서리'],[0,'카메라/캠코터용품'],[0,'광학기기/용품'],
     [0,'주변기기'],[0,'침실가구'],[0,'거실가구'],[0,'주방가구'],[0,'수납가구'],
     [0,'출산/육아'],[0,'스포츠/레저'],[0,'생활/건강'],[0,'여가/생활편의']]
item2_sub=item2[:]
#dbms 연결 부분
conn = pymysql.connect(host='211.105.15.41', user='project', password='dkansk12',db='project', charset='utf8')
cursor = conn.cursor() 


# In[3]:


패션의류=['패션의류','여성의류','여성언더웨어/잠옷','남성의류','남성언더웨어/잠옷']
패션잡화=['패션잡화','여성신발','남성신발','신발용품','여성가방','남성가방','여행용가방/소품','지갑',
     '벨트','모자','장갑','양말','선글라스/안경테','헤어액세사리','패션소품','시계','순금','주얼리']
화장품=['화장품','스킨케어','베이스메이크업','색조메이크업','클렌징','마스크/팩','선케어','남성화장품','향수','바디케어','헤어케어','헤어스타일링','네일케어','뷰티소품']
디지털=['디지털/가전','휴대폰','휴대폰액세서리','카메라/캠코터용품','광학기기/용품',"영상가전","음향가전","생활가전",
    "이미용가전","주방가전","자동차기기","계절가전","학습기기","게임기/타이틀","PC","PC액세서리",
    "노트북","노트북악세서리","태블릿PC","태블릿PC액세서리","모니터","모니터주변기기",
    "주변기기"]
가구=['가구/인테리어','침실가구','거실가구','주방가구','수납가구',"아동/주니어가구","서재/사무용가구",
   "아웃도어가구","DIY자재/용품","인테리어소품"]
출산=['출산/육아','분유','기저귀']
식품=["식품"]
스포츠=['스포츠/레저']
생활=['생활/건강']
여가=['여가/생활편의']


# In[4]:


#데이터랩에서 검색할때 사용할 배열
aw=[]
aw.append(패션의류)
aw.append(패션잡화)
aw.append(화장품)
aw.append(디지털)
aw.append(가구)
aw.append(출산)
aw.append(식품)
aw.append(스포츠)
aw.append(생활)
aw.append(여가)


# In[5]:


# 피어슨 상관계수 구하기
def sim_pearson(data, name1, name2):
    sumX=0
    sumY=0 
    sumPowX=0
    sumPowY=0
    sumXY=0 
    count=0 
    for i in data[name1]: 
        if i in data[name2]: 
            sumX+=data[name1][i]
            sumY+=data[name2][i]
            sumPowX+=pow(data[name1][i],2)
            sumPowY+=pow(data[name2][i],2)
            sumXY+=data[name1][i]*data[name2][i]
            count+=1
    try:
        return ( sumXY- ((sumX*sumY)/count) )/ sqrt( (sumPowX - (pow(sumX,2) / count)) * (sumPowY - (pow(sumY,2)/count)))
    except:
        return 0


# In[6]:


def top_match(data, name, index=3, sim_function=sim_pearson):
    li=[]
    for i in data:
        if name!=i: 
            li.append((sim_function(data,name,i),i))
    li.sort() 
    li.reverse()
    return li[:index]


# In[7]:


def getRecommendation (data,person,sim_function=sim_pearson):
    result = top_match(cri, person ,len(data)) 
    simSum=0 # 유사도 합을 위한 변수
    score=0 # 평점 합을 위한 변수
    li=[] # 리턴을 위한 리스트
    score_dic={} # 유사도 총합을 위한 dic
    sim_dic={} # 평점 총합을 위한 dic
 
    for sim,name in result: # 튜플이므로 한번에 
        #if sim<0 : continue #유사도가 양수인 사람만
        for it in data[name]: 
            score+=sim*data[name][it] 
            score_dic.setdefault(it,0) 
            score_dic[it]+=score 
 
            # 조건에 맞는 사람의 유사도의 누적합을 구한다
            sim_dic.setdefault(it,0) 
            sim_dic[it]+=sim
 
        score=0  
    
    for key in score_dic:
        try:
            score_dic[key]=score_dic[key]/sim_dic[key] 
            li.append((score_dic[key],key)) # list((tuple))의 리턴을 위해서.
        except:
            continue
    li.sort() #오름차순
    li.reverse() #내림차순
    if li==[]:
        return [[0,rogin_user[1][0]],[0,rogin_user[2][0]],[0,rogin_user[3][0]],[0,rogin_user[4][0]],[0,rogin_user[5][0]]]
    return li


# In[8]:


def sim(user_in,user_inf,ita):
    it_sum=0
    sql="select 가중치 from "+user_info[2]+user_info[3]
    cursor.execute(sql)
    rows=cursor.fetchall()
    conn.commit()
    for i in rows:
        it_sum=it_sum+i[0]
    it=[]
    for i in ita:
        critics={}
        sql="select * from "+user_in+user_inf+" where id='"+i+"'"
        cursor.execute(sql)
        rows=cursor.fetchall()
        conn.commit()
        for a in range(0,len(item1)):
            it.append((item1[a],rows[0][a+2]/it_sum))
        for j in it:
             critics[j[0]]=j[1]
        cri[i]=critics


# In[9]:


class Worker_1(QThread):
     def run(self):
            global s
            item2.sort(reverse=True)
            s.append(selectThing(item2[0][1]).getInstance())
         


# In[10]:


class Worker_2(QThread):
     def run(self):
            global s
            item2.sort(reverse=True)
            s.append(selectThing(item2[1][1]).getInstance())


# In[11]:


class Worker_3(QThread):
     def run(self):
            global s
            item2.sort(reverse=True)
            ite=item2[:2]
            ita=[]
            for i in ite:
                ita.append(i[1])
            sim(user_info[2],user_info[3],ita)
            s.append(selectThing(getRecommendation(cri, user_info[4])[0][1]).getInstance())


# In[12]:


class Worker1_1(QThread):
    def run(self):
            global s
            s.append(selectThing(user_info[4]).getInstance())
        


# In[13]:


class Worker1_2(QThread):
    def run(self):
            global s
            s.append(selectThing(rogin_user[0][0]).getInstance())


# In[14]:


class Worker1_3(QThread):
    def run(self):
            global s
            ita=[user_info[4],user_info[5],rogin_user[0][0]]
            sim(user_info[2],user_info[3],ita)
            s.append(selectThing(getRecommendation(cri, user_info[4])[0][1]).getInstance())


# In[15]:


class UClass(QMainWindow) :
    #성별을 선택하는데 사용되는 윈도우
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.initUI()
    def initUI(self):
        self.btn1 = QPushButton('회원가입', self)
        self.btn2 = QPushButton('로그인', self)
        self.title=QLabel('FINDER',self)
        self.label1 = QLabel('아이디', self)
        self.label2 = QLabel('비밀번호', self)
        self.title.setFont(QFont('Times', 15))
        self.title2=QLabel('',self) 
        self.title3=QLabel('',self)
        self.title2.move(150, 400)
        self.title3.move(150, 430)
        self.title.move(200, 80)
        self.label1.move(170,150)
        self.label2.move(170,250)
        self.btn1.move(150, 300)
        self.btn2.move(250, 300)
        self.btn1.clicked.connect(self.make)
        self.btn2.clicked.connect(self.rogin)
        self.le = QLineEdit(self)
        self.le2 = QLineEdit(self)
        self.le2.setEchoMode(2)
        self.le.move(250, 150)
        self.le2.move(250, 250)
        self.setWindowTitle('로그인창')
        self.setGeometry(400,250,500,500)
        self.show()

    def rogin(self):
        sql="select * from user_data";
        cursor.execute(sql)
        count=0
        rows=cursor.fetchall()
        conn.commit()
        for i in rows:
            if(i[0]==self.le.text() and i[1] != self.le2.text()):
                count=count+1
            elif(i[0]==self.le.text() and i[1]==self.le2.text()):
                    user_info.append(i[0])
                    user_info.append(i[1])
                    user_info.append(i[2])
                    user_info.append(i[3])
                    user_info.append(i[4])
                    user_info.append(i[5])
                    sql="select * from "+user_info[2]+user_info[3]+" where id='"+user_info[4]+"'"
                    cursor.execute(sql)
                    rows=cursor.fetchall()
                    conn.commit()
                    for i in range(0,len(item1)):
                        rogin_user.append((item1[i],rows[0][i+2]))
                    rogin_user.sort(key=lambda x:x[1],reverse=True)
                    user_info.append(rogin_user[0][0])
                    self.worker1 = Worker1_1()
                    self.worker2 = Worker1_2()
                    self.worker3 = Worker1_3()
                    self.worker1.start()
                    self.worker2.start()
                    self.worker3.start()
                    self.parent().stack.setCurrentIndex(4)
            else:
                continue
        if count!=0 :
            self.title2.setText('비밀번호가 다릅니다') 
            self.title3.setText('비밀번호를 확인해주세요')
            self.title2.show()
            self.title3.show()
        
        else:
            self.title2.setText('아이디가 없습니다') 
            self.title3.setText('회원가입 해주세요')
            self.title2.move(200, 400)
            self.title3.move(200, 430)
            self.title2.show()
            self.title3.show()
    def make(self):
        sql="select * from user_data";
        cursor.execute(sql)
        count=0
        rows=cursor.fetchall()
        for i in rows:
            if(i[0]==self.le.text()):
                count=count+1
        if count==1:
                self.title2.setText('이미 존재하는') 
                self.title3.setText('회원입니다.')
        elif (self.le.text()=="" or self.le2.text()==""):
            self.title2.setText('빈칸을') 
            self.title3.setText('채워주세요')
        else:
            user_info.append(self.le.text())
            user_info.append(self.le2.text())
            self.parent().stack.setCurrentIndex(1)


# In[16]:


class SClass(QMainWindow, form_class1) :
    #성별을 선택하는데 사용되는 윈도우
    def __init__(self, parent=None) :
        super().__init__(parent=parent)
        self.setupUi(self)
        #버튼에 기능을 연결하는 코드
        self.man.clicked.connect(self.button1Function)
        self.women.clicked.connect(self.button2Function)

    def button1Function(self) :
        user_info.append('남')
        self.parent().stack.setCurrentIndex(2)
    def button2Function(self) :
        user_info.append('여')
        self.parent().stack.setCurrentIndex(2)


# In[17]:


class AClass(QMainWindow, form_class2):
    #나이를 선택하는데 사용되는 윈도우
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        #QRadioButton 사용
        self.ten.clicked.connect(self.groupboxRadFunction)
        self.ten_2.clicked.connect(self.groupboxRadFunction)
        self.ten_3.clicked.connect(self.groupboxRadFunction)
        self.ten_4.clicked.connect(self.groupboxRadFunction)
        self.ten_5.clicked.connect(self.groupboxRadFunction)
        self.ten_6.clicked.connect(self.groupboxRadFunction)
    def groupboxRadFunction(self) :
        if self.ten.isChecked() : 
            user_info.append('10')
            self.parent().stack.setCurrentIndex(3)
        elif self.ten_2.isChecked() : 
            user_info.append('20')
            self.parent().stack.setCurrentIndex(3)
        elif self.ten_3.isChecked() : 
            user_info.append('30')
            self.parent().stack.setCurrentIndex(3)
        elif self.ten_4.isChecked() : 
            user_info.append('40')
            self.parent().stack.setCurrentIndex(3)
        elif self.ten_5.isChecked() : 
            user_info.append('50')
            self.parent().stack.setCurrentIndex(3)
        elif self.ten_6.isChecked() : 
            user_info.append('60')
            self.parent().stack.setCurrentIndex(3)


# In[18]:


class IClass(QMainWindow,form_class):
    #item을 선택하는데 사용되는 윈도우
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.initUI()
    def initUI(self):
        self.setGeometry(450,250,941,708)
        self.abutton=QPushButton("시작하기",self)
        self.abutton.clicked.connect(self.bu)    
        
        ##텍스트
        self.clabel=QLabel('관심있는 카테고리를 선택해주세요...',self)
        self.clabel.setGeometry(150,0,400,50)
        
    def bu(self):
        self.count=0
        self.s=CB(item,self.count).gets()
        self.setGeometry(450,250,941,708)
        self.btnList=[]
        self.btnTop=150
        for i in range(0,len(self.s)):
            self.btnList.append(QPushButton(self.s[i],self))
            self.btnList[i].resize(QSize(180,100))
            if(i<5):
                self.btnList[i].move(180*i,self.btnTop)
            else:
                self.btnList[i].move(180*(i-5),self.btnTop+(100*2))
            self.btnList[i].show()
            self.btnList[i].clicked.connect(self.buttonClicked)
    def buttonClicked(self) :
        for i in range(0,len(self.btnList)):
            self.btnList[i].deleteLater()
        self.count=self.count+1
        sender=self.sender()
        SB(sender.text(),self.count,self.s)
        self.s=CB(item,self.count).gets()
        my_list=[]
        for v in self.s:
            if v not in my_list:
                my_list.append(v)
        self.btnList=[]
        self.btnTop=150
        for i in range(0,len(my_list)):
            self.btnList.append(QPushButton(my_list[i],self))
            self.btnList[i].resize(QSize(180,100))
            if(i<5):
                self.btnList[i].move(180*i,self.btnTop)
            else:
                self.btnList[i].move(180*(i-5),self.btnTop+(100*2))
        if self.count==7:
            item2.sort(reverse=True)
            self.worker1 = Worker_1()
            self.worker2 = Worker_2()
            self.worker3 = Worker_3()
            self.worker1.start()
            self.worker2.start()
            self.worker3.start()
            self.parent().stack.setCurrentIndex(4) 
        else:
            for i in range(0,len(my_list)):
                self.btnList[i].show()
                self.btnList[i].clicked.connect(self.buttonClicked)


# In[19]:


class CB:
    def __init__(self,name,count):
        self.name=name
        self.count=count
        self.s=[]
        self.s1=[]
        self.init()
    def init(self):
        if self.count<5:
            for i in range(0,10):
                self.s.append(self.name[i+(self.count*10)])
        elif self.count==5:
            item2.sort(reverse=True)
            sql="select id,가중치 from "+user_info[2]+user_info[3]
            cursor.execute(sql)
            rows=cursor.fetchall()
            conn.commit()
            rog=list(rows)
            rog.sort(key=lambda x:x[1],reverse=True)
            for i in range(0,5):
                self.s.append(item2[i][1])
                self.s.append(rog[i][0])
        else:
            global cri
            item2.sort(reverse=True)
            ite=item2[:5]
            ita=[]
            for i in ite:
                ita.append(i[1])
            sim(user_info[2],user_info[3],ita)
            for i in range(1,6):
                self.s.append(item2[i][1])
                self.s.append(getRecommendation(cri, user_info[4])[i-1][1])
    def gets(self):
        random.shuffle(self.s)
        return self.s


# In[20]:


class SB:
    def __init__(self,name,count,s):
        self.s1 = [[0 for col in range(2)] for row in range(10)]
        self.name=name
        self.count=count
        self.s=s
        self.con=0
        self.init()
    def init(self):
        if self.count==6:
            user_info.append(self.name)
            for a in range(0,len(item)):
                for i in self.s:
                    if item2[a][1]==i:
                        self.s1[self.con][0]=item2[a][0]
                        self.s1[self.con][1]=i
                        self.con=self.con+1
            self.s1.sort()
            if self.name==self.s1[9][1]:
                for a in range(0,len(item)):
                        if item2[a][1]==self.name:
                            item2[a][0]=100
            else:
                for a in range(0,len(item)):
                        if item2[a][1]==self.name:
                            item2[a][0]=100
        elif self.count==7:
            user_info.append(self.name)
            for a in range(0,len(item)):
                for i in self.s:
                    if item2[a][1]==i:
                        self.s1[self.con][0]=item2[a][0]
                        self.s1[self.con][1]=i
                        self.con=self.con+1
            
            self.s1.sort()
            if self.name==self.s1[9][1]:
                for a in range(0,len(item)):
                        if item2[a][1]==self.name:
                            item2[a][0]=50
            else:
                for a in range(0,len(item)):
                        if item2[a][1]==self.name:
                            item2[a][0]=50
        else:
            for a in range(0,len(item)):
                for i in self.s:
                    if item2[a][1]==i:
                        self.s1[self.con][0]=item2[a][0]
                        self.s1[self.con][1]=i
                        self.con=self.con+1
            
            self.s1.sort()
            if self.name==self.s1[9][1]:
                for a in range(0,len(item)):
                        if item2[a][1]==self.name:
                            item2[a][0]=item2[a][0]+1
            else:
                for a in range(0,len(item)):
                        if item2[a][1]==self.name:
                            item2[a][0]=self.s1[9][0]+1


# In[21]:


class selectThing:
    #선호도 물품의 가장 많이 검색된 1,2,3위를 추천하는 부분입니다.
    def __init__(self,name):
        self.name=name
        self.init()
    def init(self):
        q=1
        w=0
        naljiBreak=True
        for a in aw:
            w=0
            for j in a:
                if(j==self.name):
                    naljiBreak=False
                    break
                w=w+1
            if(naljiBreak==False):
                break
            q=q+1
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        
        

        
        driver = webdriver.Chrome('chromedriver.exe',chrome_options=options)
        driver.get("https://datalab.naver.com/shoppingInsight/sCategory.naver")
        time.sleep(0.01)
        #driver.implicitly_wait(100) 
        
        element1 = driver.find_element_by_xpath( '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span')
        element1.click()
        choice1 = driver.find_element_by_xpath( '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li['+str(q)+']')
        choice1.click()
        if(w!=0):
            element2 = driver.find_element_by_xpath( '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span')
            element2.click()
            choice2=driver.find_element_by_xpath( '//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li['+str(w)+']')
            choice2.click()
        element3=driver.find_element_by_xpath('//*[@id="18_device_0"]')
        element3.click()
        if(user_info[2]=='여'):
            se=1
        else:
            se=2
        element4=driver.find_element_by_xpath('//*[@id="19_gender_'+str(se)+'"]')
        element4.click()
        if(user_info[3]=='10'):
            age=1
        elif(user_info[3]=='20'):
            age=2
        elif(user_info[3]=='30'):
            age=3
        elif(user_info[3]=='40'):
            age=4
        elif(user_info[3]=='50'):
            age=5
        else:
            age=6
        element5=driver.find_element_by_xpath('//*[@id="20_age_'+str(age)+'"]')
        element5.click()
        element6=driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div/a/span')
        element6.click()
        time.sleep(1)
        #driver.implicitly_wait(100000000000) 
        item1=driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li[1]/a')
        item2=driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li[2]/a')
        item3=driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/div[1]/ul/li[3]/a')
        self.it=[]
        self.it.append(item1.text)
        self.it.append(item2.text)
        self.it.append(item3.text)
        for i in range(0,3):
            #네이버 open api를 통해 1,2,3,위의 물품 제일 위쪽에 검색되는 상품의 주소를 받아오는 부분입니다.
            self.it[i]=self.it[i][2:]
            client_id = "tChP3rm6ZZnsp7WIJTpV"
            client_secret = "PlTuZnmVW4"
            encText = urllib.parse.quote(self.it[i])
            url = "https://openapi.naver.com/v1/search/shop?query="+encText
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request)
            response_body = response.read()
            info=json.loads(response_body.decode('utf-8'))
            qw.append([self.it[i],info['items'][0]['link'],info['items'][0]['image']])
        driver.quit()
        
    def getInstance(self):
        return self.it


# In[22]:


class TClass(QMainWindow):
    #item을 선택하는데 사용되는 윈도우
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.initUI()
    def initUI(self):
        self.setGeometry(400,250,500,300)
        self.progress = QProgressBar(self)
        self.timer = QBasicTimer()
        self.step = 0
        self.progress.setGeometry(50,50 , 400, 50)
        self.btnbutton=QPushButton("시작하기",self)
        
       # 텍스트 
        self.tlabel=QLabel('상품을 추천중입니다..',self)
        self.tlabel.setGeometry(150,150,200,50)
        
        
        self.progress.setMaximum(100)
        self.btnbutton.show()
        self.progress.show()
        self.btnbutton.clicked.connect(self.buttonClicked)
    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.btnbutton.setText('시작하기')
            self.step=0
            self.progress.setValue(self.step)
            self.parent().stack.setCurrentIndex(5)
            return
        self.step = self.step + 5 # 로딩 속도 조절
        self.progress.setValue(self.step)
    def buttonClicked(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btnbutton.setText('Start')
        else:
            self.timer.start(100, self)
            self.btnbutton.setText('Stop')


# In[23]:


class LClass(QMainWindow,form_class):
    #추천 아이템의 좌표를 제공하는데 사용되는 윈도우
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.initUI()
    def initUI(self):
        self.setGeometry(10,10,1200,1000)  ##0 0 1200 1200
        self.btnbutton=QPushButton("추천상품 확인",self) ##추천된 상품 확인하기
        self.btnTop=100
        self.btnbutton.show()
        self.btnbutton.clicked.connect(self.buttonClicked)
        
        self.textlabel=QLabel('마음에 들지 않으셨다면 재추천을, 마음에 드셨다면 만족을 눌러주십시오',self)
        self.textlabel.setGeometry(200,0,500,50)
        
    def buttonClicked(self) :
        self.btnList=[]
        self.titList=[]
        for i in range(0,len(qw)):
                self.titList.append(QLabel(qw[i][0], self))
                self.btnList.append(QPushButton(qw[i][0],self))
                self.btnList[i].resize(QSize(300,200))
                url=qw[i][2]
                urllib.request.urlretrieve(url, "test.jpg")
                self.btnList[i].setStyleSheet("border-image : url(test.jpg);")
                if i<3:
                    self.titList[i].move(350*i,60)
                    self.btnList[i].move(350*i,self.btnTop)
                elif 2<i<6:
                    self.titList[i].move(350*(i-3),310)
                    self.btnList[i].move(350*(i-3),self.btnTop+250)
                else:
                    self.titList[i].move(350*(i-6),560)
                    self.btnList[i].move(350*(i-6),self.btnTop+500)
                self.btnList[i].show()
                self.titList[i].show()
                self.btnList[i].clicked.connect(self.btnClicked)
        self.btn1=QPushButton("재추천",self) ## 다시하기-> 재추천
        self.btn1.resize(QSize(200,100))
        self.btn2=QPushButton("만족",self)
        self.btn2.resize(QSize(200,100))
        self.btn1.move(350,900)
        self.btn2.move(550,900)
        self.btn1.clicked.connect(self.btn1Clicked)
        self.btn2.clicked.connect(self.btn2Clicked)
        self.btn1.show()
        self.btn2.show()
    def btnClicked(self):
        sender=self.sender()
        for i in range(0,len(qw)):
            if qw[i][0]==sender.text():
                from selenium import webdriver
                driver = webdriver.Chrome('chromedriver.exe')
                driver.get(qw[i][1])
                break;
    def btn1Clicked(self):
        for i in self.btnList:
            i.deleteLater()
        self.btn1.deleteLater()
        self.btn2.deleteLater()
        global user_info
        global item2
        global s
        global qw
        global cri
        for i in self.btnList:
            i.deleteLater()
        for i in self.titList:
            i.clear()
        s=[]
        qw=[]
        cri={}
        user_info=user_info[:4]
        item2=item2_sub
        self.parent().stack.setCurrentIndex(3)
    def btn2Clicked(self):
        try:
            sql="""insert into user_data values (%s,%s,%s,%s,%s,%s)""";
            val=(user_info[0],user_info[1],user_info[2],user_info[3],user_info[4],user_info[5])
            cursor.execute(sql, val)
            sql="""insert into update_list(name,F,S) values (%s,%s,%s)""";
            val=(user_info[2]+user_info[3],user_info[4],user_info[5])
            cursor.execute(sql, val)
            conn.commit()
            conn.close()
            self.deleteLater()
        except:
            sql="""insert into update_list(name,F,S) values (%s,%s,%s)""";
            val=(user_info[2]+user_info[3],user_info[4],user_info[5])
            cursor.execute(sql, val)
            sql="update user_data set FIRST_PRODUCT= '"+user_info[4]+"' where id= '"+user_info[0]+"'"
            cursor.execute(sql)
            sql="update user_data set SECOND_PRODUCT= '"+user_info[5]+"' where id= '"+user_info[0]+"'"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            self.deleteLater()


# In[24]:



  ##  start_time=time.time()
 ##   pool=Pool(processes=8)#8개의 프로세스
 ##   pool.map(selectThing)
##    print("--- %s seconds ---" % (time.time() - start_time))


# In[ ]:


class MainWindow(QMainWindow,form_class):
    #위에 창들을 합친 윈도우
    def __init__(self):
        super().__init__()
        self.stack = QtWidgets.QStackedLayout(self)
        self.stack1 = UClass(self)
        self.stack2 = SClass(self)
        self.stack3 = AClass(self)
        self.stack4 = IClass(self)
        self.stack5 = TClass(self)
        self.stack6= LClass(self)
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)
        self.stack.addWidget(self.stack4)
        self.stack.addWidget(self.stack5)
        self.stack.addWidget(self.stack6)
        self.show()
app = QtWidgets.QApplication([])
main = MainWindow()
app.exec()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




