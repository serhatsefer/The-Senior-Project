/*************************************  ESP8266 Kütüphanesi ************************************
 *                                     -> SOURCE FILE <-
 *
 *                                   | 2019 SERHAT SEFER |  
 *									    						 serhatsefer.cf
 * 
 *     -KULLANIM:
 *      Kütüptanede 6 adet LED tanimlanmistir.Bu LED'lder A portunun 0,1,2,3,4 ve 5. pinlerine baglanmistir.
 *		Pinlerdeki LED Renkleri Su Sekilde Olmalidir:
 *		A0 , A1 -> Beyaz
 *		A2 , A3 -> Mavi
 *		A4 , A5 -> Kirmizi
 *		
 *	   LED'lerin Pinlerini LED PINLERI Kismindan Degistirebilirsiniz.
 *		
 *     LED'lerin Pinlerini LED PINLERI Kismindan Degistirebilirsiniz.      
 *     ESP_Init() Fonksiyonu ESP8266'yi Hazirlar Ve WIFI Agina Baglanir.
 *     clear_rcvbuffer() Fonksiyonu Rx_Buffer'i Temizler.
 *     ESP_Read() Fonksiyonu Gelen HTTP Istegini Okur Ve Gelen Istege Göre LED yakar.
 *
 **/


// -- Gerekli Kütüphaneler Ve Degiskenler Eklendi. ---

#include "esp8266.h"


// Bool Tanimi
enum bool {false=0,true=1};

// --- Baglanilacak WIFI Aginin SSID Ve Sifresi ---
const char* ssid="Serhat3";
const char* pass="-trworld19962009-";

// --- Daha Sonra Kullanilacak Degiskenler Tanimlandi. ---
char Rx_Buffer[RX_BUFFER_SIZE],buffer[TX_BUFFER_SIZE],veriuzunluk[4];
char *htmlcode,*read_ok,*read_error,*stat,*reset,*login,*successful,*unsuccessful,*connection,*apip,*id,*test,*ip,*asd = "";
uint8_t Rx_data = '\0';
int status_wifi,last,uzunluk;
char ip_[30];
int status = 0;
UART_HandleTypeDef huart1;
UART_HandleTypeDef huart3;

int ok = 0;
static int Rx_indx,check = 0;


// --- Gelen Datayi Okur Ve Geçici Buffer'a Atar. ---

void HAL_UART_RxCpltCallback(UART_HandleTypeDef*huart)
{	
	//__HAL_UART_FLUSH_DRREGISTER(&huart1);
	if (huart->Instance == USART1)
	{	
	
		if( (Rx_data != '\n') && (Rx_indx < RX_BUFFER_SIZE))
		//if ( (check == 0)  && (Rx_indx < 250))																			// CR degilse datayi al
		{
			
			Rx_Buffer[Rx_indx++] = Rx_data;
			//USART1->DR = Rx_data;
		}
		else
		{
			//Rx_Buffer[Rx_indx-1] = 0;
			Rx_Buffer[Rx_indx-1] = '\0';
			Rx_indx = 0;
		}
	
 // read_ok		 = strstr(Rx_Buffer, "OK");
//	read_error = strstr(Rx_Buffer,"ERROR"); 
	stat 	 = strstr(Rx_Buffer, "WIFI DISCONNECT");
//	test 	 = strstr(Rx_Buffer,"?ssid=");
//	login 	 = strstr(Rx_Buffer, "/login HTTP/1.1");
	reset  = strstr(Rx_Buffer, "/reset HTTP/1.1");
	successful = strstr(Rx_Buffer,"/successful HTTP/1.1");
	unsuccessful = strstr(Rx_Buffer,"/unsuccessful HTTP/1.1");
	
}
	HAL_UART_Receive_IT(&huart1, &Rx_data, 1);
}




// --- Rx_Buffer'ini Temizler. ---

void clear_rcvbuffer(void)
{
	memset(Rx_Buffer,0,RX_BUFFER_SIZE);
	Rx_indx = 0;

}

char* Send_ESP(char*data,int delay)
{
	strcpy(buffer,data);
	strcat(buffer,"\r\n");
	uzunluk=strlen(buffer)+1;
	HAL_UART_Transmit_IT(&huart1, (uint8_t*) buffer, uzunluk+1);
	read_ok = strstr(Rx_Buffer, "OK");
	HAL_Delay(delay);
	
	
	return read_ok;
}

char* Send_ESP_Conc(char*data,int length,int delay)
{
	strcpy(buffer,data);
	sprintf(veriuzunluk, "%d",length);
	strcat(buffer,veriuzunluk);
	strcat(buffer, "\r\n");
	uzunluk = strlen(buffer)+1;
	HAL_UART_Transmit_IT(&huart1, (uint8_t*) buffer, uzunluk);
	read_ok = strstr(Rx_Buffer, "OK");
	HAL_Delay(delay);

	
	return read_ok;
}

