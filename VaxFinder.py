import requests
import time
import json
#from playsound import playsound
import os
#from text_to_speech import speak
from sys import platform
from datetime import date,timedelta
try:
    import winsound
except:
    pass
class VaccineAvailability:
    def __init__(self):
        self.d={}
    def playit(self,name):
        if platform == 'linux':
            os.system(f'mpg123 -q -k 300 "{name}"')
        else:
            winsound.PlaySound('Five Little Ducks.wav',winsound.SND_FILENAME)
    # def txt2Spch(self,words):
    #     speak(words, "en", save=False)
    def chkAndPlay(self,curr):
        if curr['name'] in self.d:
            if curr['date'] not in self.d[curr['name']]:
                self.d[curr['name']][curr['date']]=curr['avail']
                self.playit('Five Little Ducks.mp3')
                return True
        else:
            self.playit('Five Little Ducks.mp3')
            self.d[curr['name']] = {curr['date']:curr['avail']}
            return True
        return False
    def query(self,Q):
        Q=Q.replace('/public','')
        url = 'https://cdn-api.co-vin.in/api{}'
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
        response=requests.get(url.format(Q),headers=headers)
        if response.status_code!=200:
            print(response.status_code,response.url)
        return response.json()
    def finder(self,name,nameList,key):
        for i in nameList:
            if i[key]==name:
                return i
        return False
    def findStateCode(self,name):
        with open('States.json') as f:
            data = json.load(f) 
        return data[name]
    def findDisCode(self,disName,stateName='Delhi'):
        with open(f'Districts/{stateName}.json') as f:
            data = json.load(f) 
        return data[disName]
    def getCenterDetails(self,centers,addr):
        for center in centers:
            sessions = center['sessions']
            for session in sessions:
                if session['available_capacity']>0 and session['min_age_limit']==18:
                    print(center['name'],session['date'],session['available_capacity'],session['vaccine'],addr)
                    newD={'name':center['name'],'date':session['date'],'avail':session['available_capacity']}
                    if(self.chkAndPlay(newD)):
                        file = open(f'vaccx_{addr}.txt','a')
                        file.write(f"{center['name']}_{session['date']}_{session['available_capacity'],{addr}}\n")
                        file.close()
    def getAvailbyDis(self,disName,date,stateName='Delhi'):
        disCode = self.findDisCode(disName,stateName)
        response = self.query(f'/v2/appointment/sessions/public/calendarByDistrict?district_id={disCode}&date={date}')
        centers = response['centers']
        self.getCenterDetails(centers,disName)
    def getAvailbyPIN(self,PIN,date):
        response = self.query(f'/v2/appointment/sessions/public/calendarByPin?pincode={PIN}&date={date}')
        centers = response['centers']
        self.getCenterDetails(centers,PIN)
    def getAvailbyState(self,stateName='Delhi',noW=1):
        statecode = self.findStateCode(stateName)
        districts = self.query(f'/v2/admin/location/districts/{statecode}')['districts']
        curr_date = date.today()
        for i in range(noW):
            quer_date = date.today()+timedelta(7*i)
            for district in districts:
                try:
                    self.getAvailbyDis(district['district_name'],quer_date.strftime("%d-%m-%Y"))
                except:
                    pass
    def QueriedDistricts(self,DistrictList,stateName='Delhi',noW=1):
        try:
            curr_date = date.today()
            for i in range(noW):
                quer_date = curr_date+timedelta(7*i)
                quer_date=quer_date.strftime("%d-%m-%Y")
                for district in DistrictList:
                    self.getAvailbyDis(district,quer_date,stateName)
        except Exception as E:
            print(E)
            pass
    def QueriedPINs(self,PINList,noW=1):
        try:
            curr_date = date.today()
            for i in range(noW):
                quer_date = curr_date+timedelta(7*i)
                quer_date=quer_date.strftime("%d-%m-%Y")
                for PIN in PINList:
                    self.getAvailbyPIN(PIN,quer_date)
        except:
            pass

val=0
Vax=VaccineAvailability()
AllPins = [] 
while True:
    print(val)
    #Vax.getAvailbyState()
    #Vax.QueriedPINs(AllPins)
    Vax.QueriedDistricts([])
    time.sleep(10)
    val+=1