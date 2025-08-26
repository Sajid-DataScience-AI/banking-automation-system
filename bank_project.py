from tkinter import Tk,Label,Frame,Entry,Button,messagebox
from tkinter.ttk import Combobox
from captcha_test import generate_captcha
import time,random
from PIL import Image,ImageTk
from table_creation import generate
from email_test import send_openacn_ack,send_otp,send_otp_4_pass
import sqlite3
import re


generate()

def show_dt():
    dt=time.strftime("%A %d-%b-%Y %r")
    dt_lbl.configure(text=dt)
    dt_lbl.after(1000,show_dt) #ms (1 sec)

list_imgs=["images/logo1.jpg","images/logo_3.jpg","images/logo_4.jpg","images/logo.jpg"]
def image_animation():
    index=random.randint(0,3)
    img=Image.open(list_imgs[index]).resize((250,115))
    imgtk=ImageTk.PhotoImage(img,master=root)
    logo_lbl=Label(root,image=imgtk)
    logo_lbl.place(relx=0,rely=0)
    logo_lbl.image=imgtk
    logo_lbl.after(1000,image_animation)



root=Tk()
root.state("zoomed")
root.configure(bg="pink")

title=Label(root,text="Banking Automation",fg="blue",bg="pink",font=("Aerial",50,"bold","underline"))
title.pack()

dt_lbl=Label(root,font=("Arial",15,),bg="pink")
dt_lbl.pack(pady=3)
show_dt()

img=Image.open("images/logo.jpg").resize((250,115))
imgtk=ImageTk.PhotoImage(img,master=root)


image_animation()

footer_lbl=Label(root,font=("Arial",20),fg="blue",bg="pink",text="Developed By\n Sajid @ 6009588699")
footer_lbl.pack(side="bottom")
def main_screen():
    def refresh_captcha():
        new_captcha=generate_captcha()
        captcha_value_lbl.configure(text=new_captcha)

    frm=Frame(root,highlightbackground="brown",highlightthickness=2)
    frm.configure(bg="powder blue")
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.76) 

    code_captcha=generate_captcha()

    def forgot():
        frm.destroy()
        fp_screen()   

    def login():
            utype=acntype_cb.get()
            uacn=acnno_e.get()
            upass=pass_e.get()

            if utype=="Admin":
                 if uacn=='0' and upass=='admin':
                    ucaptcha=captcha_e.get()
                    if code_captcha.replace(' ','')==ucaptcha:
                         frm.destroy()
                         admin_screen()
                    else:
                         messagebox.showerror("Login","Invalid captcha")     
                      
                 
                    
                 else:
                      messagebox.showerror("Login","You are not Admin")
                           
            else:
                 ucaptcha=captcha_e.get()
                 if code_captcha.replace(' ','')==ucaptcha:  
                      conobj=sqlite3.connect(database='bank.sqlite')
                      curobj=conobj.cursor()
                      query='select * from accounts where acn_acno=? and acn_pass=?'
                      curobj.execute(query,(uacn,upass)) 
                      row=curobj.fetchone()
                      if row==None:
                           messagebox.showerror("login","invalid ACN/PASS")
                      
                      else:
                            frm.destroy()
                            user_screen(row[0],row[1])
                 else:
                      messagebox.showerror("Login","invalid captcha")       
                          
                          

    acntype_lbl=Label(frm,text="ACN Type",font=("Arial",20,"bold"),bg="powder blue")
    acntype_lbl.place(relx=.3,rely=.1)

    acntype_cb=Combobox(frm,values=["User","Admin"],font=("Arial",20,"bold"))
    acntype_cb.current(0)
    acntype_cb.place(relx=.45,rely=.1)

    acnno_lbl=Label(frm,text="🔑ACN",font=("Arial",20,"bold"),bg="powder blue")
    acnno_lbl.place(relx=.3,rely=.2)

    acnno_e=Entry(frm,font=("Arial",20,"bold"),bd=5)
    acnno_e.place(relx=.45,rely=.2)
    acnno_e.focus()

    pass_lbl=Label(frm,text="🔒Pass",font=("Arial",20,"bold"),bg="powder blue")
    pass_lbl.place(relx=.3,rely=.3)

    pass_e=Entry(frm,font=("Arial",20,"bold"),bd=5,show="*")
    pass_e.place(relx=.45,rely=.3)

    captcha_lbl=Label(frm,text="🔄Captcha",font=("Arial",20,"bold"),bg="powder blue")
    captcha_lbl.place(relx=.3,rely=.4)

    captcha_value_lbl=Label(frm,text=code_captcha,fg="green",font=("Arial",20,"bold"))
    captcha_value_lbl.place(relx=.45,rely=.4)

    refresh_btn=Button(frm,text="refresh 🔄",command=refresh_captcha)
    refresh_btn.place(relx=.6,rely=.4)

    captcha_e=Entry(frm,font=("Arial",20,"bold"),bd=5)
    captcha_e.place(relx=.44,rely=.5)

    submit_btn=Button(frm,text="👤Login",command=login,width=17,bg="pink",bd=5,font=("Arial",20,"bold"))
    submit_btn.place(relx=.45,rely=.6)

    fp_btn=Button(frm,text="Forgot pass",command=forgot,width=17,bg="pink",bd=5,font=("Arial",20,"bold"))
    fp_btn.place(relx=.45,rely=.72)

    

