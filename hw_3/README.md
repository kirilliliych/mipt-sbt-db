# CouchDB + PouchDB
## Установка
Установим CouchDB, пользуясь гайдом по [ссылке](https://vegastack.com/tutorials/how-to-install-couchdb-on-ubuntu-22-04/).

## Работа в CouchDB
В браузере перейдем по ссылке `http://127.0.0.1:5984/_utils/` и залогинимся: логин `admin`,
пароль `password` (пароль выбран при установке couchDB).
В открывшемся веб-интерфейсе создадим базу данных `sbt_hw3_db` через _Create database_:
![creating_database](/hw_3/pictures/creating_database.png)

Затем добавим в него документ с моей фамилией через _New document_->_Create document_, вписав "name":
![adding_name_to_document](/hw_3/pictures/adding_name_to_document.png)

Включим CORS в Config, поставим _All domains_, чтобы точно не было проблем с подключением к базе данных:
![configuring_CORS](/hw_3/pictures/configuring_CORS.png)

Теперь нужно отредактировать [html-файл](/hw_3/ДЗ3.html): в качестве src на строке 18 поставим
`"http://cdn.jsdelivr.net/npm/pouchdb@8.0.1/dist/pouchdb.min.js"`, как на [официальном сайте](https://pouchdb.com/download.html),
а на строке 25 - адрес, по которому будет осуществляться доступ к базе данных: `'http://localhost:5984/sbt_hw3_db'`

Затем откроем html-файл, нажмем на `Sync` и убедимся, что фамилия выводится:
[html_first_launch](/hw_3/pictures/html_first_launch.png)

После этого остановим CouchDB:
[stopping_couch](/hw_3/pictures/stopping_couchDB.png)

Когда после этого обновим/переоткроем html-страницу и снова нажмем на 'Sync', то сможем
убедиться, что фамилия по-прежнему выводится:
[html_after_stopping_couchDB](/hw_3/pictures/html_after_stopping_couchDB.png)

Тем не менее, сервер с удаленной базой данных отключен:
[couchDB_stopped_proof](/hw_3/pictures/couchDB_stopped_proof.png)

Произошло это вследствие синхронизации с локальной PouchDB, то есть в случае недоступности
удаленной PouchDB локальная все еще может показать данные, сохраненные с момента последнего подключения.

[Сохраненный из Chrome html-файл](/hw_3/PouchDB.html)

