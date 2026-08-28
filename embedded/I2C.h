#ifndef I2C_H_
#define I2C_H_

#include <util/twi.h>
#include <stdbool.h>

#define MYTWBR 0x20
#define PRESCALER ~((1 << TWPS1) | (1 << TWPS0))

#define NACK 0
#define ACK  1

#define ADXL343_ADDR 0x1D
#define XL9535_ADDR  0x27
#define NAU7802_ADDR 0x2A

void I2C_init(void);
unsigned char I2C_status(void);
void I2C_start(void);
void I2C_stop(void);
void I2C_write(unsigned char data);
unsigned char I2C_read(bool ack);
void I2C_sla_rw(unsigned char address, unsigned char rw);
void I2C_config(unsigned char address, unsigned char reg, unsigned char data);

#endif /* I2C_H_ */
