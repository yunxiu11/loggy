#include <avr/interrupt.h>
#include <avr/eeprom.h>
#include <stdbool.h>
#include <stdlib.h>
#include "main.h"
#include "clock.h"
#include "timer.h"
#include "USART.h"
#include "LCD.h"
#include "I2C.h"
#include "NAU7802.h"
#include "ADXL343.h"
#include "LM335.h"
#include "XL9535.h"

// EEPROM variables
uint8_t EEMEM voltage_range;
AlarmMode EEMEM alarm_modes[NUM_CHANNELS];
uint16_t EEMEM thresh_ls[NUM_CHANNELS];
uint16_t EEMEM thresh_hs[NUM_CHANNELS];
	
// Flags changed in ISRs
volatile bool timer_matched = false;
volatile bool btn0_pressed = false;
volatile bool btn1_pressed = false;
volatile bool btn2_pressed = false;
volatile bool data_received = false;

// Buffer to store data received
volatile char data_buffer[MAX_DATA_BUFFER_SIZE] = {0};
volatile int buffer_index = 0;

// Function prototypes
void config_data_init(ConfigData* config_data);
void channels_init(Channel channels[]);
void sampling_led_init(void);
void buttons_init(void);
void display_init(void);
bool thresh_exceeded(int meas, int thresh_l, int thresh_h);
void set_channels_displayed(int ch_index);
void display_channel_readings(Channel channels[], int first_channel);
void set_voltage_range(int voltage_range);
void configure_alarm_leds(ConfigData config_data, uint8_t thresh_leds);
void draw_alarm_icon(unsigned char thresh_leds);
void unlatch_alarms(ConfigData config_data, unsigned char* thresh_leds);
uint8_t get_other_led_states(ConfigData config_data, uint8_t thresh_leds);
void select_voltage_range(uint8_t voltage_range);
void select_voltage_channel(uint8_t channel);
void send_config_data(ConfigData config_data);
void process_data_received(ConfigData* config_data, bool* pc_connected);

