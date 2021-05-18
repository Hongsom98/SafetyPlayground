from tkinter import *
import webbrowser
import XmlProcess


def Button_Namuwiki_Link():
    webbrowser.open("https://namu.wiki/w/%EA%B2%BD%EB%A7%88")


class MainGui:
    def __init__(self):
        self.MainWnd = Tk()
        self.MainWnd.title("SafetyPlayGround")
        self.MainWnd.geometry("480x680+660+240")
        self.MainWnd.resizable(False, False)

        self.MainWnd_Button_List = []
        self.SearchObjectsList = []

        self.photoGmail = PhotoImage(file="Photo/Gmail_icon.png")
        self.photoTelegram = PhotoImage(file="Photo/Telegram_icon.png")
        self.photoNamuwiki = PhotoImage(file="Photo/Namuwiki_icon.png")

        self.input_text = None

        self.MainSceneButtons()

        self.MainWnd.mainloop()

    def MainSceneButtons(self):

        self.MainWnd_Button_List.append(
            Button(self.MainWnd, text='서울', width=10, height=5, command=self.ButtonSeoulInput))
        self.MainWnd_Button_List.append(
            Button(self.MainWnd, text='부경', width=10, height=5, command=self.ButtonBugyoungInput))
        self.MainWnd_Button_List.append(
            Button(self.MainWnd, text='제주', width=10, height=5, command=self.ButtonJejuInput))

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
        self.input_text = StringVar()
        self.SearchObjectsList.append(Entry(self.MainWnd, textvariable=self.input_text, width=30))

        self.SearchObjectsList.append(Button(self.MainWnd, text="검색", command=self.SearchDef))

        self.SearchObjectsPlace()

    def SearchObjectsPlace(self):
        self.SearchObjectsList[0].place(x=0, y=110)
        self.SearchObjectsList[1].place(x=250, y=110)

    def SearchDef(self):
        Result = XmlProcess.SearchHorseProfile(self.input_text.get())
        for key, value in Result.items():
            print(key, ":", value)


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
        pass

    def ButtonTelegramSend(self):
        pass



if __name__ == '__main__':
    MainGui()
