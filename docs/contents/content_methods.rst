.. _`POST Upload`: https://developer.testkontur.ru/extern/post-v1-%7BaccountId%7D-contents
.. _`PUT UploadByParts`: https://developer.testkontur.ru/extern/put-v1-%7BaccountId%7D-contents-%7Bid%7D
.. _`GET Download`: https://developer.testkontur.ru/extern/get-v1-%7BaccountId%7D-contents-%7Bid%7D

Методы сервиса контентов
========================

.. _rst-marckup-post-content:

Инициализация загрузки контента
-------------------------------

Метод: `POST Upload`_

Метод инициализирует загрузку контента. Для загрузки документов размером больше 64 Мбайт следует применять загрузку по частям.

**Заголовки запроса**

``Content-Type`` — отвечает за тип сохраняемого контента, если он не передан, будет использовано значение по умолчанию application-octet/stream.

``Content-Range`` — инициализирует частичную загрузку контента. Если заголовок не передать, контент будет загружен за один запрос.

    В Content-Range указаны необходимые байтовые диапазоны. Принимает значения вида: "bytes {from}-{to}/{totalLength}" или "bytes {from}-{to}/*", где:

    * from — целое число. Начало диапазона.
    * to — целое число. Конец диапазона.
    * totalLength — целое число. Размер всего контента.

    Если заранее не известен размер всего контента, вместо totalLength указывается * . В этом случае решение о полной загрузке контента будет приниматься только после получения сервером запроса с явным указанием totalLength.

**Коды ответа**

- 200 — инициализирована загрузка контента по частям. В ответе будет содержаться идентификатор контента. Необходимо продолжить загрузку методом PUT.
- 201 — загрузка контента завершена. В ответе будет содержаться идентификатор контента. 

.. _rst-marckup-put-content:

Загрузка контента по частям
---------------------------

Метод: `PUT UploadByParts`_

Метод загружает часть контента.

**Заголовки запроса**

 ``Content-Range`` — указывает необходимые байтовые диапазоны части загружаемого контента. Рекомендуется разбивать контенты на части по 64 Мбайт. Загрузка частей возможна в любом порядке. 

**Коды ответа**

- 200 — часть контента успешно загружена. Ответ содержит идентификатор контента.
- 201 — последняя часть контента успешно загружена. Ответ содержит идентификатор загруженного контента.

.. _rst-marckup-get-content:

Получение контента по идентификатору
------------------------------------

Метод: `GET Download`_

Метод инициализирует скачивание контента полностью или по частям. Для загрузки контента по частям необходимо передать заголовок Range.

**Коды ответа**

- 200 — скачивание контента успешно завершено. Ответ содержит контент запрошенного ресурса.
- 206 — скачивание части контента успешно завершено. Ответ содержит контент запрошенного ресурса.