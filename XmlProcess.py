import urllib
import http.client
from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser
from xml.etree import ElementTree
import RandomForest
from multipledispatch import dispatch
import os
import GetLucky


SearchLegion = None
ServiceKey = "s523%2FmgXSIIE%2B6eS%2By64bcqPxeQv19uqkY3JBSbCjg%2F%2Bob66pyHuaR5qW5uEspagQYQqTVXZfuTg%2B%2BD91g84UA%3D%3D"
DataPotal = "apis.data.go.kr"


def DoSearchWithRaceRound(InputDate):
    Fronturl = "/B551015/API26/entrySheet?serviceKey="
    conn = http.client.HTTPConnection(DataPotal)

    conn.request("GET", Fronturl+ServiceKey+"&pageNo=1&numOfRows=500&meet=1&rc_date=" + InputDate + "&rc_month=" + InputDate[:6])
    req = conn.getresponse()

    if int(req.status) == 200:
        Tree = ElementTree.fromstring(req.read())
        ItemInElements = Tree.iter("item")
        rcNo = 0
        for item in ItemInElements:
            rcNo = item.find("rcNo").text
        return rcNo
    else:
        print("Xml DownLoad Error")

def MakeNHorseList(rcDate, rcRound):
    url = "http://race.kra.co.kr/raceScore/ScoretableDetailList.do?meet=1&realRcDate=" + str(rcDate) + "&realRcNo=" + str(rcRound)
    result = urlopen(url)
    html = result.read()
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find_all('table')
    p = parser.make2d(temp[2])
    del p[0]
    for i in range(len(p)):
        p[i] = p[i][2]
    return p

@dispatch(str)
def SearchHorseProfile(InputHorseName):
    FrontUrl = "/B551015/API8/raceHorseInfo?ServiceKey="
    conn = http.client.HTTPConnection(DataPotal)
    HorseName = urllib.parse.quote(InputHorseName)

    conn.request("GET", FrontUrl + ServiceKey + "&pageNo=1&numOfRows=10&hr_name=" + HorseName + "&meet=" + SearchLegion)
    req = conn.getresponse()

    if int(req.status) == 200:
        return ExtractData(req.read())
    else:
        print("Xml DownLoad Error")

@dispatch(str, str)
def SearchHorseProfile(InputHorseName, region):
    global SearchLegion
    if region == "??????":
        SearchLegion = "1"
    elif region == "??????":
        SearchLegion = "2"
    else:
        SearchLegion = "3"
    FrontUrl = "/B551015/API8/raceHorseInfo?ServiceKey="
    conn = http.client.HTTPConnection(DataPotal)
    HorseName = urllib.parse.quote(InputHorseName)

    conn.request("GET", FrontUrl+ServiceKey+"&pageNo=1&numOfRows=10&hr_name="+HorseName+"&meet="+SearchLegion)
    req = conn.getresponse()

    if int(req.status) == 200:
        return ExtractData(req.read())
    else:
        print("Xml DownLoad Error")

def SearchHorseRaceResults(InputHorseNum):
    url = "https://studbook.kra.co.kr/html/info/ind/s_race_result.jsp?mabun=" + InputHorseNum
    result = urlopen(url)
    html = result.read()
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all('table')
    p = parser.make2d(tables[2])
    del p[0]
    dateList = []
    roundList = []
    rankList = []
    for i in p:
        dateList.append('.'.join(i[0].split('-')))
        roundList.append(i[1])
        rankList.append(int(i[6]))
    return [dateList, roundList, rankList]

def ExtractData(XmlStr):
    Tree = ElementTree.fromstring(XmlStr)
    ItemInElements = Tree.iter("item")

    Result = []
    for item in ItemInElements:
        Result.append(item.find("birthday").text)
        Result.append(item.find("chaksunT").text)
        Result.append(item.find("hrName").text)
        Result.append(item.find("hrNo").text)
        Result.append(item.find("name").text)
        Result.append(item.find("rank").text)
        Result.append(item.find("rating").text)
        Result.append(item.find("ord1CntY").text)
        Result.append(item.find("ord2CntY").text)
        Result.append(item.find("ord3CntY").text)
        Result.append(item.find("sex").text)
        Result.append(item.find("trName").text)
        Result.append(item.find("trNo").text)

    raceList = SearchHorseRaceResults(Result[3])

    return [Result, raceList]

def ForPredictDate():
    import datetime

    today = datetime.datetime.now().strftime("%Y%m%d")
    while True:
        temp = pd.Timestamp(today).day_name()
        if temp == "Saturday" or temp == "Sunday":
            return today
        today = str(int(today)+1)

def TakeListToPredict():
    RandomForest.Predict()

    DateToPredict = ForPredictDate()
    CharToDelete = "/()??????"
    for x in range(len(CharToDelete)):
        DateToPredict = DateToPredict.replace(CharToDelete[x], "")

    ToPredictSet = TakeDataToPredict(DateToPredict)

    PredictedSet = []
    for i in ToPredictSet:
        PredictedSet.append(GetLucky.GetLuckyNumber(int(i[0]), int(i[1])))
    os.remove('PredictSet.txt')
    return [ToPredictSet, PredictedSet]

def TakeDataToPredict(DateToPredict):
    pgCnt = 1
    WillPredict = []
    while True:
        if pgCnt > 15:
            break

        url = "https://race.kra.co.kr/chulmainfo/registStateRegistList.do?meet=1&date=" + DateToPredict + "&pgNo=" + str(pgCnt)
        result = urlopen(url)
        html = result.read()
        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.find_all("table")
        p = parser.make2d(temp[2])
        del p[0]

        if p[0][0] != "????????? ????????????.":
            for i in p:
                WillPredict.append([i[0], i[6]])
        pgCnt += 1

    return WillPredict

def TakeRounds(DateToPredict):
    pgCnt = 1
    Return = []
    while True:
        if pgCnt > 15:
            break

        url = "https://race.kra.co.kr/chulmainfo/registStateRegistList.do?meet=1&date=" + DateToPredict + "&pgNo=" + str(pgCnt)
        result = urlopen(url)
        html = result.read()
        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.find_all("table")
        p = parser.make2d(temp[2])
        del p[0]

        if p[0][0] != "????????? ????????????.":
            Return.append(pgCnt)
        pgCnt += 1

    return Return
