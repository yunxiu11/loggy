#ifndef UART_H_
#define UART_H_

void USART_init(unsigned int ubrr);
void USART_transmit(unsigned char data);
void USART_transmit_str(const char* str);
unsigned char USART_receive(void);

#endif /* UART_H_ */
