#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# sudo apt-get install dbus-x11
import os
import re
import sys ,time
import subprocess
from subprocess import PIPE
import json
import readline
import signal
import threading
import requests 
from Chat_Package.Banner import *
for i in range(readline.get_current_history_length()):
    print (readline.get_history_item(i + 1))
    print(readline.get_line_buffer())
    
if "--color-off" in sys.argv:
    W,R,B,Y ='','','',''   
elif "-C" in sys.argv:
    W,R,B,Y ='','','',''
else:  
    W,R,B,Y = '\033[0m','\033[1;31m','\033[1;34m' ,'\033[1;33m' 

def Check_argv():
    printf="""usage: Chatgpt [ -C ] or [ --color-off ]  [ --terminal ] or [ -T ] [ --webchat ] [ -W ]
                  🚨️  -C  --color-off    ignore the color 
                  🚨️  -T  --terminal     chat in terminal interface
                  🚨️  -W  --webchat      chat in webside interface
                """
    Command_Useful  =["--color-off","--terminal","--webchat",'-W','-T','-C']
    if "python" or "python3" in sys.argv[0]:
        lenAV = sys.argv[1:]
    else:
        lenAV = sys.argv[0:]     
    if len(lenAV) == 0 or  len(lenAV) > 2:       
        print(printf)       
        exit()
    else:  
        for command in lenAV: 
            if command not in Command_Useful:
                print(printf)
                exit()                                                                        
Check_argv()  
def Test_API():
    try:
        with open('./Chat_Package/.KEY_AI.json','r') as APIKEY:
            APIKEY = APIKEY.read().split(':')[1][2:-3]
            Back_end_api= "https://api.openai.com/v1/completions"
            response = requests.post(
            Back_end_api,
            headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer "+f"{APIKEY}",
                    },
            json={
                    "prompt": 'Great Welcome',
                    "model": "gpt-3.5-turbo",
                    "max_tokens": 500,
                    "temperature": 0.5
                    },
            ) 
        if response.status_code == 200:
            time.sleep(2)
            os.system('cls||clear')
            time.sleep(3)
        else:
            run = Banner_Logo()
            print(R+'⛔ Error API         : '+APIKEY )
            print("⛔ API repones code  : 429-Too Many Requests")
            print(R+'🌐️ Visit Link        : '+Y+'https://platform.openai.com/docs/guides/rate-limits?context=tier-free')
            exit()  
    except FileNotFoundError:
          pass         
