#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 2-axis orthogonal step motor platform, carrying petri-dish.
# image captured by mobile phone equipped with external microscopic lens.
# multiple images stitched by python script.

from m2controller import m2controller
from m2controller import m2Const
import signal
import time
import usrCfg
import sys
import datetime

waitSecStepperMove = 1
waitSecPhoto = 2
requestExit = False
def signal_handler(sig, frame):
    global requestExit
    print('user Ctrl-C')
    requestExit = True

signal.signal(signal.SIGINT, signal_handler)

def sanityCheck():
    return False

def callbackfunc(telemetry):
    pass

iPhotoIndex = 0
photofilenamePreamble = 'Test{date:%Y-%m-%d-%H_%M_%S}'.format(date=datetime.datetime.now())
def getPhotoFileName():
    global iPhotoIndex
    global photofilenamePreamble
    photoFilename = "%s(%d).jpg"%(photofilenamePreamble,iPhotoIndex)
    iPhotoIndex += 1
    print("take photo with name:%s"%photoFilename)
    return photoFilename

iLoopCnt = 0
iSMstep = 0
iSMsubstep = 0
def move2nextSMstate():
    global iSMstep,iSMsubstep
    iSMstep += 1
    iSMsubstep = 0

if usrCfg.ctrlType != CONST.etAndroid and usrCfg.ctrlType != CONST.etInternet:
    print("microscope needs phone camera to take sample images for further computer vision processing")
    sys.exit()
controller = m2controller.BleCtrller("",callbackfunc)
#controller = m2controller.BleCtrller(usrCfg.BleMACaddress,callbackfunc)
    
controller.connect()
if sanityCheck():
    print("controller HW setting error")
else:
    while True:
        if requestExit:
            controller.stop()
            break
        iLoopCnt += 1
        if iLoopCnt == 50:
            break
        print("step(%d,%d)"%(iSMstep,iSMsubstep))
        controller.setSeqID(iSMstep)
        if iSMstep == 0:
            time.sleep(0.5)
            move2nextSMstate()
        elif iSMstep == 1:
            if iSMsubstep < 3:
                controller.moveStepper_n(CONST.stepMotorRollIndex, -128)
                controller.SendCmdTransBlking(False)
                iSMsubstep += 1
                time.sleep(waitSecStepperMove)
            else:
                move2nextSMstate()
        elif iSMstep == 2:
            if iSMsubstep < 3:
                controller.moveStepper_n(CONST.stepMotorPitchIndex, -128)
                controller.SendCmdTransBlking(False)
                iSMsubstep += 1
                time.sleep(waitSecStepperMove)
            else:
                move2nextSMstate()
        elif iSMstep == 3:
            controller.take_a_photo(getPhotoFileName())
            controller.SendCmdTransBlking(False)
            time.sleep(waitSecPhoto)
            move2nextSMstate()
        elif iSMstep == 4:
            controller.moveStepper_n(CONST.stepMotorRollIndex, 127)
            time.sleep(waitSecStepperMove)
            controller.take_a_photo(getPhotoFileName())
            controller.SendCmdTransBlking(False)
            time.sleep(waitSecPhoto)
            move2nextSMstate()
        elif iSMstep == 5:
            controller.moveStepper_n(CONST.stepMotorPitchIndex, 127)
            time.sleep(waitSecStepperMove)
            controller.take_a_photo(getPhotoFileName())
            controller.SendCmdTransBlking(False)
            time.sleep(waitSecPhoto)
            move2nextSMstate()
        elif iSMstep == 6:
            controller.moveStepper_n(CONST.stepMotorRollIndex, -127)
            time.sleep(waitSecStepperMove)
            controller.take_a_photo(getPhotoFileName())
            controller.SendCmdTransBlking(False)
            time.sleep(waitSecPhoto)
            move2nextSMstate()
        elif iSMstep >= 7:
            print("congratulations, data collection campaign completed!")
            controller.stop()
            break;
                
        
        
