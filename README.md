# Metrics
Client and server for sending and receiving metrics

Клиент-серверное приложение для отправки и приема метрик.

Сервер запускается вызовом метода run_server()

Клиент подключается к серверу при создании экземпляра данного класса. У экземпляра есть 2 метода для общения с сервером: 
put(key, value) - для отправки метрик на сервер;
get(key) - для запроса метрик.
