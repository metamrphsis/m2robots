#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import usrCfg
import CONST
import ConstSharedAppSdk
if usrCfg.ctrlType == CONST.etDebian:
    from bluepy import btle
    import pygame
import time
import app2py_sharedFileDecoder
import bleDataDecoder
import ctypes
from app2pyListeningServer import app2pyListeningServer
import socket
import sys
import json
#from collections import deque
#try:
#    from Queue import Queue
#except:
#    from queue import Queue
from queue import Queue
if usrCfg.ctrlType == CONST.etInternet:
    import mqttutils

def servo_pm1ctrl_to_i8(pm1Val):
    if pm1Val > 1.0:
        pm1Val = 1.0
    if pm1Val < -1.0:
        pm1Val = -1.0
    val = round(pm1Val*127)
    if val > 127:
        val = 127
    if val < -127:
        val = -127
    return round(val)

def getMs():
    return int(round(time.time() * 1000))

def normalizeAngleTo_pm180deg(angleDeg):
    while angleDeg > 180:
        angleDeg -= 360
    while angleDeg < -180:
        angleDeg += 360
    return angleDeg

class BleCtrller:
    def __init__(self, platform, callback=None):
        self.errorStatus = False
        if platform not in CONST.platformTypes:
            self.errorStatus = True
            return
        self.m_platform = platform
        self.m_CommsTunnel = "" # etAndroid: socket; etDebian: Bluepy; etInternet: mqtt
        self.m_app2pyListeningServer = None
        self.hService = ""
        self.char1 = ""
        self.char3 = ""
        self.char4 = ""
        self.callback = callback
        self.m_setting = None
        self.m_DictTelemetry = None
        self.requestExit = False
        # cmd python=>app/BLEdevice
        self.cmd_MP3PLAY = None
        self.cmd_SENDSMS = None
        self.cmd_TAKEPHOTO = None
        self.cmd_SetWallpaper = None
        self.cmd_u8GPIO = None
        self.cmd_u8SeqID = None
        self.cmd_i8StepperMovCnt = None
        self.GPIO_beingUsed = 0
        self.cmd_i8AarrServos = None
        self.Servo_beingUsed = 0
        self.LastCmdSentTimeMs = getMs()
        self.baLastBLEbinaryPkt = None
        self.clearPreviousCmd()
        self.m_startTimeS = None
        self.m_savedAzimuthIMUpm180deg = None
        self.m_mqttQueue = None
        self.m_bPygame_mixer_init_done = False

    #def signal_handler(self, sig, frame):
    #    self.requestExit = True
        
    #return True if system in Error
    def chkSafeStatus(self):
        if self.errorStatus:
            print ("system in error, return")
            return True
        else:
            return False
    
    def getPlatformType(self):
        return self.m_platform
    
    def saveCurrAzimuthIMU(self):
        if self.m_DictTelemetry is None:
            print("no telemetry estimate available, maybe BLE not connected?")
        self.m_savedAzimuthIMUpm180deg = self.m_DictTelemetry['m_fRPYdeg'][2]

    def saveCurrIMUfRPYdeg(self):
        if self.m_DictTelemetry is None:
            print("no telemetry estimate available, maybe BLE not connected?")
        self.m_savedIMUfRPYdeg = self.m_DictTelemetry['m_fRPYdeg']
    
    def getErrFromSavedAzimuth(self):
        if self.m_DictTelemetry is None:
            print("no telemetry estimate available, maybe BLE not connected?")
            return None
        if self.m_savedAzimuthIMUpm180deg is None:
            print("no referenece azimuth set by function saveCurrAzimuthIMU")
            return None
        ErrDeg = self.m_DictTelemetry['m_fRPYdeg'][2] - self.m_savedAzimuthIMUpm180deg
        return normalizeAngleTo_pm180deg(ErrDeg) 

    def getErrFromSavedIMUfRPYdeg(self):
        res = [];
        for ii in range(3):
            res.append(self.m_DictTelemetry['m_fRPYdeg'][ii]-self.m_savedIMUfRPYdeg[ii])
        return res
        
    def getAbsErrFromSavedAzimuth(self):
        return abs(self.getErrFromSavedAzimuth())

    def getAbsErrFromSavedIMUfRPYdeg(self):
        res = [];
        for ii in range(3):
            res.append(abs(self.m_DictTelemetry['m_fRPYdeg'][ii]-self.m_savedIMUfRPYdeg[ii]))
        return res
    
    def getMaxAbsErrFromSavedIMUfRPYdeg(self):
        return max(self.getAbsErrFromSavedIMUfRPYdeg())
        
    def stop(self):
        self.requestExit = True
        self.m_CommsTunnel.disconnect()
        
    def connect(self):
        if self.chkSafeStatus():
            return
        if self.m_platform == CONST.etAndroid or self.m_platform == CONST.etLocalNet:
            # socket is opened before each data transmission
            if self.callback is not None:
                self.m_app2pyListeningServer = app2pyListeningServer(self.callback)
                self.m_app2pyListeningServer.runAsThread()
        elif self.m_platform == CONST.etDebian:
            self.m_CommsTunnel = btle.Peripheral(usrCfg.BleMACaddress)
            self.m_CommsTunnel.setDelegate( DelegateIfc(self.callback))
            self.hService = self.m_CommsTunnel.getServiceByUUID(btle.UUID("0000fff0-0000-1000-8000-00805f9b34fb"))
            #for ch in self.hService.getCharacteristics():
            #    print(str(ch))
            self.char1 = self.hService.getCharacteristics(btle.UUID("0000fff1-0000-1000-8000-00805f9b34fb"))[0]
            self.char3 = self.hService.getCharacteristics(btle.UUID("0000fff3-0000-1000-8000-00805f9b34fb"))[0]
            self.char4 = self.hService.getCharacteristics(btle.UUID("0000fff4-0000-1000-8000-00805f9b34fb"))[0]
            if self.callback is not None:
                self.m_CommsTunnel.writeCharacteristic(self.char4.valHandle+1, bytes([0x1,0x0]))
        elif self.m_platform == CONST.etInternet:
            self.m_mqttQueue = Queue()
            self.m_CommsTunnel = mqttutils.MQTTClientProxy(self.m_mqttQueue,usrCfg.hostIPaddr,usrCfg.mqttPort)
            self.m_CommsTunnel.connect()
            self.m_CommsTunnel.runAsThread()
            self.m_CommsTunnel.subscribe(CONST.TOPIC_APP_INTERNET_Char4_TELEMETRY)
        else:
            pass
            
    def requestInternetTelemetry(self):
        if self.m_platform == CONST.etInternet:
            self.SendInternetCmdTrans(CONST.TOPIC_APP_INTERNET_MQTT_MetaCtrl,CONST.strREQUEST_Telemetry)
            
    def getInternetTelemetry(self):
        if self.m_mqttQueue.empty():
            return None
        else:
            rcvd_bytes = self.m_mqttQueue.get().payload
            self.m_DictTelemetry = bleDataDecoder.decodeBleTelemetry(rcvd_bytes)
            return self.m_DictTelemetry
            
    def listAllBleServices(self):
        print ("all Services...")
        for svc in self.dev.services:
            print(str(svc))
    
    def clearPreviousCmd(self):
        # these two command will be ignored by android if control value stays unchanged. 
        # another benefit is to avoid a single shot command gets missed.
        #self.cmd_SENDSMS = None
        #self.cmd_TAKEPHOTO = None
        self.cmd_u8GPIO = 0
        self.cmd_i8AarrServos = bytearray(CONST.RcPWMchanNum)
        self.cmd_i8StepperMovCnt = bytearray(CONST.StepMotorCnt)
        self.cmd_u8SeqID = 0
    
    def getPy2appDictionaryData(self):
        dictionarydata = None
        if not self.chkSafeStatus():
            if self.cmd_MP3PLAY is None:
                dictionarydata = {'m_MP3PLAY':["",""]}
            else:
                dictionarydata = {'m_MP3PLAY':[self.cmd_MP3PLAY["MP3fileRelativePath"],self.cmd_MP3PLAY["playmode"]]}
            
            if self.cmd_SENDSMS is None:
                dictionarydata['m_SENDSMS'] = ["",""]
            else:
                dictionarydata['m_SENDSMS'] = [self.cmd_SENDSMS["strPhoneNum"],self.cmd_SENDSMS["strSmsContent"]]
            
            if self.cmd_TAKEPHOTO is None:
                dictionarydata['m_TAKEPHOTO'] = ["",""]
            else:
                dictionarydata['m_TAKEPHOTO'] = [self.cmd_TAKEPHOTO["strPhotoFileName"]]

            if self.cmd_SetWallpaper is None:
                dictionarydata['m_iWallpaper'] = [ConstSharedAppSdk.emoPic_Invalid]
            else:
                dictionarydata['m_iWallpaper'] = [self.cmd_SetWallpaper["iWallpaper"]]
            
            listData = [self.cmd_u8GPIO, self.GPIO_beingUsed]  
            dictionarydata['m_SeqID'] = listData
            
            if self.cmd_u8SeqID is None:
                dictionarydata['m_SeqID'] = ["",""]
            else:
                dictionarydata['m_SeqID'] = [self.cmd_u8SeqID, 1]
            
            
            stepperMask = 0
            if self.cmd_i8StepperMovCnt[CONST.stepMotorRollIndex] != 0:
                stepperMask += 1<<CONST.stepMotorRollIndex
            if self.cmd_i8StepperMovCnt[CONST.stepMotorPitchIndex] != 0:
                stepperMask += 1<<CONST.stepMotorPitchIndex
            listData = [self.cmd_i8StepperMovCnt[CONST.stepMotorRollIndex], self.cmd_i8StepperMovCnt[CONST.stepMotorPitchIndex], stepperMask]  
            dictionarydata['m_StepperCtrl'] = listData
            
            listData = [];
            for ii in range(CONST.RcPWMchanNum):
                listData.append(self.cmd_i8AarrServos[ii])
            listData.append(self.Servo_beingUsed)
            dictionarydata['m_PWMctrl_pm127'] = listData
        return dictionarydata
    
    # return False if command is successfully sent out           
    def SendCmdTransBlking(self, bIgnoreIdenticalCmd=True, bBlk=True):
        if self.chkSafeStatus():
            return True
        if self.requestExit:
            return True
        else:
            if bBlk:
                while True:
                    if getMs()-self.LastCmdSentTimeMs > CONST.MinMsIntervalForInternetCtrl:
                        break
                    else:
                        time.sleep(0.01) #10ms
                if bIgnoreIdenticalCmd:
                    if self.isNewBleCmd(self.getBleCmdContent()):
                        self.__sendCmdUnconditional()
                        return False
                    else:
                        print("ignore repeated cmd")
                        return True
                else:
                    self.__sendCmdUnconditional()
                    return False
            else:
                if getMs()-self.LastCmdSentTimeMs < CONST.MinMsIntervalForInternetCtrl:
                    print("ignore overly frequent cmd")
                    return True
                else:
                    if bIgnoreIdenticalCmd:
                        if self.isNewBleCmd(self.getBleCmdContent()):
                            self.__sendCmdUnconditional()
                            return False
                        else:
                            print("ignore repeated cmd")
                            return True
                    else:
                        self.__sendCmdUnconditional()
                        return False

    def __sendCmdUnconditional(self):
        self.LastCmdSentTimeMs = getMs()
        if self.m_platform == CONST.etAndroid or self.m_platform == CONST.etLocalNet:
            self.socketSendStr(self.getPy2appJson())
        elif self.m_platform == CONST.etDebian:
            # direct control BLE, in PC ubuntu or RPi
            self.SendBleCmdTrans(self.getBleCmdContent())
        elif self.m_platform == CONST.etInternet:
            self.SendInternetCmdTrans(CONST.TOPIC_APP_INTERNET_MQTT_CTRL+usrCfg.mqttusername,self.getPy2appJson())
        self.cmd_MP3PLAY = None # avoid start MP3 play twice, press & release key 
    
    def getPy2appJson(self):
        return json.dumps(self.getPy2appDictionaryData())
        
    def socketSendStr(self,strSent):
        # create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to server
        if self.m_platform == CONST.etAndroid or self.m_platform == CONST.etLocalNet:
            if self.m_platform == CONST.etAndroid:
                host = '127.0.0.1' # server address
            elif self.m_platform == CONST.etLocalNet:
                host = usrCfg.hostIPaddr
            else:
                print("laughable coding bug drgwerhsdndhrh")
                quit()
            port = CONST.socketServerPORT_SDKpy2app # server port
            s.connect((host, port))
            s.send(strSent.encode('ASCII'))
            # close the connection
            s.close()
        else:
            print("unsupported Socket Transmission")
                
    def getBleCmdContent(self):
        cmdBytes = bytearray(CONST.CHAR3_BYTE_LEN)
        cmdBytes[0] = 0;
        cmdBytes[1] = 0xFF;
        cmdBytes[CONST.FC_CTRL_BLE_MSGTYPE_LEN+CONST.etRoll_PwmCH] = self.cmd_i8AarrServos[0];
        cmdBytes[CONST.FC_CTRL_BLE_MSGTYPE_LEN+CONST.etPitchPwmCH] = self.cmd_i8AarrServos[1];
        cmdBytes[CONST.FC_CTRL_BLE_MSGTYPE_LEN+CONST.etThrotPwmCH] = self.cmd_i8AarrServos[2];
        cmdBytes[CONST.FC_CTRL_BLE_MSGTYPE_LEN+CONST.etRudd_PwmCH] = self.cmd_i8AarrServos[3];
        cmdBytes[CONST.FC_CTRL_BLE_MSGTYPE_LEN+CONST.etAUX1_PwmCH] = self.cmd_i8AarrServos[4];
        cmdBytes[CONST.FC_CTRL_BLE_MSGTYPE_LEN+CONST.etAUX2_PwmCH] = self.cmd_i8AarrServos[5];

        cmdBytes[CONST.FC_CTRL_BLE_MSGTYPE_LEN+CONST.etAUX4_CH] = self.cmd_i8StepperMovCnt[CONST.stepMotorRollIndex];
        cmdBytes[CONST.FC_CTRL_BLE_MSGTYPE_LEN+CONST.etAUX5_CH] = self.cmd_i8StepperMovCnt[CONST.stepMotorPitchIndex];
        
        cmdBytes[13] = self.cmd_u8GPIO;
        return cmdBytes
    
    def isNewBleCmd(self,bytearrayData):
        if bytearrayData == self.baLastBLEbinaryPkt:
            return False
        else:
            return True
        
    def SendBleCmdTrans(self,bytearrayData):
        if self.chkSafeStatus():
            return
        self.baLastBLEbinaryPkt = bytearrayData
        self.char3.write(bytearrayData)
        # print("BLE cmd %d bytes sent: %s"%(len(bytearrayData),bytearrayData))
    
    def SendInternetCmdTrans(self,strTOPIC,bytearrayData):
        if self.chkSafeStatus():
            return
        self.baLastBLEbinaryPkt = bytearrayData
        self.m_CommsTunnel.publish(strTOPIC,bytearrayData)
        print(" sent")

    def playMP3withID(self,MP3ID):
        if self.m_platform == CONST.etDebian:
            if not self.m_bPygame_mixer_init_done:
                pygame.mixer.init()
                self.m_bPygame_mixer_init_done = True
            thunder1 = pygame.mixer.Sound("./resources/thundersoundeffect.ogg")
            thunder1.play()
        elif self.m_platform == CONST.etAndroid or self.m_platform == CONST.etInternet or self.m_platform == CONST.etLocalNet:
            self.cmd_MP3PLAY = {"MP3fileRelativePath":MP3ID,"playmode":"PLAY_RES"};
        else:
            print("unhandled platform definition")
            return ""
                
    def playMP3file(self,MP3fileRelativePath,bRepeatedly = False):
        if self.m_platform == CONST.etDebian:
            if not self.m_bPygame_mixer_init_done:
                pygame.mixer.init()
                self.m_bPygame_mixer_init_done = True
            thunder1 = pygame.mixer.Sound("./resources/thundersoundeffect.ogg")
            thunder1.play()
        elif self.m_platform == CONST.etAndroid or self.m_platform == CONST.etLocalNet:
            if bRepeatedly:
                self.cmd_MP3PLAY = {"MP3fileRelativePath":MP3fileRelativePath,"playmode":"REPEATEDPLAY"};
            else:
                self.cmd_MP3PLAY = {"MP3fileRelativePath":MP3fileRelativePath,"playmode":"PLAY"};
        elif self.m_platform == CONST.etInternet:
            print("MP3 play not supported in %s mode"%self.m_platform)
        else:
            print("unhandled platform definition")
            return ""
        

    def stopMP3(self):
        if self.m_platform == CONST.etDebian:
            # TODO: add pygame sound play
            pass
        elif self.m_platform == CONST.etAndroid or self.m_platform == CONST.etLocalNet:
            self.cmd_MP3PLAY = {"MP3fileRelativePath":"","playmode":"STOP"};
        elif self.m_platform == CONST.etInternet:
            print("MP3 stop cmd not supported in %s mode"%self.m_platform)
        else:
            print("unhandled platform definition")
            return ""
        
    def send_a_SMS(self,strPhoneNum,strSmsContent):
        if self.m_platform == CONST.etAndroid:
            self.cmd_SENDSMS = {"strPhoneNum":strPhoneNum,"strSmsContent":strSmsContent};
        elif self.m_platform == CONST.etDebian:
            print("SMS not supported in platform type: %s"%self.m_platform)
        elif self.m_platform == CONST.etInternet:
            print("SMS not supported in %s mode"%self.m_platform)
        else:
            print("unsupported platform for send_a_SMS: %s"%self.m_platform)
        
    def take_a_photo(self,strPhotoFileName):
        if self.m_platform == CONST.etAndroid:
            self.cmd_TAKEPHOTO = {'strPhotoFileName':strPhotoFileName}
        elif self.m_platform == CONST.etDebian:
            print("photo not supported in platform type: %s"%self.m_platform)
        elif self.m_platform == CONST.etInternet:
            self.cmd_TAKEPHOTO = {'strPhotoFileName':strPhotoFileName}
        else:
            print("unsupported platform for take_a_photo: %s"%self.m_platform)

    def set_wallpaper(self,iWallpaper):
        if self.m_platform == CONST.etAndroid or self.m_platform == CONST.etLocalNet:
            self.cmd_SetWallpaper = {'iWallpaper':iWallpaper}
        elif self.m_platform == CONST.etDebian:
            print("photo not supported in platform type: %s"%self.m_platform)
        elif self.m_platform == CONST.etInternet:
            self.cmd_SetWallpaper = {'iWallpaper':iWallpaper}
        else:
            print("unsupported platform for set_wallpaper: %s"%self.m_platform)
        
    def setSeqID(self,SeqID):
        self.cmd_u8SeqID = SeqID

    def releaseSeqID(self):
        self.cmd_u8SeqID = None 
       
    def setGPIOn(self,n):
        if n < 0 or n >= CONST.USR_GPIO_CNT:
            print("GPIO %d doesn't exist"%n)
            pass
        else:
            self.cmd_u8GPIO |= (1<<n)
            self.GPIO_beingUsed |= (1<<n)

    def resetGPIOn(self,n):
        if n < 0 or n >= CONST.USR_GPIO_CNT:
            print("GPIO %d doesn't exist"%n)
            pass
        else:
            self.cmd_u8GPIO &= ~(1<<n)
            self.GPIO_beingUsed |= (1<<n)

    def moveStepper_n(self,n,stepCnt):
        if n < 0 or n >= CONST.StepMotorCnt:
            print("Step motor %d(0-indexed) doesn't exist"%n)
            pass
        else:
            if stepCnt > 127 or stepCnt < -128:
                print("input Step motor movement steps(%d) must be within -128 to 127"%stepCnt)
                return None
            self.cmd_i8StepperMovCnt[n:n+1] = ctypes.c_int8(stepCnt)
            for GPIOii in range(n*CONST.GPIOgroupCntStepMotor,(n+1)*CONST.GPIOgroupCntStepMotor):
                self.GPIO_beingUsed |= (1<<GPIOii)

    def setPWM_n_pm1(self,n,pm1Val=0):
        if n < 0 or n >= CONST.RcPWMchanNum:
            print("Servo %d doesn't exist, only [0 to %d]"%(n,CONST.RcPWMchanNum-1))
            pass
        else:
            if pm1Val > 1.0 or pm1Val < -1.0:
                print("acceptable Servo ctrl input range [-1,1]")
                return
            else:
                self.cmd_i8AarrServos[n:n+1] = ctypes.c_int8(servo_pm1ctrl_to_i8(pm1Val))
                self.Servo_beingUsed |= (1<<n)
                #print("PwmCh(%d):%d"%(n,self.cmd_i8AarrServos[n]))

    def motorHbridgeCtrl_pm1(self,index0to2, speed_pm1):
        if index0to2 < 0 or index0to2 > 2:
            print('motorHbridgeCtrl index can only be in the range of [0,2]')
            return
        if speed_pm1 > 1.0 or speed_pm1 < -1.0:
            print('motorHbridgeCtrl speed_pm1 can only be in the range of [-1,1]')
            return
        self.setPWM_n_pm1(index0to2*2,speed_pm1)
        
    def centerServo_n(self,n):
        if n < 0 or n >= CONST.RcPWMchanNum:
            print("Servo %d doesn't exist, only [0 to %d]"%(n,CONST.RcPWMchanNum-1))
            pass
        else:
            self.cmd_i8AarrServos[n] = 0
            self.Servo_beingUsed |= (1<<n)
            
    def handleTelemetryDataPkg(self):
        if self.callback is None:
            defaultTelemDataProcess(self.m_DictTelemetry)
        else:
            self.callback(self.m_DictTelemetry)

    def readSettingData(self):
        if self.m_platform == CONST.etDebian:
            self.m_setting = bleDataDecoder.decodeNVsetting(self.char1.read())
            return self.m_setting
        elif self.m_platform == CONST.etAndroid or self.m_platform == CONST.etLocalNet:
            print("In android platform, we use app to configure this setting")
        elif self.m_platform == CONST.etInternet:
            print("read Setting not supported now, to be added later")
        else:
            print("unhandled platform definition")
            return None

    def readTelemetryData(self):
        if self.m_platform == CONST.etDebian:
            self.m_DictTelemetry = bleDataDecoder.decodeBleTelemetry(self.char4.read())
        elif self.m_platform == CONST.etAndroid:
            self.m_DictTelemetry = app2py_sharedFileDecoder.decodeFileTelemetry(self.getHomeFolderPath()+CONST.strApp2pyCmdFilename+".txt")
        elif self.m_platform == CONST.etInternet:
            # TODO: do we need it?
            print("not supported now. I didn't find its proper use. Add if needed")
        else:
            print("unhandled platform definition")
            return None
        self.handleTelemetryDataPkg()
        return self.m_DictTelemetry
        
    def check4Notifications(self,timeoutSec = 1.0):
        if self.chkSafeStatus():
            return
        if self.m_CommsTunnel.waitForNotifications(timeoutSec):
            pass # handleNotification() has been called
  
    def setTime0(self):
        self.m_startTimeS = time.time()
        
    def secSinceTime0(self):
        return time.time() - self.m_startTimeS

