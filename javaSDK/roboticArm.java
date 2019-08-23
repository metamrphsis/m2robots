public class roboticArm {
	static final int ServoBase = 0; // positive ctrl input: topview, CCW
	static final int ServoShoulder = 1; // positive ctrl input: rightview, CCW
	static final int ServoElbow = 2; // positive ctrl input: rightview, CW
	static final int ServoPump = 3;
	static final int ServoValve = 4;

    public static void main(String[] args) throws InterruptedException {

    	utilities util = new utilities(); 
		util.initilize();        
		
		M2StemController ctrller = new M2StemController();
		ctrller.connect(usrCfg.BleMACaddress);
        
    	byte[] PWMctrlValsCurrent = new byte[CONST.RcPWMchanNum];
    	byte[] PWMctrlValsTarget = new byte[CONST.RcPWMchanNum];
    	byte[] PWMctrlValsStepDistance = new byte[CONST.RcPWMchanNum]; // non-negative value
    	for (int ii = 0; ii < CONST.RcPWMchanNum; ii++) {
    		PWMctrlValsCurrent[ii] = 0;
    		PWMctrlValsTarget[ii] = 0;
    		PWMctrlValsStepDistance[ii] = 0;
    	}
    	byte u8GPIO_val = 0;
    	int iDanceStepii = 0;
    	boolean bLastStepReturn2Origin = false;
        while (util.isRunning()) {
    	    boolean bTargetReached = true;
    	    for (int ii = 0; ii < CONST.RcPWMchanNum; ii++) {
        		if (PWMctrlValsCurrent[ii] != PWMctrlValsTarget[ii]) {
        			bTargetReached = false;
        			break;
        		}
        	}
    	    if (bTargetReached) {
    	    	iDanceStepii ++;
    	    	if (bLastStepReturn2Origin)
    	    		break;
    	    }
    	    byte stepSizeJoint = 1;
    	    byte PrepareRange = 3;
    	    byte tochDownPositionShoulder = -67;
    	    byte tochDownPositionShoulderPrepare = (byte)(tochDownPositionShoulder+PrepareRange);
    	    byte tochDownPositionElbow = 67;
    	    byte tochDownPositionElbowPrepare = (byte)(tochDownPositionElbow+PrepareRange);
	    	System.out.print("step("+iDanceStepii+")");
    	    switch( iDanceStepii ) {
	    	    case 0:
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = 0;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = 0;	PWMctrlValsStepDistance[ServoShoulder] = stepSizeJoint;
	    	    	PWMctrlValsTarget[ServoElbow] = 0;		PWMctrlValsStepDistance[ServoElbow] = stepSizeJoint;
	    	    	PWMctrlValsTarget[ServoPump] = -127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 1: // touch down
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = 0;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = tochDownPositionShoulderPrepare;	PWMctrlValsStepDistance[ServoShoulder] = 127;
	    	    	PWMctrlValsTarget[ServoElbow] = tochDownPositionElbowPrepare;		PWMctrlValsStepDistance[ServoElbow] = 127;
	    	    	PWMctrlValsTarget[ServoPump] = -127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 2: // final touch down
	    	    	util.delay_ms(200);
	    	    	PWMctrlValsTarget[ServoBase] = 0;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = tochDownPositionShoulder;	PWMctrlValsStepDistance[ServoShoulder] = stepSizeJoint;
	    	    	PWMctrlValsTarget[ServoElbow] = tochDownPositionElbow;		PWMctrlValsStepDistance[ServoElbow] = stepSizeJoint;
	    	    	PWMctrlValsTarget[ServoPump] = 127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 3: // vacuum pump 1sec operation
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = 0;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = tochDownPositionShoulder;	PWMctrlValsStepDistance[ServoShoulder] = stepSizeJoint;
	    	    	PWMctrlValsTarget[ServoElbow] = tochDownPositionElbow;		PWMctrlValsStepDistance[ServoElbow] = stepSizeJoint;
	    	    	PWMctrlValsTarget[ServoPump] = 127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 4: // move up slowly
	    	    	util.delay_ms(100);
	    	    	PWMctrlValsTarget[ServoBase] = 0;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = tochDownPositionShoulder;	PWMctrlValsStepDistance[ServoShoulder] = 1;
	    	    	PWMctrlValsTarget[ServoElbow] = (byte)(tochDownPositionElbow-10);		PWMctrlValsStepDistance[ServoElbow] = 1;
	    	    	PWMctrlValsTarget[ServoPump] = 127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 5: // move up
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = 0;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = -20;	PWMctrlValsStepDistance[ServoShoulder] = 127;
	    	    	PWMctrlValsTarget[ServoElbow] = 20;		PWMctrlValsStepDistance[ServoElbow] = 127;
	    	    	PWMctrlValsTarget[ServoPump] = 127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 6: // turn
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = 50;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = -20;	PWMctrlValsStepDistance[ServoShoulder] = 127;
	    	    	PWMctrlValsTarget[ServoElbow] = 20;		PWMctrlValsStepDistance[ServoElbow] = 127;
	    	    	PWMctrlValsTarget[ServoPump] = 127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 7: // put it down
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = 50;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = tochDownPositionShoulder;	PWMctrlValsStepDistance[ServoShoulder] = 127;
	    	    	PWMctrlValsTarget[ServoElbow] = tochDownPositionElbow;		PWMctrlValsStepDistance[ServoElbow] = 127;
	    	    	PWMctrlValsTarget[ServoPump] = 127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 8: // release
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = 50;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = tochDownPositionShoulder;	PWMctrlValsStepDistance[ServoShoulder] = 127;
	    	    	PWMctrlValsTarget[ServoElbow] = tochDownPositionElbow;		PWMctrlValsStepDistance[ServoElbow] = 127;
	    	    	PWMctrlValsTarget[ServoPump] = -127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = 127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 9: // make sure release completed
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = 50;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = 0;	PWMctrlValsStepDistance[ServoShoulder] = 127;
	    	    	PWMctrlValsTarget[ServoElbow] = 0;		PWMctrlValsStepDistance[ServoElbow] = 127;
	    	    	PWMctrlValsTarget[ServoPump] = -127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = 127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 10: // center
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = 0;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = 0;	PWMctrlValsStepDistance[ServoShoulder] = 127;
	    	    	PWMctrlValsTarget[ServoElbow] = 0;		PWMctrlValsStepDistance[ServoElbow] = 127;
	    	    	PWMctrlValsTarget[ServoPump] = -127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 11: // touch down
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = 0;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = tochDownPositionShoulderPrepare;	PWMctrlValsStepDistance[ServoShoulder] = 127;
	    	    	PWMctrlValsTarget[ServoElbow] = tochDownPositionElbowPrepare;		PWMctrlValsStepDistance[ServoElbow] = 127;
	    	    	PWMctrlValsTarget[ServoPump] = -127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 12: // final touch down
	    	    	util.delay_ms(200);
	    	    	PWMctrlValsTarget[ServoBase] = 0;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = tochDownPositionShoulder;	PWMctrlValsStepDistance[ServoShoulder] = stepSizeJoint;
	    	    	PWMctrlValsTarget[ServoElbow] = tochDownPositionElbow;		PWMctrlValsStepDistance[ServoElbow] = stepSizeJoint;
	    	    	PWMctrlValsTarget[ServoPump] = 127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 13: // vacuum pump 1sec operation
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = 0;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = tochDownPositionShoulder;	PWMctrlValsStepDistance[ServoShoulder] = stepSizeJoint;
	    	    	PWMctrlValsTarget[ServoElbow] = tochDownPositionElbow;		PWMctrlValsStepDistance[ServoElbow] = stepSizeJoint;
	    	    	PWMctrlValsTarget[ServoPump] = 127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 14: // move up slowly
	    	    	util.delay_ms(100);
	    	    	PWMctrlValsTarget[ServoBase] = 0;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = tochDownPositionShoulder;	PWMctrlValsStepDistance[ServoShoulder] = 1;
	    	    	PWMctrlValsTarget[ServoElbow] = (byte)(tochDownPositionElbow-10);		PWMctrlValsStepDistance[ServoElbow] = 1;
	    	    	PWMctrlValsTarget[ServoPump] = 127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 15: // move up
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = 0;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = -20;	PWMctrlValsStepDistance[ServoShoulder] = 127;
	    	    	PWMctrlValsTarget[ServoElbow] = 20;		PWMctrlValsStepDistance[ServoElbow] = 127;
	    	    	PWMctrlValsTarget[ServoPump] = 127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 16: // turn
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = -50;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = -20;	PWMctrlValsStepDistance[ServoShoulder] = 127;
	    	    	PWMctrlValsTarget[ServoElbow] = 20;		PWMctrlValsStepDistance[ServoElbow] = 127;
	    	    	PWMctrlValsTarget[ServoPump] = 127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 17: // put it down
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = -50;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = tochDownPositionShoulder;	PWMctrlValsStepDistance[ServoShoulder] = 127;
	    	    	PWMctrlValsTarget[ServoElbow] = tochDownPositionElbow;		PWMctrlValsStepDistance[ServoElbow] = 127;
	    	    	PWMctrlValsTarget[ServoPump] = 127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = -127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 18: // release
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = -50;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = tochDownPositionShoulder;	PWMctrlValsStepDistance[ServoShoulder] = 127;
	    	    	PWMctrlValsTarget[ServoElbow] = tochDownPositionElbow;		PWMctrlValsStepDistance[ServoElbow] = 127;
	    	    	PWMctrlValsTarget[ServoPump] = -127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = 127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
	    	    case 19: // make sure release completed
	    	    	util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = -50;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = 0;	PWMctrlValsStepDistance[ServoShoulder] = 127;
	    	    	PWMctrlValsTarget[ServoElbow] = 0;		PWMctrlValsStepDistance[ServoElbow] = 127;
	    	    	PWMctrlValsTarget[ServoPump] = -127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = 127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	break;
    	    	default:
		    		util.delay_ms(1000);
	    	    	PWMctrlValsTarget[ServoBase] = 0;		PWMctrlValsStepDistance[ServoBase] = 127;
	    	    	PWMctrlValsTarget[ServoShoulder] = 0;	PWMctrlValsStepDistance[ServoShoulder] = 127;
	    	    	PWMctrlValsTarget[ServoElbow] = 0;		PWMctrlValsStepDistance[ServoElbow] = 127;
	    	    	PWMctrlValsTarget[ServoPump] = -127;		PWMctrlValsStepDistance[ServoPump] = 127;
	    	    	PWMctrlValsTarget[ServoValve] = 127;		PWMctrlValsStepDistance[ServoValve] = 127;
	    	    	bLastStepReturn2Origin = true;
		    		break;
    	    }
    	    for (int CHii = 0; CHii < 5; CHii++) {
    	    	boolean Positive = true;
    	    	if (PWMctrlValsTarget[CHii] != PWMctrlValsCurrent[CHii]) {
    	    		if (PWMctrlValsTarget[CHii] < PWMctrlValsCurrent[CHii]) {
    	    			Positive = false;
    	    		}
    	    		if (Positive) {
    	    			if ((int)PWMctrlValsCurrent[CHii] + (int)PWMctrlValsStepDistance[CHii] > (int)PWMctrlValsTarget[CHii]) {
    	    				PWMctrlValsCurrent[CHii] = PWMctrlValsTarget[CHii];
    	    			}
    	    			else {
    	    				PWMctrlValsCurrent[CHii] += PWMctrlValsStepDistance[CHii];
    	    			}
    	    		}
    	    		else {
    	    			if ((int)PWMctrlValsCurrent[CHii] - (int)PWMctrlValsStepDistance[CHii] < (int)PWMctrlValsTarget[CHii]) {
    	    				PWMctrlValsCurrent[CHii] = PWMctrlValsTarget[CHii];
    	    			}
    	    			else {
    	    				PWMctrlValsCurrent[CHii] -= PWMctrlValsStepDistance[CHii];
    	    			}    	    			
    	    		}
    	    	}
    	    }
	    	for (int ii = 0; ii < 5; ii++) {
	    		System.out.print(String.format("%d,", PWMctrlValsCurrent[ii]));
	    	}
	    	System.out.print("\n");
	    	
	    	ctrller.setCtrl(PWMctrlValsCurrent,u8GPIO_val);
            byte[] ctrlCmd = ctrller.getBinaryTxCtrlCmd();
            ctrller.writeCmd(ctrlCmd);
        }
        System.out.print("exit\n");
        ctrller.disconnect();
    }

}