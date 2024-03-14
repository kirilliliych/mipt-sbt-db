## Установка Docker
Будем развертывать MongoDB в Docker. Разумно предположить, что для этого потребуется установить Docker. Сделаем это, следуя инструкции по [ссылке](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04). Запустим `hello-world`, чтобы удостовериться, что Docker работает корректно:
![docker_hello_world](/pictures/installed_docker.png)

## Установка MongoDB
Развернем MongoDB в Docker через ![docker-compose файл](/docker-compose.yaml) командой docker compose up:
![docker_compose_up](/pictures/installed_mongo_docker.png)

До кучи поставим GUI MongoDB Compass, так хоть не только на голую консоль смотреть) Скачаем [отсюда](https://www.mongodb.com/try/download/compass)
MongoDB Shell и MongoDB Compass и установим (GDebi package installer в помощь):
![installed_mongo_shell](/pictures/installed_mongosh.png)
![installed_mongodb_compass](/pictures/installed_mongodb_compass.png)

## Создание базы данных и коллекции, заполненной датасетом
Создадим базу данных `people_parameters` и в ней коллекцию `height_weight_18yo`: для разнообразия (иначе зачем гуи?)
сделаем это в графическом интерфейсе (мне точно не лень писать mongoimport):
![made_db_and_collection](/pictures/created_database_and_collection.png)

Пользуясь удобным функционалом `ADD DATA`->`Import JSON or CSV file`, импортируем
[датасет с ростом и весом 18-летних людей](https://www.kaggle.com/datasets/burnoutminer/heights-and-weights-dataset?resource=download)
в коллекцию:
![import_dataset](/pictures/import_csv.png)

## Выполнение CRUD операций
Теперь будем пользоваться MongoDB Shell (иначе неинтересно).
### C - create
Вставим значения по абсолютно случайно выбранным индексам 52 (`insertOne`) и 1337, 6666 (`insertMany`).
![insert_one_and_many](/pictures/insert_one_and_many.png)

Проверим, что вставленные документы действительно оказались в коллекции:
![results_insert_one_and_many_additional](/pictures/result_6666_insert_many.png)
![result_6666_insert_many.png](/pictures/result_6666_insert_many.png)

### R - read
Выполним `find` чуть посложнее, чем вся коллекция:
![find](/pictures/find.png)

А что будет, если под фильтр `findOne` попадают несколько документов? Посмотрим на примере:
![find_one](/pictures/find_one.png)

(Ага, если документ был вставлен раньше другого, то и `findOne` находит именно его!) На самом деле все зависит от
натурального порядка, который (см. [ссылку](https://www.mongodb.com/docs/manual/reference/method/db.collection.findOne/))
определяет формат хранения данных на диске.

### U - update
Обновим пару значений через `updateOne` и `updateMany`:
![update_one_and_many](/pictures/update_one_and_many.png)

Видим, что у документов, удовлетворяющих фильтру, заменились соответствующие поля.

Теперь применим `replaceOne` к одному из обновленных документов и посмотрим результат выполнения:
![replace_one](/pictures/replace_one.png)
Документ под индексом 1337 исчез, а его место занял документ под индексом 666, как и предполагалось.

### D - delete
Удалим только что созданный путем `replaceOne` документ `{"Index": 666, "Height(Inches)": 66}`, а также
все документы, где Weight меньше 110 фунтов (нет анорексии):
![delete_one](/pictures/delete_one.png)
![delete_one](/pictures/delete_many.png)

## Добавление индекса
Выполним запрос `db.height_weight_18yo.find({'Height(Inches)': {$gt: 70}}).explain("executionStats")`,
который затронет большинство документов коллекции и предоставит информацию об исполнении `find` с соответствующим фильтром.

Нас интересует количество исследованных документов:
![no_index_find](/pictures/no_index_find.png)

Видим, что под нее попало абсолютное большинство (если не все) документы коллекции; кроме того, операция заняла 21 миллисекунду
(executionTimeMillis).

Добавим возрастающий индекс по полю Height(Inches):
![added_index](/pictures/added_index.png)

Затем выполним вышеупомянутый запрос:
![index_find](/pictures/index_find.png)

В силу упорядочивания по индексу существенно уменьшилось количество исследованных документов, что на больших выборках данных
даст значительный прирост производительности. Кроме того, несколько уменьшилось executionTimeMillis -- теперь 17
миллисекунд вместо 21. Победа!

