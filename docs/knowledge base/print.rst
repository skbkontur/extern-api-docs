

Печать документов
=================

Особенности метода 
------------------

Метод печати Print может преобразовать документы в печатную форму контролирующего органа в виде pdf файла. Метод поддерживает не все типы документов и работает с ограничениями на тип передаваемого контента. Ниже мы привели список исключений, но его знать не обязательно. Если печать невозможна, метод вернет ошибку 400 documentPrintUnsupported.

**Метод печати умеет работать только с контентами следующих типов документов:**

1. "application/octet-stream",
2. "application/xml",
3. "text/xml"

**Метод печати не поддерживает следующие типы документов:**

1. urn:document:fns534-report-description
2. urn:document:fns534-report-attachment
3. urn:document:fns534-letter-description
4. urn:document:fns534-letter-attachment
5. urn:document:fns534-submission-description
6. urn:document:fns534-application-description
7. urn:document:stat-report-description
8. urn:document:pfr-report-description
9. urn:document:pfr-report-attachment
10. urn:document:pfr-report-error-description
11. urn:document:pfr-report-protocol-appendix
12. urn:document:fss-report-date-confirmation
13. urn:document:fss-report-error
14. urn:document:fss-report-error-receipt
15. urn:document:fss-report-receipt
16. urn:document:fss-report-date-confirmation

В теле метода необходимо передать идентификатор из :doc:`сервиса контенов</knowledge base/content>` content-id, по которому можно получить контент. **Контент должен быть расшифрованным и разжатым.**

    Если документ в документообороте уже расшифрован и разжат, у документа признаки encrypted, compressed равны false — скачивать ничего не нужно, передайте в теле запроса идентификатор. 

    *Если документ зашифрован и сжат*, то вам необходимо самостоятельно на своей стороне скачать его, расшифровать и извлечь контент из архива. Далее нужно загрузить контент обратно в сервис контентов и передать идентификатор методу печати.

Асинхронное выполнение метода
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Метод печати рекомендуем запускать с флагом deferred = "true". Тогда метод будет выполняться асинхронно. В ответе вам вернется TaskId поставленной задачи. Для получения результата печати нужно проверить статус выполнения задачи по TaskId. Если задача успешно выполнена, в ответе вернется идентификатор сервиса контентов, по которому можно получить печатную форму документа.

Если флаг deferred = "false" или не передан, то необходимо дождаться результата выполнения запроса. В случае успеха метод вернет идентификатор сервиса контентов, по которому можно получить печатную форму документа.

Проверка подписи
~~~~~~~~~~~~~~~~

Во время печати метод проверяет переданный на печать расшифрованный и разжатый документ на соответствие подписи этого документа в документообороте. Если на печать передали контент измененного документа, то вернется ошибка.

Пример печати документа
~~~~~~~~~~~~~~~~~~~~~~~

Для удобства тестирования алгоритма печати можно скачать файл коллекции Postman:

:download:`файл коллекции Postman <../files/печать.postman_collection.json>`

1. Получаем документ в документообороте методом GET DocflowDocument. В ответе нам важно посмотреть, что лежит в параметре docflow-document-contents.

**Запрос**

.. code-block:: http

    GET /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8 HTTP/1.1
    X-Kontur-Apikey: ****
    Authorization: auth.sid ****

