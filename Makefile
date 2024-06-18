# name of your application
APPLICATION = lab_uno

# name of your board
BOARD ?= stm32f334c8-disco

# Used modules
USEMODULE += xtimer
USEMODULE += periph_gpio_irq
USEMODULE += periph_rtc
USEMODULE += periph_pwm

# This has to be the absolute path to the RIOT base directory:
RIOTBASE ?= $(CURDIR)/../..

# Comment this out to disable code in RIOT that does safety checking
# which is not needed in a production environment but helps in the
# development process:
DEVELHELP ?= 1

# Change this to 0 show compiler invocation lines by default:
QUIET ?= 1

include $(RIOTBASE)/Makefile.include
