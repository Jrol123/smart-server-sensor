#include <stdio.h>
#include <periph/gpio.h>
#include <board.h>
#include <xtimer.h>
#include <ds18.h>

// #include "net/ipv6/addr.h"
#include "net/gnrc.h"
// #include "net/gnrc/netif.h"
// #include "msg.h"

#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

#define SAMPLING_PERIOD 2
#define SEND_ADDR  "fe80::c9a2:d0:9919:3ba3"
#define SEND_PORT  5001

int main(void)
{
    // Инициализация подключения к серверу
    struct sockaddr_in6 addr_src, addr_dst;
	char *iface = NULL;
	int sock = 0;

    // NULL address structures
	memset(&addr_src, 0, sizeof(addr_src));
	memset(&addr_dst, 0, sizeof(addr_dst));
	addr_src.sin6_family = AF_INET6;
	addr_dst.sin6_family = AF_INET6;
	
    // Get proper interface for address 
	// (in case we have multiple network interfaces)
    iface = ipv6_addr_split_iface(SEND_ADDR);
    if (iface) {
		netif_t *netif = netif_get_by_name(iface);
        if (netif) {
            addr_dst.sin6_scope_id = (uint32_t) netif_get_id(netif);
			addr_src.sin6_scope_id = addr_dst.sin6_scope_id;
		}
        else
            printf("unknown network interface %s\n", iface);
    }
    // Convert string address representation to binary number
    if (inet_pton(AF_INET6, SEND_ADDR, &addr_dst.sin6_addr) != 1) {
        puts("Error: unable to parse destination address");
		return 1;
    }
    // Set port (in network byte order)
    addr_dst.sin6_port = htons(SEND_PORT);
    addr_src.sin6_port = htons(SEND_PORT);
	
	// Create IPv6 UDP socket
    sock = socket(AF_INET6, SOCK_DGRAM, IPPROTO_UDP);
    if (sock < 0) {
        puts("error initializing socket...");
        return 1;
    }
	
	// Bind socket to local address
	if (bind(sock,(struct sockaddr*)&addr_src, sizeof(addr_src))) {
        puts("failed to bind...");
        return 1;
    }

    // объявление основных переменных
    ds18_t dev;
    ds18_params_t ds18_params;
    ds18_params.pin = GPIO_PIN(PORT_A, 15);
    ds18_params.out_mode = GPIO_OUT;
    ds18_params.in_mode = GPIO_IN;

    int16_t temperature = 0;
    char post_data[32];
    
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
            printf("%f\n", temperature / 100.0);
            sprintf(post_data, "temperature=%f", temperature / 100.0);
            sendto(sock, post_data, strlen(post_data) + 1, 0, 
                   (struct sockaddr *)&addr_dst, sizeof(addr_dst));

            // Формирование POST-запроса
            // sprintf(request, 
            //         "POST / HTTP/1.1\r\nHost: localhost\r\nContent-length: %i\r\n\r\n%s", 
            //         strlen(post_data), post_data);

            // // Отправка POST-запроса
            // if (send(sockfd, request, strlen(request), 0) < 0) {
            //     perror("Ошибка при отправке POST-запроса");
            //     return 1;
            // }
        }
        else
        {
            puts("Could not read temperature");
        }
        // temp /= 100;
        // puts("read");

        xtimer_sleep(SAMPLING_PERIOD);
    }

    close(sock);
    return 0;
}
