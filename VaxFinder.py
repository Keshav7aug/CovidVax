import requests
import time
from playsound import playsound
import os

def playit(name):
    os.system(f'mpg123 "{name}"')
def chkAndPlay(d,curr):
    if curr['name'] in d:
        if curr['date'] not in d[curr['name']]:
            d[curr['name']][curr['date']]=curr['avail']
            playit('Five Little Ducks.mp3')
    else:
        playit('Five Little Ducks.mp3')
        d[curr['name']] = {curr['date']:curr['avail']}
def query(Q):
    url = 'https://cdn-api.co-vin.in/api{}'
    response=requests.get(url.format(Q))
    return response.json()
def finder(name,nameList,key):
    for i in nameList:
        if i[key]==name:
            return i
    return False
def findStateCode(name):
    res=query('/v2/admin/location/states')
    states = res['states']
    return finder(name,states,'state_name')
def findDisCode(disName,stateCode=9):
    Districts = query(f'/v2/admin/location/districts/{stateCode}')['districts']
    return finder(disName,Districts,'district_name')
def getAvailbyDis(disName,date,stateCode=9,d={}):
    disCode = findDisCode(disName,stateCode)['district_id']
    response = query(f'/v2/appointment/sessions/public/calendarByDistrict?district_id={disCode}&date={date}')
    centers = response['centers']
    for center in centers:
        sessions = center['sessions']
        for session in sessions:
            if session['available_capacity']>0 and session['min_age_limit']==18:
                print(center['name'],session['date'],session['available_capacity'],disName)
                newD={'name':center['name'],'date':session['date'],'avail':session['available_capacity']}
                chkAndPlay(d,newD)
                file = open(f'vaccx_{stateCode}.txt','a')
                file.write(f"{center['name']}_{session['date']}_{session['available_capacity'],{disName}}\n")
                file.close()
def getAvailbyState(statecode,d={}):
    districts = query(f'/v2/admin/location/districts/{statecode}')['districts']
    for district in districts:
        getAvailbyDis(district['district_name'],'02-05-2021')
        getAvailbyDis(district['district_name'],'09-05-2021')

val=0
d={}
while val<1:
    getAvailbyState(9,d)
    getAvailbyDis(findDisCode('Gurgaon',12)['district_name'],'02-05-2021',12,d)
    getAvailbyDis(findDisCode('Gurgaon',12)['district_name'],'09-05-2021',12,d)
    print(val)
    time.sleep(60)
    val+=1