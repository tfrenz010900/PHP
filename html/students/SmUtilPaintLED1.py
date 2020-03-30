# Copyright 2019, Looking Glass Applications, LLC, All Rights Reserved.
#  Author:  Tim Crosno
#  Date Created:  06-24-19
#  Last Update:  06-24-19
#  Python 3.5 on Debian Stretch with MariaDB (MySQL)
#
#
#
#import argparse      #7/25/18 htc - from Terry's (UK) file player utility (artdmx_Script.py)
import binascii     #7/25/18 htc - from Terry's (UK) file player utility (artdmx_Script.py)
import logging      #7/25/18 htc - from Terry's (UK) file player utility (artdmx_Script.py)
import os           #7/25/18 htc - from Terry's (UK) file player utility (artdmx_Script.py)
import socket       #7/25/18 htc - from Terry's (UK) file player utility (artdmx_Script.py)
import struct       #7/25/18 htc - from Terry's (UK) file player utility (artdmx_Script.py)
import sys          #7/25/18 htc - from Terry's (UK) file player utility (artdmx_Script.py)
import time      #7/25/18 - used for time delays and log file timestamps, accurate to 100th second (maybe better??)
import datetime   #8/25/18 htc - used for date time delays
import gc     #8/25/18 htc - found in google post to keep database connections cleaner from open/close a lot.
import argparse
import io
import numpy as np
from PIL import Image
import subprocess

global GlobalMachineID
GlobalMachineID = 'Machine ID NOT SET'


global smMainVersion
smMainVersion = '__SmUtilLED1.py'


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




#---------------------------------   END OF GLOBAL SECTION ---------------------------------------------------------------


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


    if strColor6BytesIn < "000000":
        strColor6BytesIn = "f0f0f0"

    ClearMarqueeArea()

    intLen = len(WordToDisplay)

#11/29/18 htc Marquee is only EIGHT characters long - chars on end (9+) "bunch Up" and make display look goofy.
    if intLen > 8:
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





def SeqLightNo(Xin, Yin):

    for intIX in range(1, 781):  # loops 1 to 780
        if LedArray1260ColNum[intIX] == Xin:
            if LedArray1260RowNum[intIX] == Yin:
                return LedArray1260SeqNo[intIX]






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



def __main__():

    x = input('Press Enter To Display Image on LED.')

    Build1260ArrayStucture()   #   create blank array
    MarqueeWord( 'LED TEST','')
    Write1260ArrayToArtnetFile() #   Write array to NdbArtNetCtrlString.txt file
    ArtdmxToNDB()   # play current NdbArtNetCtrlString.txt on disk in home folder to NDB/LED 10.0.0.100

#    ClearTargetArea()

#    ClearMarqueeArea()

#    gc.collect()

 #   def BuildSelectedBaseTargetArrayForThisRun(TargetToDefine, strX1, intY1, strX2, intY2):

#        global CurrentTargetName
#        CurrentTargetName = TargetToDefine

        # Clear the 1260 array and actually build the target in there (That's the list storage array "paint box" works on/in).
    ClearTargetArea()

        # 8/3/18 htc - now Find the target def for this session that was passed to this routine. (should have read from SESSION RECORD).
