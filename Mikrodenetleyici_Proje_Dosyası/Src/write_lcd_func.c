#include "write_lcd_func.h"
#include "ssd1306.h"
#include "esp8266.h"
#include <string.h>

char cache_ssid[100];
extern char* ssid;

void send_intro_lcd(void){
		ssd1306_Init();
		ssd1306_Fill(Black);
    ssd1306_SetCursor(20, 0);
    ssd1306_WriteString("Gebze Technical", Font_7x10, White);
		ssd1306_SetCursor(35, 10);
    ssd1306_WriteString("University", Font_7x10, White);
		ssd1306_SetCursor(20, 30);
    ssd1306_WriteString("Electronics", Font_7x10, White);
		ssd1306_SetCursor(35, 40);
    ssd1306_WriteString("Engineering", Font_7x10, White);
		ssd1306_UpdateScreen();
		HAL_Delay(1000);
		
		ssd1306_Fill(Black);
		ssd1306_SetCursor(35, 0);
    ssd1306_WriteString("The Final", Font_7x10, White);
		ssd1306_SetCursor(50, 10);
    ssd1306_WriteString("Project", Font_7x10, White);
		ssd1306_SetCursor(35, 25);
		ssd1306_WriteString("- 2019 -", Font_7x10, White);
		ssd1306_SetCursor(30, 40);
    ssd1306_WriteString("Serhat SEFER", Font_7x10, White);
		ssd1306_SetCursor(45, 50);
    ssd1306_WriteString("141024040", Font_7x10, White);
		ssd1306_UpdateScreen();
		HAL_Delay(1000);
		ssd1306_Fill(Black);
		ssd1306_SetCursor(20, 30);
    ssd1306_WriteString("Initializing...", Font_7x10, White);
		ssd1306_UpdateScreen();
		strcat(cache_ssid,ssid);
	}

	
void send_connected_lcd(void)
{
	
					ssd1306_Fill(Black);
					ssd1306_SetCursor(10, 10);
					ssd1306_WriteString("Connected To", Font_7x10, White);
					ssd1306_SetCursor(15, 20);
					ssd1306_WriteString("WIFI!", Font_7x10, White);
					ssd1306_SetCursor(10, 30);
					ssd1306_WriteString("Can Connect To", Font_7x10, White);
					ssd1306_SetCursor(15, 40);
					ssd1306_WriteString("Device With", Font_7x10, White);
					ssd1306_SetCursor(15, 50);
					ssd1306_WriteString("AP Or Stat. Mode", Font_7x10, White);
					ssd1306_UpdateScreen();
	
}

void send_not_connected_lcd(void)
{

					ssd1306_Fill(Black);
					ssd1306_SetCursor(10, 10);
					ssd1306_WriteString("Not Connected", Font_7x10, White);
					ssd1306_SetCursor(15, 20);
					ssd1306_WriteString("To WIFI!", Font_7x10, White);
					ssd1306_SetCursor(10, 30);
					ssd1306_WriteString("Can Connect To", Font_7x10, White);
					ssd1306_SetCursor(15, 40);
					ssd1306_WriteString("Device With", Font_7x10, White);
					ssd1306_SetCursor(15, 50);
					ssd1306_WriteString("Only AP Mode", Font_7x10, White);
					ssd1306_UpdateScreen();
	
}

void send_ready_lcd(void)
{
		ssd1306_Fill(Black);
		ssd1306_SetCursor(10, 10);
    ssd1306_WriteString("Device Is Ready!", Font_7x10, White);
		ssd1306_SetCursor(10, 30);
		ssd1306_WriteString("WIFI:", Font_7x10, White);
		ssd1306_SetCursor(50, 30);
	extern int status_wifi;
		if (status_wifi == 1){
		ssd1306_WriteString(cache_ssid, Font_7x10, White);
	  ssd1306_SetCursor(10, 50);
		ssd1306_WriteString("Mode:AP+STA", Font_7x10, White);
		}
		else
		{
		ssd1306_WriteString("Not Connect", Font_7x10, White);
		ssd1306_SetCursor(10, 50);
		ssd1306_WriteString("Mode:AP", Font_7x10, White);
		}
		ssd1306_UpdateScreen();
}

void send_payment_successful(void)
{

		ssd1306_Fill(Black);
		ssd1306_SetCursor(10, 10);
    ssd1306_WriteString("Payment", Font_7x10,White);
		ssd1306_SetCursor(10, 25);
    ssd1306_WriteString("Has Been", Font_7x10,White);
		ssd1306_SetCursor(10,40);
    ssd1306_WriteString("Successfull!", Font_7x10,White);
		ssd1306_UpdateScreen();
	
}

void send_payment_unsuccessful(void)
{

		ssd1306_Fill(Black);
		ssd1306_SetCursor(10, 10);
    ssd1306_WriteString("Payment", Font_7x10,White);
		ssd1306_SetCursor(10, 25);
    ssd1306_WriteString("Has Been", Font_7x10,White);
		ssd1306_SetCursor(10,40);
    ssd1306_WriteString("Unsuccessfull!", Font_7x10,White);
		ssd1306_UpdateScreen();
	
}

void send_wifi_disconnected(void)
{
		ssd1306_Fill(Black);
		ssd1306_SetCursor(20, 10);
    ssd1306_WriteString("WIFI WAS", Font_7x10, White);
		ssd1306_SetCursor(35,20);
    ssd1306_WriteString("DISCONNECTED!", Font_7x10, White);
		ssd1306_SetCursor(20, 40);
    ssd1306_WriteString("Trying To", Font_7x10, White);
		ssd1306_SetCursor(35, 50);
    ssd1306_WriteString("Reconnect", Font_7x10, White);
		ssd1306_UpdateScreen();
	
}
