import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class utilities {
	static private boolean running = true;
	static private Lock lock;
	static private Condition cv;
	
	public void initilize() {
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
	}
	
	public boolean isRunning() {
		return running;
	}
	
    void delay_ms(int ms) {
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
