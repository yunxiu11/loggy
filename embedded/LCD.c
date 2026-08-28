#include <string.h>
#include "LCD.h"
#include "clock.h"

unsigned char pc_not_connected[] = {0x0e, 0x1f, 0x00, 0x0a, 0x1f, 0x0e, 0x0e, 0x04};
unsigned char pc_connected[] = {0x0e, 0x1f, 0x0e, 0x0e, 0x04, 0x04, 0x04, 0x08};
unsigned char plus_minus[] = {0x00, 0x04, 0x0e, 0x04, 0x00, 0x0e, 0x00, 0x00};
unsigned char alarm_triggered[] = {0x00, 0x04, 0x0e, 0x0e, 0x0e, 0x1f, 0x04, 0x00};

void LCD_send_nibble(unsigned char byte) {
	PORTD = (PORTD & 0x0F) | (byte & 0xF0);
	
	// Pulse Enable pin to transmit data
	PORTB |= EN;
	_delay_us(1);
	PORTB &= ~EN;
	_delay_us(1);
}

void LCD_send_byte(unsigned char byte) {
	LCD_send_nibble(byte);
	LCD_send_nibble(byte << 4);
}

void LCD_cmd(unsigned char cmd) {
	PORTB &= ~RS;
	LCD_send_byte(cmd);
	if (cmd == 0x01 || cmd == 0x02) {
		_delay_ms(3);
	} else {
		_delay_us(50);
	}
}

void LCD_data(char data) {
	PORTB |= RS;
	LCD_send_byte(data);
	_delay_us(50);
}

void LCD_write_str(char* str, int max_length) {
	int i = 0;
	for (; i < strlen(str); i++) {
		LCD_data(str[i]);
	}
	for (; i < max_length; i++) {
		LCD_data(' ');
	}
}

void LCD_init(void) {
	DDRD |= 0xF0;
	DDRB |= RS | EN;

	_delay_ms(200);

	LCD_cmd(0x28); // 4-bit mode, 2 display lines
	LCD_cmd(0x0C); // Display on, cursor off
	LCD_cmd(0x06); // Cursor increments every write
	LCD_cmd(0x01); // Clear display

	LCD_cmd(0x40); // CGRAM address
	for (int i = 0; i < 8; i++) {
		LCD_data(pc_not_connected[i]);
	}
	for (int i = 0; i < 8; i++) {
		LCD_data(pc_connected[i]);
	}
	for (int i = 0; i < 8; i++) {
		LCD_data(plus_minus[i]);
	}
	for (int i = 0; i < 8; i++) {
		LCD_data(alarm_triggered[i]);
	}
	_delay_ms(10);
}

void LCD_set_cursor_pos(int row, int col) {
	int address = ((64 * row) % 108) + col;
	LCD_cmd(0x80 | address);
}
