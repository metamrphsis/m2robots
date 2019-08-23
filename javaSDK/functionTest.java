public class functionTest {
    public static void main(String[] args) throws InterruptedException {
    	utilities util = new utilities(); 
		util.initilize();
		M2StemController ctrller = new M2StemController();
		ctrller.connect(usrCfg.BleMACaddress);
		
    	byte[] PWMctrlValsPendingTx = new byte[CONST.RcPWMchanNum];
    	byte u8GPIO_val_fromUI = 0;
        while (util.isRunning()) {
            for (int ii = 0; ii < CONST.RcPWMchanNum; ii++)
            	PWMctrlValsPendingTx[ii] = (byte)((int)u8GPIO_val_fromUI*10);
        	u8GPIO_val_fromUI ++;
        	ctrller.setCtrl(PWMctrlValsPendingTx,u8GPIO_val_fromUI);
            byte[] ctrlCmd = ctrller.getBinaryTxCtrlCmd();
            ctrller.writeCmd(ctrlCmd);

            util.delay_ms(100);
            
        	byte[] m_byteArrTelemetry = ctrller.readTelem();
        	dictionarydata telem = ctrller.decodeTelemetry(m_byteArrTelemetry);
        	//System.out.print(String.format("iCompassDeg:%d, fAccelHwUnit[0]:%f\n", telem.iCompassDeg,telem.fAccelHwUnit[0]));
            
            System.out.print("===========================================================================\n");
            System.out.print(String.format("fRPYdeg:%f,%f,%f\n", telem.fRPYdeg[0],telem.fRPYdeg[1],telem.fRPYdeg[2]));
            System.out.print(String.format("fAccelHwUnit:%f,%f,%f\n", telem.fAccelHwUnit[0],telem.fAccelHwUnit[1],telem.fAccelHwUnit[2]));
            System.out.print(String.format("fGyroHwUnit:%f,%f,%f\n", telem.fGyroHwUnit[0],telem.fGyroHwUnit[1],telem.fGyroHwUnit[2]));
            System.out.print(String.format("fMagHwUnit:%f,%f,%f\n", telem.fMagHwUnit[0],telem.fMagHwUnit[1],telem.fMagHwUnit[2]));
            System.out.print(String.format("iCompassDeg:%d\n", telem.iCompassDeg));
            System.out.print(String.format("fTemperatureDeg:%2.1f\n", telem.fTemperatureDeg));
            
            util.delay_ms(100);
        }
        ctrller.disconnect();
    }

}
