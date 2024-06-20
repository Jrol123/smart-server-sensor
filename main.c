#include <stdio.h>
#include <periph/gpio.h>
#include <board.h>
#include <xtimer.h>
#include <ds18.h>

#define SAMPLING_PERIOD 2

int main(void)
{
    ds18_t dev;
    ds18_params_t ds18_params;
    ds18_params.pin = GPIO_PIN(PORT_A, 15);
    ds18_params.out_mode = GPIO_OUT;
    ds18_params.in_mode = GPIO_IN;
    int16_t temperature = 0;

    xtimer_init();
    printf("Init DS18B20...");

    if (ds18_init(&dev, &ds18_params) == DS18_ERROR)
    {
        puts("FAILED");
        return 1;
    }
    else
    {
        puts("OK");
    };

    while (1)
    {
        if (ds18_get_temperature(&dev, &temperature) == DS18_OK)
        {
            printf("%f\n", temperature / 100.0);
        }
        else
        {
            puts("Could not read temperature");
        }
        // temp /= 100;
        // puts("read");

        xtimer_sleep(SAMPLING_PERIOD);
    }
    return 0;
}
