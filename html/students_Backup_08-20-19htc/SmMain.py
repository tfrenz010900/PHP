# Copyright 2018, Looking Glass Applications, LLC, All Rights Reserved.
#  Author:  Tim Crosno
#  Date Created:  7/1/2018
#  Last Update:  01/05/19
#  Python 3.5 on Debian Stretch with MariaDB (MySQL)
#  Originally Authored on Tim Crosno's Asus with LGA's PyCharm software.
#  Migrated to Intel NUC SM990005 late August 2018 to work directly on SQL/Maria DB.
#
#
#
#import argparse      #7/25/18 htc - from Terry's (UK) file player utility (artdmx_Script.py)
import binascii     #7/25/18 htc - from Terry's (UK) file player utility (artdmx_Script.py)
import logging      #7/25/18 htc - from Terry's (UK) file player utility (artdmx_Script.py)
import os           #7/25/18 htc - from Terry's (UK) file player utility (artdmx_Script.py)
import platform   #7/25/18 htc
#  import re           #7/25/18 htc - from Terry's (UK) file player utility (artdmx_Script.py) - Regular Expressions
import socket       #7/25/18 htc - from Terry's (UK) file player utility (artdmx_Script.py)
import struct       #7/25/18 htc - from Terry's (UK) file player utility (artdmx_Script.py)
import sys          #7/25/18 htc - from Terry's (UK) file player utility (artdmx_Script.py)
import time      #7/25/18 - used for time delays and log file timestamps, accurate to 100th second (maybe better??)

import datetime   #8/25/18 htc - used for date time delays

import json

import mysql.connector as mariadb  #8/13/18 htc - downloaded win654.msi installer package to get this work in win10.
import requests
import gc     #8/25/18 htc - found in google post to keep database connections cleaner from open/close a lot.

#this section START from Terry's artnet string to jpg utility I integrated on 9/3/18 htc.
import argparse
###import binascii
import io
###import os
###import sys
import numpy as np
from PIL import Image

#9/16/18 htc added subprocess
import subprocess


#this section END from Terry's artnet string to jpg utility I integrated on 9/3/18 htc.

#------------------------------------------------------------------------------------------------------------------
#GLOBAL VARIABLE SCOPE - with some program initialization/setup coding here too- 7/25/18 htc.

#8/25/18 htc - 1st setup GlobalMachineID for this unit.
global GlobalMachineID
GlobalMachineID = 'Machine ID NOT SET'





global smMainVersion
smMainVersion = '__SmMain_Ver6g-190121_htc.py'



#12/18/18 htc
global bolDisplaySessNoAndPitchNoOnMarqee
#bolDisplaySessNoAndPitchNoOnMarqee = True
bolDisplaySessNoAndPitchNoOnMarqee = False

global bolDisplayPitchNoOnMainLED
#bolDisplayPitchNoOnMainLED = True
bolDisplayPitchNoOnMainLED = False







global strStartupOptionsForTesting
global RunMode
global RunThisSessionNumber



cwd = str(os.getcwd())

#JustCheckingThis = os.sep   #should be separateor use by following statement
smCurrentFunctionName = ' - GLOBAL CODE  ***'

#parse arguments if this .py script called with args

ThisPythonScriptName = sys.argv[0]    #5/25/18 htc always "SmMain.py", but DOES give you the FULL PATH !!!!
##  - 5/25/18 htc - this doesn't help me at client sites, always "SmMain.py" - set above again manually from program actual name.# smMainVersion = sys.argv[0]
#if counter(sys.argv) > 0:              # 9/21/18 htc, took out 1st parm= "SESSION" , only take in session number as #1 arg.
#if len(sys.argv) > 1:
#    ScriptArgumentOne = sys.argv[1]
#    print(sys.argv[1])
#    RunMode = sys.argv[1]
#else:
#    RunMode = 'DefaultRunMode'
RunThisSessionNumber = 0
if len(sys.argv) > 1:
    ScriptArgumentTwo = sys.argv[1]
    ScriptArgumentOne = sys.argv[1]
#    print(sys.argv[1])
    RunMode = 'SESSION'
    if str(sys.argv[1]) > '0':
        RunThisSessionNumber = sys.argv[1]



#10/25/18 htc - moved these "Up" to prefent SyntaxWarning- assigned before global declaration message.
global SpeedFilePath
global NetworkSharePath
global StopFilePath1
global StopFilePath2
global SessionsLocalSaveFolder
global PathForFilesToDisplayOnDevice
global ImpactLocatorHomeFolder
global gintFinalImpactSMgridY
global gintFinalImpactSMgridX
global gstrFinalImpactSMgridX
global ThisSess_ShutdownMode



MainLogFileName = os.getcwd() + '/MainLog.txt'
bolMainLogExists = os.path.isfile(MainLogFileName)


#9/22/18 htc - had permission issues trying to open MainLog.txt for Append, just sudo'd a delete on it everytime for now, FUCK !!!!!!!!!!!!  WHAT FUCKING NEXT !!!!
if bolMainLogExists:
#  os.system('sudo rm ' + MainLogFileName)
  os.remove(MainLogFileName)                 #9/29/18 htc - changed to "os.remove" the "sudo" command was taking around 3 to 5 seconds to execute, STRANGE !!!!!!!!!!!!!!!!!!!!!!

# 7/27/18 htc -
bolMainLogExists = os.path.isfile(MainLogFileName)
if bolMainLogExists:
   statinfo = os.stat(MainLogFileName)
#   print ('MainLog.txt file size:' + str(statinfo.st_size))
   if statinfo.st_size > 100000:
       # os.remove(MainLogFile)
       MainLogFileObject = open(MainLogFileName, 'w')
       MainLogFileObject.writelines(str(time.localtime()) + ' : ' +smMainVersion + ' : Main -' +
                                    'MainLogFile Initialized - Size exceeded 100K.' +
                                    ' TZ:' + str(time.timezone) + '  GMT- ' + str(time.gmtime()))
   else:
       MainLogFileObject = open(MainLogFileName, 'a')
       MainLogFileObject.writelines(str(time.localtime()) + ' : ' +smMainVersion + ' : Main -' +
                                    'MainLogFile Opened For Append Writing.' +
                                    ' TZ:' + str(time.timezone) + '  GMT- ' + str(time.gmtime()))

else:
    MainLogFileObject = open(MainLogFileName, 'w')
    MainLogFileObject.writelines('Local Time: ' + time.strftime('%a, %d %b %Y %H:%M:%S',time.localtime()) + ' |** ' + smMainVersion + '-GLOBAL CODE **| ' +
                          'MMainLogFile Initialized - NEW file.' +
                          ' | TZ:' + str(time.timezone) + ' |  GMT- ' + time.strftime('%a, %d %b %Y %H:%M:%S',time.gmtime()) + '\n')

#GMT- Sat, 15 Sep 2018 22:35:18

# BUILD GLOBAL 1260 ARRAY STRUCTURE
#    WriteLogFile('Initializing 1260 LED Internal Array:', '0004- GLOBAL ROUTINE  -')




#01/01/19 htc - added SOUND ZONE Values "hard coded"
global gstrSoundTopLeftX
global gintSoundTopLeftY
global gstrSoundBottomRightX
global gintSoundBottomRightY
global gbolHomeRunThisPitch
gbolHomeRunThisPitch = False

gstrSoundTopLeftX = ''
gintSoundTopLeftY = 0
gstrSoundBottomRightX = ''
gintSoundBottomRightY = 0

#1/3/19 htc - set to LARGE AREA (Still doesn't "work" on Beginner target!!) Per TRF's request at Dallas baseball show.
gstrSoundTopLeftX = 'K'
gintSoundTopLeftY = 10
gstrSoundBottomRightX = 'P'
gintSoundBottomRightY = 16


#1/4/19 htc - set to MAX AREA (I didn't have a good selection of test pitches with on in the "box" defined above).  TEMPORARY !!!!!!!!!!!!
#gstrSoundTopLeftX = 'D'
#gintSoundTopLeftY = 5
#gstrSoundBottomRightX = 'T'
#gintSoundBottomRightY = 20

MainLogFileObject.writelines('Play Sound Coordinates: ' + gstrSoundTopLeftX + ', ' + str(gintSoundTopLeftY) + ' to ' + gstrSoundBottomRightX + ', ' + str(gintSoundBottomRightY) + '\n')




#11/30/18 htc Startup timing debug statement - trying to find out what's causing startup delay.
MainLogFileObject.writelines('Local Time: ' + time.strftime('%H:%M:%S',time.localtime()) + ' | Check Point 1 | ' + '\n')


# 7/29/18 htc - define the 'zero elements' of the array fields here.
LedArray1260SeqNo = [0]
LedArray1260ColNum = [0]
LedArray1260RowNum = [0]
LedArray1260HexColorValue = ['000000']

# 8/4/18 htc - added array for current target colors for success/miss checking
#Target780SeqNo = [0]    # these are not needed, they are redundant from 1260 array and can use values form 1260
#Target780ColNum = [0]    # these are not needed, they are redundant from 1260 array and can use values form 1260
#Target780RowNum = [0]    # these are not needed, they are redundant from 1260 array and can use values form 1260

Target780HexColorValue = ['000000']     # init "global" array for current target- only 780 entries for target area of LED only.

CurrTargetSuccessHexColorValue = '00f000'  #SM_Green  - DEFAULT ALL TARGETS TO GREEN FOR HIT FOR NOW.

##--------------SUCCESS, MISS, No-Pitch COUNTER VARIABLES
SuccessCount = 0
MissCount = 0
NoPitchCount = 0

ThisSess_MachineId = ''
ThisSess_AccountId = ''
ThisSess_SeqNumber = ''
ThisSess_InitialStatus = ''
ThisSess_CurrentStatus = ''
ThisSess_Type = ''
ThisSess_StandTargetGuid = ''
ThisSess_PracticeGuid = ''
ThisSess_GameLineUpGuid = ''
ThisSess_ArcadeGuid = ''
ThisSess_BallType = ''
ThisSess_DisplaySpeedSecs = 0
ThisSess_DisplayImpactSecs = 0
ThisSess_SuspendTimeOutSeconds_ReallyMINUTES = 15
ThisSess_DisplayRiverYN = 'N'  # Y = yes, N = no
ThisSess_DisplayPitchCountBarsYN = 'Y'
ThisSess_YdeltaPlusMinus3 = 0
ThisSess_PitchingDistanceFeet = 0
ThisSess_SystemOnLineYN = 'N'
ThisSess_ShutdownMode = 'NONE'
ThisSess_StudentDisplayName = '--------'
ThisSess_RepetitionCountLimit = 1
ThisSess_CurrentRepCount = 0

#8/29/18 htc - added hard coded path names for now.
SpeedFilePath = '/home/pi/NetworkShare/speed.txt'
NetworkSharePath = '/home/pi/NetworkShare'
StopFilePath1 = '/home/pi/NetworkShare/stop.txt'
StopFilePath2 = '/var/www/html/students/stop.txt'
#StopFilePath = '/var/www/html/students/stop.txt'
#9/22/18 htc - added 2 more paths because had to run out of "students" sub-folder in www/html area becasue PHP couldn't launch .py in /home/pi ?????
#9/30/18 hts - had to move to /var/... sub-folder for PHP/Web server permissions issue and access to files    SessionsLocalSaveFolder = '/home/pi/PitchSessionFiles'
SessionsLocalSaveFolder = '/var/www/html/students/PitchSessionFiles'
PathForFilesToDisplayOnDevice = '/var/www/html/students/PitchSessionFiles'    #10/30/18 htc - for some reason, Kris started using this folder. I only need it for initial disp in "5 windows".
ImpactLocatorHomeFolder = '/home/pi/ImpactLocator'
#9/22/18 htc - made these variables "global"



#11/30/18 htc Startup timing debug statement - trying to find out what's causing startup delay.
MainLogFileObject.writelines('Local Time: ' + time.strftime('%H:%M:%S',time.localtime()) + ' | Check Point 2 | ' + '\n')




#/10/26/18 htc - delete both stop files if exist every time program starts - I think this works best with new logic to kill old lefter over tasks of SmMain.py.
#9/23/18 htc - always remove these files if present.
if os.path.isfile(StopFilePath1):
    os.system('sudo chmod 777 ' +  StopFilePath1)
    os.system('sudo rm ' + StopFilePath1)
#time.sleep(.51)
if os.path.isfile(StopFilePath2):
    os.system('sudo chmod 777 ' +  StopFilePath2)
    os.system('sudo rm ' + StopFilePath2)
#time.sleep(.51)



#11/30/18 htc Startup timing debug statement - trying to find out what's causing startup delay.
MainLogFileObject.writelines('Local Time: ' + time.strftime('%H:%M:%S',time.localtime()) + ' | Check Point 3 | ' + '\n')




# **************************************************************  10/30/18 htc - Default .jpg displays in "5 windows" - Logo and Cam 1/2 Ozan startup snapshot


#10/30/18 htc - added copy of "latest" cam 1/2 snapshots to .jpg default display locations for PHP Pitch Log "5 boxes" to show cam views on "startup" of session.

if os.path.isfile(PathForFilesToDisplayOnDevice + '/Cam1CriticalFrame.jpg'):
    os.system('sudo chmod 777 ' +  PathForFilesToDisplayOnDevice + '/Cam1CriticalFrame.jpg')
    CmdCallResult = os.system('sudo rm ' + PathForFilesToDisplayOnDevice + '/Cam1CriticalFrame.jpg')

if os.path.isfile(PathForFilesToDisplayOnDevice + '/Cam2CriticalFrame.jpg'):
    os.system('sudo chmod 777 ' +  PathForFilesToDisplayOnDevice + '/Cam2CriticalFrame.jpg')
    CmdCallResult = os.system('sudo rm ' + PathForFilesToDisplayOnDevice + '/Cam2CriticalFrame.jpg')

if os.path.isfile(PathForFilesToDisplayOnDevice + '/Impact.jpg'):
    os.system('sudo chmod 777 ' +  PathForFilesToDisplayOnDevice + '/Impact.jpg')
    CmdCallResult = os.system('sudo rm ' + PathForFilesToDisplayOnDevice + '/Impact.jpg')



#11/30/18 htc Startup timing debug statement - trying to find out what's causing startup delay.
MainLogFileObject.writelines('Local Time: ' + time.strftime('%H:%M:%S',time.localtime()) + ' | Check Point 4 | ' + '\n')



if os.path.isfile('/home/pi/SmartMittLogoForInternalPgmDisplay.jpg'):
    CommandToCall = 'sudo cp ' + '/home/pi/SmartMittLogoForInternalPgmDisplay.jpg ' + PathForFilesToDisplayOnDevice + '/Impact.jpg'
    CmdCallResult = os.system(CommandToCall)

if os.path.isfile('/home/pi/Cam1-bg.png'):
    CommandToCall = 'sudo cp ' + '/home/pi/Cam1-bg.png ' + PathForFilesToDisplayOnDevice + '/Cam1CriticalFrame.jpg'
    CmdCallResult = os.system(CommandToCall)

if os.path.isfile('/home/pi/Cam2-bg.png'):
    CommandToCall = 'sudo cp ' + '/home/pi/Cam2-bg.png ' + PathForFilesToDisplayOnDevice + '/Cam2CriticalFrame.jpg'
    CmdCallResult = os.system(CommandToCall)



#11/30/18 htc Startup timing debug statement - trying to find out what's causing startup delay.
MainLogFileObject.writelines('Local Time: ' + time.strftime('%H:%M:%S',time.localtime()) + ' | Check Point 5 | ' + '\n')




# ******************************************************


#9/24/18 htc - clean up impact file if present.      #10/30/18 - this file location is obsolete, all dynamic display wiht path from PITCH TABLE SQL field.
#if os.path.isfile(PathForFilesToDisplayOnDevice + '/ImpactNEW.jpg'):
#    os.system('sudo chmod 777 ' +  PathForFilesToDisplayOnDevice + '/ImpactNEW.jpg')
#    os.system('sudo rm ' + PathForFilesToDisplayOnDevice + '/ImpactNEW.jpg')
#time.sleep(.51)
#9/24/18 htc - clean up crictial frame files if present.
#if os.path.isfile(PathForFilesToDisplayOnDevice + '/Cam1CriticalFrameNEW.png'):
#    os.system('sudo chmod 777 ' +  PathForFilesToDisplayOnDevice + '/Cam1CriticalFrameNEW.jpg')
#    os.system('sudo rm ' + PathForFilesToDisplayOnDevice + '/Cam1CriticalFrameNEW.png')
#time.sleep(.51)
#if os.path.isfile(PathForFilesToDisplayOnDevice + '/Cam2CriticalFrameNEW.png'):
#    os.system('sudo chmod 777 ' +  PathForFilesToDisplayOnDevice + '/Cam2CriticalFrameNEW.jpg')
#    os.system('sudo rm ' + PathForFilesToDisplayOnDevice + '/Cam2CriticalFrameNEW.png')
#time.sleep(.51)





#9/24/18 htc - always flush out network share on program startup.
for EachFile in os.listdir(NetworkSharePath):
    FileToRemoveFullPath = NetworkSharePath + '/' + EachFile
    os.remove(FileToRemoveFullPath)




#11/30/18 htc Startup timing debug statement - trying to find out what's causing startup delay.
MainLogFileObject.writelines('Local Time: ' + time.strftime('%H:%M:%S',time.localtime()) + ' | Check Point 6 | ' + '\n')




#9/11/18 htc - added "global" fields for current pitch
CurrPitch_PlateSpeedMPH = 0
CurrPitch_ReleaseSpeedMPH = 0
CurrPitch_PitchNumber = 0
CurrPitch_ImpactXstr = ''
CurrPitch_ImpactXint = 0
CurrPitch_ImpactYint = 0
CurrPitch_SpinRPM = 0
CurrPitch_SpinAxis = ''
CurrPitch_Call = ''
CurrPitch_DateTime = datetime
CurrPitch_TargetGUID = ''
CurrPitch_MovementInfo =''
CurrPitch_ExpectedPitch = ''
CurrPitch__ExpectedSpeedRange = ''
CurrPitch_MarqueeContent = ''
CurrPitch_PracticeModeHitZones = ''
CurrPitch_FullPath1 = ''
CurrPitch_FullPath2 = ''
CurrPitch_FullPath3 = ''
CurrPitch_FullPath4 = ''
CurrPitch_FullPath5 = ''
CurrPitch_FullPath6 = ''
#11/30/18 htc
CurrPitch_ImpactXstrZ1 = ''
CurrPitch_ImpactXintZ1 = 0
CurrPitch_ImpactYintZ1 = 0



#9/27/18 htc Added for PRACTICE MODE today :)   FUCKING FINALLY !!!!   Each "step" in Practice mode is a FRAME which is 1 record in the mode definition table.

CurrFrame_BaseTarget = ''
CurrFrame_SuccessCount = 0
CurrFrame_MissCount = 0
CurrFrame_TotalCount = 0
CurrFrame_MoveOnLiteral = ''
CurrFrame_MoveOnSuccessCount = 0
CurrFrame_MoveOnMissCount = 0
CurrFrame_MoveOnTotalCount = 0
CurrFrame_FrameNumber = 0
CurrFrame_PractModeGUID = ''
CurrFrame_PaintTargetSquareYN = 'N'
CurrFrame_StartX = ''
CurrFrame_StartY = 0
CurrFrame_EndXX = ''
CurrFrame_EndXY = 0



# 7/29/18 htc - copied in my Marquee Font Definitions
gfontA = 'A,5x7,00100,02020,30003,40004,55555,60006,70007'
gfontB = 'B,5x7,11110,20002,30003,44440,50005,60006,77770'
gfontC = 'C,5x7,01110,20002,30000,40000,50000,60006,07770'
gfontD = 'D,5x7,11100,20020,30003,40004,50005,60060,77700'
gfontE = 'E,5x7,11111,20000,30000,44444,50000,60000,77777'
gfontF = 'F,5x7,11111,20000,30000,44444,50000,60000,70000'
gfontG = 'G,5x7,01110,20002,30000,40000,50055,60006,07770'
gfontH = 'H,5x7,10001,20002,30003,44444,50005,60006,70007'
gfontI = 'I,5x7,11111,00200,00300,00400,00500,00600,77777'
gfontJ = 'J,5x7,00111,00020,00030,00040,00050,60060,07700'
gfontK = 'K,5x7,10001,20020,30300,44000,50500,60060,70007'
gfontL = 'L,5x7,10000,20000,30000,40000,50000,60000,77777'
gfontM = 'M,5x7,10001,22022,30303,40404,50005,60006,70007'
gfontN = 'N,5x7,10001,22002,30303,40404,50505,60066,70007'
gfontO = 'O,5x7,01110,20002,30003,40004,50005,60006,07770'
gfontP = 'P,5x7,11110,20002,30003,44440,50000,60000,70000'
gfontQ = 'Q,5x7,11110,20020,30030,40040,50050,66666,00077'
gfontR = 'R,5x7,11110,20002,30003,44440,50050,60006,70007'
gfontS = 'S,5X7,01111,20000,30000,04440,00005,00006,77770'
gfontT = 'T,5x7,11111,00200,00300,00400,00500,00600,00700'
gfontU = 'U,5x7,10001,20002,30003,40004,50005,60006,07770'
gfontV = 'V,5x7,10001,20002,30003,04040,05050,00600,00700'
gfontW = 'W,5x7,10001,20002,30003,40404,50505,60606,07770'
gfontX = 'X,5x7,10001,20002,03030,00400,05050,60006,70007'
gfontY = 'Y,5x7,10001,20002,03030,04040,00500,00600,00700'
gfontZ = 'Z,5x7,11111,00002,00030,00400,05000,60000,77777'
gfont1 = '1,5x7,01100,00200,00300,00400,00500,00600,07770'
gfont2 = '2,5x7,01110,20002,00030,00400,05000,60000,77777'
gfont3 = '3,5x7,11110,00002,00003,00440,00005,00006,77770'
gfont4 = '4,5x7,10000,20020,30030,44444,00050,00060,00070'
gfont5 = '5,5x7,11111,20000,30000,44444,00005,00006,77777'   #9/5/18 htc, changed very last digit from 0 to 7 to fill in that lower right corder on "5"s.
gfont6 = '6,5x7,01110,20000,30000,44440,50005,60006,07770'
gfont7 = '7,5x7,11111,00002,00030,00400,05000,60000,70000'
gfont8 = '8,5x7,01110,20002,30003,04440,50005,60006,07770'
gfont9 = '9,5x7,01110,20002,30003,04444,00005,00006,07770'
gfont0 = '0,5x7,01110,20002,30003,40404,50005,60006,07770'
gfont_ = '0,5x7,00000,00000,00000,00000,00000,00000,77777'
gfontDASH = '0,5x7,00000,00000,00000,44444,00000,00000,00000'
#
#11/29/18 htc - added font special characters.
gfontPLUS = '0,5x7,00000,00200,00300,44444,00500,00600,00000'
gfontEQUAL = '0,5x7,00000,00000,33333,00000,55555,00000,00000'
gfontDOT = '0,5x7,00000,00000,00000,00000,00000,06600,07700'
gfontSPACE = '0,5x7,00000,00000,00000,00000,00000,00000,00000'



# 7/29/18 htc - copied in SmartMitt Standard LED Color definitions.
#Public ConstP SM_Red_Hi = 'f00000'
#Public Const SM_Red_Med = '900000'
#Public Const SM_Red_Low = '400000'
# 03/27/18 htc - forced all to hi-intensity for UCLA outdoors
SM_Red_Hi = 'f00000'
SM_Red_Med = '900000'
SM_Red_Low = '400000'
SM_Green_Hi = '00f000'
SM_Green_Med = '009000'
SM_Green_Low = '004000'
SM_Blue_Hi = '0000f0'
SM_Blue_Med = '000090'
SM_Blue_Low = '000040'
SM_Yellow_Hi = 'f0f000'
SM_Yellow_Med = '909000'
SM_Yellow_Low = '404000'
SM_White_Hi = 'f0f0f0'
SM_White_Med = '909090'
SM_White_Low = '909090'
SM_Black = '000000'
SM_Off = '000000'
SM_Red = 'f00000'
SM_Green = '00f000'
SM_Blue = '0000f0'
SM_Yellow = 'f0f000'
SM_White = 'f0f0f0'


#12/04/18 htc - make intA-Z GLOBAL so I have them wherever I need them in code - trying to work out TRF's movement calcualtions - UGGGHHH!
global intA
global intB
global intC
global intD
global intE
global intF
global intG
global intH
global intI
global intJ
global intK
global intL
global intM
global intN
global intO
global intP
global intQ
global intR
global intS
global intT
global intU
global intV
global intW
global intX
global intY
global intZ


#11/30/18 htc Startup timing debug statement - trying to find out what's causing startup delay.
MainLogFileObject.writelines('Local Time: ' + time.strftime('%H:%M:%S',time.localtime()) + ' | Check Point 7 | ' + '\n')




#---------------------------------   END OF GLOBAL SECTION ---------------------------------------------------------------

#--------  TERRY from UK , August 2018, artnet string file to .jpg format code STARTS HERE

#!/usr/bin/env python3
"""
SmartMitt Artnet/RGB Hex Strings to Image converter - by Terry from UK, August 2018.
9/3/18 htc - integrated this in to HTC's current version of: SmMainVer2a.py.
    made copy of last SPEED led, last TARGET led, and last IMPACT led to 3 separate .jpg files in "home" folder.
"""

#### 8/13/18 htc added the following comments from Terry Cain's emails from August 2018 to tcrosno45@gmail.compile
####Cool, I have a script that works. It takes an argument for the input text file, and an argument for output file, output file extension dictates what image ####format, so if the output filename ends in .jpg it'll be a JPEG, .png a PNG etc...
####Example invocation: ./rgb2jpg.py rgb/ArtnetString_PitchAdvWithRiver.txt test.png
####if the input file doesn't exist, it'll have an exit status of 1
####Requires python libraries numpy and pillow.
###Firstly, save as a png, you'll generally get better quality. Have added a --width option and will generally make larger images.
###Here is the output when set to 500 pixels wide - ./rgb2jpg.py --width 500 rgb/ArtnetString_Numbers77.txt test.png
### 8/13/18 - Terry made this latest version for force 2 to 1 aspect ratio.

## 9/3/18 htc - moved "import stmts" up to my main import section a top of code.
##import argparse
##import binascii
##import io
##import os
##import sys
##import numpy as np
##from PIL import Image

def YevalNetLocPctCoordsV1(intPctOfYrow):
#9/14/18 htc - converted this code from MSM Access/VBA to Python.

# MAKE THIS LINE A WRITE-LOG STATEMENT
#Print  # 19, Now() & " : Ozans Raw Coords (Pct of X,Y): " & intPctOfXcol & ", " & intPctOfYrow

# 10-03-18 htc moved logging down to where called from,     WriteLogFile('Translate Y - Vertical up/dn value- Ozans IMPACT percentage = ' + str(intPctOfYrow), '0102-Evaluate Ozans Pct to Y Coord -')

