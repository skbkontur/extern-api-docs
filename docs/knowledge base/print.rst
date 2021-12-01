Печать документов
=================

В API Контур.Экстерна реализована печать документов в черновиках и документооборотах. 

* для печати документа в черновике используйте метод :ref:`GET DraftDocumentPrint<rst-markup-draft-print>`.
* для печати документа в документообороте используйте метод :ref:`POST DocflowDocumentPrint<rst-markup-dcprint>`.
* для печати документа в документообороте описи используйте метод :ref:`POST DocumentPrint<rst-markup-inventory-print>`.

Особенности методов печати
--------------------------

1. Методы печати подготавливают печатную форму документа в формате pdf файла.
2. Методы работают только с расшифрованными контентами.
3. Методы поддерживают не все типы документов и контентов. Если печать невозможна, методы вернут ошибку 400 documentPrintUnsupported.
4. Методы печати умеют работать только со следующими типами контента:

	- «application/octet-stream»,
	- «application/xml»,
	- «text/xml».

.. _rst-markup-print-async:

Асинхронный вызов методов
-------------------------

Рекомендуется выполнять запросы печати документа асинхронно. Для этого в параметрах запроса необходимо передать флаг deferred = true. Если флаг deferred = false или не передан, запрос выполняется синхронно. Так как операция печати может быть трудоемкой, вы можете не дождаться ее окончания.  

Асинхронный вызов запроса создает задачу на печать. В ответе метода вернется идентификатор TaskId поставленной задачи. Для получения печатной формы нужно проверить статус выполнения задачи. Когда статус задачи будет равен succeed, печатная форма будет загружена в сервис контентов. В поле task-result будет лежать идентификатор контента content-id.

.. Для синхронного вызова методов есть ограничение на размер печатаемого файла: 32 МБ для тестовой и 64 МБ для рабочей площадки. Если контент файла будет больше указанных значений, методы вернут ошибку 400 contentIsTooLarge. В случае успеха метод сразу вернет сформированную печатную форму документа:

Синхронный вызов метода в случае успеха сразу вернет сформированную печатную форму документа:

  - для документа в черновике в виде строки в формате base64;
  - для документа в документообороте ответ будет в том же формате, что и запрос. Если в запросе контент передан в формате base64, метод вернет строку с печатной формой в формате base64. Если в запросе передан content-id, результат также будет загружен в сервис контентов.


Печать документа в черновике
----------------------------

Методу печати в черновике в запросе нужно передать только идентификатор документа, так как все расшифрованные контенты были предварительно загружены в черновик.

Алгоритм печати документа в черновике
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Вызвать метод печати :ref:`GET DraftDocumentPrint <rst-markup-draft-print>` с флагом deferred = true. В случае успеха метод вернет идентификатор TaskId поставленной на печать задачи.
2. Получить задачу :ref:`GET DraftDocumentTask<rst-markup-DraftDocumentTask>` по TaskId. Когда статус будет равен значению succeed, в поле task-result будет лежать идентификатор контента content-id.
3. Получить сформированную печатную форму документа :ref:`GET Download<rst-markup-get-content>` по content-id.

Печать документа в документообороте
-----------------------------------

**Как передать расшифрованный контент документа** 
    
    Для метода печати в документообороте :ref:`DocflowDocument Print<rst-markup-dcprint>` в теле запроса необходимо передать идентификатор расшифрованного контента документа из :doc:`сервиса контентов</knowledge base/content>`. 

    *Если документ зашифрован*, у документа в модели docflow-document-contents свойство encrypted равно true, то необходимо предварительно скачать и дешифровать документ. Если контент сжат — признак compressed = true, извлекать контент из архива не обязательно, метод умеет извлекать контент из архива. Далее нужно загрузить контент в сервис контентов. Полученный идентификатор передать в теле метода печати.

    *Если документ уже расшифрован*, у документа признак encrypted равен false — скачивать ничего не нужно,  в теле запроса передать идентификатор контента content-id. Идентификатор контента можно посмотреть в информации о документе, в параметре content. 

**Можно ли заранее узнать возможность печати?**

В свойствах документа есть вспомогательный параметр ``SupportPrint`` (модель DocflowDocumentDescription). Это поле подсказывает, возможна ли печать документа. Оно может принимать значения: Yes, No, Unknown. 

- Если значение ``SupportPrint = yes``, можно вызывать метод печати, и он вернет печатную форму документа.
- Если значение ``SupportPrint = no``, печать документа не поддерживается.
- Если значение ``SupportPrint = unknown``, не получилось определить возможность печати документа, можно попробовать вызвать метод печати. 

**Проверка подписи в документообороте**

Во время печати метод проверяет переданный на печать расшифрованный и разжатый документ на соответствие подписи этого документа в документообороте. Если на печать передали контент измененного документа, то вернется ошибка.

.. _rst-markup-process-print:

Алгоритм печати документа в документообороте
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Для удобства тестирования печати можно скачать файл коллекции Postman:

:download:`файл коллекции Postman <../files/печать.postman_collection.json>`

1. Получить документ в документообороте методом :ref:`GET DocflowDocument<rst-markup-get-dc-document>`. В ответе важно посмотреть, что лежит в параметре docflow-document-contents: идентификатор content-id, по которому можно получить контент в сервисе контентов, флаги compressed и encrypted. В примере ниже контент документа зашифрован и сжат, флаги равны true. 

**Запрос**

.. code-block:: http

    GET /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8 HTTP/1.1

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
                ],
                "support-print": "yes"
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

2. Скачать контент из сервиса контентов :ref:`GET Download<rst-markup-get-content>` по content-id.
3. Расшифровывать полученный документ и загрузить его обратно в сервис контентов :ref:`POST Upload<rst-markup-post-content>`. В ответе метод вернет новый идентификатор content-id2.
4. Вызвать метод печати :ref:`POST DocflowDocumentPrint<rst-markup-dcprint>` с флагом deferred = true. В теле метода передать content-id2. В ответе вернется идентификатор поставленной на печать задачи TaskId.

**Запрос**

.. code-block:: http

    POST /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8/print?deferred=true HTTP/1.1
    Authorization: Bearer <token>
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

5. Получить по TaskId результат выполнения задачи на печать в методе :ref:`GET DocflowDocumentTask<rst-markup-DocflowDocumentTask>`. Запрашивать задачу нужно до тех пор, пока task-state = running. Когда задача завершится со статусом succeed, в поле "task-result" будет лежать новый идентификатор content-id3.
    
    .. note:: Чем больше документ, тем больше времени необходимо сервису для печати, рекомендуемый интервал между повторными запросами — 5 секунд.

**Запрос**

.. code-block:: http

    GET /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/75d929b9-08a9-4692-961d-111cc87dc2e8/tasks/819ade20-665c-470a-befc-e897a56e1641 HTTP/1.1
    Authorization: Bearer <token>

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

6. Получить документ из сервиса контентов по content-id3. Будет загружен готовый pdf файл.
