# Azure Sphere for PlatformIO
Azure Sphere SDK for PlatformIO

## is not ready yet ... do not install !!! ##

it's almost done ... NICE I found solution with **uploader** and I will update soon all + Arduino port


[Demo movie Arduino](https://www.youtube.com/watch?v=bPYGXtNt8fg)

[Demo movie Linux](https://www.youtube.com/watch?v=tIwjUzBBPTg)


## [INSTALL NOTES - READ](https://github.com/Wiz-IO/platform-azure/wiki/Install-Notes)


## Installation
( comming soon )

Install VS Code + PlatformIO + Git

PlatformIO - Home - Platforms - Advanced Installation

Paste link: https://github.com/Wiz-IO/platform-azure ( look the big text at the begining )

## New Project - PlatformIO

PlatformIO - Home - New
* enter Project Name - search 'azure' - select Linux or Arduino - Create

You will have basic template project

OPEN: 'platformio.ini' and edit your settings

OPEN: 'src/app_manifest.json' and enter your 'Capabilities'

Build, Upload ... if uploader work ( tested on Windows 10 ) - nice ... enjoy

## Manual upload

**azsphere device sideload delete** delete old

**azsphere device sideload deploy --imagepackage PATH-TO-PROJECT\NAME\.pio\build\VARIANT\app.image**

## IF YOU WANT HELP / SUPPORT - CONNECT ME

## Thanks to:
* [Ivan Kravets ( PlatformIO )](https://platformio.org/)
* [Comet electronics](https://www.comet.bg/?cid=111)
* your name


![Project](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/azure.png) 

![Project](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/azure-platformio.png) 