#'2/11/18 htc - setup Translation from % of X,Y as % of net size (56"x44").
# NOT USED 9/15/18 htc    gdblStart1 = 0

    bolUseOriginal = False
    bolUseCustom1 = False
    bolUseCustom2 = True

    if bolUseCustom1:    #10/25/18 htc - "custom" with TRF 1st try Summer 2018.
        WriteLogFile('Using CUSTOM-ONE Values for Y translation of Ozan % of net to Row (1-26) :', '6543-YevalNetLocPctCoordsV1          -')
        gdblStart2 = 0
        gdblStart3 = 0
        gdblStart4 = 0
        gdblStart5 = 6
        gdblStart6 = 12
        gdblStart7 = 18
        gdblStart8 = 23
        gdblStart9 = 28
        gdblStart10 = 33
        gdblStart11 = 38
        gdblStart12 = 43
        gdblStart13 = 47
        gdblStart14 = 50
        gdblStart15 = 53
        gdblStart16 = 56
        gdblStart17 = 59
        gdblStart18 = 62
        gdblStart19 = 65
        gdblStart20 = 70
        gdblStart21 = 75
        gdblStart22 = 80
        gdblStart23 = 85
        gdblStart24 = 90
        gdblStart25 = 95
        gdblStart26 = 100


    if bolUseCustom2:  # 10/24/18 htc - TRF at 2228 threw for hr or two and came up with these.
        WriteLogFile('Using CUSTOM-TWO Values for Y translation of Ozan % of net to Row (1-26) :', '6543-YevalNetLocPctCoordsV1          -')
        gdblStart2 = 0
        gdblStart3 = 0
        gdblStart4 = 0
        gdblStart5 = 4
        gdblStart6 = 8
        gdblStart7 = 10
        gdblStart8 = 12
        gdblStart9 = 18
        gdblStart10 = 23
        gdblStart11 = 28
        gdblStart12 = 33
        gdblStart13 = 38
        gdblStart14 = 43
        gdblStart15 = 47
        gdblStart16 = 50
        gdblStart17 = 53
        gdblStart18 = 56
        gdblStart19 = 59
        gdblStart20 = 62
        gdblStart21 = 65
        gdblStart22 = 70
        gdblStart23 = 75
        gdblStart24 = 80
        gdblStart25 = 85
        gdblStart26 = 100

    if bolUseOriginal:      #From AIO Feb'18
        WriteLogFile('Using ORIGINAL (A.I.O.) Values for Y translation of Ozan % of net to Row (1-26) :', '6543-YevalNetLocPctCoordsV1          -')
        gdblStart1 = 0
        gdblStart2 = 0
        gdblStart3 = 0
        gdblStart4 = 0
        gdblStart5 = 3
        gdblStart6 = 9
        gdblStart7 = 12
        gdblStart8 = 17
        gdblStart9 = 23
        gdblStart10 = 27
        gdblStart11 = 30
        gdblStart12 = 34
        gdblStart13 = 37
        gdblStart14 = 40
        gdblStart15 = 43
        gdblStart16 = 47
        gdblStart17 = 50
        gdblStart18 = 53
        gdblStart19 = 57
        gdblStart20 = 60
        gdblStart21 = 64
        gdblStart22 = 67
        gdblStart23 = 70
        gdblStart24 = 75
        gdblStart25 = 80
        gdblStart26 = 85


    global gintFinalImpactSMgridY
    gintFinalImpactSMgridY = 0

    if intPctOfYrow < 1 or intPctOfYrow > 99:
        return (102)

    if intPctOfYrow < gdblStart2:
        gintFinalImpactSMgridY = 1
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart3:
        gintFinalImpactSMgridY = 2
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart4:
        gintFinalImpactSMgridY = 3
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart5:
        gintFinalImpactSMgridY = 4
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart6:
        gintFinalImpactSMgridY = 5
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart7:
        gintFinalImpactSMgridY = 6
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart8:
        gintFinalImpactSMgridY = 7
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart9:
        gintFinalImpactSMgridY = 8
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart10:
        gintFinalImpactSMgridY = 9
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart11:
        gintFinalImpactSMgridY = 10
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart12:
        gintFinalImpactSMgridY = 11
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart13:
        gintFinalImpactSMgridY = 12
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart14:
        gintFinalImpactSMgridY = 13
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart15:
        gintFinalImpactSMgridY = 14
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart16:
        gintFinalImpactSMgridY = 15
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart17:
        gintFinalImpactSMgridY = 16
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart18:
        gintFinalImpactSMgridY = 17
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart19:
        gintFinalImpactSMgridY = 18
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart20:
        gintFinalImpactSMgridY = 19
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart21:
        gintFinalImpactSMgridY = 20
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart22:
        gintFinalImpactSMgridY = 21
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart23:
        gintFinalImpactSMgridY = 22
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart24:
        gintFinalImpactSMgridY = 23
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart25:
        gintFinalImpactSMgridY = 24
        return(gintFinalImpactSMgridY)

    if intPctOfYrow < gdblStart26:
        gintFinalImpactSMgridY = 25
        return(gintFinalImpactSMgridY)

    gintFinalImpactSMgridY= 26
    return(gintFinalImpactSMgridY)


def XevalNetLocPctCoordsV1(intPctOfXcol):
 #9/14/18 htc - converted this code from MSM Access/VBA to Python.

 # MAKE THIS LINE A WRITE-LOG STATEMENT
 #Print  # 19, Now() & " : Ozans Raw Coords (Pct of X,Y): " & intPctOfXcol & ", " & intPctOfYrow

 # 10/03/18 htc - moved logging down to where called from.   WriteLogFile('Translate X - Horizontal rt/lft value- Ozans IMPACT percentage = ' + str(intPctOfXcol), '0101-Evaluate Ozans Pct to X-Y Coords -')

    bolUseCustom = True

 #'2/11/18 htc - setup Translation from % of X,Y as % of net size (56"x44").
 # NOT USED 9/15/18 htc    gdblStartA = 0

    bolUseOriginal = False
    bolUseCustom1 = False
    bolUseCustom2 = True

    if bolUseCustom1:  # 10/25/18 htc - "custom" with TRF 1st try Summer 2018.
        WriteLogFile('Using CUSTOM-ONE Values for X translation of Ozan % of net to Columns (A-Z) :','6521-XevalNetLocPctCoordsV1          -')
        gdblStartB = 5
        gdblStartC = 10
        gdblStartD = 12
        gdblStartE = 15
        gdblStartF = 18
        gdblStartG = 21
        gdblStartH = 24
        gdblStartI = 27
        gdblStartJ = 33
        gdblStartK = 39
        gdblStartL = 45
        gdblStartM = 49
        gdblStartN = 52
        gdblStartO = 55
        gdblStartP = 58
        gdblStartQ = 64
        gdblStartR = 70
        gdblStartS = 74
        gdblStartT = 77
        gdblStartU = 80
        gdblStartV = 82
        gdblStartW = 84
        gdblStartX = 87
        gdblStartY = 90
        gdblStartZ = 100

    if bolUseCustom2:  # 10/24/18 htc - TRF at 2228 threw for hr or two and came up with these.
        WriteLogFile('Using CUSTOM-TWO Values for X translation of Ozan % of net to Columns (A-Z) :','6521-XevalNetLocPctCoordsV1          -')
        gdblStartB = 0
        gdblStartC = 5
        gdblStartD = 10
        gdblStartE = 12
        gdblStartF = 15
        gdblStartG = 18
        gdblStartH = 21
        gdblStartI = 26
        gdblStartJ = 32
        gdblStartK = 38
        gdblStartL = 42
        gdblStartM = 45
        gdblStartN = 49
        gdblStartO = 52
        gdblStartP = 55
        gdblStartQ = 58
        gdblStartR = 62
        gdblStartS = 68
        gdblStartT = 70
        gdblStartU = 74
        gdblStartV = 77
        gdblStartW = 82
        gdblStartX = 84
        gdblStartY = 87
        gdblStartZ = 100


    if bolUseOriginal:  # From AIO Feb'18
        WriteLogFile('Using ORIGINAL (A.I.O.) Values for Y translation of Ozan % of net to Columns (A-Z) :', '6521-XevalNetLocPctCoordsV1          -')
        gdblStartA = 0
        gdblStartB = 10
        gdblStartC = 15
        gdblStartD = 17
        gdblStartE = 20
        gdblStartF = 23
        gdblStartG = 26
        gdblStartH = 29
        gdblStartI = 32
        gdblStartJ = 35
        gdblStartK = 38
        gdblStartL = 41
        gdblStartM = 44
        gdblStartN = 47
        gdblStartO = 50
        gdblStartP = 53
        gdblStartQ = 56
        gdblStartR = 59
        gdblStartS = 62
        gdblStartT = 65
        gdblStartU = 68
        gdblStartV = 71
        gdblStartW = 74
        gdblStartX = 78
        gdblStartY = 81
        gdblStartZ = 85


    global gintFinalImpactSMgridX
    global gstrFinalImpactSMgridX

    gintFinalImpactSMgridX = 0
    gstrFinalImpactSMgridX = ''

    if intPctOfXcol < 1 or intPctOfXcol > 99:
        return(101)

    if intPctOfXcol < gdblStartB:
        gintFinalImpactSMgridX = 1
        gstrFinalImpactSMgridX = 'A'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartC:
        gintFinalImpactSMgridX = 2
        gstrFinalImpactSMgridX = 'B'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartD:
        gintFinalImpactSMgridX = 3
        gstrFinalImpactSMgridX = 'C'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartE:
        gintFinalImpactSMgridX = 4
        gstrFinalImpactSMgridX = 'D'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartF:
        gintFinalImpactSMgridX = 5
        gstrFinalImpactSMgridX = 'E'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartG:
        gintFinalImpactSMgridX = 6
        gstrFinalImpactSMgridX = 'F'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartH:
        gintFinalImpactSMgridX = 7
        gstrFinalImpactSMgridX = 'G'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartI:
        gintFinalImpactSMgridX = 8
        gstrFinalImpactSMgridX = 'H'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartJ:
        gintFinalImpactSMgridX = 9
        gstrFinalImpactSMgridX = 'I'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartK:
        gintFinalImpactSMgridX = 10
        gstrFinalImpactSMgridX = 'J'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartL:
        gintFinalImpactSMgridX = 11
        gstrFinalImpactSMgridX = 'K'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartM:
        gintFinalImpactSMgridX = 12
        gstrFinalImpactSMgridX = 'L'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartN:
        gintFinalImpactSMgridX = 13
        gstrFinalImpactSMgridX = 'M'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartO:
        gintFinalImpactSMgridX = 14
        gstrFinalImpactSMgridX = 'N'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartP:
        gintFinalImpactSMgridX = 15
        gstrFinalImpactSMgridX = 'O'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartQ:
        gintFinalImpactSMgridX = 16
        gstrFinalImpactSMgridX = 'P'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartR:
        gintFinalImpactSMgridX = 17
        gstrFinalImpactSMgridX = 'Q'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartS:
        gintFinalImpactSMgridX = 18
        gstrFinalImpactSMgridX = 'R'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartT:
        gintFinalImpactSMgridX = 19
        gstrFinalImpactSMgridX = 'S'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartU:
        gintFinalImpactSMgridX = 20
        gstrFinalImpactSMgridX = 'T'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartV:
        gintFinalImpactSMgridX = 21
        gstrFinalImpactSMgridX = 'U'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartW:
        gintFinalImpactSMgridX = 22
        gstrFinalImpactSMgridX = 'V'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartX:
        gintFinalImpactSMgridX = 23
        gstrFinalImpactSMgridX = 'W'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartY:
        gintFinalImpactSMgridX = 24
        gstrFinalImpactSMgridX = 'X'
        return(gstrFinalImpactSMgridX)

    if intPctOfXcol < gdblStartZ:
        gintFinalImpactSMgridX = 25
        gstrFinalImpactSMgridX = 'Y'
        return(gstrFinalImpactSMgridX)

    gintFinalImpactSMgridX = 26
    gstrFinalImpactSMgridX = 'Z'
    return(gstrFinalImpactSMgridX)


def chunk(_iter, chunk_size):
    """
    Takes an iterator and chunks the data according to chunk size
    :param _iter: Iterator, a list, binary string etc...
    :param chunk_size: Chunk size
    :type chunk_size: int

    :return: List of chunked data
    :rtype: list
    """
    return [_iter[i:i + chunk_size] for i in range(0, len(_iter), chunk_size)]


def ArtnetTxtToJpg(input_file, output_file, width=300):
    """
    Takes an input hex file and creates an image from it

    :param input_file: Input file
    :type input_file: str
    :param output_file: Output file
    :type output_file: str
    """
    if not os.path.exists(input_file):
        WriteLogFile('Input does not exist, Trying to convert this INPUT FILE : [' + str(input_file) + '] to this OUTPUT FILE: [' + str(output_file) + ']',
                     'xxxx-ArtnetTxtToJpg          -')
#        print('Input file does not exist')
        sys.exit(187)

    # Read the data, convert hex to binary, then put it into a buffer
    rgb_hex = open(input_file, 'r').read().strip()
    rgb_hex = binascii.unhexlify(rgb_hex)
    buffer = io.BytesIO(rgb_hex)

    # Create initial Numpy array for the image,
    arr = np.zeros(shape=(26, 30, 3), dtype=np.uint8)

    # Loop row by row
    for index, row in enumerate(range(0, 26)):
        # Check if its an even row, as we'd need to flip
        reverse = index % 2 == 1

        # Read a row's worth of bytes
        row_data = buffer.read(90)

        # Split up binary string into 3byte chunks representing RGB
        row_rgb = chunk(row_data, 3)

        # Flip every other row of RGB bytes
        if reverse:
            row_rgb.reverse()

        # For each RGB column, write to the array
        for col, rgb in enumerate(row_rgb):
            arr[row, col] = (rgb[0], rgb[1], rgb[2])

    # Create image from array
    img = Image.fromarray(arr)

    height = 2 * width

    # Resize image
    img = img.resize((width, height), Image.NEAREST)

    img.save(output_file)


    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Text file containing hex string')
    parser.add_argument('output_file', help='Output file, should end with either .png or .jpg')
    parser.add_argument('--width', type=int, default=300, help='Width')



def ArtdmxToNDB():
    #10/09/18 htc - added repeat of write to NDB  like we had to do on old AIO/MS Access with Calls out to write utility we used then.
  ## 10/26/18 htc - took out to clean up log file.  WriteLogFile('Writing NdbArtNetCtrlString.txt to NDB/LED at 10.0.0.100:6454.  ', '0002b-ArtdmxToNDB     -')


    Artdmx_Script_Ver1a()

    time.sleep(.11)

    Artdmx_Script_Ver1a()


def Artdmx_Script_Ver1a():
    ## 10/26/18 htc - took out to clean up log file.     WriteLogFile('Writing NdbArtNetCtrlString.txt to NDB/LED at 10.0.0.100:6454.  ', '0002a-Artdmx_Script_Ver1a     -')

   logger = logging.getLogger('SmartMittArtDmxFileToNDB')
   logger.setLevel(logging.INFO)
   file_handler = logging.FileHandler('ArtNetWriteModuleLogFile.txt')  #7/25/18 htc changed in parens, hard code log file name
   stdout_handler = logging.StreamHandler()
   formatter = logging.Formatter('[%(asctime)s %(levelname)8s] %(message)s')
   file_handler.setFormatter(formatter)
   stdout_handler.setFormatter(formatter)
   logger.addHandler(file_handler)
   logger.addHandler(stdout_handler)

   #  print ('CheckPoint1: ArtdmxToNDB')

   ip_address = '10.0.0.100'
   port = 6454
   rgb_file = 'NdbArtNetCtrlString.txt'
   # Get RGB data from input file
   # print ('CheckPoint2: ArtdmxToNDB')
   try:
       with open(rgb_file, 'rb') as rgb_file:
           data = rgb_file.read()
           if len(data) != 7560:
               logger.critical('File length is not 7560 bytes, incorrect ArtNet RGB text file content, len is: ' + str(len(data)))

           data = binascii.unhexlify(data)
# 9/7/18 htc commented out          print('CheckPoint1: ArtdmxToNDB')

   except Exception as err:
       logger.exception('Failed to import RGB data. See the stack trace below', exc_info=err)
       sys.exit(2)

   try:
# 9/7/18 htc commented out       print('CheckPoint3: ArtdmxToNDB')
# 9/7/18 htc commented out       logger.info('Sending {0} RGB values to {1}:{2}'.format(int(len(data)/3), ip_address, port))

       # Max length of DMX data in a ArtDMX packet is 510 bytes so divide up the data so its in at most 510 byte chunks
       data_chunks = [data[i:i+510] for i in range(0, len(data), 510)]
# 9/7/18 htc commented out       logger.info('{0} ArtDMX packets to send'.format(len(data_chunks)))

       # Open Socket
       sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

       for universe, chunk in enumerate(data_chunks, start=1):
           # 0x5000 OpCode = ArtDMX,
           # 0, 14 = Protocol version 14
           artdmx_header = struct.pack('<8sHBB', b'Art-Net\0', 0x5000, 0, 14)
           artdmx_body = struct.pack('>BBBBH', 0, 0, universe, 0, len(chunk))

           pkt = artdmx_header + artdmx_body + chunk
           sock.sendto(pkt, (ip_address, port))
           # 9/7/18 htc commented out           logger.info('Sent packet {0} (length {1}) to {2}:{3}'.format(universe, len(pkt), ip_address, port))
 ##          logger.info('Packet {0} hex: {1}'.format(universe, binascii.hexlify(pkt).decode()))

   # 9/7/18 htc commented out       logger.info('Finished')
     #  print('done: ArtdmxToNDB')

   except Exception as err:
       logger.exception('Failed to send RGB data. See the stack trace below', exc_info=err)
       sys.exit(3)


def WriteLogFile(MessageToWrite: object, CallingFunctionName: object) -> object:

    if CallingFunctionName == '':
        PrintThisFunctionName = smCurrentFunctionName
    else:
        PrintThisFunctionName = CallingFunctionName

    StringToWrite = 'Local: ' + time.strftime('%m/%d/%y %H:%M:%S', time.localtime()) + ' | ' +  PrintThisFunctionName + ' | '  + \
                    str(MessageToWrite) + ' | TZ:'   + str(time.timezone) + ' |  GMT- ' + time.strftime('%m/%d/%y %H:%M:%S', time.gmtime()) + '\n'

    MainLogFileObject.writelines(StringToWrite)


#10/11/18 htc - copied time.strftime "man page" in here.
 #time.strftime(format[, t])

 #   Convert a tuple or struct_time representing a time as returned by gmtime() or localtime() to a string as specified by the format argument. If t is not provided, the current time as returned by localtime() is used. format must be a string. ValueError is raised if any field in t is outside of the allowed range. strftime() returns a locale dependent byte string; the result may be converted to unicode by doing strftime(<myformat>).decode(locale.getlocale()[1]).

  #  Changed in version 2.1: Allowed t to be omitted.

#    Changed in version 2.4: ValueError raised if a field in t is out of range.

 #   Changed in version 2.5: 0 is now a legal argument for any position in the time tuple; if it is normally illegal the value is forced to a correct one.

  #  The following directives can be embedded in the format string. They are shown without the optional field width and precision specification, and are replaced by the indicated characters in the strftime() result:
 #   Directive 	Meaning 	Notes
 #   %a 	Locale’s abbreviated weekday name.
 #   %A 	Locale’s full weekday name.
 #   %b 	Locale’s abbreviated month name.
 #   %B 	Locale’s full month name.
 #   %c 	Locale’s appropriate date and time representation.
 #   %d 	Day of the month as a decimal number [01,31].
 #   %H 	Hour (24-hour clock) as a decimal number [00,23].
 #   %I 	Hour (12-hour clock) as a decimal number [01,12].
 #   %j 	Day of the year as a decimal number [001,366].
 #   %m 	Month as a decimal number [01,12].
 #   %M 	Minute as a decimal number [00,59].
 #   %p 	Locale’s equivalent of either AM or PM. 	(NOTE 1)
 #   %S 	Second as a decimal number [00,61]. 	(NOTE 2)
 #   %U 	Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0. 	(NOTE 3)
 #   %w 	Weekday as a decimal number [0(Sunday),6].
 #   %W 	Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0. 	(NOTE 3)
 #   %x 	Locale’s appropriate date representation.
 #   %X 	Locale’s appropriate time representation.
 #   %y 	Year without century as a decimal number [00,99].
 #   %Y 	Year with century as a decimal number.
 #   %Z 	Time zone name (no characters if no time zone exists).
 #   %% 	A literal '%' character.

 #   Notes:
#    1    When used with the strptime() function, the %p directive only affects the output hour field if the %I directive is used to parse the hour.
#    2    The range really is 0 to 61; this accounts for leap seconds and the (very rare) double leap seconds.
#    3    When used with the strptime() function, %U and %W are only used in calculations when the day of the week and the year are specified.


def Build1260ArrayStucture():
    intLedNo = 1

    #this does the first 26 rows (780 lights) that are 30 LEDs per row.
    for intRow in range(1,27):   # loops 1 to 26
        for intCol in range(1,31):   # loops 1 to 30

            LedArray1260SeqNo.append (intLedNo)
            LedArray1260HexColorValue.append ('000000')
            LedArray1260RowNum.append (intRow)
            intInteger = int(intRow / 2)    # do some integer math to find out if on odd/even row in LED panel lines
            dblRemainder = (intRow /2) - intInteger  # if remainder = zero, on EVEN row, COUNT DOWN (backwards)
            if dblRemainder == 0:
                LedArray1260ColNum.append (31 - intCol)
            else:
                LedArray1260ColNum.append (intCol)

            intLedNo = intLedNo + 1

    #  Next intCol  - implied by python indentation rules
    #Next intRow   - implied by python indentation rules

   #6/20/18 htc  added marquee rows, 8 additional rows but with SIXTY (60) LED's per meter (row).
    for intRow in range(27,35):   # loops 27 to 34
        for intCol in range(1,61):   # loops 1 to 60

            LedArray1260SeqNo.append (intLedNo)
            LedArray1260HexColorValue.append ('000000')
            LedArray1260RowNum.append (intRow)
            intInteger = int(intRow / 2)    # do some integer math to find out if on odd/even row in LED panel lines
            dblRemainder = (intRow /2) - intInteger  # if remainder = zero, on EVEN row, COUNT DOWN (backwards)
            if dblRemainder == 0:
                LedArray1260ColNum.append (61 - intCol)
            else:
                LedArray1260ColNum.append (intCol)

            intLedNo = intLedNo + 1

    #  Next intCol  - implied by python indentation rules
    #Next intRow   - implied by python indentation rules


#8/8/18 htc - go ahead and build out the 780 entry list/array to for testing success/miss.  Then just populate from target with loop, 1 to 780.
   #this does the first 26 rows (780 lights) that are 30 LEDs per row.
    intLedNo = 1
    for intRow in range(1,27):   # loops 1 to 26
        for intCol in range(1,31):   # loops 1 to 30

            Target780HexColorValue.append ('000000')

            intLedNo = intLedNo + 1
    #  Next intCol  - implied by python indentation rules
    #Next intRow   - implied by python indentation rules


def BuildSelectedBaseTargetArrayForThisRun(TargetToDefine, strX1, intY1, strX2, intY2):
# 8/3/18 htc, build array to hold the target map only.  This can be copied to the target table part of the LED array w/ one stmt.
#9/29/18 htc, "merged" target defs for DYNAMIC practice mode (only allow ONE BOX for now) and standard targets for Standard Mode.

    global CurrentTargetName
    CurrentTargetName = TargetToDefine
    
    
    
#Clear the 1260 array and actually build the target in there (That's the list storage array "paint box" works on/in).
    ClearTargetArea()

#8/3/18 htc - now Find the target def for this session that was passed to this routine. (should have read from SESSION RECORD).
    if TargetToDefine == 'SMV1-EARLYDEV' or TargetToDefine == 'EarlyDev' or TargetToDefine == 'EarlyDevelopment' or TargetToDefine == 'Early Development':
        PaintThisBox(SM_Green, 9, 9, 22, 22)

    if TargetToDefine == 'SMV1-ED-R' or TargetToDefine == 'EarlyDevRiver' or TargetToDefine == 'EarlyDevelopmentRiver' or TargetToDefine == 'Early Development with River':
        PaintThisBox(SM_Yellow, 6, 6, 25, 25)  # River box
        PaintThisBox(SM_Off, 7, 7, 24, 24)   # Clear interior of River
        PaintThisBox(SM_Green, 9, 9, 22, 22)   # Paint in ED strike zone

    if TargetToDefine == 'SMV1-INTERMED' or TargetToDefine == 'Intermediate' or TargetToDefine == 'Intermed' or TargetToDefine == 'Intermediate Devlopment':
        PaintThisBox(SM_Green, 9, 9, 22, 22)  # Paint in IM strike zone
        PaintThisBox(SM_Red, 11, 11, 20, 20)  # Paint in IM internal red/miss zone

    if TargetToDefine == 'SMV1-IM-R' or TargetToDefine == 'IntermediateRiver' or TargetToDefine == 'IntermedRiver' or TargetToDefine == 'Intermediate Devlopment with River':
        PaintThisBox(SM_Yellow,6, 6, 25, 25)  # River box
        PaintThisBox(SM_Off, 7, 7, 24, 24)   # Clear interior of River
        PaintThisBox(SM_Green, 9, 9, 22, 22)  # Paint in IM strike zone
        PaintThisBox(SM_Red, 11, 11, 20, 20)  # Paint in IM internal red/miss zone

    if TargetToDefine == 'SMV1-SELECT' or TargetToDefine == 'Select' or TargetToDefine == 'Sel' or TargetToDefine == 'Select Development':
        PaintThisBox(SM_Green, 9, 9, 22, 22)  # Green success box
        PaintThisBox(SM_Red, 9, 12, 22, 19)  # Middle Read miss box

    if TargetToDefine == 'SMV1-SL-R' or TargetToDefine == 'SelectRiver' or TargetToDefine == 'SelRiver' or TargetToDefine == 'Select Development with River':
        PaintThisBox(SM_Yellow, 6, 6, 25, 25)  # River box
        PaintThisBox(SM_Off, 7, 7, 24, 24)  # Clear interior of River
        PaintThisBox(SM_Green, 9, 9, 22, 22)  # Green success box
        PaintThisBox(SM_Red, 9, 12, 22, 19)  # Middle Read miss box

    if TargetToDefine == 'SMV1-PITCHADV' or TargetToDefine == 'PitchersAdvantage' or TargetToDefine == 'PitchAdv' or TargetToDefine == 'Pitchers Advantage':
        PaintThisBox(SM_Green, 5, 9, 26, 22)  # Build big green box
        PaintThisBox(SM_Off, 5, 12, 26, 19)  # Clear middle out
        PaintThisBox(SM_Red, 9, 9, 22, 22)  # Paint in full red strike xon

    if TargetToDefine == 'SMV1-PA-R' or TargetToDefine == 'PitchersAdvantageRiver' or TargetToDefine == 'PitchAdvRiver' or TargetToDefine == 'PitchAdvantageRiver' or TargetToDefine == 'Pitchers Advantage with River':
        PaintThisBox(SM_Yellow, 4, 6, 27, 25)  # River box
        PaintThisBox(SM_Off, 5, 7, 26, 24)  # Clear interior of River
        PaintThisBox(SM_Green, 5, 9, 26, 22)  # Build big green box
        PaintThisBox(SM_Off, 5, 12, 26, 19)  # Clear middle out
        PaintThisBox(SM_Red, 9, 9, 22, 22)  # Paint in full red strike xon

    if TargetToDefine == 'SMV1-PRACTICE' or TargetToDefine == 'Practice' or TargetToDefine == 'Pract' or TargetToDefine == 'Target Outline' or TargetToDefine == 'TargetOutline':
        PaintThisBox(SM_Blue, 9, 9, 22, 22)  # Strike Zone box in blue
        PaintThisBox(SM_Off, 10, 10, 21, 21)  # clear interior to make strike zone blue outline

    if TargetToDefine == 'SMV1-PRACT-R' or TargetToDefine == 'PracticeRiver' or TargetToDefine == 'PractRiver' or TargetToDefine == 'Target Outline with River' or TargetToDefine == 'TargetOutlineRiver':
        PaintThisBox(SM_Yellow, 6, 6, 25, 25)  # # River box in Yellow
        PaintThisBox(SM_Off, 7, 7, 24, 24)  # Clear interior of River Box
        PaintThisBox(SM_Blue, 9, 9, 22, 22)  # Strike Zone box in blude
        PaintThisBox(SM_Off, 10, 10, 21, 21)  # clear interior to make strike zone blue outline

