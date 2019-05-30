
#ifndef WRITE_LCD_FUNCTIONS
#define WRITE_LCD_FUNCTIONS

#include "ssd1306.h"
#include "esp8266.h"

void send_intro_lcd(void);
void send_connected_lcd(void);
void send_not_connected_lcd(void);
void send_ready_lcd(void);
void send_payment_successful(void);
void send_payment_unsuccessful(void);
void send_wifi_disconnected(void);

#endif
