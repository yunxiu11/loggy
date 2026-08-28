#include <avr/io.h>
#include <stdbool.h>
#include "I2C.h"

// Set SCL frequency to 100kHz and enable TWI
void I2C_init(void) {
	TWBR = MYTWBR;
	TWSR &= PRESCALER;
	TWCR = (1 << TWEN);
}

// Get I2C status for debugging
unsigned char I2C_status(void) {
	return TW_STATUS;
}

void I2C_start(void) {
	TWCR = (1 << TWINT) | (1 << TWEN) | (1 << TWSTA); // Transmit START condition
	while (!(TWCR & (1 << TWINT))); // Wait until START condition is transmitted
}

void I2C_stop(void) {
	TWCR = (1 << TWINT) | (1 << TWEN) | (1 << TWSTO); // Enable TWI and send STOP condition
}

void I2C_write(unsigned char data) {
	TWDR = data;
	TWCR = (1 << TWINT) | (1 << TWEN); // Transmit data register
	while (!(TWCR & (1 << TWINT))); // Wait until data is transmitted
}

unsigned char I2C_read(bool ack) {
	TWCR = (1 << TWINT) | (1 << TWEN) | (ack ? (1 << TWEA) : 0);
	while (!(TWCR & (1 << TWINT))); // Wait until ACK/NACK is transmitted
	return TWDR;
}

void I2C_sla_rw(unsigned char address, unsigned char rw) {
	unsigned char sla_rw = (address << 1) | rw;
    I2C_write(sla_rw); // Transmit SLA+R/W
}

void I2C_config(unsigned char address, unsigned char reg, unsigned char data) {
	I2C_start();
	I2C_sla_rw(address, TW_WRITE);
	I2C_write(reg);
	I2C_write(data);
	I2C_stop();
}