# htc - lay over practice mode targe area if defined.
    if str(strX1).upper() >= 'A' and str(strX1).upper() <= 'Z' and str(strX2).upper() >= 'A' and str(strX2).upper() <= 'Z':
        if int(intY1) >= 1 and int(intY1) <= 26 and int(intY2) >= 1 and int(intY2) <= 26:
            PaintThisBox(SM_Green, strX2int(strX1), int(intY1), strX2int(strX2), int(intY2))

    for intNo in range(1, 781):   # loops 1 to 780
        Target780HexColorValue[intNo] = LedArray1260HexColorValue[intNo]


def Write1260ArrayToArtnetFile():
    ### 9/18/81 htc too much log file clutter    WriteLogFile('write internal 1260 byte control array to NdbArtNetCtrlString.txt file:', '0005-Write1260ArrayToArtnetFile  -')

    rgb_file = 'NdbArtNetCtrlString.txt'

    ArnNetFileObject = open('NdbArtNetCtrlString.txt', 'w')

    # 7/29/18 htc - define the 'zero elements' of the array fields here.
#    LedArray1260SeqNo = [0]
#    LedArray1260ColNum = [0]
#    LedArray1260RowNum = [0]
#    LedArray1260HexColorValue = ['000000']


#this does the first 26 rows (760 lights) that are 30 LEDs per row.
    for intArrayPos in range(1,1261):   # loops 1 to 1260

        ArnNetFileObject.writelines(LedArray1260HexColorValue[intArrayPos])

    ArnNetFileObject.close()


def PaintThisBox(strColor6BytesIn, intStartCol, intStartRow, intEndCol, intEndRow):

### 9/18/81 htc too much log file clutter
#    WriteLogFile('PaintThisBox: (' + strColor6BytesIn + ', '  + str(intStartCol) + ', ' + str(intStartRow) + ' / ' + str(intEndCol) + ', ' + str(intEndRow) + ')', '0006-PaintThisBox          -')
#    print('PaintThisBox: ' + strColor6BytesIn + ', '  + str(intStartCol) + ', ' + str(intStartRow) + ' / ' + str(intEndCol) + ', ' + str(intEndRow))

#    if strColor6BytesIn < '0' or intEndRow < 0 or intEndRow > 26 or intStartRow < 1 or intStartRow > 26 or intEndCol < 1 or intEndCol > 30 or intStartCol < 1 or intStartCol > 30:
#        WriteLogFile('PaintThisBox: Invalid parameters passed to 0006-PaintThisBox - see previous line in log file for values.','0006-PaintThisBox          -')
#        goto(1)

    for intIX in range(1, 1261):  # loops 1 to 1260
        if LedArray1260RowNum[intIX] >= intStartRow and LedArray1260ColNum[intIX] >= intStartCol and LedArray1260RowNum[intIX] <= intEndRow and LedArray1260ColNum[intIX] <= intEndCol:
            LedArray1260HexColorValue[intIX] = strColor6BytesIn


def ClearTargetArea():

    for intIX in range(1, 781):  # loops 1 to 780
        LedArray1260HexColorValue[intIX] = '000000'


def ClearMarqueeArea():

    for intIX in range(781, 1261):  # loops 1 to 780
        LedArray1260HexColorValue[intIX] = '000000'


def DisplaySpeed(intSpeed, strColor, str8CharMarquee):
    ## 10/26/18 htc - took out to clean up log file.     WriteLogFile('display speed routine, (valid speeds 10 to 109), speed: ' + str(intSpeed), '0007-DisplaySpeed                -')

# 11/30/18 htc - added font COLOR and MARQUEE word for display of "release" speed if "Addon" > 0.

#clear the target area on LED
    PaintThisBox(SM_Off, 1, 1, 30, 26) #clear target area of LED
    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()

    if intSpeed == 0 or str(intSpeed) == '0' or intSpeed < 10 or str(intSpeed) < '10':
        return(999)

#   if intSpeed < 10 Or intSpeed > 109 Then Exit Function    7/30/18 htc - FIX VALIDATION ROUTINES LATER.

    if intSpeed > 99:
        PaintThisBox(strColor, 1, 4, 2, 19)
#        PaintThisBox(SM_Red_Med, 2, 6, 4, 17)
#        PaintThisBox(SM_Red_Med, 1, 18, 3, 19)
        intSpeed = str(intSpeed)
        SpeedDigitOne = intSpeed[1]
        SpeedDigitTwo = intSpeed[2]
    else:
        intSpeed = str(intSpeed)
        SpeedDigitOne = intSpeed[0]
        SpeedDigitTwo = intSpeed[1]


    if SpeedDigitOne == '1':
        PaintThisBox(strColor, 7, 4, 12, 5)
        PaintThisBox(strColor, 9, 6, 12, 17)
        PaintThisBox(strColor, 7, 18, 14, 19)

    if SpeedDigitTwo == '1':
        PaintThisBox(strColor, 18, 4, 23, 5)
        PaintThisBox(strColor, 20, 6, 23, 17)
        PaintThisBox(strColor, 18, 18, 25, 19)

    if SpeedDigitOne == '2':
        PaintThisBox(strColor, 5, 4, 14, 19)
        PaintThisBox(SM_Off, 5, 6, 11, 10)
        PaintThisBox(SM_Off, 8, 13, 14, 17)

    if SpeedDigitTwo == '2':
        PaintThisBox(strColor, 18, 4, 27, 19)
        PaintThisBox(SM_Off, 18, 6, 24, 10)
        PaintThisBox(SM_Off, 21, 13, 27, 17)

    if SpeedDigitOne == '3':
        PaintThisBox(strColor, 5, 4, 14, 19)
        PaintThisBox(SM_Off, 5, 6, 11, 10)
        PaintThisBox(SM_Off, 5, 13, 11, 17)

    if SpeedDigitTwo == '3':
        PaintThisBox(strColor, 18, 4, 27, 19)
        PaintThisBox(SM_Off, 18, 6, 24, 10)
        PaintThisBox(SM_Off, 18, 13, 24, 17)

    if SpeedDigitOne == '4':
        PaintThisBox(strColor, 5, 4, 14, 19)
        PaintThisBox(SM_Off, 8, 4, 11, 10)
        PaintThisBox(SM_Off, 5, 13, 11, 19)

    if SpeedDigitTwo == '4':
        PaintThisBox(strColor, 18, 4, 27, 19)
        PaintThisBox(SM_Off, 21, 4, 24, 10)
        PaintThisBox(SM_Off, 18, 13, 24, 19)

    if SpeedDigitOne == '5':
        PaintThisBox(strColor, 5, 4, 14, 19)
        PaintThisBox(SM_Off, 8, 6, 14, 10)
        PaintThisBox(SM_Off, 5, 13, 11, 17)

    if SpeedDigitTwo == '5':
        PaintThisBox(strColor, 18, 4, 27, 19)
        PaintThisBox(SM_Off, 21, 6, 27, 10)
        PaintThisBox(SM_Off, 18, 13, 24, 17)

    if SpeedDigitOne == '6':
        PaintThisBox(strColor, 5, 4, 14, 19)
        PaintThisBox(SM_Off, 8, 6, 14, 10)
        PaintThisBox(SM_Off, 8, 13, 11, 17)

    if SpeedDigitTwo == '6':
        PaintThisBox(strColor, 18, 4, 27, 19)
        PaintThisBox(SM_Off, 21, 6, 27, 10)
        PaintThisBox(SM_Off, 21, 13, 24, 17)

    if SpeedDigitOne == '7':
        PaintThisBox(strColor, 5, 4, 15, 5)
        PaintThisBox(strColor, 12, 6, 15, 19)

    if SpeedDigitTwo == '7':
        PaintThisBox(strColor, 18, 4, 28, 5)
        PaintThisBox(strColor, 25, 6, 28, 19)

    if SpeedDigitOne == '8':
        PaintThisBox(strColor, 5, 4, 14, 19)
        PaintThisBox(SM_Off, 8, 6, 11, 10)
        PaintThisBox(SM_Off, 8, 13, 11, 17)

    if SpeedDigitTwo == '8':
        PaintThisBox(strColor, 18, 4, 27, 19)
        PaintThisBox(SM_Off, 21, 6, 24, 10)
        PaintThisBox(SM_Off, 21, 13, 24, 17)

    if SpeedDigitOne == '9':
        PaintThisBox(strColor, 5, 4, 14, 12)
        PaintThisBox(SM_Off, 8, 6, 11, 10)
        PaintThisBox(strColor, 12, 13, 14, 19)

    if SpeedDigitTwo == '9':
        PaintThisBox(strColor, 18, 4, 27, 12)
        PaintThisBox(SM_Off, 21, 6, 24, 10)
        PaintThisBox(strColor, 25, 13, 27, 19)

    if SpeedDigitOne == '0':
        PaintThisBox(strColor, 5, 4, 14, 19)
        PaintThisBox(SM_Off, 8, 6, 11, 17)

    if SpeedDigitTwo == '0':
        PaintThisBox(strColor, 18, 4, 27, 19)
        PaintThisBox(SM_Off, 21, 6, 24, 17)

    if str8CharMarquee > '' or str8CharMarquee > ' ':
        MarqueeWord(str8CharMarquee, '')

    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()

#9/23/18 htc - after moving python program to bullshit fucking /php/students area, can't write this file like I used to, just skip for now.
#    ArtnetTxtToJpg('NdbArtNetCtrlString.txt', 'speed.jpg', width=300)


def RunBootUpLedCheck():

    WriteLogFile('Run LED panel exercise/self-check at bootup', '0008-RunBootUpLedCheck             -')

    ClearTargetArea()
    ClearMarqueeArea()

    # marquee exercise
#    MarqueeWord('TESTMODE', '')

#11/30/18 htc - added color and marquee WORD to the display speed routine call.
    DisplaySpeed(11, SM_Red_Med, 'TESTMODE')
    time.sleep(0.71)

    DisplaySpeed(22, SM_Red_Med, 'TESTMODE')
    time.sleep(0.71)

#    MarqueeWord('ABCDEFGH', '')

    DisplaySpeed(33, SM_Green_Med, 'ABCDEFGH')
    time.sleep(0.71)

    DisplaySpeed(44, SM_Green_Med, 'ABCDEFGH')
    time.sleep(0.71)

#    MarqueeWord('IJKLMNOP', '')

    DisplaySpeed(55, SM_Blue_Med, 'IJKLMNOP')
    time.sleep(0.71)

    DisplaySpeed(66, SM_Blue_Med, 'IJKLMNOP')
    time.sleep(0.71)

#    MarqueeWord('QRSTUVWX', '')

    DisplaySpeed(77, SM_Yellow_Med, 'QRSTUVWX')
    time.sleep(0.71)


    DisplaySpeed(88, SM_Yellow_Med, 'QRSTUVWX')
    time.sleep(0.71)

 #   MarqueeWord('YZ  2SP', '')

    DisplaySpeed(99, SM_Red_Med, 'YZ  2SP')
    time.sleep(0.71)

 #   MarqueeWord('- _=+-', '')

    DisplaySpeed(99, SM_Red_Med, '- _=+-')
    time.sleep(0.71)

#    MarqueeWord('0123456789-TOO LONG TEST', '')

    DisplaySpeed(99, SM_Red_Med, '0123456789-TOO LONG TEST')
    time.sleep(0.71)

#    MarqueeWord('23456789', '')

    DisplaySpeed(109, SM_Red_Med, '23456789')
    time.sleep(0.71)


    ClearTargetArea()
    MarqueeWord('TARGETS', '')
    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()
    time.sleep(0.81)

    BuildSelectedBaseTargetArrayForThisRun('SMV1-EARLYDEV', '-', 0, '-', 0)
    MarqueeWord('EARLYDEV', '')
    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()
    ArtnetTxtToJpg('NdbArtNetCtrlString.txt', 'SMV1-EARLYDEV.jpg', width=300)
    time.sleep(1.10)

    BuildSelectedBaseTargetArrayForThisRun('SMV1-ED-R', '-', 0, '-', 0)
    MarqueeWord('ED-RIVER', '')
    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()
    ArtnetTxtToJpg('NdbArtNetCtrlString.txt', 'SMV1-ED-R.jpg', width=300)
    time.sleep(1.10)

    BuildSelectedBaseTargetArrayForThisRun('SMV1-INTERMED', '-', 0, '-', 0)
    MarqueeWord('INTERMED', '')
    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()
    ArtnetTxtToJpg('NdbArtNetCtrlString.txt', 'SMV1-INTERMED.jpg', width=300)
    time.sleep(1.10)

    BuildSelectedBaseTargetArrayForThisRun('SMV1-IM-R', '-', 0, '-', 0)
    MarqueeWord('IM-RIVER', '')
    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()
    ArtnetTxtToJpg('NdbArtNetCtrlString.txt', 'SMV1-IM-R.jpg', width=300)
    time.sleep(1.10)

    BuildSelectedBaseTargetArrayForThisRun('SMV1-SELECT', '-', 0, '-', 0)
    MarqueeWord('SELECT', '')
    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()
    ArtnetTxtToJpg('NdbArtNetCtrlString.txt', 'SMV1-SELECT.jpg', width=300)
    time.sleep(1.10)

    BuildSelectedBaseTargetArrayForThisRun('SMV1-SL-R', '-', 0, '-', 0)
    MarqueeWord('SL-RIVER', '')
    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()
    ArtnetTxtToJpg('NdbArtNetCtrlString.txt', 'SMV1-SL-R.jpg', width=300)
    time.sleep(1.10)

    BuildSelectedBaseTargetArrayForThisRun('SMV1-PITCHADV', '-', 0, '-', 0)
    MarqueeWord('PITCHADV', '')
    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()
    ArtnetTxtToJpg('NdbArtNetCtrlString.txt', 'SMV1-PITCHADV.jpg', width=300)
    time.sleep(1.10)

    BuildSelectedBaseTargetArrayForThisRun('SMV1-PA-R', '-', 0, '-', 0)
    MarqueeWord('PA RIVER', '')
    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()
    ArtnetTxtToJpg('NdbArtNetCtrlString.txt', 'SMV1-PA-R.jpg', width=300)
    time.sleep(1.10)

    BuildSelectedBaseTargetArrayForThisRun('SMV1-PRACTICE', '-', 0, '-', 0)
    MarqueeWord('PRACTICE', '')
    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()
    ArtnetTxtToJpg('NdbArtNetCtrlString.txt', 'SMV1-PRACTICE.jpg', width=300)
    time.sleep(1.10)

    BuildSelectedBaseTargetArrayForThisRun('SMV1-PRACT-R', '-', 0, '-', 0)
    MarqueeWord('PM RIVER', '')
    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()
    ArtnetTxtToJpg('NdbArtNetCtrlString.txt', 'SMV1-PRACT-R.jpg', width=300)
    time.sleep(1.10)

    ClearTargetArea()
    ClearMarqueeArea()

    MarqueeWord('COUNTERS', '')

    global ThisSess_DisplayPitchCountBarsYN
    ThisSess_DisplayPitchCountBarsYN = 'Y'   # force so it will display the counters for "demo" / self-test.
    for intIX in range(1, 50):  # loops 1 to 50
        UpdateSuccessMissCountersInLedArray(intIX,intIX)
        Write1260ArrayToArtnetFile()
        ArtdmxToNDB()
 #       time.sleep(0.05)

    ClearTargetArea()

    ClearMarqueeArea()

    MarqueeWord('NO PITCH', '')

    for intIX in range(1, 21):  # loops 1 to 20
        UpdateNoPitchCountInLedArray(intIX)
        Write1260ArrayToArtnetFile()
        ArtdmxToNDB()
#        time.sleep(0.050)

    ClearTargetArea()
    ClearMarqueeArea()

    MarqueeWord('BYE !', '')
    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()

    time.sleep(3.050)

    ClearTargetArea()
    ClearMarqueeArea()
    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()


def MarqueeChar(strColor6BytesIn, intColumn, strGFONTstring):
# 7/31/18 htc - migrated from my Access/VBA version that used DB Table, this uses 1260Array.

#7/31/18 htc - do one line at a time, one pixel at a time, odd rows count up from column, odd count down.
# Process strGFONTstring row ONE of character in starting in column number provided.
    if strGFONTstring[6] == '1':
        LedArray1260HexColorValue[intColumn + 780] = strColor6BytesIn
    if strGFONTstring[7] == '1':
        LedArray1260HexColorValue[intColumn + 780 + 1] = strColor6BytesIn
    if strGFONTstring[8] == '1':
        LedArray1260HexColorValue[intColumn + 780 + 2] = strColor6BytesIn
    if strGFONTstring[9] == '1':
        LedArray1260HexColorValue[intColumn + 780 + 3] = strColor6BytesIn
    if strGFONTstring[10] == '1':
        LedArray1260HexColorValue[intColumn  + 780 + 4] = strColor6BytesIn

# Process strGFONTstring row TWO of character in starting in column number provided.
    if strGFONTstring[12] == '2':
        LedArray1260HexColorValue[121 - intColumn + 780] = strColor6BytesIn    # needs to be 111 (plus 780)
    if strGFONTstring[13] == '2':
        LedArray1260HexColorValue[121 - intColumn + 780 - 1] = strColor6BytesIn
    if strGFONTstring[14] == '2':
        LedArray1260HexColorValue[121 - intColumn + 780 - 2] = strColor6BytesIn
    if strGFONTstring[15] == '2':
        LedArray1260HexColorValue[121 - intColumn + 780 - 3] = strColor6BytesIn
    if strGFONTstring[16] == '2':
        LedArray1260HexColorValue[121 - intColumn  + 780 - 4] = strColor6BytesIn   #needs to be 107  (plus 780)

# Process strGFONTstring row THREE of character in starting in column number provided.
    if strGFONTstring[18] == '3':
        LedArray1260HexColorValue[intColumn + 780 + (60 * 2)] = strColor6BytesIn
    if strGFONTstring[19] == '3':
        LedArray1260HexColorValue[intColumn + 780 + (60 * 2) + 1] = strColor6BytesIn
    if strGFONTstring[20] == '3':
        LedArray1260HexColorValue[intColumn + 780 + (60 * 2) + 2] = strColor6BytesIn
    if strGFONTstring[21] == '3':
        LedArray1260HexColorValue[intColumn + 780 + (60 * 2) + 3] = strColor6BytesIn
    if strGFONTstring[22] == '3':
        LedArray1260HexColorValue[intColumn  + 780 + (60 * 2) + 4] = strColor6BytesIn

# Process strGFONTstring row FOUR of character in starting in column number provided.
    if strGFONTstring[24] == '4':
        LedArray1260HexColorValue[241 - intColumn + 780] = strColor6BytesIn
    if strGFONTstring[25] == '4':
        LedArray1260HexColorValue[241 - intColumn + 780 - 1] = strColor6BytesIn   # needs to be 230 (plus 780)
    if strGFONTstring[26] == '4':
        LedArray1260HexColorValue[241 - intColumn + 780 - 2] = strColor6BytesIn   # needs to be 229 (plus 780)
    if strGFONTstring[27] == '4':
        LedArray1260HexColorValue[241 - intColumn + 780 - 3] = strColor6BytesIn   # needs to be 228 (plus 780)
    if strGFONTstring[28] == '4':
        LedArray1260HexColorValue[241 - intColumn  + 780 - 4] = strColor6BytesIn

# Process strGFONTstring row FIVE of character in starting in column number provided.
    if strGFONTstring[30] == '5':
        LedArray1260HexColorValue[intColumn + 780 + (60 * 4)] = strColor6BytesIn
    if strGFONTstring[31] == '5':
        LedArray1260HexColorValue[intColumn + 780 + (60 * 4) + 1] = strColor6BytesIn
    if strGFONTstring[32] == '5':
        LedArray1260HexColorValue[intColumn + 780 + (60 * 4) + 2] = strColor6BytesIn
    if strGFONTstring[33] == '5':
        LedArray1260HexColorValue[intColumn + 780 + (60 * 4) + 3] = strColor6BytesIn
    if strGFONTstring[34] == '5':
        LedArray1260HexColorValue[intColumn  + 780 + (60 * 4) + 4] = strColor6BytesIn

# Process strGFONTstring row SIX of character in starting in column number provided.
    if strGFONTstring[36] == '6':
        LedArray1260HexColorValue[361 - intColumn + 780] = strColor6BytesIn   # needs to be 351 (plus 780)
    if strGFONTstring[37] == '6':
        LedArray1260HexColorValue[361 - intColumn + 780 - 1] = strColor6BytesIn
    if strGFONTstring[38] == '6':
        LedArray1260HexColorValue[361 - intColumn + 780 - 2] = strColor6BytesIn
    if strGFONTstring[39] == '6':
        LedArray1260HexColorValue[361 - intColumn + 780 - 3] = strColor6BytesIn
    if strGFONTstring[40] == '6':
        LedArray1260HexColorValue[361 - intColumn  + 780 - 4] = strColor6BytesIn   # needs to be 347 (plus 780)

# Process strGFONTstring row SEVEN of character in starting in column number provided.
    if strGFONTstring[42] == '7':
        LedArray1260HexColorValue[intColumn +780 + (60 * 6)] = strColor6BytesIn
    if strGFONTstring[43] == '7':
        LedArray1260HexColorValue[intColumn + 780 + (60 * 6) + 1] = strColor6BytesIn
    if strGFONTstring[44] == '7':
        LedArray1260HexColorValue[intColumn + 780 + (60 * 6) + 2] = strColor6BytesIn
    if strGFONTstring[45] == '7':
        LedArray1260HexColorValue[intColumn + 780 + (60 * 6) + 3] = strColor6BytesIn
    if strGFONTstring[46] == '7':
        LedArray1260HexColorValue[intColumn  + 780 + (60 * 6) + 4] = strColor6BytesIn


def MarqueeWord(WordToDisplay, strColor6BytesIn):

    WriteLogFile('MarqueeWord sub-routine with value: [' + str(WordToDisplay) + ']', '0009-MarqueeWord             -')

# 7/31/18 htc - ADD THIS ERROR/ STRING VALIDATOIN CHEKCING LATER
# if intLen < 1 Or intLen > 8 Then WRITE LOG FILE ERROR, GoTo EndMarqueeWord

    if strColor6BytesIn < "000000":
        strColor6BytesIn = "f0f0f0"

    ClearMarqueeArea()

    intLen = len(WordToDisplay)

#11/29/18 htc Marquee is only EIGHT characters long - chars on end (9+) "bunch Up" and make display look goofy.
    if intLen > 8:
        WriteLogFile('MarqueeWord sub-routine TRUNCATED input word to 8 characters: [' + str(WordToDisplay) + ']','0009-MarqueeWord             -')
        WordToDisplay = WordToDisplay[0:8]
        intLen = 8
#9/10/18 htc force string to UPPER CASE, if lower case is found, repeats the LAST uppercase character for rest of string'
#                "ALthrow" displays as "ALLLLLL"
    WordToDisplay = str(WordToDisplay).upper()
    for intInt in range(0,intLen ):
        strCurrChar = WordToDisplay[intInt]
        if strCurrChar == "A":
            strGfontValue = gfontA
        if strCurrChar == "B":
            strGfontValue = gfontB
        if strCurrChar == "C":
            strGfontValue = gfontC
        if strCurrChar == "D":
            strGfontValue = gfontD
        if strCurrChar == "E":
            strGfontValue = gfontE
        if strCurrChar == "F":
            strGfontValue = gfontF
        if strCurrChar == "G":
            strGfontValue = gfontG
        if strCurrChar == "H":
            strGfontValue = gfontH
        if strCurrChar == "I":
            strGfontValue = gfontI
        if strCurrChar == "J":
            strGfontValue = gfontJ
        if strCurrChar == "K":
            strGfontValue = gfontK
        if strCurrChar == "L":
            strGfontValue = gfontL
        if strCurrChar == "M":
            strGfontValue = gfontM
        if strCurrChar == "N":
            strGfontValue = gfontN
        if strCurrChar == "O":
            strGfontValue = gfontO
        if strCurrChar == "P":
            strGfontValue = gfontP
        if strCurrChar == "Q":
            strGfontValue = gfontQ
        if strCurrChar == "R":
            strGfontValue = gfontR
        if strCurrChar == "S":
            strGfontValue = gfontS
        if strCurrChar == "T":
            strGfontValue = gfontT
        if strCurrChar == "U":
            strGfontValue = gfontU
        if strCurrChar == "V":
            strGfontValue = gfontV
        if strCurrChar == "W":
            strGfontValue = gfontW
        if strCurrChar == "X":
            strGfontValue = gfontX
        if strCurrChar == "Y":
            strGfontValue = gfontY
        if strCurrChar == "Z":
            strGfontValue = gfontZ
        if strCurrChar == "1":
            strGfontValue = gfont1
        if strCurrChar == "2":
            strGfontValue = gfont2
        if strCurrChar == "3":
            strGfontValue = gfont3
        if strCurrChar == "4":
            strGfontValue = gfont4
        if strCurrChar == "5":
            strGfontValue = gfont5
        if strCurrChar == "6":
            strGfontValue = gfont6
        if strCurrChar == "7":
            strGfontValue = gfont7
        if strCurrChar == "8":
            strGfontValue = gfont8
        if strCurrChar == "9":
            strGfontValue = gfont9
        if strCurrChar == "0":
            strGfontValue = gfont0
        if strCurrChar == "_":
            strGfontValue = gfont_
        if strCurrChar == " ":
            strGfontValue = gfontSPACE
        if strCurrChar == "-":
            strGfontValue = gfontDASH

 #11/29/18 htc - added special characters below and fixed gfont_ above in font defs at heading of this program.
        if strCurrChar == "+":
            strGfontValue = gfontPLUS
        if strCurrChar == "=":
            strGfontValue = gfontEQUAL
        if strCurrChar == ".":
            strGfontValue = gfontDOT




        strColorBytesIn = 'f0f0f0'
        MarqueeChar(strColor6BytesIn, (intInt * 7) + 3, strGfontValue)


def UpdateSuccessMissCountersInLedArray(NumSuccess, NumMiss):

    # 9/11/18 htc - realized the green in the SUCCESS counter columns (physical led columns 1 and 2) could be
    #               mistaken for a SUCCESS in the impact evaluation routine.
    #       TO FIX:  I forced a slightly different color string instead of SM_Green ='00f000', Forced '00f001' for SUCCESS
    #                counters on left side of LED.

    #  9/9/18 htc - added check if displaying pitch counts or not.
    global ThisSess_DisplayPitchCountBarsYN
    checkitYN = str(ThisSess_DisplayPitchCountBarsYN[0:2]).upper()
    if ThisSess_DisplayPitchCountBarsYN == '' or ThisSess_DisplayPitchCountBarsYN == None or ThisSess_DisplayPitchCountBarsYN == 'None' or \
            str(ThisSess_DisplayPitchCountBarsYN[0]).upper() == 'Y' or str(ThisSess_DisplayPitchCountBarsYN[0:2]).upper() == 'ON':

 ## 10/26/18 htc - took out to clean up log file.        WriteLogFile('UpdateSuccessMissCountersInLedArray Success/miss values: [' + str(NumSuccess) + '/' + str(NumMiss) + ']', '0010-UpdateSuccessMissInLedArray-')