def fp_screen():
    frm=Frame(root,highlightbackground="brown",highlightthickness=2)
    frm.configure(bg="green")
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.76)

    def back():
        frm.destroy()
        main_screen()

    def fp_pass():
         uemail=email_e.get()  
         uacn=acnno_e.get()

         conobj=sqlite3.connect(database='bank.sqlite')
         curobj=conobj.cursor()
         query='select * from accounts where acn_acno=?'
         curobj.execute(query,(uacn,))
         torow=curobj.fetchone()
         if torow==None:
              messagebox.showerror("Forgot Password"," ACN does not exist") 
         else:
              if uemail==torow[3]:
                   otp=random.randint(1000,9999)
                   send_otp_4_pass(uemail,otp)
                   messagebox.showinfo("Forgot Password","Otp send to registered email,kindly verify")

                   def verify_otp():
                        uotp=int(otp_e.get())
                        if otp==uotp:
                                   conobj=sqlite3.connect(database='bank.sqlite')
                                   curobj=conobj.cursor()
                                   query1='select acn_pass from accounts where acn_acno=?'
                                   curobj.execute(query1,(uacn,))
                                  
                                   messagebox.showinfo("Forgot Password",f"Your Password is {curobj.fetchone()[0]}")
                                   conobj.close()
                                   frm.destroy()
                                   main_screen()
                        else:
                             messagebox.showerror("Forgot Password","Invalid otp!")
                   otp_e=Entry(frm,font=("Arial",18,"bold"),bd=5)
                   otp_e.place(relx=.4,rely=.6)
                   otp_e.focus()

                        
                   verify_btn=Button(frm,text="verify",command=verify_otp,bg="pink",bd=3,font=("Arial",15,"bold"))
                   verify_btn.place(relx=.7,rely=.6)
                   
                                   
                              
                          
              else:
                   messagebox.showerror("Forgot Password","email is not match")
                    
    back_btn=Button(frm,text="⬅️Back",command=back,bg="pink",bd=5,font=("Arial",20,"bold"))
    back_btn.place(relx=0,rely=.0)

    acnno_lbl=Label(frm,text="🔑ACN",font=("Arial",20,"bold"),bg="powder blue")
    acnno_lbl.place(relx=.3,rely=.2)

    acnno_e=Entry(frm,font=("Arial",20,"bold"),bd=5)
    acnno_e.place(relx=.45,rely=.2)
    acnno_e.focus()

    email_lbl=Label(frm,text="📩Email",font=("Arial",20,"bold"),bg="powder blue")
    email_lbl.place(relx=.3,rely=.3)

    email_e=Entry(frm,font=("Arial",20,"bold"),bd=5)
    email_e.place(relx=.45,rely=.3)

    sub_btn=Button(frm,text="Submit",command=fp_pass,bg="pink",bd=5,font=("Arial",20,"bold"))
    sub_btn.place(relx=.5,rely=.4)

