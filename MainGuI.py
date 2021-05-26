from tkinter import *
import webbrowser
import XmlProcess

from io import BytesIO
import urllib
import urllib.request
from PIL import Image,ImageTk


host = "smtp.gmail.com"  # Gmail SMTP 서버 주소.
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

        self.input_text = None
        self.input_date = None
        self.MainSceneButtons()

        self.Datacanvas = None
        self.Graphcanvas = None

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
        self.SearchObjectsList.append(Entry(self.MainWnd, textvariable=self.input_text, width=30))
        self.SearchObjectsList.append(Button(self.MainWnd, text="검색", command=self.SearchDef))
        self.SearchObjectsList.append(Button(self.MainWnd, text="불러오기", command=self.LoadDataDef))

        self.input_date = StringVar()  # 경기날짜 입력
        self.input_round = StringVar()  # 경기라운드 입력
        self.SearchObjectsList.append(Entry(self.MainWnd, textvariable=self.input_date, width=20))
        self.SearchObjectsList.append(Label(self.MainWnd, text="날짜"))
        self.SearchObjectsList.append(Entry(self.MainWnd, textvariable=self.input_round, width=20))
        self.SearchObjectsList.append(Label(self.MainWnd, text="라운드"))
        self.SearchObjectsList.append(Button(self.MainWnd, text="검색", command=self.SearchDateDef))

        self.SearchObjectsList.append(Button(self.MainWnd, text="다음 경기 예측하기", command=self.TenserFlow, width=64, height=3))

        # self.SearchObjectsList.append(Canvas(self.MainWnd,bg='white',width=400,height=300))
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

        self.Datacanvas.place(x=10, y=90)
        self.Graphcanvas.place(x=10, y=465)

    def LoadDataDef(self):
        pass

    def TenserFlow(self):
        topWnd = Toplevel(self.MainWnd)
        topWnd.geometry("320x200+820+100")

        topWnd.title("경기 예측 결과")

        pass

    def SearchDateDef(self):
        self.VideoOpen = "http://kra.fiveplayer.co.kr/player.php?f=" + self.input_date.get() + "/s" + self.input_round.get() + "r"
        from selenium import webdriver
        driver = webdriver.Chrome('chromedriver.exe')
        driver.implicitly_wait(3)
        driver.get(self.VideoOpen)
        pass

    def SearchDef(self):
        self.Datacanvas.delete('data')
        Result = XmlProcess.SearchHorseProfile(self.input_text.get())
        x = 10
        y = 15

        for key, value in Result.items():
            self.Datacanvas.create_text(x, y, text=key + ":" + value, tags='data', justify=LEFT, anchor = W)
            if key == "hrNo":
                self.HrNo = value
                print(self.HrNo)
            y = y + 15
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
        # webbrowser.open(url)

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

        self.TurnToSearchScene()

    def ButtonBugyoungInput(self):
        XmlProcess.SearchLegion = "2"

        self.TurnToSearchScene()

    def ButtonJejuInput(self):
        XmlProcess.SearchLegion = "3"

        self.TurnToSearchScene()

    def ButtonGmailSend(self):
        global host, port
        MsgTopLevel = Toplevel(self.MainWnd)
        MsgTopLevel.geometry("320x200+820+100")
        MsgTopLevel.title("메일 보내기")

        html = ""

        self.MsgTitle = StringVar()
        # MsgTitle = str(input('제목 :'))

        self.recipientAddr = StringVar()
        # recipientAddr = str(input('보낼 대상의 이메일을 입력하세요 :'))
        self.msgtext = StringVar()
        # msgtext = str(input('내용 :'))

        Label(MsgTopLevel, text="제목 :").place(x=0, y=0)
        Entry(MsgTopLevel, textvariable=self.MsgTitle, width=20).place(x=40, y=0)

        Label(MsgTopLevel, text="받는이 :").place(x=0, y=20)
        Entry(MsgTopLevel, textvariable=self.recipientAddr, width=20).place(x=40, y=20)

        Label(MsgTopLevel, text="내용 :").place(x=0, y=40)
        Entry(MsgTopLevel, textvariable=self.msgtext, width=20).place(x=40, y=40)

        Button(MsgTopLevel, text="발송", command=self.ButtonSend).place(x=100, y=80)
        # SearchObjectsList.append(Button(MsgTopLevel, text="검색", command=self.SearchDateDef))

    def ButtonSend(self):
        import mysmtplib

        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart('alternative')

        msg['Subject'] = self.MsgTitle.get()
        msg['From'] = self.senderAddress
        msg['To'] = self.recipientAddr.get()

        msgPart = MIMEText(self.msgtext.get(), 'plain')
        # bookPart = MIMEText(html, 'html', _charset='UTF-8')

        msg.attach(msgPart)

        # print("connect smtp server ... ")
        s = mysmtplib.MySMTP(host, port)

        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(self.senderAddress, self.passwd)
        s.sendmail(self.senderAddress, [self.recipientAddr.get()], msg.as_string())
        s.close()

        # print("Mail sending complete!!!")
        pass

    def ButtonTelegramSend(self):
        pass


if __name__ == '__main__':
    MainGui()
