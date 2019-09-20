/*
    Created on: 20.09.2019
    Author: Georgi Angelov
      http://www.wizio.eu/
      https://github.com/Wiz-IO/platform-azure 


  Amazon IoT Core - Manage
  Create Thing and Certificates, DOWNLOAD it and Activate
  Policies Allow
  Interact - get YOUR HTTPS URL 

  Put 'your_certificate.pem' and 'your_private_key.pem' in Project SRC folder

  Open Project 'platformio.ini' and set this files for copy to app-image
    board_build.copy = your_certificate.pem your_private_key.pem 

  Open Project 'app_manifest.json' and enable your amazon url
    "AllowedConnections": [ "YOUR.iot.us-east-2.amazonaws.com" ]   
*/

#define AWS_PORT 8883

/* use application GUID ( ComponentId ) from 'app_manifest.json', lower-case */
#define CERT_PATH "/mnt/apps/5c485373-2e66-4c51-b985-9a5c64a08d1c/"

// edit your https amazon url 
#define AWS_HOST "YOUR_HTTP_URL_TO.amazonaws.com"

// edit your 'your_certificate.pem' name 
#define AWS_CERTIFICATE CERT_PATH "certificate.pem"

// edit your 'your_private_key.pem' name 
#define AWS_PRIVATE_KEY CERT_PATH "private.pem"
