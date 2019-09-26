/*
  PlatformIO - Arduino 2019 Georgi Angelov
    https://github.com/Wiz-IO/platform-azure
    http://www.wizio.eu/

  Modification of: https://github.com/cesanta/v7      

  Javascript 'test.js' is packed to application image as read-only. 
  Can be used MutableStorage

  Need: EXPERIMENTAL MODE, read here:
    https://github.com/Wiz-IO/platform-azure/wiki/Arduino-INI-file#experimental-mode  
 */

#include <Arduino.h>
#include <applibs/storage.h>
#include "v7.h"
struct v7 *v7;

static v7_val_t js_wait(struct v7 *v7)
{
  v7_val_t pinv = v7_arg(v7, 0);
  double d = v7_get_double(v7, v7_arg(v7, 0)) * 1000;
  delay((uint32_t)d);
  return 0;
}

void js_init(struct v7 *v7)
{
  v7_val_t global = v7_get_global(v7);
  v7_set_method(v7, global, "wait", js_wait);
}

void setup()
{
  Serial.begin(115200);
  Serial.println("Azure Sphere JavaScript 2019 Georgi Angelov");
  Serial.redirect(stderr);
  Serial.redirect(stdout);

  Serial.printf("[JAVA] BEGIN");
  v7 = v7_create();
  js_init(v7);
  v7_val_t exec_result;

  /* Load from file*/
  char *scrypt = Storage_GetAbsolutePathInImagePackage("test.js");
  v7_err err = v7_exec_file(v7, scrypt, &exec_result);

  Serial.printf("[JAVA] END ( %d )", err);
}

void loop()
{
  sleep(1);
}