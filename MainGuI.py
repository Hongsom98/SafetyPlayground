from tkinter import *
import webbrowser
import XmlProcess

from io import BytesIO
import urllib
import urllib.request
from PIL import Image,ImageTk

import pickle

from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time

import folium
import sys
from cefpython3 import cefpython as cef

from tkinter.filedialog import askopenfilename
import tkinter.messagebox

from youtubesearchpython import *

from tkcalendar import Calendar, DateEntry
host = "smtp.gmail.com"  # Gmail SMTP 서버 주소.
port = "587"


def Button_Namuwiki_Link():
    webbrowser.open("https://namu.wiki/w/%EA%B2%BD%EB%A7%88")


class MainGui:
    def __init__(self):
        self.MainWnd = Tk()
        self.MainWnd.title("SafetyPlayGround")
        self.MainWnd.geometry("480x680+660+240")
        #self.MainWnd.configure(background="black")
        self.senderAddress = 'gksduddls33@gmail.com'
        self.passwd = 'brownie9065!@'

        self.MainWnd.resizable(False, False)

        self.MainWnd_Button_List = []
        self.SearchObjectsList = []
        self.SearchDateObjectsList = []
        self.photoGmail = PhotoImage(file="Photo/Gmail_icon.png")
        self.photoTelegram = PhotoImage(file="Photo/Telegram_icon.png")
        self.photoNamuwiki = PhotoImage(file="Photo/Namuwiki_icon.png")
        self.photoWhiteStar = PhotoImage(file="Photo/book_mark_off.png")
        self.photoYellowStar = PhotoImage(file="Photo/book_mark_on.png")
        self.input_text = None
        self.input_date = None
        self.MainSceneButtons()
        self.FavList = []

        self.Datacanvas = None
        self.Graphcanvas = None
        self.SelectRocation = None
        self.MsgTitle = None
        self.recipientAddr = None
        self.msgtext = None

        self.MainWnd.mainloop()

    def MainSceneButtons(self):
        self.MainWnd_Button_List.append(Button(self.MainWnd, text='서울', width=10, height=5, command=self.ButtonSeoulInput))
        self.MainWnd_Button_List.append(Button(self.MainWnd, text='부경', width=10, height=5, command=self.ButtonBugyoungInput))
        self.MainWnd_Button_List.append(Button(self.MainWnd, text='제주', width=10, height=5, command=self.ButtonJejuInput))

        self.MainWnd_Button_List.append(Button(self.MainWnd, image=self.photoGmail, command=self.ButtonGmailSend))
        self.MainWnd_Button_List.append(Button(self.MainWnd, image=self.photoTelegram, command=self.ButtonTelegramSend))
        self.MainWnd_Button_List.append(Button(self.MainWnd, image=self.photoNamuwiki, command=Button_Namuwiki_Link))

        self.MainScenePlace()

    def MainScenePlace(self):
        self.MainWnd_Button_List[0].place(x=200, y=50)
        self.MainWnd_Button_List[1].place(x=200, y=200)
        self.MainWnd_Button_List[2].place(x=200, y=350)
        self.MainWnd_Button_List[3].place(x=0, y=580)
        self.MainWnd_Button_List[4].place(x=380, y=580)
        self.MainWnd_Button_List[5].place(x=190, y=580)

    def SetSearchButtons(self):
        self.input_text = StringVar()  # 경주마 이름 입력
        self.SearchObjectsList.append(Entry(self.MainWnd, textvariable=self.input_text, width=30)) # 0
        self.SearchObjectsList.append(Button(self.MainWnd, text="검색", command=self.SearchDef)) #1
        self.SearchObjectsList.append(Button(self.MainWnd, text="불러오기", command=self.LoadDataDef)) #2

        self.input_date = StringVar()  # 경기날짜 입력
        self.input_round = StringVar()  # 경기라운드 입력
        self.SearchObjectsList.append(Entry(self.MainWnd, textvariable=self.input_date, width=20)) # 날짜 3
        self.SearchObjectsList.append(Label(self.MainWnd, text="날짜")) # 4
        self.SearchObjectsList.append(Entry(self.MainWnd, textvariable=self.input_round, width=20)) # 라운드 5
        self.SearchObjectsList.append(Label(self.MainWnd, text="라운드")) # 6
        self.SearchObjectsList.append(Button(self.MainWnd, text="검색", command=self.SearchDateDef)) # 검색 7
        #self.SearchObjectsList.append(Button(self.MainWnd, text="검색", command=self.PressDate))
        self.SearchObjectsList.append(Button(self.MainWnd, text="다음 경기 예측하기", command=self.TenserFlow, width=64, height=3)) # 예측 8
        self.SearchObjectsList.append(Button(self.MainWnd, image=self.photoWhiteStar, command=self.Favorate, width=50, height=50)) # 북마크 9
        # self.SearchObjectsList.append(Canvas(self.MainWnd,bg='white',width=400,height=300))
        self.SearchObjectsList.append(Button(self.MainWnd, text="날짜선택", command=self.dateSelect, width=20))  # 예측 10
        self.Datacanvas = Canvas(self.MainWnd, bg='white', width=150, height=300)
        self.Datacanvas.pack()
        self.Graphcanvas = Canvas(self.MainWnd, bg='white', width=450, height=170)
        self.Graphcanvas.pack()
        self.SearchObjectsPlace()

    def SearchObjectsPlace(self):
        self.SearchObjectsList[0].place(x=0, y=50)
        self.SearchObjectsList[1].place(x=220, y=49)
        self.SearchObjectsList[2].place(x=260, y=49)
        self.SearchObjectsList[3].place(x=0, y=650)
        self.SearchObjectsList[4].place(x=150, y=650)
        self.SearchObjectsList[5].place(x=180, y=650)
        self.SearchObjectsList[6].place(x=300, y=649)
        self.SearchObjectsList[7].place(x=370, y=649)
        self.SearchObjectsList[8].place(x=10, y=400)
        self.SearchObjectsList[9].place(x=320, y=30)
        self.SearchObjectsList[10].place(x=0, y=650)
        self.Datacanvas.place(x=10, y=90)
        self.Graphcanvas.place(x=10, y=465)

    def LoadDataDef(self):
        try:
            with open('bookmark', 'rb') as f:
                self.FavList = pickle.load(f)
                print("성공")
                print(self.FavList)
                print("여기까지 리스트")
        except:
            print("실패")
            pass

    def Favorate(self):
        self.SearchObjectsList[9].destroy()
        Result=XmlProcess.SearchHorseProfile(self.input_text.get())
        print("시작")
        print(self.FavList)
        print("중간시작")
        print(Result)
        print("끝")
        if Result[0] in self.FavList:
            print("리스트에있음")
            self.SearchObjectsList[9] = Button(self.MainWnd, image=self.photoWhiteStar, command=self.Favorate, width=50,height=50)
            self.FavList.remove(Result[0])
        else:
            print("리스트에없음")
            self.SearchObjectsList[9] = Button(self.MainWnd, image=self.photoYellowStar, command=self.Favorate,width=50, height=50)
            self.FavList.append(Result[0])
        '''for i in self.FavList :
            if i == Result[0] :
                self.SearchObjectsList[9] = Button(self.MainWnd, image=self.photoWhiteStar, command=self.Favorate, width=50, height=50)
                del self.FavList[i]
                break
            else:
                self.SearchObjectsList[9] = Button(self.MainWnd, image=self.photoYellowStar, command=self.Favorate, width=50, height=50)
                self.FavList.append(Result)'''
        with open('bookmark', 'wb') as f:
            pickle.dump(self.FavList, f)
        self.SearchObjectsList[9].place(x=320, y=30)


    def TenserFlow(self):
        topWnd = Toplevel(self.MainWnd)
        topWnd.geometry("320x200+820+100")

        topWnd.title("경기 예측 결과")

    def PressDate(self):
        thread = threading.Thread(target=self.SearchDateDef)
        thread.daemon = True
        thread.start()

    def SearchDateDef(self):
        keyword = self.SelectRocation + " "+ self.input_date + " " + self.input_round.get() + "경주"

        print(keyword)
        videoSearch = VideosSearch(keyword,limit=10)

        result = videoSearch.result()
        for i in range(10):
            print(result['result'][i]['title'], end='->')
            print(result['result'][i]['link'])
        sys.excepthook = cef.ExceptHook
        cef.Initialize()
        cef.CreateBrowserSync(url=result['result'][0]['link'], window_title="경마 시청")
        cef.MessageLoop()

    def dateSelect(self):
        def print_sel():
            k = str(cal.selection_get())
            print(k[5:7])
            self.input_date = k[0:4]+"."+k[5:7] + "." + k[8:10]

        top = Toplevel(self.MainWnd)

        cal = Calendar(top,
                       font="Arial 14", selectmode='day',
                       cursor="hand1", year=2021, month=6, day=5)
        cal.pack(fill="both", expand=True)
        Button(top, text="ok", command=print_sel).pack()

    def SearchDef(self):
        self.Datacanvas.delete('data')
        ReturnResult = XmlProcess.SearchHorseProfile(self.input_text.get())
        self.SearchObjectsList[9].destroy()
        if ReturnResult[0] in self.FavList:
            self.SearchObjectsList[9] = Button(self.MainWnd, image=self.photoYellowStar, command=self.Favorate, width=50, height=50)
        else:
            self.SearchObjectsList[9] = Button(self.MainWnd, image=self.photoWhiteStar, command=self.Favorate, width=50,height=50)
        self.SearchObjectsList[9].place(x=320, y=30)
        print(ReturnResult[0])
        HorseInfo = ReturnResult[0]
        HorseRaceDate = ReturnResult[1][0]
        HorseRaceRank = ReturnResult[1][1]
        x = 10
        y = 15
        #for i in self.FavList.values():
        #    #print(i.find(str(Result["hrNo"])))
        #    if (i.find(str(Result["hrNo"])) == 0 ):
        #        print("있음")
        #    else:
        #        print("없음")
        #print(HorseRaceDate)
        #print(HorseRaceRank)
        '''for key, value in HorseInfo.items():
            self.Datacanvas.create_text(x, y, text=":" + value, tags='data', justify=LEFT, anchor = W)
            if key == "hrNo":
                self.HrNo = value
                print(self.HrNo)
            y = y + 15'''
        for i in range(13):
            if i ==0:
                self.Datacanvas.create_text(x, y, text= "생일:" + ReturnResult[0][i], tags='data', justify=LEFT, anchor=W)
            elif i ==1:
                self.Datacanvas.create_text(x, y, text="상금:" + ReturnResult[0][i], tags='data', justify=LEFT, anchor=W)
            elif i ==2:
                self.Datacanvas.create_text(x, y, text="이름:" + ReturnResult[0][i], tags='data', justify=LEFT, anchor=W)
            elif i ==3:
                self.Datacanvas.create_text(x, y, text="마번:" + ReturnResult[0][i], tags='data', justify=LEFT, anchor=W)
                self.HrNo = ReturnResult[0][3]
            elif i ==4:
                self.Datacanvas.create_text(x, y, text="태어난곳:" + ReturnResult[0][i], tags='data', justify=LEFT, anchor=W)
            elif i ==5:
                self.Datacanvas.create_text(x, y, text="등급조건:" + ReturnResult[0][i], tags='data', justify=LEFT, anchor=W)
            elif i ==6:
                self.Datacanvas.create_text(x, y, text="레이팅:" + ReturnResult[0][i], tags='data', justify=LEFT, anchor=W)
            elif i ==7:
                self.Datacanvas.create_text(x, y, text="최근 1착:" + ReturnResult[0][i], tags='data', justify=LEFT, anchor=W)
            elif i ==8:
                self.Datacanvas.create_text(x, y, text="최근 2착:" + ReturnResult[0][i], tags='data', justify=LEFT, anchor=W)
            elif i ==9:
                self.Datacanvas.create_text(x, y, text="최근 3착:" + ReturnResult[0][i], tags='data', justify=LEFT, anchor=W)
            elif i ==10:
                self.Datacanvas.create_text(x, y, text="성별:" + ReturnResult[0][i], tags='data', justify=LEFT, anchor=W)
            elif i ==11:
                self.Datacanvas.create_text(x, y, text="조교사명:" + ReturnResult[0][i], tags='data', justify=LEFT, anchor=W)
            elif i ==12:
                self.Datacanvas.create_text(x, y, text="조교사번호:" + ReturnResult[0][i], tags='data', justify=LEFT, anchor=W)
            y = y+15

            # print(key, ":", value)
        urlFirst = 'https://studbook.kra.co.kr/h_photo/' #042/042945-l.jpg'
        url = urlFirst + self.HrNo[0] + self.HrNo[1] + self.HrNo[2] + '/' + self.HrNo + '-l.jpg'

        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        im = im.resize((300, 300))
        image = ImageTk.PhotoImage(im)

        temp = Label(self.MainWnd, image=image)
        temp.image = image
        temp.place(x=170, y=90)

    def TurnToSearchScene(self):
        for i in range(len(self.MainWnd_Button_List)):
            self.MainWnd_Button_List[i].destroy()
        self.MainWnd_Button_List.clear()

        self.SetSearchButtons()

    def TurnToMainScene(self):
        for i in range(len(self.SearchObjectsList)):
            self.SearObjectsList.destroy()
        self.SearchObjectsList.clear()

        self.MainSceneButtons()

    def ButtonSeoulInput(self):
        XmlProcess.SearchLegion = "1"
        self.SelectRocation = "(서울)"
        self.TurnToSearchScene()

    def ButtonBugyoungInput(self):
        XmlProcess.SearchLegion = "2"
        self.SelectRocation = "(부경)"
        self.TurnToSearchScene()

    def ButtonJejuInput(self):
        XmlProcess.SearchLegion = "3"
        self.SelectRocation = "(제주)"
        self.TurnToSearchScene()

    def ButtonGmailSend(self):
        global host, port
        MsgTopLevel = Toplevel(self.MainWnd)
        MsgTopLevel.geometry("320x200+820+100")
        MsgTopLevel.title("메일 보내기")

        html = ""

        self.MsgTitle = StringVar()

        self.recipientAddr = StringVar()
        self.msgtext = StringVar()

        Label(MsgTopLevel, text="제목 :").place(x=0, y=0)
        Entry(MsgTopLevel, textvariable=self.MsgTitle, width=20).place(x=40, y=0)

        Label(MsgTopLevel, text="받는이 :").place(x=0, y=20)
        Entry(MsgTopLevel, textvariable=self.recipientAddr, width=20).place(x=40, y=20)

        Label(MsgTopLevel, text="내용 :").place(x=0, y=40)
        Entry(MsgTopLevel, textvariable=self.msgtext, width=20).place(x=40, y=40)

        Button(MsgTopLevel, text="발송", command=self.ButtonSend).place(x=100, y=80)

    def ButtonSend(self):
        import mysmtplib

        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart('alternative')

        msg['Subject'] = self.MsgTitle.get()
        msg['From'] = self.senderAddress
        msg['To'] = self.recipientAddr.get()

        msgPart = MIMEText(self.msgtext.get(), 'plain')

        msg.attach(msgPart)

        s = mysmtplib.MySMTP(host, port)

        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(self.senderAddress, self.passwd)
        s.sendmail(self.senderAddress, [self.recipientAddr.get()], msg.as_string())
        s.close()

    def ButtonTelegramSend(self):
        pass


if __name__ == '__main__':
    MainGui()
