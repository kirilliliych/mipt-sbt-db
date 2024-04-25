# Weaviate - Vector Database
![weaviate_logo](/pictures/weaviate_logo.png)

## История развития Weaviate
[Weaviate - это опенсорсная СУБД](https://weaviate.io/), предназначенная для хранения, поиска и анализа как структурированных, так и неструктурированных данных. История развития этой системы начинается в _2018_ году, когда команда разработчиков из компании SeMI Technologies начала работу над проектом.

Идея создания Weaviate возникла из необходимости разработки системы, способной эффективно обрабатывать сложные структурированные и неструктурированные данные в реальном времени. Разработчики стремились создать интеллектуальную СУБД, способную обрабатывать данные различных типов и источников, а также предоставлять разнообразные методы поиска и анализа информации. Основными достоинствами Weaviate являются семантический поиск и семантическая классификация данных.

Первая версия Weaviate была выпущена в конце _2018_ года и содержала основные функции, такие как хранение структурированных и неструктурированных данных, поиск информации с использованием векторных запросов и автоматическое индексирование данных для быстрого доступа. С течением времени разработчики постоянно совершенствовали систему. В _2020_ году была запущена облачная версия Weaviate, что позволило пользователям использовать систему без необходимости установки и настройки на собственных серверах.

В настоящее время Weaviate является одной из ведущих СУБД, предоставляя широкий спектр возможностей для хранения и анализа данных различных типов. Разработчики продолжают активно развивать систему, добавляя новые функции и интеграции, чтобы удовлетворить потребности пользователей в области обработки больших данных и машинного обучения.

## Инструменты для взаимодействия с Weaviate
Weaviate предлагает [следующие способы взаимодействия](https://weaviate.io/developers/weaviate/concepts/interface):
1. [GraphQL API](https://weaviate.io/developers/weaviate/api/graphql) -- имеет достаточно жестко фиксированный формат с целью борьбы с переизбытком/недостатком возвращенных данных, обычно используется для доступа к объектам данных, будь это простой просмотр объекта или полноценный скалярный/векторный поиск.
2. [REST API](https://weaviate.io/developers/weaviate/api/rest) -- как правило, используется для CRUD-операций и управления самой базой данных. С версии v1.23 доступен стабильный [gRPC API](https://weaviate.io/developers/weaviate/api/grpc), который быстрее и проще в использовании.
3. Клиентские библиотеки для некоторых популярных языков (использующие вышеупомянутые принципы):
    - [Python](https://weaviate.io/developers/weaviate/client-libraries/python)
    - [JavaScript/TypeScript](https://weaviate.io/developers/weaviate/client-libraries/typescript)
    - [Go](https://weaviate.io/developers/weaviate/client-libraries/go)
    - [Java](https://weaviate.io/developers/weaviate/client-libraries/java)
Также присутствует [небольшой список библиотек, поддерживаемых сообществом](https://weaviate.io/developers/weaviate/client-libraries/community)(.NET/C#, PHP, Ruby).
4. Возможно и взаимодействие из командной строки, так как есть [официальный CLI](https://github.com/weaviate/weaviate-cli), с помощью него можно взаимодействовать с Weaviate из терминала.

## Какой database engine используется в Weaviate?
Weaviate использует свой собственный database engine, отличный от привычных нам в других СУБД, и сам по сути является таковым. Вместо традиционного формата хранения данных используется механизм "векторной индексации" (vector indexing). Пространство данных представляется не привычными строками и колонками, а чем-то похожим на векторное пространство, где объекты со схожими параметрами будут находиться, условно говоря, недалеко друг от друга. Поиск, как правило, не выдаст 100% корректный результат, но найдет весьма похожий. Подробнее по [ссылке](https://weaviate.io/developers/weaviate/introduction), раздел "What is a vector database?".

## Как устроен язык запросов в Weaviate?
В основном запросы осуществляются с помощью функций из библиотек для языков программирования. Есть стандартные CRUD-операции: `create` (создать коллекцию), `insert`, `insert_many`, `delete_by_id`, `delete_many`, `update`... Есть и привычные `exists`, `replace`, простой поиск `fetch_objects` наподобие `SELECT` в SQL, но интереснее посмотреть основную фишку Weaviate - векторный поиск.

Пользуясь облачной версией Weaviate, создадим там схему-песочницу:
![creating_sandbox](pictures/creating_sandbox.png)

Соединимся с песочницей по URL и токену, создадим там таблицу `Question` и заполним ее данными из небольшого датасета:

```
client = weaviate.connect_to_wcs(
    cluster_url="https://mipt-sbt-db-5bhod7yu.weaviate.network",
    auth_credentials=weaviate.auth.AuthApiKey("gJ0sD5gCiFyPKTUdCjPmkS2984c6ZKrbWFI9"),
    headers={
        "X-OpenAI-Api-Key": "sk-proj-pWYMnmCAq3dWzm8PddM8T3BlbkFJ0NDY1ucxbbSo3XZZBGVt"
    }
)

try:
    # creating collection "Question"
    questions = client.collections.create(
        name="Question",
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
        generative_config=wvc.config.Configure.Generative.openai()
    )

    # importing data
    resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
    data = json.loads(resp.text)  # loading data

    question_objs = list()
    for i, d in enumerate(data):
        question_objs.append({
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        })

    questions = client.collections.get("Question")
    questions.data.insert_many(question_objs)


finally:
    client.close()  # closing client
```

Поскольку в коллекции сконфигурирован `Vectorizer`, наши данные хранятся там не просто в виде строки, а в виде вектора.
Значит, теперь мы можем применить семантический векторный поиск! Поиск `near_text` ищет те объекты, чьи вектора наиболее сходны с запрашиваемым:

```
# semantic search for vector which are most similar to that of "biology"
questions = client.collections.get("Question")
response = questions.query.near_text(
    query="biology",
    limit=2
)
print(response.objects[0].properties) # getting only first object
```

Результат:
![ans1](/pictures/ans1.png)

Возвращено 2 результата, поскольку установлен лимит в 2 ответа.

Этот же поиск можно отфильтровать. Например, хотим видеть ответы на предыдущий запрос только из категории "ANIMALS" (животные). Тогда отфильтруем:
```
response = questions.query.near_text(
    query="biology",
    limit=2,
    filters=wvc.query.Filter.by_property("category").equal("ANIMALS")
)
print(response.objects[0].properties)
```

Результат:
![ans2](/pictures/ans2.png)

Теперь попробуем генеративный поиск: в нем промптом для LLM (большой языковой модели) служит комбинация запроса пользователя и полученной из базы данных информации.
Попросим найденные результаты объяснить ОЧЕНЬ подробно:

```
response = questions.generate.near_text(
    query="biology",
    limit=2,
    single_prompt="Explain {answer} as you might to a five-year-old."
)
print(response.objects[0].generated)
```

Увидим результат:
![ans3](/pictures/ans3.png)

Можно видеть, что результаты те же самые, что и раньше, но теперь они включают в себя дополнительно сгенерированный текст с объяснением каждого ответа.

Теперь посмотрим групповой генеративный поиск, в которым один ответ использует все результаты запроса к базе данных:
```
response = questions.generate.near_text(
    query="Cute animals",
    limit=3,
    grouped_task="What do these animals have in common, if anything?"
)
print(response.generated)
```

Результат:
![ans4](/pictures/ans4.png)
## 
