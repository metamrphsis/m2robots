#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import M2StemController
import signal
import time,datetime
import CONST
from IPython.utils import _process_win32_controller

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
    
bUseCallBack = True #True False, choose to use callback or explicit read request for telemetry data retrieval
#controller = M2StemController.BleCtrller("",callbackfunc)
if bUseCallBack:
    controller = M2StemController.BleCtrller(callbackfunc)
else:
    controller = M2StemController.BleCtrller(None)

controller.connect() # 建立硬件连接
controller.saveCurrIMUfRPYdeg() # 保存当前门所在角度，作为比较基准
while True:
    if controller.getMaxAbsErrFromSavedIMUfRPYdeg() > 30: # 家里没人，门打开超过30度，执行下面的操作
        #发短信，电话号码13013013013，短信内容：年-月-日-小时-分-秒 门开
        controller.send_a_SMS("13013013013",'door opened at {date:%Y/%m/%d/%H:%M:%S}'.format(date=datetime.datetime.now()))
    time.sleep(0.5) # 每半秒钟检查一次

    if requestExit:
        controller.stop()
        break


