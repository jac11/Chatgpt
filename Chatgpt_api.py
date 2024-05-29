#!/usr/bin/env  python
import os
import sys
import requests
from Chat_Package.ChatGpt import Chat_GPT,Check_argv
from Chat_Package.Banner import *
import sys

if "--color-off" in sys.argv:
    W,R,B,Y ='','','',''   
elif "-C" in sys.argv:
    W,R,B,Y ='','','',''
else:  
    W,R,B,Y = '\033[0m','\033[1;31m','\033[1;34m' ,'\033[1;33m'   
printf="""usage: Chatgpt [ -C ] or [ --color-off ]  [ --terminal ] or [ -T ] [ --webchat ] [ -W ]
                  🚨️  -C  --color-off    ignore the color 
                  🚨️  -T  --terminal     chat in terminal interface
                  🚨️  -W  --webchat      chat in webside interface
                """         
class Control:
    def __init__(self): 
        Chat_GPT._Conections(self)
        Check_argv.__init__()   
        Chat_GPT._Check_Import(self)
        Check_key = os.listdir("./Chat_Package/")
        if ".KEY_AI.json" in Check_key :
            self.Control_all()
        else:
            if "--color-off" in sys.argv[1] and len(sys.argv)==2:
               Banner2_logo()
               print(printf)
            elif "-C" in sys.argv[1] and len(sys.argv)==2:
               Banner2_logo()
               print(printf)   
            else:   
                self._Input_Info()
    def _Input_Info(self):
        try: 
            run =Banner2_logo()
            Info = R+"                    "+"""For first time run 
                    To add an API key to ChatGPT, you'll need to create an account on the ChatGPT website.
                    Once you've created an account, you'll be able to generate an API key which you can then add to the ChatGPT tool.
                    To do this, go to the Settings page, click the 'API Keys' tab, and click the 'Generate API Key' button.
                    Copy the generated API key and paste it into the ChatGPT tool."""+W+'\n'\
                     +"                                                           "
            Info += Y+"https://www.openai.com"""+W+'\n'+\
            "                                        "                   
            Info += R+"""***************************************************************\n"""+W

            for word in Info:          
                sys.stdout.write(word)
                sys.stdout.flush()
                time.sleep(4./90)       
            try:
                Input_Key = str(input(Y+"🌏 add the API KEY   : "+W)).strip()
            except KeyboardInterrupt :
                 print(R+"\n⛔ Error          : KeyboardInterrupt")
                 exit()   
            with open('./Chat_Package/.KEY_AI.json','w') as APIKEY:
                APIKEY = APIKEY.write("{"+'\n'\
                    +'  "OPENAI_API_KEY" '+' : '+'"'+Input_Key+'"'+'\n'\
                    +"}")  
            def Test_API():
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
                    self.Control_all()
                else:
                    from Chat_Package.Error_HTTP import Error_HTTP
                    run = Error_HTTP(self)
                    for Code,Error in self.HTTP_Error_Codes.items():
                        if str(response.status_code) == Code :
                            print(R+"⛔ Error API         :",APIKEY+'\n'+"⛔ API repones code  : "+Code+"-"+Error+W)                      
                            if os.path.exists('./Chat_Package/.KEY_AI.json'):
                               os.remove('./Chat_Package/.KEY_AI.json')
                               break
                            exit()    
            Test_API() 
        except KeyboardInterrupt :
            print(R+"\n⛔ Error          : KeyboardInterrupt")
            exit()                             
    def Control_all(self):
        if "--webchat"in sys.argv  :
            from Chat_Package.Web_Chat import Web_side
            run = Web_side()
        elif "--terminal" in sys.argv:
            run = Banner_Logo()
            run = Chat_GPT()
        elif "-T" in sys.argv:
            run = Banner_Logo()
            run = Chat_GPT()  
        elif "-W" in sys.argv:
            from Chat_Package.Web_Chat import Web_side   
            run = Web_side()
        else:                
            print(printf)
        
                          
if __name__=='__main__':
    Control()
