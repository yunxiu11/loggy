#include <avr/io.h>

void ADC_init() {
	ADMUX = (1 << REFS0);
	ADCSRA = (1 << ADEN) | (1 << ADPS1) | (1 << ADPS0); 
}

uint16_t ADC_read(unsigned char channel) {
	ADMUX = (ADMUX & 0xF0) | (channel & 0x0F); // Connect channel to ADC
	ADCSRA |= (1 << ADSC); // Start conversion
	while (ADCSRA & (1 << ADSC)); // Wait until conversion is complete
	return ADC;
}

float convert_temp(uint16_t adc_value) {
	float voltage = adc_value * 3.3 / 1024.0; // 10-bit ADC with 3.3V supply
	return ((voltage * 100.0) - 273.15) * 1000.0; // 10mV/K conversion
}
