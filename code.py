#Screen Res:    1920x1200
#Window maximised
#Top banner and chat collapsed
#Scrollbar hidden by injecting "* { overflow: hidden; }" into the CSS of the site
#Play area: 65,174(top left) -> 1888,649(bottom right)

#TO-DO:
#   - Function placeCurrentBet() places bet on black by default. Change this so it can place bet on either (whatever is passed to it)
#   - Make it so any coordinates can be passed in and there is a gui when you launch the script that lets you set the coords

#-----------------------------#
# Imports
#-----------------------------#

import ImageGrab
import os
import time
import win32api, win32con
import ImageOps
from numpy import *


#-----------------------------#
# Global variables
#-----------------------------#

def locTime(): #its a function but acts like a variable
    return "["+time.strftime("%H:%M:%S")+"] " #localtime

x_padding=72
y_padding=173

ballValues={ #note that some balls might have the same values
    8721:"zero", #
    7344:"one", #
    7688:"two", #
    7887:"three", #
    7788:"four", #
    7887:"five", # #same as 3
    7716:"six", #
    7663:"seven", #
    7611:"eight", #
    7468:"nine", #
    7361:"ten", #
    6918:"eleven", #
    7361:"twelve", # #same as 10
    7611:"thirteen", # #same as 8
    7719:"fourteen", #
    2270:"chat not collapsed"
    } #0=green, 1-7=red, 8-14=black

barValues={ 
    "red":132,
    "gray":255,
    "grey":255
    }


#-----------------------------#
# Classes
#-----------------------------#

class Cord: #class holding all coordinates
    
    #b_ prefix denotes any buttons handling the bankroll/bets
    b_clear=(52,263)
    b_1plus=(149,264)
    b_10plus=(193,268)
    b_double=(407,261)
    
    #bet_ prefix denotes the location of the bet placing buttons
    bet_black=(1311,399)

    #ball_ prefix denotes ball locations (without padding) and size values 
    ball_width=45
    ball_height=45
    ball_1=(679,143)
    ball_2=(726,143)
    ball_3=(773,143)
    ball_4=(820,143)
    ball_5=(867,143)
    ball_6=(914,143)
    ball_7=(961,143)
    ball_8=(1008,143)
    ball_9=(1055,143)
    ball_10=(1102,143)

    redBar=(104,196)

class playerVars: #class holding any values related to the user

    currentBet=1
    startingBet=1
    

#-----------------------------#
# Mouse funcs
#-----------------------------#

def leftDown(): #simulates LMB down
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    print "LMB down"

def leftUp(): #simulates LMB up
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    print "LMB up"

def leftClick(): #simulates LMB down then up
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print "LMB click"

def mousePos(cord): #changes mouse position instantly. cord = tuple (x,y)
    win32api.SetCursorPos((x_padding+cord[0],y_padding+cord[1]))

def get_cords(): #tool for finding mouse location
    x,y=win32api.GetCursorPos()
    x=x-x_padding
    y=y-y_padding
    print x,y


#-----------------------------#
# Misc funcs
#-----------------------------#

def screenGrab(): #screenshots of the game area
    box=(x_padding+1,y_padding+1,x_padding+1824,y_padding+476)
    im=ImageGrab.grab(box)
    #too verbose. pls ignore :)
    #im.save(os.getcwd()+'\\full_snap__'+str(int(time.time()))+'.png','PNG')
    return im

def grab(): #screenshots of the game area
    box=(x_padding+1,y_padding+1,x_padding+1824,y_padding+476)
    im=ImageOps.grayscale(ImageGrab.grab(box))
    a=array(im.getcolors())
    a=a.sum()
    print a
    return a

def get_bar(): #returns whether the bar is red or gray
    box=(Cord.redBar[0],Cord.redBar[1],Cord.redBar[0]+2,Cord.redBar[1]+5)
    im=ImageOps.grayscale(ImageGrab.grab(box))
    a=array(im.getcolors())
    a=a.sum()
    return a


#-----------------------------#
# Get ball value funcs
#-----------------------------#

