# name of your application
APPLICATION = lab_duolingo

# name of your board
BOARD ?= stm32f334c8-disco

# FEATURES_REQUIRED += cpp

# Used modules
USEMODULE += xtimer
USEMODULE += periph_gpio
USEMODULE += ds18
USEMODULE += printf_float
# USEMODULE += curl_curl

# This has to be the absolute path to the RIOT base directory:
RIOTBASE ?= $(CURDIR)/../..

# Comment this out to disable code in RIOT that does safety checking
# which is not needed in a production environment but helps in the
# development process:
DEVELHELP ?= 1

# Change this to 0 show compiler invocation lines by default:
QUIET ?= 1

include $(RIOTBASE)/Makefile.include