if usrCfg.ctrlType == CONST.etDebian:
    class DelegateIfc(btle.DefaultDelegate):
        def __init__(self, callback = None):
            btle.DefaultDelegate.__init__(self)
            if callback:
                self.callback = callback
            else:
                self.callback = None
    
        def handleNotification(self, cHandle, notif_byteArr):
            self.m_DictTelemetry = bleDataDecoder.decodeBleTelemetry(notif_byteArr)
            self.handleTelemetryDataPkg()
    
        def handleTelemetryDataPkg(self):
            if self.callback is None:
                defaultTelemDataProcess(self.m_DictTelemetry)
            else:
                self.callback(self.m_DictTelemetry)
        
def defaultTelemDataProcess(telemetry):
    '''
    print("\nseqID(%d)------------------------------------------------------------------"%telemetry['SeqID'])
    print("x/y/z:\tRPY(deg)\tAccel(mG)\tGyro(dps)\tMag(mGauss)")
    for ii in range(3):
        print("axis%d: %8.2f\t\t%8.2f\t%8.2f\t%8.2f"%(ii,telemetry['fRPYdeg'][ii],telemetry['fAccel_mG'][ii],telemetry['fGyro_dps'][ii],telemetry['fMag_mGauss'][ii]))
    GPIOinput = telemetry['GPIOinput']
    print("GPIO status %d %d %d %d %d %d"%(GPIOinput&(1<<0)==0,GPIOinput&(1<<1)==0,GPIOinput&(1<<2)==0,GPIOinput&(1<<3)==0,GPIOinput&(1<<4)==0,GPIOinput&(1<<5)==0)) 
    print("Battery: %3.2f(V)\tCompass:%d(deg)\ttemperature:%3.2f(Deg)"%(telemetry['BatteryVolt'],telemetry['CompassDeg'],telemetry['temperatureDeg']))
    '''
    pass
