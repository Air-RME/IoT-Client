import json
import time;
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient


class IoTClient:

    def __init__(self):
        self._shadowC = AWSIoTMQTTShadowClient("")
        self._shadowC.configureEndpoint("a1g1flllk3y7ps.iot.ap-northeast-1.amazonaws.com", 8883)
        self._shadowC.configureCredentials("credentials/aws/aws-root.pem",
                                           "credentials/device/4bb00f45b1-private.pem.key",
                                           "credentials/device/4bb00f45b1-certificate.pem.crt")
        self._shadowC.configureConnectDisconnectTimeout(10)
        self._shadowC.configureMQTTOperationTimeout(5)

    def __del__(self):
        self._shadowC.disconnect()

    def connect(self):
        connected = self._shadowC.connect()

        if connected:
            self._shadowD = self._shadowC.createShadowHandlerWithName("Air-RME-test", True)

            self._shadowD.shadowGet(self._setStateCallback, 5)

            self._shadowD.shadowRegisterDeltaCallback(self._echoCallback)
        return connected

    def _setStateCallback(self, payload, responseStatus, token):
        self._state = json.loads(payload)
        reported = '{"state":{"reported":' + json.dumps(self._state["state"]["desired"]) + '}}'
        self._shadowD.shadowUpdate(reported, None, 5)

    def _echoCallback(self, payload, responseStatus, token):
        print('--- Update Received ---')
        print("Status: " + responseStatus)
        p = json.loads(payload)
        self._state["state"]["desired"] = p["state"]
        print(json.dumps(self._state["state"], indent=4, sort_keys=True))
        print('--- End of Update ---')
        reported = '{"state":{"reported":' + json.dumps(p["state"]) + '}}'
        self._shadowD.shadowUpdate(reported, None, 5)


client = IoTClient()

print("Trying to connect to MQTT broker...")

if client.connect():
    print("Connected")
else:
    print("Connection failed.")

while True:
    time.sleep(1)
