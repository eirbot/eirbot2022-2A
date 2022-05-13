# Protocole de communication Raspberry PI <-> Nucleo

Le Protocole Lacrymal Série (PLS) permet de communiquer des paramètres de déplacements comme une distance ou un angle de rotation via un port série du NTM32. Il permet également de vous faire pleurer des larmes de sang.

PLS a été écrit sous forme de librairie C: `Core/Inc/pls.h` et `Core/Src/pls.c`. Il suffit d'inclure `pls.h` et d'utiliser la fonction `wait_cmd` dans la boucle principal. ** Attention: cette fonction est bloquante **

Exemple d'utilisation:
``` c++
#include "pls.h"

// variable init

...

while(1) {
    id = wait_cmd(params_int16, &param_size);

    switch(id) {
        case 0xFF:
            // parsing error
            // do nothing...
            break;

        case PLS_RESET:
            // can be used to reset asserv
            break;

        case SPO:
            d = params_int16[0];
            theta = params_int16[1];

            //maj asserv

            //if everything is ok
            send_byte(RPOOK);
            //else
            //send_byte(ROUT)
            break;

        case SRO:
            theta = params_int16[0];

            //maj asserv

            //if everything is ok
            send_byte(RROOK);
            //else
            //send_byte(ROUT)
            break;

        case SVI:
            //maj asserv

            break;

        case STOP:
            //maj asserv

            break;
    }
}
```
