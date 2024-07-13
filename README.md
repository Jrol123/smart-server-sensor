# smart-server-sensor
## Описание
Создание прошивки для микроконтроллера на основе RIOT OS, отправляющей данные на сервер и сам сервер-приёмник-обработчик.

Данный проект выполнялся для дисциплины "Программирование микроконтроллеров" на втором курсе обучения в институте.

## Используемые технологии
Сервер выполнен на Flask (python).

Микроконтроллер использовался с OS RIOT с датчиками температуры ds18.

# Допустимые варианты использования
Можно подключить неограниченное количество контроллеров через порты устройства.

К сожалению, *ethernet* часть не была реализована, однако вы можете найти её среди коммитов. Она должна работать, но её придётся подправить для подключения *ethernet* или *wifi* модуля.

# Структура
## Сервер
### Серверная составляющая
### Считывание данных с контроллера
### Графическая составляющая


## Прошивка


# Распределение обязанностей
1. **ARTEMII POPOVKIN**
	- Тимлидер
	- Продумал финальный вариант работы сервера и прошивки. 
	- Модуль `read_port`.
2. **ARTEM GROMYKO**