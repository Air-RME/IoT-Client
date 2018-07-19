git clone https://github.com/aws/aws-iot-device-sdk-python.git
cd aws-iot-device-sdk-python

sudo python3 setup.py install

cd ..

git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT

sudo python setup.py install
sudo python3 setup.py install

cd ..

rm -rf aws-iot-device-sdk-python
rm -rf Adafruit_Python_DHT