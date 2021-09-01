#uniform_shop.py
#S.Amichand, April 13

#The BDSC uniform shop wants you to create an app for uniform orders. It is an app for students of age 13-18. 
# Existing student users may log in or create an account to use the app. Then the app displays a menu with prices for placing orders. 
# Once the user chooses items, the app displays order details - items, quantity, price and total. 

# Imports tkinter for GUI | PIL for the pillow module so I can use images | Sys so I can terminate the app | Messagebox to display a message box Based on conditions.| Sqlite3 for the database
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import sys, tkinter.messagebox, sqlite3

# ================= This function allows me to freely change the height and width of my app anywhere in my code/classes =================#
def window_size(self, w, h):
    #================= Get screen width and height =================#
    self.ws = self.master.winfo_screenwidth()
    self.hs = self.master.winfo_screenheight()
    # calculate position x, y
    self.x = (self.ws/2) - (self.w/2)    
    self.y = (self.hs/2) - (self.h/2)
    self.master.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))

# ================= Allows me to have an exit prompt ================= # 
def iExit():
    iExit = tkinter.messagebox.askyesno("Exit?", "Are you sure you wish to exit?")
    if iExit > 0:
        sys.exit()

# ================= First part of my uniform shop app. Checks the users age =================#
class AgeChecker():
    def __init__(self,master):
        self.master = master

        #=================  Sets the window title and color =================#
        self.master.title("Age Verification")

        #================= Sets window size (width and height) =================#
        self.w = 1090
        self.h = 490

        window_size(self, self.w, self.h)

        # ================= Variables Used in this file and with the other files. =================#
        userAge = tk.StringVar()
        AGEMIN = 13
        AGEMAX = 90
        # ================= Styling my app (colors etc) =================#
        self.master.MFrame = ttk.Style()
        self.master.MFrame.configure('MF.TFrame', background='Cadet Blue')

        self.master.txtcolor = "#7ecfed"
        self.master.TLabel = ttk.Style()
        self.master.TLabel.configure('L.TLabel', background='#141313', foreground=self.master.txtcolor)

        self.master.configure(background="Cadet Blue")

        # ================= Sets the main frame that the other frames are under =================#
        self.frame1 = ttk.Frame(self.master, style="MF.TFrame")
        self.frame1.grid(row=0, column=0)
        
        #================= Image =================#
        image = Image.open("images/age.png")
        resize_image = image.resize((450, 170))
        my_img1 = ImageTk.PhotoImage(resize_image)

        #================= Frames =================#
        ageFrame = ttk.Frame(self.frame1, relief='sunken', style="MF.TFrame", borderwidth="10")
        ageFrame.grid(row=1, column=0)
        
        agebtnFrame = ttk.Frame(self.frame1, relief='raised')
        agebtnFrame.grid(row=2, column=0)

        #================= Label =================#
        lblTitle1 = ttk.Label(ageFrame, text = "Age Verification", font=('arial', 50, 'bold underline'), style="L.TLabel", foreground=self.master.txtcolor)
        lblTitle1.grid(row=0, column=0, pady=30)

        ageimg = ttk.Label(ageFrame, image=my_img1)
        ageimg.photo = my_img1
        ageimg.grid(row = 1, column = 0)

        lblage = ttk.Label(ageFrame, text="Hello! This app will allow you to order your BDSC uniform. To start I need to verify your age. If you are done, press enter or the button below. \n How old are you?",
                                font=('arial', 13, 'italic'), style="L.TLabel", foreground=self.master.txtcolor, justify="center")
        lblage.grid(row=2, column=0, pady=10)
        
        #================= Entry =================#
        ageEntry = ttk.Entry(ageFrame, textvariable=userAge, width=5, font=('arial', 10, ''))
        ageEntry.grid(row=3, column=0, pady=10)
        ageEntry.focus()

        #================= Functions used by the buttons =================#
        def verify(self, userAge, AGEMIN, AGEMAX):        
            age = (userAge.get().strip())
            if age.isdigit():
                if int(age) >= AGEMIN and int(age) <= AGEMAX:
                    tkinter.messagebox.showinfo("Old Enough", "You are old enough and may continue")
                    self.frame1.destroy()
                    LoginChoice(self.master)
                    
                elif int(age) > 90:
                    tkinter.messagebox.showerror("Unrealistic Age", "Please enter a valid age")
                    userAge.set("")
                    return False

                else:
                    tkinter.messagebox.showerror("Too Young", "Sorry you are too young to use this app.")
                    sys.exit()

            else:
                    tkinter.messagebox.showerror("Wrong Data", "Please type only a whole number.")
                    userAge.set("")

        #================= Buttons and bind user to enter =================#
        btnDone = ttk.Button(agebtnFrame, text="Verify", width = 17, command= lambda: verify(self, userAge, AGEMIN, AGEMAX))
        btnDone.grid(row=4, column=0)
        ageEntry.bind("<Return>", (lambda event: verify(self, userAge, AGEMIN, AGEMAX)))
        btnExit = ttk.Button(agebtnFrame, text="Exit", width = 17, command = lambda: iExit())
        btnExit.grid(row=4, column=1)
        self.master.protocol("WM_DELETE_WINDOW", iExit)

        for child in self.frame1.winfo_children():
            child.grid_configure(padx=5, pady=5)

