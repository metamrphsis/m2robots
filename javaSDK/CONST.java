public class CONST {
	public static final int FC_STATUS_EACH_AXIS_BYTE = 5;
	public static final int RPY_floatIntConversion = 2;
	public static final int LSB_DROP_ACC = 5;
	public static final float ACC_DYNAMIC_FS_RNG = 2.0f; // g. MPU6050_ACCEL_FS_2: \pm 2G
	public static final float GYRO_DYNAMIC_FS_RNG = 2000.0f; // deg/sec
	public static final int LSBcountPerGauss = 6842; // LIS3MDL, \pm 4Gauss full range
	public static final int ByteIndex0Compass = 17;
	public static final int LSB_DROP_MAG = 6;
	public static final int LSB_DROP_GYR = 0;
	public static final int ByteIndex0Tmpture = 18;
	public static final int CHAR3_BYTE_LEN = 20;
    public static final int FC_CTRL_BLE_MSGTYPE_LEN = 2;
    public static final byte FC_CTRL_MSG_PREAMBLE_TYPE_TX[]      = new byte[] {(byte)0x0, (byte)0xFF};
    public static final byte FC_CTRL_MSG_PREAMBLE_TYPE_SETNAME[] = new byte[] {(byte)0x55, (byte)0xAA};
    public static final byte FC_CTRL_MSG_PREAMBLE_TYPE_SET_PID[] = new byte[] {(byte)0x17, (byte)0x88};
    public static final int FC_CTRL_MSG_SET_PID_Byte0_forValue = 4;
    public static final int RcPWMchanNum = 6;
    public static final int HbridgeCnt = RcPWMchanNum/2;
    static final byte SeqIDbitCnt = 2;
    static final byte etRoll_PwmCH = 0;
    static final byte etPitchPwmCH = 1;static final byte RcJoystickCHnum = 2;
    static final byte etThrotPwmCH = 2;
    static final byte etRudd_PwmCH = 3;
    static final byte etAUX1_PwmCH = 4;
    static final byte etAUX2_PwmCH = 5;
    static final byte etFlightModeSeqIdCH = 6; // realtime settings, flight mode. MSB=>LSB, AUX3_FightModeMask, SeqIDbitCnt
    static final byte etAUX4_CH = 7;
    static final byte etAUX5_CH = 8;
    static final byte etAUX6_CH = 9;
    static final byte etAUX7_CH = 10;
    static final byte etGPIO_CTRL_BYTE = 11;
    static final byte RcAllCHnum = 12;
    public static final int StepMotorCnt = 2;
    public static final int stepMotorRollIndex = 0;
    public static final int stepMotorPitchIndex = 1;
    public enum fightModeSetting{
        DirectCmdMode("DirectCmdMode",(byte)0),
        AttitudeCtrlMode("AttitudeCtrlMode",(byte)1);
        private String m_strname;
        private byte m_byteEnumVal;
        private fightModeSetting(String stringname, byte byteEnumVal) {
            this.m_strname = stringname;
            this.m_byteEnumVal = byteEnumVal;
        }
        @Override
        public String toString(){
            return m_strname;
        }
        public byte get_byteEnumVal() { return m_byteEnumVal; }
    }
    
    
    
}
