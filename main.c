#include <stdio.h>
#include <periph/gpio.h>
#include <board.h>
#include <xtimer.h>
#include <ds18.h>

#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

#define SAMPLING_PERIOD 2


int main(void)
{
    // Инициализация подключения к серверу
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("Error opening socket");
        exit(1);
    }

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(5000);

    const char* ip_address = "127.0.0.1";
    struct in_addr addr;
    if (inet_pton(AF_INET, ip_address, &addr) <= 0) {
        perror("inet_pton error");
        exit(EXIT_FAILURE);
    }

    server_addr.sin_addr.s_addr = addr.s_addr;

    if (connect(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("Error connecting to server");
        exit(1);
    }

    // объявление основных переменных
    ds18_t dev;
    ds18_params_t ds18_params;
    ds18_params.pin = GPIO_PIN(PORT_A, 15);
    ds18_params.out_mode = GPIO_OUT;
    ds18_params.in_mode = GPIO_IN;

    int16_t temperature = 0;
    // char buf[10];
    char post_data[32];
    char request[256];
    
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
            // sprintf(buf, "%0.4f", temperature / 100.0);
            // printf("%0.4f\n", temperature / 100.0);
            sprintf(post_data, "temperature=%0.4f", temperature / 100.0);
            snprintf(request, sizeof(request), 
                     "POST / HTTP/1.1\r\nHost: 127.0.0.1\r\nContent-Length: %i\r\n\r\n%s", 
                     strlen(post_data), post_data);
            
            if (send(sockfd, request, strlen(request), 0) < 0) {
                perror("Error sending request");
                exit(1);
            }
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