Test_API()              
class Chat_GPT:
    def __init__(self):    
        self.__Connect_Openai()
    def _Conections(self): 
        Check_Internet ='ping  -w1 www.google.com  >/dev/null 2>&1 '   
        communicate = os.system(Check_Internet)
        if communicate  == 0 :
            pass
        else:
            if communicate == 512:
                print("[+] No Internet Connection")
                exit()  
        
    def _Check_Import (self):  
        Check_Import ="pip show requests"
        Check_Import = subprocess.call(Check_Import,shell=True,stderr=subprocess.PIPE,stdout=PIPE) 
        if Check_Import == 0:
            pass
        else:
            os.system("pip3 install --upgrade requests >/dev/null 2>&1")
            Process = "pip install  requests"  
            subprocess.call(Process,shell=True,stderr=subprocess.PIPE,stdout=PIPE)     
        list_Pakages = [
                        "which aspell            > /dev/unll 2>&1 ",
                        "which gnome-terminal    > /dev/unll 2>&1 ",
                        ]       
        for package in list_Pakages :
            test_packages = subprocess.call(  package ,shell=True,stderr=subprocess.PIPE,stdout=PIPE)  
            if test_packages == 0  :                     
                 continue
            else:  
                  subprocess.call(package,shell=True,stderr=subprocess.PIPE,stdout=PIPE) 
    def __Connect_Openai(self): 
        try:

            import json
            with open("Chat_Package/.KEY_AI.json") as json_File:
                json_File = json.load(json_File)
                json_File = json_File["OPENAI_API_KEY"]
                openai_api_key = json_File    
                Bearer = "Bearer "+f"{openai_api_key}"  
                Back_end_api= "https://api.openai.com/v1/completions"
                Connect_Session = requests.Session() 
            def requests_Qury():
                prompt = input(R+"👨 USER     ---|  "+W).strip()
                with open("Chat_Package/.Check_SPelling.txt" ,'w')as Checker   :
                    Checker.write(prompt) 
                SystemCall = subprocess.getstatusoutput('cat  Chat_Package/.Check_SPelling.txt | aspell --list')[1]
                if len(SystemCall) == 0 :
                   pass
                else:  
                    order2 = "aspell -c Chat_Package/.Check_SPelling.txt"
                    command_proc3 = ' gnome-terminal --geometry 60x15+1000+60  -e ' +'"' + order2 +'"'  
                    call_termminal = subprocess.call(command_proc3,shell=True,stderr=subprocess.PIPE) 
                    while True:
                        Process = subprocess.getstatusoutput("ps ax | grep aspell | grep -v grep")[1]
                        if len(Process) != 0: 
                            sys.stdout.write('\x1b[1A')  
                            sys.stdout.write('\x1b[2K')
                            print(R+"👨 USER     ---|  "+W+str(prompt))
                        else:                
                            break   
                    with open("Chat_Package/.Check_SPelling.txt" ,'r') as Checker :
                        prompt = Checker.read().strip()  
                        sys.stdout.write('\x1b[1A')  
                        sys.stdout.write('\x1b[2K')
                        print(R+"👨 USER     ---|  "+W+str(prompt))                                  
                if prompt == "EXIT".lower() or prompt=="exit".upper():
                    print(R+'\n🚧️ Session is Closed : Exit Terminal'+W)
                    Connect_Session.close()
                    exit()
                else:
                    pass      
                if "code" in prompt:  
                    from Chat_Package.Code_Writer import Writer  
                    prompt_tittel =f'{prompt}'+" . Provide only code, no text",  
                else:
                    prompt_tittel = prompt            
                response = Connect_Session.post(
                            Back_end_api,
                    headers={
                        "Content-Type": "application/json",
                         "Authorization": f"{Bearer}",
                    },
                    json={
                        "prompt": prompt_tittel,
                        "model": "gpt-3.5-turbo",
                        "max_tokens": 500,
                        "temperature": 0.5
                    },
                ) 
                response_text = json.loads(response.text)
                if "code" in prompt : 
                    search = str(response_text["choices"][0]["text"])                     
                    codeback = "\n".join(re.split("\\n\\n" ,search[2:]))                
                    with open('Chat_Package/.Code_re.txt','w') as code_write:
                        coderwite =  code_write.write(codeback) 
                    thread = threading.Thread(target=Writer)  
                    thread.start()
                    return  re.split("\\n\\n" ,search[2:]) 

                else:   
                    search = str(response_text["choices"][0]["text"])          
                    return  re.split("\\n\\n" ,search[2:])
            while True  :
                reply = requests_Qury()
                with open("Chat_Package/.answer.txt",'w')as answer :
                    for i in reply:
                        try:
                           answer.write(i+'\n')
                        except :
                            pass       
                with open("Chat_Package/.answer.txt",'r') as read_answer:
                    ReadData = read_answer.readlines()
                    print(Y+"🦾 ChatGPT  ---|  "+W+B,end='')  
                    C = 0
                    for i in  ReadData[0]: 
                        if C == 100:
                            print("\n"+"\t\t  "+"-",end='') 
                            C = 0
                        sys.stdout.write(i)
                        sys.stdout.flush()
                        time.sleep(3./90)  
                        C +=1 
                    print("\t\t  ",end='')  
                     
                    ReadData = str("".join(ReadData[1:])) 
                    C = 0
                    for i in ReadData : 
                        if C == 100:
                            print("\n"+"\t\t  "+"-",end='') 
                            C = 0
                        sys.stdout.write(i)
                        sys.stdout.flush()
                        time.sleep(3./90) 
                        if '\n' in i :
                          print("\t\t  ",end='')
                    print("\n",end='') 
        except KeyboardInterrupt :        
            print(R+'\n🚧️ Session is Closed : Exit Terminal'+W)
            Connect_Session.close()
            exit()
            
if __name__=='__main__':
    Chat_GPT()             
