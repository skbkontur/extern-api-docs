Печать документов
=================

Особенности печати документов 
-----------------------------

Методы печати :ref:`DocflowDocument Print<rst-markup-dcprint>` и :ref:`DraftDocument Print<rst-markup-draft-print>` подготавливают печатную форму документа в формате pdf файла. Методы поддерживают не все типы документов и контентов. Ниже приведен список исключений, но его знать не обязательно. Если печать невозможна, методы вернут ошибку 400 documentPrintUnsupported.

**Методы печати умеют работать только со следующими типами контента:**

1. "application/octet-stream",
2. "application/xml",
3. "text/xml"

**Методы печати не поддерживают следующие типы документов:**

1. urn:document:fns534-report-description;
2. urn:document:fns534-report-attachment — если тип контента не xml;
3. urn:document:fns534-letter-description;
4. urn:document:fns534-letter-attachment;
5. urn:document:fns534-submission-description;
6. urn:document:fns534-application-description;
7. urn:document:stat-report-description;
8. urn:document:pfr-report-description;
9. urn:document:pfr-report-error-description;
10. urn:document:pfr-report-protocol-appendix;
11. urn:document:fss-report-date-confirmation;
12. urn:document:fss-report-error;
13. urn:document:fss-report-error-receipt;
14. urn:document:fss-report-receipt;
15. urn:document:fss-report-date-confirmation.

Проверка подписи в документообороте
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Во время печати метод проверяет переданный на печать расшифрованный и разжатый документ на соответствие подписи этого документа в документообороте. Если на печать передали контент измененного документа, то вернется ошибка.

Параметры запроса 
~~~~~~~~~~~~~~~~~

Для метода печати в документообороте :ref:`DocflowDocument Print<rst-markup-dcprint>` в параметрах запроса необходимо передать конент документа. 

    В теле метода необходимо передать идентификатор из :doc:`сервиса контентов</knowledge base/content>` content-id, по которому можно получить контент. **Контент должен быть расшифрованным и разжатым.** Идентификатор контента можно посмотреть в информации о документе, в параметре content.

    *Если документ зашифрован или сжат*, у документа признаки encrypted, compressed равны true, то вам необходимо самостоятельно на своей стороне скачать его, расшифровать и/или извлечь контент из архива. Далее нужно загрузить контент в сервис контентов. Полученный идентификатор передать в теле метода печати.

    *Если документ уже расшифрован и разжат*, у документа признаки encrypted, compressed равны false — скачивать ничего не нужно, передайте в теле запроса идентификатор контента. 

Для метода печати в черновике :ref:`DraftDocument Print<rst-markup-draft-print>` нужно передать только идентификатор документа, так как все расшифрованные контенты были предварительно загружены в черновик. 

.. _rst-markup-deferred-print:

**Асинхронное выполнение метода** — ставится задача на печать.

Методы печати рекомендуется запускать с флагом ``deferred = true``. Тогда запрос будет выполняться асинхронно. В ответе вернется идентификатор поставленной задачи. Для получения результата печати нужно проверить статус выполнения задачи по TaskId. Для документооборота метод :ref:`GET DocflowDocumentTask<rst-markup-DocflowDocumentTask>`, для черновиков метод :ref:`GET DraftDocumentTask<rst-markup-DraftDocumentTask>`. Если задача успешно выполнена, в ответе вернется идентификатор сервиса контентов, по которому можно получить печатную форму документа.

**Синхронное выполнение** — ожидаем окончания работы метода.

Если флаг ``deferred = false`` или не передан, то необходимо дождаться результата выполнения запроса. В случае успеха будет сформирована печатная форма документа, результат возвращается в виде строки base64. 

.. _rst-markup-process-print:

Пример печати документа в документообороте
------------------------------------------

Для удобства тестирования печати можно скачать файл коллекции Postman:

:download:`файл коллекции Postman <../files/печать.postman_collection.json>`

1. Получить документ в документообороте методом GET DocflowDocument. В ответе важно посмотреть, что лежит в параметре docflow-document-contents.

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

В параметре docflow-document-contents находится идентификатор content-id, по которому можно получить конент в сервисе контентов. Сам контент зашифрован и сжат, флаги compressed и encrypted равны true. 

2. Скачать контент из сервиса контентов.
3. Расшифровывать м и разархивировать контент.
4. Загрузить контент в сервис контентов.
5. Запустить печать методом Print. В теле метода передать идентификатор из сериса контентов. В ответе вернется идентификатор поставленной на печать задачи TaskId.

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

6. Получить результат выполнения задачи на печать в методе :ref:`GET DocflowDocumentTask<rst-markup-DocflowDocumentTask>`. Запрашивать задачу нужно до тех пор, пока task-state = running. Когда задача завершится со статусом succeed, в поле "task-result" будет лежать content-id.
    
    Чем больше документ, тем больше времени необходимо сервису для печати, рекомендуется задать интервал между повторными запросами 5 секунд.

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

7. Получить документ из сервиса контентов. Будет загружен готовый pdf файл.