#================= Second part of my uniform shop app. It allows the user to login. =================#
class LoginChoice():
    def __init__(self, master):
        self.master = master
        self.master.title("Age")
        self.master.configure(background="Cadet Blue")

        self.w = 420    
        self.h = 440

        window_size(self, self.w, self.h)

        self.frame2 = ttk.Frame(self.master, style='MF.TFrame')
        self.frame2.grid(row=0, column=0, padx=5, pady=5)

        # Connects to database, then creates the tables with their column headers if needed, then saves it and closes it
        with sqlite3.connect('uniformshop.db') as db:
            c = db.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL PRIMARY KEY,password TEX NOT NULL);')
        c.execute('CREATE TABLE IF NOT EXISTS uniformdb (uniform TEXT NOT NULL PRIMARY KEY,price DECIMAL NOT NULL);')
        db.commit()
        db.close() 
        
        #================= Variables Used =================#
        user = tk.StringVar()
        password = tk.StringVar()
        self.check = tk.IntVar()

        #================= Sets the image =================#  
        image2 = Image.open("images/login.png")
        resize_image2 = image2.resize((175, 160))
        my_img2 = ImageTk.PhotoImage(resize_image2)

        #================= Frames Set =================#
        userlogin1 = ttk.Frame(self.frame2, width=400, height=200, style="MF.TFrame", relief='ridge')
        userlogin1.grid(row = 1, column=0, padx=5, pady=5)
        userlogin2 = ttk.Frame(self.frame2, width=400, height=200, style="MF.TFrame", relief='ridge')
        userlogin2.grid(row = 2, column=0, padx=5, pady=5)
        
        loginbtnFrame = ttk.Frame(self.frame2, width=400, height=200, style="MF.TFrame", relief='ridge')
        loginbtnFrame.grid(row=3, column=0, padx=5, pady=5)
        
        #================= Label =================#
        lblTitle1 = ttk.Label(self.frame2, text="Login",  font=('arial', 50,'bold'), style="L.TLabel", foreground=self.master.txtcolor)
        lblTitle1.grid(row=0, column=0)
        loginimg = ttk.Label(userlogin1, image=my_img2, style='L.TLabel')
        loginimg.photo = my_img2
        loginimg.grid(row=1, column=0, padx=5, pady=5)
        lblChoice = ttk.Label(userlogin1, text="Enter your username and password to login. \n If you wish to create an account press the button below"
                                 ,font=('arial', 12,'italic'), style='L.TLabel', foreground=self.master.txtcolor)
        lblChoice.grid(row=2, column=0, padx=5, pady=5)
        
        lbluser = ttk.Label(userlogin2, text="Enter your name:", font=('arial', 12,''), anchor = 'w', 
                           style='L.TLabel', foreground=self.master.txtcolor)
        lbluser.grid(row=3, column=0, padx=5, pady=5)

        lblpass = ttk.Label(userlogin2, text="Enter your password:", font=('arial', 12,''), anchor = 'w', 
                           style='L.TLabel', foreground=self.master.txtcolor)
        lblpass.grid(row=4, column=0, padx=5, pady=5)

        #================= Entry =================#
        userEntry = ttk.Entry(userlogin2, textvariable=user, font=('arial', 10, ''))
        userEntry.grid(row=3, column=1,padx=5, pady=5)
        userEntry.focus()
        
        passEntry = ttk.Entry(userlogin2, textvariable=password, show='*', font=('arial', 10, ''))
        passEntry.grid(row=4, column=1, padx=5, pady=5)
    
        #================= Functions Used by Buttons=================#

        # ================= This functions wipes the previous frame and creates a new one for the registration =================#
        def register(self):
            self.frame2.destroy()
            self.w = 550    
            self.h = 480
            window_size(self, self.w, self.h)
            # Variables
            newUser = tk.StringVar()
            newPass = tk.StringVar()
            
            image3 = Image.open("images/createacc.png")
            resize_image3 = image3.resize((170, 160))
            my_img3 = ImageTk.PhotoImage(resize_image3)

            # Frames
            self.frame2 = ttk.Frame(self.master, style='MF.TFrame')
            self.frame2.grid(row=0, column=0, padx=5, pady=5)
            register1 = ttk.Frame(self.frame2, style='MF.TFrame', relief='ridge')
            register1.grid(row=1, column=0, padx=5, pady=5)
            register2 = ttk.Frame(self.frame2, width=400, height=200, style='MF.TFrame', relief='ridge')
            register2.grid(row=2, column=0, padx=5, pady=5)
            registerbtn = ttk.Frame(self.frame2, width=400, height=200, style='MF.TFrame', relief='ridge')
            registerbtn.grid(row=3,column=0, padx=5, pady=5)

            # Label
            lblTitle2 = ttk.Label(self.frame2, text="Sign up", font=('arial', 50,'bold'), style='L.TLabel', foreground=self.master.txtcolor)
            lblTitle2.grid(row=0, column=0)

            createaccImg = ttk.Label(register1, image=my_img3, style='L.TLabel')
            createaccImg.photo = my_img3
            createaccImg.grid(row=1, column=0, padx=5, pady=5)
            
            lblinfo = ttk.Label(register1, text="Enter your username and password in the field below. Make sure \n your password is 6 characters long and has one capital letter. \n If you wish to login then press the login button."
                                                     ,font=('arial', 13,'italic'), style='L.TLabel', foreground=self.master.txtcolor)
            lblinfo.grid(row=2, column=0, padx=10, pady=10)

            lblcreateUser = ttk.Label(register2, text="Username:", font=('arial', 12,''), anchor = 'w'
                                    ,style='L.TLabel', foreground=self.master.txtcolor)
            lblcreateUser.grid(row=3, column=0,padx=5, pady=5)

            lblcreatePass = ttk.Label(register2, text="Password:", font=('arial', 12,''), anchor = 'w', 
                                     style='L.TLabel', foreground=self.master.txtcolor)
            lblcreatePass.grid(row=4, column=0, padx=5, pady=5)

            # Entry
            createuserEntry = ttk.Entry(register2, textvariable=newUser, font=('arial', 10, ''))
            createuserEntry.grid(row=3, column=1,padx=5, pady=5)
            createuserEntry.focus()

            createpassEntry = ttk.Entry(register2, textvariable=newPass, show='*', font=('arial', 10, ''))
            createpassEntry.grid(row=4, column=1, padx=5, pady=5)

            #Functions for buttons
            def created(newUser, newPass):
                with sqlite3.connect('uniformshop.db') as db:
                    c = db.cursor()
                find_user = ('SELECT * FROM user WHERE username = ? ')
                c.execute(find_user,[(newUser.get())])
                if c.fetchall():
                    tkinter.messagebox.showerror("Error", "Please choose another username as this is taken.")
                    return False

                else: # Checks length and if there is any upper case letter
                    if len(newPass.get().strip()) > 6 and any(userP.isupper() for userP in (newPass.get())):
                        insert = 'INSERT INTO user(username,password) VALUES(?,?)'
                        c.execute(insert,[(newUser.get()),(newPass.get())])
                        db.commit()
                        tkinter.messagebox.showinfo("Account Created", "Your account was successfully created and you may proceed")
                        self.frame2.destroy()   
                        MenuChoice(self.master)

                    else:
                        tkinter.messagebox.showerror("Error", "Make sure your password is 6 characters long and you have one captial letter")
                        return False

            def return_back():
                self.frame2.destroy()
                LoginChoice(self.master)

            def show_pass2(check, createpassEntry):
                if self.check.get() == 1 :
                    createpassEntry.configure(show = "")
                elif self.check.get() == 0 :
                    createpassEntry.configure(show = "*")

            # Buttons
            checkshowPass2 = ttk.Checkbutton(register2, text="Show", variable = self.check, onvalue = 1, 
            offvalue = 0, width = 5, command = lambda: show_pass2(self.check, createpassEntry))
            checkshowPass2.grid(row=4, column=2)
            btnLogin = ttk.Button(registerbtn, text="Go Back",width = 20, command= lambda: return_back())
            btnLogin.grid(row=5, column=0)

            btnCreate = ttk.Button(registerbtn, text="Create your account", width = 20, command = lambda: created(newUser, newPass))
            btnCreate.grid(row=5, column=1)
            createuserEntry.bind("<Return>", (lambda event: created(newUser, newPass)))
            createpassEntry.bind("<Return>", (lambda event: created(newUser, newPass)))

            btnExit = ttk.Button(registerbtn, text="Exit", width = 20, command = lambda: iExit())
            btnExit.grid(row=5, column=2)

        def login(user, password):
            with sqlite3.connect('uniformshop.db') as db:
                c = db.cursor()
            
            find_user = ('SELECT * FROM user where username = ? and password = ?')
            c.execute(find_user,[(user.get().strip()), (password.get())])
            result = c.fetchall()
            if result:
                tkinter.messagebox.showinfo("Logged in", "You are now logged in and may continue.")
                
                self.frame2.destroy()
                MenuChoice(self.master)

            else:
                tkinter.messagebox.showerror("Wrong Data", "Either your username or password does not match the existing account")
                user.set("")
                password.set("")
                userEntry.focus()

        def show_pass1(check, passEntry):
            if self.check.get() == 1 :
                passEntry.configure(show = "")
            elif self.check.get() == 0 :
                passEntry.configure(show = "*")

        #================= Buttons Used =================#

        # Creates a check button so the user can toggle to see their password
        checkshowPass1 = ttk.Checkbutton(userlogin2, text="Show", variable = self.check, onvalue = 1, 
        offvalue = 0, width = 5, command = lambda: show_pass1(self.check, passEntry))
        checkshowPass1.grid(row=4, column=2)

        btnRegister = ttk.Button(loginbtnFrame, text="Sign Up", width = 17, command = lambda: register(self))
        btnRegister.grid(row=5, column = 0)
        btnLogin = ttk.Button(loginbtnFrame, text="Login",width = 17, command= lambda: login(user, password))
        btnLogin.grid(row=5, column=1, )
        userEntry.bind("<Return>", (lambda event: login(user, password)))
        passEntry.bind("<Return>", (lambda event: login(user, password)))
        btnExit = ttk.Button(loginbtnFrame, text="Exit", width = 17, command = lambda: iExit())
        btnExit.grid(row=5, column=2,)

        #================= Last class so that the user may add the uniforms they want to buy =================#
