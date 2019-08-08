# Azure Sphere for PlatformIO
Azure Sphere SDK for PlatformIO

## is not ready yet ... do not install !!! ##

it's almost done... I have only one problem - Uploader - Microsoft use "TAP-Windows Provider V9" 

I install driver manually but I dont know how to config to work with the board 

and at this moment you need full ( 3Gb ) VS + Azure SDK installation...

If someone ( Microsoft, Avnet, Seed, Element14... ) help - full installation not need

[Demo movie](https://www.youtube.com/watch?v=tIwjUzBBPTg)

## Microsoft ADD Accaunt

You need email at hotmail.com or ... or account at Microsoft

Example: **wizio[@]hotmail.com**

goto **Azure Portal** -> Azure Active Directory -> Users -> **New user**

Enter:

Name: Your Name ( does not matter )

User name: azure[@]wiziohotmail.onMicrosoft.com ( azure@ as your preferences, **wiziohotmail** as your email )

Create User

Select this user -> Directory role -> ADD -> **Global administrator**

That is all... 

Lets test: 

**azsphere login**

**azsphere dev show-attached** Show the details of the attached device

**azsphere dev recover** For device update

**azsphere prep-debug** Set up a device for local debugging

## Installation
( I need 150Mb "cloud" for compiler and tools )

Install VS Code + PlatformIO

PlatformIO - Home - Platforms - Advanced Installation

Paste: https://github.com/Wiz-IO/platform-azure ( look big text at the begining )

## New Project - PlatformIO

enter Project Name - search 'azure' - select Linux - Create

**Build** after this you will have basic template project

OPEN: 'platformio.ini' and edit your settings

OPEN: 'src/app_manifest.json' and enter your 'Capabilities'

Build, Upload ... if uploader work - nice ... enjoy

## Manual upload

**azsphere device sideload delete** delete old

**azsphere device sideload deploy --imagepackage PATH-TO-PROJECT\NAME\.pio\build\VARIANT\app.image**

## IF YOU WANT HELP - CONNECT ME

## Thanks to:
* [Ivan Kravets ( PlatformIO )](https://platformio.org/)
* [Comet electronics](https://www.comet.bg/?cid=111)
* your name


![Project](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/azure.png) 

![Project](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/azure-platformio.png) 
