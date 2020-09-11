/**
 *
 * \file
 *
 * \brief FreeRTOS USART driver echo test tasks
 *
 *
 * Copyright (c) 2012-2018 Microchip Technology Inc. and its subsidiaries.
 *
 * \asf_license_start
 *
 * \page License
 *
 * Subject to your compliance with these terms, you may use Microchip
 * software and any derivatives exclusively with Microchip products.
 * It is your responsibility to comply with third party license terms applicable
 * to your use of third party software (including open source software) that
 * may accompany Microchip software.
 *
 * THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES,
 * WHETHER EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE,
 * INCLUDING ANY IMPLIED WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY,
 * AND FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT WILL MICROCHIP BE
 * LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE, INCIDENTAL OR CONSEQUENTIAL
 * LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND WHATSOEVER RELATED TO THE
 * SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS BEEN ADVISED OF THE
 * POSSIBILITY OR THE DAMAGES ARE FORESEEABLE.  TO THE FULLEST EXTENT
 * ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN ANY WAY
 * RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
 * THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
 *
 * \asf_license_stop
 *
 */

/* Standard includes. */
#include <stdio.h>
#include <string.h>
#include <ioport.h>
#include "globais.h"
/* Kernel includes. */
#include "FreeRTOS.h"
#include "task.h"

/* Atmel library includes. */
#include "freertos_usart_serial.h"
/* Demo includes. */
#include "demo-tasks.h"

#if (defined confINCLUDE_USART_ECHO_TASKS)

/* The size of the buffer used to receive characters from the USART driver.
 * This equals the length of the longest string used in this file. */
#define RX_BUFFER_SIZE          (79)

/* The baud rate to use. */
#define USART_BAUD_RATE         (9600)
/*-----------------------------------------------------------*/

/*
 * Tasks used to develop the USART drivers.  One task sends out a series of
 * strings, the other task expects to receive the same series of strings.  An
 * error is latched if any characters are missing.  A loopback connector is
 * required to ensure the transmitted characters are also received.
 */
//static void usart_echo_tx_task(void *pvParameters);
static void usart_echo_rx_task(void *pvParameters);

/*-----------------------------------------------------------*/

/* The buffer provided to the USART driver to store incoming character in. */
static uint8_t receive_buffer[RX_BUFFER_SIZE] = {0};

/* Counts the number of times the Rx task receives a string.  The count is used
to ensure the task is still executing. */
static uint32_t rx_task_loops = 0UL;

/* The array of strings that are sent by the Tx task, and therefore received by
the Rx task. */


const char *estado_atual[] = {"DIS#",
							"SBY#",
							"FWD#",
							"LFT#",
							"RGT#",
							"BAK#",};
static uint8_t local_buffer[RX_BUFFER_SIZE];
StateType SmState;
/*-----------------------------------------------------------*/

void create_usart_echo_test_tasks(Usart *usart_base,
		uint16_t stack_depth_words,
		unsigned portBASE_TYPE task_priority)
{
	freertos_usart_if freertos_usart;
	freertos_peripheral_options_t driver_options = {
		receive_buffer,								/* The buffer used internally by the USART driver to store incoming characters. */
		RX_BUFFER_SIZE,									/* The size of the buffer provided to the USART driver to store incoming characters. */
		configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY,	/* The priority used by the USART interrupts. */
		USART_RS232,									/* Configure the USART for RS232 operation. */
		(USE_TX_ACCESS_SEM | USE_RX_ACCESS_MUTEX)
	};

	const sam_usart_opt_t usart_settings = {
		USART_BAUD_RATE,
		US_MR_CHRL_8_BIT,
		US_MR_PAR_NO,
		US_MR_NBSTOP_1_BIT,
		US_MR_CHMODE_NORMAL,
		0 /* Only used in IrDA mode. */
	}; /*_RB_ TODO This is not SAM specific, not a good thing. */

	/* Initialise the USART interface. */
	freertos_usart = freertos_usart_serial_init(usart_base,
			&usart_settings,
			&driver_options);
	configASSERT(freertos_usart);

	/* Create the two tasks as described above. */
	xTaskCreate(usart_echo_rx_task, (const signed char *const) "Rx",
			stack_depth_words, (void *) freertos_usart,
			task_priority + 1, NULL);
}