#        if TargetToDefine == 'SMV1-EARLYDEV' or TargetToDefine == 'EarlyDev' or TargetToDefine == 'EarlyDevelopment' or TargetToDefine == 'Early Development':
    PaintThisBox(SM_Green, 9, 9, 22, 22)

    PaintThisBox(SM_Red_Med, 25, 1, 27, 1)
    PaintThisBox(SM_Red_Med, 25, 2, 27, 2)
    PaintThisBox(SM_Red_Med, 23, 3, 27, 3)

    PaintThisBox(SM_Yellow_Med, 24, 4, 25, 4)
    PaintThisBox(SM_Red_Med, 26, 4, 27, 4)

    PaintThisBox(SM_Yellow_Med, 24, 5, 25, 5)
    PaintThisBox(SM_Red_Med, 27, 5, 27, 5)

    PaintThisBox(SM_Yellow_Med, 24, 6, 24, 6)
    PaintThisBox(SM_Red_Med, 25, 6, 26, 6)

    PaintThisBox(SM_Red_Med, 24, 7, 24, 7)
    PaintThisBox(SM_Yellow_Med, 25, 7, 25, 7)

    PaintThisBox(SM_Red_Med, 23, 8, 23, 8)
    PaintThisBox(SM_Blue_Med, 24, 8, 26, 8)

    PaintThisBox(SM_Yellow_Med, 24, 9, 25, 9)
    PaintThisBox(SM_Blue_Med, 26, 9, 26, 9)

    PaintThisBox(SM_Yellow_Med, 23, 10, 24, 10)
    PaintThisBox(SM_Blue_Med, 25, 10, 26, 10)

    PaintThisBox(SM_Yellow_Med, 23, 11, 23, 11)
    PaintThisBox(SM_Blue_Med, 24, 11, 26, 11)

    PaintThisBox(SM_Blue_Med, 24, 12, 26, 12)

    PaintThisBox(SM_Blue_Med, 24, 13, 26, 13)

    PaintThisBox(SM_Blue_Med, 24, 14, 26, 15)

    PaintThisBox(SM_Red_Med, 24, 15, 26, 15)

    PaintThisBox(SM_Blue_Med, 24, 16, 26, 16)

    PaintThisBox(SM_Blue_Med, 24, 17, 26, 17)

    PaintThisBox(SM_Blue_Med, 24, 18, 26, 18)

    PaintThisBox(SM_Blue_Med, 24, 19, 26, 19)

    PaintThisBox(SM_Blue_Med, 24, 20, 26, 20)

    PaintThisBox(SM_Blue_Med, 25, 21, 26, 21)

    PaintThisBox(SM_Blue_Med, 25, 22, 26, 22)

    PaintThisBox(SM_Yellow_Med, 25, 23, 26, 23)

    PaintThisBox(SM_Yellow_Med, 25, 24, 26, 24)

    PaintThisBox(SM_Yellow_Med, 25, 25, 26, 25)

    PaintThisBox(SM_Yellow_Med, 25, 26, 26, 26)

#    PaintThisBox(SM_Red_Med, 23, 25, 26, 25)


#        if TargetToDefine == 'SMV1-ED-R' or TargetToDefine == 'EarlyDevRiver' or TargetToDefine == 'EarlyDevelopmentRiver' or TargetToDefine == 'Early Development with River':
#            PaintThisBox(SM_Yellow, 6, 6, 25, 25)  # River box
#            PaintThisBox(SM_Off, 7, 7, 24, 24)  # Clear interior of River
#            PaintThisBox(SM_Green, 9, 9, 22, 22)  # Paint in ED strike zone


#   print(strImpactInfo)


    Write1260ArrayToArtnetFile()
    ArtdmxToNDB()

    # 9/24/18 htc - make two copies of Impact.jpg - one for PHP to display in "students" folder, One for archive with pit
    # ORIGINAL - "HOME" FOLDER.    ArtnetTxtToJpg('NdbArtNetCtrlString.txt', 'Impact.jpg', width=300)

    #    WriteLogFile('Attempting to create this file from (NdbArtNetCtrlString.txt) in home folder: [' + NetworkSharePath + '/Impact.jpg' ']', '0071-DisplayImpactLocation              -')

    ArtnetTxtToJpg('NdbArtNetCtrlString.txt', NetworkSharePath + '/TestDisplayJune2019.jpg', width=300)

    gc.collect()

    time.sleep(1.10)

    x = input('Press Enter Exit Program - image will remain on LED Panel')

    sys.exit(0)


#        RunBootUpLedCheck()
#        sys.exit(777)

__main__()

