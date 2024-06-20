#include "ds18.h"
#include "xtimer.h"
#include "periph/gpio.h"
#include "board.h"

#define SAMPLING_PERIOD 2

static const ds18_params_t ds18_params = {
        .pin = GPIO_PIN(PORT_A, 1),
        .out_mode = GPIO_OD,
        .in_mode = GPIO_IN,
    };

    static ds18_t dev;
    int16_t temperature;

int main(void)
{
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
            printf("%d\n", temperature);
        }
        else
        {
            puts("Could not read temperature");
        };
        // temp /= 100;
        // puts("read");

        xtimer_sleep(SAMPLING_PERIOD);
    }
}