def get_ball(cord):
    box=(cord[0]+x_padding,cord[1]+y_padding,cord[0]+x_padding+Cord.ball_width,cord[1]+y_padding+Cord.ball_height)
    im=ImageOps.grayscale(ImageGrab.grab(box))
    a=array(im.getcolors())
    a=a.sum()
    #no longer needed; verbose
    #print a
    #im.save(os.getcwd()+"\\b1__"+str(int(time.time()))+".png","PNG")
    return a

def get_ball_all():
    l=[]
    l.append(get_ball(Cord.ball_1))
    l.append(get_ball(Cord.ball_2))
    l.append(get_ball(Cord.ball_3))
    l.append(get_ball(Cord.ball_4))
    l.append(get_ball(Cord.ball_5))
    l.append(get_ball(Cord.ball_6))
    l.append(get_ball(Cord.ball_7))
    l.append(get_ball(Cord.ball_8))
    l.append(get_ball(Cord.ball_9))
    l.append(get_ball(Cord.ball_10))
    return l
    

#-----------------------------#
# Betting related funcs
#-----------------------------#

def placeCurrentBet(): #Places the current bet on black
    print "Placing current bet amount"
    mousePos(Cord.bet_black)
    time.sleep(.1)
    leftClick()
    print "Finished placing bet"

def setCurrentBet(betAmount): #bets however much is passed to it
    timesToClickTen,timesToClickOne=divmod(betAmount,10)
    print "Current bet set to: "+str(betAmount)
    print "Tens: "+str(timesToClickTen)+" | Ones: "+str(timesToClickOne)
    print "Placing current bet amount"
    
    mousePos(Cord.b_clear) #clear bet
    leftClick()
    
    for t in range(timesToClickTen): #click ten however many times needed
        time.sleep(.1)
        mousePos(Cord.b_10plus)
        leftClick()

    for o in range(timesToClickOne): #click one however many times needed
        time.sleep(.1)
        mousePos(Cord.b_1plus)
        leftClick()
        
    playerVars.currentBet=betAmount
    print "Finished setting current bet VAR"


#-----------------------------#
# Main func
#-----------------------------#

def main():
    
    userEnteredBetAmount=1
    userEnteredBetAmount=int(raw_input("Bet amount?"))
    print userEnteredBetAmount
    playerVars.currentBet=userEnteredBetAmount
    playerVars.startingBet=userEnteredBetAmount
    
    state=0 #0 = bar is gray; wait. 1 = bar is red; bet.
    hasBet=0
    multiplierTrue=0
    l1=[]
    while True:
        #see if its red or grey
        if get_bar()==barValues["grey"]:
            print locTime()+"bar is gray"
            state=0
            while state==0:
                if get_bar()==barValues["red"]:
                    break
        elif get_bar()==barValues["red"]:
            print locTime()+"bar is red"
            state=1
            hasBet=0
            l1=get_ball_all()
            if ballValues[l1[-1]] in ("eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen"):
                print locTime()+"WIN: " + ballValues[l1[-1]]
                playerVars.currentBet=playerVars.startingBet
                print locTime()+"bet has been reset to "+str(playerVars.startingBet)
                multiplierTrue=0
                print locTime()+"betting now... "+str(playerVars.currentBet)
                setCurrentBet(playerVars.currentBet)
                placeCurrentBet()
                print locTime()+"bet has been placed"
            else:
                print locTime()+"LOSS: " + ballValues[l1[-1]]
                print locTime()+"multiplying bet by 2..."
                multiplierTrue=1
                playerVars.currentBet*=2
                print locTime()+"betting now... "+str(playerVars.currentBet)
                setCurrentBet(playerVars.currentBet)
                placeCurrentBet()
                print locTime()+"bet has been placed"
            while state==1:
                if get_bar()==barValues["grey"]:
                    print locTime()+"i should wait now"
                    print locTime()+"breaking"
                    break
        else:
            print locTime()+"can't get bar value; waiting for 1.5 seconds."
            time.sleep(1.5)


if __name__ == '__main__':
    main()
