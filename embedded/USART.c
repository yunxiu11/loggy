#include <avr/io.h>
#include "USART.h"

void USART_init(unsigned int ubrr)
{
    UBRR0H = (unsigned char)(ubrr >> 8);
    UBRR0L = (unsigned char)ubrr;
	
    UCSR0B = (1 << RXEN0) | (1 << TXEN0) | (1 << RXCIE0);
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00); 
} 

void USART_transmit(unsigned char data)
{
    while (!(UCSR0A & (1 << UDRE0)));
	
    UDR0 = data;
}

void USART_transmit_str(const char* str) {
	while (*str) {
		USART_transmit(*str++);
	}
}

unsigned char USART_receive(void)
{
    while (!(UCSR0A & (1 << RXC0)));
	
    return UDR0;
}
