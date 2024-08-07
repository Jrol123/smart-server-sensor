# name of your application
APPLICATION = lab_duolingo

# name of your board
BOARD ?= stm32f334c8-disco

# FEATURES_REQUIRED += cpp
# FEATURES_BLACKLIST += picolibc

DEVELHELP ?= 0

# Used modules
USEMODULE += xtimer
USEMODULE += periph_gpio
USEMODULE += ds18
USEMODULE += printf_float

# USEMODULE += libhttp
# USEMODULE += curl
# EXTERNAL_LIBS += -lcurl

# USEMODULE += netdev_default
# USEMODULE += auto_init_gnrc_netif

# USEMODULE += gnrc_netif_single
# USEMODULE += gnrc_ipv6
# USEMODULE += gnrc_icmpv6_echo
# USEMODULE += prng_minstd
# USEMODULE += enc28j60

# USEMODULE += sock_udp
# USEMODULE += posix_sockets
# USEMODULE += posix_inet

# This has to be the absolute path to the RIOT base directory:
RIOTBASE ?= $(CURDIR)/../..

# Comment this out to disable code in RIOT that does safety checking
# which is not needed in a production environment but helps in the
# development process:
DEVELHELP ?= 1

# Change this to 0 show compiler invocation lines by default:
QUIET ?= 1

include $(RIOTBASE)/Makefile.include

# CC = arm-none-eabi-gcc
# CFLAGS = -c -mcpu=cortex-m3 -mthumb

# CFLAGS += -I vcpkg/installed/x64-linux/include
# CFLAGS += -I $(RIOTBASE)/boards/stm32f334c8-disco/include

# LDFLAGS = -L vcpkg/installed/x64-linux/lib -lcurl

# LDFLAGS = -L/path/to/curl/lib
# LIBS = -lcurl


# CFLAGS += -I$(RIOTBASE)/examples/smart-server-sensor/vcpkg/packages/curl_x64-linux/include
# CFLAGS += -DLOG_LEVEL=LOG_NONE  # disable log output
# CFLAGS += -DCONFIG_GNRC_NETIF_IPV6_ADDRS_NUMOF=2 \
#           -DGNRC_NETIF_IPV6_GROUPS_NUMOF=2 -DCONFIG_GNRC_IPV6_NIB_NUMOF=1 \
#           -DCONFIG_GNRC_IPV6_NIB_OFFL_NUMOF=1 # be able to configure at least one route
# CFLAGS += -I/curl/include
# CFLAGS += -L$(RIOTBASE)/examples/smart-server-sensor/vcpkg/packages/curl_x64-linux/lib -lcurl

# EXTERNAL_MODULE_DIRS += $(RIOTBASE)/examples/smart-server-sensor/curl
# -DCMAKE_TOOLCHAIN_FILE=/home/tyferse/RIOT/examples/smart-server-sensor/vcpkg/scripts/buildsystems/vcpkg.cmake

# QUIET ?= 1

# ifndef CONFIG_GNRC_PKTBUF_SIZE
#   CFLAGS += -DCONFIG_GNRC_PKTBUF_SIZE=512
# endif

# Set a custom channel if needed
include $(RIOTMAKE)/default-radio-settings.inc.mk


# SRCS = main.c
# OBJS = $(SRCS:.c=.o)

# .PHONY: all clean

# all: $(APPLICATION)

# $(APPLICATION): $(OBJS) \
#  $(CC) $(LDFLAGS) $^ $(LIBS) -o $@

# %.o: %.c \
#  $(CC) $(CFLAGS) $< -o $@

# clean: \
#  rm -f $(OBJS) $(APPLICATION)
