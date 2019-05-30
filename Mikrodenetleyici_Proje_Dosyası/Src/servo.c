#include "servo.h"


void initServo(TIM_HandleTypeDef htim4)
{	
	HAL_TIM_PWM_Start(&htim4,TIM_CHANNEL_1);	
}


void openCover(TIM_HandleTypeDef htim4)
{
	htim4.Instance->CCR1 = 25;
	HAL_Delay(1000);
}




void closeCover(TIM_HandleTypeDef htim4)
{
	htim4.Instance->CCR1 = 125;
	HAL_Delay(1000);	
}
