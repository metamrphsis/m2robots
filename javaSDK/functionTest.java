import tinyb.*;
import java.util.*;
import java.util.concurrent.locks.*;
import java.util.concurrent.TimeUnit;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class functionTest {
	static private boolean running = true;
	static private Lock lock;
	static private Condition cv;

    /*
     * This program connects to a TI SensorTag 2.0 and reads the temperature characteristic exposed by the device over
     * Bluetooth Low Energy. The parameter provided to the program should be the MAC address of the device.
     *
     * A wiki describing the sensor is found here: http://processors.wiki.ti.com/index.php/CC2650_SensorTag_User's_Guide
     *
     * The API used in this example is based on TinyB v0.3, which only supports polling, but v0.4 will introduce a
     * simplied API for discovering devices and services.
     */
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
    	byte[] PWMctrlValsPendingTx = new byte[CONST.RcPWMchanNum];
    	byte u8GPIO_val_fromUI = 0;
        while (running) {
            for (int ii = 0; ii < CONST.RcPWMchanNum; ii++)
            	PWMctrlValsPendingTx[ii] = (byte)((int)u8GPIO_val_fromUI*10);
        	u8GPIO_val_fromUI ++;
        	M2StemController.setCtrl(PWMctrlValsPendingTx,u8GPIO_val_fromUI);
            byte[] ctrlCmd = M2StemController.getBinaryTxCtrlCmd();
            M2StemController.writeCmd(ctrlCmd);

            delay_ms(100);
            
        	byte[] m_byteArrTelemetry = M2StemController.readTelem();
            M2StemController.decodeTelemetry(m_byteArrTelemetry);
           
            delay_ms(100);
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