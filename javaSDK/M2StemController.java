import tinyb.*;
import java.util.*;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class M2StemController {
	private byte m_byteFlightMode = CONST.fightModeSetting.DirectCmdMode.get_byteEnumVal();
	private byte[] m_PWMctrlValsPendingTx = new byte[CONST.RcPWMchanNum];
	private byte m_u8GPIO_val_fromUI = 0;
	
    private byte m_getBinaryTxCtrlCmdCnt = 0;
    private boolean m_bRunning = true;
    private BluetoothDevice sensor;
    private BluetoothGattCharacteristic char3, char4;
    
    void setRunning(boolean running) {
    	m_bRunning = running;
    }
    
    void setCtrl(byte[] PWMctrlValsPendingTx, byte u8GPIO_val_fromUI) {
    	m_PWMctrlValsPendingTx = PWMctrlValsPendingTx;
    	m_u8GPIO_val_fromUI = u8GPIO_val_fromUI;
    }

    boolean connect( String MACaddress ) {
        /*
         * To start looking of the device, we first must initialize the TinyB library. The way of interacting with the
         * library is through the BluetoothManager. There can be only one BluetoothManager at one time, and the
         * reference to it is obtained through the getBluetoothManager method.
         */
        BluetoothManager manager = BluetoothManager.getBluetoothManager();

        /*
         * The manager will try to initialize a BluetoothAdapter if any adapter is present in the system. To initialize
         * discovery we can call startDiscovery, which will put the default adapter in discovery mode.
         */
        boolean discoveryStarted = manager.startDiscovery();

        System.out.println("The discovery started: " + (discoveryStarted ? "true" : "false"));
        try {
        	sensor = getDevice(MACaddress);
        } catch (Exception e) {
            System.err.println("getDevice failure");
            return true;
        }
        /*
         * After we find the device we can stop looking for other devices.
         */
        try {
            manager.stopDiscovery();
        } catch (BluetoothException e) {
            System.err.println("Discovery could not be stopped.");
            return true;
        }

        if (sensor == null) {
            System.err.println("No sensor found with the provided address.");
            System.exit(-1);
        }

        System.out.print("Found device: ");
        printDevice(sensor);

        try {
            if (sensor.connect())
                System.out.println("Sensor with the provided address connected");
            else {
                System.out.println("Could not connect device.");
                System.exit(-1);
            }        	
        }
        catch (Exception e) {
        	System.err.println("exception occurs when attempting to connect");
            System.exit(-1);
        }
        BluetoothGattService m2ctrllerService = null;
        try {
        	m2ctrllerService = getService(sensor, "0000fff0-0000-1000-8000-00805f9b34fb");
        }
        catch (Exception e) {
        	System.err.println("exception occurs when attempting to getService");
            System.exit(-1);
        }
        
        if (m2ctrllerService == null) {
            System.err.println("This device does not have the service we are looking for.");
            sensor.disconnect();
            System.exit(-1);
        }
        System.out.println("Found service " + m2ctrllerService.getUUID());

        char3 = M2StemController.getCharacteristic(m2ctrllerService, "0000fff3-0000-1000-8000-00805f9b34fb");
        char4 = M2StemController.getCharacteristic(m2ctrllerService, "0000fff4-0000-1000-8000-00805f9b34fb");

        if (char3 == null || char4 == null) {
            System.err.println("Could not find the correct characteristics.");
            sensor.disconnect();
            System.exit(-1);
        }

        System.out.println("Found the m2ctrller characteristics");
        
        return false;
    }
    
    void disconnect() {
    	sensor.disconnect();
    }
    
    void writeCmd(byte[] ctrlCmd) {
    	char3.writeValue(ctrlCmd);
    }
    
    byte[] readTelem() {
    	byte[] m_byteArrTelemetry = char4.readValue();
    	return m_byteArrTelemetry;
    }
    
    void printDevice(BluetoothDevice device) {
        System.out.print("Address = " + device.getAddress());
        System.out.print(" Name = " + device.getName());
        System.out.print(" Connected = " + device.getConnected());
        System.out.println();
    }

    /*
     * After discovery is started, new devices will be detected. We can get a list of all devices through the manager's
     * getDevices method. We can the look through the list of devices to find the device with the MAC which we provided
     * as a parameter. We continue looking until we find it, or we try 15 times (1 minutes).
     */
    BluetoothDevice getDevice(String address) throws InterruptedException {
        BluetoothManager manager = BluetoothManager.getBluetoothManager();
        BluetoothDevice sensor = null;
        for (int i = 0; (i < 15) && m_bRunning; ++i) {
            List<BluetoothDevice> list = manager.getDevices();
            if (list == null)
                return null;

            for (BluetoothDevice device : list) {
                printDevice(device);
                /*
                 * Here we check if the address matches.
                 */
                if (device.getAddress().equals(address))
                    sensor = device;
            }

            if (sensor != null) {
                return sensor;
            }
            Thread.sleep(4000);
        }
        return null;
    }

    /*
     * Our device should expose a temperature service, which has a UUID we can find out from the data sheet. The service
     * description of the SensorTag can be found here:
     * http://processors.wiki.ti.com/images/a/a8/BLE_SensorTag_GATT_Server.pdf. The service we are looking for has the
     * short UUID AA00 which we insert into the TI Base UUID: f000XXXX-0451-4000-b000-000000000000
     */
    BluetoothGattService getService(BluetoothDevice device, String UUID) throws InterruptedException {
        System.out.println("Services exposed by device:");
        BluetoothGattService m2ctrllerService = null;
        List<BluetoothGattService> bluetoothServices = null;
        do {
            bluetoothServices = device.getServices();
            if (bluetoothServices == null)
                return null;

            for (BluetoothGattService service : bluetoothServices) {
                System.out.println("UUID: " + service.getUUID());
                if (service.getUUID().equals(UUID))
                    m2ctrllerService = service;
            }
            Thread.sleep(4000);
        } while (bluetoothServices.isEmpty() && m_bRunning);
        return m2ctrllerService;
    }

    static BluetoothGattCharacteristic getCharacteristic(BluetoothGattService service, String UUID) {
        List<BluetoothGattCharacteristic> characteristics = service.getCharacteristics();
        if (characteristics == null)
            return null;

        for (BluetoothGattCharacteristic characteristic : characteristics) {
            if (characteristic.getUUID().equals(UUID))
                return characteristic;
        }
        return null;
    }
    
    byte[] getBinaryTxCtrlCmd()
    {
        m_getBinaryTxCtrlCmdCnt ++;
        // byte: -128 to 127
        byte[] TxCtrlCmd = new byte[CONST.CHAR3_BYTE_LEN];
        int iBeginByteForCtrlCmd = 0;

        for (int ii = 0; ii < CONST.FC_CTRL_BLE_MSGTYPE_LEN; ii++) {
            TxCtrlCmd[ii] = CONST.FC_CTRL_MSG_PREAMBLE_TYPE_TX[ii];
        }
        iBeginByteForCtrlCmd = CONST.FC_CTRL_BLE_MSGTYPE_LEN;

        for (int phyCHii = 0; phyCHii < CONST.RcPWMchanNum; phyCHii++) { // sequential in the TX data packet
        	TxCtrlCmd[iBeginByteForCtrlCmd + phyCHii] = m_PWMctrlValsPendingTx[phyCHii];
        }

        byte transmittedSeqID = m_getBinaryTxCtrlCmdCnt;

        TxCtrlCmd[iBeginByteForCtrlCmd+CONST.etFlightModeSeqIdCH] = (byte)((m_byteFlightMode << CONST.SeqIDbitCnt) + transmittedSeqID&((1<<CONST.SeqIDbitCnt)-1));
        TxCtrlCmd[iBeginByteForCtrlCmd + CONST.etAUX4_CH] = 0;
        TxCtrlCmd[iBeginByteForCtrlCmd + CONST.etAUX5_CH] = 0;
        TxCtrlCmd[iBeginByteForCtrlCmd+CONST.etAUX6_CH] = 0;
        TxCtrlCmd[iBeginByteForCtrlCmd+CONST.etAUX7_CH] = 0;
        TxCtrlCmd[iBeginByteForCtrlCmd+CONST.etGPIO_CTRL_BYTE] = (byte)(m_u8GPIO_val_fromUI);
        return TxCtrlCmd;
    }

    dictionarydata decodeTelemetry(byte [] m_byteArrTelemetry) {
    	dictionarydata telem = new dictionarydata();
    	telem.fRPYdeg = new float[3];
    	telem.fAccelHwUnit = new float[3]; // HW unit
    	telem.fGyroHwUnit = new float[3];    // HW unit
    	telem.fMagHwUnit = new float[3];
        int byte0;
        for (int ii = 0; ii < 3; ii++) {
            byte piece0;
            byte piece1;

            byte0 = ii * CONST.FC_STATUS_EACH_AXIS_BYTE;
            // lower 6 bit in i16byteArr[0] is always 0 since we pack 16bit data into 10bit protocol storage
            // which 10bit out of 16 bit depends on LSB_DROP_XXX
            byte[] i16byteArr = new byte[2];
            i16byteArr[0] = (byte) (((int) m_byteArrTelemetry[byte0 + 0] & 0x03) << 6);
            piece0 = (byte) ((m_byteArrTelemetry[byte0 + 0] & 0xFC) >>> 2);
            piece1 = (byte) ((m_byteArrTelemetry[byte0 + 1] & 0x03) << 6);
            i16byteArr[1] = (byte) (piece0 + piece1);
            int i16value = ByteBuffer.wrap(Arrays.copyOfRange(i16byteArr, 0, 2)).order(ByteOrder.LITTLE_ENDIAN).getShort();
            i16value = i16value >> 6;
            telem.fRPYdeg[ii] = ((float) i16value / CONST.RPY_floatIntConversion);

            i16byteArr[0] = (byte) (((int) m_byteArrTelemetry[byte0 + 1] & 0x0C) << 4);
            piece0 = (byte) ((m_byteArrTelemetry[byte0 + 1] & 0xF0) >>> 4);
            piece1 = (byte) ((m_byteArrTelemetry[byte0 + 2] & 0x0F) << 4);
            i16byteArr[1] = (byte) (piece0 + piece1);
            int i16_acc;
            i16_acc = (ByteBuffer.wrap(Arrays.copyOfRange(i16byteArr, 0, 2)).order(ByteOrder.LITTLE_ENDIAN).getShort());
            i16_acc = i16_acc >> (6 - CONST.LSB_DROP_ACC - 1);
            telem.fAccelHwUnit[ii] = (float) i16_acc * CONST.ACC_DYNAMIC_FS_RNG * 1000 / (float) Math.pow(2, 15);

            i16byteArr[0] = (byte) (((int) m_byteArrTelemetry[byte0 + 2] & 0x30) << 2);
            piece0 = (byte) ((m_byteArrTelemetry[byte0 + 2] & 0xC0) >>> 6);
            piece1 = (byte) ((m_byteArrTelemetry[byte0 + 3] & 0x3F) << 2);
            i16byteArr[1] = (byte) (piece0 + piece1);
            int i16_gyro;
            i16_gyro = (ByteBuffer.wrap(Arrays.copyOfRange(i16byteArr, 0, 2)).order(ByteOrder.LITTLE_ENDIAN).getShort());
            i16_gyro = i16_gyro >> (6 - CONST.LSB_DROP_GYR - 3);
            telem.fGyroHwUnit[ii] = (float) i16_gyro * CONST.GYRO_DYNAMIC_FS_RNG / (float) Math.pow(2, 15);

            i16byteArr[0] = (byte) (((int) m_byteArrTelemetry[byte0 + 3] & 0xC0));
            i16byteArr[1] = m_byteArrTelemetry[byte0 + 4];
            int i16_mag;
            // rebuild i16 data with lower 6 bits all-zero
            i16_mag = (ByteBuffer.wrap(Arrays.copyOfRange(i16byteArr, 0, 2)).order(ByteOrder.LITTLE_ENDIAN).getShort());
            // rebuild the actual i16 data transmitted
            i16_mag = i16_mag >> (6-CONST.LSB_DROP_MAG);
        telem.fMagHwUnit[ii] = (float) i16_mag * 1000 / CONST.LSBcountPerGauss;
        }
        telem.iCompassDeg = m_byteArrTelemetry[CONST.ByteIndex0Compass] * 2;
        // 16bit 6050 temperature reading
        //int i16Temperature = ByteBuffer.wrap(Arrays.copyOfRange(m_byteArrTelemetry, CONST.ByteIndex0Tmpture, CONST.ByteIndex0Tmpture + 2)).order(ByteOrder.LITTLE_ENDIAN).getShort();
        //float fTemperatureDeg = (float) i16Temperature / 340 + 36.53f;
        // 8-bit 6050 temperature reading
        byte i8Temperature = m_byteArrTelemetry[CONST.ByteIndex0Tmpture];
        telem.fTemperatureDeg = (float) i8Temperature / (340.0f/256.0f) + 36.53f;
        return telem;
    }
}