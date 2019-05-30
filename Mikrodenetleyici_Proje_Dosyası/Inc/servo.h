#ifndef SERVO
#define SERVO

#include "stm32f1xx_hal.h"


void initServo(TIM_HandleTypeDef htim4);
void openCover(TIM_HandleTypeDef htim4);
void closeCover(TIM_HandleTypeDef htim4);





#endif
