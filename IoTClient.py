import json
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient, AWSIoTMQTTClient
import redis
import os
from IoTClient.lib import sensor_data


class IoTClient:
    _redis = None

    def __init__(self):
        path = os.path.abspath(os.path.dirname(__file__))

        self._shadowC = AWSIoTMQTTShadowClient("shadow")
        self._shadowC.configureEndpoint("a1g1flllk3y7ps.iot.ap-northeast-1.amazonaws.com", 8883)
        self._shadowC.configureCredentials(os.path.join(path, "credentials/aws/aws-root.pem"),
                                           os.path.join(path, "credentials/device/private.pem.key"),
                                           os.path.join(path, "./credentials/device/certificate.pem.crt"))
        self._shadowC.configureConnectDisconnectTimeout(10)
        self._shadowC.configureMQTTOperationTimeout(5)

        # For certificate based connection
        self._mqttC = AWSIoTMQTTClient("regular")
        self._mqttC.configureEndpoint("a1g1flllk3y7ps.iot.ap-northeast-1.amazonaws.com", 8883)
        self._mqttC.configureCredentials(os.path.join(path, "credentials/aws/aws-root.pem"),
                                         os.path.join(path, "credentials/device/private.pem.key"),
                                         os.path.join(path, "./credentials/device/certificate.pem.crt"))

        self._mqttC.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self._mqttC.configureDrainingFrequency(2)  # Draining: 2 Hz
        self._mqttC.configureConnectDisconnectTimeout(10)  # 10 sec
        self._mqttC.configureMQTTOperationTimeout(5)  # 5 sec

    def __del__(self):
        try:
            self._shadowC.disconnect()
            self._mqttC.disconnect()
        except Exception:
            pass

    def connect(self):
        self._redis = redis.Redis(host='localhost', port=6379)

        try:
            self._redis.get("test")  # getting None returns None or throws an exception
        except (redis.exceptions.ConnectionError,
                redis.exceptions.BusyLoadingError):
            print("Failed to connect to Redis server")
            return False

        connected = self._shadowC.connect() and self._mqttC.connect()

        if connected:
            self._shadowD = self._shadowC.createShadowHandlerWithName("Air-RME-test", True)

            self._shadowD.shadowGet(self._setStateCallback, 5)

            self._shadowD.shadowRegisterDeltaCallback(self._echoCallback)
        return connected

    def _setStateCallback(self, payload, responseStatus, token):
        self._state = json.loads(payload)
        reported = '{"state":{"reported":' + json.dumps(self._state["state"]["desired"]) + '}}'
        self._redis.rpush("order", self._state["state"]["desired"]);
        print(self._redis.lpop("order").decode('utf-8'))
        self._shadowD.shadowUpdate(reported, None, 5)

    def _echoCallback(self, payload, responseStatus, token):
        print('--- Update Received ---')
        print("Status: " + responseStatus)
        p = json.loads(payload)
        self._state["state"]["desired"] = p["state"]
        print(json.dumps(self._state["state"], indent=4, sort_keys=True))
        print('--- End of Update ---')
        reported = '{"state":{"reported":' + json.dumps(p["state"]) + '}}'
        self._redis.rpush("order", json.dumps(self._state["state"]["desired"]))
        self._shadowD.shadowUpdate(reported, None, 5)

    def publish(self, topic, message):
        self._mqttC.publish(topic, json.dumps(message), 0)

    def run(self):
        print("Trying to connect to MQTT broker...")

        if self.connect():
            print("Connected")

            lastTemp = 0
            lastHum = 0

            while True:
                humidity, temperature = sensor_data.get_temperature_info()

                if lastTemp != temperature or lastHum != humidity:
                    data = {
                        "temp": temperature,
                        "hum": humidity
                    }

                    self.publish("/Air-RME-test/sensor", data)
                    lastTemp = temperature
                    lastHum = humidity

                time.sleep(1)
        else:
            print("Connection failed.")

        return


if __name__ == "__main__":
    client = IoTClient()

    while True:
        time.sleep(1)
