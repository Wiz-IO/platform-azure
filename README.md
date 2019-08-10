# Azure Sphere - PlatformIO
Support Linux ( HighLevelApp ) and Arduino applications

## is not ready yet ... do not install !!! ##

It's almost done ... I will update soon all

[Youtube Arduino Blink](https://www.youtube.com/watch?v=bPYGXtNt8fg)

[Youtube Arduino PubSub](https://www.youtube.com/watch?v=-hhSmKoT8T0)

[Youtube Linux](https://www.youtube.com/watch?v=tIwjUzBBPTg)

## [INSTALL NOTES - READ](https://github.com/Wiz-IO/platform-azure/wiki/Install-Notes)

## Platform Installation
( comming soon, look the big text at the begining )

Install VS Code + PlatformIO

PlatformIO - Home - Platforms - Advanced Installation

Paste link: https://github.com/Wiz-IO/platform-azure 

## New Project - PlatformIO

PlatformIO - Home - New
* enter Project Name - Board write-search '**azure**' - Select **Linux** or **Arduino** 
* you will have basic template project
* Open 'src/app_manifest.json' and enter your 'Capabilities'
* Open 'platformio.ini' and edit your settings
* INI example:
```ini
[env:avnet_aesms_mt3620]
platform = azure
board = avnet_aesms_mt3620
framework = arduino
monitor_port = COM6
monitor_speed = 115200
;build_flags = -D MQTT_MAX_PACKET_SIZE=1024 -D MQTT_KEEPALIVE=60 ; any other
```

Build, Upload ... if uploader work ( tested on Windows 10 ) - nice ... enjoy

## Manual upload

**azsphere device sideload delete** delete old

**azsphere device sideload deploy --imagepackage PATH-TO-PROJECT\NAME\.pio\build\VARIANT\app.image**

## IF YOU WANT HELP / SUPPORT - CONNECT ME
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ESUP9LCZMZTD6)

## Thanks to:
* [Ivan Kravets ( PlatformIO )](https://platformio.org/)
* [Comet electronics](https://www.comet.bg/?cid=111)
* your name


![Project](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/azure.png) 

![Project](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/azure-platformio.png) 
