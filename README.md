# Azure Sphere for PlatformIO
Azure Sphere SDK for PlatformIO

## is not ready yet ... do not install !!! ##

it's almost done... I have only one problem - Uploader - Microsoft use "TAP-Windows Provider V9" 

I install driver manually but I dont know how to config to work with the board 

## Microsoft ADD Accaunt

You need email at hotmail.com or ... account at microsoft

Example: wizio[@]hotmail.com

goto Azure Portal -> Azure Active Directory -> Users -> New user

enter ....

Name: Your Name

User name: azure[@]wiziohotmail.onMicrosoft.com ( azure@ as your preferences, **wiziohotmail** as your email )

CREATE User

Select this user -> Directory role -> ADD -> **Global administrator**

That is all... Test: 
**azsphere login**
**azsphere dev show-attached** Show the details of the attached device
**azsphere dev recover** For device update
**azsphere prep-debug** Set up a device for local debugging

## Installation
( at the begining will be manually, I need 150M bytes "cloud" )



![Project](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/azure.png) 

![Project](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/azure-platformio.png) 
