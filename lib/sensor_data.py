import Adafruit_DHT

def get_temperature_info(sensor=Adafruit_DHT.DHT11, pin=4):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    return humidity, temperature