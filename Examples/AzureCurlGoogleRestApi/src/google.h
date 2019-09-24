/*
    Created on: 21.09.2019
    Author: Georgi Angelov
      http://www.wizio.eu/
      https://github.com/Wiz-IO/platform-azure 


Google IoT Core:
  https://cloud.google.com/iot/docs/how-tos/mqtt-bridge
  Download Googles CA certificates for "mqtt.googleapis.com" to D:\CERT
  The complete Google root CA 
    https://pki.goog/roots.pem
    https://cloud.google.com/iot/docs/how-tos/mqtt-bridge#using_a_long-term_mqtt_domain
  Download long-term primary and backup for "mqtt.2030.ltsapis.goog" to D:\CERT
    https://pki.goog/gtsltsr/gtsltsr.crt
    https://pki.goog/gsr4/GSR4.crt
  Convert to PEM and split at one file "google_long_ca.pem"

*/

#define GOOGLE_DEVICE           "device_007"
#define GOOGLE_LOCATION         "europe-west1"
#define GOOGLE_PROJECT          "top-suprstate-123456"
#define GOOGLE_REGISTRY         "test_reg"
#define GOOGLE_CLIENT           "projects/" GOOGLE_PROJECT "/locations/" GOOGLE_LOCATION "/registries/" GOOGLE_REGISTRY "/devices/" GOOGLE_DEVICE

//for Azure Sphere: empty
#define CERT_PATH               ""

//#define USE_LONG_TERM

#ifndef USE_LONG_TERM
#define MQTT_HOST_NAME          "mqtt.googleapis.com" 
#define GOOGLE_CA_LIST          CERT_PATH "google_roots.pem"
#else
#define MQTT_HOST_NAME          "mqtt.2030.ltsapis.goog"
#define GOOGLE_CA_LIST          CERT_PATH "google_long_ca.pem"
#endif

#define GOOGLE_CIPHERS          "ECDHE-ECDSA-AES128-GCM-SHA256"

#define MQTT_USER_NAME          "unused"
#define MQTT_PORT               8883
#define API_PORT                443

/* 
    To get the private key run (where private-key.pem is the ec private key
    used to create the certificate uploaded to google cloud iot):
        openssl ec -in <private-key.pem> -noout -text
    and copy priv: part.
    
    The key length should be exactly the same as the key length bellow (32 pairs
    of hex digits). If it's bigger and it starts with "00:" delete the "00:". If
    it's smaller add "00:" to the start. If it's too big or too small something
    is probably wrong with your key.
*/
#define PRIVATE_KEY             "6e:b8:17:35:c7:fc:6b:d7:a9:cb:cb:49:7f:a0:67:"\
                                "63:38:b0:90:57:57:e0:c0:9a:e8:6f:06:0c:d9:ee:"\
                                "31:41"

#define TOPIC_EVENTS            "/devices/" GOOGLE_DEVICE "/events"


//https://cloud.google.com/iot/docs/how-tos/http-bridge
//https://cloud.google.com/iot/docs/reference/cloudiotdevice/rest/v1/projects.locations.registries.devices/publishEvent
#define GOOGLE_URL              "https://cloudiotdevice.googleapis.com/v1/"\
                                "projects/"     GOOGLE_PROJECT\
                                "/locations/"   GOOGLE_LOCATION\
                                "/registries/"  GOOGLE_REGISTRY\
                                "/devices/"     GOOGLE_DEVICE\
                                ":publishEvent"

