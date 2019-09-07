#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# the plane will deploy its payload by activating a servo after it senses a left/left/right/right sequence of roll maneuver

from m2controller import m2controller
from m2controller import m2Const
import signal
import time
bUseCallBack = False #True False, choose to use callback or explicit read request fosetLighteningStepr telemetry data retrieval

def setLighteningStep(DurationS,R0=-1.0,G0=-1.0,B0=-1.0,R1=-1.0,G1=-1.0,B1=-1.0):
    return {'DurationS':DurationS,'R0':R0,'G0':G0,'B0':B0,'R1':R1,'G1':G1,'B1':B1}

CloudsSeq = []
CloudsSeq.append(setLighteningStep(1.0))
CloudsSeq.append(setLighteningStep(1.0, 1.0,-1.0,-1.0,-1.0,-1.0,-1.0))
CloudsSeq.append(setLighteningStep(1.0, 0.5,-1.0,-1.0,-1.0,-1.0,-1.0))
CloudsSeq.append(setLighteningStep(1.0, 0.0,-1.0,-1.0,-1.0,-1.0,-1.0))
CloudsSeq.append(setLighteningStep(1.0, -0.5,-1.0,-1.0,-1.0,-1.0,-1.0))
CloudsSeq.append(setLighteningStep(1.0, -1.0,-1.0,-1.0,-1.0,-1.0,-1.0))
CloudsSeq.append(setLighteningStep(2))
CloudsSeq.append(setLighteningStep(1.0, 1.0,-1.0,-1.0,-1.0,1.0,-1.0))
CloudsSeq.append(setLighteningStep(1.0, 0.5,-1.0,-1.0,-1.0,0.5,-1.0))
CloudsSeq.append(setLighteningStep(1.0, -1.0,-1.0,-1.0,-1.0,-1.0,-1.0))
CloudsSeq.append(setLighteningStep(1.0, -0.5,-1.0,-1.0,-1.0,-0.5,-1.0))
CloudsSeq.append(setLighteningStep(1.0, -1.0,-1.0,-1.0,-1.0,-1.0,-1.0))

requestExit = False
def signal_handler(sig, frame):
    global requestExit
    print('user Ctrl-C')
    requestExit = True

signal.signal(signal.SIGINT, signal_handler)

def sanityCheck():
    hardware_settings = controller.readSettingData()
    if (not hardware_settings['CH0dutyCycleMode']):
        return True
    if (not hardware_settings['CH1dutyCycleMode']):
        return True
    if (not hardware_settings['CH2dutyCycleMode']):
        return True
    if (not hardware_settings['CH3dutyCycleMode']):
        return True
    if (not hardware_settings['CH4dutyCycleMode']):
        return True
    if (not hardware_settings['CH5dutyCycleMode']):
        return True
    return False
    
controller = m2controller.BleCtrller(None)
controller.connect()
if sanityCheck():
    print("controller HW setting error")
else:
    controller.playMP3file("./resources/thundersoundeffect.ogg",True)
    for danceStepii in range(len(CloudsSeq)):
        controller.setTime0()
        print("sequence step[%d]"%danceStepii)
        currentCloudSetting = CloudsSeq[danceStepii] 
        controller.setPWM_n_pm1(0,currentCloudSetting['R0'])
        controller.setPWM_n_pm1(1,currentCloudSetting['G0'])
        controller.setPWM_n_pm1(2,currentCloudSetting['B0'])
        controller.setPWM_n_pm1(3,currentCloudSetting['R1'])
        controller.setPWM_n_pm1(4,currentCloudSetting['G1'])
        controller.setPWM_n_pm1(5,currentCloudSetting['B1'])
        controller.SendCmdTransBlking()
        while True:
            if controller.secSinceTime0() > currentCloudSetting['DurationS'] or requestExit:
                break
            else:
                time.sleep(0.1)


