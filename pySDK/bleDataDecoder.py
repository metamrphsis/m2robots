#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import CONST

def decodeNVsetting(byteArr):
    NVsetting = {
        "CH0dutyCycleMode":(byteArr[0]&(0x1<<0))>0,
        "CH1dutyCycleMode":(byteArr[0]&(0x1<<1))>0,
        "CH2dutyCycleMode":(byteArr[0]&(0x1<<2))>0,
        "CH3dutyCycleMode":(byteArr[0]&(0x1<<3))>0,
        "CH4dutyCycleMode":(byteArr[0]&(0x1<<4))>0,
        "CH5dutyCycleMode":(byteArr[0]&(0x1<<5))>0,
        "CH01_merged2be_H_bridge":(byteArr[1]&(0x1<<0))>0,
        "CH23_merged2be_H_bridge":(byteArr[1]&(0x1<<1))>0,
        "CH45_merged2be_H_bridge":(byteArr[1]&(0x1<<2))>0,
    };    
    return NVsetting

def decodeBleTelemetry(byteArr):
    SeqID = byteArr[CONST.ByteIndex0Seq_n_Btn] & 0x3
    fRPYdeg=[0,0,0]
    fAccelHwUnit=[0,0,0]
    fGyroHwUnit=[0,0,0]
    fMagHwUnit=[0,0,0]
    for ii in range(3):
        byte0 = ii*CONST.FC_STATUS_EACH_AXIS_BYTE;
        i16byteArr = bytearray([0x0, 0x0]);
        i16byteArr[0] = ((byteArr[byte0+0]&0x03) << 6);
        piece0 = ((byteArr[byte0+0]&0xFC) >> 2);
        piece1 = ((byteArr[byte0+1]&0x03) << 6);
        i16byteArr[1] = (piece0 + piece1);
        i16value = int.from_bytes(i16byteArr, byteorder='little', signed=True)
        i16value = i16value >> 6;
        fRPYdeg[ii] = (i16value/CONST.RPY_floatIntConversion);

        i16byteArr[0] = ((byteArr[byte0+1]&0x0C) << 4);
        piece0 = ((byteArr[byte0+1]&0xF0) >> 4);
        piece1 = ((byteArr[byte0+2]&0x0F) << 4);
        i16byteArr[1] = (piece0 + piece1);
        i16value = int.from_bytes(i16byteArr, byteorder='little', signed=True)
        i16value = i16value >> (6-CONST.LSB_DROP_ACC-1);
        fAccelHwUnit[ii] = i16value*CONST.ACC_DYNAMIC_FS_RNG*1000/(2**15);

        i16byteArr[0] = ((byteArr[byte0+2]&0x30) << 2);
        piece0 = ((byteArr[byte0+2]&0xC0) >> 6);
        piece1 = ((byteArr[byte0+3]&0x3F) << 2);
        i16byteArr[1] = (piece0 + piece1);
        i16value= int.from_bytes(i16byteArr, byteorder='little', signed=True)
        i16value = i16value >> (6-CONST.LSB_DROP_GYR-3);
        fGyroHwUnit[ii] = i16value*CONST.GYRO_DYNAMIC_FS_RNG/(2**15);

        i16byteArr[0] = ((byteArr[byte0+3]&0xC0));
        i16byteArr[1] = byteArr[byte0+4];
        i16value = int.from_bytes(i16byteArr, byteorder='little', signed=True)
        i16value = i16value >> (6-CONST.LSB_DROP_MAG);
        fMagHwUnit[ii] = i16value*1000/CONST.LSBcountPerGauss;
        
    GPIOdata = (byteArr[CONST.ByteIndex0Seq_n_Btn] & 0xFC) >> 2
    BtnStatus = []
    for ii in range(CONST.USR_BTN_CNT):
        BtnStatus.append((GPIOdata>>ii)&0x1 != 0)
        
    fVoltage = byteArr[CONST.ByteIndex0ADC1_1tenthV] / 10.0
    iCompass_pm180deg = byteArr[CONST.ByteIndex0Compass] * 2 -180
    fTemperatureDeg = byteArr[CONST.ByteIndex0Tmpture]/10
    telemetry = {
        "m_BtnStatus":BtnStatus,
        "m_SeqID":SeqID,
        "m_fAccelHwUnit":fAccelHwUnit,
        "m_fGyroHwUnit":fGyroHwUnit,
        "m_fMagHwUnit":fMagHwUnit,
        "m_fPhoneRPYdeg":[0.0,0.0,0.0],
        "m_fRPYdeg":fRPYdeg,
        "m_fTemperatureDeg":fTemperatureDeg,
        "m_fVoltage":fVoltage,
        "m_iCompass_pm180deg":iCompass_pm180deg,
        };    
    return telemetry