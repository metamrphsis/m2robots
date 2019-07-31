#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# the plant is watered at programmable time and amount. Group study of the same plant growth rate is an interesting topic

import M2StemController
import signal
import time
import datetime
import usrCfg

def get_iSecondSinceMidNight():
    now = datetime.datetime.now()
    return round((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())

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
    if (hardware_settings['CH01_merged2be_H_bridge']):
        return True
    return False

def callbackfunc(telemetry):
    pass

bUseCallBack = False #True False, choose to use callback or explicit read request for telemetry data retrieval
#controller = M2StemController.BleCtrller("",callbackfunc)
if bUseCallBack:
    controller = M2StemController.BleCtrller(usrCfg.BleMACaddress,callbackfunc) # 配置使用回调函数
else:
    controller = M2StemController.BleCtrller(usrCfg.BleMACaddress,None)
    
controller.connect() # 建立硬件连接
if sanityCheck():    # 硬件自检，确认配置符合硬件用途
    print("controller HW setting error 控制器硬件配置错误")
else:
    iSecond = 0 # 系统计时
    while True:
        if requestExit: 
            break  # 用户通过Ctrl-C停止程序的执行
        Sec = get_iSecondSinceMidNight() # 得到从凌晨0点0分到当前时间的时长，(秒)
        if (Sec > 8*3600 and Sec < 8*3600+100) or (Sec > 17*3600 and Sec < 17*3600+100): #早晨8点开始100秒，下午5点开始100秒，执行下面的操作
            controller.setPWM_n_pm1(0,1) #执行机构动作，打开浇水阀门
        else:
            controller.setPWM_n_pm1(0,0) #不在这个时间段，执行机构动作，关闭浇水阀门
        time.sleep(1) # 每秒钟检查一次状态
        iSecond += 1
        if (iSecond%60) == 0: # 每分钟执行下面的动作：
            photofilename = 'photo-{date:%Y-%m-%d-%H_%M_%S}.jpg'.format(date=datetime.datetime.now())
            controller.take_a_photo(photofilename) #拍照，照片命名的格式是photo-年-月-日-小时-分-秒.jpg
        
