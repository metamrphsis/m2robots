public class l1_variable {
    public static void main(String[] args) throws InterruptedException {
    	M2StemController ctrller = new M2StemController();
		ctrller.connect(usrCfg.BleMACaddress);
        /////////////////////////////////////////////
        // change this variable and observe the LED output
    	byte byteGPIO_val;
    	byteGPIO_val = 127; // b1111111
        /////////////////////////////////////////////
    	byte[] PWMctrlValsPendingTx = new byte[CONST.RcPWMchanNum];
    	ctrller.setCtrl(PWMctrlValsPendingTx,byteGPIO_val);
        byte[] ctrlCmd = ctrller.getBinaryTxCtrlCmd();
        ctrller.writeCmd(ctrlCmd);
        ctrller.disconnect();
    }
}
