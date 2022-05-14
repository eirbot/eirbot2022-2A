#!/usr/bin/env python3

import serial
import serial.tools.list_ports as list_ports
import struct

# TX codes
operation: dict[str, bin] = {"SPO": 1,
                             "RESET": 2,
                             "SRO": 4,
                             "SVI": 5,
                             "STOP": 6}
type: dict[str, bin] = {"int_16": 0,
                        "int_32": 1}

# RX codes
return_codes: dict[str, bin] = {"KMS": 0,
                                "RPOOK": 1,
                                "RROOUT": 2,
                                "RROOK": 3,
                                "RPOUT": 4,
                                "PLS": 5}
# bin_list = ["000","001","010","011","100"]

def send_cmd(op, int_type, param_array):
    header = op << 4 | int_type << 3 | len(param_array)
    data = []

    for param in param_array:
        if( int_type == type["int_16"] ):
            if(param < 32768 or param > 32767):
                raise ValueError
            data += struct.pack("!h", param)

        elif( int_type == type["int_32"] ):
            if(param < -2147483648 or param > 2147483647):
                raise ValueError
            data += struct.pack("!i", param)

    cmd = [header] + data

    print("tx:", cmd)
    ser.write(cmd)

def main():
    while(True):
        try:
            user_cmd = input("> ")
            splited = user_cmd.split()

            n_var = len(splited) - 1

            ope = splited.pop(0)
            param = list(map(int, splited))

            send_cmd(operation[ope.upper()], type["int_16"], param)

            answer = ser.read()[0]
            for ret_code in return_codes:
                if answer == return_codes[ret_code]:
                    print("rx:", ret_code)

            # seconde réponse pour SPO ou SRO (pas testé)
            if(ope.upper() == "SPO" or ope.upper() == "SRO"):
                answer = ser.read()[0]
                for ret_code in return_codes:
                    if answer == return_codes[ret_code]:
                        print("rx:", ret_code)

        except KeyError:
            print("Commande inconnue")
        except ValueError:
            print("Paramètre en dehors des limites (-32 768 à 32 767 inclus pour int16 et -2 147 483 648 à 2 147 483 647 pour int32)")


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
        print("\nAu revoir\n")
        ser.close()
        break
