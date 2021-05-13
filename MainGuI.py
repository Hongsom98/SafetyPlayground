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

        self.Button_Seoul.place(x=200, y=50)
        self.Button_Bugyoung.place(x=200, y=200)
        self.Button_Jeju.place(x=200, y=350)

        self.MainWnd.mainloop()

    def Button_Seoul_Input(self):
        self.Button_Seoul.destroy()
        self.Button_Bugyoung.destroy()
        self.Button_Jeju.destroy()

        self.TurnToSearchScene()

    def Button_Bugyoung_Input(self):
        self.Button_Seoul.destroy()
        self.Button_Bugyoung.destroy()
        self.Button_Jeju.destroy()

        self.TurnToSearchScene()

    def Button_Jeju_Input(self):
        self.Button_Seoul.destroy()
        self.Button_Bugyoung.destroy()
        self.Button_Jeju.destroy()

        self.TurnToSearchScene()

    def TurnToSearchScene(self):
        pass

    def TurnToMainScene(self):
        pass

if __name__ == '__main__':
    MainGui()