# 9/11/18 htc        if NumSuccess > 0: LedArray1260HexColorValue[780] = SM_Green
        if NumSuccess > 0: LedArray1260HexColorValue[780] = '00f001'
        if NumSuccess > 1: LedArray1260HexColorValue[721] = '00f001'
        if NumSuccess > 2: LedArray1260HexColorValue[720] = '00f001'
        if NumSuccess > 3: LedArray1260HexColorValue[661] = '00f001'
        if NumSuccess > 4: LedArray1260HexColorValue[660] = '00f001'
        if NumSuccess > 5: LedArray1260HexColorValue[601] = '00f001'
        if NumSuccess > 6: LedArray1260HexColorValue[600] = '00f001'
        if NumSuccess > 7: LedArray1260HexColorValue[541] = '00f001'
        if NumSuccess > 8: LedArray1260HexColorValue[540] = '00f001'
        if NumSuccess > 9: LedArray1260HexColorValue[481] = '00f001'
        if NumSuccess > 10: LedArray1260HexColorValue[480] = '00f001'
        if NumSuccess > 11: LedArray1260HexColorValue[421] = '00f001'
        if NumSuccess > 12: LedArray1260HexColorValue[420] = '00f001'
        if NumSuccess > 13: LedArray1260HexColorValue[361] = '00f001'
        if NumSuccess > 14: LedArray1260HexColorValue[360] = '00f001'
        if NumSuccess > 15: LedArray1260HexColorValue[301] = '00f001'
        if NumSuccess > 16: LedArray1260HexColorValue[300] = '00f001'
        if NumSuccess > 17: LedArray1260HexColorValue[241] = '00f001'
        if NumSuccess > 18: LedArray1260HexColorValue[240] = '00f001'
        if NumSuccess > 19: LedArray1260HexColorValue[181] = '00f001'
        if NumSuccess > 20: LedArray1260HexColorValue[180] = '00f001'
        if NumSuccess > 21: LedArray1260HexColorValue[121] = '00f001'
        if NumSuccess > 22: LedArray1260HexColorValue[120] = '00f001'
        if NumSuccess > 23: LedArray1260HexColorValue[61] = '00f001'
        if NumSuccess > 24: LedArray1260HexColorValue[60] = '00f001'
        if NumSuccess > 25: LedArray1260HexColorValue[779] = '00f001'
        if NumSuccess > 26: LedArray1260HexColorValue[722] = '00f001'
        if NumSuccess > 27: LedArray1260HexColorValue[719] = '00f001'
        if NumSuccess > 28: LedArray1260HexColorValue[662] = '00f001'
        if NumSuccess > 29: LedArray1260HexColorValue[659] = '00f001'
        if NumSuccess > 30: LedArray1260HexColorValue[602] = '00f001'
        if NumSuccess > 31: LedArray1260HexColorValue[599] = '00f001'
        if NumSuccess > 32: LedArray1260HexColorValue[542] = '00f001'
        if NumSuccess > 33: LedArray1260HexColorValue[539] = '00f001'
        if NumSuccess > 34: LedArray1260HexColorValue[482] = '00f001'
        if NumSuccess > 35: LedArray1260HexColorValue[479] = '00f001'
        if NumSuccess > 36: LedArray1260HexColorValue[422] = '00f001'
        if NumSuccess > 37: LedArray1260HexColorValue[419] = '00f001'
        if NumSuccess > 38: LedArray1260HexColorValue[362] = '00f001'
        if NumSuccess > 39: LedArray1260HexColorValue[359] = '00f001'
        if NumSuccess > 40: LedArray1260HexColorValue[302] = '00f001'
        if NumSuccess > 41: LedArray1260HexColorValue[299] = '00f001'
        if NumSuccess > 42: LedArray1260HexColorValue[242] = '00f001'
        if NumSuccess > 43: LedArray1260HexColorValue[239] = '00f001'
        if NumSuccess > 44: LedArray1260HexColorValue[182] = '00f001'
        if NumSuccess > 45: LedArray1260HexColorValue[179] = '00f001'
        if NumSuccess > 46: LedArray1260HexColorValue[122] = '00f001'
        if NumSuccess > 47: LedArray1260HexColorValue[119] = '00f001'
        if NumSuccess > 48: LedArray1260HexColorValue[62] = '00f001'
        if NumSuccess > 49: LedArray1260HexColorValue[59] = '00f001'

        if NumMiss > 0: LedArray1260HexColorValue[751] = SM_Red
        if NumMiss > 1: LedArray1260HexColorValue[750] = SM_Red
        if NumMiss > 2: LedArray1260HexColorValue[691] = SM_Red
        if NumMiss > 3: LedArray1260HexColorValue[690] = SM_Red
        if NumMiss > 4: LedArray1260HexColorValue[631] = SM_Red
        if NumMiss > 5: LedArray1260HexColorValue[630] = SM_Red
        if NumMiss > 6: LedArray1260HexColorValue[571] = SM_Red
        if NumMiss > 7: LedArray1260HexColorValue[570] = SM_Red
        if NumMiss > 8: LedArray1260HexColorValue[511] = SM_Red
        if NumMiss > 9: LedArray1260HexColorValue[510] = SM_Red
        if NumMiss > 10: LedArray1260HexColorValue[451] = SM_Red
        if NumMiss > 11: LedArray1260HexColorValue[450] = SM_Red
        if NumMiss > 12: LedArray1260HexColorValue[391] = SM_Red
        if NumMiss > 13: LedArray1260HexColorValue[390] = SM_Red
        if NumMiss > 14: LedArray1260HexColorValue[331] = SM_Red
        if NumMiss > 15: LedArray1260HexColorValue[330] = SM_Red
        if NumMiss > 16: LedArray1260HexColorValue[271] = SM_Red
        if NumMiss > 17: LedArray1260HexColorValue[270] = SM_Red
        if NumMiss > 18: LedArray1260HexColorValue[211] = SM_Red
        if NumMiss > 19: LedArray1260HexColorValue[210] = SM_Red
        if NumMiss > 20: LedArray1260HexColorValue[151] = SM_Red
        if NumMiss > 21: LedArray1260HexColorValue[150] = SM_Red
        if NumMiss > 22: LedArray1260HexColorValue[91] = SM_Red
        if NumMiss > 23: LedArray1260HexColorValue[90] = SM_Red
        if NumMiss > 24: LedArray1260HexColorValue[31] = SM_Red
        if NumMiss > 25: LedArray1260HexColorValue[752] = SM_Red
        if NumMiss > 26: LedArray1260HexColorValue[749] = SM_Red
        if NumMiss > 27: LedArray1260HexColorValue[692] = SM_Red
        if NumMiss > 28: LedArray1260HexColorValue[689] = SM_Red
        if NumMiss > 29: LedArray1260HexColorValue[632] = SM_Red
        if NumMiss > 30: LedArray1260HexColorValue[629] = SM_Red
        if NumMiss > 31: LedArray1260HexColorValue[572] = SM_Red
        if NumMiss > 32: LedArray1260HexColorValue[569] = SM_Red
        if NumMiss > 33: LedArray1260HexColorValue[512] = SM_Red
        if NumMiss > 34: LedArray1260HexColorValue[509] = SM_Red
        if NumMiss > 35: LedArray1260HexColorValue[452] = SM_Red
        if NumMiss > 36: LedArray1260HexColorValue[449] = SM_Red
        if NumMiss > 37: LedArray1260HexColorValue[392] = SM_Red
        if NumMiss > 38: LedArray1260HexColorValue[389] = SM_Red
        if NumMiss > 39: LedArray1260HexColorValue[332] = SM_Red
        if NumMiss > 40: LedArray1260HexColorValue[329] = SM_Red
        if NumMiss > 41: LedArray1260HexColorValue[272] = SM_Red
        if NumMiss > 42: LedArray1260HexColorValue[269] = SM_Red
        if NumMiss > 43: LedArray1260HexColorValue[212] = SM_Red
        if NumMiss > 44: LedArray1260HexColorValue[209] = SM_Red
        if NumMiss > 45: LedArray1260HexColorValue[152] = SM_Red
        if NumMiss > 46: LedArray1260HexColorValue[149] = SM_Red
        if NumMiss > 47: LedArray1260HexColorValue[92] = SM_Red
        if NumMiss > 48: LedArray1260HexColorValue[89] = SM_Red
        if NumMiss > 49: LedArray1260HexColorValue[32] = SM_Red


def UpdateNoPitchCountInLedArray(NoPitchCount):

    #  9/9/18 htc - added check if displaying pitch counts or not.
    global ThisSess_DisplayPitchCountBarsYN
    if ThisSess_DisplayPitchCountBarsYN == '' or  str(ThisSess_DisplayPitchCountBarsYN[0]).upper() == 'Y':

 ## 10/26/18 htc - took out to clean up log file.  WriteLogFile('UpdateNoPitchCountInLedArray: [' + str(NoPitchCount) + ']', '0011-UpdateNoPitchCountInLedArray-')

# 10/12/18 htc - changed color to BLUE per TRF's request and added ColorCodeToUse variable.
#        ColorCodeToUse = SM_Yellow
        ColorCodeToUse = SM_Blue

        if NoPitchCount > 0: LedArray1260HexColorValue[766] = ColorCodeToUse
        if NoPitchCount > 1: LedArray1260HexColorValue[765] = ColorCodeToUse
        if NoPitchCount > 2: LedArray1260HexColorValue[767] = ColorCodeToUse
        if NoPitchCount > 3: LedArray1260HexColorValue[764] = ColorCodeToUse
        if NoPitchCount > 4: LedArray1260HexColorValue[768] = ColorCodeToUse
        if NoPitchCount > 5: LedArray1260HexColorValue[763] = ColorCodeToUse
        if NoPitchCount > 6: LedArray1260HexColorValue[769] = ColorCodeToUse
        if NoPitchCount > 7: LedArray1260HexColorValue[762] = ColorCodeToUse
        if NoPitchCount > 8: LedArray1260HexColorValue[770] = ColorCodeToUse
        if NoPitchCount > 9: LedArray1260HexColorValue[761] = ColorCodeToUse
        if NoPitchCount > 10: LedArray1260HexColorValue[771] = ColorCodeToUse
        if NoPitchCount > 11: LedArray1260HexColorValue[760] = ColorCodeToUse
        if NoPitchCount > 12: LedArray1260HexColorValue[772] = ColorCodeToUse
        if NoPitchCount > 13: LedArray1260HexColorValue[759] = ColorCodeToUse
        if NoPitchCount > 14: LedArray1260HexColorValue[773] = ColorCodeToUse
        if NoPitchCount > 15: LedArray1260HexColorValue[758] = ColorCodeToUse
        if NoPitchCount > 16: LedArray1260HexColorValue[774] = ColorCodeToUse
        if NoPitchCount > 17: LedArray1260HexColorValue[757] = ColorCodeToUse
        if NoPitchCount > 18: LedArray1260HexColorValue[775] = ColorCodeToUse
        if NoPitchCount > 19: LedArray1260HexColorValue[756] = ColorCodeToUse


def EvalSuccessMiss(BallType, impactXnum, impactYnum):

    WriteLogFile('EvalSuccessMiss: [' + BallType + ', ' + str(impactXnum) + ', ' + str(impactYnum) + ']', '0021-EvalSuccessMiss                   -')

    if str(impactXnum) == 'None' or str(impactXnum) == 'none' or str(impactXnum) == '' or impactXnum < 1 or impactXnum > 26 or impactYnum < 1 or impactYnum > 26:
        return('NO PITCH')
#    CurrTargetSuccessHexColorValue = '00f000'  # SM_Green  -SET IN GLOBAL AREA   8/8/18 htc - for NOW, only SUCCESS COLOR is GREEN '00f000'
#     Target780HexColorValue = LedArray1260HexColorValue.copy()      this is why this routine works, base target was copied to 780 array when it was initially built.

#8/8/18 htc - the reason X (Right/Left) and Y (Up/Down) Variance is different is because X light spacing is 1.3" (30/meter) and Y is 2.6"


# 9/11/18 htc *****************************************************************************************************************

#9/11/18 htc - realized the LEFT side 2 physical LED rows are SUCCESS Counters that are GREEN !
#              So I "forced" some code here if impact in any of the FOUR side rows on EITHER SIDE = MISS !
# 9/15/18 htc - I changed the color of greeen slightly for the Green side bar in col 1 and 2, this is not needed now!!!
#   if impactXnum >= 1 and impactXnum <= 4:
#       return ('MISS')
#   if impactXnum >= 27 and impactXnum <= 30:
#       return ('MISS')

# 9/11/18 htc *****************************************************************************************************************

#****************************************************************************************************************
# ****************************************************************************************************************
# ****************************************************************************************************************
# ****************************************************************************************************************

#9/15/18 - HTC - Figured out had to ADD TWO (2) to the X (horizontal) integer value to evaluate success/miss
#                The rows (Y value) are OK.
#                A or column 1 is actually physically colum 3 in the led grid,
#                The Target780NexColorValue array has 30 lights per row to match the physical LED strips (30/meter).
#                All the ball impact location logic runs on 26 columns and 26 rows., physical col 3 through 28 !!!
#                Of course, Columns 1/2, and 29/30 are reserved for pitch count "bars"- red/green

    impactXnum = impactXnum + 2


