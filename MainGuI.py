import traceback
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
import Gif
import telepot
from telegram.ext import Updater
from telegram.ext import CommandHandler
import os

# -*- coding:utf-8 -*-

host = "smtp.gmail.com"
port = "587"
HorseInfoForSave = None


def Button_Namuwiki_Link():
    webbrowser.open("https://namu.wiki/w/%EA%B2%BD%EB%A7%88")


def FindLuckyNumIndexes(PredictResult):
    temp = PredictResult
    returnlist = []
    for i in range(4):
        returnlist.append(temp.index(max(temp)))
        del temp[temp.index(max(temp))]
    return list(set(returnlist))

class MainGui:
    def __init__(self):
        self.MainWnd = Tk()
        self.MainWnd.title("SafetyPlayGround")
        self.MainWnd.geometry("480x815+660+240")
        self.MainWnd.configure(bg="RoyalBlue4")
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
        self.photoTitle = PhotoImage(file="Photo/dae mun.png")
        self.photoBack = PhotoImage(file="Photo/Back_icon.png")
        self.photoPredict = PhotoImage(file="Photo/predict.png")
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
        self.nHorseList = None
        self.nHorseButtons = []

        self.MainSceneButtons()
        self.MainWnd.mainloop()

    def MainSceneButtons(self):
        self.MainObjectList.append(Button(self.MainWnd, text='서울', width=10, height=5, command=self.ButtonSeoulInput))
        self.MainObjectList.append(Button(self.MainWnd, text='부경', width=10, height=5, command=self.ButtonBugyoungInput))
        self.MainObjectList.append(Button(self.MainWnd, text='제주', width=10, height=5, command=self.ButtonJejuInput))

        self.MainObjectList.append(Button(self.MainWnd, image=self.photoGmail, borderwidth=0, command=self.ButtonGmailSend))
        self.MainObjectList.append(Button(self.MainWnd, image=self.photoTelegram, borderwidth=0, command=self.ButtonTelegramSend))
        self.MainObjectList.append(Button(self.MainWnd, image=self.photoNamuwiki, borderwidth=0, command=Button_Namuwiki_Link))
        self.MainObjectList.append(Label(self.MainWnd, image=self.photoTitle, borderwidth=0))
        self.MainObjectList.append(Button(self.MainWnd, image=self.photoPredict, borderwidth=0, command=self.ButtonPredict))
        self.lbl = Gif.ImageLabel(self.MainWnd)
        self.lbl.load('Photo/Hani.gif')
        self.lbr = Gif.ImageLabel(self.MainWnd)
        self.lbr.load('Photo/horseRight.gif')
        self.MainScenePlace()

    def MainScenePlace(self):
        self.MainObjectList[0].place(x=30, y=210)
        self.MainObjectList[1].place(x=200, y=210)
        self.MainObjectList[2].place(x=380, y=210)
        self.MainObjectList[3].place(x=0, y=580)
        self.MainObjectList[4].place(x=380, y=580)
        self.MainObjectList[5].place(x=190, y=580)
        self.MainObjectList[6].place(x=0, y=0)
        self.MainObjectList[7].place(x=160, y=350)
        self.lbl.place(x=0, y=680)
        self.lbr.place(x=240, y=680)

    def SetSearchButtons(self):
        self.input_text.set("마명이나 원하는 경기 변호를 입력해주세요")
        self.ForRaceDateSelector.set("원하시면 경기 날짜 선택")
        self.SearchObjectsList.append(Entry(self.MainWnd, textvariable=self.input_text, width=40))  # 0
        self.SearchObjectsList.append(Button(self.MainWnd, text="검색", padx=12.5, command=partial(self.SearchDef, self.input_text.get(), "Search")))  # 1
        self.SearchObjectsList.append(Button(self.MainWnd, text="불러오기", command=self.LoadDataDef))  # 2
        self.SearchObjectsList.append(Button(self.MainWnd, image=self.photoWhiteStar, command=self.Favorite, width=50, height=45))  # 북마크 3
        self.SearchObjectsList.append(Button(self.MainWnd, image=self.photoBack, command=self.TurnToMainScene, width=50, height=45))  # 뒤로가기 4
        self.SearchObjectsList.append(Button(self.MainWnd, textvariable=self.ForRaceDateSelector, width=40, height=1, command=self.RaceDateSelector))  # 달력 5
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

        topWnd.title("경기 날짜 선택")

    def GetDate(self, cal, topWnd):
        temp = cal.get_date().split('/')
        if len(temp[0]) == 1:
            temp[0] = "0" + temp[0]
        if len(temp[1]) == 1:
            temp[1] = "0" + temp[1]
        self.ForRaceDateSelector.set("20" + temp[2] + temp[0] + temp[1])
        temp = XmlProcess.DoSearchWithRaceRound(self.ForRaceDateSelector.get())

        self.input_text.set(self.ForRaceDateSelector.get() + "에는 1~" + str(temp) + "경기가 있습니다")
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
        global HorseInfoForSave
        if HorseInfoForSave is None:
            return

        self.SearchObjectsList[3].destroy()
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

    def SearchDef(self, InputValue, InputType):
        global HorseInfoForSave
        if InputType == "Search":
            if self.input_text.get().isalpha():
                ReturnResult = XmlProcess.SearchHorseProfile(self.input_text.get())
                HorseInfo = ReturnResult[0]
                HorseRaceDate = ReturnResult[1][0]
                HorseRaceRound = ReturnResult[1][1]
                HorseRaceRank = ReturnResult[1][2]
                HorseInfoForSave = HorseInfo

                self.SearchObjectsList[3].destroy()
                if HorseInfoForSave in self.FavList:
                    self.SearchObjectsList[3] = Button(self.MainWnd, image=self.photoYellowStar, command=self.Favorite, width=50, height=50)
                else:
                    self.SearchObjectsList[3] = Button(self.MainWnd, image=self.photoWhiteStar, command=self.Favorite, width=50, height=50)
                self.SearchObjectsList[3].place(x=360, y=10)

                self.PrintHorseInfo(HorseInfo)
                self.PrintHorsePicture(HorseInfo[3])
                self.PrintBarChart(HorseRaceDate, HorseRaceRound, HorseRaceRank)
                self.input_text.set("")
            else:
                self.Datacanvas.delete("all")
                self.Graphcanvas.delete("all")
                if self.HorsePicture is not None:
                    self.HorsePicture.destroy()
                for i in range(len(self.nHorseButtons)):
                    self.nHorseButtons[i].destroy()
                self.nHorseButtons.clear()
                self.nHorseList = XmlProcess.MakeNHorseList(self.ForRaceDateSelector.get(), self.input_text.get())
                for i in range(len(self.nHorseList)):
                    self.nHorseButtons.append(
                        Button(self.MainWnd, text=str(i + 1) + '번 경주마', padx=10, width=15, borderwidth=0, background='white', command=partial(self.SearchDef, self.nHorseList[i], "nHorse")))
                    self.nHorseButtons[i].place(x=10, y=90 + i * 20)
        else:
            for i in range(len(self.nHorseButtons)):
                self.nHorseButtons[i].place(x=-200, y=90 + i * 20)
            self.nHorseButtons.append(Button(self.MainWnd, text="뒤로가기", command=self.BackNHorseList, borderwidth=0, background='white'))
            self.nHorseButtons[-1].place(x=20, y=340)
            ReturnResult = XmlProcess.SearchHorseProfile(InputValue)
            HorseInfo = ReturnResult[0]
            HorseRaceDate = ReturnResult[1][0]
            HorseRaceRound = ReturnResult[1][1]
            HorseRaceRank = ReturnResult[1][2]
            HorseInfoForSave = HorseInfo

            self.PrintHorseInfo(HorseInfo)
            self.PrintHorsePicture(HorseInfo[3])
            self.PrintBarChart(HorseRaceDate, HorseRaceRound, HorseRaceRank)
            self.input_text.set("")

    def BackNHorseList(self):
        self.Datacanvas.delete("all")
        if self.HorsePicture is not None:
            self.HorsePicture.destroy()
        self.Graphcanvas.delete("all")
        for i in range(len(self.RaceDateButtonList)):
            self.RaceDateButtonList[i].destroy()
        self.RaceDateButtonList.clear()
        for i in range(len(self.nHorseList)):
            self.nHorseButtons[i].place(x=10, y=90 + i * 20)
        self.nHorseButtons[-1].destroy()
        del self.nHorseButtons[-1]

    def PrintHorseInfo(self, HorseInfo):
        self.Datacanvas.delete("all")
        self.Datacanvas.create_text(10, 15, text="생년월일:" + HorseInfo[0], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 30, text="통산착순상금:" + HorseInfo[1], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 45, text="이름:" + HorseInfo[2], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 60, text="마번:" + HorseInfo[3], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 75, text="출생지:" + HorseInfo[4], justify=LEFT, anchor=W)
        self.Datacanvas.create_text(10, 90, text="등급:" + HorseInfo[5], justify=LEFT, anchor=W)
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

        try:
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
        except:
            with urllib.request.urlopen("https://studbook.kra.co.kr/servlet/ImageResizer?file=/h_photo/040/040827-l.JPG&width=210&height=142") as u:
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
        self.Graphcanvas.delete("all")
        for i in range(len(self.RaceDateButtonList)):
            self.RaceDateButtonList[i].destroy()
        self.RaceDateButtonList.clear()
        for x, i in enumerate(RaceRank):
            if x > 4:
                break
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = 270 - ((15 - i) * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = 270 - y_gap
            self.Graphcanvas.create_rectangle(x0, y0, x1, y1, fill="#020721", outline='yellow')
            self.Graphcanvas.create_text(x0 + 7, y0, anchor=SW, text=str(i) + "등")
            self.RaceDateButtonList.append(Button(self.MainWnd, text=RaceDate[x], borderwidth=0, background='white', command=partial(self.ShowRaceVideo, RaceDate[x], RaceRound[x])))
            self.RaceDateButtonList[x].place(x=x0 - 2, y=y1 + 400)

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
        MsgTopLevel.geometry("200x100")
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
        chkBox = IntVar()
        Checkbutton(MsgTopLevel, text="예측 보내기", variable=chkBox).place(x=00, y=60)
        Button(MsgTopLevel, text="발송", command=partial(self.ButtonSend, MsgTopLevel, chkBox)).place(x=150, y=60)

    def ButtonSend(self, TopLv, chkBox):
        import mysmtplib

        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart('alternative')

        msg['Subject'] = self.MsgTitle.get()
        msg['From'] = self.senderAddress
        msg['To'] = self.recipientAddr.get()

        msgPart = MIMEText(self.msgtext.get(), 'plain')
        msg.attach(msgPart)

        if chkBox:
            infile = open("LuckyNums.txt", "r", encoding='cp949')
            SndTXT = infile.read()
            msgPredict = MIMEText(SndTXT, 'plain')
            msg.attach(msgPredict)

        s = mysmtplib.MySMTP(host, port)

        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(self.senderAddress, self.passwd)
        s.sendmail(self.senderAddress, [self.recipientAddr.get()], msg.as_string())
        s.close()
        TopLv.destroy()

    def ButtonTelegramSend(self):

        bot = telepot.Bot('1834221680:AAGmsL3Wb3uYq2jGPY2tLGXDbKR22_R8OfU')
        updater = Updater('1834221680:AAGmsL3Wb3uYq2jGPY2tLGXDbKR22_R8OfU')


        def sendMessage(user, msg):
            try:
                bot.sendMessage(user, msg)
            except:
                traceback.print_exc(file=sys.stdout)

        def send_Predict(user):
            infile = open("LuckyNums.txt", "r", encoding='cp949')
            if infile == None:
                self.ButtonPredict()
                infile = open("LuckyNums.txt", "r", encoding='cp949')
            SndTXT = infile.read()
            sendMessage(user, SndTXT)
            os.remove("LuckyNums.txt")

        def handle(msg):
            content_type, chat_type, user = telepot.glance(msg)
            if content_type != 'text':
                sendMessage(user, '난 텍스트 이외의 메시지는 처리하지 못해요.')
                return
            text = msg['text']
            args = text.split(' ')

            if text.startswith('경마') and len(args) > 1:
                region = args[1]
                data = str(args[2])
                HorseInfo = XmlProcess.SearchHorseProfile(data, region)
                msgInfo = "생년월일:" + HorseInfo[0][0] + "\n통산착순상금:" + HorseInfo[0][1] + "\n이름:" + HorseInfo[0][2] + \
                          "\n마번:" + HorseInfo[0][3] + "\n출생지:" + HorseInfo[0][4] + "\n등급:" + HorseInfo[0][5] + \
                          "\n레이팅:" + HorseInfo[0][6] + "\n1년1착횟수:" + HorseInfo[0][7] + "\n2년1착횟수:" + HorseInfo[0][8] + \
                          "\n3년1착횟수:" + HorseInfo[0][9] + "\n성별:" + HorseInfo[0][10] + "\n조교사:" + \
                          HorseInfo[0][11] + "\n조교사번호:" + HorseInfo[0][12]
                sendMessage(user, msgInfo)

            elif text.startswith('즐찾'):
                with open('bookmark', 'rb') as f:
                    lst = pickle.load(f)

                for i in lst:
                    msg = "생년월일:" + i[0] + "\n통산착순상금:" + i[1] + "\n이름:" + i[2] + \
                          "\n마번:" + i[3] + "\n출생지:" + i[4] + "\n등급:" + i[5] + \
                          "\n레이팅:" + i[6] + "\n1년1착횟수:" + i[7] + "\n2년1착횟수:" + i[8] + \
                          "\n3년1착횟수:" + i[9] + "\n성별:" + i[10] + "\n조교사:" + \
                          i[11] + "\n조교사번호:" + i[12]
                    sendMessage(user, msg)
            elif text.startswith('예측'):
                send_Predict(user)
            elif text.startswith('하이'):
                msg = '안녕하세요 영인이네 안전놀이터입니다\n'
                msg += '''경기 일★정 조회

                §§경주마 정보/성적 조회§§

                ♜경기 영상 링크♜

                관심 경주마 저장/관련 정보 연동

                ※다음 경기 예측 무료 제공￥
                '''
                sendMessage(user,msg)
            else:
                sendMessage(user, '모르는 명령어입니다.\n 마명 [장소] [말이름], 예측,즐찾 중 하나의 명령어를 입력하세요')

        bot.message_loop(handle)

    def ButtonPredict(self):
        Result = XmlProcess.TakeListToPredict()
        PredictDate = XmlProcess.ForPredictDate()
        PredictRounds = XmlProcess.TakeRounds(PredictDate)
        NumList = Result[0]
        PredictResult = Result[1]

        for i in range(len(NumList)):
            NumList[i] = int(NumList[i][0])

        idx_list = [idx for idx, val in enumerate(NumList) if val == 1]
        size = len(NumList)
        res = [NumList[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[-1] != size else []))]
        del res[0]

        res2 = []
        for i in res:
            res2.append(PredictResult[0:len(i)])
            del PredictResult[0:len(i)]

        topWnd = Toplevel(self.MainWnd)
        topWnd.geometry("320x350+720+450")

        ForSave = []
        for i in range(len(PredictRounds)):
            Label(topWnd, text=str(PredictDate[0:4]) + "년 " + str(PredictDate[4:6]) + "월 " + str(PredictDate[6:]) + "일 제" + str(PredictRounds[i]) + "경기의 행운의 숫자는").pack()
            indexes = FindLuckyNumIndexes(res2[i])
            luckynums = ""
            for j in indexes:
                luckynums += str(res[0][j]) + " "
            Label(topWnd, text=luckynums + '\n').pack()
            ForSave.append([str(str(PredictDate[0:4]) + "년 " + str(PredictDate[4:6]) + "월 " + str(PredictDate[6:]) + "일 제" + str(PredictRounds[i]) + "경기의 행운의 숫자는"), luckynums])

        topWnd.title("예측 결과")

        with open('LuckyNums.txt', 'w') as f:
            for item in ForSave:
                for i in item:
                    f.write(i + "\n")


if __name__ == '__main__':
    MainGui()
