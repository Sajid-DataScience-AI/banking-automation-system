import random
def generate_captcha():
    captcha=""
    a=str(random.randint(0,9))
    b=chr(random.randint(97,122))
    c=str(random.randint(0,9))
    d=chr(random.randint(65,80))
    captcha="  "+a+" "+b+" "+c+" "+d+"  "
    return captcha



 
