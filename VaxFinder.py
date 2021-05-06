import requests
import time
from playsound import playsound
import os
from text_to_speech import speak
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
            os.system(f'mpg123 "{name}"')
        else:
            winsound.PlaySound('Five Little Ducks.wav',winsound.SND_FILENAME)
    def txt2Spch(self,words):
        speak(words, "en", save=False)
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
        while response.status_code!=200:
            print(response.status_code)
            time.sleep(60)
            response=requests.get(url.format(Q),headers=headers)
        return response.json()
    def finder(self,name,nameList,key):
        for i in nameList:
            if i[key]==name:
                return i
        return False
    def findStateCode(self,name):
        res=self.query('/v2/admin/location/states')
        states = res['states']
        return self.finder(name,states,'state_name')
    def findDisCode(self,disName,stateCode=9):
        Districts = self.query(f'/v2/admin/location/districts/{stateCode}')['districts']
        return self.finder(disName,Districts,'district_name')
    def getCenterDetails(self,centers,addr,stateCode=9):
        for center in centers:
            sessions = center['sessions']
            for session in sessions:
                if session['available_capacity']>0 and session['min_age_limit']==18:
                    print(center['name'],session['date'],session['available_capacity'],addr)
                    newD={'name':center['name'],'date':session['date'],'avail':session['available_capacity']}
                    if(self.chkAndPlay(newD)):
                        file = open(f'vaccx_{stateCode}.txt','a')
                        file.write(f"{center['name']}_{session['date']}_{session['available_capacity'],{addr}}\n")
                        file.close()
    def getAvailbyDis(self,disName,date,stateCode=9):
        disCode = self.findDisCode(disName,stateCode)['district_id']
        response = self.query(f'/v2/appointment/sessions/public/calendarByDistrict?district_id={disCode}&date={date}')
        centers = response['centers']
        self.getCenterDetails(centers,disName,stateCode)
    def getAvailbyPIN(self,PIN,date,stateCode=9):
        response = self.query(f'/v2/appointment/sessions/public/calendarByPin?pincode={PIN}&date={date}')
        centers = response['centers']
        self.getCenterDetails(centers,PIN,stateCode)
    def getAvailbyState(self,stateName='Delhi',noW=2):
        statecode = self.findStateCode(stateName)['state_id']
        districts = self.query(f'/v2/admin/location/districts/{statecode}')['districts']
        curr_date = date.today()
        for i in range(noW):
            quer_date = date.today()+timedelta(7*i)
            for district in districts:
                self.getAvailbyDis(district['district_name'],quer_date.strftime("%d-%m-%Y"))
    def QueriedDistricts(self,DistrictList,stateCode=9,noW=2):
        curr_date = date.today()
        for i in range(noW):
            quer_date = curr_date+timedelta(7*i)
            quer_date=quer_date.strftime("%d-%m-%Y")
            for district in DistrictList:
                self.getAvailbyDis(district,quer_date,stateCode)
    def QueriedPINs(self,PINList,stateCode=9,noW=2):
        curr_date = date.today()
        for i in range(noW):
            quer_date = curr_date+timedelta(7*i)
            quer_date=quer_date.strftime("%d-%m-%Y")
            for PIN in PINList:
                self.getAvailbyPIN(PIN,quer_date,stateCode)

val=0
Delhi=VaccineAvailability() 
while val<900:
    print(val)
    Delhi.getAvailbyState()
    Delhi.QueriedPINs(['110022'])
    time.sleep(60)
    val+=1