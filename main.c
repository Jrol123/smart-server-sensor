#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <periph/gpio.h>
#include <board.h>
#include <xtimer.h>
#include <ds18.h>
// TODO: Переработать define под config.txt

// ID устройства
#define ID (0)
// Геолокация
#define GEOLOCATION ("00.00.00.00")

// Частота считывания данных
#define SAMPLING_PERIOD (3000)

int main(void) {
    // Объявление основных переменных
    ds18_t dev;
    ds18_params_t ds18_params;
    ds18_params.pin = GPIO_PIN(PORT_A, 15);
    ds18_params.out_mode = GPIO_OUT;
    ds18_params.in_mode = GPIO_IN;

    int16_t temperature = 0;

    // Инициализация таймера
    xtimer_init();

    // Инициализация датчика с обработкой ошибки
    if (ds18_init(&dev, &ds18_params) == DS18_ERROR) {
        puts("FAILED");
        return 1;
    }

    // Отправка метаданных при подключении
    printf("%s %d\n", GEOLOCATION, ID);

    // Ожидание ответа сервера
    #define const_pr (3)
    int count = 0;

    char buff[32];
    while (count < const_pr) {
        gets(buff);
        if (strstr(buff, "OK") != NULL) {
            break;
        } else {
            printf("%s %d\n", GEOLOCATION, ID);
            xtimer_sleep(1);
        }
        count += 1;
    }

    // Отправка температуры
    while (1) {
        // Успех
        if (ds18_get_temperature(&dev, &temperature) == DS18_OK) {
            printf("%d\n", temperature);
        } else {
        // Неудача
            puts("Could not read temperature");
        }
        xtimer_msleep(SAMPLING_PERIOD);
    }

    return 0;
}
