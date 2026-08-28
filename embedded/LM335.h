#ifndef LM335_H_
#define LM335_H_

void ADC_init();
uint16_t ADC_read(unsigned char channel);
float convert_temp(uint16_t adc_value);

#endif /* LM335_H_ */
