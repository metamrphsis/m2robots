#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# the spider will make relative turning angles based on its current orientation and left/right turn command
import signal
import time
from m2controller import m2controller
from m2controller import m2Const
import usrCfg

requestExit = False
def signal_handler(sig, frame):
    global requestExit
    print('user Ctrl-C')
    requestExit = True

signal.signal(signal.SIGINT, signal_handler)

def callbackfunc(bytedata):
    pass
    
def stopEverything():
    controller.motorHbridgeCtrl_pm1(CONST.spiderPWMchSteer,0.0)
    controller.motorHbridgeCtrl_pm1(CONST.spiderPWMchSpeed,0.0)
    controller.SendCmdTransBlking(False)
    print("stopEverything")

def goStraight_thr_pm1(thr_pm1):
    controller.motorHbridgeCtrl_pm1(CONST.spiderPWMchSteer,0)
    controller.motorHbridgeCtrl_pm1(CONST.spiderPWMchSpeed,thr_pm1)
    controller.SendCmdTransBlking(False)
    print("goStraight_thr_pm1%f"%thr_pm1)
    
def steer_pm1(steering_pm1):
    controller.motorHbridgeCtrl_pm1(CONST.spiderPWMchSteer,steering_pm1)
    controller.motorHbridgeCtrl_pm1(CONST.spiderPWMchSpeed,0)
    controller.SendCmdTransBlking(False)
    print("steering_pm1:%f"%steering_pm1)

m_iDanceStepii = 0

def turnCrank():
    global m_iDanceStepii
    if m_iDanceStepii == 0:
        stopEverything()
        danceStepDurationS = 1.0
    elif m_iDanceStepii == 1:
        goStraight_thr_pm1(0.6)
        danceStepDurationS = 2.0
    elif m_iDanceStepii == 2:    
        steer_pm1(0.6)
        danceStepDurationS = 3.0
    elif m_iDanceStepii == 3:    
        goStraight_thr_pm1(0.4)
        danceStepDurationS = 2.0
    elif m_iDanceStepii == 4:    
        steer_pm1(-0.6)
        danceStepDurationS = 1.0
    elif m_iDanceStepii == 5:    
        goStraight_thr_pm1(0.4)
        danceStepDurationS = 2.0
    elif m_iDanceStepii == 6:    
        steer_pm1(0.6)
        danceStepDurationS = 3.0
    elif m_iDanceStepii == 7:    
        goStraight_thr_pm1(0.4)
        danceStepDurationS = 2.0
    elif m_iDanceStepii == 8:    
        steer_pm1(-0.6)
        danceStepDurationS = 1.0
    elif m_iDanceStepii == 9:    
        goStraight_thr_pm1(-0.4)
        danceStepDurationS = 2.0
    else:
        stopEverything()
        return True

    if controller.secSinceTime0() > danceStepDurationS:
        m_iDanceStepii += 1
        controller.setTime0()
        
    return False

def sanityCheck():
    if usrCfg.ctrlType == CONST.etInternet or usrCfg.ctrlType == CONST.etAndroid or usrCfg.ctrlType == CONST.etLocalNet:
        # TODO:
        return False
    hardware_settings = controller.readSettingData()
    if (not hardware_settings['CH0dutyCycleMode']):
        return True
    if (not hardware_settings['CH1dutyCycleMode']):
        return True
    if (not hardware_settings['CH2dutyCycleMode']):
        return True
    if (not hardware_settings['CH3dutyCycleMode']):
        return True
    if (not hardware_settings['CH01_merged2be_H_bridge']):
        return True
    if (not hardware_settings['CH23_merged2be_H_bridge']):
        return True
    return False
    
controller = m2controller.BleCtrller(callbackfunc)
    
controller.connect()
if sanityCheck():
    print("controller HW setting error")
    quit() 

controller.setTime0()

while True:
    time.sleep(0.2)
    if turnCrank():
        break
    if requestExit:
        break
controller.m_app2pyListeningServer.request_exit()    

