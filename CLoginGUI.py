import tkinter as tk
from tkinter import *
from CClient_Main_GUI import *

BTN_IMAGE = "./Images/GUI - button small.png"
BG_IMAGE = "./Images/GUI - BG Login.png"
FONT = "Calibri"
FONT_BUTTON = (FONT, 16)


class CLoginGUI:


    def __init__(self, parent_wnd, callback_register, callback_signin):
        self._login = ""
        self._password = ""
        self._parent_wnd = parent_wnd
        self._this_wnd = tk.Toplevel(parent_wnd)
        self._callback_register = callback_register
        self._callback_signin = callback_signin

        self._canvas = None
        self._img_bg = None
        self._img_btn = None

        self._entry_Login = None
        self._entry_Password = None

        self._btn_Register = None
        self._btn_SignIn=None
        self._btn_Ok = None
        self._btn_Cancel = None

        self.create_ui()

    def create_ui(self):
        self._this_wnd.title("Login")

        # Load bg image
        self._img_bg = PhotoImage(file=BG_IMAGE)
        img_width = self._img_bg.width()
        img_height = self._img_bg.height()

        # Set size of the application window = image size
        self._this_wnd.geometry(f'{img_width}x{img_height}')
        self._this_wnd.resizable(False,False)

        # Create a canvas to cover the entire window
        self._canvas = tk.Canvas(self._this_wnd,width=img_width,height=img_height)
        self._canvas.pack(fill='both',expand=True)
        self._canvas.create_image(0,0,anchor="nw",image=self._img_bg)

        # Add labels, the same as. add text on canvas
        self._canvas.create_text(50,40,text='Login',font=('Calibri',28),fill='#808080')
        self._canvas.create_text(30,100,text='Login:',font=FONT_BUTTON,fill='#000000',anchor='w')
        self._canvas.create_text(30,150,text='Password:',font=FONT_BUTTON,fill='#000000',anchor='w')

        # Load button image
        self._img_btn = PhotoImage(file=BTN_IMAGE)
        img_btn_w = self._img_btn.width()
        img_btn_h = self._img_btn.height()

        # Button "Register"
        self._btn_Register = tk.Button(self._canvas,text="Register",font=FONT_BUTTON,fg="#c0c0c0",compound="center",
                                      width=img_btn_w,height=img_btn_h,image=self._img_btn,bd=0,
                                      command=self.on_click_register)
        self._btn_Register.place(x=380,y=50)

        # Button "SignIn"
        self._btn_SignIn = tk.Button(self._canvas,text="Sign In",font=FONT_BUTTON,fg="#c0c0c0",compound="center",
                                         width=img_btn_w,height=img_btn_h,image=self._img_btn,bd=0,
                                         command=self.on_click_signin)
        self._btn_SignIn.place(x=380,y=90)

        # Button "Ok"
        self._btn_Ok = tk.Button(self._canvas,text="Ok",font=FONT_BUTTON,fg="#c0c0c0",compound="center",
                                   width=img_btn_w,height=img_btn_h,image=self._img_btn,bd=0)
        self._btn_Ok.place(x=380,y=130)

        # Button "Cancel"
        self._btn_Cancel = tk.Button(self._canvas, text="Cancel", font=FONT_BUTTON, fg="#c0c0c0", compound="center",
                                   width=img_btn_w, height=img_btn_h, image=self._img_btn, bd=0)
        self._btn_Cancel.place(x=380, y=170)

        # Create Entry boxes
        self._entry_Login = tk.Entry(self._canvas,font=('Calibri',16),fg='#808080')
        self._entry_Login.insert(0,'...')
        self._entry_Login.place(x=135,y=85)

        self._entry_Password = tk.Entry(self._canvas,font=('Calibri',16),fg='#808080')
        self._entry_Password.insert(0,"")
        self._entry_Password.place(x=135,y=130)


    def run(self):
        self._this_wnd.mainloop()

    def on_click_register(self):
        self._login = self._entry_Login.get()
        self._password = self._entry_Password.get()
        #data = '{"login": self._login, "password": self._password}'
        data = {}
        data["login"] = f"{self._login}"
        data["password"] = f"{self._password}"
        json_data = json.dumps(data)
        #data_json = json.loads(data)
        self._callback_register(json_data)
        self.close_window()

    def on_click_signin(self):
        self._login = self._entry_Login.get()
        self._password = self._entry_Password.get()
        data = {"login": self._login, "password": self._password}
        self._callback_signin(data)

    def close_window(self):
        self._this_wnd.destroy()


    def on_click_ok(self):
        pass


if __name__ == "__main__":
    client = CLoginGUI()
    client.run()

