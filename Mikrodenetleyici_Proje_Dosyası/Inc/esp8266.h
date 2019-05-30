/*
 ************************************  ESP8266 Kütüphanesi ************************************
 *									   									-> HEADER FILE <-
 *
 *                                   | 2019 SERHAT SEFER | 
 *									   								 serhatsefer.cf
 */

#ifndef ESP8266_DEFINE
#define ESP8266_DEFINE

#include "stm32f1xx_hal.h"
#include "write_lcd_func.h"
#include "servo.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>



//------------------------------------------------

#define RX_BUFFER_SIZE 50
#define TX_BUFFER_SIZE 1500
// -------- LED PINLERI ---------

#define BeyazLed1				GPIO_PIN_0
#define BeyazLed2				GPIO_PIN_1
#define MaviLed1        GPIO_PIN_2
#define MaviLed2        GPIO_PIN_3
#define KirmiziLed1     GPIO_PIN_4
#define KirmiziLed2     GPIO_PIN_5

// --------------------------------

extern TIM_HandleTypeDef htim4;


void ESP_Init(void);
void ESP_Read(void);
void ESP_Login(void);
void ESP_TCP(void);
void clear_response(void);
void clear_rcvbuffer(void);
char* Send_ESP(char*data,int delay);
char* Send_ESP_Conc(char*data,int length,int delay);
char* Send_ESP_Connect(const char*ssid,const char*pass,int delay);
char* Get_IP(void);




// -------- HTML KODLARI ---------

static const  char* successful_msg = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n\
		<!DOCTYPE html>\
		<html><body><center><h2><b>Successful!</b><br></h2>Payment Has Been Successful!</center></body></html>\r\n\
		";

static const  char* unsuccessful_msg = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n\
		<!DOCTYPE html>\
		<html><body><center><h2><b>Error!</b></h2><br>Payment Has Been Unsuccessful!</center></body></html>\r\n\
		";

static const char* reset_msg = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n\
		<!DOCTYPE html>\
		<html><body><center>STM32 Yeniden Baslatildi!</center></body></html>\r\n\
		";

static const char* login_msg = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n\
	<!DOCTYPE html> \
	<html> \
	<body> \
	<body bgcolor =\"#ccd9ff\"> \
	<title>ESP8266 - Please Enter SSID & Pass</title> \
	<header> \
	<center> \
  <h2> <b>Gebze Technical University</b> </h2> \
	<h3> <b>Department Of Electronics Engineering</b> </h3> \
	<h3> <b>The Final Project</b> </h3> \
	&nbsp;\
	&nbsp;\
	&nbsp;\
	&nbsp;\
	&nbsp;\
	&nbsp;\
	<h3> <b><span style=\"color: #ff0000;\">WIFI Network Can Not Find Or No Connection!</span></b> </h3> \
	<h3> <b><span style=\"color: #ff0000;\">Please Enter The SSID And Password To Connect.</span></b> </h3></center> \
	</header> \
	&nbsp;\
	<form action = \"\" method = \"get\"> \
	<center><table border = \"1\"><span style = \"color : #000000;\"><tr><td>WIFI SSID : &nbsp &nbsp &nbsp &nbsp </td><td><input type = \"text\" name = \"ssid\" value = \"\"><br></td></tr></center> \
	<center><tr><td>WIFI Password : </td><td><input type = \"text\" name = \"pass\" value = \"\"><br></td></tr></center> \
	</tbody> \
	</table> \
	<br><center><input type = \"submit\" value = \"Save & Connect\"></center> \
	<br><br> \
	</form> \
	<center>  <h3> <b>2019 Serhat SEFER.</b></h3></center> \
	<center>  <h3> <b>Copyright All Reserved.</b></h3></center> \
	</body> \
	</html> \
	";
	
#endif