.. container:: toggle

    .. container:: header

        **Ответ GET DocflowDocument:**

    .. code-block:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=utf-8
        Content-Encoding: gzip

        {
            "id": "75d929b9-08a9-4692-961d-111cc87dc2e8",
            "description": {
                "type": "urn:document:fns534-report",
                "filename": "NO_SRCHIS_0007_0007_7757424860680345565_20200129_92425a70-4ac9-4680-bada-3666f0c0514n.xml",
                "content-type": "application/xml",
                "encrypted-content-size": 2237,
                "compressed": true,
                "requisites": {},
                "related-docflows-count": 0,
                "support-recognition": false,
                "encrypted-certificates": [
                {
                    "serial-number": "01D0850043AB3C924A605B8D8661E43E"
                },
                {
                    "serial-number": "33AC7500C3AAAE924839AA8AE6C459FE"
                },
                {
                    "serial-number": "19CCC7C800010000215D"
                }
                ]
            },
            "content": {
                "encrypted": {
                "rel": "encrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8/encrypted-content"
                },
                "docflow-document-contents": [
                {
                    "content-id": "f1facbc3-5d74-498f-a8af-dbfd57f82f1f",
                    "encrypted": true,
                    "compressed": true
                }
                ]
            },
            "send-date": "2020-02-26T06:51:08.4636938Z",
            "signatures": [
                {
                "id": "82d5457d-5297-49fb-949a-f9865a1491b1",
                "title": "ООО 'Баланс Плюс' (Марков Георгий Эльдарович)",
                "signature-certificate-thumbprint": "20AACA440F33D0C90FBC052108012D3062D44873",
                "content-link": {
                    "rel": "content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8/signatures/82d5457d-5297-49fb-949a-f9865a1491b1/content"
                },
                "links": [
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8/signatures/82d5457d-5297-49fb-949a-f9865a1491b1/content"
                    },
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9"
                    }
                ]
                },
                {
                "id": "045d9beb-7748-4789-a539-4416fa7969b9",
                "title": "ООО 'Баланс Плюс' (Марков Георгий Эльдарович)",
                "signature-certificate-thumbprint": "20AACA440F33D0C90FBC052108012D3062D44873",
                "content-link": {
                    "rel": "content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8/signatures/045d9beb-7748-4789-a539-4416fa7969b9/content"
                },
                "links": [
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8/signatures/045d9beb-7748-4789-a539-4416fa7969b9/content"
                    },
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9"
                    }
                ]
                },
                {
                "id": "565164bb-c9d5-4805-8250-7f6a4ac9d4aa",
                "title": "Корионов  Илья Валерьянович",
                "signature-certificate-thumbprint": "344AAD7111FC77ADE2A98FFB5E35F039BC4DD650",
                "content-link": {
                    "rel": "content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8/signatures/565164bb-c9d5-4805-8250-7f6a4ac9d4aa/content"
                },
                "links": [
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8/signatures/565164bb-c9d5-4805-8250-7f6a4ac9d4aa/content"
                    },
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9"
                    }
                ]
                }
            ],
            "links": [
                {
                "rel": "docflow",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9"
                },
                {
                "rel": "self",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8"
                },
                {
                "rel": "related-docflow",
                "href": "https://extern-api.testkontur.ru//v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8/related"
                },
                {
                "rel": "encrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8/encrypted-content"
                },
                {
                "rel": "decrypt-content",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8/decrypt-content"
                }
            ]
        }

Как видно из параметра docflow-document-contents контент можно получить по идентификатору content-id в сервисе контентов. Сам контент зашифрован и сжат. 

2. Если контент зашифрован и сжат, скачиваем контент из сервиса контентов. Иначе переходим к п.5.
3. Расшифровываем и разархивируем контент.
4. Загружаем конент в сервис контентов. Или сразу переходим к п.5.
5. Запускаем печать методом Print. В теле метода можно передать сам контент или идентификатор из сериса контентов. В ответе вернется идентификатор задачи TaskId.

**Запрос**

.. code-block:: http

    POST /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8/print?deferred=true HTTP/1.1
    X-Kontur-Apikey: ****
    Authorization: auth.sid ****
    Content-Type: application/json

    {
        "content-id": "d065adea-8b9d-4228-bc17-8f86539e01a3"
    }

**Ответ**

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=utf-8
    Content-Length: 126

    {
        "id": "819ade20-665c-470a-befc-e897a56e1641",
        "task-state": "running",
        "task-type": "urn:task-type:docflowPrint"
    }

6. Получаем результат выполнения задачи на печать в методе GET Task.

**Запрос**

.. code-block:: http

    GET /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8/tasks/819ade20-665c-470a-befc-e897a56e1641 HTTP/1.1
    X-Kontur-Apikey: ****
    Authorization: auth.sid ****

**Ответ**

.. code-block:: http
    
    HTTP/1.1 200 OK
    Content-Type: application/json; charset=utf-8
    Content-Length: 210

    {
        "id": "819ade20-665c-470a-befc-e897a56e1641",
        "task-state": "succeed",
        "task-type": "urn:task-type:docflowPrint",
        "task-result": {
            "content-id": "9f6b57db-db9f-4e4c-8375-62a3504e663d"
        }
    }

7. Получаем документ из сервиса контентов, будет загружен готовый pdf файл.
