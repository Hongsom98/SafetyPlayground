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
        print("Xml DownLoad Complete")
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
    rankList = []
    for i in p:
        dateList.append(i[0])
        rankList.append(int(i[6]))
    return [dateList, rankList]

def ExtractData(XmlStr):
    Tree = ElementTree.fromstring(XmlStr)

    ItemInElements = Tree.iter("item")

    Result = {}
    for item in ItemInElements:
        Result["birthday"] = item.find("birthday").text
        Result["chaksunT"] = item.find("chaksunT").text
        Result["hrName"] = item.find("hrName").text
        Result["hrNo"] = item.find("hrNo").text
        Result["birthplace"] = item.find("name").text
        Result["rank"] = item.find("rank").text
        Result["rating"] = item.find("rating").text
        Result["ord1CntY"] = item.find("ord1CntY").text
        Result["ord2CntY"] = item.find("ord2CntY").text
        Result["ord3CntY"] = item.find("ord3CntY").text
        Result["sex"] = item.find("sex").text
        Result["trName"] = item.find("trName").text
        Result["trNo"] = item.find("trNo").text
    raceList = SearchHorseRaceResults(Result["hrNo"])
    return [Result, raceList]
