#include <stdio.h>
#include <periph/gpio.h>
#include <board.h>
#include <xtimer.h>
#include <ds18.h>

// #include "net/ipv6/addr.h"
// #include "net/gnrc.h"
#include "net/gnrc/netif.h"
// #include "msg.h"

// #include "curl/include/curl/curl.h"
// #include <curl/curl.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

#define SAMPLING_PERIOD 2
#define SEND_ADDR  "fe80::2812:caa2:9b2d:c2ea%10"
#define SEND_PORT  7777
// sudo stlink -P examples/smart-server-sensor/bin/stm32f334c8-disco/lab_duolingo.bin 0x08000000
// ./configure --host=arm-none-eabi --disable-ftp --disable-file --enable-ipv6 --disable-dict --disable-ldap --disable-ldaps --disable-telnet --disable-tftp --disable-pop3 --disable-imap --disable-smtp --disable-gopher --disable-sspi --disable-schannel --disable-rtsp --disable-esni --disable-co --disable-manual --disable-https --disable-tls-srp --disable-unix-sockets --disable-ares --disable-rt --disable-soname-bump --with-wolfssl --without-ssl --without-libidn2 --without-libpsl --without-nghttp2 --without-libmetalink --without-zstd --without-brotli --without-quiche

int main(void)
{
    // Инициализация подключения к серверу
    // int client_socket;
    // struct sockaddr_in server_address;

    // client_socket = socket(AF_INET, SOCK_STREAM, 0);
    
    // // Устанавливаем параметры сервера
    // server_address.sin_family = AF_INET;
    // server_address.sin_port = htons(SEND_PORT);
    // // server_address.sin_addr.s_addr = inet_addr(SEND_ADDR);
    // inet_pton(AF_INET, SEND_ADDR, &server_address.sin_addr);

    // // Подключаемся к серверу
    // int con1 = connect(client_socket, 
    //         (struct sockaddr *)&server_address, 
    //         sizeof(server_address));
    // printf("%i\n", con1);

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

    // int con1 = connect(sock, 
    //         (struct sockaddr *)&addr_dst, 
    //         sizeof(addr_dst));
    // int con2 = connect(sock, 
    //         (struct sockaddr *)&addr_src, 
    //         sizeof(addr_src));
    // printf("%i\n", con1);

    // объявление основных переменных
    ds18_t dev;
    ds18_params_t ds18_params;
    ds18_params.pin = GPIO_PIN(PORT_A, 15);
    ds18_params.out_mode = GPIO_OUT;
    ds18_params.in_mode = GPIO_IN;

    int16_t temperature = 0;
    char post_data[32];
    // char buffer[256];
    // char request[256];
    
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
            // printf("%f\n", temperature / 100.0);
            sprintf(post_data, "temperature=%f", temperature / 100.0);
            
            // // Формирование POST-запроса
            // sprintf(buffer, "POST /postt HTTP/1.1\r\nHost: 127.0.0.1:5000\r\n"
            //                 // "Content-Type: application/x-www-form-urlencoded\r\n"
            //                 "Content-Length: %i\r\n\r\n%s", 
            //                 strlen(post_data) + 1, post_data);

            // // Отправка данных на сервер
            // ssize_t sent_bytes = send(client_socket, post_data, strlen(post_data) + 1, 0);

            // ssize_t sent_bytes = sendto(sockfd, post_data, strlen(post_data), 0, 
            //                             (struct sockaddr *) &dest_addr, 
            //                             sizeof(dest_addr));

            ssize_t sent_bytes = sendto(sock, post_data, strlen(post_data) + 1, 0, 
                   (struct sockaddr *)&addr_dst, sizeof(addr_dst));

            if (sent_bytes < 0) {
                perror("sendto failed\n");
                return 1;
            }
            else {
                printf("bytes sent: %d\n", sent_bytes);
            };

            printf("%f\n", temperature / 100.0);

            // Формирование POST-запроса
            // sprintf(request, 
            //         "POST / HTTP/1.1\r\nHost: %s:%i\r\nContent-length: %i\r\n\r\n%s", 
            //         SEND_ADDR, SEND_PORT, strlen(post_data), post_data);

            // Отправка POST-запроса
            // if (send(sock, request, strlen(request), 0) < 0) {
            //     perror("Ошибка при отправке POST-запроса");
            //     // return 1;
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

    // curl_easy_cleanup(curl);
    // close(sockfd);
    return 0;
}
