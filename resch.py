import mysql.connector as sql
from datetime import datetime
class sqlcom:
    def sqlcheck(self,d):
        try:
            self.con=sql.connect(host='localhost',user='root',password='1234')
            self.mc = self.con.cursor()
            self.mc.execute("use hostel")
            self.mc.execute(f"select u.name,r.role_name,u.pass,r.permissions from user u,role r where u.role_id=r.role_id and u.name='{d[0]}' and u.pass='{d[1]}'")
            t=self.mc.fetchall()
            if len(t)==1:
                return "You Logged In !!!",True,list(t[0])
            else:
                return "Invalid Username Or Password",False,[]
        except Exception as e:
            return "My SQL Error : "+str(e),False
    def sqlstuconnect(self):
        try:
            self.con=sql.connect(host='localhost',user='root',password='1234')
            self.mc = self.con.cursor()
            self.mc.execute("use hostel")
            return (True,)
        except:
            return False,'Unable To Connect The Server. Please Try Again Later'
    def sqlstucheck(self,d):
        #try:
        self.con=sql.connect(host='localhost',user='root',password='1234')
        self.mc = self.con.cursor()
        self.mc.execute("use hostel")
        self.mc.execute(f"select student_id,room_id,course_id,password,verify from student where registration_no='{d[0]}' and name='{d[1]}' and password='{d[2]}'")
        t=self.mc.fetchall()
        if len(t)!=1:
            return "Invalid Student Details Or Password",False,[]
        elif t[0][4]==0:
            return "Your Registration Has Not Verified Yet By Admin. Please Try Again Later",False,[]
        else:
            return "You Logged In !!!",True,list(t[0])              
        #except:
            #return 'Unable To Connect The Server. Please Try Again Later',False,[]
    def sqlreccount(self,name):
        self.mc.execute(f"SELECT COUNT(*) FROM {name}")
        return self.mc.fetchone()
    def sqlallreccount(self):
        t=[]
        t.append(self.sqlreccount('student')[0])
        t.append(self.sqlreccount('room')[0])
        t.append(self.sqlreccount('course')[0])
        t.append(self.sqlreccount('payment where payment_date is null')[0])
        t.append(self.sqlreccount('student where verify=0')[0])
        return tuple(t)
    def sqlcheckcount(self,t,i):
        if t in ('course','room'):
            self.mc.execute(f"select count(*) from student where {t}_id='{i}'")
            return self.mc.fetchone()[0]==0
        else:
            return False
    def sqlgetcol(self,p):
        self.mc.execute(f"desc {p}")
        o=[i[0] for i in self.mc.fetchall()]
        if p=='student':
            o[-1]='Course_name'
        return o
    def sqlsearchrec(self,t,sc,v,c='*'):
        self.mc.execute(f"select {c} from {t} where {sc} like'%{v}%'")
        return self.mc.fetchall()
    def sqlgetallrec(self,t,c='*'):
        self.mc.execute(f"select {c} from {t}")
        return self.mc.fetchall()
    
    def sqlsearch_student_rec(self,t,u):
        if t=='Gender':
            if u.strip().lower() in 'male':
                u='M'
            elif u.strip().lower() in 'female':
                u='F'
        if t=='Verify':
            if u.strip().lower() in 'verified':
                u=1
            elif u.strip().lower() in 'pending':
                u=0
        u=" is NULL" if t in('Course_Name','Room_id') and u.strip().lower() in 'na' else f" like '%{u}%'"
        t=('c.' if t=='Course_Name' else 's.')+t
        self.mc.execute(f"select s.Student_id,s.Registration_No,s.Name,s.Gender,s.Father_Name,s.Mother_Name,s.DOB,s.Address,s.Phone_no,s.Room_id,c.Course_name,s.Verify from student s LEFT JOIN course c on s.course_id=c.course_id where {t}{u}")
        return self.mc.fetchall()
    def sqlgetall_student_rec(self):
        self.mc.execute("select s.Student_id,s.Registration_No,s.Name,s.Gender,s.Father_Name,s.Mother_Name,s.DOB,s.Address,s.Phone_no,s.Room_id,c.Course_name,s.Verify from student s LEFT JOIN course c on s.course_id=c.course_id")
        return self.mc.fetchall()
    def sql_student_verify(self,sid):
        self.mc.execute(f"update student set Verify =1 where Student_id={sid}")
        self.con.commit()
    def sqlsearchpaymentrec(self,t,u):
        u=" is NULL" if t in('Course_Name','Room_id') and u.strip().lower() in 'na' else f" like '%{u}%'"
        t=('c.'if t=='Course_Name' else 's.') +t
        self.mc.execute(f"select s.student_id,s.name,s.room_id,c.course_name from student s LEFT JOIN course c on s.course_id=c.course_id where s.Verify=1 and {t}{u}")
        return self.mc.fetchall()
    def sqlgetallpaymentrec(self):
        self.mc.execute(f"select s.student_id,s.name,s.room_id,c.course_name from student s LEFT JOIN course c on s.course_id=c.course_id where s.Verify=1")
        return self.mc.fetchall()
    def sqladmingetallrec(self):
        self.mc.execute(f"select u.name,r.role_name from user u,role r where u.role_id=r.role_id")
        return self.mc.fetchall()
    def sqlchecksameroomclone(self,i,b):
        self.mc.execute(f"select count(*) from room where room_no='{i}'and block='{b}'")
        return self.mc.fetchone()[0]==0
    def sqlsetnew(self,d,t,c):
        s= f"room where {c[0]}='{d[1]}' and {c[1]}='{d[2]}'" if t=='room' else f"{t} where {c}='{d[t!='user']}'"
        if self.sqlreccount(s)[0]==0:
            s=",".join(["%s"] * len(d))
            self.mc.execute(f"insert into {t} values ({s})",d)
            self.con.commit()
            return True,"Added Successfully"
        else:
            return False,t.capitalize()+" Already Exitst !"
    def sqlsetdel(self,p,i):
        if p=='student' or self.sqlcheckcount(p,i):
            if len(self.sqlsearchrec(p,p+'_id',i))!=0:
                self.mc.execute(f"delete from {p} where {p}_id='{i}'")
                self.con.commit()
                return "Delected Sucessfully"
            else:
                return "Record Not Found !"
        elif p=="user":
                self.mc.execute(f"delete from user where name='{i}'")
                self.con.commit()
                return "Delected Sucessfully"
        else:
            return f"Student Have Already Taken {p}"
    def sqlupdaterole(self,n,r):
        self.mc.execute(f"update user set role_id={r} where name='{n}'")
        self.con.commit()
        return "Admin Role Updated"
    def sqlconclose(self):
        self.mc.close()
        self.con.close()
        return "You Logged Out !"
    def sqlexeother(self,q,t,d,c):
        s= f"room where {c[0]}='{d[0]}' and {c[1]}='{d[1]}'" if t=='room' else f"{t} where {c}='{d[0]}'"
        if self.sqlreccount(s)[0]!=0:
            self.mc.execute(q,d)
            self.con.commit()
            return True,"Modified Sucessfully"
        else:
            return False,"Record Not Found !"
    def sqladminpass(self,u,p):
        self.mc.execute(f"update user set pass ='{p}' where name='{u}'")
        self.con.commit()
    def sqlgetstublock(self,t):
        if t=='student':
            rec=[[]]
            self.mc.execute("select  room_id,beds from room where Available='Y'")
            t=self.mc.fetchall()
            for i in t:
                self.mc.execute(f"select  count(*) from student where room_id='{i[0]}'")
                if i[1]>self.mc.fetchone()[0]:
                    rec[0].append(i[0])
            self.mc.execute('select course_id,course_name from course')
            t=self.mc.fetchall()
            rec.append([i[1].title() for i in t])
            rec.append([i[0] for i in t])
            return rec
        elif t=='room':
            self.mc.execute('select block from room group by block')
            return [i[0] for i in self.mc.fetchall()]
    def sqlgetpayments(self,p):
        self.mc.execute(f"select  payment_id,amount,due_date,payment_date from payment where student_id={p}")
        return self.mc.fetchall()
    def sqlnewpayment(self,p):
        self.mc.execute(f"insert into payment (payment_id,student_id,amount,due_date) values {p}")
        self.con.commit()
    def sqldelpayment(self,p):
        self.mc.execute(f"delete from payment where payment_id={p}")
        self.con.commit()
    def sqlupadatepayment(self,p,i):
        self.mc.execute(f"update payment set payment_date='{p}' where payment_id={i}")
        self.con.commit()
    def sqlgetrolename(self,a=''):
        s=[[],[],[]]
        self.mc.execute(f"select role_id,role_name,permissions from role{a} order by role_id")
        for i in self.mc.fetchall():
            s[0].append(i[0])
            s[1].append(i[1])
            s[2].append(i[2])
        return s
    def sqludpatepermission(self,p,r):
        p='NULL' if p is None else "'"+p+"'"
        self.mc.execute(f"update role set permissions={p} where role_id={r}")
        self.con.commit()
    def sqladdnewrole(self,i,n):
        self.mc.execute(f"insert into role value({i},'{n}',NULL)")
        self.con.commit()
    def sqlremoverole(self,i):
        self.mc.execute(f"delete from role where role_id={i}")
        self.con.commit()
    def sqlget_all_id(self,t):
        self.mc.execute(f"select {t}_id from {t} order by {t}_id")    
        return [i[0] for i in self.mc.fetchall()]
    def sql_student_name_roomcourse_id(self,n,b,c):
        i=[]
        if n=='NA' or n=='NA':
            self.mc.execute(f"select room_id from room where room_no={n} and block='{b}'")
            i.append(self.mc.fetchall()[0])
        else:
            i.append(None)
        if c=='NA':
            self.mc.execute(f"select course_id from course where course_name='{c}'")
            i.append(self.mc.fetchall()[0])
        else:
            i.append(None)
        return i
    def sql_import(self,t,v):
        s=",".join(["%s"] * len(v))
        self.mc.execute(f"insert into {t} values ({s})",v)
        self.con.commit()
    def sql_student_registration(self,v):
        if self.server.sqlreccount(f"student where registration_no={v[1]} and name='{v[2]}'")[0]==0:
            s=",".join(["%s"] * len(v))
            self.mc.execute(f"insert into student values ({s})",v)
            self.con.commit()
            return 'Your Registration Successfully Completed'
        else:
            return 'Registration Number Or Name Already Existed'
    def sql_clear(self):
        self.mc.execute(f"delete from user where role_id!=1")
        self.mc.execute(f"delete from role where role_id>1")
        self.mc.execute(f"delete from payment")
        self.mc.execute(f"delete from student")
        self.mc.execute(f"delete from course")
        self.mc.execute(f"delete from room")
        self.con.commit()
    def sql_id_info(self,t,i):
        if t=='student':
            self.mc.execute(f"select Registration_No,Name,Gender,Father_Name,Mother_Name,DOB,Address,Phone_no,Password from student where student_id={i}")
        elif t=='room':
            self.mc.execute(f"select Room_no,Block,Available,Beds,AC,Wifi,TV from room where room_id={i}")
        elif t=='course':
            self.mc.execute(f"select Course_Name,Duration from course where course_id={i}")
        return self.mc.fetchall()[0]
    def sql_stu_pass(self,i,p):
        self.mc.execute(f"update student set password ='{p}' where student_id='{i}'")
        self.con.commit()
    def sql_stu_payment_search(self,p,s):
        self.mc.execute(f"select payment_id,amount,due_date,payment_date from payment where student_id={p}{s}")
        return self.mc.fetchall()
    def sql_stu_payment_make(self,p):
        d=datetime.now().strftime('%Y-%m-%d')
        self.mc.execute("UPDATE payment SET payment_date = %s WHERE payment_id = %s", (d, p))
        self.con.commit()

