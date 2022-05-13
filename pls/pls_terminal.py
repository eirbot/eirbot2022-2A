#!/usr/bin/env python3

import serial
import serial.tools.list_ports as list_ports

operation: dict[str, bin] = {"SPO": "0001",
                            "RESET": "0010",
                            "SRO": "0100",
                            "SVI": "0101",
                            "STOP": "0110"}
type: dict[str, bin] = {"int_16": "0",
                        "int_32": "1"}
return_codes: dict[str, bin] = {"KMS": "0000",
                                "RPOOK": "0001",
                                "RROOUT": "0010",
                                "RROOK": "0011",
                                "RPOUT": "0100",
                                "ERROR": "0101"}
bin_list = ["000","001","010","011","100"]

def main():
    while(True):
        try:
            user_cmd = input("> ")
            splited = user_cmd.split()

            n_var = len(splited) - 1

            header = operation[splited[0].upper()] + type["int_16"] + bin_list[n_var]

            print(header)
            ser.write(bytes(header, "utf-8"))

            splited.pop(0)
            for param in splited:
                print(bytes(str(param), "utf-8"))
                ser.write(bytes(str(param), "utf-8"))

            answer = ser.read()
            for ret_code in return_codes:
                if answer == bytes(return_codes[ret_code], "utf-8"):
                    print(ret_code)

        except KeyError:
            print("Commande inconnue")

######## LIST DES COMMANDES ########

print("Liste des commandes:")
for key in operation:
    print("\t -", key.lower())

######## CHOIX DU PORT ########

print()
print("Choix du port:")

index = 0
for port in list_ports.comports():
    print(index, '=', port.device)
    index += 1

while(True):
    try:
        user_port = int(input("? "))
        if( user_port >= 0 and user_port < index ):
            break
        else:
            raise ValueError
    except ValueError:
        print("Entrée non valide")
    except KeyboardInterrupt:
        quit()

ser = serial.Serial(list_ports.comports()[user_port].device, 115200)
ser.timeout = 0.1

######## main loop ########

while(True):
    try:
        main()
    except KeyboardInterrupt:
        print("Au revoir")
        ser.close()
        break
