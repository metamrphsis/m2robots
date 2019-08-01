import java.util.concurrent.locks.*;
import java.util.concurrent.TimeUnit;

public class roboticArm {
	static private boolean running = true;
	static private Lock lock;
	static private Condition cv;
	static final int ServoBase = 0;
	static final int ServoShoulder = 1;
	static final int ServoElbow = 2;
	static final int ServoPump = 3;
	static final int ServoValve = 4;

    public static void main(String[] args) throws InterruptedException {

        if (args.length > 0) {
            System.err.println("device MAC address defined in usrCfg.java");
            System.exit(-1);
        }
        
        lock = new ReentrantLock();
        cv = lock.newCondition();
        Runtime.getRuntime().addShutdownHook(new Thread() {
            public void run() {
                running = false;
                lock.lock();
                try {
                    cv.signalAll();
                } finally {
                    lock.unlock();
                }
            }
        });
        
        M2StemController.connect(usrCfg.BleMACaddress);
        
    	byte[] PWMctrlVals = new byte[CONST.RcPWMchanNum];
    	for (int ii = 0; ii < CONST.RcPWMchanNum; ii++)
    		PWMctrlVals[ii] = 0;
    	byte u8GPIO_val = 0;
    	int iDanceStepii = 0;
    	boolean bSendCmd = true;
        while (running) {
	    	System.out.print("step("+iDanceStepii+")\n");
    	    switch( iDanceStepii ) {
	    	    case 0:
	    	    	delay_ms(1000);
	    	    	PWMctrlVals[ServoBase] = 0;
	    	    	PWMctrlVals[ServoShoulder] = 0;
	    	    	PWMctrlVals[ServoElbow] = 0;
	    	    	PWMctrlVals[ServoPump] = 0;
	    	    	PWMctrlVals[ServoValve] = 0;
	    	    	break;
	    	    case 1:
	    	    	delay_ms(2000);
	    	    	PWMctrlVals[ServoBase] = 0;
	    	    	PWMctrlVals[ServoShoulder] = 10;
	    	    	PWMctrlVals[ServoElbow] = 10;
	    	    	PWMctrlVals[ServoPump] = 127;
	    	    	PWMctrlVals[ServoValve] = 127;
	    	    	break;
	    	    /*case 2:
	    	    	delay_ms(1000);
	    	    	PWMctrlVals[ServoBase] = -127;
	    	    	PWMctrlVals[ServoShoulder] = -127;
	    	    	PWMctrlVals[ServoElbow] = -127;
	    	    	PWMctrlVals[ServoPump] = -127;
	    	    	PWMctrlVals[ServoValve] = -127;
	    	    	break;
	    	    case 3:
	    	    	delay_ms(1000);
	    	    	PWMctrlVals[ServoBase] = 127;
	    	    	PWMctrlVals[ServoShoulder] = 127;
	    	    	PWMctrlVals[ServoElbow] = 127;
	    	    	PWMctrlVals[ServoPump] = 127;
	    	    	PWMctrlVals[ServoValve] = 127;
	    	    	break;*/
	    	    	
		    	default:
		    		delay_ms(2000);
		    		bSendCmd = false;
		    		break;
    	    }
    	    iDanceStepii ++;
    	    if (bSendCmd) {
        	    M2StemController.setCtrl(PWMctrlVals,u8GPIO_val);
                byte[] ctrlCmd = M2StemController.getBinaryTxCtrlCmd();
                M2StemController.writeCmd(ctrlCmd);
    	    }
    	    else {
    	    	System.out.print("exit\n");
    	    	break;
    	    }
        }
        M2StemController.disconnect();
    }
    
    static void delay_ms(int ms) {
        lock.lock();
        try {
        	cv.await(ms, TimeUnit.MILLISECONDS);
        }
        catch (Exception e) {
        }
        finally {
            lock.unlock();
        }
    }
}