/*
 * pls.h
 *
 *  Created on: May 10, 2022
 *      Author: lucas
 */

#ifndef SRC_PLS_H_
#define SRC_PLS_H_

#include "stm32f4xx_hal.h"

#define MAX_CMD_BUF 16
#define MAX_PARAM 2
#define PLS_TIMEOUT 100

#define ID_MASK 0xF0
#define TYPE_MASK 0x08
#define NCMD_MASK 0x07

/*
 * 		| 1er octet | 2e octet | 3e octet | 4e octet | 5e octet | ...
 * 		| en-tete   |         var1        |         var2        | ...
 * 	ex:	| iiiitnnn  | 0x12     |  0x34    | 0x56       0x78     | ...
 *
 * i: identifiant commande (16 possiblité)
 * t: type des variables (2 max)
 * n: nombre de variables (8 max)
 */

// identifiant commande rasp->nucleo
#define GPO 0x00
#define SPO 0x01
#define PLS_RESET 0x02
#define GRO 0x03
#define SRO 0x04
#define SVI 0x05
#define STOP 0x06

// identifiant commande nucleo->rasp
#define KMS 0x00  //rx confirmation ("ACK")
#define RPOOK 0x01
#define ROUT 0x02
#define RROOK 0x03
#define RPOUT 0x04
#define ERROR 0x05 // something wrong happened :'(

void send_byte(uint8_t ch);

/*
 * wait incoming bytes from serial huart2
 * returns:
 * - command id (GPO, SPO, etc)
 * - parameters array (distance, theta, ...)
 * - number of params
 */
uint8_t wait_cmd(int16_t params[], uint8_t* param_size);


#endif /* SRC_PLS_H_ */
