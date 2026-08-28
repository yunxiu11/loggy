#ifndef XL9535_H_
#define XL9535_H_

#define XL9535_OUTPUT_PORT0 0x02
#define XL9535_OUTPUT_PORT1 0x03
#define XL9535_CONFIG_PORT0 0x06
#define XL9535_CONFIG_PORT1 0x07

void XL9535_init(void);
void XL9535_write(unsigned char port, unsigned char data);

#endif /* XL9535_H_ */