int main(void)
{
	USART_init(MYUBRR);
	timer_init();
	I2C_init();
	ADC_init();
	NAU7802_init();
	ADXL343_init();
	XL9535_init();
	LCD_init();
	sampling_led_init();
	buttons_init();
	
	// Variables which store device states
	ConfigData config_data;
	Channel channels[NUM_CHANNELS];
	int ch_index = 0;
	uint8_t thresh_leds = 0x00;
	bool pc_connected = false;

    // Initialise configuration data (read from EEPROM)
	config_data_init(&config_data);
	
	// Initialise channels
	channels_init(channels);
	select_voltage_channel(ch_index);
	
	// Initialise LCD display
	display_init();

	// Initialise voltage range
	DDRC |= V_RANGE_SELECT;
	set_voltage_range(config_data.voltage_range);
	
	configure_alarm_leds(config_data, thresh_leds);

	sei();
	//select_channel(2);
	while (1)
	{
		if (timer_matched) {
			float adc_voltages[NUM_VOLT_CHANNELS] = {0};
		    uint8_t raw_accel[NUM_ACCEL_BYTES] = {0};
			uint16_t adc_temp = 0;
			
			// Turn sampling LED on
			PORTD |= SAMPLING_LED_PIN;
	        
			// Read voltage data (CH1-4)
			for (int i = 0; i < 4; i++) {
				select_voltage_channel(i);
				_delay_ms(20);
				adc_voltages[i] = NAU7802_read_voltage();
			}
			
			// Read acceleration data (CH5-7)
			ADXL343_read(raw_accel);
            
			// Read temperature data (CH8)
			adc_temp = ADC_read(0);
			
			// Turn sampling LED off
			PORTD &= ~SAMPLING_LED_PIN;
			
			// Convert and store voltage data (CH1-4)
			for (int i = 0; i < 4; i++) {
				channels[CH_VOLT1 + i].meas = convert_voltage(adc_voltages[i], config_data.voltage_range);
			}
			
			// Convert and store acceleration data (CH5-7)
			for (int i = 0; i < NUM_AXES; i++) {
				channels[CH_ACCEL_X + i].meas = convert_accel(raw_accel[(i * NUM_AXIS_BYTES) + 1], raw_accel[i * NUM_AXIS_BYTES]);
			}
			
			// Convert and store temperature data
			channels[CH_TEMP].meas = convert_temp(adc_temp);
			
			// Send channel readings to PC
			for (int i = 0; i < NUM_CHANNELS; i++) {
				char buffer[MAX_DATA_BUFFER_SIZE];
				snprintf(buffer, sizeof(buffer), data_format_d, ch_read_str, i + 1, channels[i].meas);
				USART_transmit_str(buffer);
			}
			// Check thresholds
	        for (int i = 0; i < NUM_CHANNELS; i++) {
				// Turn on LED if a threshold is exceeded (live and latching LEDs only)
				if ((config_data.alarm_modes[i] != DISABLED) && thresh_exceeded(channels[i].meas, config_data.thresh_ls[i], config_data.thresh_hs[i])) {
					thresh_leds |= (1 << i);
				}
				// Turn off LED if alarm is disabled or within the thresholds (live LEDs only)
				if ((config_data.alarm_modes[i] == DISABLED) || ((config_data.alarm_modes[i] == LIVE) && !thresh_exceeded(channels[i].meas, config_data.thresh_ls[i], config_data.thresh_hs[i]))) {
					thresh_leds &= ~(1 << i);
				}
			}
			// Update device based on channel readings
			configure_alarm_leds(config_data, thresh_leds);
			draw_alarm_icon(thresh_leds);
			display_channel_readings(channels, ch_index);
			
			char buffer[MAX_DATA_BUFFER_SIZE] = {0};
			sprintf(buffer, data_format_d, thresh_leds_str, NO_CHANNEL, thresh_leds);
			USART_transmit_str(buffer);
			
			timer_matched = false;
		}
		if (btn0_pressed) { // Scroll channels
			ch_index++;
			if (ch_index > CH_TEMP) {
				ch_index = 0;
			}
			
			set_channels_displayed(ch_index);
			display_channel_readings(channels, ch_index);
			btn0_pressed = false;
		}
		if (btn1_pressed) { // Toggle voltage range
			config_data.voltage_range = !config_data.voltage_range;
            set_voltage_range(config_data.voltage_range);
			           
		    char buffer[MAX_DATA_BUFFER_SIZE] = {0};
		    sprintf(buffer, data_format_s, v_range_str, NO_CHANNEL, config_data.voltage_range ? one_volt_str : ten_volt_str);
		    USART_transmit_str(buffer);
			
			eeprom_busy_wait();
			eeprom_update_byte(&voltage_range, config_data.voltage_range);
			btn1_pressed = false;
		}
		if (btn2_pressed) { // Unlatch alarms
			unlatch_alarms(config_data, &thresh_leds);
			btn2_pressed = false;
		}	
		if (data_received) {
			process_data_received(&config_data, &pc_connected);	
			UCSR0B |= (1 << RXCIE0); //Re-enable receive interrupt
			data_received = false;
		}
		LCD_set_cursor_pos(PC_ICON_ROW, PC_ICON_COL);
		pc_connected ? LCD_data(ICON_PC_CONNECTED) : LCD_data(ICON_PC_NOT_CONNECTED);
		pc_connected = false;
	}
	return 0;
}

void config_data_init(ConfigData* config_data) {
	config_data->voltage_range = eeprom_read_byte(&voltage_range);
	for (int i = 0; i < NUM_CHANNELS; i++) {
		config_data->thresh_ls[i] = eeprom_read_word(&thresh_ls[i]);
		config_data->thresh_hs[i] = eeprom_read_word(&thresh_hs[i]);
		config_data->alarm_modes[i] = eeprom_read_byte((uint8_t*)&alarm_modes[i]);
	}
}

void channels_init(Channel channels[]) {
	for (int i = 0; i < NUM_CHANNELS; i++) {
		channels[i].meas = 0;
		if (i < 4) {
			channels[i].unit = "V";
	    } else if (i < 7) {
			channels[i].unit = "m/s^2";
	    } else {
			channels[i].unit = "C";
		}
	}
}

void sampling_led_init(void) {
	DDRD |= SAMPLING_LED_PIN;
	PORTD &= SAMPLING_LED_PIN;
}

void buttons_init(void) {
	DDRB &= ~BTN_MASK;
	PORTB |= BTN_MASK;
	PCICR |= (1 << PCIE0);
	PCMSK0 |= BTN_MASK;
}

void display_init(void) {
	for (int i = 0; i < NUM_CH_DISPLAYED; i++) {
		LCD_set_cursor_pos(i, 0);
		LCD_write_str("CH :", NO_PADDING);
	}
	LCD_set_cursor_pos(3, 0);
	LCD_write_str("V-RANGE: ", NO_PADDING);
	LCD_data(ICON_PLUS_MINUS);
	
	set_channels_displayed(CH_VOLT1);
	LCD_set_cursor_pos(PC_ICON_ROW, PC_ICON_COL);
	LCD_data(ICON_PC_NOT_CONNECTED);
}

