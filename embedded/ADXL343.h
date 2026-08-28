#ifndef ADXL343_H_
#define ADXL343_H_

#define ADXL343_NUM_DATA 6

#define ADXL343_POWER_CTL     0x2D
#define ADXL343_MEASURE       0x08
#define ADXL343_DATAX0        0x32
#define ADXL343_OFSX          0x1E
#define ADXL343_OFSY          0x1F
#define ADXL343_OFSZ          0x20
#define ADXL343_X_AXIS_OFFSET 0x03
#define ADXL343_Y_AXIS_OFFSET 0xFF
#define ADXL343_Z_AXIS_OFFSET 0xFF

void ADXL343_init(void);
void ADXL343_read(unsigned char* data);
int convert_accel(unsigned char data_MSB, unsigned char data_LSB);

#endif /* ADXL343_H_ */
