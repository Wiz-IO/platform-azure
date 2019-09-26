/*  
    PlatformIO 2019 Georgi Angelov
        https://github.com/Wiz-IO
        http://www.wizio.eu/
 */

#include <errno.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#define UART_STRUCTS_VERSION 1
#include <applibs/uart.h>
#include <applibs/log.h>

int uartFd = -1;

void redirect(int fd, void *file)
{
    int *p = (int *)((char *)file + 60);
    *p = fd;
}

void open_uart(int N)
{
    UART_Config uartConfig;
    UART_InitConfig(&uartConfig);
    uartConfig.baudRate = 115200;
    uartConfig.flowControl = UART_FlowControl_None;
    uartFd = UART_Open(N, &uartConfig);
    if (uartFd > 0)
    {
        redirect(uartFd, stderr);
        redirect(uartFd, stdout);
        Log_Debug("Log_Debug\n");
        printf("printf %d\n", 42);
    }
}

int main(int argc, char *argv[])
{
    open_uart(4);
    Log_Debug("Azure Sphere PlatformIO 2019 WizIO\n");
    Log_Debug("Hello World\n");
    while (1)
    {
        Log_Debug("Ping ");
        sleep(5);
        printf("Pong\n");
        sleep(1);
    }
    return 0;
}