/*  
    Azure Sphere 2019 Georgi Angelov
        https://github.com/Wiz-IO/platform-azure
        http://www.wizio.eu/

    OPEN: 'platformio.ini' and edit your settings
    OPEN: 'src/app_manifest.json' and enter your 'Capabilities'
 */

#include <stdio.h>
#include <stdarg.h>

#include "mt3620.h"
#include <os_hal_uart.h>
#include <os_hal_gpt.h>

/******************************************************************************/
/* Configurations */
/******************************************************************************/
static const uint8_t uart_port_num = UART_ISU_0;
static const uint8_t gpt_timer_id = GPT_ID_0;
static const uint32_t gpt_timer_val = 500; // 500ms
static const char *gpt_cb_data = "Hello World";
#define MAX_UART_LOG_BUFFER 64

/******************************************************************************/
/* Functions */
/******************************************************************************/
void unused(void) {}
static void LogToUart(const char *format, ...)
{
	static char print_buffer[MAX_UART_LOG_BUFFER] = {0};
	va_list arg;

	va_start(arg, format);
	memset(print_buffer, 0, sizeof(print_buffer));
	vsnprintf(print_buffer, MAX_UART_LOG_BUFFER, format, arg);
	va_end(arg);

	mtk_os_hal_uart_put_str(uart_port_num, print_buffer);
}

static void Gpt0Callback(void *cb_data)
{
	static uint8_t print_counter = 0;

	LogToUart("%s %d\r\n", (char *)cb_data, print_counter);
	print_counter++;
}

_Noreturn void RTCoreMain(void)
{
	struct os_gpt_int gpt0_int;

	// Init Vector Table
	NVIC_SetupVectorTable();
	STD_Init();

	// Init UART
	mtk_os_hal_uart_ctlr_init(uart_port_num);
	LogToUart("UART Inited (port_num=%d)\r\n", uart_port_num);

	// Init GPT
	gpt0_int.gpt_cb_hdl = Gpt0Callback;
	gpt0_int.gpt_cb_data = (void *)gpt_cb_data;
	mtk_os_hal_gpt_init();

	//	configure GPT0 clock speed (as 1KHz) and register GPT0 user interrupt callback handle and user data.
	mtk_os_hal_gpt_config(gpt_timer_id, false, &gpt0_int);
	//	configure GPT0 timeout value (as 500ms) and configure it as repeat mode.
	mtk_os_hal_gpt_reset_timer(gpt_timer_id, gpt_timer_val, true);
	//	start timer
	mtk_os_hal_gpt_start(gpt_timer_id);
	LogToUart("GPT0 Started (timer_id=%d)(timer_val=%dms)\r\n", gpt_timer_id, gpt_timer_val);

	for (;;)
	{
		__asm__("wfi");
	}
}
