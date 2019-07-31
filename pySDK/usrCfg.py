#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# ubuntu <==bluepy==> Ble HW 
import CONST
ctrlType = CONST.etDebian
#ctrlType = CONST.etInternet
#ctrlType = CONST.etLocalNet
#ctrlType = CONST.etAndroid

if ctrlType == CONST.etInternet:
# ubuntu <==internet MQTT==> android App 
    BleMACaddress = None
    hostIPaddr = "98.142.131.109"
    mqttPort = 1883
    mqttusername = ""
    mqttpassword = ""
elif ctrlType == CONST.etDebian:
    # ubuntu <==bluepy==> Ble HW 
    BleMACaddress= "80:6F:B0:A7:F7:F1" #"80:6F:B0:A7:F7:CA" #
    hostIPaddr = None
    mqttPort = None
    mqttusername = None
    mqttpassword = None
elif ctrlType == CONST.etLocalNet:
    # python running in computer within same LAN <==socket==> background android app
    BleMACaddress= None
    hostIPaddr = "192.168.1.105"
    mqttPort = None
    mqttusername = None
    mqttpassword = None
elif ctrlType == CONST.etAndroid:
    # python running in android termux <==socket==> background android app
    BleMACaddress= None
    hostIPaddr = None
    mqttPort = None
    mqttusername = None
    mqttpassword = None
else:
    quit()
