import urllib
import http.client
from urllib.request import urlopen
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser
from xml.etree import ElementTree

SearchLegion = None
ServiceKey = "s523%2FmgXSIIE%2B6eS%2By64bcqPxeQv19uqkY3JBSbCjg%2F%2Bob66pyHuaR5qW5uEspagQYQqTVXZfuTg%2B%2BD91g84UA%3D%3D"
DataPotal = "apis.data.go.kr"

def InitSettings():
    pass

def SearchHorseProfile(InputHorseName):
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
    return [dateList, roundList,rankList]

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
