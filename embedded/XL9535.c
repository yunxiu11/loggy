#include "I2C.h"
#include "XL9535.h"

void XL9535_init(void) {
	// Set pins as outputs
	I2C_config(XL9535_ADDR, XL9535_CONFIG_PORT0, 0x00);
	I2C_config(XL9535_ADDR, XL9535_CONFIG_PORT1, 0x00);
}

void XL9535_write(unsigned char port, unsigned char data) {
	I2C_config(XL9535_ADDR, port, data);
}
