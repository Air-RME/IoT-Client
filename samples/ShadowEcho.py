from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import json
import atexit
import time


def echoCallback(payload, responseStatus, token):
    global shadowDevice
    print('--- Update Received ---')
    print("Status: " + responseStatus)
    p = json.loads(payload)
    print(json.dumps(p, indent=4, sort_keys=True))
    print('--- End of Update ---')
    p["state"]["sensor_data"] = {
        "temperature": 16,
        "humidity": 17
    }
    reported = '{"state":{"reported":' + json.dumps(p["state"]) + '}}'
    shadowDevice.shadowUpdate( reported, None, 5)

# クライアントセットアップ
shadowClient = AWSIoTMQTTShadowClient("")
shadowClient.configureEndpoint("a1g1flllk3y7ps.iot.ap-northeast-1.amazonaws.com", 8883)
shadowClient.configureCredentials("../credentials/aws/aws-root.pem", "../credentials/device/4bb00f45b1-private.pem.key",
                                  "../credentials/device/4bb00f45b1-certificate.pem.crt")
shadowClient.configureConnectDisconnectTimeout(10)
shadowClient.configureMQTTOperationTimeout(5)

shadowClient.connect()

shadowDevice = shadowClient.createShadowHandlerWithName("Air-RME-test", True)

shadowDevice.shadowRegisterDeltaCallback(echoCallback)


def exit_handler():
    global shadowDevice
    shadowDevice.shadowUnregisterDeltaCallback()
    shadowClient.disconnect()


atexit.register(exit_handler)

while True:
    time.sleep(1)
