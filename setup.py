from setuptools import setup

setup(
    name='IoT-Client',
    version='0.0.1',
    packages=['samples'],
    url='https://github.com/Air-RME/IoT-Client',
    license='',
    author='Kristoffer Ahlen Bergman',
    author_email='kba_93@live.se',
    description='Air RMEプロジェットのIoTクライアント',
    install_requires=[
        'AWSIoTPythonSDK==1.4.0',
        'Adafruit_Python_DHT==1.3.2'
    ],
    dependency_links=[
        "https://github.com/adafruit/Adafruit_Python_DHT/tarball/master",
        "https://github.com/aws/aws-iot-device-sdk-python/tarball/master"
    ],
)
