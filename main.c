#include <stdio.h>
#include <periph/gpio.h>
#include <board.h>
#include <xtimer.h>
#include <ds18.h>
#include <curl/curl.h>

#define SAMPLING_PERIOD 2


// chmod +x ./vcpkg
int main(void)
{
    // Инициализация подключения к серверу (пока только ради теста)
    CURL *curl;
    CURLcode res;
    curl = curl_easy_init();
    curl_easy_setopt(curl, CURLOPT_URL, "http://127.0.0.1:5000");

    ds18_t dev;
    ds18_params_t ds18_params;
    ds18_params.pin = GPIO_PIN(PORT_A, 15);
    ds18_params.out_mode = GPIO_OUT;
    ds18_params.in_mode = GPIO_IN;
    int16_t temperature = 0;
    char buf[10];

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
            sprintf(buf, "%0.4f", temperature / 100.0);
            // printf("%0.4f\n", temperature / 100.0);

            struct curl_slist *headers = NULL;
            headers = curl_slist_append(headers, "Content-Type: application/json");
            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
            
            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "{\"temperature\": " + buf + "}");
            
            // Выполняем запрос
            res = curl_easy_perform(curl);
            
            // Проверка на успешность запроса
            if(res != CURLE_OK) {
                fprintf(stderr, "Ошибка: %s\n", curl_easy_strerror(res));
            }
            
            // Освобождаем ресурсы
            curl_slist_free_all(headers);
            curl_easy_cleanup(curl);
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
