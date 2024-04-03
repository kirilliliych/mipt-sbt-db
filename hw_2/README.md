# Redis

## Большой json-файл
Возьмем большой json по [ссылке](https://github.com/json-iterator/test-data/blob/master/large-file.json).

## Тест сохранения и чтения на одной ноде
Зайдем в директорию [redis_one_node](/hw_2/redis_one_node/) и поднимем контейнер с redis командой `docker compose up -d`
(порт будет 6379):
![redis_one_node_docker](/hw_2/pictures/redis_one_node_docker.png)

Затем проверим, что redis доступен:
![redis_one_node_ping](/hw_2/pictures/redis_one_node_ping.png)

Теперь запустим `python3 json_redis_test.py` и посмотрим на результаты замеров скорости:
![redis_one_node_time](/hw_2/pictures/redis_one_node_time.png)

## Тест сохранения и чтения на кластере
Теперь организуем кластер. Аналогично зайдем в директорию [redis-cluster](/hw_2/redis_cluster/) и поднимем контейнер через `docker compose up -d` 
(порты будут 6380, 6381 и 6382, на них будут соответственно master и две slave ноды):
![redis_cluster_docker](/hw_2/pictures/redis_cluster_docker.png)

Опять проверим, что redis отвечает:
![redis_cluster_ping](/hw_2/pictures/redis_cluster_ping.png)

Удостоверимся, что конфигурация нод соответствует желаемой:
![redis_cluster_info](/hw_2/pictures/redis_cluster_info.png)

Как можем видеть, у master ноды действительно 2 slaves.

Осталось посмотреть производительность аналогичным прошлому способом (не забыть поменять порт в [тестовом файле](/hw_2/json_redis_test.py) на 6380!):
![redis_cluster_time](/hw_2/pictures/redis_cluster_time.png)

Видим, что время работы запросов на кластере возросло, что есть некоторая плата за синхронизацию и, как следствие, большую надежность.