bool thresh_exceeded(int meas, int thresh_l, int thresh_h) {
	return (meas < thresh_l || meas > thresh_h);
}

void set_channels_displayed(int ch_index) {
	for (int i = 0; i < NUM_CH_DISPLAYED; i++) {
		int ch_num = ch_index + i;
		if (ch_num == NUM_CHANNELS) {
			ch_num = 0;
		}
		
		LCD_set_cursor_pos(i, 2);
		LCD_data('1' + (ch_index + i) % NUM_CHANNELS);
	}
}

void display_channel_readings(Channel channels[], int ch_index) {
	char str[MAX_CH_LENGTH];
	
	for (int i = 0; i < NUM_CH_DISPLAYED; i++) {
		int ch_num = ch_index + i;
		if (ch_num == NUM_CHANNELS) {
			ch_num = 0;
		}
		
		memset(str, 0, MAX_CH_LENGTH);
		char* sign = (channels[ch_num].meas < 0) ? "-" : "";
		int meas = abs(channels[ch_num].meas);
		
		// Cap voltage readings at the range values
		if (ch_num < 4) {
			int max_voltage = eeprom_read_byte(&voltage_range) ? 1000 : 10000;
			if (meas > max_voltage) {
				meas = max_voltage;
			}
		}
		
		int meas_int = meas / 1000;
		int meas_dec = meas % 1000;
		sprintf(str, "%s%d.%03d%s", sign, meas_int, meas_dec, channels[ch_num].unit);
		LCD_set_cursor_pos(i, 5);
		LCD_write_str(str, MAX_CH_LENGTH);
	}
}

void set_voltage_range(int range) {
	int length = strlen("V-RANGE: ") + 1; // + 1 for the plus or minus symbol
	LCD_set_cursor_pos(3, length);
	range ? LCD_write_str("1V", MAX_V_RANGE_LENGTH) : LCD_write_str("10V", MAX_V_RANGE_LENGTH);
	
	if (range == V_RANGE_10V) {
		PORTC &= ~V_RANGE_SELECT;
    } else {
		PORTC |= V_RANGE_SELECT;
	}
}

void configure_alarm_leds(ConfigData config_data, uint8_t thresh_leds) {
	XL9535_write(XL9535_OUTPUT_PORT0, thresh_leds);
	XL9535_write(XL9535_OUTPUT_PORT1, get_other_led_states(config_data, thresh_leds));
}

void draw_alarm_icon(uint8_t thresh_leds) {
	LCD_set_cursor_pos(ALARM_ICON_ROW, ALARM_ICON_COL);
	if (thresh_leds != 0) {
		LCD_data(ICON_ALARM_TRIGGERED);
	} else {
		LCD_data(' ');
	}
}

void unlatch_alarms(ConfigData config_data, uint8_t* thresh_leds) {
	for (int i = 0; i < NUM_CHANNELS; i++) {
		if (config_data.alarm_modes[i] == LATCHING) {
			*thresh_leds &= ~(1 << i);
		}
	}
	configure_alarm_leds(config_data, *thresh_leds);
	draw_alarm_icon(*thresh_leds);
}

uint8_t get_other_led_states(ConfigData config_data, uint8_t thresh_leds) {
	uint8_t other_leds = 0;
	for (int i = 0; i < NUM_CHANNELS; i++) {
		if (config_data.alarm_modes[i] != DISABLED) {
			other_leds |= (~(thresh_leds >> i) & 1) << (7 - i);
		}
	}
	return other_leds;
}

void select_voltage_range(uint8_t voltage_range) {
	if (voltage_range == V_RANGE_10V) {
		PORTC &= ~V_RANGE_SELECT;
	} else {
		PORTC |= V_RANGE_SELECT;
	}
}

void select_voltage_channel(uint8_t channel) {
	if (channel > 3) {
		channel = 0;
	}
	
	// Clear select pins
	PORTC &= ~V_CH_SELECT;
	
	// Set/clear PC3 and PC2 based on channel
	if (channel & 1) {
		PORTC |= V_CH_SELECT_L;
	}
	if ((channel >> 1) & 1) {
		PORTC |= V_CH_SELECT_H;
	}
}