# ****************************************************************************************************************
# ****************************************************************************************************************
# ****************************************************************************************************************
# ****************************************************************************************************************

    if len(BallType) > 4:
       BallType = str(BallType[0:4]).upper()

    else:
       BallType = str(BallType).upper()

    if BallType == 'BASE':     # BASEballs get +/- ONE COLUM LEFT and RIGHT, NO Variance on "Y" axis (Up and down).

        if impactXnum == 1:
            if Target780HexColorValue[SeqLightNo(1, impactYnum)] == CurrTargetSuccessHexColorValue:
                return ('SUCCESS')
            if Target780HexColorValue[SeqLightNo(1 + 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                return ('SUCCESS')

        if impactXnum == 30:
            if Target780HexColorValue[SeqLightNo(30, impactYnum)] == CurrTargetSuccessHexColorValue:
                return('SUCCESS')
            if Target780HexColorValue[SeqLightNo(30 - 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                return('SUCCESS')

        if impactXnum >= 2 and impactXnum <= 29:
            if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum)] == CurrTargetSuccessHexColorValue:
                return('SUCCESS')
            if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                return('SUCCESS')
            if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                return('SUCCESS')
#----8/8/18 htc ---------------------END OF BASE BALL, Simple becuase variance is +/- 1 on cols only, not rows!!


    if BallType == 'SOFT':     # SOFTballs get +/- TWO COLUM LEFT and RIGHT, and +/- ONE ROW Variance on "Y" axis (Up and down).

        if impactYnum == 1 or impactYnum == 26:   # hit on row one or row 26, check this row and row 2 for THIS Colum and +/- 2 colums
#first check the row we are "on", impactYnum, or 1 in this case.
            if impactXnum == 1:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 2, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 2:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 2, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 30:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 2, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return('SUCCESS')

            if impactXnum == 29:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 2, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return('SUCCESS')

            if impactXnum >= 3 and impactXnum <= 28:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 2, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 2, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return('SUCCESS')

# then check the next row (row + 1 = 2) IF ROW ONE (impactYnum + 1) because Softballs get +/- one row, plus one row in this case.
        if impactYnum == 1:
            if impactXnum == 1:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 2, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 2:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 2, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 30:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 2, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 29:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 2, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum >= 3 and impactXnum <= 28:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 2, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 2, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

    # then check the PREVIOUS row (row -1 = 29) IF ROW THIRTY (impactYnum - 1) because Softballs get +/- one row, plus one row in this case.
        if impactYnum == 26:
            if impactXnum == 1:
                if Target780HexColorValue[
                    SeqLightNo(impactXnum, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum + 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum + 2, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 2:
                if Target780HexColorValue[
                    SeqLightNo(impactXnum, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum + 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum + 2, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum - 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 30:
                if Target780HexColorValue[
                    SeqLightNo(impactXnum, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum - 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum - 2, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 29:
                if Target780HexColorValue[
                    SeqLightNo(impactXnum, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum - 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum - 2, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum + 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum >= 3 and impactXnum <= 28:
                if Target780HexColorValue[
                    SeqLightNo(impactXnum, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum - 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum - 2, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum + 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum + 2, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')


        if impactYnum >= 2 and impactYnum <= 25:  # hit on row BETWEEN 2 and 25 (inclusive), check this row and row and +/1 ros for THIS row and +/- 2 colums
            # first check the row we are "on", impactYnum
            if impactXnum == 1:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 2, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 2:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 2, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 30:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 2, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 29:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 2, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum >= 3 and impactXnum <= 28:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 2, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 2, impactYnum)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            # then check the next row (row + 1 = 2) IF ROW ONE (impactYnum + 1) because Softballs get +/- one row, plus one row in this case.
            if impactXnum == 1:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 2, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 2:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 2, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 30:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 2, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 29:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 2, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum >= 3 and impactXnum <= 28:
                if Target780HexColorValue[SeqLightNo(impactXnum, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum - 2, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 1, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[SeqLightNo(impactXnum + 2, impactYnum + 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

         # then check the PREVIOUS row (row -1 = 29) IF ROW THIRTY (impactYnum - 1) because Softballs get +/- one row, plus one row in this case.
            if impactXnum == 1:
                if Target780HexColorValue[
                    SeqLightNo(impactXnum, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum + 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum + 2, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 2:
                if Target780HexColorValue[
                    SeqLightNo(impactXnum, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum + 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum + 2, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum - 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 30:
                if Target780HexColorValue[
                    SeqLightNo(impactXnum, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum - 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum - 2, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum == 29:
                if Target780HexColorValue[
                    SeqLightNo(impactXnum, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum - 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum - 2, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum + 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

            if impactXnum >= 3 and impactXnum <= 28:
                if Target780HexColorValue[
                    SeqLightNo(impactXnum, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum - 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum - 2, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum + 1, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')
                if Target780HexColorValue[
                    SeqLightNo(impactXnum + 2, impactYnum - 1)] == CurrTargetSuccessHexColorValue:
                    return ('SUCCESS')

    return ('MISS')


def SeqLightNo(Xin, Yin):

    for intIX in range(1, 781):  # loops 1 to 780
        if LedArray1260ColNum[intIX] == Xin:
            if LedArray1260RowNum[intIX] == Yin:
                return LedArray1260SeqNo[intIX]


def TestRunSuccessMissLogic():

    WriteLogFile('Run routine to exercise the success/miss logic based on target color and array in memory of current target', '0020-RunTestSuccessMissLogic       -')

#    CurrTargetSuccessHexColorValue = '00f000'  # SM_Green  -SET IN GLOBAL AREA   8/8/18 htc - for NOW, only SUCCESS COLOR is GREEN '00f000'

# list of current valid targes 8/8/18 htc.
    #  'SMV1-PRACTICE':    0
    # 'SMV1-EARLYDEV':   1
    # 'SMV1-ED-R':     2
    # 'SMV1-INTERMED':   3
    # 'SMV1-IM-R':     4
    # 'SMV1-SELECT':   5
    # 'SMV1-SL-R':   6
    #  'SMV1-PITCHADV':   7
    # 'SMV1-PA-R':       8
    # 'SMV1-PRACT-R':    9

    TargetNames = ['SMV1-PRACTICE', 'SMV1-EARLYDEV', 'SMV1-ED-R', 'SMV1-INTERMED', 'SMV1-IM-R', 'SMV1-SELECT', 'SMV1-SL-R', 'SMV1-PITCHADV', 'SMV1-PA-R', 'SMV1-PRACT-R']

# set target type to test on (only loads in to 1260 array, then copies to 780 array that we compare against.
    for TargetIndex in range(1,10):   # loops 1 to 10

        BuildSelectedBaseTargetArrayForThisRun(TargetNames[TargetIndex])
    #    BuildSelectedBaseTargetArrayForThisRun('SMV1-INTERMED')

        MarqueeWord('SYS-MAIN', '')

        # these next three lines are necessary ONLY to display it to the LED for reference
        Write1260ArrayToArtnetFile()
        ArtdmxToNDB()
        time.sleep(0.01)

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'BASE'
        lclXnum = 1
        lclYnum = 1
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
#        print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'BASE'
        lclXnum = 30
        lclYnum = 26
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
#        print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'BASE'
        lclXnum = 6
        lclYnum = 6
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
#        print(lclPrintString)
        WriteLogFile(lclPrintString, 'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'BASE'
        lclXnum = 7
        lclYnum = 7
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
#        print(lclPrintString)
        WriteLogFile(lclPrintString, 'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'BASE'
        lclXnum = 8
        lclYnum = 8
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
#        print(lclPrintString)
        WriteLogFile(lclPrintString, 'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'BASE'
        lclXnum = 9
        lclYnum = 9
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
#        print(lclPrintString)
        WriteLogFile(lclPrintString, 'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'BASE'
        lclXnum = 10
        lclYnum = 10
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
#        print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'BASE'
        lclXnum = 15
        lclYnum = 15
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
#        print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'BASE'
        lclXnum = 17
        lclYnum = 17
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
#        print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'BASE'
        lclXnum = 18
        lclYnum = 18
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'BASE'
        lclXnum = 19
        lclYnum = 19
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'BASE'
        lclXnum = 20
        lclYnum = 20
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'BASE'
        lclXnum = 25
        lclYnum = 25
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'SOFT'
        lclXnum = 1
        lclYnum = 1
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'SOFT'
        lclXnum = 30
        lclYnum = 26
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'SOFT'
        lclXnum = 6
        lclYnum = 6
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString, 'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'SOFT'
        lclXnum = 7
        lclYnum = 7
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString, 'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'SOFT'
        lclXnum = 8
        lclYnum = 8
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString, 'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'SOFT'
        lclXnum = 9
        lclYnum = 9
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString, 'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'SOFT'
        lclXnum = 10
        lclYnum = 10
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'SOFT'
        lclXnum = 15
        lclYnum = 15
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'SOFT'
        lclXnum = 17
        lclYnum = 17
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'SOFT'
        lclXnum = 18
        lclYnum = 18
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'SOFT'
        lclXnum = 19
        lclYnum = 19
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'SOFT'
        lclXnum = 20
        lclYnum = 20
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')

        # repeat these 6 lines for every test "pitch" to be evaluated against target above
        lclBallType = 'SOFT'
        lclXnum = 25
        lclYnum = 25
        lclPrintString = CurrentTargetName + ' - ' + CurrTargetSuccessHexColorValue + ' - ' + lclBallType + ' : ' + str(lclXnum) + ', ' + str(lclYnum) + '  Result: ' + str(EvalSuccessMiss(lclBallType, lclXnum, lclYnum))
 #       print(lclPrintString)
        WriteLogFile(lclPrintString,'CALL FUNCTION TESTING')


def WriteOnePitchToLocalPitchTable():

    global ThisSess_MachineId
    global ThisSess_AccountId
    global ThisSess_SeqNumber
    global ThisSess_InitialStatus
    global ThisSess_CurrentStatus
    global ThisSess_Type
    global ThisSess_StandTargetGuid
    global ThisSess_PracticeGuid
    global ThisSess_GameLineUpGuid
    global ThisSess_ArcadeGuid
    global ThisSess_BallType
    global ThisSess_DisplaySpeedSecs
    global ThisSess_DisplayImpactSecs
    global ThisSess_SuspendTimeOutSeconds_ReallyMINUTES
    global ThisSess_DisplayRiverYN
    global ThisSess_DisplayPitchCountBarsYN
    global ThisSess_YdeltaPlusMinus3
    global ThisSess_PitchingDistanceFeet
    global ThisSess_SystemOnLineYN
    global ThisSess_ShutdownMode
    global ThisSess_StudentDisplayName

    global CurrPitch_PlateSpeedMPH
    global CurrPitch_ReleaseSpeedMPH
    global CurrPitch_PitchNumber
    global CurrPitch_ImpactXstr
    global CurrPitch_ImpactXint
    global CurrPitch_ImpactYint
    global CurrPitch_SpinRPM
    global CurrPitch_SpinAxis
    global CurrPitch_Call
    global CurrPitch_DateTime
    global CurrPitch_TargetGUID
    global CurrPitch_MovementInfo
    global CurrPitch_ExpectedPitch
    global CurrPitch__ExpectedSpeedRange
    global CurrPitch_MarqueeContent
    global CurrPitch_PracticeModeHitZones
    global CurrPitch_FullPath1
    global CurrPitch_FullPath2
    global CurrPitch_FullPath3
    global CurrPitch_FullPath4
    global CurrPitch_FullPath5
    global CurrPitch_FullPath6
#11/30/18 htc
    global CurrPitch_ImpactXstrZ1
    global CurrPitch_ImpactXintZ1
    global CurrPitch_ImpactYintZ1


#    ThisSess_MachineId = str(ThisSess_MachineId)
    if str(ThisSess_Type).upper() == 'STANDARD':
        TargetGuidForThisSession = ThisSess_StandTargetGuid
        TargetNameForThisSession = 'STANDARD'
    if str(ThisSess_Type).upper() == 'PRACTICE':
        TargetGuidForThisSession = ThisSess_PracticeGuid
        TargetNameForThisSession = 'PRACTICE'

    global gbolHomeRunThisPitch
    gbolHomeRunThisPitch = False


    smartmitt_conn = mariadb.connect(user='smartmitt', password='smartmitt', database='smartmitt', host='localhost')
    cursor_local_pitches = smartmitt_conn.cursor()

 #   SQLstring = 'INSERT INTO LocalPitchTable (CreateDtm) values ("' + str(datetime.datetime.now()).format("%Y-%m-%d %H:%M:%S") + '")'


#9/30/18 htc - fix these being "unassigned" just short term fix !!
# 10/11/18 htc    TargetGuidForThisSession = ''
# 10/11/18 htc    TargetNameForThisSession = ''


# 11/30/18 htc added ThisSess_ReleaseSpeedAddon and speed acquisition method notes to pitch record.
    if int(ThisSess_ReleaseSpeedAddon) > 0:
        CurrPitch_ReleaseSpeedMPH = CurrPitch_PlateSpeedMPH + int(ThisSess_ReleaseSpeedAddon)
    else:
        CurrPitch_ReleaseSpeedMPH = 0

    strPitchPlateSpeedMethod = 'measured by dt100 radar behind plate'
    strPitchReleaseSpeedMethod = 'measured plate speed plus addon MANUALLY entered on User Record of ' + str(ThisSess_ReleaseSpeedAddon)


    SQLstring = 'INSERT INTO LocalPitchTable ('
    VALstring = ') Values ('

    SQLstring = SQLstring + 'MachineID, PitcherAccountID, SessionNumber, PitchNumber, '
    SQLstring = SQLstring + 'PlateSpeedMph, ReleaseSpeedMph, ImpactXint, ImpactXstr, '
    SQLstring = SQLstring + 'ImpactYint, PitchCall, PitchingDistance, BallType, '
    SQLstring = SQLstring + 'CreateDtm, SessionType, TargetGUID, TargetName, '
    SQLstring = SQLstring + 'YDeltaAdjustPlusMinusThreeValue, StandardModeInfo, PracticeModeInfo, GameLineupModeInfo, '
    SQLstring = SQLstring + 'ArcadeModeInfo, SpinRPM, SpinAxis, MarqueeContentBeforePitch, '
    SQLstring = SQLstring + 'ExpectedPitch, ExpectedSpeedRange, MovementInfo, UploadToCloudDtm, '
    SQLstring = SQLstring + 'PracticeModeHitZonesInfo, CriticalFramePhotoRightCamTag, CriticalFramePhotoLeftCamTag, SpinCameraVideoTag, '
    SQLstring = SQLstring + 'UserDisplayImage1FullLocalPath, UserDisplayImage2FullLocalPath, UserDisplayImage3FullLocalPath, '
    SQLstring = SQLstring + 'UserDisplayImage4FullLocalPath, UserDisplayImage5FullLocalPath, UserDisplayImage6FullLocalPath, '
    SQLstring = SQLstring + 'ImpactFileLedViewTag, LineImageRightTag, LineImageLeftTag, TargetFileLedViewTag, AudioFileToPlayOnceFullLocalPath, '

#11/30/18 htc added following fields to local SQL pitch table update
    SQLstring = SQLstring + 'PlateSpeedMethod, ReleaseSpeedMethod, ImpactXintZ1, ImpactXstrZ1, ImpactYintZ1'



#12/02/18 htc Hard coded the audio file in here for now (Tom wanted it in 'next version' demo for Softball show.)
#01/01/19 htc - added variables (hard coded for now) to the play sound logic.
#gstrSoundTopLeftX = 'L'
#gintSoundTopLeftY = 11
#gstrSoundBottomRightX = 'N'
#gintSoundBottomRightY = 15
    gbolHomeRunThisPitch = False
    M14toN15_FileToPlay = ''
    if CurrPitch_Call != 'SUCCESS':
        if TargetGuidForThisSession != 'SMV1-EARLYDEV' and gintSoundTopLeftY != 0 and gintSoundBottomRightY !=0:
            if CurrPitch_ImpactXstr >= gstrSoundTopLeftX and CurrPitch_ImpactYint >= gintSoundTopLeftY:
                if CurrPitch_ImpactXstr <= gstrSoundBottomRightX and CurrPitch_ImpactYint <= gintSoundBottomRightY:
                    M14toN15_FileToPlay = 'GoCrazyFolksOzzieShort.wav'
                    gbolHomeRunThisPitch = True

                    MarqueeWord('HOME RUN', SM_Red)
                    Write1260ArrayToArtnetFile()
                    ArtdmxToNDB()

                    time.sleep(0.81)

                    print('HOME RUN - HOME RUN - HOME RUN')
                    WriteLogFile('HOME RUN - HOME RUN - HOME RUN', 'Added debug line 1/3/19 htc     ')
                    time.sleep(5.9)

    #    M14toN15_FileToPlay = '/var/www/html/students/GoCrazyFolksOzzieShort.wav'
#    M14toN15_FileToPlay = 'GoCrazyFolksOzzieShort.wav'




    VALstring = VALstring + '"' + ThisSess_MachineId + '", "' + ThisSess_AccountId + '", "' + str(ThisSess_SeqNumber) + '", "' + str(CurrPitch_PitchNumber) + '", '
    VALstring = VALstring + '"' + str(CurrPitch_PlateSpeedMPH) + '", "' + str(CurrPitch_ReleaseSpeedMPH) + '", "' + str(CurrPitch_ImpactXint) + '", "' + CurrPitch_ImpactXstr + '", '
    VALstring = VALstring + '"' + str(CurrPitch_ImpactYint) + '", "' + CurrPitch_Call + '", "' + str(ThisSess_PitchingDistanceFeet) + '", "' + ThisSess_BallType + '", '
    VALstring = VALstring + '"' + str(datetime.datetime.now()).format("%Y-%m-%d %H:%M:%S") + '", "' + ThisSess_Type + '", "' + TargetGuidForThisSession + '", "' + TargetNameForThisSession + '", '
    VALstring = VALstring + '"' + str(ThisSess_YdeltaPlusMinus3) + '", "' + '-*-' + '", "' + '-*-' + '", "' + '-*-' + '", '
    VALstring = VALstring + '"' + '-*-' + '", "' + str(CurrPitch_SpinRPM) + '", "' + str(CurrPitch_SpinAxis) + '", "' + CurrPitch_MarqueeContent + '", '
    VALstring = VALstring + '"' + CurrPitch_ExpectedPitch + '", "' + '-*-' + '", "' + CurrPitch_MovementInfo + '", "' + '01/01/1900' + '", '
    VALstring = VALstring + '"' + '-*-' + '", "' + 'right cam tag' + '", "' + 'left cam tag' + '", "' + 'spin cam tag' + '", '
    VALstring = VALstring + '"'  + str(CurrPitch_FullPath1) + '", "' + str(CurrPitch_FullPath2) + '", "' +str(CurrPitch_FullPath3) + '", '
    VALstring = VALstring + '"'  + str(CurrPitch_FullPath4) + '", "' + str(CurrPitch_FullPath5) + '", "' +str(CurrPitch_FullPath6) + '", '
    VALstring = VALstring + '"' + 'impact' + '", "' + 'img right' + '", "' + 'img left' + '", "' + 'target' + '", "' + M14toN15_FileToPlay + '", '

#11/30/18 htc added following fields to local SQL pitch table update
    VALstring = VALstring + '"' + str(strPitchPlateSpeedMethod) + '", "' + str(strPitchReleaseSpeedMethod) + '", "' + str(CurrPitch_ImpactXintZ1) + \
                '", "' + str(CurrPitch_ImpactXstrZ1) + '", "' + str(CurrPitch_ImpactYintZ1) + '")'

    SQLstring = SQLstring + VALstring
    cursor_local_pitches.execute(SQLstring)
    smartmitt_conn.commit()
    smartmitt_conn.close()
    gc.collect()

    WriteLogFile('Valstring: ' + VALstring, '3460-WriteOnePitchToLocalPitchTable -')
    WriteLogFile('CurrPitch_MovementInfo for Pitch [' + str(CurrPitch_PitchNumber) + '] ' + CurrPitch_MovementInfo, '3460-WriteOnePitchToLocalPitchTable -')


def DisplayImpactLocation(impactXnum, impactYnum):

    WriteLogFile('Display Impact location: [' + str(impactXnum) + ', ' + str(impactYnum) + ']', '0071-DisplayImpactLocation              -')

    strImpactInfo = 'Display Impact Loc DATA IN: (impactXnum: '  + str(impactXnum) + ', ' + str(impactYnum)
    print(strImpactInfo)

#    CurrTargetSuccessHexColorValue = '00f000'  # SM_Green  -SET IN GLOBAL AREA   8/8/18 htc - for NOW, only SUCCESS COLOR is GREEN '00f000'
#     Target780HexColorValue = LedArray1260HexColorValue.copy()      this is why this routine works, base target was copied to 780 array when it was initially built.

#8/8/18 htc - the reason X (Right/Left) and Y (Up/Down) Variance is different is because X light spacing is 1.3" (30/meter) and Y is 2.6"

#    if intSpeed > 99:
#       PaintThisBox(SM_Red_Med, 1, 4, 2, 19)

# 9/9/18 htc - IMPACT box is 4 squares, main IMPACT square is always top, left most LED, light one right, one down, and one down and right to make 4.
#              BLACK OUT box is SIXTEEN SQUARES AROUND the 4 square impact box.  CODE BELOW is to keep boxes from being "painted" off the LED grid.
# black out
# 9/9/18 htc -
# hit main part of LED, not adjustment needed for blackout/impact areas
#    if impactXnum > 1 and impactXnum < 25 and impactYnum > 1 and impactYnum < 25:
# Adjust X,Y values for impacts in the corners where there isn't room to blackout and paint hit 4x4.
#    if impactXnum == 1:
#        impactXnum = 2
#    if impactXnum > 24:
#        impactXnum = 24
#    if impactYnum == 1:
#        impactYnum = 2
#    if impactYnum > 24:
#        impactYnum = 24
    # ****************************************************************************************************************
    # ****************************************************************************************************************
    # ****************************************************************************************************************
    # ****************************************************************************************************************

    # 9/15/18 - HTC - Figured out had to ADD TWO (2) to the X (horizontal) integer value to DISPLAY IMPACT LOCATION (same as eval code)
    #                The rows (Y value) also need to be adjusted right at top or bottom, 1,25, or 26.
    #                ROW TWO (2) IS OK !! Paint down and right from impact point!
    #                A or column 1 is actually physically colum 3 in the led grid,
    #                The Target780NexColorValue array has 30 lights per row to match the physical LED strips (30/meter).
    #                All the ball impact location logic runs on 26 columns and 26 rows., physical col 3 through 28 !!!
    #                Columns 1/2, and 29/30 are reserved for pitch count "bars"- red/green

    impactXnum = impactXnum + 2

    if impactYnum > 24:
        impactYnum = 24

    if impactYnum == 1:
        impactYnum = 2

    # ****************************************************************************************************************
    # ****************************************************************************************************************
    # ****************************************************************************************************************
    # ****************************************************************************************************************

    PaintThisBox(SM_Black, impactXnum -1, impactYnum -1, impactXnum +2, impactYnum +2)

    PaintThisBox(SM_White_Hi, impactXnum, impactYnum, impactXnum +1, impactYnum +1)

    strImpactInfo = 'Impact Loc: (SM_White_Hi, '  + str(impactXnum) + ', ' + str(impactYnum) + ' / ' + str(impactXnum +1) + ', ' + str(impactYnum +1) + ')'
    print(strImpactInfo)

    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()

#9/24/18 htc - make two copies of Impact.jpg - one for PHP to display in "students" folder, One for archive with pit
# ORIGINAL - "HOME" FOLDER.    ArtnetTxtToJpg('NdbArtNetCtrlString.txt', 'Impact.jpg', width=300)

#    WriteLogFile('Attempting to create this file from (NdbArtNetCtrlString.txt) in home folder: [' + NetworkSharePath + '/Impact.jpg' ']', '0071-DisplayImpactLocation              -')

    ArtnetTxtToJpg('NdbArtNetCtrlString.txt', NetworkSharePath + '/Impact.jpg', width=300)


def WaitForSpeedFile(TimeOutValueToAbort):

    global ThisSess_ShutdownMode

    StartTime = datetime.datetime.now()
    ExpireTime = StartTime + datetime.timedelta(seconds=TimeOutValueToAbort)
    CurrentTime = datetime.datetime.now()
    while (ExpireTime > CurrentTime ):

        if os.path.isfile(StopFilePath1):
            WriteLogFile('stop.txt #1 file found, ending SmMain.py: [' + str(StopFilePath1) + ']','2033-WaitForSpeedFile          -')
            StopFile = open(StopFilePath1, 'r')
            ThisSess_ShutdownMode = StopFile.read()
            if os.path.isfile(StopFilePath1):
                os.system('sudo chmod 777 ' + StopFilePath1)
                os.system('sudo rm ' + StopFilePath1)
#10/26/18 htc - ONLY delete ONE stop file, that way if some how TWO SmMain.py's are running, one will get file1, the other will get file2 ???  I hope !
#            if os.path.isfile(StopFilePath2):
#                os.system('sudo chmod 777 ' + StopFilePath2)
#                os.system('sudo rm ' + StopFilePath2)
            return(3)   #STOP.TXT file found, end program accordingly.
        if os.path.isfile(StopFilePath2):
            WriteLogFile('stop.txt #2 file found, ending SmMain.py: [' + str(StopFilePath2) + ']','2033-WaitForSpeedFile          -')
            StopFile = open(StopFilePath2, 'r')
            ThisSess_ShutdownMode = StopFile.read()
# 10/26/18 htc - ONLY delete ONE stop file, that way if some how TWO SmMain.py's are running, one will get file1, the other will get file2 ???  I hope !
#           if os.path.isfile(StopFilePath1):
#               os.system('sudo chmod 777 ' + StopFilePath1)
#               os.system('sudo rm ' + StopFilePath1)
            if os.path.isfile(StopFilePath2):
                os.system('sudo chmod 777 ' + StopFilePath2)
                os.system('sudo rm ' + StopFilePath2)
            return (3)  # STOP.TXT file found, end program accordingly.
        if os.path.isfile(SpeedFilePath):
            SpeedFile = open(SpeedFilePath, 'r')
            SpeedString = SpeedFile.read()
            os.remove(SpeedFilePath)

       #10/23/18 htc- added debug statements because changed way I parse out actual speed.
            WriteLogFile('Parse this speed.txt file string: [' + SpeedString + ']', '0274-WaitForSpeedFile(TimeOutValueToAbort)   -')

            #            Speed = int(SpeedString[1:5])          10/23/18 htc - OLD WAY

            Speed = ''
            if str(SpeedString[0]) >= '0' and str(SpeedString[0]) <= '9':
                Speed = Speed + str(SpeedString[0])
            if str(SpeedString[1]) >= '0' and str(SpeedString[1]) <= '9':
                Speed = Speed + str(SpeedString[1])
            if str(SpeedString[2]) >= '0' and str(SpeedString[2]) <= '9':
                Speed = Speed + str(SpeedString[2])
            if str(SpeedString[3]) >= '0' and str(SpeedString[3]) <= '9':
                Speed = Speed + str(SpeedString[3])
            if str(SpeedString[4]) >= '0' and str(SpeedString[4]) <= '9':
                Speed = Speed + str(SpeedString[4])
            if str(SpeedString[5]) >= '0' and str(SpeedString[5]) <= '9':
                Speed = Speed + str(SpeedString[5])
#            if str(SpeedString[6]) >= '0' and str(SpeedString[6]) <= '9':
#                Speed = Speed + str(SpeedString[6])
#            if str(SpeedString[7]) >= '0' and str(SpeedString[7]) <= '9':
                Speed = Speed + str(SpeedString[7])
            intSpeed = int(Speed)

            WriteLogFile('Got this speed (integer): [' + str(intSpeed) + ']', '0274-WaitForSpeedFile(TimeOutValueToAbort)   -')

            return(intSpeed)

        time.sleep(1.1)
        CurrentTime = datetime.datetime.now()

    return(2)   # Time-out occured waiting for files


def strX2int(strXin):
    if len(strXin) < 1:
        return(0)

    charX =  str(strXin[0]).upper()
    if charX < 'A' or charX > 'Z':
        return(0)

    if charX == 'A': return(1)
    if charX == 'B': return(2)
    if charX == 'C': return(3)
    if charX == 'D': return(4)
    if charX == 'E': return(5)
    if charX == 'F': return(6)
    if charX == 'G': return(7)
    if charX == 'H': return(8)
    if charX == 'I': return(9)
    if charX == 'J': return(10)
    if charX == 'K': return(11)
    if charX == 'L': return(12)
    if charX == 'M': return(13)
    if charX == 'N': return(14)
    if charX == 'O': return(15)
    if charX == 'P': return(16)
    if charX == 'Q': return(17)
    if charX == 'R': return(18)
    if charX == 'S': return(19)
    if charX == 'T': return(20)
    if charX == 'U': return(21)
    if charX == 'V': return(22)
    if charX == 'W': return(23)   #FUCK ME RUNNING - 10/23/18 htc This "W" was set to "Y" - caused 'int' error (value was 'none').
    if charX == 'X': return(24)
    if charX == 'Y': return(25)
    if charX == 'Z': return(26)


def intX2str(intXin):
    if int(intXin) == 0: return(0)
    if int(intXin) < 0 or int(intXin) > 26: return(0)
    if int(intXin) == 1: return('A')
    if int(intXin) == 2: return('B')
    if int(intXin) == 3: return('C')
    if int(intXin) == 4: return('D')
    if int(intXin) == 5: return('E')
    if int(intXin) == 6: return('F')
    if int(intXin) == 7: return('G')
    if int(intXin) == 8: return('H')
    if int(intXin) == 9: return('I')
    if int(intXin) == 10: return('J')
    if int(intXin) == 11: return('K')
    if int(intXin) == 12: return('L')
    if int(intXin) == 13: return('M')
    if int(intXin) == 14: return('N')
    if int(intXin) == 15: return('O')
    if int(intXin) == 16: return('P')
    if int(intXin) == 17: return('Q')
    if int(intXin) == 18: return('R')
    if int(intXin) == 19: return('S')
    if int(intXin) == 20: return('T')
    if int(intXin) == 21: return('U')
    if int(intXin) == 22: return('V')
    if int(intXin) == 23: return('W')
    if int(intXin) == 24: return('X')
    if int(intXin) == 25: return('Y')
    if int(intXin) == 26: return('Z')


def ProcessOneBallCentersString(strInput):
 #10/26/18 htc - was old ReplaceCRLF, enhanced it to process/format ball centers string from ozan's output files.  They have CR/LF in them.
    if strInput != None and str(strInput) != 'None' and str(strInput) > '':
        if len(str(strInput)) < 1:
            return(strInput)
        else:
            strWork = strInput.replace('\n',' / ')
            strWork = strWork[:-3]
            return(strWork.replace(',',', '))
    else:
        return(strInput)


def PickOffPair(strInput, intThisPairNo):

#1/21/19 htc - attempted to make this routine handle up to EIGHT pairs, slower, curve balls trying to get "movement" (still stupid on these cameras/angles).
#                           caused ball to move so slow, started giving us more that 2 or 3 or 4 pairs !!!!!!!!!!!!


    if intThisPairNo < 1 or intThisPairNo > 8:
        return('error 323')

    intStrLen = len(strInput)
    intBeginOfPair = 1
    intEndOfPair = intStrLen

    intFoundCount = 0
    intCharPosition = 0
    intStartPair1 = 0
    intEndPair1 = intStrLen
    intEndPair2 = intStrLen
    intEndPair3 = intStrLen
    intEndPair4 = intStrLen
    intEndPair5 = intStrLen
    intEndPair6 = intStrLen
    intEndPair7 = intStrLen
    intEndPair8 = intStrLen
    intCharPosition = 1
    for char in strInput:
        if char == '/':
            intFoundCount = intFoundCount + 1
            if intFoundCount == 1:
                intStartPair2 = intCharPosition
                intEndPair1 = intCharPosition - 1
            if intFoundCount == 2:
                intStartPair3 = intCharPosition
                intEndPair2 = intCharPosition - 1
            if intFoundCount == 3:
                intStartPair4 = intCharPosition
                intEndPair3 = intCharPosition - 1
            if intFoundCount == 4:
                intStartPair5 = intCharPosition
                intEndPair4 = intCharPosition - 1
            if intFoundCount == 5:
                intStartPair6 = intCharPosition
                intEndPair5 = intCharPosition - 1
            if intFoundCount == 6:
                intStartPair7 = intCharPosition
                intEndPair6 = intCharPosition - 1
            if intFoundCount == 7:
                intStartPair8 = intCharPosition
                intEndPair7 = intCharPosition - 1
            if intFoundCount == 8:
                intEndPair8 = intCharPosition - 1

        intCharPosition = intCharPosition + 1

    if intFoundCount == 0:
        return('error 324')

    if intThisPairNo == 1:
    #        if intEndPair2 > 0:
        return (str(strInput[intStartPair1:intEndPair1]).strip())
    #        else:
    #            return(str(strInput[intStartPair2:intStrLen]).strip)

    if intThisPairNo == 2:
#        if intEndPair2 > 0:
            return(str(strInput[intStartPair2:intEndPair2]).strip())
#        else:
#            return(str(strInput[intStartPair2:intStrLen]).strip)

    if intThisPairNo == 3:
#        if intEndPair3 > 0:
            return(str(strInput[intStartPair3:intEndPair3]).strip())
#        else:
#            return(str(strInput[intStartPair3:intStrLen]).strip)

    if intThisPairNo == 4:
#        if intEndPair4 > 0:
            return(str(strInput[intStartPair4:intEndPair4]).strip())



    if intThisPairNo == 5:
#        if intEndPair4 > 0:
            return(str(strInput[intStartPair5:intEndPair5]).strip())

    if intThisPairNo == 6:
#        if intEndPair4 > 0:
            return(str(strInput[intStartPair6:intEndPair6]).strip())

    if intThisPairNo == 7:
#        if intEndPair4 > 0:
            return(str(strInput[intStartPair7:intEndPair7]).strip())

    if intThisPairNo == 8:
#        if intEndPair4 > 0:
            return(str(strInput[intStartPair8:intEndPair8]).strip())




def CalculateMovementVer1():
    # 11/30/18 htc created this routine.


# 12/01/18 htc added flag below to "pair" up "pair's".


    bolSameCoordPairSeqNum = True   #12/03/18 htc - per Tom's request use this logic.
    # if 2 pair, use pair 2 from each, if 3 pair, use 3, if 2 on one and 3 on other- only use TWO on each, ignore 3rd.


    bolLastCoordPairValues = False
    # always use the LAST pair value no matter if same number of pairs per camera or not, farthest out "frame".


    # strXcoord = XevalNetLocPctCoordsV1(intPctOfXcol)
    # intYcoord = YevalNetLocPctCoordsV1(intPctOfYrow)

    # CurrPitch_ImpactXstr = intX2str(intXcoord)
    # CurrPitch_ImpactXint = intXcoord
    # CurrPitch_ImpactYint = intYcoord

    global CurrPitch_ImpactXstrZ1
    global CurrPitch_ImpactXintZ1
    global CurrPitch_ImpactYintZ1
    global BallCentersString1
    global BallCentersString2
    global CurrPitch_MovementInfo

    CurrPitch_ImpactXstrZ1 = ''
    CurrPitch_ImpactXintZ1 = 0
    CurrPitch_ImpactYintZ1 = 0

    Dummy1 = BallCentersString1
    Dummy2 = BallCentersString2
    Dummy3 = len(BallCentersString1)
    Dummy4 = len(BallCentersString2)

    WriteLogFile('Inside MOVEMENT Sub-Routine. BallCentersString1 (ONE) = [' + str(BallCentersString1) +']', 'DEBUG LINE 01-05-19 htc             ')
    WriteLogFile('Inside MOVEMENT Sub-Routine. BallCentersString2 (TWO) = [' + str(BallCentersString2) +']', 'DEBUG LINE 01-05-19 htc             ')

    if len(BallCentersString1) < 3:
        return('error-13')
    if len(BallCentersString2) < 3:
        return('error-23')


    CamOneData = ProcessOneBallCentersString(BallCentersString1)
    CamTwoData = ProcessOneBallCentersString(BallCentersString2)

    intC1_CoordCountComma = CamOneData.count(',')   #this should tell you how many pairs there are
    intC2_CoordCountComma = CamTwoData.count(',')
    intC1_CoordCountSlash = CamOneData.count('/')   #this is number of pairs MINUS ONE (-1)
    intC2_CoordCountSlash = CamTwoData.count('/')


#1/21/19 HTC - added code to allow for up to EIGHT BALL CENTERS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   Happened at trade show !!!
    if intC1_CoordCountComma < 2 or intC1_CoordCountComma > 8:
        return('error-11')
    if intC2_CoordCountComma < 2 or intC2_CoordCountComma > 8:
        return('error-21')
    if intC1_CoordCountSlash < 1 or intC1_CoordCountComma > 8:
        return('error-12')
    if intC2_CoordCountSlash < 1 or intC2_CoordCountComma > 8:
        return('error-22')



    if bolLastCoordPairValues:
        Cam1PairToUse = PickOffPair(CamOneData, intC1_CoordCountComma)
        Cam2PairToUse = PickOffPair(CamTwoData, intC2_CoordCountComma)

    if bolSameCoordPairSeqNum:
        intHighestCommonPairNumber = 0
        if intC1_CoordCountComma > 1 and intC2_CoordCountComma > 1:
            intHighestCommonPairNumber = 2
        if intC1_CoordCountComma > 2 and intC2_CoordCountComma > 2:
            intHighestCommonPairNumber = 3
        if intC1_CoordCountComma > 3 and intC2_CoordCountComma > 3:
            intHighestCommonPairNumber = 4
        if intC1_CoordCountComma > 4 and intC2_CoordCountComma > 4:
            intHighestCommonPairNumber = 5
        if intC1_CoordCountComma > 5 and intC2_CoordCountComma > 5:
            intHighestCommonPairNumber = 6
        if intC1_CoordCountComma > 6 and intC2_CoordCountComma > 6:
            intHighestCommonPairNumber = 7
        if intC1_CoordCountComma > 7 and intC2_CoordCountComma > 7:
            intHighestCommonPairNumber = 8


        if intHighestCommonPairNumber > 0:
            Cam1PairToUse = PickOffPair(CamOneData, intHighestCommonPairNumber)
            Cam2PairToUse = PickOffPair(CamTwoData, intHighestCommonPairNumber)

    Cam1NetPair = PickOffPair(CamOneData, 1)
    Cam2NetPair = PickOffPair(CamTwoData, 1)

    intA = int(Cam1NetPair[:Cam1NetPair.find(',')])
    intB = int(Cam1NetPair[Cam1NetPair.find(',')+1:Cam1NetPair.find(',')+5])
    intC = int(Cam2NetPair[:Cam2NetPair.find(',')])
    intD = int(Cam2NetPair[Cam2NetPair.find(',')+1:Cam2NetPair.find(',')+5])

    intE = int(Cam1PairToUse[:Cam1PairToUse.find(',')])
    intF = int(Cam1PairToUse[Cam1PairToUse.find(',')+1:Cam1PairToUse.find(',')+5])
    intG = int(Cam2PairToUse[:Cam2PairToUse.find(',')])
    intH = int(Cam2PairToUse[Cam2PairToUse.find(',')+1:Cam2PairToUse.find(',')+5])

##    intI =int(0)

    intJ = intA - intE
    intK = intB - intF
    intL = intC - intG
    intM = intD - intH

##    intN =int(0)

    intO = (intJ + intL)/2
    intP = (intK + intM)/2

# Pctg of change DIVIDED BY 480
#    intQ = intO / 480
#    intR = intP / 480
# Pctg of change DIVIDEB BY 640   12/3/18 htc - TRF and HTC agreed, divide by 640 yeilds smaller numbers, less drastic FOR NOW!!!.
    intQ = intO / 640   #12/5/18 htc - ESTIMATED pct of change on X
    intR = intP / 640   # on Y


#    HTC = CurrPitch_ImpactXstr
#    HTC = CurrPitch_ImpactXint
#    HTC = CurrPitch_ImpactYint

    # 12/04/18 HTC - made these global variables in process pitch session, Ozan's ImpactLocator Output values (percentages of X/Y).
    HTC = intPctOfXcol
    HTC = intPctOfYrow
    htcNetXinches = int((intPctOfXcol/100) * 40)
    htcNetYinches = int((intPctOfYrow/100) * 70)


    intS = intQ * 40   # X changes in inches at Z-1
    intT = intR * 70   # Y changes in inches at Z-1

    if intS < 1 and intS > 0:
        intS = 1
    else:
        if intS < 0 and intS > -1:
            intS = -1
    intS = int(intS)

    if intT < 1 and intT > 0:
        intT = 1
    else:
        if intT < 0 and intT > -1:
            intT = -1
    intT = int(intT)

    minusValues = False
 #   plusValues = True

    if minusValues:
        intU = htcNetXinches - intS
        intV = htcNetYinches - intT

        if intU < 1:
            intU = 1
        if intV < 1:
            intV = 1
    else:
        intU = htcNetXinches + intS
        intV = htcNetYinches + intT

        if intU > 40:
            intU = 40
        if intV > 70:
            intV = 70







 # 1/3/19 htc First Try "order"   Z1Params = str(intU) + ',-12.5,' + str(intV)


#    Z1Params = str(intU) + ',-12.5,' + str(intV)

    Z1Params = str(intU) + ', 0,' + str(70 - intV)

    # 1/3/19 htc Second Try "order"   Z1Params = str(intV) + ',-12.5,' + str(intU)


 #   Z1Params = str(intV) + ',-12.5,' + str(intU)





    tempXval = int(intPctOfXcol + (intQ *100)) + 1
    if tempXval > 98:
        tempXval = 99
    if tempXval < 1:
        tempXval = 1
    CurrPitch_ImpactXstrZ1 = XevalNetLocPctCoordsV1(tempXval)

    tempYval = int(intPctOfYrow + (intR * 100))+1
    if tempYval > 98:
        tempYval = 99
    if tempYval < 1:
        tempYval = 1
    CurrPitch_ImpactYintZ1 = YevalNetLocPctCoordsV1(tempYval)

 #############################################################  12/5/18 htc smoothing SUCKS !!   intermedCoordsA = str(intU) + ',-12.4,' + str(intV)
 #############################################################################################   intermedCoordsB = str(htcNetXinches) + ',-0.1,' + str(htcNetYinches)






    NetParams = str(htcNetXinches) + ',-12.5,' + str(70 - htcNetYinches)


#    NetParams = str(htcNetYinches) + ',0,' + str(htcNetXinches)







    #12/05/18 htc - if "room" between coords/numbers, "spread" the 2 intemediate coord (A and B) as evenly as possible.
    if 'Smooth All Four Data Points' == 'dont run right now':
        if abs(htcNetXinches - intU) == 0:
            intDiffX1inches = 0
            intDiffX2inches = 0

        if abs(htcNetXinches - intU) == 1:
            intDiffX1inches = .3
            intDiffX2inches = .6

        if abs(htcNetXinches - intU) == 2:
            intDiffX1inches = .5
            intDiffX2inches = 1

        if abs(htcNetXinches - intU) == 3:
            intDiffX1inches = 1
            intDiffX2inches = 2

        if abs(htcNetXinches - intU) > 3:
            intDiffX1inches = int((htcNetXinches - intU) / 3)
            intDiffX2inches = int(intDiffX1inches * 2)
            if intDiffX2inches > 3:
                intDiffX2inches = 3


        if abs(htcNetYinches - intV) == 0:
            intDiffY1inches = 0
            intDiffY2inches = 0

        if abs(htcNetYinches - intV) == 1:
            intDiffY1inches = .3
            intDiffY2inches = .6

        if abs(htcNetYinches - intV) == 2:
            intDiffY1inches = .5
            intDiffY2inches = 1

        if abs(htcNetYinches - intV) == 3:
            intDiffY1inches = 1
            intDiffY2inches = 2

        if abs(htcNetYinches - intV) > 3:
            intDiffY1inches = int((htcNetYinches - intV) / 3)
            intDiffY2inches = int(intDiffY1inches * 2)
            if intDiffY2inches > 3:
                intDiffY2inches = 3

        if htcNetXinches - intU > 0:  # X axis numberg getting BIGGER , so add A and B "steps" to htcNet values.
            intermedCoordsA = str(htcNetXinches - intDiffX1inches)
            intermedCoordsB = str(htcNetXinches - intDiffX2inches)

 #           intermedCoordsA = intermedCoordsA  + ',-4,'
 #           intermedCoordsB = intermedCoordsB  + ',-8,'

        else:
            intermedCoordsA = str(htcNetXinches + intDiffX1inches)
            intermedCoordsB = str(htcNetXinches + intDiffX2inches)

        intermedCoordsA = intermedCoordsA + ',-4,'
        intermedCoordsB = intermedCoordsB + ',-8,'

        if htcNetYinches - intV > 0:  # Y axis numberg getting BIGGER , so add A and B "steps" to htcNet values.
            intermedCoordsA = intermedCoordsA + str(htcNetYinches + intDiffY1inches)
            intermedCoordsB = intermedCoordsB + str(htcNetYinches + intDiffY2inches)
        else:
            intermedCoordsA = intermedCoordsA + str(htcNetYinches - intDiffY1inches)
            intermedCoordsB = intermedCoordsB + str(htcNetYinches - intDiffY2inches)


    #12/03/18 htc - setup call to Wiggy's graphing program.
    # 12/04/18 htc - command line needs to look like this:   python plotsingle.py -o "/home/pi/front.png" -p "10,-5,46|21,0,23" -a "Front" -c "r" -t "Front Title \n Second line"

    CmdToCall = 'python /var/www/html/students/plotsingle.py '

#    Z1Params = '10,-5,46'  values hard coded for initial testing
#    NetParams = '21,0,23'

#    WriteLogFile('START TIME- call THREE MOVEMENT .png creations: [' + str(CmdToCall) + ']','4040-CalculateMovementVer1          -')
    WriteLogFile('START TIME- call THREE MOVEMENT .png creations WITH FOUR POINT SMOOTHING: [' + str(CmdToCall) + ']','5050-CalculateMovementVer1          -')

    if os.path.isfile('/home/pi/front.png'):     #      os.system('sudo chmod 777 ' + '/home/pi/front.png')
       CmdCallResult = os.system('sudo rm /home/pi/front.png')

    cmdParameters1 = '-o "/home/pi/front.png" -p "'
    strAngle = '" -a "Front" '
    strColor = '-c "r" '
    strTitleMultiLine = '-t "Front View- Sess: ' + str(ThisSess_SeqNumber) + '  Name: ' + ThisSess_StudentDisplayName + '\n'

#1/21/19 htc - if CurrPitch_ReleaseSpeedMPH is zero, don't even show it!
    if CurrPitch_ReleaseSpeedMPH > 0:
       strTitleMultiLine = strTitleMultiLine + 'Pitch#: ' + str(CurrPitch_PitchNumber) + '  Plate MPH: ' + str(CurrPitch_PlateSpeedMPH)  + '  Release MPH: ' + str(CurrPitch_ReleaseSpeedMPH) + '\n'
    else:
       strTitleMultiLine = strTitleMultiLine + 'Pitch#: ' + str(CurrPitch_PitchNumber) + '  Plate MPH: ' + str(CurrPitch_PlateSpeedMPH)   + '\n'


    strTitleMultiLine = strTitleMultiLine + 'Pitch Call: ' + CurrPitch_Call + '  Impact Coords: ' + CurrPitch_ImpactXstr + ', ' + str(CurrPitch_ImpactYint) +'"'

#12/5/18 htc    CommandToCall = CmdToCall + cmdParameters1 + Z1Params + '|' + intermedCoordsB + '|' + intermedCoordsA + '|' +NetParams + strAngle + strColor + strTitleMultiLine



    # 1/21/19 htc - copied following line to make it "reversable" on parameters for testing/getting graphs right.
    CommandToCall = CmdToCall + cmdParameters1 + Z1Params + '|' + NetParams + strAngle + strColor + strTitleMultiLine
    # CommandToCall = CmdToCall + cmdParameters1 + NetParams + '|' + Z1Params + strAngle + strColor + strTitleMultiLine



    return_code = subprocess.call(CommandToCall, shell=True)


#1/3/19 htc added debug lines (TRF at ABCA in Dallas today, tomorrow (Fri) and Saturday.
    WriteLogFile('First Graph Call COMMAND STRING: ' + str(CommandToCall) + ']','5050-CalculateMovementVer1          -')
    WriteLogFile('First Graph Call RESULT: ' + str(return_code) + ']','5050-CalculateMovementVer1          -')
    print('First Graph Call COMMAND STRING: [' + str(CommandToCall) + ']')
    print('First Graph Call RESULT: [' + str(return_code) + ']')



    if os.path.isfile('/home/pi/side.png'):  # os.system('sudo chmod 777 ' + '/home/pi/front.png')
        CmdCallResult = os.system('sudo rm /home/pi/side.png')

    cmdParameters1 = '-o "/home/pi/side.png" -p "'
    strAngle = '" -a "Side" '
    strColor = '-c "g" '
    strTitleMultiLine = '-t "Side View- Sess: ' + str(ThisSess_SeqNumber) + '  Name: ' + ThisSess_StudentDisplayName + '\n'



    # 1/21/19 htc - if CurrPitch_ReleaseSpeedMPH is zero, don't even show it!
    if CurrPitch_ReleaseSpeedMPH > 0:
        strTitleMultiLine = strTitleMultiLine + 'Pitch#: ' + str(CurrPitch_PitchNumber) + '  Plate MPH: ' + str(
            CurrPitch_PlateSpeedMPH) + '  Release MPH: ' + str(CurrPitch_ReleaseSpeedMPH) + '\n'
    else:
        strTitleMultiLine = strTitleMultiLine + 'Pitch#: ' + str(CurrPitch_PitchNumber) + '  Plate MPH: ' + str(
            CurrPitch_PlateSpeedMPH) + '\n'



    strTitleMultiLine = strTitleMultiLine + 'Pitch Call: ' + CurrPitch_Call + '  Impact Coords: ' + CurrPitch_ImpactXstr + ', ' + str(CurrPitch_ImpactYint) +'"'

#    CommandToCall = CmdToCall + cmdParameters1 + Z1Params + '|' + intermedCoordsB + '|' + intermedCoordsA + '|' + NetParams + strAngle + strColor + strTitleMultiLine

#1/21/19 htc - copied following line to make it "reversable" on parameters for testing/getting graphs right.
    CommandToCall = CmdToCall + cmdParameters1 + Z1Params + '|' + NetParams + strAngle + strColor + strTitleMultiLine
#    CommandToCall = CmdToCall + cmdParameters1 + NetParams + '|' + Z1Params + strAngle + strColor + strTitleMultiLine

    return_code = subprocess.call(CommandToCall, shell=True)


    # 1/3/19 htc added debug lines (TRF at ABCA in Dallas today, tomorrow (Fri) and Saturday.
    WriteLogFile('Second Graph Call COMMAND STRING: ' + str(CommandToCall) + ']', '5050-CalculateMovementVer1          -')
    WriteLogFile('Second Graph Call RESULT: ' + str(return_code) + ']', '5050-CalculateMovementVer1          -')
    print('Second Graph Call COMMAND STRING: [' + str(CommandToCall) + ']')
    print('Second Graph Call RESULT: [' + str(return_code) + ']')


    if os.path.isfile('/home/pi/top.png'):  # os.system('sudo chmod 777 ' + '/home/pi/front.png')
        CmdCallResult = os.system('sudo rm /home/pi/top.png')

    cmdParameters1 = '-o "/home/pi/top.png" -p "'
    strAngle = '" -a "Top" '
    strColor = '-c "b" '
    strTitleMultiLine = '-t "Top View- Sess: ' + str(ThisSess_SeqNumber) + '  Name: ' + ThisSess_StudentDisplayName + '\n'


    # 1/21/19 htc - if CurrPitch_ReleaseSpeedMPH is zero, don't even show it!
    if CurrPitch_ReleaseSpeedMPH > 0:
        strTitleMultiLine = strTitleMultiLine + 'Pitch#: ' + str(CurrPitch_PitchNumber) + '  Plate MPH: ' + str(
            CurrPitch_PlateSpeedMPH) + '  Release MPH: ' + str(CurrPitch_ReleaseSpeedMPH) + '\n'
    else:
        strTitleMultiLine = strTitleMultiLine + 'Pitch#: ' + str(CurrPitch_PitchNumber) + '  Plate MPH: ' + str(
            CurrPitch_PlateSpeedMPH) + '\n'



    strTitleMultiLine = strTitleMultiLine + 'Pitch Call: ' + CurrPitch_Call + '  Impact Coords: ' + CurrPitch_ImpactXstr + ', ' + str(CurrPitch_ImpactYint) +'"'

#    CommandToCall = CmdToCall + cmdParameters1 + Z1Params + '|' + intermedCoordsB + '|' + intermedCoordsA + '|' +NetParams + strAngle + strColor + strTitleMultiLine

    # 1/21/19 htc - copied following line to make it "reversable" on parameters for testing/getting graphs right.
    CommandToCall = CmdToCall + cmdParameters1 + Z1Params + '|' + NetParams + strAngle + strColor + strTitleMultiLine
    # CommandToCall = CmdToCall + cmdParameters1 + NetParams + '|' + Z1Params + strAngle + strColor + strTitleMultiLine

    return_code = subprocess.call(CommandToCall, shell=True)
    print('Third Graph Call COMMAND STRING: [' + str(CommandToCall) + ']')
    print('Third Graph Call RESULT: [' + str(return_code) + ']')



    # 1/3/19 htc added debug lines (TRF at ABCA in Dallas today, tomorrow (Fri) and Saturday.
    WriteLogFile('Third Graph Call COMMAND STRING: ' + str(CommandToCall) + ']', '5050-CalculateMovementVer1          -')
    WriteLogFile('Third Graph Call RESULT: ' + str(return_code) + ']', '5050-CalculateMovementVer1          -')


    WriteLogFile('STOP TIME- call THREE MOVEMENT .png creations: [' + str(CommandToCall) + ']', '3010-CalculateMovementVer1          -')


    HTC_DUMMY_STOPPER_LINE = 'stop'


def SetVarsFromMoveOnLiteral(strMoveOnLiteralStringIN):


#10/22/18 htc - has TRF's new 2 miss/total or 1 success option in it.

    global CurrFrame_MoveOnSuccessCount
    global CurrFrame_MoveOnMissCount
    global CurrFrame_MoveOnTotalCount

    CurrFrame_MoveOnSuccessCount = 0
    CurrFrame_MoveOnMissCount = 99    #9/29/18 htc - TRF didn't put # of misses in first version of Practice Mode setup on SmartSheet page so alwasy set to 99.
    CurrFrame_MoveOnTotalCount =0


    if len(strMoveOnLiteralStringIN) < 1:
        return(213)

    strMoveOnLiteralStringIN = str(strMoveOnLiteralStringIN)

    if strMoveOnLiteralStringIN.upper() == 'AFTER 1ST PITCH':
        CurrFrame_MoveOnSuccessCount = 99
        CurrFrame_MoveOnTotalCount =1
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 2ND PITCH':
        CurrFrame_MoveOnSuccessCount = 99
        CurrFrame_MoveOnTotalCount =2
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 3RD PITCH':
        CurrFrame_MoveOnSuccessCount = 99
        CurrFrame_MoveOnTotalCount =3
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 4TH PITCH':
        CurrFrame_MoveOnSuccessCount = 99
        CurrFrame_MoveOnTotalCount =4
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 5TH PITCH':
        CurrFrame_MoveOnSuccessCount = 99
        CurrFrame_MoveOnTotalCount =5
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 6TH PITCH':
        CurrFrame_MoveOnSuccessCount = 99
        CurrFrame_MoveOnTotalCount =6
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 7TH PITCH':
        CurrFrame_MoveOnSuccessCount = 99
        CurrFrame_MoveOnTotalCount =7
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 8TH PITCH':
        CurrFrame_MoveOnSuccessCount = 99
        CurrFrame_MoveOnTotalCount =8
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 9TH PITCH':
        CurrFrame_MoveOnSuccessCount = 99
        CurrFrame_MoveOnTotalCount =9
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 10TH PITCH':
        CurrFrame_MoveOnSuccessCount = 99
        CurrFrame_MoveOnTotalCount =10
        return(0)

    if strMoveOnLiteralStringIN.upper() == 'AFTER 1ST SUCCESSFUL PITCH':
        CurrFrame_MoveOnSuccessCount = 1
        CurrFrame_MoveOnTotalCount =99
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 2ND SUCCESSFUL PITCH':
        CurrFrame_MoveOnSuccessCount = 2
        CurrFrame_MoveOnTotalCount =99
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 3RD SUCCESSFUL PITCH':
        CurrFrame_MoveOnSuccessCount = 3
        CurrFrame_MoveOnTotalCount =99
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 4TH SUCCESSFUL PITCH':
        CurrFrame_MoveOnSuccessCount = 4
        CurrFrame_MoveOnTotalCount =99
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 5TH SUCCESSFUL PITCH':
        CurrFrame_MoveOnSuccessCount = 5
        CurrFrame_MoveOnTotalCount =99
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 6TH SUCCESSFUL PITCH':
        CurrFrame_MoveOnSuccessCount = 6
        CurrFrame_MoveOnTotalCount =99
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 7TH SUCCESSFUL PITCH':
        CurrFrame_MoveOnSuccessCount = 7
        CurrFrame_MoveOnTotalCount =99
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 8TH SUCCESSFUL PITCH':
        CurrFrame_MoveOnSuccessCount = 8
        CurrFrame_MoveOnTotalCount =99
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 9TH SUCCESSFUL PITCH':
        CurrFrame_MoveOnSuccessCount = 9
        CurrFrame_MoveOnTotalCount =99
        return(0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 10TH SUCCESSFUL PITCH':
        CurrFrame_MoveOnSuccessCount = 10
        CurrFrame_MoveOnTotalCount =99
        return(0)

#10/22/18 htc - added this for TRF - he added a drill for Naperville's open house today at 7:30 AM for me to "fix" and update.
    if strMoveOnLiteralStringIN.upper() == 'AFTER 1ST PITCH OR SUCCESS':
        CurrFrame_MoveOnSuccessCount = 1
        CurrFrame_MoveOnMissCount = 1
        CurrFrame_MoveOnTotalCount = 1
        return (0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 1 PITCH OR SUCCESS':    #here due to TRF's typo on smartsheet 10/22/18.
        CurrFrame_MoveOnSuccessCount = 1
        CurrFrame_MoveOnMissCount = 1
        CurrFrame_MoveOnTotalCount = 1
        return (0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 2ND PITCH OR SUCCESS':
        CurrFrame_MoveOnSuccessCount = 1
        CurrFrame_MoveOnMissCount = 2
        CurrFrame_MoveOnTotalCount = 2
        return (0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 3RD PITCH OR SUCCESS':
        CurrFrame_MoveOnSuccessCount = 1
        CurrFrame_MoveOnMissCount = 3
        CurrFrame_MoveOnTotalCount = 3
        return (0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 4TH PITCH OR SUCCESS':
        CurrFrame_MoveOnSuccessCount = 1
        CurrFrame_MoveOnMissCount = 4
        CurrFrame_MoveOnTotalCount = 4
        return (0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 5TH PITCH OR SUCCESS':
        CurrFrame_MoveOnSuccessCount = 1
        CurrFrame_MoveOnMissCount = 5
        CurrFrame_MoveOnTotalCount = 5
        return (0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 6TH PITCH OR SUCCESS':
        CurrFrame_MoveOnSuccessCount = 1
        CurrFrame_MoveOnMissCount = 6
        CurrFrame_MoveOnTotalCount = 6
        return (0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 7TH PITCH OR SUCCESS':
        CurrFrame_MoveOnSuccessCount = 1
        CurrFrame_MoveOnMissCount = 7
        CurrFrame_MoveOnTotalCount = 7
        return (0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 8TH PITCH OR SUCCESS':
        CurrFrame_MoveOnSuccessCount = 1
        CurrFrame_MoveOnMissCount = 8
        CurrFrame_MoveOnTotalCount = 8
        return (0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 9TH PITCH OR SUCCESS':
        CurrFrame_MoveOnSuccessCount = 1
        CurrFrame_MoveOnMissCount = 9
        CurrFrame_MoveOnTotalCount = 9
        return (0)
    if strMoveOnLiteralStringIN.upper() == 'AFTER 10TH PITCH OR SUCCESS':
        CurrFrame_MoveOnSuccessCount = 1
        CurrFrame_MoveOnMissCount = 10
        CurrFrame_MoveOnTotalCount = 10
        return (0)

    return (119)


def RunStandardAndPracticeSession(CurrentSessNoFromArgs):

    WriteLogFile('run STANDARD Session Mode with session number: [' + str(RunThisSessionNumber) + ']','0030-RunStandardAndPracticeSession       -')

    smartmitt_conn = mariadb.connect(user='smartmitt', password='smartmitt', database='smartmitt', host='127.0.0.1')
    cursor_session = smartmitt_conn.cursor()
    cursor_session.execute('SELECT * FROM sessions WHERE SeqSessionNumber = ' + str(RunThisSessionNumber))
    row = cursor_session.fetchone()
#    WriteLogFile('Session Number READ / id Returned: ' + row[3] + ' / ' + row[0] + '   0001-Main -                   -')

    global ThisSess_MachineId
    global ThisSess_AccountId
    global ThisSess_SeqNumber
    global ThisSess_InitialStatus
    global ThisSess_CurrentStatus
    global ThisSess_Type
    global ThisSess_StandTargetGuid
    global ThisSess_PracticeGuid
    global ThisSess_GameLineUpGuid
    global ThisSess_ArcadeGuid
    global ThisSess_BallType
    global ThisSess_DisplaySpeedSecs
    global ThisSess_DisplayImpactSecs
    global ThisSess_SuspendTimeOutSeconds_ReallyMINUTES
    global ThisSess_DisplayRiverYN
    global ThisSess_DisplayPitchCountBarsYN
    global ThisSess_YdeltaPlusMinus3
    global ThisSess_PitchingDistanceFeet
    global ThisSess_SystemOnLineYN
    global ThisSess_ShutdownMode
    global ThisSess_StudentDisplayName
    global ThisSess_RepetitionCountLimit
    global ThisSess_CurrentRepCount

    global SuccessCount
    global MissCount
    global NoPitchCount


#11/30/18 htc
    global ThisSess_ReleaseSpeedAddon
    ThisSess_ReleaseSpeedAddon = 0




#12/04/18 HTC
    global intPctOfXcol
    global intPctOfYrow




#10/09/18 htc - made ThisSessionFolderName a global variable so I can access it at the end of the program to capture copy of MainLog.txt file.
    global ThisSessionFolderName


 # 8/29/18 htc - added hard coded path names for now.
 #   SpeedFilePath = '/home/pi/NetworkShare/speed.txt'
 #   NetworkSharePath = '/home/pi/NetworkShare'
 #   StopFilePath = '/home/pi/NetworkShare/stop.txt'

##    ThisSess_MachineId = row[1]  9/9/18 HTC - Set in MAIN from control file in the main SQL database on this "machine"
    ThisSess_AccountId = row[2]
    ThisSess_SeqNumber = row[3]
    ThisSess_InitialStatus = row[4]
    ThisSess_CurrentStatus = row[4]
    ThisSess_Type = row[5]
    ThisSess_StandTargetGuid = row[6]
    ThisSess_PracticeGuid = row[7]
    ThisSess_GameLineUpGuid = row[8]
    ThisSess_ArcadeGuid = row[9]
    ThisSess_BallType = row[10]
    ThisSess_DisplaySpeedSecs = row[11]
    ThisSess_DisplayImpactSecs = row[12]
    ThisSess_SuspendTimeOutSeconds_ReallyMINUTES = row[13]      #9/23/18 HTC - says Seconds but is actually minutes.  x60 below.
    ThisSess_DisplayRiverYN  = row[14]
    ThisSess_DisplayPitchCountBarsYN = row[15]
    ThisSess_YdeltaPlusMinus3 = row[16]
    ThisSess_PitchingDistanceFeet = row[17]
    ThisSess_SystemOnLineYN = row[18]
    ThisSess_ShutdownMode = 'TimeOut'
    ThisSess_StudentDisplayName = str(row[19])
#12/04/18 htc - ALWAYS read the student record.
#    if ThisSess_StudentDisplayName == '' or ThisSess_StudentDisplayName == 'None':
    smartmitt_conn = mariadb.connect(user='smartmitt', password='smartmitt', database='smartmitt', host='127.0.0.1')
    cursor_localuser = smartmitt_conn.cursor()
    cursor_localuser.execute('SELECT * FROM LocalUsers WHERE AccountID = ' +  "'" + str(ThisSess_AccountId) + "'")
    UserRow = cursor_localuser.fetchone()
    if UserRow == 'None' or UserRow == None:
        ThisSess_StudentDisplayName = '--------'
        ThisSess_BallType = 'Baseball'   #default   10/09/18 htc
    else:
        ThisSess_StudentDisplayName = UserRow[6]
        ThisSess_BallType = UserRow[12]


# 9/25/18 htc - added rep count per TRF's request.
    ThisSess_RepetitionCountLimit = str(row[25])
    if ThisSess_RepetitionCountLimit  == 'None':
        ThisSess_RepetitionCountLimit = 1
    if ThisSess_RepetitionCountLimit  == None:
        ThisSess_RepetitionCountLimit = 1
    if str(ThisSess_RepetitionCountLimit) < '0':
        ThisSess_RepetitionCountLimit = 1
    if str(ThisSess_RepetitionCountLimit) > '9':
        ThisSess_RepetitionCountLimit = 1



# 11/30/18 htc - added ReleaseSpeedAddon field
    if str(UserRow[26]) >= '1' and str(UserRow[26]) <= '9':
        ThisSess_ReleaseSpeedAddon = UserRow[26]
    else:
        ThisSess_ReleaseSpeedAddon = 0
#12/04/18 htc - PATCH to Kris code, he's NOT putting speedAddon in SESSION record, I have to get it from student record.

    if ThisSess_ReleaseSpeedAddon == 0:
        ThisSess_ReleaseSpeedAddon = UserRow[35]


    if ThisSess_SuspendTimeOutSeconds_ReallyMINUTES < 1:
        ThisSess_SuspendTimeOutSeconds_ReallyMINUTES = 15     #default to 15 minutes. Says seconds, but is actually minutes- 9/23/18 htc.

    smartmitt_conn.close()
    gc.collect()

    for EachFile in os.listdir(NetworkSharePath):
        FileToRemoveFullPath = NetworkSharePath + '/' + EachFile
        os.remove(FileToRemoveFullPath)

    #9/15/18 htc added code to create a sub-folder for every session by YYYYMMDD-MachID-SessNo-AccountID.   NOTE: Session number is zero filled to 6 digits.
##
    ##
         ## ************************************** NOTE: 9/15/18 hts - if FOLDER EXISTS, means RESUMING (most liikely) this session
    ##                                                   Be on the "lookout" for EXISTING files with SAME PITCH NUMBER ???????????

# 9/23/18 htc - copied from gloabl top section:   SessionsLocalSaveFolder = '/home/pi/PitchSessionFiles'
### 9/27/18 htc - decided to take DATE out of folder session path name, if they resume a suspended session on a later day, makes finding appending to that session a mother fuckin BITCH !!!
###    ThisSessionFolderName = SessionsLocalSaveFolder + '/' + time.strftime('%Y%m%d', time.localtime()) + '-' + ThisSess_MachineId + '-' + str(ThisSess_SeqNumber).zfill(6) + '-' + ThisSess_AccountId


    ThisSessionFolderName = SessionsLocalSaveFolder + '/' + ThisSess_MachineId + '-' + str(ThisSess_SeqNumber).zfill(6) + '-' + ThisSess_AccountId

    gintResumeSession_StartPitchNumber = 0

    if os.path.isdir(ThisSessionFolderName) == False:
        gintResumeSession_StartPitchNumber = 0

#9/23/18 htc - had to "sudo" these commands now that my .py code is running from "php-students"
####   ACTUALLY- moved this back to /home/pi   - 9/23/18 htc. but kept "sudo" code here just in case for later.
## 10/04/18 htc         os.mkdir(ThisSessionFolderName)

 ###       WriteLogFile('Try to run- sudo cp  -r   on: /var/www/html/students/PitchSessionFiles/empty to new: ' + ThisSessionFolderName, '0030-RunStandardAndPracticeSession       -')

        ###        OsReturnResult = os.system('sudo cp -r /var/www/html/students/PitchSessionFiles/empty ' + ThisSessionFolderName)

        ###       WriteLogFile('Return value from OS on sudo cp  -r : [' + str(OsReturnResult) + ']', '0030-RunStandardAndPracticeSession       -')



#        WriteLogFile('Try to run- sudo chmod -R 511 on: /var/www/html/students/PitchSessionFiles', '0030-RunStandardAndPracticeSession       -')
#        OsReturnResult = os.system('sudo chmod -R 511 /var/www/html/students/PitchSessionFiles')
#        WriteLogFile('Return value from OS on sudo chmod -R 511 /var/www/html/students/PitchSessionFilescommand: [' + str(OsReturnResult) + ']', '0030-RunStandardAndPracticeSession       -')


        WriteLogFile('Try to run- sudo mkdir  on: [' + str(ThisSessionFolderName) + ']', '0030-RunStandardAndPracticeSession       -')

        OsReturnResult = os.system('sudo mkdir ' + ThisSessionFolderName)

        WriteLogFile('Return value from OS on sudo mkdir command: [' + str(OsReturnResult) + ']', '0030-RunStandardAndPracticeSession       -')


## 10/04/18 htc        os.chmod(ThisSessionFolderName, 511)  #INTEGER, NOT OCTAL, so 511 dec = 777 octal

        WriteLogFile('Try to run- sudo chmod 777 on: [' + str(ThisSessionFolderName) + ']', '0030-RunStandardAndPracticeSession       -')

        OsReturnResult = os.system('sudo chmod 777 ' + ThisSessionFolderName)

        WriteLogFile('Return value from OS on sudo chmod 777 command: [' + str(OsReturnResult) + ']', '0030-RunStandardAndPracticeSession       -')

# 10/04/18 htc - when I "auto-run" from PHP, the owner of this folder is "www-data" and I can't write files to it.
#               So I used these commands to change owner and group
    #         os.chown(ThisSessionFolderName, 'pi')

        WriteLogFile('Try to run- sudo chown pi on: [' + str(ThisSessionFolderName) + ']', '0030-RunStandardAndPracticeSession       -')

        OsReturnResult = os.system('sudo chown pi ' + ThisSessionFolderName)

        WriteLogFile('Return value from OS on sudo chOWN command: [' + str(OsReturnResult) + ']', '0030-RunStandardAndPracticeSession       -')

        WriteLogFile('Try to run- sudo chgrp pi on: [' + str(ThisSessionFolderName) + ']', '0030-RunStandardAndPracticeSession       -')

        OsReturnResult = os.system('sudo chgrp pi ' + ThisSessionFolderName)

        WriteLogFile('Return value from OS on sudo chGRP command: [' + str(OsReturnResult) + ']', '0030-RunStandardAndPracticeSession       -')


    else:   #9/27/18 htc- check pitch table with this session ID and get last pitch number, then add 1 and sset SequentialPitchNumber.
        smartmitt_conn = mariadb.connect(user='smartmitt', password='smartmitt', database='smartmitt', host='127.0.0.1')
        cursor_session = smartmitt_conn.cursor()
        cursor_session.execute('SELECT Max(PitchNumber) FROM LocalPitchTable WHERE SessionNumber = ' + str(RunThisSessionNumber) + ' Group By SessionNumber;')
        row = cursor_session.fetchone()
        #
        if row == None:
            gintResumeSession_StartPitchNumber = 0
        else:
            gintResumeSession_StartPitchNumber = row[0]

        smartmitt_conn.close()
        gc.collect()

    KeepProcessingPitches = True
    SequentialPitchNumber = gintResumeSession_StartPitchNumber

#9/20/18 htc - moved this global declaration up to top after it threw an error for Kris (SanFran pgmer) trying to launch this program.
#    global strStartupOptionsForTesting

#9/14/18 htc added CURRENT PITCH global variables
    global CurrPitch_PlateSpeedMPH
    global CurrPitch_ReleaseSpeedMPH
    global CurrPitch_PitchNumber
    global CurrPitch_ImpactXstr
    global CurrPitch_ImpactXint
    global CurrPitch_ImpactYint
    global CurrPitch_SpinRPM
    global CurrPitch_SpinAxis
    global CurrPitch_Call
    global CurrPitch_TargetGUID
    global CurrPitch_MovementInfo
    global CurrPitch_ExpectedPitch
    global CurrPitch__ExpectedSpeedRange
    global CurrPitch_MarqueeContent
    global CurrPitch_PracticeModeHitZones
    global CurrPitch_FullPath1
    global CurrPitch_FullPath2
    global CurrPitch_FullPath3
    global CurrPitch_FullPath4
    global CurrPitch_FullPath5
    global CurrPitch_FullPath6

#11/30/18 htc
    global CurrPitch_ImpactXstrZ1
    global CurrPitch_ImpactXintZ1
    global CurrPitch_ImpactYintZ1
    global BallCentersString1
    global BallCentersString2
    global CurrPitch_MovementInfo



# 9/22/18 htc - copied these variables down here just for reference.
#    SpeedFilePath = '/home/pi/NetworkShare/speed.txt'
#    NetworkSharePath = '/home/pi/NetworkShare'
#    StopFilePath = '/home/pi/NetworkShare/stop.txt'
#    # StopFilePath = '/var/www/html/students/stop.txt'
#    # 9/22/18 htc - added 2 more paths because had to run out of "students" sub-folder in www/html area becasue PHP couldn't launch .py in /home/pi ?????
#    SessionsLocalSaveFolder = '/home/pi/PitchSessionFiles'
#    PathForFilesToDisplayOnDevice = '/var/www/html/students'
#    ImpactLocatorHomeFolder = '/home/pi/ImpactLocator'



# 9/27/18 htc - added Current Frame Global Variables for PRACTICE MODE.
    global CurrFrame_SuccessCount
    global CurrFrame_MissCount
    global CurrFrame_TotalCount
    global CurrFrame_MoveOnLiteral
    global CurrFrame_MoveOnSuccessCount
    global CurrFrame_MoveOnMissCount
    global CurrFrame_MoveOnTotalCount
    global CurrFrame_PaintTargetSquareYN
    global CurrFrame_StartX
    global CurrFrame_StartY
    global CurrFrame_EndX
    global CurrFrame_EndXY
    global CurrFrame_PitchType

 #9/28/18 htc - setup counters for Practice mode IF selected, Always set counter to "trigger" a "new frame" on first pass through loop.
    CurrFrame_FrameNumber = 0
    ThisSess_CurrentRepCount = 0
    CurrFrame_SuccessCount = 999
    CurrFrame_MissCount = 999
    CurrFrame_TotalCount = 999
    CurrFrame_MoveOnSuccessCount = 0
    CurrFrame_MoveOnMissCount = 0
    CurrFrame_MoveOnTotalCount =0
    CurrFrame_StartX  = ''
    CurrFrame_StartY = 0
    CurrFrame_EndX = ''
    CurrFrame_EndXY = 0
#12/05/18 htc
    CurrFrame_PitchType = ''

#CurrPitch_ExpectedPitch
    CurrPitch_ExpectedPitch = 'STANDARD'

    WriteLogFile('Starting while loop for KeepProcessingPitches','0030-RunStandardAndPracticeSession       -')

    TargetToDefine = ThisSess_StandTargetGuid


#1/3/19 htc
    global gbolHomeRunThisPitch
    gbolHomeRunThisPitch = False


    while KeepProcessingPitches:


##  display target
        ClearTargetArea()   #not sure this is necessary with the next stmt.



        if ThisSess_Type.upper() == 'PRACTICE':


            if CurrFrame_SuccessCount >= CurrFrame_MoveOnSuccessCount or CurrFrame_MissCount >= CurrFrame_MoveOnMissCount or CurrFrame_TotalCount >= CurrFrame_MoveOnTotalCount:
                CurrFrame_SuccessCount = 0
                CurrFrame_MissCount = 0
                CurrFrame_TotalCount = 0
                CurrFrame_FrameNumber =  CurrFrame_FrameNumber + 1


                smartmitt_conn_pracframe = mariadb.connect(user='smartmitt', password='smartmitt', database='smartmitt', host='127.0.0.1')
                cursor_pracframe = smartmitt_conn_pracframe.cursor()
                cursor_pracframe.execute('SELECT * FROM PracticeModeFrames WHERE PrimaryColumn = ' + '"' + str(ThisSess_PracticeGuid) + '"' + ' and PracModeSeq = '+  str(CurrFrame_FrameNumber) )
    #            cursor_pracframe.execute('SELECT * FROM PracticeModeFrames WHERE PrimaryColumn = ' + '"' + str(ThisSess_PracticeGuid) + '"')
                framerow = cursor_pracframe.fetchone()


                if framerow == None and CurrFrame_FrameNumber == 1:
                    WriteLogFile('ERROR - Practice Mode FIRST FRAME NOT FOUND for sess/guid/frame#- exiting program 888: [' + str(RunThisSessionNumber) +  ' - ' + str(ThisSess_PracticeGuid) + str(CurrFrame_FrameNumber) + ']',
                                 '0030-RunSTANDARDSession       -')
                    smartmitt_conn_pracframe.close()
                    gc.collect()
                    exit(888)

                else:
    #9/30/18 htc  - implemnet repcount logic here by simply resetting variables, maybe read ALL frames and set upper frame number limit when enter this routine above ?????????\
    #    ThisSess_CurrentRepCount = ThisSess_CurrentRepCount + 1
    # 9/27/18 htc -  ThisSess_RepetitionCountLimit - set off session record in SQL read above.
                    if framerow == None and CurrFrame_FrameNumber > 1:

                        ThisSess_CurrentRepCount = ThisSess_CurrentRepCount + 1       #ThisSess_RepetitionCountLimit
                        WriteLogFile('PRACTICE MODE Repeat Count > 1, loop  [' + str(ThisSess_CurrentRepCount) + ' of  ' + str(ThisSess_RepetitionCountLimit)  + ']', '0030-RunStandardAndPracticeSession       -')

                        if str(ThisSess_CurrentRepCount) >= str(ThisSess_RepetitionCountLimit):

                            KeepProcessingPitches = False

                            WriteLogFile('Practice Mode Rep Limit Hit- normal stop pgm: for sess/guid: [' + str(RunThisSessionNumber) + ' - ' + str(ThisSess_PracticeGuid) + ']', '0030-RunSTANDARDSession       -')

                        else:

                            CurrFrame_FrameNumber = 1

                            cursor_pracframe.execute('SELECT * FROM PracticeModeFrames WHERE PrimaryColumn = ' + '"' + str(ThisSess_PracticeGuid) + '"' + ' and PracModeSeq = ' + str(CurrFrame_FrameNumber))
                    #            cursor_pracframe.execute('SELECT * FROM PracticeModeFrames WHERE PrimaryColumn = ' + '"' + str(ThisSess_PracticeGuid) + '"')
                            framerow = cursor_pracframe.fetchone()



                #                        WriteLogFile('End Of Frames for sess/guid/frame#- exiting program 811: [' + str(
#                            RunThisSessionNumber) + ' - ' + str(ThisSess_PracticeGuid) + str(CurrFrame_FrameNumber) + ']',
#                                     '0030-RunSTANDARDSession       -')
#                        smartmitt_conn_pracframe.close()
#                        gc.collect()
#                        exit(811)


#                    else:  #  Next frame successfully read from frame table, set variables and go on.
                        # 9/30/18 htc - TODAY- CAN NOT RESUME A PRACTICE MODE !!!!!!!!!!!!!!                    gintResumeSession_StartPitchNumber = row[0]

                    if KeepProcessingPitches:
                        CurrFrame_PractModeGUID = ThisSess_PracticeGuid
                        CurrFrame_MoveOnLiteral = framerow[12]
                        SetVarsFromMoveOnLiteral(str(CurrFrame_MoveOnLiteral))
#10/23/18 HTC Added in set vars routine, more options now in pract mode setup on SSheet.   CurrFrame_MoveOnMissCount = 99  #9/29/18 htc - TRF didn't setup any MISS counts in the SmartSheet practice mode detail "FRAME" table, always force to 99 for now.

                        CurrFrame_PaintTargetSquareYN = 'Y'
                        CurrFrame_StartX = framerow[8]
                        CurrFrame_StartY = framerow[9]
                        CurrFrame_EndX = framerow[10]
                        CurrFrame_EndXY = framerow[11]

#12/05/18 htc
                        CurrFrame_PitchType = framerow[7]
                        CurrPitch_ExpectedPitch = CurrFrame_PitchType

                        TargetBoxCoords =  str(CurrFrame_StartX) + ',' + str(CurrFrame_StartY) + ' / ' + str(CurrFrame_EndX) + ',' + str(CurrFrame_EndXY)

                        CurrPitch_MarqueeContent = framerow[7]

                        TargetToDefine = framerow[6]    #  CurrFrame_BaseTarget
                        CurrFrame_BaseTarget = TargetToDefine

                        smartmitt_conn_pracframe.close()
                        gc.collect()


                        WriteLogFile('PractMode Success-Miss-Total FRAME # - count/limit format:[Frame:(' +  str(CurrFrame_FrameNumber) + ')' +
                           '  Succ:' + str(CurrFrame_SuccessCount) + '/' + str(CurrFrame_MoveOnSuccessCount) +
                           '  Miss:' + str(CurrFrame_MissCount) + '/' + str(CurrFrame_MoveOnMissCount) +
                           '  Totl:' + str(CurrFrame_TotalCount) + '/' + str(CurrFrame_MoveOnTotalCount),'DEBUG FOR PRACT MODE- MainLoop')
                        WriteLogFile('Marquee Content, MoveOnLiteral, TargetBox: ' + str(CurrPitch_MarqueeContent) + ' - ' + str(CurrFrame_MoveOnLiteral) + ' - ' + str(TargetBoxCoords),'DEBUG FOR PRACT MODE- MainLoop')



        if KeepProcessingPitches:


            ClearMarqueeArea()


#12/18/18 htc
            if bolDisplayPitchNoOnMainLED == False:
                BuildSelectedBaseTargetArrayForThisRun(TargetToDefine, CurrFrame_StartX, CurrFrame_StartY, CurrFrame_EndX, CurrFrame_EndXY)
            else:
                DisplaySpeed(CurrPitch_PitchNumber, SM_Green, 'PITCH NO')



#12/18/18 htc added  bolDisplaySessNoAndPitchNoOnMarqee  logic
            if bolDisplaySessNoAndPitchNoOnMarqee == False:
                if ThisSess_Type.upper() == 'PRACTICE':
                    MarqueeWord(CurrPitch_MarqueeContent, '')
                else:
                    MarqueeWord(ThisSess_StudentDisplayName, '')
            else:
                MarqueeWord(str(ThisSess_SeqNumber) + ' - ' + str(CurrPitch_PitchNumber), '')





            UpdateSuccessMissCountersInLedArray(SuccessCount, MissCount)

            UpdateNoPitchCountInLedArray(NoPitchCount)

            Write1260ArrayToArtnetFile()  # Write array to NdbArtNetCtrlString.txt file
            ArtdmxToNDB()  # play current NdbArtNetCtrlString.txt on disk in home folder to NDB/LED 10.0.0.100

    #        ArtnetTxtToJpg('NdbArtNetCtrlString.txt', 'CurrTarget.jpg', width=300)
    #        ArtnetTxtToJpg('NdbArtNetCtrlString.txt', '/home/pi/NetworkShare/CurrTarget.jpg', width=300)

    ##################   WAIT FOR SPEED.TXT or TIMEOUT              It says SECONDS but is really minutes from PHP interface!!! 9/23/18/htc
            ReturnSpeedValue = WaitForSpeedFile(ThisSess_SuspendTimeOutSeconds_ReallyMINUTES * 60)


            WriteLogFile('Response from WaitForSpeedFile:  ReturnSpeedValue = [' + str(ReturnSpeedValue) + ']' +
                         '  SpeedAddon = [' + str(ThisSess_ReleaseSpeedAddon) + ']', '0030-RunStandardAndPracticeSession       -')


    # 9/9/18 htc - no matter what - set the time the SpeedDisplayTimerSecs will "expire".
            CurrentTime = datetime.datetime.now()
            ImpactOkToDisplayAtThisTime = CurrentTime + datetime.timedelta(seconds=ThisSess_DisplaySpeedSecs)

            if ReturnSpeedValue > 10 and ReturnSpeedValue < 110:

                if ThisSess_DisplaySpeedSecs > 0:

 # 11/30/18 htc moved to inside DisplaySpeed routine                   MarqueeWord('PLATE SP', '')

 #12/05/18 htc - ThisSess_ReleaseSpeedValue had "NoneType" value ???  just forced it.
                    if ThisSess_ReleaseSpeedAddon == None:
                        ThisSess_ReleaseSpeedAddon = 0

                    if str(ThisSess_ReleaseSpeedAddon) == '':
                        ThisSess_ReleaseSpeedAddon = 0


                    if int(ThisSess_ReleaseSpeedAddon) > 0 and int(ThisSess_ReleaseSpeedAddon) < 10:

                        DisplaySpeed(ReturnSpeedValue, SM_Red_Med, 'PLATE SP')
                        time.sleep(ThisSess_DisplaySpeedSecs)


                        DisplaySpeed(ReturnSpeedValue + int(ThisSess_ReleaseSpeedAddon), SM_Blue_Med,  '-RELEASE')
                        time.sleep(ThisSess_DisplaySpeedSecs)

                    else:

                        DisplaySpeed(ReturnSpeedValue, SM_Red_Med, 'PLATE SP')


                strXcoord = ''
                intXcoord = 0
                intYcoord = 0
                NoPitchFlag = False

                StartTime = datetime.datetime.now()
    #           ExpireTime = StartTime + datetime.timedelta(seconds=TimeOutValueToAbort)
                ExpireTime = StartTime + datetime.timedelta(seconds=(ThisSess_SuspendTimeOutSeconds_ReallyMINUTES * 60))   #9/22/18 htc - I think this is MINUTES, so x60.

    # 9/17/18 htc - added checks for speed dispaly and impact dispaly - if ZERO, do not display at all, BUT, SPEED wait still 3 seconds for ozans file to show up!!!!!!!
                if ThisSess_DisplaySpeedSecs > 3:
                    CurrentTime = datetime.datetime.now()
                    while (ImpactOkToDisplayAtThisTime > CurrentTime):
                        time.sleep(0.6)               #11/30/18 htc - changed from 1.1 to 0.6
                        CurrentTime = datetime.datetime.now()
                else:
                    time.sleep(3.1)

                NoPitchFlag = False
                bolGotBallLineFile1 = False
                bolGotBallLineFile2 = False

    #9/22/18 htc - see if "quick" nopitch flag from ozans programs.
                for EachFile in os.listdir(NetworkSharePath):
                    if EachFile == 'NOPITCH.txt':
                        strXcoord = ''
                        intXcoord = 0
                        intYcoord = 0
                        NoPitchFlag = True
                        bolGotBallLineFile1 = False
                        bolGotBallLineFile2 = False
                        WriteLogFile('Found NOPITCH.txt file in NetworkSharePath, abortintg this pitch as no-pitch.', '0030-RunStandardAndPracticeSession       -')

                if NoPitchFlag:

                    for EachFile in os.listdir(NetworkSharePath):
                        FileToRemoveFullPath = NetworkSharePath + '/' + EachFile
                        os.remove(FileToRemoveFullPath)

                else:

                    bolGotBallLineFile1 = False
                    bolGotBallLineFile2 = False
                    for EachFile in os.listdir(NetworkSharePath):

    # 9/16/18 htc - take care of "Cam1_ballLine_20180913165741.png" files 1 and 2 here- these are INPUT to ImpactLocator (ozan's program) for impact results/location.
                        if EachFile[0:3] == 'Cam' and EachFile[5:13] == 'ballLine':
                            CamNumOnly = EachFile[3:4]
                            if CamNumOnly == '1':
                                bolGotBallLineFile1 = True
                                os.rename(NetworkSharePath + '/' + EachFile, NetworkSharePath + '/Cam1BallLine.png')
     #                           CommandToCall = 'cp ' + NetworkSharePath + '/Cam1BallLine.png ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam1BallLine.png'
     #                           CmdCallResult = os.system(CommandToCall)

                            if CamNumOnly == '2':
                                bolGotBallLineFile2 = True
                                os.rename(NetworkSharePath + '/' + EachFile, NetworkSharePath + '/Cam2BallLine.png')
     #                          CommandToCall = 'cp ' + NetworkSharePath + '/Cam2BallLine.png ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam2BallLine.png'
     #                           CmdCallResult = os.system(CommandToCall)


    # 9/16/18 htc - take care of "Cam1_20180913165741.png" files 1 and 2 here. CRITICAL FRAME
                        if EachFile[0:3] == 'Cam' and EachFile[5:13] != 'ballLine' and EachFile[-4:-1] == '.pn':
                            CamNumOnly = EachFile[3:4]
                            if CamNumOnly == '1':
                                bolGotBallLineFile1 = True
                                os.rename(NetworkSharePath + '/' + EachFile, NetworkSharePath + '/Cam1CriticalFrame.png')
 # 10/30/18 htc not needed anymore, displayed direct from archive folder via full path stored in SQL datbase on each pitch. if os.path.isfile(PathForFilesToDisplayOnDevice + '/Cam1CriticalFrameNEW.png'):
  # 10/30/18 htc not needed anymore                                   os.system('sudo rm ' + PathForFilesToDisplayOnDevice + '/Cam1CriticalFrameNEW.png')
  # 10/30/18 htc not needed anymore                               CommandToCall = 'cp ' + NetworkSharePath + '/Cam1CriticalFrame.png ' + PathForFilesToDisplayOnDevice + '/Cam1CriticalFrameNEW.png'
  # 11/11/18 htc commented out -causing runtime error     CmdCallResult = os.system(CommandToCall)

    #                            CommandToCall = 'cp ' + NetworkSharePath + '/Cam1CriticalFrame.png ' + ThisSessionFolderName + '/' + str(
    #                                CurrPitch_PitchNumber).zfill(3) + 'Cam1CriticalFrame.png'
    #                            CmdCallResult = os.system(CommandToCall)

                            if CamNumOnly == '2':
                                bolGotBallLineFile2 = True
                                os.rename(NetworkSharePath + '/' + EachFile, NetworkSharePath + '/Cam2CriticalFrame.png')
    # 10/30/18 htc not needed anymore                             if os.path.isfile(PathForFilesToDisplayOnDevice + '/Cam2CriticalFrameNEW.png'):
    # 10/30/18 htc not needed anymore                                 os.system('sudo rm ' + PathForFilesToDisplayOnDevice + '/Cam2CriticalFrameNEW.png')
     # 10/30/18 htc not needed anymore                                CommandToCall = 'cp ' + NetworkSharePath + '/Cam2CriticalFrame.png ' + PathForFilesToDisplayOnDevice + '/Cam2CriticalFrameNEW.png'

    #                            CommandToCall = 'cp ' + NetworkSharePath + '/Cam2CriticalFrame.png ' + ThisSessionFolderName + '/' + str(
    #                                CurrPitch_PitchNumber).zfill(3) + 'Cam2CriticalFrame.png'
    #                            CmdCallResult = os.system(CommandToCall)


    # 9/25/18 htc - BallCenters contain X,Y informatoin from Ozan's program that TRF wanted for Z-1, Z-2, Z-3, etc for MOVEMENT INFORMATION - NOT FUCKING TESTED !!!!!!
                        if EachFile[0:3] == 'Cam' and EachFile[5:16] == 'ballCenters':
                            CamNumOnly = EachFile[3:4]
                            if CamNumOnly == '1':
                                os.rename(NetworkSharePath + '/' + EachFile, NetworkSharePath + '/Cam1BallCenters.txt')
    #                            CommandToCall = 'mv ' + NetworkSharePath + '/' + EachFile + ' ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + '-Cam1BallCenters.txt'
    #                            CmdCallResult = os.system(CommandToCall)

                            if CamNumOnly == '2':
                                os.rename(NetworkSharePath + '/' + EachFile, NetworkSharePath + '/Cam2BallCenters.txt')
    #                            CommandToCall = 'mv ' + NetworkSharePath + '/' + EachFile + ' ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + '-Cam2BallCenters.txt.png'
    #                            CmdCallResult = os.system(CommandToCall)




                    # 9/16/18 htc - take care of "CCam1_20180913165809_2000_0.avi" files 1 and 2 here.  VIDEO files from both cameras if there- OPTION setup in each camera config file.
                    # 9/18/18 htc - Only archive these files, they are MOVED after we know we have a valid pitch and can save the files in the session subfolder with current pitch number.
                    # 9/25/18 htc - DO NOT save the *.avi (movie) files, they are around 15MB EACH from each camera.  just discard for now, no real useful info in them for now for space used.
                    #                    SO - imply ignore them in the NetworkShare folder and they will be deleted by the clean-up process.
                    #                    On our 120 GB SSD drives, around 6,000 videows would fill up the disk.  That's ONLY 60 pitches in only 100 sessions !!!!!!!!!!!!!!!!!!

                    strXcoord = ''
                    intXcoord = 0
                    intYcoord = 0

                    if bolGotBallLineFile1 and bolGotBallLineFile2:
    #                    CommandToCall = '/home/pi/ImpactLocator/ImpactLocator.out '
                        CommandToCall = '/home/pi/ImpactLocator/ImpactLocator.out '
                        CommandToCall = CommandToCall + '/home/pi/NetworkShare/Cam1BallLine.png '
                        CommandToCall = CommandToCall + '/home/pi/NetworkShare/Cam2BallLine.png '
                        CommandToCall = CommandToCall + '> /home/pi/NetworkShare/ImpactResult.txt'


                        WriteLogFile('Calling InpactResult: [' + CommandToCall + ']','0030-RunStandardAndPracticeSession       -')


                        return_code = subprocess.call(CommandToCall, shell=True)

                        ImpactResultFile = open('/home/pi/NetworkShare/ImpactResult.txt', 'r')
                        ImpactResultString = ImpactResultFile.read()
                        strWork1htc = ImpactResultString[0:6]
                        if strWork1htc.upper() != 'PIXEL:':
                            strXcoord = ''
                            intXcoord = 0
                            intYcoord = 0
                            NoPitchFlag = True
                            intPctOfXcol = 0
                            intPctOfYrow = 0
                        else:
     # 9/26/18 htc - parse new "4 line" output from Ozans ImpactLocator program (he fixed 9/24/18 to put out 4 lines instead of 1).
     ### these are old way, only one line
     ###                       strWork1htc = ImpactResultString[14:22]   # Impact Point: 137,137
     ###                       CommaLocation = strWork1htc.find(',')
     ###                       intPctOfXcol = int(strWork1htc[0:CommaLocation])
     ###                       SlashLocation = strWork1htc.find('\n')
     ###                       intPctOfYrow = int(strWork1htc[CommaLocation + 1:SlashLocation])
     ###                       htcDegugXpct = int((intPctOfXcol/640)*100)
     ###                       htcDegugYpct = int((intPctOfYrow/640)*100)

    # 9/26/18 htc - Actual code to parse FOUR line input, the whole file gets read as one string with "\n" in string for new lines.
    # Sample string to pares:  Pixel: 42, 211\nRatio: 0.14,0.44\nFeet: 6,28\nRowCol: 10,12   not sure if \n on last line or not, or EOF marker????
    #                        strWork1htc = ImpactResultString[14:22]
                            strWork1htc = ImpactResultString
                            strRatioLocation = strWork1htc.find('Ratio:')
                            strFeetLocation = strWork1htc.find('Feet:')
                            strWork1htc = strWork1htc[strRatioLocation + 7:strFeetLocation]
                            CommaLocation = strWork1htc.find(',')
                            strXlocDec = strWork1htc[0:CommaLocation]
                            SlashLocation = strWork1htc.find('\n')
                            strYlocDec = strWork1htc[CommaLocation + 1:SlashLocation]

                            intPctOfXcol = int(float(strXlocDec) * 100)
                            intPctOfYrow = int(float(strYlocDec) * 100)

    #9/18/18 htc - actully looks like Ozan's impact locator is now giving me RAW PIXEL COUNTS - 640 cols X 408 rows
    #                So now, before the coord evaluation, convert to percentages - as integer.
    #                        intXcoord = XevalNetLocPctCoordsV1(intPctOfXcol)
    #                        intYcoord = YevalNetLocPctCoordsV1(intPctOfYrow)

                            strXcoord = XevalNetLocPctCoordsV1(intPctOfXcol)
                            intYcoord = YevalNetLocPctCoordsV1(intPctOfYrow)

                            strDecValsToXYinfo ='Translate Ozans Pct X/Y to Actual X/Y Values = ' + str(intPctOfXcol) + ' X-pct = ' + str(strXcoord) + ' / ' + str(intPctOfYrow) + ' Y-pct = ' + str(intYcoord)
                            WriteLogFile(strDecValsToXYinfo, 'DEBUG LINE 10-03-18 htc - x/y coordinate Pct Teaks')
                            print('===============================================================')
                            print(strDecValsToXYinfo)

                if NoPitchFlag or strXcoord < 'A' or strXcoord > 'Z' or intYcoord < 1 or intYcoord > 26:

     #9/27/18 htc - added "CurrFrame" varaiables to suppor Practice Mode
     #               CurrFrame_SuccessCount = CurrFrame_SuccessCount + 1
                    CurrFrame_MissCount = CurrFrame_MissCount + 1
                    CurrFrame_TotalCount = CurrFrame_MissCount + 1

                    NoPitchCount = NoPitchCount + 1

                    ClearMarqueeArea()
                    MarqueeWord('NO PITCH', SM_Blue)
                    Write1260ArrayToArtnetFile()  # Write array to NdbArtNetCtrlString.txt file
                    ArtdmxToNDB()  # play current NdbArtNetCtrlString.txt on disk in home folder to NDB/LED 10.0.0.100
           #         ArtnetTxtToJpg('NdbArtNetCtrlString.txt', 'Impact.jpg', width=300)
                    time.sleep(ThisSess_DisplayImpactSecs)
                    for EachFile in os.listdir(NetworkSharePath):
                        FileToRemoveFullPath = NetworkSharePath + '/' + EachFile
                        os.remove(FileToRemoveFullPath)


                    print('NO PITCH - NO PITCH - NO PITCH')
                    WriteLogFile('NO PITCH - NO PITCH - NO PITCH', 'DEBUG LINE 10-26-18 htc             ')

                else:

                    intXcoord = strX2int(strXcoord)  #now we have number between 1 and 26 to convert to column ALPHA value.
                    SequentialPitchNumber = SequentialPitchNumber + 1
    #9/30/18 htc                BuildSelectedBaseTargetArrayForThisRun(ThisSess_StandTargetGuid)


                    CurrPitch_PitchNumber = SequentialPitchNumber


                    BuildSelectedBaseTargetArrayForThisRun(TargetToDefine, CurrFrame_StartX, CurrFrame_StartY, CurrFrame_EndX, CurrFrame_EndXY)



                    if EvalSuccessMiss(ThisSess_BallType, intXcoord, intYcoord) == 'SUCCESS':

                        # 9/27/18 htc - added "CurrFrame" varaiables to suppor Practice Mode
                        CurrFrame_SuccessCount = CurrFrame_SuccessCount + 1
     #                   CurrFrame_MissCount = CurrFrame_MissCount + 1
                        CurrFrame_TotalCount = CurrFrame_TotalCount + 1

                        SuccessCount = SuccessCount + 1

                        MarqueeWord('SUCCESS', SM_Green)
                        CurrPitch_Call = 'SUCCESS'
                    else:

                        # 9/27/18 htc - added "CurrFrame" varaiables to suppor Practice Mode
     #                   CurrFrame_SuccessCount = CurrFrame_SuccessCount + 1
                        CurrFrame_MissCount = CurrFrame_MissCount + 1
                        CurrFrame_TotalCount = CurrFrame_TotalCount + 1

                        MissCount = MissCount + 1

                        MarqueeWord('- MISS -', SM_Red)
                        CurrPitch_Call = 'MISS'

                    if ThisSess_DisplayImpactSecs > 0:
                        DisplayImpactLocation(intXcoord, intYcoord)


                    CurrPitch_FullPath1 = 'FP1'
                    CurrPitch_FullPath2 = 'FP2'
                    CurrPitch_FullPath3 = 'FP3'


                    if os.path.isfile(ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam1BallLine.png'):
                        os.system('sudo rm ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam1BallLine.png')
                    if os.path.isfile(NetworkSharePath + '/Cam1BallLine.png'):
                        os.system('sudo cp ' + NetworkSharePath + '/Cam1BallLine.png ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam1BallLine.png')
    # SessionsLocalSaveFolder
    #  if Kris/PHP can't read these mother fuckers, might have to chmod on it
    #        os.chmod(ThisSessionFolderName, 511)  #INTEGER, NOT OCTAL, so 511 dec = 777 octal

                    if os.path.isfile(ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam2BallLine.png'):
                        os.system('sudo rm ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam2BallLine.png')
                    if os.path.isfile(NetworkSharePath + '/Cam2BallLine.png'):
                        os.system('sudo cp ' + NetworkSharePath + '/Cam2BallLine.png ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam2BallLine.png')



                    if os.path.isfile(ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam1CriticalFrame.png'):
                        os.system('sudo rm ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam1CriticalFrame.png')
                    if os.path.isfile(NetworkSharePath + '/Cam1CriticalFrame.png'):
                        os.system('sudo cp ' + NetworkSharePath + '/Cam1CriticalFrame.png ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam1CriticalFrame.png')
    #                    CurrPitch_FullPath1 = ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam1CriticalFrame.png'
                        CurrPitch_FullPath1 = ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam1CriticalFrame.png'
    #9/30/18 htc cutoff front of path to store in format Kris needs to display in pitch table on users device. -- same for all files below.
                        CurrPitch_FullPath1 = str(CurrPitch_FullPath1)[23:100]
                    if os.path.isfile(ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam2CriticalFrame.png'):
                        os.system('sudo rm ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam2CriticalFrame.png')
                    if os.path.isfile(NetworkSharePath + '/Cam2CriticalFrame.png'):
                        os.system('sudo cp ' + NetworkSharePath + '/Cam2CriticalFrame.png ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam2CriticalFrame.png')
                        CurrPitch_FullPath2 = ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam2CriticalFrame.png'
                        # 9/30/18 htc cutoff front of path to store in format Kris needs to display in pitch table on users device. -- same for all files below.
                        CurrPitch_FullPath2 = str(CurrPitch_FullPath2)[23:100]

                    if os.path.isfile(ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam1BallCenters.txt'):
                        os.system('sudo rm ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam1BallCenters.txt')
                    if os.path.isfile(NetworkSharePath + '/Cam1BallCenters.txt'):
                        Cam1CentersFile = open(NetworkSharePath + '/Cam1BallCenters.txt', 'r')
                        BallCentersString1 =  Cam1CentersFile.read()
                        BallCentersString =  'Cam-ONE-pixelsX/Y: ' + BallCentersString1
                        CurrPitch_MovementInfo = ProcessOneBallCentersString(BallCentersString) #this just cleans up cr/lf type stuff.  12/01/18 htc
                        os.system('sudo cp ' + NetworkSharePath + '/Cam1BallCenters.txt ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam1BallCenters.txt')

                    if os.path.isfile(ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam2BallCenters.txt'):
                        os.system('sudo rm ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam2BallCenters.txt')
                    if os.path.isfile(NetworkSharePath + '/Cam2BallCenters.txt'):
                        Cam2CentersFile = open(NetworkSharePath + '/Cam2BallCenters.txt', 'r')
                        BallCentersString2 = Cam2CentersFile.read()
                        BallCentersString = BallCentersString2
                        CurrPitch_MovementInfo = CurrPitch_MovementInfo + ' | Cam-TWO-pixelsX/Y: ' + ProcessOneBallCentersString(BallCentersString) #this just cleans up cr/lf type stuff.  12/01/18 htc
                        os.system('sudo cp ' + NetworkSharePath + '/Cam2BallCenters.txt ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Cam2BallCenters.txt')


                    if os.path.isfile(ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Impact.jpg'):
                        os.system('sudo rm ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Impact.jpg')
                    if os.path.isfile(NetworkSharePath + '/Impact.jpg'):
                        os.system('sudo cp ' + NetworkSharePath + '/Impact.jpg ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Impact.jpg')
                        CurrPitch_FullPath3 = ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'Impact.jpg'
                        # 9/30/18 htc cutoff front of path to store in format Kris needs to display in pitch table on users device. -- same for all files below.
                        CurrPitch_FullPath3 = str(CurrPitch_FullPath3)[23:100]

                    #9/26/18 htc - added ImpactResult.txt
    # ImpactResultFile = open('/home/pi/NetworkShare/ImpactResult.txt', 'r')
                    if os.path.isfile(ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'ImpactResult.txt'):
                        os.system('sudo rm ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'ImpactResult.txt')
                    if os.path.isfile(NetworkSharePath + '/ImpactResult.txt'):
                        os.system('sudo cp ' + NetworkSharePath + '/ImpactResult.txt ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'ImpactResult.txt')


                    time.sleep(ThisSess_DisplayImpactSecs)

                    CurrPitch_PlateSpeedMPH = ReturnSpeedValue
                    CurrPitch_ReleaseSpeedMPH = 0
                    CurrPitch_PitchNumber = SequentialPitchNumber
                    CurrPitch_ImpactXstr = intX2str(intXcoord)
                    CurrPitch_ImpactXint = intXcoord
                    CurrPitch_ImpactYint = intYcoord
                    CurrPitch_SpinRPM = 0
                    CurrPitch_SpinAxis = 'unknown'
 #                   CurrPitch_TargetGUID  =  ThisSess_StandTargetGuid   # TargetToDefine
                    CurrPitch_TargetGUID  =  TargetToDefine   # TargetToDefine
 # 10/26/18 htc                   CurrPitch_MovementInfo = RemoveCRLF(CurrPitch_MovementInfo)
                    CurrPitch_ExpectedPitch = 'unknown'
                    CurrPitch__ExpectedSpeedRange = 'unknown'
    ## 9/30/18 htc using thisnow with practice mode                CurrPitch_MarqueeContent = 'unknown'
                    CurrPitch_PracticeModeHitZones = str(CurrFrame_StartX) + ',' + str(CurrFrame_StartY) + ':' + str(CurrFrame_EndX) + ',' + str(CurrFrame_EndXY)

                    # 9/25/18 htc set above with copy to archive folder section                CurrPitch_FullPath1 = 'CRITICAL FRAME CAMERA ONE FULL PATH'
    # 9/25/18 htc set above with copy to archive folder section                CurrPitch_FullPath2 = 'CRITICAL FRAME CAMERA TWO FULL PATH'
    # 9/25/18 htc set above with copy to archive folder section                CurrPitch_FullPath3 = 'IMPACT DOT JPEG FULL PATH'



# 11/30/18 htc added process BALL CENTERS sub-routine for "Z1" calculations.



                    print('Preparing to call MOVEMENT Sub-Routine.')
                    WriteLogFile('Preparing to call MOVEMENT Sub-Routine.', 'DEBUG LINE 01-05-19 htc             ')

                    MovementCallResult = CalculateMovementVer1()

                    print('Movement Sub-routine Call Result: [' + str(MovementCallResult) + ']')
                    WriteLogFile('Movement Sub-routine Call Result: [' + str(MovementCallResult) + ']', 'DEBUG LINE 01-05-19 htc             ')



                    CurrPitch_FullPath4 = 'FP4'
                    if os.path.isfile('/home/pi/front.png'):  # os.system('sudo chmod 777 ' + '/home/pi/front.png')
                        if os.path.isfile(ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'front.png'):
                            CmdCallResult = os.system('sudo rm ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'front.png')
                        os.system('sudo cp /home/pi/front.png ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'front.png')
                        CurrPitch_FullPath4 = ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'front.png'
                        CurrPitch_FullPath4 = str(CurrPitch_FullPath4)[23:100]
#01/05/19 htc                         CmdCallResult = os.system('sudo rm /home/pi/front.png')


                    CurrPitch_FullPath5 = 'FP5'
                    if os.path.isfile('/home/pi/side.png'):  # os.system('sudo chmod 777 ' + '/home/pi/front.png')
                        if os.path.isfile(ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'side.png'):
                            CmdCallResult = os.system('sudo rm ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'side.png')
                        os.system('sudo cp /home/pi/side.png ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'side.png')
                        CurrPitch_FullPath5 = ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'side.png'
                        CurrPitch_FullPath5 = str(CurrPitch_FullPath5)[23:100]
#01/05/19 htc                        CmdCallResult = os.system('sudo rm /home/pi/side.png')


                    CurrPitch_FullPath6 = 'FP6'
                    if os.path.isfile('/home/pi/top.png'):  # os.system('sudo chmod 777 ' + '/home/pi/front.png')
                        if os.path.isfile(ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'top.png'):
                            CmdCallResult = os.system('sudo rm ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'top.png')
                        os.system('sudo cp /home/pi/top.png ' + ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'top.png')
                        CurrPitch_FullPath6 = ThisSessionFolderName + '/' + str(CurrPitch_PitchNumber).zfill(3) + 'top.png'
                        CurrPitch_FullPath6 = str(CurrPitch_FullPath6)[23:100]
#01/05/19 htc                         CmdCallResult = os.system('sudo rm /home/pi/top.png')







#01/21/19 htc - SPECIAL MODIFICATION FOR TRF - Program is only displaying FIVE (5) .jpg/.png windows in the PHP pitch screen, quick fix for today.
                    # Bubble up the pitches, 3 to 2, 4 to 3, 5, to 4, 6 to 5 (sacrifice ONE of the critical frame shots to see ALL movememnt graphs).

                    CurrPitch_FullPath2 = CurrPitch_FullPath3
                    CurrPitch_FullPath3 = CurrPitch_FullPath4
                    CurrPitch_FullPath4 = CurrPitch_FullPath5
                    CurrPitch_FullPath5 = CurrPitch_FullPath6
                    CurrPitch_FullPath6 = ''








                    WriteOnePitchToLocalPitchTable()



#1/3/19 htc - added homerun check here too. (same logic as in WritePitch module.
 #                   if ThisSess_StandTargetGuid != 'SMV1-EARLYDEV' and gintSoundTopLeftY != 0 and gintSoundBottomRightY != 0:
 #                       if CurrPitch_ImpactXstr >= gstrSoundTopLeftX and CurrPitch_ImpactYint >= gintSoundTopLeftY:
 #                           if CurrPitch_ImpactXstr <= gstrSoundBottomRightX and CurrPitch_ImpactYint <= gintSoundBottomRightY:
 #                               MarqueeWord('HOME RUN', SM_Red)
 #                               ArtdmxToNDB()
 #                               print('HOME RUN - HOME RUN - HOME RUN')
 ##                               WriteLogFile('HOME RUN - HOME RUN - HOME RUN', 'Added debug line 1/3/19 htc     ')
  #                              time.sleep(4.9)



                    for EachFile in os.listdir(NetworkSharePath):
                        FileToRemoveFullPath = NetworkSharePath + '/' + EachFile
                        os.remove(FileToRemoveFullPath)


            if ReturnSpeedValue == 1:
                WriteLogFile('bad speed.txt file found - format problem, look at entry in log file.',
                                 '0030-RunStandardAndPracticeSession       -')

            if ReturnSpeedValue == 2:
                WriteLogFile('time-out occurred waiting for stop.txt or speed.txt, hard coded 10 minutes',
                             '0030-RunStandardAndPracticeSession       -')
                KeepProcessingPitches = False

            if ReturnSpeedValue == 3:
                WriteLogFile('stop.txt file found, ending program normally- reason: [' + ThisSess_ShutdownMode + '] ',
                             '0030-RunStandardAndPracticeSession       -')
                KeepProcessingPitches = False



#************************************************************************************************************************
#************************************************************************************************************************

def __main__():

    WriteLogFile('START OF MAIN in home folder: ' + cwd, '0001-Main                    -')   #writing this one to use Global Var smCurrentFunctionName.
    WriteLogFile('Python Script Runtime Arguments: ' + ThisPythonScriptName + ' - ' + str(sys.argv), '0001-Main                    -')   #writing this one to use Global Var smCurrentFunctionName.


    # 11/30/18 htc Startup timing debug statement - trying to find out what's causing startup delay.
    MainLogFileObject.writelines('Local Time: ' + time.strftime('%H:%M:%S', time.localtime()) + ' | Check Point 8 | ' + '\n')


    global SpeedFilePath
    global NetworkSharePath
    global StopFilePath
    global GlobalMachineID
    global ThisSess_MachineId

    #   SoundWaveToPlay = wave.open('c:\smartmitt\SoundFiles\GoCrazyFolksOzzieShort.wav', mode='rb')
  #  if platform.uname() == 'Windows':
  #      print('playing sound')
  #      winsound.PlaySound('c:\smartmitt\SoundFiles\GoCrazyFolksOzzieShort.wav', winsound.SND_ASYNC)
  #      print ('winsound.PlaySound(c:\smartmitt\SoundFiles\GoCrazyFolksOzzieShort.wav, winsound.SND_ASYNC)')
  #      print ('done playing sound')

    WriteLogFile(platform.uname()[0:80],'0001-Main                    -')
    WriteLogFile(platform.uname()[81:160],'0001-Main                    -')
    WriteLogFile(platform.uname(), '0001-Main                    -')

    #    input('Press return to write out 1260 file')   7/30/18 htc - left this here as example of input stmt.

    smartmitt_conn = mariadb.connect(user='smartmitt', password='smartmitt', database='smartmitt', host='localhost')
    cursor_machineid = smartmitt_conn.cursor()
    cursor_machineid.execute('SELECT UnitSerialNumber FROM smconfig WHERE ID = 1')
    row = cursor_machineid.fetchone()
    GlobalMachineID = row[0]
    ThisSess_MachineId = row[0]
    smartmitt_conn.close()
    gc.collect()
    WriteLogFile('Machine ID (UnitSerialNumber) from local smconfig table: ' + GlobalMachineID, '0001-Main -                   -')

    Build1260ArrayStucture()   #   create blank array
    MarqueeWord(GlobalMachineID, '')
    Write1260ArrayToArtnetFile() #   Write array to NdbArtNetCtrlString.txt file
    ArtdmxToNDB()   # play current NdbArtNetCtrlString.txt on disk in home folder to NDB/LED 10.0.0.100
 #   time.sleep(2.01)     #   wait one second to make sure it writes completely (probably not a problem!!)


#9/23/18 htc - exit if not session number passed in.
#10/23/18 htc - commented this out - run RunBootUpLedCheck() if no session passed in.
#    if RunThisSessionNumber == 0:
#       WriteLogFile(smMainVersion + ' - NO SESSION NUMBER OR ZERO SESSION NUMBER PASSED AS PARAMETER ONE- ENDING PROGRAM.' +
#                                 ' TZ:' + str(time.timezone) + '  GMT- ' + str(time.gmtime()),' INITIALIZAITION SECTION ')
#       gc.collect()
#       exit(999)

#    ClearTargetArea()

#    ClearMarqueeArea()

#    MarqueeWord(GlobalMachineID, '')
#    Write1260ArrayToArtnetFile() #   Write array to NdbArtNetCtrlString.txt file
#    ArtdmxToNDB()   # play current NdbArtNetCtrlString.txt on disk in home folder to NDB/LED 10.0.0.100

#  8/8/18 htc - call test routine to "exercise" the success/miss logic
#######################   TestRunSuccessMissLogic()
######################    sys.exit(0)


## 8/3/18 htc  - these worked so commented out, only APIs I need to do is Coach/Pract and PITCH UPLOAD,
##               Just using this "known" code as test to E.I. API connection in general.
##    api_url = 'https://www.easy-insight.com/app/reports/MBXGZApSwiCEKayGLfGS/basic.json?StudentEmail=' + 'thomasfrenz@gmail.com'
##    headers = {'Authorization': 'Basic Q3ZGRVhnbVBYbndlTlpzb21CaUQ6a25Kd0RKamVkUEhmT05oeWNRRGk='}
##    response = requests.get(api_url, headers=headers)
##    if response.status_code == 200:
##        return json.loads(response.content.decode('utf-8'))

#    headers = {'Authorization': 'TOK:<MY_TOKEN>'})
#strRespText = Trim(http.responseText)
#strRespStatus = Trim(http.Status)
#if strRespText = "[]" And strRespStatus = "200"
#if Len(Trim(strRespText)) > 10 AndstrRespStatus = "200" Then
#####           ParseUserLoginReturnString(Trim(strRespText))
#if Trim(gstrCurrStudentPassword) <> Trim(Me.txtPassword)
#if Trim(UCase(gstrCurrStudentActive)) <> "TRUE"
#Trim(UCase(gstrCurrStudentActive)) <> "YES"

# 8/29/18 htc - clean up files left over from previous runs, successful and aborted.
#    if os.path.isfile(SpeedFilePath):
#        os.remove(SpeedFilePath)
#    if os.path.isfile(StopFilePath):
#        os.remove(StopFilePath)


# 9/14/18 htc - just always clear out the entire NetworkShare folder contents.
    for EachFile in os.listdir(NetworkSharePath):
        FileToRemoveFullPath = NetworkSharePath + '/' + EachFile
        os.remove(FileToRemoveFullPath)

    global RunMode
    global RunThisSessionNumber


    # 11/30/18 htc Startup timing debug statement - trying to find out what's causing startup delay.
    MainLogFileObject.writelines('Local Time: ' + time.strftime('%H:%M:%S', time.localtime()) + ' | Check Point 9 | ' + '\n')


    if str(RunThisSessionNumber) > '0':

        # 11/30/18 htc Startup timing debug statement - trying to find out what's causing startup delay.
        MainLogFileObject.writelines('Local Time: ' + time.strftime('%H:%M:%S', time.localtime()) + ' | Check Point 10 | ' + '\n')


        WriteLogFile('Session Number PASSED TO PROGRAM: ' + RunThisSessionNumber , '   0001-Main -                   -')

        smartmitt_conn = mariadb.connect(user='smartmitt', password='smartmitt', database='smartmitt', host='127.0.0.1')
        cursor_session = smartmitt_conn.cursor()
        cursor_session.execute('SELECT * FROM sessions WHERE SeqSessionNumber = ' + str(RunThisSessionNumber))
##        cursor_session.execute('SELECT * FROM sessions WHERE id = ' + str(RunThisSessionNumber))
        row = cursor_session.fetchone()

        global ThisSess_CurrentStatus
        global ThisSess_Type
        global ThisSess_SystemOnLineYN
        global ThisSess_StudentDisplayName

        ThisSess_CurrentStatus = row[4]
        ThisSess_Type = row[5]
        ThisSess_SystemOnLineYN = row[18]
        ThisSess_StudentDisplayName = row[19]

        WriteLogFile('Session Number READ / id Returned: ' + str(row[3]) + ' / ' + str(row[0]) , '   0001-Main -                   -')

#9/23/18 htc - forced session number here for fix above with mixup with "id" field by Kris.
##        RunThisSessionNumber = row[3]


        smartmitt_conn.close()
        gc.collect()

        if str(ThisSess_Type).upper() == 'STANDARD' or str(ThisSess_Type).upper() == 'PRACTICE':
            RunStandardAndPracticeSession(RunThisSessionNumber)

 #       if str(ThisSess_Type).upper() == 'PRACTICE':
 #          RunPracticeSession(RunThisSessionNumber)

        ClearTargetArea()
        ClearMarqueeArea()

        MarqueeWord(ThisSess_ShutdownMode, '')
        Write1260ArrayToArtnetFile()  # Write array to NdbArtNetCtrlString.txt file
        ArtdmxToNDB()  # play current NdbArtNetCtrlString.txt on disk in home folder to NDB/LED 10.0.0.100

        time.sleep(5.10)

        MarqueeWord(GlobalMachineID, '')
        Write1260ArrayToArtnetFile() #   Write array to NdbArtNetCtrlString.txt file
        ArtdmxToNDB()   # play current NdbArtNetCtrlString.txt on disk in home folder to NDB/LED 10.0.0.100

        WriteLogFile('Session Number ' + RunThisSessionNumber + ' Ended with Status: ' + ThisSess_ShutdownMode, '0001-Main -                   -')

        smartmitt_conn.close()
        gc.collect()
        time.sleep(1.10)

        MainLogFileObject.close()

        if os.path.isfile(ThisSessionFolderName + '/MainLog.txt'):
            os.system('sudo rm ' + ThisSessionFolderName + '/MainLog.txt')
        if os.path.isfile('/var/www/html/students/MainLog.txt'):
            os.system('sudo cp ' + '/var/www/html/students/MainLog.txt ' + ThisSessionFolderName + '/a_MainLog' + RunThisSessionNumber + '.txt')


#10/30/18 htc - file maintenance for dispaly files shown on user's "start-up" device.
        # 10/30/18 htc - added copy of "latest" cam 1/2 snapshots to .jpg default display locations for PHP Pitch Log "5 boxes" to show cam views on "startup" of session.
        if os.path.isfile(PathForFilesToDisplayOnDevice + '/Cam1CriticalFrame.jpg'):
            os.system('sudo chmod 777 ' + PathForFilesToDisplayOnDevice + '/Cam1CriticalFrame.jpg')
            os.system('sudo rm ' + PathForFilesToDisplayOnDevice + '/Cam1CriticalFrame.jpg')
        if os.path.isfile(PathForFilesToDisplayOnDevice + '/Cam2CriticalFrame.jpg'):
            os.system('sudo chmod 777 ' + PathForFilesToDisplayOnDevice + '/Cam2CriticalFrame.jpg')
            os.system('sudo rm ' + PathForFilesToDisplayOnDevice + '/Cam2CriticalFrame.jpg')
        if os.path.isfile(PathForFilesToDisplayOnDevice + '/Impact.jpg'):
            os.system('sudo chmod 777 ' + PathForFilesToDisplayOnDevice + '/Impact.jpg')
            os.system('sudo rm ' + PathForFilesToDisplayOnDevice + '/Impact.jpg')

        #10/30/18 htc - might as well re-copy these files here - ??????????
        if os.path.isfile('/home/pi/SmartMittLogoForInternalPgmDisplay.jpg'):
            CommandToCall = 'cp ' + '/home/pi/SmartMittLogoForInternalPgmDisplay.jpg ' + PathForFilesToDisplayOnDevice + '/Impact.jpg'
            CmdCallResult = os.system(CommandToCall)
        if os.path.isfile('/home/pi/Cam1-bg.png'):
            CommandToCall = 'cp ' + '/home/pi/Cam1-bg.png ' + PathForFilesToDisplayOnDevice + '/Cam1CriticalFrame.jpg'
            CmdCallResult = os.system(CommandToCall)
        if os.path.isfile('/home/pi/Cam2-bg.png'):
            CommandToCall = 'cp ' + '/home/pi/Cam2-bg.png ' + PathForFilesToDisplayOnDevice + '/Cam2CriticalFrame.jpg'
            CmdCallResult = os.system(CommandToCall)


        sys.exit(0)

    else:
        RunBootUpLedCheck()
        sys.exit(777)

__main__()

