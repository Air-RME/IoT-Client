from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import json
import os


def echoCallback(payload, responseStatus, token):
    p = json.loads(payload)
    print(p)


# クライアントセットアップ
shadowClient = AWSIoTMQTTShadowClient("")
shadowClient.configureEndpoint("a1g1flllk3y7ps.iot.ap-northeast-1.amazonaws.com", 8883)
shadowClient.configureCredentials("../credentials/aws/aws-root.pem", "../credentials/device/4bb00f45b1-private.pem.key",
                                  "../credentials/device/4bb00f45b1-certificate.pem.crt")
shadowClient.configureConnectDisconnectTimeout(10)
shadowClient.configureMQTTOperationTimeout(5)

shadowClient.connect()

shadowDevice = shadowClient.createShadowHandlerWithName("Air-RME-test", True)

shadowDevice.shadowGet(echoCallback, 5)
shadowDevice.shadowRegisterDeltaCallback(echoCallback)
shadowDevice.shadowUnregisterDeltaCallback()

shadowClient.disconnect()
