#include "ds18.h"
#include "xtimer.h"
#include "periph/gpio.h"
#include "board.h"

int main(void)
{
    ds18_params_t params_datchik;

    params_datchik.in_mode = GPIO_IN;
    params_datchik.out_mode = GPIO_OUT;
    params_datchik.pin = GPIO_PIN(PORT_A, 0);

    ds18_t datchik;
    // datchik.params = params_datchik;

    ds18_init(&datchik, &params_datchik);

    while (1)
    {
        int16_t temp;
        ds18_read(&datchik, &temp);
        // temp /= 100;
        // puts("read");

        printf("output: %d\n", temp);
        xtimer_sleep(1);
    }
}
