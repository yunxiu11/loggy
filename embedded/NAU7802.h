#ifndef NAU7802_H_
#define NAU7802_H_

#define REG_PU_CTRL 0x00
#define REG_CTRL1   0x01
#define REG_CTRL2   0x02
#define REG_ADC     0x12

void NAU7802_init(void);
long NAU7802_read_adc(void);
float NAU7802_read_voltage(void);
int convert_voltage(float voltage, unsigned char range);

#endif /* NAU7802_H_ */
