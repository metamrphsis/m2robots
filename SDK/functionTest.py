#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import M2StemController
import signal
import time
import CONST
import usrCfg
import ConstSharedAppSdk

requestExit = False

def signal_handler(sig, frame):
    global requestExit
    print('user Ctrl-C')
    requestExit = True
    
signal.signal(signal.SIGINT, signal_handler)

def callbackfunc(telemetry):
    if telemetry['m_BtnStatus'][0] == 0:
        TouchEvent = 0
    else:
        TouchEvent = 1
    iCompass_pm180deg = telemetry['m_iCompass_pm180deg']
    IMUyawDeg = telemetry['m_fRPYdeg'][2]
    print("User handler: TouchEvent=%d,Compass=%2.1f(Deg),yaw=%2.1f(Deg)"%(TouchEvent,iCompass_pm180deg,IMUyawDeg))
    
######################################
controller = M2StemController.BleCtrller("",callbackfunc)
#controller = M2StemController.BleCtrller(usrCfg.BleMACaddress,callbackfunc)
#controller = M2StemController.BleCtrller(usrCfg.BleMACaddress)
#controller = M2StemController.BleCtrller("")
######################################

controller.connect()
while True:
    controller.set_wallpaper(ConstSharedAppSdk.emoPic_smile)
    controller.SendCmdTransBlking()
    time.sleep(1)
    print("done")
    break
    
    controller.clearPreviousCmd()
    #controller.send_a_SMS("14086665581", "helloworld")
    #controller.take_a_photo("myphoto.jpg")
    for ii in range(CONST.USR_GPIO_CNT):
        controller.setGPIOn(ii)
    for ii in range(CONST.RcPWMchanNum):
        controller.setPWM_n_pm1(ii,0.7)
    controller.SendCmdTransBlking()
    
    if controller.getPlatformType() == CONST.etInternet:
        Telemetry = controller.getInternetTelemetry()
        if Telemetry is not None:
            print(Telemetry)
            
    controller.requestInternetTelemetry()    
    time.sleep(1)
    for ii in range(CONST.USR_GPIO_CNT):
        controller.resetGPIOn(ii)
    for ii in range(CONST.RcPWMchanNum):
        controller.setPWM_n_pm1(ii,-0.7)
    controller.SendCmdTransBlking()
    time.sleep(1)

    if requestExit:
        controller.stop()
        break


