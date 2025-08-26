import gmail
#Put your email and app password
email_id="sajid@gmail.com"
app_pass="yqei zjnk kvbr alqm"
con=gmail.GMail("02kingofwar455@gmail.com","")

def send_openacn_ack(uemail,uname,uacn,upass):
    con=gmail.GMail(email_id,app_pass)
    sub="congrates😊,Account opened successfully"
    upass=upass.replace(' ','')
    utext=f"""hello,{uname}
Welcome to SAJID BANK
Your Acc No is {uacn}
Your Pass is {upass}
Kindly change your password when you login first

Thanks
SAJID Bank
Noida
    """
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)

def  send_otp(uemail,otp,amt): 
    con=gmail.GMail(email_id,app_pass)
    sub="otp for transfer money"
    
    utext=f"""Your otp is {otp} to transfer amount {amt}

     Kindly use this otp to complete transfer
     please don't share to anyone else

    Thanks
    SAJID Bank
     Noida
    """
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg) 

def  send_otp_4_pass(uemail,otp): 
    con=gmail.GMail(email_id,app_pass)
    sub="otp for password recovery "
    
    utext=f"""Your otp is {otp} to to recovery password 

         please don't share to anyone else

    Thanks
    SAJID Bank
     Noida
    """
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)       