char* Send_ESP_Connect(const char* ssid,const char* pass,int delay)
{
			strcpy(buffer, "AT+CWJAP=\"");
			strcat(buffer, ssid);
			strcat(buffer, "\",\"");
			strcat(buffer, pass);
			strcat(buffer, "\"\r\n");
			uzunluk = strlen(buffer);
			HAL_UART_Transmit_IT(&huart1, (uint8_t*) buffer, uzunluk);
			read_ok = strstr(Rx_Buffer, "OK");
			HAL_Delay(delay);

	
			return read_ok;
}

void Close_Connection(void){
	for (int i = 0 ; i < 5; i++){
		Send_ESP_Conc("AT+CIPCLOSE=",i,1000);
		}
}

char* Get_IP(void)
{
	int i = 0;
	char *p,*c;
	Send_ESP("AT+CIFSR",0);
	ip = strstr(Rx_Buffer,"STAIP");
	p = strtok(ip,"\"");
	p = strtok(NULL,"\"");
	while(*ip){
			ip_[i] = *ip;
			ip++;
			i++;
	}
	

	//c = strtok(NULL,"\"");
	//p = strtok(p,"a");
	//p = *(&ip + strlen(p));
/*
	while(*p)
		{
			ip_[i] = *p;
			p++;
			i++;
		}
*/	

	return ip;
}	

/* ESP8266'yi Hazirlar Ve WIFI Agina Baglar.Eger WIFI SSID Ve Sifresi Daha Önce Tanimlanmamissa 
   ESP8266 HOTSPOT olarak yayin yapar ve kendi web arayüzü üzerinden WIFI'in SSID ve sifresi girilmesi istenir.
*/

	void ESP_Init(void)
{
	
	initServo(htim4);
	status_wifi=0;
	HAL_GPIO_WritePin(GPIOA,KirmiziLed1,GPIO_PIN_SET);
	
	
	// *********** ESP8266'yi Resetler. ***********	
	Send_ESP("AT+RST",1000);

	// ************ Otomatik Baglantiyi Devredisi Birak ****************
	while(Send_ESP("AT+CWAUTOCONN=0",1000) == NULL );
	clear_rcvbuffer();
	
	// *********** ESP8266'yi SoftAP + Station Moduna Ayarlar. ***********
	while(Send_ESP("AT+CWMODE=3",500) == NULL );
	clear_rcvbuffer();
	
	// *********** SSID Ve Sifresi Belirtilen WIFI Agina Baglanir. ***********
  // 				WIFI Agina Baglandiginda A Portunun 4.Pinindeki LED Yanar.
	int counter = 0;
	if(ssid != NULL && pass != NULL)
	{
		do
		{
				connection = Send_ESP_Connect(ssid,pass,7000);
	  		counter++;
			if (connection != NULL){
				status_wifi = 1;
				HAL_GPIO_WritePin(GPIOA,KirmiziLed1,GPIO_PIN_RESET);
				send_connected_lcd();
			}
			if (counter == 5){
				status_wifi = 0;
				HAL_GPIO_WritePin(GPIOA,KirmiziLed1,GPIO_PIN_SET);
				send_not_connected_lcd();
				break;
			}
		} while (connection == NULL) ;		
	}
	
	clear_rcvbuffer();
	

	
	// *********** ESP8266'nin AP Modunun WIFI Adini Ve Sifresini Ayarlar. ***********
	while(Send_ESP("AT+CWSAP_DEF=\"Serhat_ESP\",\"serhatsefer\",5,4",500) == NULL);
	clear_rcvbuffer();
	// *********** Baglanilan Agdan Alinan IP Adresini Gösterir. ***********
	while(Get_IP() == NULL);
	//clear_rcvbuffer();
	// *********** Çoklu Baglantilara Izin Verir. ***********
	while(Send_ESP("AT+CIPMUX=1",500) == NULL);
	clear_rcvbuffer();
	// *********** WIFI Agi Tarafindan ESP8266'ya Verilen IP Adresinin 80.Portuna Server Kurar. ***********
	while(Send_ESP("AT+CIPSERVER=1,80",500) == NULL);
	clear_rcvbuffer();
	// *********** TCP Modunda Maksimum Baglanti Suresini Ayarlar ***********
	while(Send_ESP("AT+CIPSTO=5000",500) == NULL);
	clear_rcvbuffer();
	//  *********** LCD'ye Cihazin Hazir Oldugunu Yazdirir. ***********
	send_ready_lcd();
	
}
	
	// ***************************************************************************

/*  Veri Okur.Eger ESP'nin WIFI Agindan Aldigi IP Adresinin Sonuna
 *  /beyaz komutu geliyorsa beyaz led yanar.
 *  /kirmizi komutu geliyorsa kirmizi led yanar.
 *  /mavi komutu geliyorsa kirmizi led yanar.
 *  /kapat komutu geliyorsa tüm ledler söner.
 *    
 *	Örnek Kullanim: 192.168.1.1/beyaz  , 192.168.1.1/mavi    
 *	*NOT:192.168.1.1 Ip Adresi Örnek Içindir.Sizin ESP8266'nin IP Adresini Modem Arayüzünden
 *	Ya Da AT Komutlari Yardimiyla Ögrenmeniz Gerekmektedir.
 **/

