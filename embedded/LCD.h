#ifndef LCD_H_
#define LCD_H_

#include <avr/io.h>

#define RS (1 << PB6)
#define EN (1 << PB7)

#define MAX_CH_LENGTH      13
#define MAX_V_RANGE_LENGTH  3
#define NO_PADDING          0

#define ICON_PC_NOT_CONNECTED 0
#define ICON_PC_CONNECTED     1
#define ICON_PLUS_MINUS       2
#define ICON_ALARM_TRIGGERED  3

#define PC_ICON_ROW  0
#define PC_ICON_COL 19

#define ALARM_ICON_ROW  3
#define ALARM_ICON_COL 19

extern unsigned char pc_not_connected[];
extern unsigned char pc_connected[];
extern unsigned char plus_minus[];
extern unsigned char alarm_triggered[];

void LCD_send_nibble(unsigned char byte);
void LCD_send_byte(unsigned char byte);
void LCD_cmd(unsigned char cmd);
void LCD_data(char data);
void LCD_init(void);
void LCD_set_cursor_pos(int row, int col);
void LCD_write_str(char* str, int max_length);

#endif /* LCD_H_ */
