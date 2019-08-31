[31.08.2019]
* Fix times ( Junxiao Shi )
* Fix Wire ( Junxiao Shi )

[28.08.2019]
* Serial.available()
* Client.available()

[26.08.2019]
* ComponentID (GUID) once
* platformio.ini - delete current or all applications
* Try use installed SDK if exist

[22.08.2019]
* [Image packer](https://github.com/Wiz-IO/platform-azure/blob/07d94266b7e44426c8f37778d8c5164b10d92449/builder/frameworks/common.py#L56) must be work fine
* [Arduino Serial and Serial1](https://github.com/Wiz-IO/framework-azure/blob/783b1effeee9e36aececdbb03b1dfdd376c816be/arduino/core/HardwareSerial.cpp#L55) - receive - there is not allowed ioctl() for Serial.Available() and .peek ... I did "fake" ringbuffer
* I found way to use installed Microsoft SDK (for those who have it) - [will update soon](https://github.com/Wiz-IO/platform-azure/blob/b2222658ca657c9c70001924e720417a64a719f0/builder/frameworks/common.py#L126)
