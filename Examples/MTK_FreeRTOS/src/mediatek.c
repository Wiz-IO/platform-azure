/*  
    Azure Sphere 2019 Georgi Angelov
        https://github.com/Wiz-IO/platform-azure
        http://www.wizio.eu/

    OPEN: 'platformio.ini' and edit your settings
    OPEN: 'src/app_manifest.json' and enter your 'Capabilities'
 */

#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <FreeRTOS.h>
#include <task.h>
#include <mt3620.h>
#include <os_hal_uart.h>
#include <os_hal_gpio.h>

void __attribute__((weak)) LogToUart(const char *format, ...);

#define LED_GREEN 9  

const uint8_t uart_port_num = UART_ISU_0;

int is_open_debug_uart = 0;

void mon_putchar(char c) /* for printf */
{
    if (is_open_debug_uart)
        mtk_os_hal_uart_put_char(uart_port_num, c);
}

void vTaskPrint(void *pvParameters)
{
    printf("TASK PRINT SETUP\n");
    for (;;)
    {
        vTaskDelay(5000);
        printf("\nLOOP %lu\n", xTaskGetTickCount());
    }
}

void vTaskBlink(void *pvParameters)
{  
    printf("TASK BLINK SETUP\n");
    static bool led = false;
    mtk_os_hal_gpio_request(LED_GREEN);
    mtk_os_hal_gpio_set_direction(LED_GREEN, 1);
    for (;;)
    {
        vTaskDelay(500);
        mtk_os_hal_gpio_set_output(LED_GREEN, led);
        led = !led;
        printf("BEEP ");
    }
}

void MAIN(void *pvParameters)
{
    setvbuf(stdout, NULL, _IONBF, 0); // unbuffer printf
    printf("TASK MAIN\n");
    xTaskCreate(vTaskPrint, "vTaskPrint", 500, (void *)NULL, tskIDLE_PRIORITY, NULL);
    xTaskCreate(vTaskBlink, "vTaskBlink", 500, (void *)NULL, tskIDLE_PRIORITY, NULL);
    for (;;)
        __asm__("wfi");
}

void RTCoreMain(void)
{
    NVIC_SetupVectorTable();
    mtk_os_hal_gpio_ctlr_init();
    is_open_debug_uart = mtk_os_hal_uart_ctlr_init(uart_port_num) ? 0 : 1;
    mtk_os_hal_uart_put_str(uart_port_num, "Azure Sphere M4F FreeRTOS 2019 Georgi Angelov\n");
    xTaskCreate(MAIN, "MAIN", configMINIMAL_STACK_SIZE, (void *)NULL, tskIDLE_PRIORITY, NULL);
    vTaskStartScheduler();
}

void vApplicationMallocFailedHook(void)
{
    LogToUart("[ERROR] Malloc Failed\n");
    taskDISABLE_INTERRUPTS();
    abort();
}

void vAssertCalled(unsigned long ulLine, const char *const pcFileName)
{
    LogToUart("[ASSERT] (%ld) %s\n", ulLine, pcFileName);
    volatile unsigned long ul = 0;
    taskENTER_CRITICAL();
    {
        while (ul == 0)
        {
            __asm volatile("NOP");
        }
    }
    taskEXIT_CRITICAL();
}
