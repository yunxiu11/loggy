#include <avr/io.h>
#include "clock.h"
#include "timer.h"

// Initialises timer with frequency 2Hz
void timer_init(void) {
	OCR1A = 15624;
	TCCR1B = (1 << WGM12) | (1 << CS12);
	TIMSK1 = (1 << OCIE1A);
}
