#include <string.h>
#include "I2C.h"
#include "ADXL343.h"
#include "LCD.h"

void ADXL343_init(void) {
	I2C_config(ADXL343_ADDR, ADXL343_POWER_CTL, ADXL343_MEASURE);
	I2C_config(ADXL343_ADDR, ADXL343_OFSX, ADXL343_X_AXIS_OFFSET);
	I2C_config(ADXL343_ADDR, ADXL343_OFSY, ADXL343_Y_AXIS_OFFSET);
	I2C_config(ADXL343_ADDR, ADXL343_OFSZ, ADXL343_Z_AXIS_OFFSET);
}

void ADXL343_read(unsigned char* data) {
	memset(data, 0, ADXL343_NUM_DATA);
	
	I2C_start();

	I2C_sla_rw(ADXL343_ADDR, TW_WRITE);	
	I2C_write(ADXL343_DATAX0);
	
	I2C_start();
	I2C_sla_rw(ADXL343_ADDR, TW_READ);
	for (int i = 0; i < ADXL343_NUM_DATA; i++) {
		if (i < (ADXL343_NUM_DATA - 1)) {
			data[i] = I2C_read(ACK);
		} else {
			data[i] = I2C_read(NACK);
		}
	}
	I2C_stop();
}

int convert_accel(unsigned char data_MSB, unsigned char data_LSB) {
	return (int)(((int16_t)((data_MSB << 8) | data_LSB) * 9.80665 / 256.0) * 1000.0);
}