void ESP_Read(void)
{
	
	if(successful != NULL)
	{
	
		HAL_GPIO_WritePin(GPIOA,MaviLed1,GPIO_PIN_SET);
		
		send_payment_successful();
		openCover(htim4);
		
		uzunluk = strlen(successful_msg)+1;
		Send_ESP_Conc("AT+CIPSEND=0,",uzunluk,100);
		Send_ESP((char*)successful_msg,200);
		while(strstr(Rx_Buffer,"SEND OK") == NULL);
    clear_rcvbuffer();
		HAL_Delay(500);
		Close_Connection();
		clear_rcvbuffer();
		Send_ESP("AT+CIPSERVER=1,80",500);
		clear_rcvbuffer();

		
		HAL_GPIO_WritePin(GPIOA,MaviLed1,GPIO_PIN_RESET);
		closeCover(htim4);
		send_ready_lcd();
	
		
	}

	else if(unsuccessful != NULL)
	{
	
		HAL_GPIO_WritePin(GPIOA,KirmiziLed1,GPIO_PIN_SET);
		send_payment_unsuccessful();
		
		uzunluk = strlen(unsuccessful_msg);
		Send_ESP_Conc("AT+CIPSEND=0,",uzunluk,100);
		Send_ESP((char*)unsuccessful_msg,200);	
		HAL_Delay(500);
		Close_Connection();
		clear_rcvbuffer();
		Send_ESP("AT+CIPSERVER=1,80",500);
	
	
		clear_rcvbuffer();

		HAL_GPIO_WritePin(GPIOA,KirmiziLed1,GPIO_PIN_RESET);
		send_ready_lcd();
	
		
	}

	// eger WIFI baglantisi koptuysa kirmizi ledleri yak ve aga tekrar baglanmaya çalis.
	else if(stat != NULL) {
		
		send_wifi_disconnected();
		clear_rcvbuffer();
		status_wifi=0;
		HAL_GPIO_WritePin(GPIOA,KirmiziLed1,GPIO_PIN_SET);
		ESP_Init();
	}


	 else if(reset != NULL)
	{

		HAL_GPIO_WritePin(GPIOA, BeyazLed1 | BeyazLed2 |  MaviLed1 | MaviLed2 | KirmiziLed2, GPIO_PIN_RESET); 
		uzunluk = strlen(reset_msg);
		Send_ESP_Conc("AT+CIPSEND=0,",uzunluk,100);
		Send_ESP((char*)reset_msg,200);

		while(Send_ESP("AT+CIPCLOSE=5",20) == NULL);
		HAL_Delay(1000);
		NVIC_SystemReset();
	}		

	else if(login != NULL)
	{
		HAL_GPIO_WritePin(GPIOA, BeyazLed2 | MaviLed1 | MaviLed2 | BeyazLed1, GPIO_PIN_RESET); 
		ESP_Login();
	}
        	
	else if (test != NULL)
	{
		id=strstr(test,"&pass");
    last = id - test;
		memcpy(asd,test+6,12);
		HAL_Delay(100);
		ESP_Login();
		
	}

	
//-------------------- ESP_Read() Fonksiyon Sonu --------------------
}

// --- WIFI Agina Baglanmak Icin WIFI SSID Ve Sifresinin Girildigi Bir HTML Arayüzü Olusturur. ---

void ESP_Login(void)
{
	uzunluk = strlen(login_msg);
	
		Send_ESP_Conc("AT+CIPSEND=0,",uzunluk,300);
	//}while(strstr(Rx_Buffer,">") == NULL);
	
		Send_ESP((char*)login_msg,1000);
		//clear_rcvbuffer();
	do{
		clear_rcvbuffer();
	}
	while(Send_ESP("AT+CIPCLOSE=5",100) == NULL);

//	while(Send_ESP("AT+CIPMUX=1",500) == NULL);
	clear_rcvbuffer();
	// *********** WIFI Agi Tarafindan ESP8266'ya Verilen IP Adresinin 80.Portuna Server Kurar. ***********
	do{
		clear_rcvbuffer();
	}
	while(Send_ESP("AT+CIPSERVER=1,80",500) == NULL);
	clear_rcvbuffer();

}


void ESP_TCP(void){

	htmlcode="\
	POST /test.php HTTP/1.0 \r\n\
	Host: serhatesp.epizy.com\r\n\
	Accept: */*\r\n\
	Content-Type: application/x-www-form-urlencoded\r\n\
	Content-Length: 17\r\n\r\n\
	test1=10&test2=20\
		";

	
	Send_ESP("AT+CIPSTART=1,\"TCP\",\"serhatesp.epizy.com\",80",100);

	uzunluk = strlen(htmlcode);
	
	Send_ESP_Conc("AT+CIPSEND=1",uzunluk,10);
	
	Send_ESP(htmlcode,2000);

	while(Send_ESP("AT+CIPCLOSE=5",20) == NULL);


}


