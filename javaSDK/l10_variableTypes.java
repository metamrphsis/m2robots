public class l3_variableTypes {
	public static void main(String[] args) throws InterruptedException {
		utilities util = new utilities(); 
		util.initilize();
		
		M2StemController ctrller = new M2StemController();
		ctrller.connect(usrCfg.BleMACaddress);
        /////////////////////////////////////////////
        // byte value in the range of -128 to 127, 255 needs type cast for variable type byte
    	byte byteGPIO_val = (byte)255;
        /////////////////////////////////////////////
    	byte[] PWMctrlValsPendingTx = new byte[CONST.RcPWMchanNum];
    	ctrller.setCtrl(PWMctrlValsPendingTx,byteGPIO_val);
        ctrller.writeCmd(ctrller.getBinaryTxCtrlCmd());
        util.delay_ms(2000);
        /////////////////////////////////////////////
        // set new value
    	byteGPIO_val = 127;
        /////////////////////////////////////////////
    	ctrller.setCtrl(PWMctrlValsPendingTx,byteGPIO_val);
        ctrller.writeCmd(ctrller.getBinaryTxCtrlCmd());
        util.delay_ms(2000);
        /////////////////////////////////////////////
        // new value is based on changes from current value
    	byteGPIO_val = (byte)(byteGPIO_val + 1);
        /////////////////////////////////////////////
    	ctrller.setCtrl(PWMctrlValsPendingTx,byteGPIO_val);
        ctrller.writeCmd(ctrller.getBinaryTxCtrlCmd());
        util.delay_ms(2000);
        /////////////////////////////////////////////
        // alternative grammar to achieve the same change of value 
    	byteGPIO_val += 1;
        /////////////////////////////////////////////
    	ctrller.setCtrl(PWMctrlValsPendingTx,byteGPIO_val);
        ctrller.writeCmd(ctrller.getBinaryTxCtrlCmd());
        util.delay_ms(2000);
        
        ctrller.disconnect();
    }
}
