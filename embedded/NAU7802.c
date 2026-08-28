#include "NAU7802.h"
#include "I2C.h"
#include "clock.h"

uint8_t read_reg(uint8_t reg) {
	uint8_t val;
	I2C_start();
	I2C_sla_rw(NAU7802_ADDR, 0);
	I2C_write(reg);
	I2C_start();
	I2C_sla_rw(NAU7802_ADDR, 1);
	val = I2C_read(NACK);
	I2C_stop();
	return val;
}

uint8_t wait_ready(void) {
	for (int i = 0; i < 100; i++) {
		if (read_reg(REG_PU_CTRL) & (1 << 2)) {
			return 1;
		}
		_delay_ms(10);
	}
	return 0;
}

void NAU7802_init(void) {
	I2C_config(NAU7802_ADDR, REG_PU_CTRL, 0x01); // Reset
	_delay_ms(10);
	I2C_config(NAU7802_ADDR, REG_PU_CTRL, 0x02); // Power up analog
	_delay_ms(10);
	I2C_config(NAU7802_ADDR, REG_PU_CTRL, 0x06); // Power up digital + analog
	_delay_ms(100);
	I2C_config(NAU7802_ADDR, REG_CTRL2, 0x70); // 320 SPS
	_delay_ms(100);
}

long NAU7802_read_adc(void) {
	while (!wait_ready());

	I2C_start();
	I2C_sla_rw(NAU7802_ADDR, 0);
	I2C_write(REG_ADC);
	I2C_start();
	I2C_sla_rw(NAU7802_ADDR, 1);

	long result = 0;
	result |= ((long)I2C_read(ACK)) << 16;
	result |= ((long)I2C_read(ACK)) << 8;
	result |= ((long)I2C_read(NACK));

	I2C_stop();

	if (result & 0x800000) {
		result |= 0xFF000000;
	}

	return result;
}

float NAU7802_read_voltage(void) {
	long adc_voltage = NAU7802_read_adc();
	
	// Voltage at the ADC (VIN- = 1.65V, VIN+ = 3.3V)
	return ((float)adc_voltage * 1650.0 / 8388607.0) + 1650;  // 8388607 = 2^23 - 1
}

int convert_voltage(float voltage, unsigned char range) {
	return (int)((voltage - 1650.0) * ((range ? 1000.0 : 10000.0) / 1650.0));
}