def admin_screen():
     frm=Frame(root,highlightbackground="brown",highlightthickness=2)
     frm.configure(bg="#fff8e7")
     frm.place(relx=0,rely=.15,relwidth=1,relheight=.76)

     def logout():
         frm.destroy()
         main_screen()

     logout_btn=Button(frm,text="🔓Logout",command=logout,bg="pink",bd=5,font=("Arial",20,"bold"))
     logout_btn.place(relx=.88,rely=.0)

     def open():
          ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
          ifrm.configure(bg="#f5f5f5")
          ifrm.place(relx=.2,rely=.2,relwidth=.68,relheight=.69)

          t_lbl=Label(ifrm,text="This open account screen",font=("Arial",20,"bold"),bg="white",fg="purple")
          t_lbl.pack()

          def openac():
               uname=name_e.get()
               uemail=email_e.get()
               umob=mob_e.get()
               uadhar=adhar_e.get()
               uadr=adr_e.get()
               udob=dob_e.get()
               upass=generate_captcha()
               upass=upass.replace(' ','')
               ubal=0
               uopendate=time.strftime("%A %d-%b-%Y")

               # empty validation
               if len(uname)==0 or len(uemail)==0 or len(umob)==0 or len(uadhar)==0 or len(uadr)==0 or len(udob)==0:
                    messagebox.showerror("Open Account","Empty fields are not allowed")
                    return
               # email validation
               match=re.fullmatch(r"[a-zA-Z0-9_.%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+",uemail)
               if match==None:
                    messagebox.showerror("Open Account","Kindly check email!")
                    return
               # mobile validation
               match=re.fullmatch("[6-9][0-9]{9}",umob)
               if match==None:
                    messagebox.showerror("Open Account","Kindly check Your Mobile!")
                    return
               # adhar validation
               match=re.fullmatch("[0-9]{12}",uadhar)
               if match==None:
                    messagebox.showerror("Open Account","Kindly check your adhar")
                    return
                    
               conobj=sqlite3.connect(database="bank.sqlite")
               curobj=conobj.cursor()
               query='insert into accounts values(null,?,?,?,?,?,?,?,?,?)'
               curobj.execute(query,(uname,upass,uemail,umob,uadhar,uadr,udob,ubal,uopendate))
               conobj.commit()
               conobj.close()

               conobj=sqlite3.connect(database="bank.sqlite")
               curobj=conobj.cursor()
               curobj.execute("select max(acn_acno) from accounts")
               uacn=curobj.fetchone()[0]
               conobj.close()

               send_openacn_ack(uemail,uname,uacn,upass)
               messagebox.showinfo("Account","Account Opened and details sent to email")
               frm.destroy()
               admin_screen()

          name_lbl=Label(frm,text="Name",font=("Arial",20,"bold"),bg="white")
          name_lbl.place(relx=.23,rely=.4)

          name_e=Entry(frm,font=("Arial",18,"bold"),bd=5)
          name_e.place(relx=.3,rely=.4)
          name_e.focus()

          email_lbl=Label(frm,text="Email",font=("Arial",20,"bold"),bg="white")
          email_lbl.place(relx=.23,rely=.5)

          email_e=Entry(frm,font=("Arial",18,"bold"),bd=5)
          email_e.place(relx=.3,rely=.5)

          mob_lbl=Label(frm,text="Phone",font=("Arial",20,"bold"),bg="white")
          mob_lbl.place(relx=.23,rely=.6)

          mob_e=Entry(frm,font=("Arial",18,"bold"),bd=5)
          mob_e.place(relx=.3,rely=.6)

          adhar_lbl=Label(frm,text="Adhar",font=("Arial",20,"bold"),bg="white")
          adhar_lbl.place(relx=.52,rely=.4)

          adhar_e=Entry(frm,font=("Arial",20,"bold"),bd=5)
          adhar_e.place(relx=.63,rely=.4)

          adr_lbl=Label(frm,text="Address",font=("Arial",20,"bold"),bg="white")
          adr_lbl.place(relx=.52,rely=.5)

          adr_e=Entry(frm,font=("Arial",20,"bold"),bd=5)
          adr_e.place(relx=.63,rely=.5)

          dob_lbl=Label(frm,text="DOB",font=("Arial",20,"bold"),bg="white")
          dob_lbl.place(relx=.52,rely=.6)

          dob_e=Entry(frm,font=("Arial",20,"bold"),bd=5)
          dob_e.place(relx=.63,rely=.6)

          open_btn=Button(ifrm,text="Open ACN",command=openac,fg="green",bd=5,font=("Arial",20,"bold"))
          open_btn.place(relx=.7,rely=.8)


     def close():
          ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
          ifrm.configure(bg="white")
          ifrm.place(relx=.2,rely=.2,relwidth=.68,relheight=.69)

          t_lbl=Label(ifrm,text="This close account screen",font=("Arial",20,"bold"),bg="white",fg="purple")
          t_lbl.pack()

          def sent_close_otp():
               uacn=acnno_e.get()
               conobj=sqlite3.connect(database='bank.sqlite')
               curobj=conobj.cursor()
               query='select * from accounts where acn_acno=?'
               curobj.execute(query,(uacn,))
               torow=curobj.fetchone()
               if torow==None:
                    messagebox.showerror("Close Account"," ACN does not exist") 

         
               else:
                     otp=random.randint(1000,9999)
                     send_otp_4_pass(torow[3],otp)
                     messagebox.showinfo("Close Account","Otp send to registered email,kindly verify")

                    
                     def verify_otp():
                        uotp=int(otp_e.get())
                        if otp==uotp:
                                   conobj=sqlite3.connect(database='bank.sqlite')
                                   curobj=conobj.cursor()
                                   query1='delete from accounts where acn_acno=?'
                                   curobj.execute(query1,(uacn,))
                                  
                                   messagebox.showinfo("Close Accounts","Account Closed")
                                   conobj.commit()
                                   conobj.close()
                                   
                                   frm.destroy()
                                   admin_screen()
                        else:
                             messagebox.showerror("Close Account","Invalid otp!")
                     otp_e=Entry(frm,font=("Arial",18,"bold"),bd=5)
                     otp_e.place(relx=.4,rely=.6)
                     otp_e.focus()

                        
                     verify_btn=Button(frm,text="verify",command=verify_otp,bg="pink",bd=3,font=("Arial",15,"bold"))
                     verify_btn.place(relx=.7,rely=.6)
                                                      
                                                                                     
          acnno_lbl=Label(frm,text="🔑ACN",font=("Arial",20,"bold"),bg="powder blue")
          acnno_lbl.place(relx=.3,rely=.4)

          acnno_e=Entry(frm,font=("Arial",20,"bold"),bd=5)
          acnno_e.place(relx=.4,rely=.4)
          acnno_e.focus()

          otp_btn=Button(ifrm,text="Send OTP",command=sent_close_otp,bd=5,font=("Arial",20,"bold"))
          otp_btn.place(relx=.6,rely=.5)

     def view():
          ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
          ifrm.configure(bg="#f0f8ff")
          ifrm.place(relx=.2,rely=.2,relwidth=.68,relheight=.69)

          t_lbl=Label(ifrm,text="This View account screen",font=("Arial",20,"bold"),bg="white",fg="purple")
          t_lbl.pack()  
          from tktable import Table

          def view_acns():               
               table_headers=("ACN0.","NAME","Email","MOB","OPEN DATE","BALANCE")
               mytable=Table(ifrm, table_headers,headings_bold=True)
               mytable.place(relx=.1,rely=.1,relwidth=.8,relheight=.7)

               conobj=sqlite3.connect(database='bank.sqlite')
               curobj=conobj.cursor()
               query='select acn_acno,acn_name,acn_email,acn_mob,acn_opendate,acn_bal from accounts'
               curobj.execute(query)
               for tup in curobj.fetchall():
                    mytable.insert_row(tup)
               conobj.close()     

          

          view_btn=Button(ifrm,text="View",command=view_acns,bd=5,font=("Arial",20,"bold"))
          view_btn.place(relx=.75,rely=.82)
  
     


     open_btn=Button(frm,width=10,text="Open ACN",command=open,fg="green",bd=5,font=("Arial",20,"bold"))
     open_btn.place(relx=.001,rely=.1)

     close_btn=Button(frm,width=10,text="Close ACN",command=close,fg="red",bd=5,font=("Arial",20,"bold"))
     close_btn.place(relx=.001,rely=.3)

     view_btn=Button(frm,width=10,text="View ACN",command=view,fg="blue",bd=5,font=("Arial",20,"bold"))
     view_btn.place(relx=.001,rely=.5)

