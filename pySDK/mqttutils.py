# https://github.com/eclipse/paho.mqtt.python
#

import paho.mqtt.client as mqtt
import threading
import logging
import time

class MQTTClientProxy(object):
    def __init__(self, mqueue=None, hostIPaddr="98.142.131.109", port=1883, humanReadableID="MQTTClientProxy"):
        self._host = hostIPaddr
        self._port = port
        self.m_humanReadableID = humanReadableID
        self._client = None
        self.m_MsgQueue = mqueue # Queue to put received message
        self._thread = None
        self._run = True

    def disconnect(self):
        self._run = False
        self._client.disconnect()

    def on_message(self, client, userdata, msg):
        if self.m_MsgQueue is not None:
            #payload = msg.payload.decode("utf-8")
            #self.m_MsgQueue.put((client, userdata, msg))
            self.m_MsgQueue.put(msg)
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT server {}:{}".format(self._host, self._port))
        elif rc == 1:
            logging.warn("Connection refused - unacceptable protocol version")
        elif rc == 2:
            logging.warn("Connection refused - identifier rejected")
        elif rc == 3:
            logging.warn("Connection refused - server unavailable")
        elif rc == 4:
            logging.warn("Connection refused - bad user name or password")
        elif rc == 5:
            logging.warn("Connection refused - not authorised")
        else:
            logging.warn("Connection failed - result code %d" % (rc))
    
    def on_disconnect(self, client, userdata, rc):
        logging.info("MQTT disconnected")
    
    def connect(self):
        assert self._client is None
        logging.info("Trying to connect to local broker")
        self._client = mqtt.Client(self.m_humanReadableID, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message
        self._client.on_disconnect = self.on_disconnect
        self._client.username_pw_set("dev", "MMoo6687")
        connected = False
        while not connected:
            try:
                self._client.connect(self._host, self._port, 60)
                connected = True
            except:
                time.sleep(2)
    
    def subscribe(self, topic, qos=0):
        self._client.subscribe(topic, qos)
    
    def publish(self, topic, payload, qos=0, retain=False):
        return self._client.publish(topic, payload, qos, retain)
    
    def loop_forever(self):
        self._client.loop_forever() # Auto connect if disconnected
    
    def loop_while(self):
        while self._run:
            self._client.loop()

    def loop(self, timeout=0.1):
        self._client.loop(timeout)
        
    def runAsThread(self, forever=True):
        assert self._thread is None
        target = self.loop_forever if forever else self.loop_while
        self._thread = threading.Thread(target=target, name="MQTTClientProxy", args=())
        self._thread.start()

