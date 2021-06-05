from tkinter import *
from tkcalendar import *
import webbrowser
import XmlProcess
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk
import pickle
import sys
from cefpython3 import cefpython as cef
from youtubesearchpython import *
from functools import partial

host = "smtp.gmail.com"
port = "587"
global HorseInfoForSave

def Button_Namuwiki_Link():
    webbrowser.open("https://namu.wiki/w/%EA%B2%BD%EB%A7%88")

class MainGui:
    def __init__(self):
        self.MainWnd = Tk()
        self.MainWnd.title("SafetyPlayGround")
        self.MainWnd.geometry("480x680+660+240")
        self.senderAddress = 'gksduddls33@gmail.com'
        self.passwd = 'brownie9065!@'

        self.MainWnd.resizable(False, False)

        self.MainObjectList = []
        self.SearchObjectsList = []
        self.RaceDateButtonList = []
        self.photoGmail = PhotoImage(file="Photo/Gmail_icon.png")
        self.photoTelegram = PhotoImage(file="Photo/Telegram_icon.png")
        self.photoNamuwiki = PhotoImage(file="Photo/Namuwiki_icon.png")
        self.photoWhiteStar = PhotoImage(file="Photo/book_mark_off.png")
        self.photoYellowStar = PhotoImage(file="Photo/book_mark_on.png")
        self.photoBack = PhotoImage(file="Photo/Back_icon.png")
        self.input_text = StringVar()
        self.ForRaceDateSelector = StringVar()
        self.FavList = []

        self.Datacanvas = None
        self.Graphcanvas = None
        self.SelectRocation = None
        self.MsgTitle = None
        self.recipientAddr = None
        self.msgtext = None

        self.HorsePicture = None

        self.MainSceneButtons()
        self.MainWnd.mainloop()

    def MainSceneButtons(self):
        self.MainObjectList.append(Button(self.MainWnd, text='서울', width=10, height=5, command=self.ButtonSeoulInput))
        self.MainObjectList.append(Button(self.MainWnd, text='부경', width=10, height=5, command=self.ButtonBugyoungInput))
        self.MainObjectList.append(Button(self.MainWnd, text='제주', width=10, height=5, command=self.ButtonJejuInput))

        self.MainObjectList.append(Button(self.MainWnd, image=self.photoGmail, borderwidth=0, command=self.ButtonGmailSend))
        self.MainObjectList.append(Button(self.MainWnd, image=self.photoTelegram, borderwidth=0, command=self.ButtonTelegramSend))
        self.MainObjectList.append(Button(self.MainWnd, image=self.photoNamuwiki, borderwidth=0, command=Button_Namuwiki_Link))

        self.MainScenePlace()

    def MainScenePlace(self):
        self.MainObjectList[0].place(x=200, y=50)
        self.MainObjectList[1].place(x=200, y=200)
        self.MainObjectList[2].place(x=200, y=350)
        self.MainObjectList[3].place(x=0, y=580)
        self.MainObjectList[4].place(x=380, y=580)
        self.MainObjectList[5].place(x=190, y=580)

    def SetSearchButtons(self):
        self.input_text.set("마명이나 원하는 경기 변호를 입력해주세요")
        self.ForRaceDateSelector.set("원하시면 경기 날짜 선택")
        self.SearchObjectsList.append(Entry(self.MainWnd, textvariable=self.input_text, width=40))  # 0
        self.SearchObjectsList.append(Button(self.MainWnd, text="검색", padx=12.5, command=self.SearchDef))  # 1
        self.SearchObjectsList.append(Button(self.MainWnd, text="불러오기", command=self.LoadDataDef))  # 2
        self.SearchObjectsList.append(Button(self.MainWnd, image=self.photoWhiteStar, command=self.Favorite, width=50, height=45))  # 북마크 3
        self.SearchObjectsList.append(Button(self.MainWnd, image=self.photoBack, command=self.TurnToMainScene, width=50, height=45))  # 뒤로가기 4
        self.SearchObjectsList.append(Button(self.MainWnd, textvariable=self.ForRaceDateSelector, width=40, height=1, command=self.RaceDateSelector)) # 달력 5
        self.Datacanvas = Canvas(self.MainWnd, bg='white', width=150, height=300)
        self.Graphcanvas = Canvas(self.MainWnd, bg='white', width=450, height=270)

        self.SearchObjectsPlace()

    def SearchObjectsPlace(self):
        self.SearchObjectsList[0].place(x=0, y=40)
        self.SearchObjectsList[1].place(x=300, y=10)
        self.SearchObjectsList[2].place(x=300, y=35)
        self.SearchObjectsList[3].place(x=360, y=10)
        self.SearchObjectsList[4].place(x=420, y=10)
        self.SearchObjectsList[5].place(x=0, y=10)
        self.Datacanvas.place(x=10, y=90)
        self.Graphcanvas.place(x=10, y=400)

    def RaceDateSelector(self):
        topWnd = Toplevel(self.MainWnd)
        topWnd.geometry("320x200+820+100")
        cal = Calendar(topWnd, selectmode="day", year=2021, month=6)
        cal.pack()
        button = Button(topWnd, text="선택 완료", command=partial(self.GetDate, cal, topWnd))
        button.pack()

        topWnd.title("경기 날짜 선택택")

    def GetDate(self, cal, topWnd):
        temp = cal.get_date().split('/')
        if len(temp[0]) == 1:
            temp[0] = "0"+temp[0]
        self.ForRaceDateSelector.set("20"+temp[2]+temp[0]+temp[1])
        topWnd.destroy()

    def LoadDataDef(self):
        try:
            with open('bookmark', 'rb') as f:
                self.FavList = pickle.load(f)
                print("성공")
        except:
            print("실패")
            pass

    def Favorite(self):
        self.SearchObjectsList[3].destroy()
        global HorseInfoForSave
        if HorseInfoForSave in self.FavList:
            self.SearchObjectsList[3] = Button(self.MainWnd, image=self.photoWhiteStar, command=self.Favorite, width=50, height=50)
            self.FavList.remove(HorseInfoForSave)
        else:
            self.SearchObjectsList[3] = Button(self.MainWnd, image=self.photoYellowStar, command=self.Favorite, width=50, height=50)
            self.FavList.append(HorseInfoForSave)
        with open('bookmark', 'wb') as f:
            pickle.dump(self.FavList, f)
        self.SearchObjectsList[3].place(x=360, y=10)

    def ShowRaceVideo(self, RaceDate, RaceRound):
        keyword = self.SelectRocation + " 20" + RaceDate + " " + RaceRound + "경주"
        videoSearch = VideosSearch(keyword, limit=10)

        result = videoSearch.result()

        sys.excepthook = cef.ExceptHook
        cef.Initialize()
        cef.CreateBrowserSync(url=result['result'][0]['link'], window_title="경마 시청")
        cef.MessageLoop()

    def SearchDef(self):
        ReturnResult = XmlProcess.SearchHorseProfile(self.input_text.get())
        HorseInfo = ReturnResult[0]
        HorseRaceDate = ReturnResult[1][0]
        HorseRaceRound = ReturnResult[1][1]
        HorseRaceRank = ReturnResult[1][2]
        global HorseInfoForSave
        HorseInfoForSave = HorseInfo

        self.PrintHorseInfo(HorseInfo)
        self.PrintHorsePicture(HorseInfo[3])
        self.PrintBarChart(HorseRaceDate, HorseRaceRound, HorseRaceRank)
        self.input_text.set("")

    def PrintHorseInfo(self, HorseInfo):
        self.Datacanvas.delete("all")
        self.Datacanvas.create_text(10,  15, text="생년월일:" + HorseInfo[0], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10,  30, text="통산착순상금:" + HorseInfo[1], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10,  45, text="이름:" + HorseInfo[2], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10,  60, text="마번:" + HorseInfo[3], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10,  75, text="출생지:" + HorseInfo[4], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10,  90, text="등급:" + HorseInfo[5], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 105, text="레이팅:" + HorseInfo[6], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 120, text="1년1착횟수:" + HorseInfo[7], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 135, text="2년1착횟수:" + HorseInfo[8], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 150, text="3년1착횟수:" + HorseInfo[9], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 165, text="성별:" + HorseInfo[10], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 180, text="조교사:" + HorseInfo[11], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 195, text="조교사번호:" + HorseInfo[12], justify=LEFT, anchor=W)

    def PrintHorsePicture(self, HorseNum):
        if self.HorsePicture is not None:
            self.HorsePicture.destroy()

        urlFirst = 'https://studbook.kra.co.kr/h_photo/'
        url = urlFirst + HorseNum[:3] + '/' + HorseNum + '-l.jpg'

        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        im = im.resize((300, 300))
        image = ImageTk.PhotoImage(im)

        self.HorsePicture = Label(self.MainWnd, image=image)
        self.HorsePicture.image = image
        self.HorsePicture.place(x=170, y=90)

    def PrintBarChart(self, RaceDate, RaceRound, RaceRank):
        y_stretch = 15
        y_gap = 20
        x_stretch = 50
        x_width = 30
        x_gap = 40
        cnt = 0
        self.Graphcanvas.delete("all")
        for i in range(len(self.RaceDateButtonList)):
            self.RaceDateButtonList[i].destroy()
        self.RaceDateButtonList.clear()
        for i in RaceRank:
            if cnt > 4:
                break
            x0 = cnt * x_stretch + cnt * x_width + x_gap
            y0 = 270 - ((15 - i) * y_stretch + y_gap)
            x1 = cnt * x_stretch + cnt * x_width + x_width + x_gap
            y1 = 270 - y_gap
            self.Graphcanvas.create_rectangle(x0, y0, x1, y1, fill="#020721", outline='yellow')
            self.Graphcanvas.create_text(x0 + 7, y0, anchor=SW, text=str(i)+"등")
            self.RaceDateButtonList.append(Button(self.MainWnd, text=RaceDate[cnt], borderwidth=0, background='white', command=partial(self.ShowRaceVideo, RaceDate[cnt], RaceRound[cnt])))
            self.RaceDateButtonList[cnt].place(x=x0-2, y=y1+400)
            cnt += 1

    def TurnToSearchScene(self):
        for i in range(len(self.MainObjectList)):
            self.MainObjectList[i].destroy()
        self.MainObjectList.clear()

        self.SetSearchButtons()

    def TurnToMainScene(self):
        for i in range(len(self.SearchObjectsList)):
            self.SearchObjectsList[i].destroy()
        self.SearchObjectsList.clear()
        self.Graphcanvas.destroy()
        self.Datacanvas.destroy()

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

        # html = ""

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