void send_config_data(ConfigData config_data) {
	char buffer[MAX_DATA_BUFFER_SIZE] = {0};
	
	// Send voltage range
	const char* v_range = eeprom_read_byte(&voltage_range) ? one_volt_str : ten_volt_str;
	sprintf(buffer, data_format_s, v_range_str, NO_CHANNEL, v_range);
	USART_transmit_str(buffer);
	
	// Send alarm modes and thresholds
	for (int i = 0; i < NUM_CHANNELS; i++) {
		memset(buffer, 0, MAX_DATA_BUFFER_SIZE);
		const char* alarm_mode;
		switch (config_data.alarm_modes[i]) {
			case LIVE:
			alarm_mode = live_str;
			break;
			case LATCHING:
			alarm_mode = latching_str;
			break;
			default:
			alarm_mode = disabled_str;
			break;
		}
		sprintf(buffer, data_format_s, alarm_mode_str, i + 1, alarm_mode);
		USART_transmit_str(buffer);
		
		memset(buffer, 0, MAX_DATA_BUFFER_SIZE);
		sprintf(buffer, data_format_d, thresh_l_str, i + 1, config_data.thresh_ls[i]);
		USART_transmit_str(buffer);
		
		memset(buffer, 0, MAX_DATA_BUFFER_SIZE);
		sprintf(buffer, data_format_d, thresh_h_str, i + 1, config_data.thresh_hs[i]);
		USART_transmit_str(buffer);
	}
}

void process_data_received(ConfigData* config_data, bool* pc_connected) {
	// Make a nonvolatile copy of data_buffer
	char data_copy[MAX_DATA_BUFFER_SIZE];
	strcpy(data_copy, (char*)data_buffer);
	
	// Parse the data received - should be in the form "{data_type}={ch_num}:{val}\r"
	char* data_type = strtok(data_copy, "=");
	int ch_num = (atoi(strtok(NULL, ":"))) - 1; // Channel number data is 1-indexed but ch_num should be 0-indexed
	char* val = strtok(NULL, "\r"); // Extract the rest of the string
	
	// Process data based on data type (ignore invalid data)
	if (strcmp(data_type, tkinter_str) == 0) {
		if (!(*pc_connected)) {
			send_config_data(*config_data);
		}
		*pc_connected = true;
	} else if (strcmp(data_type, v_range_str) == 0) {
		config_data->voltage_range = (strcmp(val, one_volt_str) == 0) ? V_RANGE_1V : V_RANGE_10V;
		set_voltage_range(config_data->voltage_range);
		eeprom_busy_wait();
		eeprom_update_byte(&voltage_range, config_data->voltage_range);
	} else if (strcmp(data_type, alarm_mode_str) == 0) {
		if (strcmp(val, disabled_str) == 0) {
			config_data->alarm_modes[ch_num] = DISABLED;
		} else if (strcmp(val, live_str) == 0) {
			config_data->alarm_modes[ch_num] = LIVE;
		} else if (strcmp(val, latching_str) == 0) {
			config_data->alarm_modes[ch_num] = LATCHING;
		}
		eeprom_busy_wait();
		eeprom_update_byte(&alarm_modes[ch_num], config_data->alarm_modes[ch_num]);
	} else if (strcmp(data_type, thresh_l_str) == 0) {
		config_data->thresh_ls[ch_num] = atoi(val);
		eeprom_busy_wait();
		eeprom_update_word((uint16_t*)&thresh_ls[ch_num], config_data->thresh_ls[ch_num]);
	} else if (strcmp(data_type, thresh_h_str) == 0) {
		config_data->thresh_hs[ch_num] = atoi(val);
		eeprom_busy_wait();
		eeprom_update_word((uint16_t*)&thresh_hs[ch_num], config_data->thresh_hs[ch_num]);
	}
}

// ISRs
ISR(TIMER1_COMPA_vect) {
	timer_matched = true;
}

ISR(PCINT0_vect) {
	btn0_pressed = !(PINB & BTN0);
	btn1_pressed = !(PINB & BTN1);
	btn2_pressed = !(PINB & BTN2);
}

ISR(USART_RX_vect) {
	if (!data_received && buffer_index < MAX_DATA_BUFFER_SIZE - 1) {
		data_buffer[buffer_index] = UDR0;
		if (data_buffer[buffer_index++] == '\r') { // CR indicates end of data - handle this
			data_buffer[buffer_index] = '\0';
			data_received = true;
			buffer_index = 0;
			UCSR0B &= ~(1 << RXCIE0); // Temporarily disable receive interrupt
		}
	}
}
