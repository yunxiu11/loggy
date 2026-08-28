#ifndef DELAY_H_
#define DELAY_H_

#define F_CPU 8000000
#include <util/delay.h>

#define BAUD 9600
#define MYUBRR F_CPU/16/BAUD-1

#endif /* DELAY_H_ */
