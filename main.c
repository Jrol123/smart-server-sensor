#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <periph/gpio.h>
#include <board.h>
#include <xtimer.h>
#include <ds18.h>

#define ID 0

#define SAMPLING_PERIOD 3000
// sudo stlink -P examples/smart-server-sensor/bin/stm32f334c8-disco/lab_duolingo.bin 0x08000000
// sudo stlink -P bin/stm32f334c8-disco/lab_duolingo.bin 0x08000000

// int str_cut(char *str, int begin)
// {
//     int l = strlen(str);
//     if (begin < l) {
//         memmove(str, str + begin, l - begin + 1); // Перемещаем символы на правильную позицию
//         return l - begin;
//     } else {
//         str[0] = '\0'; // Если начальная позиция больше длины строки, обнуляем строку
//         return 0;
//     }
// }


int main(void)
{
    // объявление основных переменных
    ds18_t dev;
    ds18_params_t ds18_params;
    ds18_params.pin = GPIO_PIN(PORT_A, 15);
    ds18_params.out_mode = GPIO_OUT;
    ds18_params.in_mode = GPIO_IN;

    int16_t temperature = 0;

    // puts("dadadada");
    // FILE * conf = fopen("cnfg.txt", "r");
    // if (conf == NULL) {
    //     puts("error opennnning ffffffffffffiiilllleeeeeeeeeeeeeeeeeeeeeeeeeee");
    //     return -1;
    // }

    // char line[32];
    // puts("dadadadanonononon");

    // fgets(line, sizeof line, conf);
    // // str_cut(line, 3);
    // puts("wow!!!!!!!!!!!!!!!!!!!!");
    // int id = atoi(line);
    // fclose(conf);

    xtimer_init();
    // printf("Init DS18B20...");

    if (ds18_init(&dev, &ds18_params) == DS18_ERROR)
    {
        puts("FAILED");
        return 1;
    }
    // else
    // {
    //     puts("OK");
    // };

    // printf("vladivostok %d\n", ID);
    puts("vladivostok 0");

    char buff[32];
    while (true) {
        gets(buff);
        if (strstr(buff, "OK") != NULL) {
            break;
        }
    }

    //     // puts("Waiting for confirming");
    //     // xtimer_msleep(SAMPLING_PERIOD);
    //     // if ((float)rand() / RAND_MAX <= 0.1) {
    //     //     puts("OK");
    //     // }
    // }

    while (1)
    {
        if (ds18_get_temperature(&dev, &temperature) == DS18_OK)
        {
            printf("%d\n", temperature);
        }
        else
        {
            puts("Could not read temperature");
        }

        xtimer_msleep(SAMPLING_PERIOD);
    }

    return 0;
}
