from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import resch as c
import csv
class maingui:
    def __init__(self,root):
        self.root=root
        self.permission=["view students","add student","update student","remove student"
                         ,"view courses","add course","update course","remove course"
                         ,"view rooms","add room","update room","remove room"
                         ,"view payments","add payment","update payment","remove payment"]
        self.root.wm_iconbitmap("res//logo.ico")
        self.root.geometry("703x438")
        self.root.title("Hostel management system")
        self.stringstatus="Please Enter The Username And Password To Login"
        self.sbar=Label(self.root,text="Welcome",relief=SUNKEN,anchor="w")
        self.sbar.pack(side=BOTTOM,fill=X)
        self.menu=Frame(self.root,height=413,width=170,bg='#006064')
        self.menu.pack(side=LEFT,fill=Y)
        self.logo_hms=[]
        self.logo_hms.append(PhotoImage(file="res//logo.png"))
        for i in range(5):
            self.logo_hms.append(PhotoImage(file=f"res//card{i+1}.png"))
        Label(self.menu,image=self.logo_hms[0],bg='#006064').place(x=12,y=6)
        self.heading=Label(text="HOSTEL MANGEMENT SYSTEM",bg='#006064',fg='#00bcd4',padx=18,pady=20,font="stikatext 20 bold italic",anchor='w')
        self.heading.pack(side=TOP,fill=X)
        self.currentuser=[]
        self.buttons=[]
        self.f2=Frame(self.root,height=338,width=800,bg='#80deea')
        self.f2.pack(fill=BOTH,expand=True)
        self.server=c.sqlcom()
        self.timer=self.sbar.after(1000,lambda : self.sbar.config(text="Welcome"))
        self.update_status("Welcome")
        #self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.login_page()
    def on_close(self):
        pass
    def clearwid(self):
        self.clearm()
        self.buttons=[]
        for m in self.menu.winfo_children():
            if m.winfo_class() == 'Button':
                m.destroy()
    def clearm(self):
        for w in self.f2.winfo_children():
            w.destroy()
    def update_status(self,newtext):
        self.sbar.config(text=newtext)
        self.sbar.after_cancel(self.timer)
        self.timer=self.sbar.after(2000,lambda : self.sbar.config(text=self.stringstatus))
    def instance_status(self):
        self.sbar.after_cancel(self.timer)
        self.sbar.config(text=self.stringstatus)
    def buttoncheck(self,t,func):
        for i in range(len(self.buttons)):
            self.buttons[i].config(state="disabled"if i==t else "normal")
            self.buttons[i].config(bg="#80deea"if i==t else "#00ACC1")
        func()
    def name_check1(self,n):
        for i in n:
            if i not in 'abcdefghijklmnopqrstuvwxyz0123456789_$':
                return True
        else:
            return False
    def name_check2(self,n):
        for i in n:
            if i not in 'abcdefghijklmnopqrstuvwxyz0123456789_-/ ':
                return True
        else:
            return False
    def name_check3(self,n):
        for i in n:
            if i not in 'abcdefghijklmnopqrstuvwxyz ':
                return True
        else:
            return False
    def name_check4(self,n):
        for i in n:
            if i not in 'abcdefghijklmnopqrstuvwxyz0123456789_- ':
                return True
        else:
            return False
    def name_check5(self,n):
        for i in n:
            if i not in '0123456789,':
                return True
        else:
            return False
    def dobconv(self,s):
        s=s.split('-')
        s.reverse()
        return '-'.join(s)
    def dobcheck(self,s,u):
        s=s.split('-')
        if len(s)==3:
            for i in s:
                if not i.isdigit() or 1>int(i):
                        self.update_status('Please Enter Numbers In '+u)
                        return False
            if not 999<int(s[2])<10000:
                self.update_status('Please Enter Year From 1000 To 9999 In '+u)
                return False
            elif int(s[1])>12 or int(s[0])>30+((int(s[1])+int(s[1])>7)%2)-(s[1]==2)-((int(s[2])%100==0 and int(s[2])%400!=0) or (int(s[2])%4!=0)):
                self.update_status('Please Enter Valid Numbers In '+u)
                return False
            else:
                return True
        self.update_status(f'Please Enter {u} In Valid Format DD-MM-YYYY')
        return False
    def id_gen(self,n,k=1):
        d_id=self.server.sqlget_all_id(n)
        t=[]
        for h in range(k):
            if d_id==[]:
                t.append(1)
                d_id.append(1)
            elif d_id[-1]>len(d_id):
                for d in range(len(d_id)):
                    if d+1!= d_id[d]:
                        t.append(d+1)
                        d_id.insert(d,d+1)
                        break
            else:
                t.append(d_id[-1]+1)
                d_id.append(d_id[-1]+1)
        return t
    def login_page(self):
        def show():
            entry[len(entry)-1].config(show='*'if sp.get()==0 else '')
        def remove_all_widgets():
            for w in login_frame.winfo_children():
                if w!=wel_b and w!=show_pass:
                    w.destroy()
        def exit():
            self.clearwid()
            self.root.destroy()
        def stu_reg():
            nonlocal entry
            def stureg():
                d=self.server.sqlstuconnect()
                if d[0]:
                    op=[i.get() for i in entry]
                    op.insert(0,self.id_gen('student')[0])
                    for i in (2,4,5,7):
                        op[i]=op[i].lower().strip()
                    if "" in op or op[3]=='Please Select...':
                        self.update_status("Please Fill All Entries")
                    elif not op[1].isdigit():
                        self.update_status("Please Enter Registration Number In Numbers")
                    elif self.name_check3(op[2]) or self.name_check3(op[4]) or self.name_check3(op[5]):
                        self.update_status("Please Enter Valid Name Only")
                    elif self.name_check2(op[7]):
                        self.update_status("Please Enter Valid Address")
                    elif not op[8].isdigit() or len(op[8])!=10:
                        self.update_status("Please Enter 10 Numbers In Phone number")
                    elif self.name_check1(op[9].lower().strip()):
                        self.update_status("Please Enter Valid Characters 0-9,A-Z,a-z, ,_,$ In Password")
                    elif self.dobcheck(op[6],'DOB'):
                        op[1]=int(op[1])
                        op[3]='M' if op[3]=='Male' else 'F'
                        op[6]=self.dobconv(op[6])
                        op.insert(9,None)
                        op.insert(10,None)
                        op.append(0)
                        op=tuple(op)
                        self.update_status(self.server.sql_student_registration(op))
                    self.server.sqlconclose()
                else:
                    self.update_status(d[1])
            self.heading.config(text="STUDENT REGISTRATION PAGE")
            self.stringstatus="Please Enter The All Feilds To Register"
            self.instance_status()
            remove_all_widgets()
            t=['Registration Number','Student Name','Gender','Father Name','Mother Name','Date Of Birth','Address','Phone Number','Password']
            Label(login_frame,text="Student Registration",font="comicsansms 18 bold",bg='#80deea').grid(sticky=N,row=0,column=0,columnspan=2)
            for i in range(len(t)):
                Label(login_frame,text=t[i]+" :",font="comicsansms 12 bold",bg='#80deea').grid(sticky='w',row=i+1,column=0)
            entry=[]
            for i in range(9):
                if i==2:
                    e=ttk.Combobox(login_frame,values=['Please select...','Male','Female'],state='readonly')
                    e.current(0)
                else:
                    e=Entry(login_frame)
                e.grid(row=1+i,column=1,sticky="ew", pady=6,padx=4)
                entry.append(e)
            entry[8].config(show='*')
            wel_b.grid_forget()
            wel_b.grid(row = 10, column = 1,sticky="s")
            wel_b.config(text='Register',command=stureg)
            show_pass.grid_forget()
            show_pass.grid(row=10,column=0,sticky="s")
        def stu_login():
            nonlocal entry
            def stulog():
                op=[i.get() for i in entry]
                if "" in op:
                    self.update_status("Please Fill All Entries")
                elif not op[0].isdigit():
                    self.update_status("Please Enter Registration Number In Numbers")
                elif self.name_check3(op[1].strip().lower()):
                    self.update_status("Please Enter Valid Characters Only 0-9,a-z,A-Z,$,_ in Name")
                elif self.name_check1(op[2].lower().strip()):
                    self.update_status("Please Enter Valid Characters 0-9,A-Z,a-z, ,_,$ In Password")
                else:
                    self.update_status('Checking MySQL Connectivity...')
                    wel_b.config(state='disabled')
                    t=self.server.sqlstucheck(op)
                    self.update_status(t[0])
                    wel_b.config(state='normal')
                    if t[1]:
                        t=list(t[2])
                        self.currentuser=tuple(t)
                        self.student()
            self.heading.config(text="STUDENT LOGIN PAGE")
            self.stringstatus="Please Enter The All Feilds To Login"
            self.instance_status()
            remove_all_widgets()
            Label(login_frame,text="Welcome Back !",font="comicsansms 18 bold",bg='#80deea').grid(sticky=N,row=0,column=0,columnspan=2)
            Label(login_frame,text="Registration Number :",font="comicsansms 15 bold",bg='#80deea').grid(sticky='w',row=1,column=0)
            Label(login_frame,text="Student Name :",font="comicsansms 15 bold",bg='#80deea').grid(sticky='w',row=2,column=0)
            Label(login_frame,text="Password :",font="comicsansms 15 bold",bg='#80deea').grid(sticky='w',row=3,column=0)
            entry=[]
            for i in range(3):
                e=Entry(login_frame)
                e.grid(row=1+i,column=1,sticky="ew", pady=18,padx=4)
                entry.append(e)
            entry[2].config(show='*')
            wel_b.grid_forget()
            wel_b.grid(row = 4, column = 1,sticky="s")
            wel_b.config(text='Login',command=stulog)
            show_pass.grid_forget()
            show_pass.grid(row=4,column=0,sticky="s")
        def admin_login():
            nonlocal entry
            def adminlog():
                op=[i.get() for i in entry]
                if "" in op:
                    self.update_status("Please Fill All Entries")
                elif self.name_check1(op[1].strip().lower()) or self.name_check1(op[0].lower()):
                    self.update_status("Please Enter Valid Characters Only 0-9,a-z,A-Z,$,_")
                else:
                    self.update_status('Checking MySQL Connectivity...')
                    wel_b.config(state='disabled')
                    t=self.server.sqlcheck(op)
                    self.update_status(t[0])
                    wel_b.config(state='normal')
                    if t[1]:
                        t=list(t[2])
                        t[3]=None if t[3] is None else list(map(int,t[3].split(',')))
                        self.currentuser=tuple(t)
                        self.admin()
            self.heading.config(text="ADMIN LOGIN PAGE")
            self.stringstatus="Please Enter The Username And Password To Login"
            self.instance_status()
            remove_all_widgets()
            Label(login_frame,text="Welcome Back !",font="comicsansms 18 bold",bg='#80deea').grid(sticky=N,row=0,column=0,columnspan=2)
            Label(login_frame,text="Username :",font="comicsansms 15 bold",bg='#80deea').grid(sticky=E,row=1,column=0)
            Label(login_frame,text="Password :",font="comicsansms 15 bold",bg='#80deea').grid(sticky=E,row=2,column=0)
            entry=[]
            for i in range(2):
                e=Entry(login_frame)
                e.grid(row=1+i,column=1,sticky="ew", pady=18,padx=4)
                entry.append(e)
            entry[1].config(show='*')
            wel_b.grid_forget()
            wel_b.grid(row = 3, column = 1,sticky="s")
            wel_b.config(text='Login',command=adminlog)
            show_pass.grid_forget()
            show_pass.grid(row=3,column=0,sticky="se")
        self.clearwid()
        sp=IntVar()
        entry=[]
        b1=Button(self.menu,font='comicsansms 12 bold',text='Student Registration',bg='#00acc1',fg='white', disabledforeground="white", relief=FLAT,width=16,activeforeground='white',activebackground='#80deea',command=lambda :self.buttoncheck(0,stu_reg))
        b1.place(x=0,y=76)
        b2=Button(self.menu,font='comicsansms 12 bold', text='Student Login',bg='#00acc1',fg='white', disabledforeground="white",activeforeground='white',activebackground='#80deea', relief=FLAT,width=16,command=lambda :self.buttoncheck(1,stu_login))
        b2.place(x=0,y=114)
        b3=Button(self.menu,font='comicsansms 12 bold', text='Admin Login',bg='#80deea',state="disabled",fg='white', disabledforeground="white",activeforeground='white',activebackground='#80deea', relief=FLAT,width=16,command=lambda :self.buttoncheck(2,admin_login))
        b3.place(x=0,y=152)
        b4=Button(self.menu,font='comicsansms 12 bold',text='Exit',bg='#00acc1',fg='white', disabledforeground="white",activeforeground='white',activebackground='#80deea', relief=FLAT,width=16,command=lambda :self.buttoncheck(3,exit))
        b4.place(x=0,y=190)
        self.buttons=[]
        self.buttons.extend([b1,b2,b3,b4])
        login_frame=Frame(self.f2,bg='#80deea')
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        wel_b=Button(login_frame,font="comicsansms 12 bold",text='Login') 
        show_pass=Checkbutton(login_frame,text="Show Password",variable=sp,command=show,bg='#80deea',activebackground='#80deea')
        admin_login()
    def student(self):
        def buttoncheck3(t):
            for i in range(len(self.buttons)):
                self.buttons[i].config(state="disabled"if i==t else "normal")
                self.buttons[i].config(bg="#80deea"if i==t else "#00acc1")
            self.f2.rowconfigure(tuple(range(10)),weight=0)
            self.f2.columnconfigure(tuple(range(2)),weight=0)
            s=('student','room','course')
            if t==3:
                payment()
            elif t==4:
                self.logout()
            else:
                show_details(t,s[t])
        def show_details(tid,t):
            def show():
                entries[8].config(show='*'if sp.get()==0 else '')
            def setpassnew():
                if entries[8]["state"]=="disabled":
                    entries[8].config(state="normal")
                    entries[8].delete(0, 'end')
                    upb.config(text="Save Password")
                elif entries[8].get()=='':
                    self.update_status('Please Fill Out Password Entry')
                elif self.name_check1(entries[8].get().lower().strip()):
                    self.update_status("Please Enter Valid Characters Only 0-9,a-z,A-Z,$,_")
                else:
                    entries[8].config(state="disabled")
                    self.server.sql_stu_pass(self.currentuser[0],entries[8].get())
                    self.update_status('New Password Successfully Updated')
                    upb.config(text="Update New Password")
            sp=IntVar()
            entries=[]
            self.clearm()
            self.heading.config(text=t.upper()+" DETAILS")
            self.stringstatus="Showing "+t.title()+" Details"
            self.instance_status()
            if self.currentuser[tid] is not None:
                d=self.server.sql_id_info(t,self.currentuser[tid])
            s=(('Registration Number','Name','Gender','Father Name','Mother Name','Date Of Birth','Address','Phone Number','Password'),('Room no','Block','Available','Beds','AC','Wifi','TV'),('Course Name','Duration'))
            for i in range(len(s[tid])):
                Label(self.f2,text=s[tid][i]+':',font="comicsansms 12 bold",bg='#80deea').grid(row=i,column=0,sticky='w',padx=6)
                e=Entry(self.f2,disabledforeground='black')
                if self.currentuser[tid] is None:
                    e.insert(0,'NA')
                elif tid==0 and i==2:
                    e.insert(0,'Male' if d[i]=='M' else 'Female')
                elif tid==0 and i==5:
                    e.insert(0,self.dobconv(str(d[i])))
                elif tid==1 and i in (2,4,5,6):
                    e.insert(0,'Yes' if d[i]=='Y' else 'No')
                else:
                    e.insert(0,d[i])
                e.config(state='disabled')
                e.grid(row=i,column=1,sticky='we',padx=6)
                entries.append(e)
            if tid==0:
                entries[8].config(show='*')
                upb=Button(self.f2,font="comicsansms 12 bold",text='Update New Password',command=setpassnew)
                upb.grid(row=9,column=1)
                Checkbutton(self.f2,text="Show Password",variable=sp,command=show,bg='#80deea',activebackground='#80deea').grid(row=9,column=0,sticky='e')
            self.f2.rowconfigure(tuple(range(len(s[tid])+(tid==0))),weight=1)
            self.f2.columnconfigure(tuple(range(2)),weight=1)
        def payment():
            def search():
                nonlocal payment
                for item in treev.get_children():
                    treev.delete(item)
                if cbox.get()=='All':
                    c=''
                elif cbox.get()=='Pending':
                    c=' and payment_date is null'
                else:
                    c=' and payment_date is not null'
                payment=list(self.server.sql_stu_payment_search(self.currentuser[0],c))
                for r in payment:
                    r=list(r)
                    r[2]=self.dobconv(str(r[2]))
                    r[3]='Pending' if r[3] is None else self.dobconv(str(r[3]))
                    treev.insert('',END, values=r[1:])
                self.update_status(f'Showing {cbox.get()} Payments')
            def make_payment():
                selected_item = treev.selection()
                if selected_item==():
                    self.update_status('No Payment Selected. Please Select A Payment To Processed.')
                else:
                    pmt= payment[treev.index(selected_item[0])]
                    if pmt[3] is None:
                        res = messagebox.askquestion("Payment Pending", "Do you want to proceed with payment?")
                        if res=='yes':
                            self.server.sql_stu_payment_make(pmt[0])
                            self.update_status('Payment Of {pmt[1]} Has Been Successfully Processed.')
                            search()
                    else:
                        self.update_status('This payment has already been completed.')
            payment=[]
            self.clearm()
            self.heading.config(text="PAYMENT DETAILS")
            self.stringstatus="Showing Payment Details"
            self.instance_status()
            s1=Frame(self.f2,bg='#80deea',height=30)
            s1.pack(side=TOP,fill=X)
            Label(s1,text="Payment :",font="comicsansms 12 bold",bg='#80deea').grid(row=0,column=0,pady=4)
            cbox=ttk.Combobox(s1,values=['All','Completed','Pending'],state='readonly',width=19)
            cbox.grid(row=0,column=1,pady=4)
            cbox.current(0)
            Button(s1,text="Search ",font="comicsansms 12 bold",command=search).grid(row=0,column=2,pady=4,padx=6)
            s1.columnconfigure((0,1,2),weight=1)
            s2=Frame(self.f2,bg='#80deea')
            s2.pack(fill=BOTH,expand=True,padx=(6,0))
            s2.pack_propagate(False)
            treev = ttk.Treeview(s2, column=tuple('c'+str(i) for i in range(3)), show= 'headings', selectmode ='browse')
            verscrlbar = ttk.Scrollbar(s2,orient ="vertical",command = treev.yview)
            treev.pack(fill=BOTH,expand=True,side=LEFT)
            verscrlbar.pack(side =LEFT, fill =Y)
            treev.configure(yscrollcommand = verscrlbar.set)
            for i in range(3):
                treev.column("# "+str(i+1),anchor=CENTER,width=30)
                treev.heading("# "+str(i+1), text=('Amount','Due Date','Payment Date')[i])
            s3=Frame(self.f2,bg='#80deea')
            s3.pack(side=BOTTOM,fill=X)
            Button(s3,text="Make Payment ",font="comicsansms 12 bold",command=make_payment).grid(row=0,column=0,pady=4,padx=6)
            search()
        self.clearwid()
        u=("Profile","Room","Course","Payment","Log Out")
        for i in range(5):
            b=Button(self.menu,font='comicsansms 12 bold',text=u[i],bg='#00acc1',fg='white', disabledforeground="white",activeforeground='white',activebackground='#80deea', relief=FLAT,width=16,command=lambda isam=i:buttoncheck3(isam))
            b.place(x=0,y=76+38*i)
            self.buttons.append(b)
        self.buttons[0].config(state="disabled",bg="#80deea")
        show_details(0,'student')
    def admin(self):
        def resize_ui(w,can,canf_id):
            if w<1:
                w=1
            u=can.winfo_children()[0].winfo_children()
            can.winfo_children()[0].columnconfigure(tuple(range(15)), weight=0)
            num_columns =1+(w>500)+(w>700)+(w>1300)+(w>1900)
            for i in range(5):
                r=4*(i // num_columns)
                c=3*(i%num_columns)
                u[4*i].config(font="comicsansms "+str(int(w//36))+" bold")
                u[4*i].grid(row=r,column=c+1)
                pil_img = Image.open(f"res//card{i+1}.png").convert("RGBA")
                pil_img = pil_img.resize((max(1,w//6),max(1,w//6)), Image.Resampling.LANCZOS)
                self.logo_hms[i+1] = ImageTk.PhotoImage(pil_img)
                u[4*i+1].config(image=self.logo_hms[i+1])
                u[4*i+1].grid(row=r+1,column=c+1)
                u[4*i+2].grid(row=r+1,column=c+2)
                u[4*i+3].grid(row=r+2,column=c+1)
            can.winfo_children()[0].rowconfigure(tuple(range(3* num_columns)), weight=1)
            can.winfo_children()[0].columnconfigure(tuple(range(0,3*num_columns+1)), weight=1)
            self.f2.rowconfigure(tuple(range(3* num_columns)), weight=0)
            self.f2.rowconfigure(0, weight=1)
            can.config(scrollregion=(0, 0, w, can.winfo_children()[0].winfo_height()))
            can.itemconfig(canf_id, width=w)
        def buttoncheck2(t,s=False):   
            self.heading.config(text=u[t].upper())
            if self.buttons[0]['state']=='disabled':
                self.f2.unbind("<Configure>")
            for i in range(len(self.buttons)):
                self.buttons[i].config(state="disabled"if i==t else "normal")
                self.buttons[i].config(bg="#80deea"if i==t else "#00acc1")
            self.f2.rowconfigure(tuple(range(12)), weight=0)
            self.f2.columnconfigure(tuple(range(10)), weight=0)
            if s:
                show('student',True)
            elif t==0:
                dashboard()
            elif t==1:
                admindetails(show)
            elif t==6:
                database_set()
            elif t==7:
                self.logout()
            else:
                show(u[t][:-1].lower())
        def addmodify(table_name,col,rec):
            def update():
                if 2 in self.currentuser[3] or 6 in self.currentuser[3] or 10 in self.currentuser[3]:
                    fty=[entry.get() for entry in entries]
                    if table_name=='student':
                        fty.pop()
                    fty.append(rec[0])
                    update_success=False
                    if ('' not in fty) and ('Please select...' not in fty or (table_name=='student' and fty[2]!='Please select...')):
                        if table_name=='student':
                            for i in (1,3,4,6):
                                fty[i]=fty[i].lower().strip()
                            if not fty[0].isdigit():
                                self.update_status("Please Enter Registration Number In Numbers")
                            elif self.name_check3(fty[1]) or self.name_check3(fty[3]) or self.name_check3(fty[4]):
                                self.update_status("Please Enter Valid Name Only")
                            elif self.name_check2(fty[6]):
                                self.update_status("Please Enter Valid Address")
                            elif not fty[7].isdigit() or len(fty[7])!=10:
                                self.update_status("Please Enter 10 Numbers In Phone number")
                            elif self.dobcheck(fty[5],'DOB'):
                                fty[0]=int(fty[0])
                                fty[2]='M' if fty[2]=='Male' else 'F'
                                fty[5]=self.dobconv(fty[5])
                                fty[9]=None if fty[9]=='Please select...' else ty[2][ty[1].index(fty[9])]
                                fty[8]=None if fty[8]=='Please select...' else fty[8]
                                fty[10]=int(rec[11]=='Verified')
                                fty=tuple(fty)
                                ftys=f"update Student set Registration_no=%s,Name=%s,Gender=%s,Father_Name=%s,Mother_Name=%s,DOB=%s,Address=%s,Phone_no=%s,Room_id=%s,Course_id=%s,Verify=%s where Student_id=%s"
                                update_success,fty=self.server.sqlexeother(ftys,table_name,fty,col[1])
                                self.update_status(fty)
                        elif table_name=='room':
                            fty[2]=fty[2].strip()
                            if self.name_check4(fty[2].lower()):
                                self.update_status('Please Enter Valid Characters 0-9,A-Z,a-z, ,-,_ In Block Name')
                            elif fty[1].isdigit():
                                fty=tuple(('Y'if fty[x]=='Yes' else'N')if x in(3,5,6,7) else fty[x] for x in range(8))
                                ftys=f"update Room set Room_no ={fty[1]}, Block='{fty[2]}', Available='{fty[3]}', Beds='{fty[4]}', AC='{fty[5]}', Wifi='{fty[6]}', TV='{fty[7]}' where Room_id={fty[0]}'"
                                update_success,fty=self.server.sqlexeother(ftys,table_name,fty,(col[1],col[2]))
                                self.update_status(fty)
                            else:
                                self.update_status('Room Number In Digits')
                        elif table_name=='course':
                            fty[1]=fty[1].strip().lower()
                            if self.name_check2(fty[1]):
                                self.update_status("Please Enter Valid Characters 0-9,A-Z,a-z, ,_ In Course Name")
                            elif entries[0].get().strip().lower()=='na':
                                self.update_status("Please Enter Other Course Name")
                            else:
                                ftys=f"update Course set Course_Name ='{fty[1]}', Duration='{fty[2]}' where Course_id='{fty[0]}'"
                                update_success,fty=self.server.sqlexeother(ftys,table_name,fty,col[1])
                                self.update_status(fty)
                        if update_success:
                            clear()
                    else:
                        self.update_status('Please Fill All Entries')
                else:
                    self.update_status('You Have No Permission To Update '+table_name)
            def add():
                if 1 in self.currentuser[3] or 5 in self.currentuser[3] or 9 in self.currentuser[3]:
                    fty=[entry.get() for entry in entries]
                    if ('' not in fty) and ('Please select...' not in fty or (table_name=='student' and fty[2]!='Please select...')):
                        fty.insert(0,self.id_gen(table_name)[0])
                        add_success=False
                        if table_name=='student':
                            for i in (2,4,5,7):
                                fty[i]=fty[i].lower().strip()
                            if not fty[1].isdigit():
                                self.update_status("Please Enter Registration Number In Numbers")
                            elif self.name_check3(fty[2]) or self.name_check3(fty[4]) or self.name_check3(fty[5]):
                                self.update_status("Please Enter Valid Name Only")
                            elif self.name_check2(fty[7]):
                                self.update_status("Please Enter Valid Address")
                            elif not fty[8].isdigit() or len(fty[8])!=10:
                                self.update_status("Please Enter 10 Numbers In Phone number")
                            elif self.name_check1(fty[12].lower().strip()):
                                self.update_status("Please Enter Valid Characters 0-9,A-Z,a-z, ,_,$ In Password")
                            elif self.dobcheck(fty[6],'DOB'):
                                fty[1]=int(fty[1])
                                fty[3]='M' if fty[3]=='Male' else 'F'
                                fty[6]=self.dobconv(fty[6])
                                fty[10]=None if fty[10]=='Please select...' else ty[2][ty[1].index(fty[10])]
                                fty[9]=None if fty[9]=='Please select...' else fty[9]
                                fty[11],fty[12]=fty[12],1
                                fty=tuple(fty)
                                add_success,fty=self.server.sqlsetnew(fty,table_name,col[1])
                                self.update_status(fty)
                        elif table_name=='room':
                            fty[2]=fty[2].strip()
                            if self.name_check4(fty[2].lower()):
                                self.update_status('Please Enter Valid Characters 0-9,A-Z,a-z, ,-,_ In Block Name')
                            elif fty[1].isdigit():
                                fty=tuple(('Y'if fty[x]=='Yes' else'N')if x in(3,5,6,7) else fty[x] for x in range(8))
                                add_success,fty=self.server.sqlsetnew(fty,table_name,(col[1],col[2]))
                                self.update_status(fty)
                            else:
                                self.update_status('Room Number In Digits')         
                        elif table_name=='course':
                            fty[1]=fty[1].strip().lower()
                            if self.name_check2(fty[1]):
                                self.update_status("Please Enter Valid Characters 0-9,A-Z,a-z, ,_ In Course Name")
                            elif entries[0].get().strip().lower()=='na':
                                self.update_status("Please Enter Other Course Name")
                            else:
                                fty=tuple(fty)
                                add_success,fty=self.server.sqlsetnew(fty,table_name,col[1])
                                self.update_status(fty)
                        if add_success:
                            clear()
                    else:
                        self.update_status('Please Fill All Entries')
                else:
                    self.update_status('You Have No Permission To Add '+table_name)
            def search():
                nonlocal rec
                if 2 in self.currentuser[3] or 6 in self.currentuser[3] or 10 in self.currentuser[3]:
                    if table_name=='student':
                        if entries[0].get().isdigit():
                            i=self.server.sqlgetallrec(f"student s LEFT JOIN course c on s.course_id=c.course_id where Registration_No={entries[0].get()} and s.course_id is null",'s.Student_id,s.Registration_No,s.Name,s.Gender,s.Father_Name,s.Mother_Name,s.DOB,s.Address,s.Phone_no,s.Room_id,c.Course_name,s.Verify')
                            if len(i)==1:
                                rec=list(i[0])
                                rec[11]='Verified' if i[0][11]==1 else 'Pending'
                                clear()
                                for d in range(11):
                                    if d==2:
                                        entries[d].current(1+(i[0][d+1]=='M'))
                                    elif d==5:
                                        entries[d].insert(0,self.dobconv(str(i[0][d+1])))
                                    elif d==10 and i[0][d+1]==1:
                                        entries[10]=Entry(self.f2,disabledforeground='black')
                                        entries[10].insert(0,'Verified')
                                        entries[10].config(state='disabled')
                                        entries[10].grid(row=10,column=1,sticky='ew',padx=8)
                                    elif d==10:
                                        entries[10]=Frame(self.f2,bg='#80deea')
                                        Button(entries[10],font='comicsansms 8',text='Accept',command=lambda : verify_reg(True)).grid(row=0,column=0)
                                        Button(entries[10],font='comicsansms 8',text='Reject',command=lambda : verify_reg(False)).grid(row=0,column=1)
                                        entries[10].columnconfigure((0,1),weight=1)
                                        entries[10].grid(row=10,column=1,sticky='ew',padx=8)
                                    elif d in (8,9):
                                        if i[0][d+1]==None or rec=='':
                                            entries[d].current(0)
                                        else:
                                            entries[d].current(ty[d-8].index(i[0][d+1].title() if d==9 else i[0][d+1])+1)
                                    elif d in (0,7):
                                        entries[d].insert(0,i[0][d+1])
                                    else:
                                        entries[d].insert(0,i[0][d+1].title())
                                m.config(text='Modify',command=update)
                                a.config(state='disabled')
                            else:
                                self.update_status("Student Not Found")
                        else:
                            self.update_status("Please Enter Registration Number In Numbers")
                    elif table_name=='course':
                        if self.name_check2(entries[0].get().strip().lower()):
                            self.update_status("Please Enter Valid Characters 0-9,A-Z,a-z, ,_ In Course Name")
                        elif entries[0].get().strip().lower()=='na':
                            self.update_status("Please Enter Other Course Name")
                        else:
                            i=self.server.sqlgetallrec(f"course where course_name='{entries[0].get().strip().lower()}'")
                            if len(i)==1:
                                rec=list(i[0])
                                clear()
                                entries[0].insert(0,i[0][1])
                                entries[1].set(i[0][2])
                                m.config(text='Modify',command=update)
                                a.config(state='disabled')
                            else:
                                self.update_status("Course Not Found")
                    elif table_name=='room':
                        if self.name_check4(entries[1].get().strip().lower()):
                            self.update_status('Please Enter Valid Characters 0-9,A-Z,a-z, ,-,_ In Block Name')
                        elif entries[0].get().isdigit():
                            i=self.server.sqlgetallrec(f"room where room_no={entries[0].get()} and block='{entries[1].get().strip().lower()}'")
                            if len(i)==1:
                                rec=list(i[0])
                                clear()
                                for d in range(7):
                                    if d in(0,1):
                                        entries[d].insert(0,i[0][d+1])
                                    elif d==3:
                                        t2.set(i[0][4])
                                    elif i[0][d+1]=='Y':
                                        entries[d].current(1)
                                    else:
                                        entries[d].current(2)
                                m.config(text='Modify',command=update)
                                a.config(state='disabled')
                            else:
                                self.update_status("Room Not Found")
                        else:
                            self.update_status('Room Number In Digits') 
                else:
                    self.update_status('You Have No Permission To Update '+table_name)
            def clear():
                for i in range(len(col)-1+(table_name=='student')):
                    if (i==1 and table_name=='course') or (i==3 and table_name=='room'):
                        entries[i].set(1)
                    elif (i in(2,8,9) and table_name=='student') or (i in(2,4,5,6) and table_name=='room'):
                        entries[i].set('Please select...')
                    elif i==10 and table_name=='student':
                        entries[10].destroy()
                        e=Entry(self.f2,disabledforeground='black')
                        e.insert(0,'Verified')
                        e.config(state='disabled')
                        e.grid(row=10,column=1,sticky='ew',padx=8)
                        entries[10]=e
                    else:
                        entries[i].delete(0,END)
                m.config(text='Search',command=search)
                a.config(state='normal')
            def back():
                show(table_name)
            def verify_reg(v):
                if v:
                    self.server.sql_student_verify(rec[0])
                    entries[10].destroy()
                    entries[10]=Entry(self.f2,disabledforeground='black')
                    entries[10].insert(0,'Verified')
                    entries[10].config(state='disabled')
                    entries[10].grid(row=10,column=1,sticky='ew',padx=8)
                    rec[10]='Verified'
                else:
                    self.server.sqlsetdel(table_name,rec[0])
                    clear()
            self.stringstatus=f"Please Enter Details To Add / Modify Of {table_name.capitalize()}"
            self.instance_status()
            entries=[]
            self.clearm()
            a=Button(self.f2,font='comicsansms 12 bold',text='Add',state='normal' if rec=='' else 'disabled',command=add)
            a.grid(row=0,column=2,sticky='ew')
            m=Button(self.f2,font='comicsansms 12 bold',text='Search' if rec=='' else 'Modify',command=search if rec=='' else update)
            m.grid(row=1,column=2,sticky='ew')
            Button(self.f2,font='comicsansms 12 bold',text='Clear',command=clear).grid(row=2,column=2,sticky='ew')
            Button(self.f2,font='comicsansms 12 bold',text='Back',command=back).grid(row=3,column=2,sticky='ew')
            for i in range(len(col)-1):
                Label(self.f2,text=col[i+1]+':',font="comicsansms 12 bold",bg='#80deea').grid(row=i,column=0,sticky='w',padx=6)
            if table_name=='student':
                Label(self.f2,text='Password:',font="comicsansms 12 bold",bg='#80deea').grid(row=11,column=0,sticky='w',padx=6)
            self.f2.rowconfigure(tuple(range(len(col)-1+(table_name=='student'))),weight=1)
            self.f2.columnconfigure(1,weight=2)
            self.f2.columnconfigure((0,2),weight=1)
            ty=self.server.sqlgetstublock(table_name)
            for i in range(len(col)-1+(table_name=='student')):
                if table_name=='student' and i in (2,8,9,10):
                    if i==2:
                        e= ttk.Combobox(self.f2,values=['Please select...','Male','Female'],state='readonly')
                        if rec=='':
                            e.current(0)
                        elif rec[i+1]=='Male':
                            e.current(1)
                        elif rec[i+1]=='Female':
                            e.current(2)
                    elif i==10 and (rec=='' or rec[i+1]=='Verified'):
                        e=Entry(self.f2,disabledforeground='black')
                        e.insert(0,'Verified')
                        e.config(state='disabled')
                    elif i==10 and rec[i+1]=='Pending':
                        e=Frame(self.f2,bg='#80deea')
                        Button(e,font='comicsansms 8',text='Accept',command=lambda : verify_reg(True)).grid(row=0,column=0)
                        Button(e,font='comicsansms 8',text='Reject',command=lambda : verify_reg(False)).grid(row=0,column=1)
                        e.columnconfigure((0,1),weight=1)
                    else:
                        e= ttk.Combobox(self.f2,state='readonly')
                        e['values']=['Please select...']+ty[i-8]
                        e.current(ty[i-8].index(rec[i+1])+1 if rec!='' and rec[i+1]!='NA' else 0)
                elif table_name=='room' and 0<i<7:
                    if i==3:
                        t2=StringVar()
                        e=Spinbox(self.f2, from_=0, to=10,state='readonly',wrap=True,textvariable=t2)
                        if rec!='':
                            t2.set(rec[i+1])
                    elif i==1:
                        e= ttk.Combobox(self.f2,values=[''])
                        if rec=='':
                            e.current(0)
                        else:
                            e.insert(0,rec[i+1])
                        e['values']=ty
                    else:
                        e= ttk.Combobox(self.f2,values=['Please select...','Yes','No'],state='readonly')
                        if rec=='':
                            e.current(0)
                        elif rec[i+1]=='Y':
                            e.current(1)
                        elif rec[i+1]=='N':
                            e.current(2)
                elif table_name=='course' and i==1:
                    if i==1:
                        t2=StringVar()
                        e=Spinbox(self.f2, from_=1,state='readonly', to=6,wrap=True,textvariable=t2)
                        if rec!='':
                            t2.set(rec[i+1])
                else:
                    e=Entry(self.f2)
                    if rec!='' and (table_name!='student' or i!=11):
                        e.insert(0,rec[i+1])
                e.grid(row=i,column=1,sticky='ew',padx=8)
                if  (i==1 and table_name=='course') or (i==3 and table_name=='room'):
                    entries.append(t2)
                else:    
                    entries.append(e)
        def show(table_name,pending_search=False):
            def clear_all():
                for item in treev.get_children():
                    treev.delete(item)
            def clear_all2():
                for item in treev2.get_children():
                    treev2.delete(item)
                e1.delete(0,END)
                e2.delete(0,END)
                e3.delete(0,END)
            def clear_all3():
                for item in treev2.get_children():
                    treev2.delete(item)
                e1.delete(0,END)
            def search():
                clear_all()
                if table_name in('student','course','room','payment') and 4*('student','course','room','payment').index(table_name) not in self.currentuser[3]:
                    self.update_status('You have Not Permission To View '+table_name.title())
                else:
                    if table_name=='role':
                        data=[]
                        for i in t[1]:
                            if cbox.get()=='Please select...' or e.get().lower() in i:
                                data.append([i.title()])
                    elif cbox.get()!='Please select...':
                        if table_name=="user":
                            if cbox.get()=='role':
                                data=list(self.server.sqlsearchrec('user a,role r','a.role_id=r.role_id and r.role_name',e.get().lower(),'a.name,r.role_name'))
                            else:
                                data=list(self.server.sqlsearchrec('user a,role r','a.role_id=r.role_id and a.'+cbox.get(),e.get().lower(),'a.name,r.role_name'))
                        elif table_name=='payment':
                            data=list(self.server.sqlsearchpaymentrec(cbox.get(),e.get()))
                            clear_all2()
                        elif table_name=='student':
                            data=list(self.server.sqlsearch_student_rec(cbox.get(),e.get()))
                        else:
                            data=list(self.server.sqlsearchrec(table_name,cbox.get(),e.get()))
                    elif table_name=="user":
                        data=list(self.server.sqladmingetallrec())
                    elif table_name=="payment":
                        data=list(self.server.sqlgetallpaymentrec())
                        clear_all2()
                    elif table_name=="student":
                        data=list(self.server.sqlgetall_student_rec())
                    else:
                        data=list(self.server.sqlgetallrec(table_name))
                    for row in data:
                        row=list(row)
                        if table_name=='student':
                            row[6]=self.dobconv(str(row[6]))
                            row[3]='Male' if row[3]=='M' else 'Female'
                            row[9]='NA' if row[9] is None else row[9]
                            row[11]='Verified' if row[11]==1 else 'Pending'
                            for i in (2,4,5,7,10):
                                if row[10] is None:
                                    row[10]='NA'
                                else:
                                    row[i]=row[i].title()
                        elif table_name == 'payment':
                            if row[2] is None:
                                row[2]='NA'
                            if row[3] is None:
                                row[3]='NA'
                        elif table_name in ('course','user'):
                            row[1]=row[1].title()
                        treev.insert('',END, values=row)
            def deleterec():
                selectedItem = treev.item(treev.focus())['values']
                if selectedItem in ([],''):
                    self.update_status('No Record Selected To Remove')
                elif table_name=='user' and selectedItem[1]=='Lead Administrator':
                    self.update_status('You Cannot Remove The Lead Administrator')
                elif table_name in ('student','course','room','payment') and (3 not in self.currentuser[3] or 7 not in self.currentuser[3] or 11 not in self.currentuser[3] or 15 not in self.currentuser[3]):
                    self.update_status('You have Not Permission To Remove '+table_name.title())
                else:
                    self.update_status(self.server.sqlsetdel(table_name,selectedItem[0]))
                    search()
            def addmodifyrec():
                addmodify(table_name,reccol,treev.item(treev.focus())['values'])
            def addnewadmin():
                newadmin=(e1.get().strip(),e2.get().strip(),0)
                if '' in newadmin:
                    self.update_status('Please Fill The Entries To Add New Admin')
                elif self.name_check1(newadmin[0]) or self.name_check1(newadmin[1]):
                    self.update_status('Please Enter Valid Characters Only 0-9,a-z,A-Z,$,_')
                else:
                    s=self.server.sqlsetnew(newadmin,'user','name')
                    self.update_status(s)
                    search()
            def update_admin():
                selectedItem = treev.item(treev.focus())['values']
                if selectedItem in ([],''):
                    self.update_status('No Record Selected To Update Role')
                else:
                    self.update_status(self.server.sqlupdaterole(selectedItem[0],t[0][cbox2.current()]))
                    search()
            def on_row_select(e):
                clear_all2()
                selectedItem=treev.item(treev.focus())['values']
                if selectedItem not in ([],''):
                    data=list(self.server.sqlgetpayments(selectedItem[0]))
                    for row in data:
                        row=list(row)
                        row[2]=self.dobconv(str(row[2]))
                        row[3]='Pending' if row[3] is None else self.dobconv(str(row[3]))
                        treev2.insert('',END, values=row)
            def on_row_select2(e):
                clear_all3()
                selectedItem=treev.item(treev.focus())['values']
                if selectedItem:
                    data=t[2][t[1].index(selectedItem[0].lower())]
                    if data is None:
                        treev2.insert('',END, values=("No Permissions",))
                    co=[]
                    if t[0][t[1].index(selectedItem[0].lower())]!=0:
                        data=None if data==None else list(map(int,data.split(',')))
                        for row in range(len(self.permission)):
                            if data is not None and row in data:
                                treev2.insert('',END, values=(self.permission[row],))
                            else:
                                co.append(self.permission[row])
                    cbox2['values']=['Please select...']+co
            def new_payment():
                if 13 in self.currentuser[3]:
                    selectedItem=treev.item(treev.focus())['values']
                    if selectedItem in ([],''):
                        self.update_status('No Student Selected')
                    else:
                        a=e1.get()
                        b=e2.get()
                        if not a.replace('.','',1).isdigit():
                            self.update_status('Please Enter The Valid Amount')
                        elif b=='':
                            self.update_status('Please Fill All Entries')
                        elif self.dobcheck(b,'Due Date'):
                            i=self.id_gen('payment')
                            self.server.sqlnewpayment((i,selectedItem[0],round(float(a),2),self.dobconv(b)))
                            self.update_status('New Payment Added')
                            on_row_select('')
                else:
                    self.update_status('You have Not Permission To Add Payment')
            def del_payment():
                if 15 in self.currentuser[3]:
                    selectedItem=treev2.item(treev2.focus())['values']
                    if selectedItem in ([],''):
                        self.update_status('No Payment Selected')
                    else:
                        self.server.sqldelpayment(selectedItem[0])
                        self.update_status('Payment Removed Successfully')
                        on_row_select('')
                else:
                     self.update_status('You have Not Permission To Remove Payment')
            def update_payment():
                selectedItem=treev2.item(treev2.focus())['values']
                p=e3.get()
                if selectedItem in ([],''):
                    self.update_status('No Payment Selected')
                elif p=='':
                    self.update_status('Please Fill All Entries')
                elif self.dobcheck(p,'Payment Date'):
                    self.server.sqlupadatepayment(self.dobconv(p),selectedItem[0])
                    self.update_status('Payment Updated Successfully')
                    on_row_select('')
            def addnewrole():
                s=e1.get().strip().lower()
                if s=='':
                    self.update_status('Please Enter The Role Name')
                elif self.name_check2(s):
                    self.update_status('Please Enter Valid Characters 0-9,A-Z,a-z, ,_ In Role Name')
                elif s in t:
                    self.update_status('Role Already Exist')
                else:
                    for i in range(len(t[0])):
                        if i+2!= t[0][i]:
                            rid=i+2
                            break
                    else:
                        rid=i+3
                    self.server.sqladdnewrole(rid,s)
                    t[0].append(rid)
                    t[1].append(s)
                    t[2].append(None)
                    e1.delete(0, 'end')
                    self.update_status('New Role Added Successfully')
                    search()
            def removerole():
                selectedItem=treev.item(treev.focus())['values']
                if selectedItem:
                    selectedItem=t[1].index(selectedItem[0].lower())
                    if t[0][selectedItem] in (0,1):
                        self.update_status('This Role Cannot Be Removed')
                    else:
                        self.server.sqlremoverole(t[0][selectedItem])
                        self.update_status('Role Removed Successfully')
                        t[0].pop(selectedItem)
                        t[1].pop(selectedItem)
                        t[2].pop(selectedItem)
                        search()
                else:
                    self.update_status('No Role Selected')
            def remove_permissions():
                selectedItem=treev2.item(treev2.focus())['values']
                if selectedItem[0]=="No Permissions":
                    self.update_status('No Permission To Remove From This Role')
                elif selectedItem:
                    selper=self.permission.index(selectedItem[0])
                    selectedItem=treev.item(treev.focus())['values'][0]
                    if selectedItem=='Lead Administrator':
                        self.update_status('Permission Cannot Remove From Lead Administrator')
                    else:
                        selectedItem=t[1].index(selectedItem.lower())
                        per=t[2][selectedItem]
                        per=list(map(int,per.split(',')))
                        if selper%4==0 and ((table_menu=='payment' and selper+1 in self.currentuser[3]) or selper+2 in self.currentuser[3] or selper+3 in self.currentuser[3]):
                            self.update_status('Removing This Will Also Affects Remove And Update Access')
                        else:
                            per.remove(selper)
                            per=','.join(map(str,per)) if per else None
                            self.server.sqludpatepermission(per,t[0][selectedItem])
                            t[2][selectedItem]=per
                            on_row_select2(None)
                            self.update_status('Role Removed Successfully')
                else:
                    self.update_status('No Permission Selected')
            def add_permissions():
                selectedItem=cbox2.get()
                if selectedItem != 'Please select...':
                    selper=self.permission.index(selectedItem)
                    selectedItem=t[1].index(treev.item(treev.focus())['values'][0].lower())
                    per=t[2][selectedItem]
                    per=[] if per is None else list(map(int,per.split(',')))
                    if (selper>12 or (selper%4)>1) and 4*(selper//4) not in per:
                        for i in range(len(per)):
                            if 4*(selper//4)<per[i]:
                                per.insert(i,4*(selper//4))
                            break
                        else:
                            per.append(4*(selper//4))
                    for i in range(len(per)):
                        if selper<per[i]:
                            per.insert(i,selper)
                            break
                    else:
                        per.append(selper)
                    per=','.join(map(str,per))
                    self.server.sqludpatepermission(per,t[0][selectedItem])
                    t[2][selectedItem]=per
                    on_row_select2(None)
                    cbox2.current(0)
                    self.update_status('New Permission Added Successfully')
                else:
                    self.update_status('No Permission Selected')
            def back_db():
                buttoncheck2(6)
            self.clearm()
            self.stringstatus="Showing Records Of "+("Administrators" if table_name=="user" else (table_name+'s').capitalize())
            self.instance_status()
            if table_name=="user":
                reccol=("Name","Role")
            elif table_name=="payment":
                reccol=("Student_id","Name","Room_id","Course_Name")
            elif table_name=="role":
                reccol=("Role Name",)
            elif table_name=="student":
                reccol=('Student_id','Registration_No','Name','Gender','Father_Name','Mother_Name','DOB','Address','Phone_no','Room_id','Course_Name','Verify')
            else:
                reccol=self.server.sqlgetcol(table_name)
            s1=Frame(self.f2,bg='#80deea',height=30)
            s1.pack(side=TOP,fill=X)
            Label(s1,text="Search By :",font="comicsansms 12 bold",bg='#80deea').grid(row=0,column=0,pady=4)
            cbox=ttk.Combobox(s1,values=['Please select...']+list(reccol),state='readonly',width=19)
            cbox.grid(row=0,column=1,pady=4)
            cbox.current(0)
            Button(s1,text="Search ",font="comicsansms 12 bold",command=search).grid(row=0,column=3,pady=4,padx=6)
            e=Entry(s1)
            e.grid(row=0,column=2,pady=4,padx=6,sticky='ew')
            s1.columnconfigure(2,weight=1)
            s2=Frame(self.f2,bg='#80deea')
            s2.pack(fill=BOTH,expand=True,padx=(6,0))
            s2.pack_propagate(False)
            treev = ttk.Treeview(s2, column=tuple('c'+str(i) for i in range(len(reccol))), show= 'headings', selectmode ='browse')
            verscrlbar = ttk.Scrollbar(s2,orient ="vertical",command = treev.yview)
            treev.pack(fill=BOTH,expand=True,side=LEFT)
            verscrlbar.pack(side =LEFT, fill =Y)
            treev.configure(yscrollcommand = verscrlbar.set)
            for i in range(len(reccol)):
                treev.column("# "+str(i+1),anchor=CENTER,width=30)
                treev.heading("# "+str(i+1), text=reccol[i])
            if pending_search:
                cbox.current(12)
                e.insert(0,'Pending')
            
            if table_name=='payment':
                treev.bind('<<TreeviewSelect>>', on_row_select)
                treev2 = ttk.Treeview(s2, column=tuple('c'+str(i) for i in range(4)), show= 'headings', selectmode ='browse')
                verscrlbar2 = ttk.Scrollbar(s2,orient ="vertical",command = treev2.yview)
                verscrlbar2.pack(side =RIGHT, fill =Y)
                treev2.pack(fill=BOTH,expand=True,side=RIGHT)
                treev2.configure(yscrollcommand = verscrlbar2.set)
                for i in range(4):
                    treev2.column("# "+str(i+1),anchor=CENTER,width=30)
                    treev2.heading("# "+str(i+1), text=('Payment id','Amount','Due Date','Payment Date')[i])
            elif table_name=="role":
                treev.bind('<<TreeviewSelect>>', on_row_select2)
                treev2 = ttk.Treeview(s2, column=('c0',), show= 'headings', selectmode ='browse')
                verscrlbar2 = ttk.Scrollbar(s2,orient ="vertical",command = treev2.yview)
                verscrlbar2.pack(side =RIGHT, fill =Y)
                treev2.pack(fill=BOTH,expand=True,side=RIGHT)
                treev2.configure(yscrollcommand = verscrlbar2.set)
                treev2.column("# 1",anchor='w',width=30)
                treev2.heading("# 1", text="Permissions")
                t=self.server.sqlgetrolename()
            s3=Frame(self.f2,bg='#80deea')
            s3.pack(side=BOTTOM,fill=X)
            if table_name=="user":
                Label(s3,text="Name :",font="comicsansms 12 bold",bg='#80deea').grid(row=0,column=0,pady=4,sticky='w')
                Label(s3,text="Password :",font="comicsansms 12 bold",bg='#80deea').grid(row=1,column=0,pady=4,sticky='w')
                e1=Entry(s3)
                e1.grid(row=0,column=1,pady=4,padx=6,sticky='ew')
                e2=Entry(s3)
                e2.grid(row=1,column=1,pady=4,padx=6,sticky='ew')
                Button(s3,text="Back",font="comicsansms 12 bold",command=back_db).grid(row=2,column=0,pady=4)
                Button(s3,text="Add New Admin",font="comicsansms 12 bold",command=addnewadmin).grid(row=2,column=1,pady=4)
                Label(s3,text=" ",font="comicsansms 12 bold",bg='#80deea').grid(row=0,column=2,rowspan=3)
                t=self.server.sqlgetrolename(' where role_id!=1')
                cbox2=ttk.Combobox(s3,values=t[1],state='readonly')
                cbox2.grid(row=0,column=3,pady=4,padx=4,sticky='we')
                cbox2.current(1)
                Button(s3,text="Update Role Admin",font="comicsansms 12 bold",command=update_admin).grid(row=1,column=3,columnspan=2,pady=4,padx=4,sticky='we')
                Button(s3,text="Remove Admin",font="comicsansms 12 bold",command=deleterec).grid(row=2,column=3,columnspan=2,pady=4,padx=4,sticky='we')
                s3.columnconfigure(2,weight=1)
            elif table_name=='payment':
                Label(s3,text="Amount :",font="comicsansms 12 bold",bg='#80deea').grid(row=0,column=0,pady=4,sticky='w')
                Label(s3,text="Due Date :",font="comicsansms 12 bold",bg='#80deea').grid(row=1,column=0,pady=4,sticky='w')
                e1=Entry(s3)
                e1.grid(row=0,column=1,pady=4,padx=6,sticky='ew')
                e2=Entry(s3)
                e2.grid(row=1,column=1,pady=4,padx=6,sticky='ew')
                Button(s3,text="Add Payment",font="comicsansms 12 bold",command=new_payment).grid(row=2,column=0,columnspan=2,pady=4)
                Label(s3,text=" ",font="comicsansms 12 bold",bg='#80deea').grid(row=0,column=2,rowspan=3)
                Label(s3,text="Payment Date :",font="comicsansms 12 bold",bg='#80deea').grid(row=0,column=3,pady=4,sticky='w')
                e3=Entry(s3)
                e3.grid(row=0,column=4,pady=4,padx=6,sticky='ew')
                Button(s3,text="Update Payment",font="comicsansms 12 bold",command=update_payment).grid(row=1,column=3,columnspan=2,pady=4,padx=4,sticky='we')
                Button(s3,text="Remove Payment",font="comicsansms 12 bold",command=del_payment).grid(row=2,column=3,columnspan=2,pady=4,padx=4,sticky='we')
                s3.columnconfigure(2,weight=1)
            elif table_name=="role":
                Label(s3,text="Role Name:",font="comicsansms 12 bold",bg='#80deea').grid(row=0,column=0,sticky='w',padx=6,pady=4)
                e1=Entry(s3)
                e1.grid(row=0,column=1,sticky='ew',padx=6,pady=4)
                Button(s3,text="Add New Role",font="comicsansms 12 bold",command=addnewrole).grid(row=1,column=0,columnspan=2,sticky="ew",padx=6,pady=4)
                Button(s3,text="Back",font="comicsansms 12 bold",command=back_db).grid(row=2,column=0,pady=4,padx=6)
                Button(s3,text="Delete Role",font="comicsansms 12 bold",command=removerole).grid(row=2,column=1,sticky="ew",pady=4)
                Label(s3,text="Permission:",font="comicsansms 12 bold",bg='#80deea').grid(row=0,column=3,sticky='ew',padx=6,pady=4)
                cbox2=ttk.Combobox(s3,values=['Please select...'],state='readonly')
                cbox2.grid(row=0,column=4,sticky="ew",padx=6,pady=4)
                cbox2.current(0)
                Button(s3,text="Add New Permission",font="comicsansms 12 bold",command=add_permissions).grid(row=1,column=3,columnspan=2,sticky="ew",padx=6,pady=4)
                Button(s3,text="Delete Permission",font="comicsansms 12 bold",command=remove_permissions).grid(row=2,column=3,columnspan=2,sticky="ew",padx=6,pady=4)
                s3.columnconfigure(2, weight=1)
            else:
                Button(s3,text="Add / Modify",font="comicsansms 12 bold",command=addmodifyrec).grid(row=0,column=0,pady=4)
                Button(s3,text="Delete",font="comicsansms 12 bold",command=deleterec).grid(row=0,column=1,pady=4)
                s3.columnconfigure((0,1),weight=1)
            search()
        def database_set():
            def delete_database():
                r = messagebox.askquestion("Delete Database", "Are you sure you want to delete the database?")
                if r == "yes":
                    self.update_status("Database Deleted Successfully")
                    logout()
            def choose_location():
                f = filedialog.askdirectory(title="Select Directory for File Location")
                if f:
                    fl1.delete(0,END)
                    fl1.insert(0,f)
                    self.update_status("Directory Selected For Export")
                else:
                    self.update_status("Directory Not Selected For Export")
            def choose_import_file():
                f = filedialog.askopenfilename(title="Select Database File", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
                if f:
                    fl2.delete(0,END)
                    fl2.insert(0,f)
                    self.update_status("File Selected For Import")
                else:
                    self.update_status("File Not Selected For Import")
            def import_file():
                if not os.path.exists(fl2.get()):
                    self.update_status("The File Path Does Not Exist.")
                else:
                    try:
                        with open(fl2.get(), mode ='r')as file:
                            data = list(csv.reader(file))
                        if table_menu2.get()!='user':
                            i=self.id_gen(table_menu2.get(),len(data))
                        for row in range(len(data)):
                            if table_menu2.get()=='Student':
                                if len(data[row])==13:
                                    for d in (1,3,4,6,10):
                                        data[row][d]=data[row][d].lower().strip()
                                data[row][8]=data[row][8].strip()
                                if len(data[row])!=13 or self.name_check3(data[row][1]) or data[row][2] not in('Male','Female') or self.name_check3(data[row][3]) or self.name_check3(data[row][4]) or self.name_check2(data[row][6]) or not data[row][7].isdigit() or len(data[row][7])!=10 or self.dobcheck(data[row][5],'DOB') or not (data[row][8].isdigit() or data[row][8]=='NA') or (self.name_check4(data[row][9]) and data[row][9]=='NA') or (self.name_check2(data[row][10]) and data[row][9]=='NA') or self.name_check1(data[row][11]) or data[row][12] not in('Verified','Pending'):
                                    self.update_status('Student Details Are Incorrect')
                                    break
                                elif len(self.server.sqlsearchrec('Student','registration_no',data[row][0]))!=0:
                                    self.update_status('Student Registration_no Already Exist')
                                    break
                                else:
                                    d=self.server.sql_student_name_roomcourse_id(data[row][7],data[row][8],data[row][9])
                                    if '' in d:
                                        self.update_status('Room or Course Not Found In Student Details')
                                        break
                                    else:
                                        data[row][7]=d[0][0]
                                        data[row][8]=d[0][1]
                                        data[row][1]='M' if data[row][1]=='Male' else 'F'
                                        data[row][12]=int(data[row][12]=='Verified')
                                        data[row][4]=self.dobconv(data[row][4])
                                        data[row].insert(0,i[row])
                                        data[row]=tuple(data[row])
                            elif table_menu2.get()=='Course':
                                if len(data[row])==2 and not self.name_check2(data[row][0].strip().lower()) and data[row][1].isdigit() and 0<int(data[row][1])<7:
                                    if len(self.server.sqlsearchrec('Course','Course_name',data[row][0]))==0:
                                        data[row][1]=int(data[row][1])
                                        data[row].insert(0,i[row])
                                        data[row]=tuple(data[row])
                                    else:
                                        self.update_status('Course Name Already Exist')
                                        break
                                else:
                                    self.update_status('Course Details Are Incorrect')
                                    break
                            elif table_menu2.get()=='Room':
                                if len(data[row])==7 and not self.name_check4(data[row][2].strip().lower()) and data[row][2] in('Y','N') and data[row][4] in('Y','N') and data[row][5] in('Y','N') and data[row][6] in('Y','N') and data[row][0].isdigit() and data[row][3].isdigit() and -1<int(data[row][3])<11:
                                    data[row][0]=int(data[row][0])
                                    data[row][3]=int(data[row][3])
                                    if self.server.sqlchecksameroomclone(data[row][0],data[row][1]): 
                                        data[row].insert(0,i[row])
                                        data[row]=tuple(data[row])
                                    else:
                                        self.update_status('Room No And Block Already Exist')
                                        break
                                else:
                                    self.update_status('Room Details Are Incorrect')
                                    break
                            elif table_menu2.get()=='Payment':
                                if len(data[row])==4 and not self.name_check3(data[row][0]) and data[row][1].replace('.','',1).isdigit() and self.dobcheck(data[row][2],'Payment Date') and (data[row][3]=='None' or self.dobcheck(data[row][3],'Due Date')):
                                    d=self.server.sqlgetallrec(f"'Student where registration_no={data[row][0].strip()}'",'student_id')
                                    if '' in d:
                                        self.update_status('Student Registration No Not Found In Payment Details')
                                        break
                                    else:
                                        data[row][0]=d[0][0]
                                        data[row][1]=round(float(data[row][1]),2)
                                        data[row][2]=self.dobconv(data[row][2])
                                        data[row][3]=None if data[row][3]=='None' else self.dobconv(data[row][3])
                                        data[row].insert(0,i[row])
                                        data[row]=tuple(data[row])
                                else:
                                    self.update_status('Payment Details Are Incorrect')
                                    break
                            elif table_menu2.get()=='role':
                                if len(data[row])==2 and not self.name_check4(data[row][0].strip().lower()) and not self.name_check5(data[row][1].strip()):
                                    if len(self.server.sqlsearchrec('Role','Role_name',data[row][0].strip().lower()))==0:
                                        data[row][0]=data[row][0].strip().lower()
                                        data[row][1]=data[row][1].strip() if data[row][1].strip() else None
                                        data[row].insert(0,i[row])
                                        data[row]=tuple(data[row])
                                    else:
                                        self.update_status('Role Name Already Exist')
                                        break
                                else:
                                    self.update_status('Role Details Are Incorrect')
                                    break
                            elif table_menu2.get()=='user':
                                if len(data[row])==3 and not self.name_check1(data[row][0].strip().lower()) and not self.name_check1(data[row][1].strip().lower()):
                                    if len(self.server.sqlsearchrec('user','name',data[row][0].strip().lower()))==0:
                                        d=self.server.sqlgetallrec(f"role where role_name='{data[row][2]}'",'role_id')
                                        if '' in d:
                                            self.update_status('Role Name Not Found In User Details')
                                            break
                                        else:
                                            data[row][0]=data[row][0].strip().lower()
                                            data[row][1]=data[row][1].strip().lower()
                                            data[row][2]=d[0][0]
                                            data[row]=tuple(data[row])
                                    else:
                                        self.update_status('User Name Already Exist')
                                        break
                                else:
                                    self.update_status('Admin Details Are Incorrect')
                                    break
                        else:
                            for row in data:
                                self.server.sql_import(table_menu2,row)
                            self.update_status('File Imported Successfully')
                    except:
                        self.update_status('File Unable To Import.Please Try Again Later')
            def export_file():
                t=[["Student", "Course", "Room", "Payment","role","user"],
                    ['s.registration_no,s.name,s.gender,s.father_name,s.mother_name,s.dob,s.address,s.phone_no,r.room_no,r.block,c.course_name,s.password,s.verify',
                    'course_name,duration','room_no,block,available,beds,ac,wifi,tv',
                    's.registration_no,p.amount,p.due_date,p.payment_date',
                    'role_name,permissions','u.name,u.pass,r.role_name'],
                    ['student s LEFT JOIN room r ON s.room_id=r.room_id LEFT JOIN course c ON s.course_id=c.course_id',
                    'course','room','student s,payment p where s.student_id=p.student_id',
                    'role','user u,role r where u.role_id=r.role_id']]
                if self.name_check4(fn.get().lower()):
                    self.update_status("Please Valid Charcters In File Name A-Z,a-z,0-9, ,-,_")
                elif not os.path.exists(fl1.get()):
                    self.update_status("The File Path Does Not Exist.")
                elif table_menu1.get()=='All':
                    f=fl1.get()+('/' if fl1.get()[-1]!='/' else '')+fn.get()
                    if not os.path.exists(f):
                        os.mkdir(f)
                    for i in range(6):
                        data=[list(o) for o in self.server.sqlgetallrec(t[2][i],t[1][i])]
                        for d in data:
                            if i==0:
                                d[2]='Male' if d[2]=='M' else 'Female'
                                d[5]=self.dobconv(str(d[5]))
                                d[8]='NA' if d[8] is None else d[8]
                                d[9]='NA' if d[9] is None else d[9]
                                d[10]='NA' if d[10] is None else d[10]
                                d[12]='Verified' if d[12]==1 else 'Pending'
                            elif i==3:
                                d[2]=self.dobconv(str(d[2]))
                                d[3]=self.dobconv(str(d[3]))
                        with open(f+'/'+t[0][i]+'.csv', mode='w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerows(data)
                    self.update_status("All File Exported Successfully")
                else:
                    i=t[0].index(table_menu1.get())
                    data=[list(o) for o in self.server.sqlgetallrec(t[2][i],t[1][i])]
                    for d in data:
                        if i==0:
                            d[2]='Male' if d[2]=='M' else 'Female'
                            d[5]=self.dobconv(str(d[5]))
                            d[8]='NA' if d[8] is None else d[8]
                            d[9]='NA' if d[9] is None else d[9]
                            d[10]='NA' if d[10] is None else d[10]
                        elif i==3:
                            d[2]=self.dobconv(str(d[2]))
                            d[3]=self.dobconv(str(d[3]))
                    f=fl1.get()+('/' if fl1.get()[-1]!='/' else '')+fn.get()
                    with open(f+'.csv', mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(data)
                    self.update_status("File Exported Successfully")
            def delete_database():
                r = messagebox.askquestion("Delete Database", "Are you sure you want to delete the all data from database?")
                if r == "yes":
                    self.server.sql_clear()
                    self.update_status('All Data Removed Successfully')
            self.clearm()
            self.stringstatus="Showing Number Of Records"
            self.instance_status()
            self.heading.config(text="DATABASE SETTING")
            lf1=LabelFrame(self.f2,text="Admin Operations",bg="#80deea")
            lf1.grid(padx=6,sticky="news",row=0,column=0,columnspan=2)
            Button(lf1,text="Update Admins",font="comicsansms 12 bold",command=lambda x="user": show(x)).grid(row=0,column=0)
            Button(lf1,text="Update Roles",font="comicsansms 12 bold",command=lambda x="role": show(x)).grid(row=0,column=1)
            lf1.columnconfigure((0,1),weight=1)
            lf1.rowconfigure(0,weight=1)

            lf2=LabelFrame(self.f2,text="Export Database",bg="#80deea")
            lf2.grid(padx=6,sticky="news",row=1,column=0)
            Label(lf2, text="Select Table:",bg="#80deea").grid(row=0,column=0, sticky="e")
            table_menu1=StringVar(lf2)
            table_menu1.set('All')
            OptionMenu(lf2,table_menu1,"Student", "Course", "Room", "Payment","role","user", "All").grid(row=0, column=1, pady=5)
            Label(lf2, text="File Name:",bg="#80deea").grid(row=1,column=0, sticky="e")
            fn=Entry(lf2)
            fn.grid(row=1,column=1,sticky='we',padx=6)
            Label(lf2, text="File Location:",bg="#80deea").grid(row=2,column=0, sticky="e")
            fl1=Entry(lf2)
            fl1.grid(row=2,column=1,sticky='we',padx=6)
            Button(lf2,text="Choose File Location",font="comicsansms 12 bold",command=choose_location).grid(row=3,column=1)
            Button(lf2,text="Export Database",font="comicsansms 12 bold",command=export_file).grid(row=4,column=1)
            lf2.columnconfigure((0,1),weight=1)
            lf2.rowconfigure((0,1,2,3,4),weight=1)
            
            lf3=LabelFrame(self.f2,text="Import Database",bg="#80deea")
            lf3.grid(padx=6,sticky="news",row=1,column=1)
            Label(lf3, text="Select Table:",bg="#80deea").grid(row=0,column=0, sticky="e")
            table_menu2=StringVar(lf3)
            table_menu2.set('Student')
            OptionMenu(lf3,table_menu2,"Student", "Course", "Room", "Payment","role","user").grid(row=0, column=1, pady=5)
            Label(lf3, text="File Location:",bg="#80deea").grid(row=1,column=0,sticky='e')
            fl2=Entry(lf3)
            fl2.grid(row=1,column=1,sticky='we',padx=6)
            Button(lf3,text="Choose File",font="comicsansms 12 bold",command=choose_import_file).grid(row=2,column=1)
            Button(lf3,text="Import Database",font="comicsansms 12 bold",command=import_file).grid(row=3,column=1)
            lf3.columnconfigure((0,1),weight=1)
            lf3.rowconfigure((0,1,2,3),weight=1)

            lf4=LabelFrame(self.f2,text="Delete Hostel Data",bg="#80deea")
            lf4.grid(padx=6,sticky="news",row=2,column=0,columnspan=2)
            Label(lf4, text="This action will clear all hostel data:",bg="#80deea").grid(row=0,column=0,sticky='w')
            Button(lf4,text="Clear All Hostel Data",font="comicsansms 12 bold",command=delete_database).grid(row=0,column=1)
            lf4.columnconfigure((0,1),weight=1)
            lf4.rowconfigure(0,weight=1)
            
            self.f2.columnconfigure((0,1),weight=1)
            self.f2.rowconfigure(tuple(range(3)),weight=1)
        def dashboard():
            ch=(("Students","Rooms","Courses","Payment Due",'Pending Regs'),("#00bfef","#00a558","#ff9c0a",'#c2185b','#009688'),("#009ddb","#00834f","#e38c09",'#9c1f4e','#00796b'))
            self.clearm()
            self.stringstatus="Showing Number Of Records"
            self.instance_status()
            self.heading.config(text="DASHBOARD")
            t=self.server.sqlallreccount()
            can = Canvas(self.f2,bg='#80deea', bd=0, highlightthickness=0)
            can.grid(row=0, column=0, sticky="nsew")
            s = Scrollbar(self.f2, orient="vertical", command=can.yview)
            s.grid(row=0, column=1, sticky="ns")
            can.config(yscrollcommand=s.set)
            card_frame = Frame(can,bg='#80deea')
            card_id=can.create_window((0, 0), window=card_frame, anchor="nw")
            for i in range(5):
                Label(card_frame,text=ch[0][i],fg='white',font="comicsansms 20 bold",bg=ch[1][i],anchor="s").grid(padx=10,pady=(10,0),row=1,columnspan=2,column=2*i+1,sticky="ews")
                Label(card_frame,image=self.logo_hms[i+1],bg=ch[1][i]).grid(padx=(10, 0),row=2,column=2*i+1,sticky="news")
                Label(card_frame,text=str(t[i]),fg='white',font="comicsansms 40 bold",bg=ch[1][i]).grid(padx=(0, 10),row=2,column=2*i+2,sticky="news")
                Button(card_frame,text="More Info",fg="white",bg=ch[2][i],font="comicsansms 8 bold",anchor='e',relief=GROOVE,command=lambda isam=i:buttoncheck2(2 if isam==4 else isam+2,isam==4)).grid(padx=10,columnspan=2,row=3,column=2*i+1,sticky="new")
            self.f2.columnconfigure(0, weight=1)
            self.f2.rowconfigure(0, weight=1)
            resize_ui(can.winfo_width(),can,card_id)
            can.bind("<Configure>",lambda e,c=can,i=card_id: resize_ui(e.width,c,i))
        def admindetails(show2):
            def show():
                entries[2].config(show='*'if sp.get()==0 else '')
            def setpassnew():
                if entries[2]["state"]=="disabled":
                    entries[2].config(state="normal")
                    entries[2].delete(0, 'end')
                    b1.config(text="Save Password")
                elif entries[2].get()=='':
                    self.update_status('Please Fill Out Password Entry')
                elif self.name_check1(entries[2].get().lower().strip()):
                    self.update_status("Please Enter Valid Characters Only 0-9,a-z,A-Z,$,_")
                else:
                    entries[2].config(state="disabled")
                    self.server.sqladminpass(self.currentuser[0],entries[2].get())
                    self.update_status('New Password Successfully Updated')
                    b1.config(text="Update New Password")
            sp=IntVar()
            self.clearm()
            self.stringstatus="Displaying Admin Details"
            self.instance_status()
            self.heading.config(text="ADMIN PROFILE")
            entries=[]
            col=["Username","Role","Password"]
            for i in range(len(col)):
                Label(self.f2,text=col[i]+':',font="comicsansms 12 bold",bg='#80deea').grid(row=i,column=0,sticky='w',padx=6)
                e=Entry(self.f2,disabledforeground="black",show='*' if i==2 else '')
                e.grid(row=i,column=1,sticky='ew',padx=8)
                e.insert(0,self.currentuser[i])
                e.config(state="disabled")
                entries.append(e)
            per=Listbox(self.f2, disabledforeground="black")
            per.grid(row=0,column=2,pady=4,padx=4,rowspan=2,sticky='news')
            if self.currentuser[3] is None:
                per.insert(END,'No Permission')
            else:
                for i in self.currentuser[3]:
                    per.insert(END,self.permission[i])
            per.config(state="disabled")
            p=Frame(self.f2,bg='#80deea')
            p.grid(row=2,column=2)
            b1=Button(p,text="Update New Password",font="comicsansms 12 bold",command=setpassnew)
            b1.grid(row=0,column=0,pady=4,padx=4)
            Checkbutton(p,text="Show Password",variable=sp,command=show,bg='#80deea',activebackground='#80deea').grid(row=1,column=0)
            self.f2.rowconfigure((0,1,2),weight=1)
            self.f2.columnconfigure(1,weight=1)
            self.f2.columnconfigure((0,2),weight=0)
            
        self.clearwid()
        u=("Dashboard","Profile","Students","Rooms","Courses","Payments","DB Operations","Log Out")
        for i in range(7+(self.currentuser[1]=='lead administrator')):
            b=Button(self.menu,font='comicsansms 12 bold',text=u[i+(i==6 and self.currentuser[1]!='lead administrator')],bg='#00acc1',fg='white', disabledforeground="white",activeforeground='white',activebackground='#80deea', relief=FLAT,width=16,command=lambda isam=i+(i==6 and self.currentuser[1]!='lead administrator'):buttoncheck2(isam))
            b.place(x=0,y=76+38*i)
            self.buttons.append(b)
        self.buttons[0].config(state="disabled",bg="#80deea")
        dashboard()
    def logout(self):
        self.update_status(self.server.sqlconclose())
        self.login_page()
if __name__=='__main__':
    root=Tk()
    maingui(root)
    root.mainloop()
