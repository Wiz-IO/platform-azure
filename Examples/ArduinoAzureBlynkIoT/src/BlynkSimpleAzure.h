/**
 * @file       BlynkSimple_WizIO.h
 * @author     Volodymyr Shymanskyy
 * @license    This project is released under the MIT License (MIT)
 * @copyright  Copyright (c) 2015 Volodymyr Shymanskyy
 * @date       Jul 2015
 * @brief
 *
 */

#ifndef BlynkSimple_WizIO_h
#define BlynkSimple_WizIO_h

#ifndef BLYNK_INFO_DEVICE
#define BLYNK_INFO_DEVICE "AzureSphere"
#endif

// cause this causes crashes...
//#define BLYNK_NO_YIELD

//#include <BlynkApiArduino.h>
#include <Blynk/BlynkProtocol.h>
#include <BlynkAzureClient.h>
#include <wifiClient.h>

class BlynkWizIO
    : public BlynkProtocol<Blynk_WizIO_Client>
{
    typedef BlynkProtocol<Blynk_WizIO_Client> Base;

public:
    BlynkWizIO(Blynk_WizIO_Client &transp)
        : Base(transp)
    {
    }

    void config(const char *auth,
                const char *domain = BLYNK_DEFAULT_DOMAIN,
                uint16_t port = BLYNK_DEFAULT_PORT)
    {
        Base::begin(auth);
        this->conn.begin(domain, port);
    }

    void config(const char *auth,
                IPAddress ip,
                uint16_t port = BLYNK_DEFAULT_PORT)
    {
        Base::begin(auth);
        this->conn.begin(ip, port);
    }

    void begin(const char *auth, const char *domain = BLYNK_DEFAULT_DOMAIN, uint16_t port = BLYNK_DEFAULT_PORT)
    {
        BLYNK_LOG("Blynk begin");
        config(auth, domain, port);
        BLYNK_LOG("Connecting...");
        while (this->connect() != true)
        {
        }
        BLYNK_LOG("Connected");
    }
};

static wifiClient _blynkClient;
static Blynk_WizIO_Client _blynkTransport(_blynkClient);
BlynkWizIO Blynk(_blynkTransport);

#include <BlynkWidgets.h>

#endif
