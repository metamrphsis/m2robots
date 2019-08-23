public class l2_variableManipulation {
	public static void main(String[] args) throws InterruptedException {
		utilities util = new utilities(); 
		util.initilize();
		
		M2StemController ctrller = new M2StemController();
		ctrller.connect(usrCfg.BleMACaddress);
    	int iGPIO_val = 1;
    	System.out.println("variable: " + iGPIO_val + ", binary:" + Integer.toBinaryString(iGPIO_val));
    	byte[] PWMctrlValsPendingTx = new byte[CONST.RcPWMchanNum];
    	ctrller.setCtrl(PWMctrlValsPendingTx,(byte)iGPIO_val);
        ctrller.writeCmd(ctrller.getBinaryTxCtrlCmd());
        util.delay_ms(2000);
        /////////////////////////////////////////////
        // new value is based on changes from current value
    	iGPIO_val = iGPIO_val + 1; // b10
    	System.out.println("variable: " + iGPIO_val + ", binary:" + Integer.toBinaryString(iGPIO_val));
        /////////////////////////////////////////////
    	ctrller.setCtrl(PWMctrlValsPendingTx,(byte)iGPIO_val);
        ctrller.writeCmd(ctrller.getBinaryTxCtrlCmd());
        util.delay_ms(2000);
        /////////////////////////////////////////////
        // alternative grammar to achieve the same change of value 
    	iGPIO_val += 1; // b11
    	System.out.println("variable: " + iGPIO_val + ", binary:" + Integer.toBinaryString(iGPIO_val));
        /////////////////////////////////////////////
    	ctrller.setCtrl(PWMctrlValsPendingTx,(byte)iGPIO_val);
        ctrller.writeCmd(ctrller.getBinaryTxCtrlCmd());
        util.delay_ms(2000);
        
        ctrller.disconnect();
    }
}