def user_screen(uacn,uname):
     frm=Frame(root,highlightbackground="brown",highlightthickness=2)
     frm.configure(bg="#fff8e7")
     frm.place(relx=0,rely=.15,relwidth=1,relheight=.76)

     conobj=sqlite3.connect(database='bank.sqlite')
     curobj=conobj.cursor()
     query='select * from accounts where acn_acno=?'
     curobj.execute(query,(uacn,))
     row=curobj.fetchone()
     conobj.close()

     

     def logout():
         frm.destroy()
         main_screen() 

     def check():
          ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
          ifrm.configure(bg="#f0f8ff")
          ifrm.place(relx=.2,rely=.2,relwidth=.68,relheight=.69)

          t_lbl=Label(ifrm,text="This is Check Details Screen",font=("Arial",20,"bold"),bg="white",fg="black")
          t_lbl.pack()

          acn_lbl=Label(ifrm,text=f"Account No\t=\t{row[0]}",font=("Arial",20),bg="white",fg="purple")
          acn_lbl.place(relx=.2,rely=.1)

          bal_lbl=Label(ifrm,text=f"Balance\t=\t{row[8]}",font=("Arial",20),bg="white",fg="purple")
          bal_lbl.place(relx=.2,rely=.3)

          open_lbl=Label(ifrm,text=f"Open Date\t=\t{row[9]}",font=("Arial",20),bg="white",fg="purple")
          open_lbl.place(relx=.2,rely=.5)

          dob_lbl=Label(ifrm,text=f"Date of birth\t=\t{row[7]}",font=("Arial",20),bg="white",fg="purple")
          dob_lbl.place(relx=.2,rely=.7)

          adhar_lbl=Label(ifrm,text=f"ADHAR No\t=\t{row[5]}",font=("Arial",20),bg="white",fg="purple")
          adhar_lbl.place(relx=.2,rely=.9)

          

     def update():
          ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
          ifrm.configure(bg="#f0f8ff")
          ifrm.place(relx=.2,rely=.2,relwidth=.68,relheight=.69)

          t_lbl=Label(ifrm,text="This is Update Screen",font=("Arial",20,"bold"),bg="white",fg="purple")
          t_lbl.pack()

          def update_details():
               uname=name_e.get()
               upass=pass_e.get()
               uemail=email_e.get()
               umob=mob_e.get()

               conobj=sqlite3.connect(database='bank.sqlite')
               curobj=conobj.cursor()
               query='update accounts set acn_name=?,acn_pass=?,acn_email=?,acn_mob=? where acn_acno=?'
               curobj.execute(query,(uname,upass,uemail,umob,uacn))
               conobj.commit()
               conobj.close()
               messagebox.showinfo("Update","Details Updated")
               frm.destroy()
               user_screen(uacn,None)
               
               


          name_lbl=Label(frm,text="Name",font=("Arial",20,"bold"),bg="white")
          name_lbl.place(relx=.23,rely=.4)

          name_e=Entry(frm,font=("Arial",18,"bold"),bd=5)
          name_e.place(relx=.3,rely=.4)
          name_e.focus()
          name_e.insert(0,row[1])

          email_lbl=Label(frm,text="Email",font=("Arial",20,"bold"),bg="white")
          email_lbl.place(relx=.23,rely=.6)

          email_e=Entry(frm,font=("Arial",18,"bold"),bd=5)
          email_e.place(relx=.3,rely=.6)
          email_e.insert(0,row[3])

          mob_lbl=Label(frm,text="Phone",font=("Arial",20,"bold"),bg="white")
          mob_lbl.place(relx=.52,rely=.4)

          mob_e=Entry(frm,font=("Arial",20,"bold"),bd=5)
          mob_e.place(relx=.63,rely=.4)
          mob_e.insert(0,row[4])

          pass_lbl=Label(frm,text="Pass",font=("Arial",20,"bold"),bg="white")
          pass_lbl.place(relx=.52,rely=.6)

          pass_e=Entry(frm,font=("Arial",20,"bold"),bd=5)
          pass_e.place(relx=.63,rely=.6)
          pass_e.insert(0,row[2])

          update_btn=Button(ifrm,text="Update",command=update_details,bg="pink",bd=5,font=("Arial",20,"bold"))
          update_btn.place(relx=.7,rely=.75)

     def deposit():
          ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
          ifrm.configure(bg="#f0f8ff")
          ifrm.place(relx=.2,rely=.2,relwidth=.68,relheight=.69)

          t_lbl=Label(ifrm,text="This is Deposit Screen",font=("Arial",20,"bold"),bg="white",fg="purple")
          t_lbl.pack() 

          def deposit_amt():
               uamt=float(amt_e.get())
               conobj=sqlite3.connect(database='bank.sqlite')
               curobj=conobj.cursor()
               query='update accounts set acn_bal=acn_bal+? where acn_acno=?'
               curobj.execute(query,(uamt,uacn))
               conobj.commit()
               conobj.close()
               messagebox.showinfo("Deposit",f"{uamt} Amount Deposited")
               frm.destroy()
               user_screen(uacn,None)

          amt_lbl=Label(ifrm,text="Amount",font=("Arial",20,"bold"),bg="white")
          amt_lbl.place(relx=.3,rely=.4)

          amt_e=Entry(ifrm,font=("Arial",18,"bold"),bd=5)
          amt_e.place(relx=.5,rely=.4)
          amt_e.focus()

          deposit_btn=Button(ifrm,text="Deposit",command=deposit_amt,bg="pink",bd=5,font=("Arial",20,"bold"))
          deposit_btn.place(relx=.6,rely=.65)

     def withdraw():
          ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
          ifrm.configure(bg="#f0f8ff")
          ifrm.place(relx=.2,rely=.2,relwidth=.68,relheight=.69)

          t_lbl=Label(ifrm,text="This is Withdraw Screen",font=("Arial",20,"bold"),bg="white",fg="purple")
          t_lbl.pack() 

          def withdraw_amt():
               uamt=float(amt_e.get())
               if row[8]>=uamt:
                    conobj=sqlite3.connect(database='bank.sqlite')
                    curobj=conobj.cursor()
                    query='update accounts set acn_bal=acn_bal-? where acn_acno=?'
                    curobj.execute(query,(uamt,uacn))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Withdraw",f"{uamt} Amount Withdrawn")
                    frm.destroy()
                    user_screen(uacn,None)
               else:
                    messagebox.showerror("Withdaw","Insufficent Balance")     
               

          amt_lbl=Label(ifrm,text="Amount",font=("Arial",20,"bold"),bg="white")
          amt_lbl.place(relx=.3,rely=.4)

          amt_e=Entry(ifrm,font=("Arial",18,"bold"),bd=5)
          amt_e.place(relx=.5,rely=.4)
          amt_e.focus()

          withdraw_btn=Button(ifrm,text="Withdraw",command=withdraw_amt,bg="pink",bd=5,font=("Arial",20,"bold"))
          withdraw_btn.place(relx=.6,rely=.65)


     def transfer():
          ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
          ifrm.configure(bg="#f0f8ff")
          ifrm.place(relx=.2,rely=.2,relwidth=.68,relheight=.69)

          t_lbl=Label(ifrm,text="This is Transfer Screen",font=("Arial",20,"bold"),bg="white",fg="purple")
          t_lbl.pack() 

          def transfer_amt():
               toacn=to_e.get()
               uamt=float(amt_e.get())

               conobj=sqlite3.connect(database='bank.sqlite')
               curobj=conobj.cursor()
               query='select * from accounts where acn_acno=?'
               curobj.execute(query,(toacn,))
               torow=curobj.fetchone()
               if torow==None:
                    messagebox.showerror("Transfer","To ACN does not exist")
               else:
                    if row[8]>=uamt:
                         otp=random.randint(1000,9999)
                         send_otp(row[3],otp,uamt)
                         messagebox.showinfo("Transfer","Otp sen to registered email,kindly verify")

                         def verify_otp():
                              uotp=int(otp_e.get())
                              if otp==uotp:
                                   conobj=sqlite3.connect(database='bank.sqlite')
                                   curobj=conobj.cursor()
                                   query1='update accounts set acn_bal=acn_bal-? where acn_acno=?'
                                   query2='update accounts set acn_bal=acn_bal+? where acn_acno=?'
                                   curobj.execute(query1,(uamt,uacn))
                                   curobj.execute(query2,(uamt,toacn))
                                   conobj.commit()
                                   conobj.close()
                                   messagebox.showinfo("Transfer",f"{uamt} Amount Transfered")
                                   frm.destroy()
                                   user_screen(uacn,None)
                              else:
                                   messagebox.showerror("Transfer","Invalid otp!")
                         otp_e=Entry(ifrm,font=("Arial",18,"bold"),bd=5)
                         otp_e.place(relx=.4,rely=.6)
                         to_e.focus()

                        
                         verify_btn=Button(ifrm,text="verify",command=verify_otp,bg="pink",bd=3,font=("Arial",15,"bold"))
                         verify_btn.place(relx=.7,rely=.6)

                    else:
                         messagebox.showerror("Transfer","Insufficient Balance")     

          to_lbl=Label(ifrm,text="To ACN",font=("Arial",20,"bold"),bg="white")
          to_lbl.place(relx=.3,rely=.3)

          to_e=Entry(ifrm,font=("Arial",18,"bold"),bd=5)
          to_e.place(relx=.5,rely=.3)
          to_e.focus()

          amt_lbl=Label(ifrm,text="Amount",font=("Arial",20,"bold"),bg="white")
          amt_lbl.place(relx=.3,rely=.4)

          amt_e=Entry(ifrm,font=("Arial",18,"bold"),bd=5)
          amt_e.place(relx=.5,rely=.4)
          
          transfer_btn=Button(ifrm,text="Transfer",command=transfer_amt,bg="pink",bd=5,font=("Arial",20,"bold"))
          transfer_btn.place(relx=.6,rely=.65)      


     logout_btn=Button(frm,text="🔓Logout",command=logout,bg="pink",bd=5,font=("Arial",20,"bold"))
     logout_btn.place(relx=.88,rely=.0) 

     wel_lbl=Label(frm,text=f"Welcome,{row[1]}",font=("Arial",20,"bold"),bg="white",fg="purple")
     wel_lbl.place(relx=0,rely=0)

     check_btn=Button(frm,width=15,text="Check Details",command=check,fg="brown",bd=5,font=("Arial",20,"bold"))
     check_btn.place(relx=.001,rely=.15)

     update_btn=Button(frm,width=15,text="Update Details",command=update,fg="blue",bd=5,font=("Arial",20,"bold"))
     update_btn.place(relx=.001,rely=.3)

     deposit_btn=Button(frm,width=15,text="Deposit",command=deposit,fg="green",bd=5,font=("Arial",20,"bold"))
     deposit_btn.place(relx=.001,rely=.45)

     withdraw_btn=Button(frm,width=15,text="Withdraw",command=withdraw,fg="red",bd=5,font=("Arial",20,"bold"))
     withdraw_btn.place(relx=.001,rely=.6)

     transfer_btn=Button(frm,width=15,text="Transfer",command=transfer,fg="black",bd=5,font=("Arial",20,"bold"))
     transfer_btn.place(relx=.001,rely=.75)       


main_screen()



root.mainloop()