/*-----------------------------------------------------------*/

/*-----------------------------------------------------------*/

static void usart_echo_rx_task(void *pvParameters)
{
	freertos_usart_if usart_port;
	static uint8_t rx_buffer[RX_BUFFER_SIZE];
	uint32_t received;

	/* The (already open) USART port is passed in as the task parameter. */
	usart_port = (freertos_usart_if)pvParameters;
	uint8_t poot = 0;
	uint8_t local[RX_BUFFER_SIZE];
	
	
	const portTickType time_out_definition = (100UL / portTICK_RATE_MS);
	xSemaphoreHandle notification_semaphore;
	status_code_t returned_status;

	/* Create the semaphore to be used to get notified of end of
	transmissions. */
	vSemaphoreCreateBinary(notification_semaphore);
	configASSERT(notification_semaphore);

	/* Start with the semaphore in the expected state - no data has been sent
	yet.  A block time of zero is used as the semaphore is guaranteed to be
	there as it has only just been created. */
	xSemaphoreTake(notification_semaphore, 0);
	char result_txt[5] = "0000";
	uint32_t valor_sensor = 0;
	for (;;) {
		memset(rx_buffer, 0x00, sizeof(rx_buffer));
		
		received = freertos_usart_serial_read_packet(usart_port, rx_buffer,
				1,
				portMAX_DELAY);
		
		memcpy(local,rx_buffer,1);
		poot = local[0];
		switch(poot)
		{
			case 'b':
				SmState = STATE_MOVING_REVERSE;
				break;
			case 'f':
				SmState = STATE_MOVING_FORWARD;
				break;
			case 'l':
				SmState = STATE_TURNING_LEFT;
				break;
			case 'r':
				SmState = STATE_TURNING_RIGHT;
				break;
			default:
				SmState = STATE_STANDBY;
				break;
		}
		taskENTER_CRITICAL();
		// Get latest digital data value from ADC and can be used by application
		sprintf(result_txt,"%lu;%d;%d;%d;%d;%d;%d;%s",result_adc,
		ioport_get_pin_level(SENSOR_ESQUERDA),
		ioport_get_pin_level(SENSOR_FRENTE),
		ioport_get_pin_level(SENSOR_SAIDA),
		ioport_get_pin_level(SENSOR_DIREITA),
		ioport_get_pin_level(SENSOR_TRAS1), ioport_get_pin_level(SENSOR_TRAS2),
		estado_atual[SmState] );
		taskEXIT_CRITICAL();
		strcpy((char *) local_buffer,
		(const char *) result_txt);
		/* Data cannot be sent from Flash, so copy the string to RAM. */

		/* Start send. */
		returned_status = freertos_usart_write_packet_async(usart_port,
		local_buffer, strlen((char *) local_buffer),
		time_out_definition, notification_semaphore);
		configASSERT(returned_status == STATUS_OK);
		
		
		xSemaphoreTake(notification_semaphore, time_out_definition * 2);
		
		///Enviar pos comand
		//strcpy((char *) local_buffer,
		//(const char *) estado_atual[SmState]);

		/* The async version of the write function is being used, so wait for
		the end of the transmission.  No CPU time is used while waiting for the
		semaphore.*/
		
		/* Expect the next string the next time around. */
		
	}
}
/*-----------------------------------------------------------*/

portBASE_TYPE are_usart_echo_tasks_still_running(void)
{
	static uint32_t last_loop_count = 0;
	portBASE_TYPE return_value = pdPASS;

	/* Ensure the count of Rx loops is still incrementing. */
	if (last_loop_count == rx_task_loops) {
		/* The Rx task has somehow stalled, set the error LED. */
		return_value = pdFAIL;
	}

	last_loop_count = rx_task_loops;

	return return_value;
}

/*-----------------------------------------------------------*/

#endif
