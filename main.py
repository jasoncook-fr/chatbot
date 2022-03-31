from time import sleep_us, sleep
from ubinascii import b2a_base64
import random
from dictionary import StudioNames
from LCD import CharLCD
from anim import ANIM
import urequests
import _thread
import ujson
import netconn
import uping
import gc
gc.collect()

#init screen animation LEDs
a = ANIM()
'''
Sleep for a couple seconds at startup,
in case we need to interrupt for programming.
'''
sleep(2)

#values for LCD screens
lcd = CharLCD(rs=0,en=4,d4=5,d5=18,d6=19,d7=21,cols=16,rows=2)

#Website information for Nextcloud Talk session
username = 'nextcloudUserName'
password = 'nextcloudPassword'
host_URL = "https://yourDomain.ddns.net/"
room_Token = "xxxxxxxx"
website = host_URL + 'ocs/v1.php/apps/spreed/api/v1/chat/' + room_Token
headers = {'Accept': 'application/json','OCS-APIRequest': 'true'}

def encode_basic_auth(username, password):
    import ubinascii
    formated = b"{}:{}".format(username, password)
    formated = ubinascii.b2a_base64(formated)[:-1].decode("ascii")
    return {'Authorization' : 'Basic {}'.format(formated)}

def sendChatMsg(message):
    initData={'message': message}
    r = urequests.post(url=website, headers=headers, json=initData)
    rList = r.json()
    mesg = rList['ocs']['data']['id']
    return mesg

def evalMesg(string):
    global printFlag
    global msgStat
    global mesgA
    global mesgB
    global lastKnownMessageId
    c = " "
    indices = [pos for pos, char in enumerate(string) if char == c]
    strLen = len(string)
    indLen = len(indices)
    splitmark = int(strLen/2)
    targetIndex = 0
    if indLen > 0:
        if strLen - indices[indLen-1] > indices[indLen-1]:
            targetIndex = indices[indLen-1]
        else:
            for x in range(indLen):
                check = splitmark - indices[x]
                if check <= 0 and indices[x] <= 16:
                    targetIndex = indices[x]
                    break
                elif check < 0:
                    targetIndex = indices[x-1]
    else:
        targetIndex = len(string)

    mesgA = string[0:targetIndex]
    mesgB = string[targetIndex:len(string)]
    if len(mesgA) > 16 or len(mesgB) > 16:
        errorMsg='ERROR: bad message cut: '+'\n\r'+'1st Line: '+mesgA[0:16]+'\n\r'+'2nd line: '+mesgB[0:16]+'\n\r'
        lastKnownMessageId = sendChatMsg(errorMsg)
    else:
        msgStat = "CHAT"
        printFlag = True
        successMsg='PRINT SUCCESS!'+'\n\r'+'1st Line: '+mesgA[0:16]+'\n\r'+'2nd line: '+mesgB[0:16]+'\n\r'
        lastKnownMessageId = sendChatMsg(successMsg)


def lcd_task():
    lcd.clear()
    # print centered message
    lcd.set_line(0)
    lcd.message(mesgA, 2)
    lcd.set_line(1)
    lcd.message(mesgB, 2)

def second_thread():
    global printFlag
    global animStat
    global msgStat
    global mesgA
    global mesgB
    msgFlag = False

    while True:
        if printFlag is True:
            if msgStat is "NETWORK":
                mesgA = "CONNECTING TO"
                mesgB = "NETWORK"
                lcd_task()
                printFlag = False

            elif msgStat is "CHAT":
                lcd_task()
                animStat = "CENTER"
                printFlag = False

            elif msgStat is "DEFAULT":
                random.seed()
                mesgA = "STUDIO"
                mesgB = StudioNames[random.randint(0,(len(StudioNames)-1))]
                lcd_task()

        if animStat is "METEOR":
            a.meteorBounce()

        if animStat is "BOUNCE":
            a.meteorBounce(1,200,False,150,overScan=14)

        elif animStat is "CENTER":
            a.centreLight()

        elif animStat is "CHASE":
            a.runningLight()

        elif animStat is "ALERT":
            a.alert()

        elif animStat is "STACK":
            a.stack()

        elif animStat is "DEFAULT":
            msgStat = "DEFAULT"
            animStat = "METEOR"
            printFlag = True

commands = ["ALERT","CHASE","METEOR","CENTER","BOUNCE","STACK","DEFAULT", "IP"]
animStat = "CENTER"
msgStat = "NETWORK"
mesgA = ""
mesgB = ""
printFlag = True

_thread.start_new_thread(second_thread, ())
headers.update(encode_basic_auth(username, password))

while True:
    myIP, routerIP = netconn.connect()
    print("router address is: ", routerIP)
    print("my address is: ", myIP)
    #ping router to verify network connection
    try:
        uping.ping(routerIP)
        lastKnownMessageId = sendChatMsg("chatbot initialized")
        msgStat = "DEFAULT"
        animStat = "METEOR"
        printFlag = True
        pingFlag = True
    except:
        #print("PING LOST CONTACT!")
        msgStat = "NETWORK"
        printFlag = True
        pingFlag = False

    while pingFlag is True:
        #print("checking chatroom for data")
        msgData={'lookIntoFuture': '1', 'lastKnownMessageId': lastKnownMessageId, 'setReadMarker': '1', 'includeLastKnown': '0', 'actorDisplayName': 'Jason', 'timeout': '60'}
        try:
            r = urequests.get(url=website, headers=headers, json=msgData)
            rList = r.json()
            status = rList['ocs']['meta']['status']
            if status is 'failure':
                #print("no data found")
                pass

            elif status is 'ok':
                msg = rList['ocs']['data'][0]['message']
                msgLen = len(msg)
                if msg[:1] is "$":
                    #print("We have received a command!")
                    cmd = msg[1:].upper()
                    rcvMsg = "command received: " + cmd
                    lastKnownMessageId = sendChatMsg(rcvMsg)
                    if cmd is "HELP":
                        cmdList = '\n'.join(commands)
                        helpMsg = "available commands: \n" + cmdList + "\n"
                        lastKnownMessageId = sendChatMsg(helpMsg)
                    elif cmd is "IP":
                        ipMsg = "My local IP is: " + myIP + "\n" + "repl password is 'myPassword' \n"
                        lastKnownMessageId = sendChatMsg(ipMsg)
                    else:
                        cmdFlag = True
                        cmdCount = len(commands)
                        for x in range(cmdCount):
                            if cmd is commands[x]:
                                animStat = cmd
                                cmdFlag = True
                                break
                            else:
                                cmdFlag = False
                        if cmdFlag is False:
                            cmdList = '\n'.join(commands)
                            helpMsg = "ERROR: COMMAND INVALID \n available commands: \n" + cmdList + "\n"
                            lastKnownMessageId = sendChatMsg(helpMsg)


                elif msgLen > 32:
                    errorMsg = "ERROR: "+str(msgLen) + " characters is more than 32 limit"
                    lastKnownMessageId = sendChatMsg(errorMsg)
                else:
                    rcvMsg = "I received: " + msg
                    lastKnownMessageId = sendChatMsg(rcvMsg)
                    evalMesg(msg)
        except:
            msgStat = "NETWORK"
            animStat = "CENTER"
            printFlag = True
            pingFlag = False

