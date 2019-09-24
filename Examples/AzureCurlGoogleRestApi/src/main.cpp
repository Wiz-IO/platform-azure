/*
    Created on: 21.09.2019
    Author: Georgi Angelov
      http://www.wizio.eu/
      https://github.com/Wiz-IO/platform-azure 
*/

#include <Arduino.h>
#include "google.h"
#include <curlClient.h>
#include <CloudIoTCore.h>
#include <jwt.h>
CloudIoTCoreDevice goo(GOOGLE_PROJECT, GOOGLE_LOCATION, GOOGLE_REGISTRY, GOOGLE_DEVICE, GOOGLE_PRIVATE_KEY);
curlClient client;

void send(int port, const char *url, const char *message)
{
  //Log_Debug("\n[REST] Begin\n");
  String jwt = goo.createJWT(utc());
  //Log_Debug("[JWT] %s\n", jwt.c_str());
  //Log_Debug("[URL] %s\n", url);

  client.begin(url);
  client.CURL_SETOPT(CURLOPT_PORT, port);
  client.CURL_SETOPT(CURLOPT_POSTFIELDS, message);
  client.CURL_SETOPT(CURLOPT_CONNECTTIMEOUT, 30);
  client.CURL_SETOPT(CURLOPT_SSL_VERIFYPEER, 1);
  client.CURL_SETOPT(CURLOPT_SSLVERSION, CURL_SSLVERSION_TLSv1_2);

  struct curl_slist *chunk = NULL;
  char authorization[1024];
  sprintf(authorization, "authorization: Bearer %s", jwt.c_str());
  chunk = curl_slist_append(chunk, authorization);
  chunk = curl_slist_append(chunk, "content-type: application/json");
  chunk = curl_slist_append(chunk, "cache-control: no-cache");

  client.CURL_SETOPT(CURLOPT_HTTPHEADER, chunk);

  char *path;

  path = Storage_GetAbsolutePathInImagePackage(GOOGLE_CA_LIST);
  client.CURL_SETOPT(CURLOPT_CAINFO, path);

  MemoryBlock *response;
  client.run(&response);
  if (response)
    Log_Debug("[GOOGLE][%d] %.*s\n", response->size, response->size, response->data);
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
  char message[1024];
  sprintf(message, "{\"binary_data\":\"SGVsbG8gZnJvbSBBenVyZSBTcGhlcmU=\"}"); // Base64
  send(API_PORT, GOOGLE_URL, message);
  sleep(60);
}

/*

AS CONNECTION IS OK ...

[GOOGLE][202] {
  "error": {
    "code": 400,
    "message": "HTTP is disabled for device registry",
    "status": "FAILED_PRECONDITION"
  }
}

*/