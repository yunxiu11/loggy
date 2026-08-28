#ifndef MAIN_H_
#define MAIN_H_

#include <avr/io.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

#define MAX_DATA_BUFFER_SIZE 16

// Sampling LED pin
#define SAMPLING_LED_PIN (1 << PD2)

// Bitmasks for buttons
#define BTN0     (1 << PB0)
#define BTN1     (1 << PB1)
#define BTN2     (1 << PB2)
#define BTN_MASK (BTN0 | BTN1 | BTN2)

// Voltage channels
#define NUM_VOLT_CHANNELS 4

#define V_RANGE_10V 0
#define V_RANGE_1V  1

#define V_RANGE_SELECT (1 << PC1)

#define V_CH_SELECT_H (1 << PC3)
#define V_CH_SELECT_L (1 << PC2)
#define V_CH_SELECT   (V_CH_SELECT_H | V_CH_SELECT_L)

// Acceleration channels
#define NUM_AXES        3
#define NUM_AXIS_BYTES  2
#define NUM_ACCEL_BYTES (NUM_AXES * NUM_AXIS_BYTES)

#define NUM_CHANNELS     8
#define NUM_CH_DISPLAYED 2

#define NO_CHANNEL 0

// Parameter codes for data transfer
const char* const tkinter_str     = "TKINTER\r";
const char* const v_range_str     = "VOR";
const char* const ten_volt_str    = "TEN";
const char* const one_volt_str    = "ONE";
const char* const thresh_l_str    = "THL";
const char* const thresh_h_str    = "THH";
const char* const alarm_mode_str  = "ALM";
const char* const disabled_str    = "DIS";
const char* const live_str        = "LIV";
const char* const latching_str    = "LAT";
const char* const ch_read_str     = "CHR";
const char* const thresh_leds_str = "LED";

// Data format strings
const char* const data_format_s = "%s=%d:%s\n";
const char* const data_format_d = "%s=%d:%d\n";

typedef enum {
	CH_VOLT1,
	CH_VOLT2,
	CH_VOLT3,
	CH_VOLT4,
	CH_ACCEL_X,
	CH_ACCEL_Y,
	CH_ACCEL_Z,
	CH_TEMP
} ChannelType;

typedef enum {
	DISABLED,
	LIVE,
	LATCHING
} AlarmMode;

typedef struct {
	int16_t   meas;
	char* unit;
} Channel;

typedef struct {
	uint8_t   voltage_range;
	uint16_t  thresh_ls[NUM_CHANNELS];
	uint16_t  thresh_hs[NUM_CHANNELS];
	AlarmMode alarm_modes[NUM_CHANNELS];
} ConfigData;

#endif /* MAIN_H_ */
