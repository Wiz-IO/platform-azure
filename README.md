# Azure Sphere - PlatformIO
* **version 1.0.13** ( look here, [if there is something new](https://github.com/Wiz-IO/platform-azure/blob/master/fix.md) )
* **OS Windows 10 ( only )** ( not have tools for Unix... )
* * Sysroot 2+Beta1905
* * Arduino HighLevel applications
* * Linux HighLevel applications
* * Baremetal Cortex-M4 applications  
* * Wiring Cortex-M4 ( is "cut out" Arduino, [in progress...](https://www.youtube.com/watch?v=bdG8GsRaUSA) ) (**NEW**)
* It is very beta version - **[may be bugs yet](https://github.com/Wiz-IO/framework-azure)** 

**Arduino part**
* Arduino base core ( sources from last Arduino IDE )
* HardwareSerial
* GPIO
* Wire
* SPI (**NEW**)
* wifiClient
* wifiUDP (**NEW**)
* curlClient
* other in proggress...
* [Examples](https://github.com/Wiz-IO/platform-azure/tree/master/Examples)

**Wiring part ( Arduino for M4F core )**
* Arduino base core
* HardwareSerial (in progress)
* GPIO
* ADC

**Linux & Baremetal parts** 
* As original [SDK](https://docs.microsoft.com/en-us/azure-sphere/) 
* [Examples](https://github.com/Azure/azure-sphere-samples)

**Tested Boards** 
* [Azure Sphere MT3620 Starter AES-MS-MT3620-SK-G by Avnet](https://www.avnet.com/shop/us/products/avnet-engineering-services/aes-ms-mt3620-sk-g-3074457345636825680/)

**Demo movies**
* [Youtube Arduino Blink](https://www.youtube.com/watch?v=bPYGXtNt8fg)
* [Youtube Arduino PubSub](https://www.youtube.com/watch?v=-hhSmKoT8T0)
* [Youtube Linux](https://www.youtube.com/watch?v=tIwjUzBBPTg)

![Project](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/azuresphere.jpg) 

**Documentations, Support, Forums**
* [Mediatek MT3620](https://www.mediatek.com/products/azureSphere/mt3620)
* [Azure Sphere Documentation](https://docs.microsoft.com/en-us/azure-sphere/)
* [MSDN Azure Sphere forum](https://social.msdn.microsoft.com/Forums/en-US/home?forum=azuresphere)
* [AVNET Azure Sphere MT3620 Starter Kit](http://cloudconnectkits.org/product/azure-sphere-starter-kit)
* [Element14 Azure Sphere MT3620 Starter Kit](https://www.element14.com/community/community/designcenter/azure-sphere-starter-kits/)
* [Speed Test CoreMark 1.0](https://github.com/PaulStoffregen/CoreMark) = **1425.31** ( -Ofast )
* [WIKI](https://github.com/Wiz-IO/platform-azure/wiki)

## [INSTALL NOTES - READ](https://github.com/Wiz-IO/platform-azure/wiki/Install-Notes)

## Platform Installation

Install VS Code + PlatformIO

PlatformIO - Home - Platforms - Advanced Installation

Paste link: https://github.com/Wiz-IO/platform-azure 

## Fast Uninstal
* goto C:\Users\USER_NAME\.platformio\platforms **delete** folder **azure**
* goto C:\Users\USER_NAME\.platformio\packages **delete** folder **framework-azure**

## New Project - PlatformIO

PlatformIO - Home - New
* enter Project Name - Board write-search '**azure**' - Select **Linux** or **Arduino** 
* you will have basic template project
* Open 'src/app_manifest.json' and enter your 'Capabilities'
* Open 'platformio.ini' and edit your settings
* Project **platformio.ini** example:
```ini
[env:avnet_aesms_mt3620]
platform = azure
board = avnet_aesms_mt3620
framework = arduino
monitor_port = COM6
monitor_speed = 115200

;board_build.sysroot = 2  ; default is max version
;board_build.delete = all ; default is current application
;board_build.use_sdk = 0  ; default is USE installed if exist, 0 = use PIO

;build_flags = -D ANY_FLAG
```

Build, Upload ... if uploader work ( tested on Windows 10 ) - nice ... enjoy

## Manual upload

**azsphere device sideload delete** delete all or current -> **-i GUID**

**azsphere device sideload deploy --imagepackage PATH-TO-PROJECT\NAME\.pio\build\VARIANT\app.image**



## Thanks to:
* [Ivan Kravets ( PlatformIO )](https://platformio.org/)
* [Comet electronics](https://www.comet.bg/?cid=111)
* Roberto del Campo
* Junxiao Shi


![Project](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/azure.png) 

![Project](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/azure-platformio.png) 

**IF YOU WANT HELP / SUPPORT - CONNECT ME**
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ESUP9LCZMZTD6)
