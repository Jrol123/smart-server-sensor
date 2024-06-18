#include"ds18.h"
#include "periph/gpio.h"
#include "board.h"


int main(void)
{
    ds18_params_t params_datchik;

    params_datchik.in_mode = GPIO_IN;
    params_datchik.out_mode = GPIO_OUT;
    params_datchik.pin = GPIO_PIN(PORT_A, 0);

    ds18_t datchik;
    datchik.params = params_datchik;
}
