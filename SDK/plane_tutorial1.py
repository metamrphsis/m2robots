#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# the plane will deploy its payload by activating a servo after it senses a left/left/right/right sequence of roll maneuver

import M2StemController, CONST
import signal
import time
import usrCfg

bUseCallBack = False #True False
CurrStatus = 'working' # 'working','failure','done'

expectedSequence = ['initialization','level','left','level','left','level','right','level','right','level'];
iiCurrStep = 0
requestExit = False
maneuver = expectedSequence[0]

def signal_handler(sig, frame):
    global requestExit
    print('user Ctrl-C')
    requestExit = True
    
signal.signal(signal.SIGINT, signal_handler)

def callbackfunc(telemetry):
    global maneuver
    fIMUrollDeg = telemetry['m_fRPYdeg'][0]
    if abs(fIMUrollDeg) < 20.0:
        maneuver = 'level'
    else:
        if fIMUrollDeg < 0.0:
            maneuver = 'left'
        else:
            maneuver = 'right'
    print("currently we are in maneuver %s, completed %d step(s), status: %s"%(maneuver,iiCurrStep,CurrStatus))
    
bUseCallBack = True #True False, choose to use callback or explicit read request for telemetry data retrieval
#controller = M2StemController.BleCtrller(CONST.etAndroid,"",callbackfunc)
if bUseCallBack:
    controller = M2StemController.BleCtrller(CONST.etDebian,usrCfg.BleMACaddress,callbackfunc)
else:
    controller = M2StemController.BleCtrller(CONST.etDebian,usrCfg.BleMACaddress,None)

controller.connect()

def checkSeqStatus():
    global iiCurrStep
    global maneuver
    global CurrStatus
    print("maneuver=%s"%maneuver)    
    if iiCurrStep == len(expectedSequence)-1:
        CurrStatus =  'done'
    else:
        if iiCurrStep == 0:
            if maneuver == expectedSequence[iiCurrStep+1]:
                print("one step successfully completed")
                iiCurrStep += 1
        else:
            if maneuver == expectedSequence[iiCurrStep]:
                pass
            elif maneuver == expectedSequence[iiCurrStep+1]:
                print("one step successfully completed")
                iiCurrStep += 1
            else:
                print("at step %d, pattern violated, failure :-("%iiCurrStep)
                CurrStatus = 'failure'
   
while True:
    if bUseCallBack:
        controller.check4Notifications()
    else:
        callbackfunc(controller.readTelemetryData())
        
    if CurrStatus == 'failure':
        for ii in range(CONST.USR_GPIO_CNT):
            controller.setGPIOn(ii)
        controller.SendCmdTransBlking()    
        break
    elif CurrStatus == 'done':
        print("Congratulation, mission accomplished")
        controller.clearPreviousCmd()
        controller.setPWM_n_pm1(0,1.0)
        controller.SendCmdTransBlking()
        break
    else:
        checkSeqStatus()
            
    if requestExit:
        controller.stop()
        break

time.sleep(3)

