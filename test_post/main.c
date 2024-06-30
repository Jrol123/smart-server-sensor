/*
 * Copyright (C) 2022 Borovik Alexey
 *
 * Small UDP server, sending test text information as UDP packets
 */

#include <stdio.h>

// RIOT headers
#include "net/ipv6/addr.h"
#include "net/gnrc.h"
#include "net/gnrc/netif.h"
#include "xtimer.h"
#include "msg.h"

// Standart Berkeley sockets-related headers
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

// Address for sending (copy your server's IPv6 here)
#define SEND_ADDR  "fe80::2812:caa2:9b2d:c2ea"
#define SEND_PORT  7777

int main(void)
{
	struct sockaddr_in6 addr_src, addr_dst;
	char *iface = NULL;
	int sock = 0;
	char buf [20];
	
    puts("Temperature UDP server");
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
	
	// Send network UDP packets in eternal loop
	for (int i = 0;;i++) {
		if (i > 1000)
			i = 0;
		sprintf(buf,"Iteration #%d\r\n",i);
		// Send temperature string to network
		sendto(sock, buf, strlen(buf) + 1, 0, 
               (struct sockaddr *)&addr_dst, 
			   sizeof(addr_dst));
		xtimer_msleep(100);
	}
	
    return 0;
}
