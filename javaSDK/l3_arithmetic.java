public class l4_arithmetic {

	public static void main(String[] args) throws InterruptedException {
		
		utilities util = new utilities(); 
		util.initilize();

        double dThrottle_pm1 = 0.7;
        /////////////////////////////////////////////
        // start the tank
        /////////////////////////////////////////////
        double dSteeringNeutral_pm1 = 0.0; // positive value: turn right
        M2StemController ctrller = new M2StemController();
        ctrller.connect(usrCfg.BleMACaddress);
        
        /////////////////////////////////////////////
        // start the tank
        /////////////////////////////////////////////
    	byte[] PWMctrlValsPendingTx = new byte[CONST.RcPWMchanNum];
    	double dCtrlL = (dThrottle_pm1 + dSteeringNeutral_pm1);
    	dCtrlL = dCtrlL * 127.0;
    	PWMctrlValsPendingTx[0] = double2byteValueBoundryCheck(dCtrlL);
    	double dCtrlR = (dThrottle_pm1 - dSteeringNeutral_pm1);
    	dCtrlR *= 127.0;
    	PWMctrlValsPendingTx[2] = double2byteValueBoundryCheck(dCtrlR);
    	
    	ctrller.setCtrl(PWMctrlValsPendingTx,(byte)0);
    	ctrller.writeCmd(ctrller.getBinaryTxCtrlCmd());
    	util.delay_ms(3000);
        
        ctrller.disconnect();
    }
    
	static byte double2byteValueBoundryCheck(double dVal_pm127) {
		dVal_pm127 = (dVal_pm127 >  127.0)? 127.0:dVal_pm127;
		dVal_pm127 = (dVal_pm127 < -127.0)?-127.0:dVal_pm127;
		return (byte)dVal_pm127;
	}
	
}
