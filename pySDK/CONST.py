#!/usr/bin/env python
# -*- coding: UTF-8 -*-
USR_GPIO_CNT = 8
USR_BTN_CNT = 6
RcPWMchanNum = 6

GPIOgroupCntStepMotor = 2

FC_CTRL_BLE_MSGTYPE_LEN = 2
etRoll_PwmCH = 0
etPitchPwmCH = 1
etThrotPwmCH = 2
etRudd_PwmCH = 3
etAUX1_PwmCH = 4
etAUX2_PwmCH = 5
etFlightModeCH = 6
etAUX4_CH = 7
etAUX5_CH = 8
etAUX6_CH = 9
etAUX7_CH = 10
etGPIO_CTRL_BYTE = 11

CHAR3_BYTE_LEN = 20
StepMotorCnt = 2

FC_STATUS_LEN = 20
FC_STATUS_EACH_AXIS_BYTE = 5
RPY_floatIntConversion = 2
LSB_DROP_ACC = 5
ACC_DYNAMIC_FS_RNG = 2.0 # // g. MPU6050_ACCEL_FS_2: \pm 2G
LSB_DROP_GYR = 0
GYRO_DYNAMIC_FS_RNG = 2000.0 # // deg/sec
LSB_DROP_MAG = 0
LSBcountPerGauss = 1024 # earth field: 0.25 to 0.65 gauss
ByteIndex0Seq_n_Btn = 15
ByteIndex0ADC1_1tenthV = 16
ByteIndex0Compass = 17
ByteIndex0Tmpture = 18


MinMsIntervalForInternetCtrl = 500 # if py2app cmd update rate is faster than this duration, app may experience packet loss 
readApp2pyDataInterval_ms = 500
strApp2pyCmdFilename = "app2pyCmd"  
strPy2appJsonCmdFilename = "py2appJsonCmd"  

etAndroid = "android"
etDebian = "Debian"
etInternet = "mqtt"
etLocalNet = "LocalNet"

platformTypes = [etAndroid,etDebian,etInternet,etLocalNet]

TOPIC_APP_INTERNET_MQTT_CTRL = "INTERNET_CTRL"
TOPIC_APP_INTERNET_MQTT_MetaCtrl = "INTERNET_META_CTRL"
strREQUEST_Telemetry = "requestTelemetry"; # in order to save internet traffic, we may turn off the Char4 notification, and request it as needed
TOPIC_APP_INTERNET_Char4_TELEMETRY = "INTERNET_TELEMETRY"
MinMsIntervalApp2SDKnotification = 500;

stepMotorRollIndex = 0
stepMotorPitchIndex = 1

socketServerPORT_pyPrintWindow = 28090
socketServerPORT_SDKpy2app = 28091 # app as server
socketServerPORT_SDKapp2py = 28092 # app as client

spiderPWMchSpeed = 1
spiderPWMchSteer = 0










