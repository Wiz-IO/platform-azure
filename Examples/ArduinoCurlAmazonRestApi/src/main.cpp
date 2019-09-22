/*
    Created on: 21.09.2019
    Author: Georgi Angelov
      http://www.wizio.eu/
      https://github.com/Wiz-IO/platform-azure 

  Example: REST-API using curl and packed-image files

  Amazon IoT Core - Manage
  Create Thing and Certificates, DOWNLOAD it and Activate
  Policies Allow
  Interact - get YOUR HTTPS URL 

  Put 'your_certificate.pem' and 'your_private_key.pem' in Project SRC folder

  Open Project 'platformio.ini' and set this files for copy to application-image
    board_build.copy = your_certificate.pem your_private_key.pem 

  Open Project 'app_manifest.json' and enable your amazon url
    "AllowedConnections": [ "YOUR-HTTPS.amazonaws.com" ]   
*/

#include <Arduino.h>
#include <curlClient.h>
curlClient client;

#define URL "https://YOUR-HTTPS.amazonaws.com/topics/my/topic"

void send(int port, const char *topic, const char *message)
{
  //Log_Debug("\n[REST] Begin\n");
  client.begin(topic);
  client.CURL_SETOPT(CURLOPT_PORT, port);
  client.CURL_SETOPT(CURLOPT_POSTFIELDS, message);
  client.CURL_SETOPT(CURLOPT_CONNECTTIMEOUT, 30);
  client.CURL_SETOPT(CURLOPT_SSL_VERIFYPEER, 0); // rootCA 1
  client.CURL_SETOPT(CURLOPT_SSLVERSION, CURL_SSLVERSION_TLSv1_2);

  char *path;

  /* if need CA */
  //path = Storage_GetAbsolutePathInImagePackage("rootCA.pem");
  //client.CURL_SETOPT(CURLOPT_CAINFO, path);

  path = Storage_GetAbsolutePathInImagePackage("certificate.pem");
  if (NULL == path)
  {
    Log_Debug("[ERROR] Certificate\n");
    goto end;
  }
  client.CURL_SETOPT(CURLOPT_SSLCERT, path);

  path = Storage_GetAbsolutePathInImagePackage("private.pem");
  if (NULL == path)
  {
    Log_Debug("[ERROR] Private Key\n");
    goto end;
  }
  client.CURL_SETOPT(CURLOPT_SSLKEY, path);

  MemoryBlock *response;
  client.run(&response);
  if (response)
    Log_Debug("[AWS][%d] %.*s\n", response->size, response->size, response->data);
  else
    Log_Debug("[ERROR] NO RESPONSE\n");
end:
  client.end();
  //Log_Debug("[REST] End\n");
}

void setup()
{
  Serial.begin(115200);
  Serial.println("Azure Explore 2019 Georgi Angelov");
  Serial.redirect(stderr); // redirect Serial to Log_Debug() 
}

void loop()
{
  send(8443, URL, "{\"message\":\"Hello from Azure Sphere\"}");
  sleep(60);
}

/*

[REST] Begin
 -===- Downloaded content (65 bytes): -===-
[AWS][65] {"message":"OK","traceId":"0021e6a6-dbb9-2e87-67f0-a3f97064a808"}
[REST] End

*/