from tkinter import *

class MainGui:
    def __init__(self):
        self.MainWnd = Tk()
        self.MainWnd.title("SafetyPlayGround")
        self.MainWnd.geometry("480x680+660+240")
        self.MainWnd.resizable(False, False)

        self.Button_Seoul    = Button(self.MainWnd, text='서울', width=10, height=5, command=self.Button_Seoul_Input)
        self.Button_Bugyoung = Button(self.MainWnd, text='부경', width=10, height=5, command=self.Button_Bugyoung_Input)
        self.Button_Jeju     = Button(self.MainWnd, text='제주', width=10, height=5, command=self.Button_Jeju_Input)

        self.photoGmail = PhotoImage(file="Photo/Gmail_icon.png")
        self.Button_Gmail = Button(self.MainWnd, image=self.photoGmail, command=self.Button_Gmail_Send)
        self.photoTelegram = PhotoImage(file="Photo/Telegram_icon.png")
        self.Button_Telegram = Button(self.MainWnd, image=self.photoTelegram, command=self.Button_Telegram_Send)
        self.photoNamuwiki = PhotoImage(file="Photo/Namuwiki_icon.png")
        self.Button_Namuwiki = Button(self.MainWnd, image=self.photoNamuwiki, command=self.Button_Namuwiki_Link)

        self.Button_Seoul.place(x=200, y=50)
        self.Button_Bugyoung.place(x=200, y=200)
        self.Button_Jeju.place(x=200, y=350)
        self.Button_Gmail.place(x=0, y=580)
        self.Button_Telegram.place(x=380, y=580)
        self.Button_Namuwiki.place(x=190, y=580)
        self.MainWnd.mainloop()

    def Button_Seoul_Input(self):
        self.Button_Seoul.destroy()
        self.Button_Bugyoung.destroy()
        self.Button_Jeju.destroy()
        self.Button_Gmail.destroy()
        self.Button_Telegram.destroy()
        self.Button_Namuwiki.destroy()

        self.TurnToSearchScene()

    def Button_Bugyoung_Input(self):
        self.Button_Seoul.destroy()
        self.Button_Bugyoung.destroy()
        self.Button_Jeju.destroy()
        self.Button_Gmail.destroy()
        self.Button_Telegram.destroy()
        self.Button_Namuwiki.destroy()

        self.TurnToSearchScene()

    def Button_Jeju_Input(self):
        self.Button_Seoul.destroy()
        self.Button_Bugyoung.destroy()
        self.Button_Jeju.destroy()
        self.Button_Gmail.destroy()
        self.Button_Telegram.destroy()
        self.Button_Namuwiki.destroy()

        self.TurnToSearchScene()

    def Button_Gmail_Send(self):
        pass

    def Button_Telegram_Send(self):
        pass

    def Button_Namuwiki_Link(self):
        pass

    def TurnToSearchScene(self):
        pass

    def TurnToMainScene(self):
        pass

if __name__ == '__main__':
    MainGui()