class MenuChoice():
    def __init__(self, master):    
        self.master = master
        self.master.title("Menu")
        self.master.configure(background="Cadet Blue")

        self.w = 700   
        self.h = 370
        window_size(self, self.w, self.h)

        self.frame3 = ttk.Frame(self.master, style="MF.TFrame")
        self.frame3.grid(row=0, column=0, padx=5, pady=5)  

        #================= Variables Used =================#
        self.uniform = {"Shorts": 50, "Trousers": 100, "Short Sleeve Shirt": 35, 
                        "Long Sleeve Shirt": 40, "Jacket": 70, "Tie": 25, "Socks": 25}
        self.toorder = []
        ordereduniform = {}
        unidropdown = tk.StringVar()
        unidropdown.set("Uniform")
        numuniform = tk.IntVar()
        self.cost = 0
            
        # Sets the frames
        infoFrame = ttk.Frame(self.frame3, width=80, height=70, relief='ridge', style="MF.TFrame")
        infoFrame.grid(row = 1, column=1, padx=5, pady=5)
        infobtnFrame = ttk.Frame(self.frame3, width=80, height=70, relief='ridge', style="MF.TFrame")
        infobtnFrame.grid(row = 2, column=1, padx=5, pady=5)
        
        #================= Image Set =================#
        image4 = Image.open("images/bdsc_logo.png")
        resize_image4 = image4.resize((200, 150))
        my_img4 = ImageTk.PhotoImage(resize_image4)

        # Labels
        createaccImg = ttk.Label(self.frame3, image=my_img4)
        createaccImg.photo = my_img4
        createaccImg.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        lblTitle2 = ttk.Label(self.frame3, text="Add Your Uniform", font=('arial', 40,'bold'), style="L.TLabel", justify="center")
        lblTitle2.grid(row=0, column=1, pady=10, padx=5)
        lblinfo = ttk.Label(infoFrame, text="Choose the uniform you want and then the amount of it."
                        ,font=('arial', 12,'italic'), style="L.TLabel", justify="center") 
        lblinfo.grid(row=1, column=1, sticky="ns", padx=10, pady=10)

        # Create drop down with all uniform
        uniformdropDown1 = ttk.OptionMenu(infoFrame, unidropdown, *self.uniform)

        uniformdropDown1.grid(row = 2, column=1, sticky="nw", padx=80, pady=5)
        # Entry for uniform amount
        uniformnum_entry = ttk.Entry(infoFrame, textvariable=numuniform, font=('arial', 10, ''), width=5)
        uniformnum_entry.grid(row=2, column=1, padx=100, pady=5, sticky="ne")
                
        #================= Functions used for button =================#
        def add_uniform(self, unidropdown, numuniform):
            def addcostuni(self): # Writes users order in a txt file to prevent too many orders of one item
                self.f.write(self.chosenuni + " x"+str(self.numuni) + "\n")
                self.toorder.append(self.chosenuni + ' ' + str(self.numuni) + 'x')
                return self.toorder

            self.chosenuni = (unidropdown.get())
            self.numuni = (numuniform.get())
            ordereduniform.update({"Uniform": self.chosenuni})
            ordereduniform.update({"Num Uniform": self.numuni})
            self.f = open('uniformorders.txt', 'r+')
            if self.numuni > 0 and self.numuni <=5:
                if self.chosenuni not in self.f.read():
                    self.cost += self.uniform[self.chosenuni] * self.numuni 
                    addcostuni(self)

        def showuni(self):
            if len(self.toorder) > 1:
                self.toorder = 'To order: '+ ', ' .join(self.toorder)
                lblShow = ttk.Label()
                lblShow = ttk.Label(infoFrame, text = f'{self.toorder}, ${self.cost}', font=('arial', 12,'italic'), style="L.TLabel", justify="center") 
                lblShow.grid(row=6, column=1, sticky="ns", padx=10, pady=10)
        
        def iOrder(self):
            with open('uniformorders.txt', 'r+') as f:
                f.truncate(0)
                sys.exit()

        # Buttons
        btnadduni = ttk.Button(infobtnFrame, text="Add Uniform",width = 17, command = lambda: add_uniform(self, unidropdown, numuniform))
        btnadduni.grid(row=3, column=2)  
        btnExit = ttk.Button(infobtnFrame, text="Exit",width = 17, command = lambda: iExit())
        btnOrder = ttk.Button(infobtnFrame, text="Order",width = 17, command = lambda: iOrder(self))
        btnOrder.grid(row=4, column=2)   
        btnUnishow = ttk.Button(infobtnFrame, text="Show Order",width = 17, command = lambda: showuni(self))
        btnUnishow.grid(row=4, column=3)

        for child in self.frame3.winfo_children():
            child.grid_configure(padx=5, pady=5)
        for child in infobtnFrame.winfo_children():
            child.grid_configure(padx=0, pady=5)

# ================= Sets the window for my app and calls the main class =================#
if __name__ == "__main__":
    root = tk.Tk()
    AgeChecker(root)
    root.mainloop()    