import threading
from tkinter import *
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

host = "smtp.gmail.com"
port = "587"

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
        self.input_round = None
        self.HorsePicture = None

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
        self.input_date = StringVar()  # 경기날짜 입력
        self.input_round = StringVar()  # 경기라운드 입력

        self.SearchObjectsList.append(Entry(self.MainWnd, textvariable=self.input_text, width=30))  # 0
        self.SearchObjectsList.append(Button(self.MainWnd, text="검색", command=self.SearchDef))  # 1
        self.SearchObjectsList.append(Button(self.MainWnd, text="불러오기", command=self.LoadDataDef))  # 2
        self.SearchObjectsList.append(Entry(self.MainWnd, textvariable=self.input_date, width=20))  # 날짜 3
        self.SearchObjectsList.append(Label(self.MainWnd, text="날짜"))  # 4
        self.SearchObjectsList.append(Entry(self.MainWnd, textvariable=self.input_round, width=20))  # 라운드 5
        self.SearchObjectsList.append(Label(self.MainWnd, text="라운드"))  # 6
        self.SearchObjectsList.append(Button(self.MainWnd, text="검색", command=self.ShowRaceVideo))  # 검색 7
        self.SearchObjectsList.append(Button(self.MainWnd, text="다음 경기 예측하기", command=self.PredictNextRace, width=64, height=3))  # 예측 8
        self.SearchObjectsList.append(Button(self.MainWnd, image=self.photoWhiteStar, command=self.Favorite, width=50, height=50))  # 북마크 9
        self.Datacanvas = Canvas(self.MainWnd, bg='white', width=150, height=300)
        self.Graphcanvas = Canvas(self.MainWnd, bg='white', width=450, height=170)

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
        self.Datacanvas.place(x=10, y=90)
        self.Graphcanvas.place(x=10, y=465)

    def LoadDataDef(self):
        try:
            with open('bookmark', 'rb') as f:
                self.FavList = pickle.load(f)
                print("성공")
        except:
            print("실패")
            pass

    def Favorite(self):
        self.SearchObjectsList[9] = Button(self.MainWnd, image=self.photoYellowStar, command=self.Favorite, width=50, height=50)
        Result = XmlProcess.SearchHorseProfile(self.input_text.get())
        self.FavList.append(Result)
        with open('bookmark', 'wb') as f:
            pickle.dump(Result, f)

    def PredictNextRace(self):
        topWnd = Toplevel(self.MainWnd)
        topWnd.geometry("320x200+820+100")

        topWnd.title("경기 예측 결과")

    def ShowRaceVideo(self):
        keyword = self.SelectRocation + " " + self.input_date.get() + " " + self.input_round.get() + "경주"
        videoSearch = VideosSearch(keyword, limit=10)

        result = videoSearch.result()

        sys.excepthook = cef.ExceptHook
        cef.Initialize()
        cef.CreateBrowserSync(url=result['result'][0]['link'], window_title="경마 시청")
        cef.MessageLoop()

    def SearchDef(self):
        self.Datacanvas.delete('data')
        if self.HorsePicture is not None:
            self.HorsePicture.destroy()
        ReturnResult = XmlProcess.SearchHorseProfile(self.input_text.get())
        HorseInfo = ReturnResult[0]
        HorseRaceDate = ReturnResult[1][0]
        HorseRaceRank = ReturnResult[1][1]

        self.PrintHorseInfo(HorseInfo)
        self.PrintHorsePicture(HorseInfo[3])

    def PrintHorseInfo(self, HorseInfo):
        self.Datacanvas.create_text(10,  15, text="생년월일:" + HorseInfo[0], tags='data', justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10,  30, text="통산착순상금:" + HorseInfo[1], tags='data', justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10,  45, text="이름:" + HorseInfo[2], tags='data', justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10,  60, text="마번:" + HorseInfo[3], tags='data', justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10,  75, text="출생지:" + HorseInfo[4], tags='data', justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10,  90, text="등급:" + HorseInfo[5], tags='data', justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 105, text="레이팅:" + HorseInfo[6], tags='data', justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 120, text="1년1착횟수:" + HorseInfo[7], tags='data', justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 135, text="2년1착횟수:" + HorseInfo[8], tags='data', justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 150, text="3년1착횟수:" + HorseInfo[9], tags='data', justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 165, text="성별:" + HorseInfo[10], tags='data', justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 180, text="조교사:" + HorseInfo[11], tags='data', justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 195, text="조교사번호:" + HorseInfo[12], tags='data', justify=LEFT, anchor=W)

    def PrintHorsePicture(self, HorseNum):
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

    def PrintBarChart(self, RaceDate, RaceRank):
        pass
    
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
