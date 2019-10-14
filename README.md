# Azure Sphere - PlatformIO
* **Version 2.0.0** ( look here, [if there is something new](https://github.com/Wiz-IO/platform-azure/blob/master/fix.md) )
* OS Windows 10 **( preferably )** ... Tested on [Windows 8, 10](https://github.com/Wiz-IO/platform-azure/wiki/Install-Notes#azure-sphere-device-communication-service-manually)
* * Sysroot 2+Beta1905
* * Sysroot 3+Beta1909 ( NEW )
* * Arduino HighLevel applications
* * Linux HighLevel applications
* * Baremetal Cortex-M4 applications  
* * Wiring Cortex-M4 ( is "cut out" Arduino, [in progress...](https://www.youtube.com/watch?v=bdG8GsRaUSA) ) 
* [Full API](https://github.com/Wiz-IO/platform-azure/wiki/How-to-unlock-all-API-s) (**NEW**)
* [Experimental mode](https://github.com/Wiz-IO/platform-azure/wiki/Arduino-INI-file#experimental-mode) for libc and libwolfssl (**NEW** beta in process) 
* It is very beta version - **may be bugs yet** 

**Arduino part**
* Arduino base core ( sources from last Arduino IDE )
* HardwareSerial
* GPIO
* Wire
* SPI 
* wifiClient
* wifiUDP 
* curlClient
* ClientSecure
* other in proggress...
* [Examples](https://github.com/Wiz-IO/platform-azure/tree/master/Examples)

**Wiring part ( Arduino for M4F core )**
* Arduino base core
* HardwareSerial (in progress)
* GPIO (**NEW** all gpio)
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
* [Experimental Mode](https://www.youtube.com/watch?v=ucOvjfXg0-o&t=1s)

![Project](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/azuresphere.jpg) 

**Documentations, Support, Forums**
* [Mediatek MT3620](https://www.mediatek.com/products/azureSphere/mt3620)
* [Azure Sphere Documentation](https://docs.microsoft.com/en-us/azure-sphere/)
* [MSDN Azure Sphere forum](https://social.msdn.microsoft.com/Forums/en-US/home?forum=azuresphere)
* [AVNET Forum](https://www.element14.com/community/community/designcenter/azure-sphere-starter-kits/content?filterID=contentstatus[published]~objecttype~objecttype[thread]&filterID=contentstatus[published]~language~language%5Bcpl%5D)
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
* Project [platformio.ini](https://github.com/Wiz-IO/platform-azure/wiki/Arduino-INI-file) example:
```ini
[env:avnet_aesms_mt3620]
platform = azure
board = avnet_aesms_mt3620
framework = arduino
monitor_port = COM6
monitor_speed = 115200

;board_build.sdk = C:/Program Files (x86)/Microsoft Azure Sphere SDK ; path to ...
;board_build.sysroot = 2+Beta1806  ; default is max version, 3+Beta1909
;board_build.delete = all ; default is all applications, or = current 

;board_build.copy =  filename.1 filename.2 
;    copy files from project SRC to image-package, as certificates, settings, etc
;    path is /mnt/APP-GUID/filename ... Storage_GetAbsolutePathInImagePackage()

;board_build.ex_mode = enable ; empty key: disabled ; experimental mode for libc, libwolfssl...
;board_build.verbose = enable ; verbose for azsphere 

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

**IF YOU WANT HELP / SUPPORT**
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ESUP9LCZMZTD6)
