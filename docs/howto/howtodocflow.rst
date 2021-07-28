.. _`описанием документов в документообороте с ФНС`: https://www.kontur-extern.ru/support/faq/41/246
.. _`GET Docflow`: https://developer.kontur.ru/doc/extern.docflows/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D
.. _`GET Docflows`: https://developer.kontur.ru/doc/extern.docflows/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows
.. _`специальный раздел методов`: https://developer.kontur.ru/doc/extern.docflows/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fgenerate-reply
.. _`GET Document`: https://developer.kontur.ru/doc/extern.docflows/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fcontents%2F%7Bid%7D
.. _`POST CreateReplyDocument`: https://developer.kontur.ru/doc/extern.docflows/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fgenerate-reply
.. _`POST SignReplyDocument`: https://developer.kontur.ru/doc/extern.docflows/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D%2Fdocuments%2F%7BdocumentId%7D%2Freplies%2F%7BreplyId%7D%2Fcloud-sign
.. _`PUT SaveReplyDocumentSignature`: https://developer.kontur.ru/doc/extern.docflows/method?type=put&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D%2Fdocuments%2F%7BdocumentId%7D%2Freplies%2F%7BreplyId%7D%2Fsignature
.. _`POST SendReplyDocument`: https://developer.kontur.ru/doc/extern.docflows/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D%2Fdocuments%2F%7BdocumentId%7D%2Freplies%2F%7BreplyId%7D%2Fsend

Работа с документооборотом
==========================

В предыдущей статье было описано, как отправлять отчет в налоговый орган. В этой статье рассмотрим завершение документооборота с налоговым органом: как получить документооборот, проверить его статус, получить входящие документы от контролирующего органа и сформировать ответный документ. 

.. rubric:: Что такое документооборот?

Документооборот (ДО) — это обмен юридически значимыми документами между организацией и контролирующим органом (КО).

.. image:: /_static/whatisdocflow.jpg

ДО характеризуется типом и статусом и появляется после отправки черновика или при поступлении входящего запроса к организации от контролирующего органа. 

Рассмотрим работу с документооборотом после отправки черновика отчета в ФНС. Когда вы поймете как работать с отчетом в ФНС, вам станет проще понимать процесс работы с другими типами документооборотов. 

Основные понятия
----------------

Прежде чем перейти к алгоритму действий изучите :ref:`процесс смены статусов ДО<rst-markup-fnsreport-status>` в зависимости от поступающих документов. А также ознакомьтесь с `описанием документов в документообороте с ФНС`_.

Если обобщить простыми словами, то в документообороте можно выделить три категории документов:

1. Отправленные документы — отчет пользователя с приложениями.
2. Входящие технологические документы — все, что пришло пользователю на его отправленный отчет. 
3. Ответный документ (reply document) — технологический документ Извещение о получении, который пользователь должен отправлять в ответ на входящие документы. Для создания ответных документов в документообороте будут появляться ссылки с типом *reply*.

У документооборота с ФНС типа декларация (urn:docflow:fns534-report) возможны следующие статусы:

* Отправлен (urn:docflow-common-status:sent) — черновик отправлен. В документообороте появился документ Подтверждение даты отправки, сформированный оператором ЭДО, а также новая ссылка с типом reply. Переходим к формированию ответного документа;
* Доставлен (urn:docflow-common-status:delivered) — документ дошел до ФНС и принят в работу. В документообороте при этом появится новый документ Извещение о получении, никаких действий не требуется;
* Получен ответ (urn:docflow-common-status:response-arrived) — на отправленный документооборот пришли результаты приема или результаты обработки. В документообороте появилась новая ссылка с типом reply. Переходим к формированию ответного документа;
* Ответ обработан (urn:docflow-common-status:response-processed) — пользователь отправил Извещение о получении на квитанцию о приеме;
* Завершен (urn:docflow-common-status:finished) — документооборот завершен. 

Особенности работы с документооборотом
--------------------------------------

1. Статусы документооборота меняются, когда появляются новые документы со стороны налоговой инспекции, либо при отправке Извещения о получении.
2. Ссылки с типом *reply* появляются постепенно после отправки документооборота. 
3. На все ссылки с типом *reply* необходимо сформировать ответный документ. 

.. note:: Таким образом, работа с документооборотом — это: 
    
    * запрос статуса документооборота (отслеживание изменений в метаинформации);
    * получение входящих документов от контролирующего органа;
    * формирование ответного документа по ссылкам с типом reply, по мере их появления в документообороте.

Порядок работы с документооборотом после отправки черновика
-----------------------------------------------------------

1. Запрашиваем статус документооборота. Ожидаем значение статуса "Отправлен" и получения подтверждения даты отправки.
2. Формируем и отправляем ответный документ.
3. Запрашиваем статус документооборота. Ожидаем значение статуса "Доставлен" и появления извещения о получении либо сообщения об ошибке. 
    
    - Если было получено сообщение об ошибке, документооборот завершен.

4. Запрашиваем статус документооборота. Ожидаем значение статуса "Получен ответ" и получения квитанции о приеме либо уведомления об отказе. Квитанция подтверждает факт приема отчета, уведомление об отказе свидетельствует, что отчет не прошел проверку. 
5. Смотрим и печатаем результаты приема отчета.
6. Формируем и отправляем ответные документы.

    - Если в результате приема пришло уведомление об отказе, документооборот завершен. Нужно исправить ошибки и отправить отчет заново. 

7. Запрашиваем статус документооборота. Ожидаем получения извещения о вводе или уведомления об уточнении — результатов обработки. Данные документы подтверждают факт переноса данных отчета в базу налогового органа.
8. Смотрим и печатаем результаты обработки. 
9. Формируем и отправляем ответный документ. Документооборот завершен, статус должен смениться на "Завершен". Если пришло уведомление об уточнении, пользователю необходимо ознакомиться с документом и, возможно, направить корректировку отчета.

**Порядок работы в виде схемы:**

.. image:: /_static/docflow.jpg
    :width: 800

*Документы от контролирующего органа могут прийти раньше, чем вы проверите статус документооборота. Поэтому вы можете не увидеть некоторые статусы, а сразу получить в документообороте N новых документов со статусом "Получен ответ". В этом случае нужно сформировать ответные документы по всем ссылкам типа reply и завершить документооборот*.

Для удобства тестирования работы с документооборотом можно скачать файл коллекции Postman:

:download:`файл коллекции Postman <../files/Работа с документооборотом.postman_collection.json>`

.. _rst-markup-track-docflow-status:

Проверка статуса документооборота
---------------------------------

В этом примере рассмотрим, как по идентификатору получить документооборот и посмотреть его статус.

Запросить статус документооборота можно двумя способами. Первый — запрашивать периодически конкретный документооборот, запомнив его id при отправке черновика, методом `GET Docflow`_. Второй — запрашивать список документооборотов своей учетной записи методом `GET Docflows`_.

После успешной отправки черновика методом Send вы получите идентификатор сформированного документооборота. Для примера посмотрим результат выполнения задачи методом :ref:`GET DraftTask<rst-markup-draftTask>`. В параметре task-result лежит идентификатор документооборота. 

Также можно выполнить поиск документооборотов и выбрать нужный идентификатор в общем списке. По полученному идентификатору получаем документооборот методом :ref:`GET Docflow<rst-markup-get-dc>`. В ответе метода нужно посмотреть на статус документооборота и сформированные ссылки (параметры status и links).

**Пример запроса GET Docflow**

.. code-block:: http

    GET /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9 HTTP/1.1
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json

.. container:: toggle

    .. container:: header

        **Пример ответа GET Docflow**

    .. code-block:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=utf-8
        
        {
            "id": "0c4e50b5-66ac-4a92-b051-3bc95472dddb",
            "organization-id": "988b38f1-5580-4ba9-b9f8-3215e7f392ea",
            "type": "urn:docflow:fns534-report",
            "status": "urn:docflow-common-status:response-arrived",
            "success-state": "urn:docflow-state:successful",
            "description": {
                "form-version": {
                "knd": "1110018",
                "version": "100501",
                "form-fullname": "Сведения о среднесписочной численности работников за предшествующий календарный год",
                "form-shortname": "Сведения о среднесписочной численности"
                },
                "recipient": "0007",
                "final-recipient": "0007",
                "correction-number": 0,
                "period-begin": "2018-01-01T00:00:00.0000000",
                "period-end": "2018-12-31T00:00:00.0000000",
                "period-code": "34",
                "payer-inn": "7757424860-680345565",
                "original-draft-id": "d9622b9d-aa31-477b-a399-fc676588bfb5"
            },
            "documents": [
                {
                "id": "09da96fe-a21a-4f69-84db-ff9d82c86bde",
                "description": {
                    "type": "urn:document:fns534-report-processing-result-ok",
                    "filename": "IV_NOSRCHIS_7757424860_7757424860_0007_20200422_171abbd163074f34ae30d3f9b9439579.xml",
                    "content-type": "application/xml",
                    "encrypted-content-size": 1642,
                    "compressed": true,
                    "requisites": {},
                    "support-recognition": false,
                    "encrypted-certificates": [
                    {
                        "serial-number": "01D0850043AB3C924A605B8D8661E43E"
                    }
                    ]
                },
                "content": {
                    "encrypted": {
                    "rel": "encrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/09da96fe-a21a-4f69-84db-ff9d82c86bde/encrypted-content"
                    },
                    "docflow-document-contents": [
                    {
                        "content-id": "7eded1eb-5d84-4e64-b8ca-82576a345eb0",
                        "encrypted": true,
                        "compressed": true
                    }
                    ]
                },
                "send-date": "2020-04-22T14:17:13.8960679Z",
                "signatures": [
                    {
                    "id": "c3eca6e8-2409-41e5-aec5-3aa1a566fb6e",
                    "title": "Корионов  Илья Валерьянович",
                    "signature-certificate-thumbprint": "344AAD7111FC77ADE2A98FFB5E35F039BC4DD650",
                    "content-link": {
                        "rel": "content",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/09da96fe-a21a-4f69-84db-ff9d82c86bde/signatures/c3eca6e8-2409-41e5-aec5-3aa1a566fb6e/content"
                    },
                    "links": [
                        {
                        "rel": "self",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/09da96fe-a21a-4f69-84db-ff9d82c86bde/signatures/c3eca6e8-2409-41e5-aec5-3aa1a566fb6e/content"
                        },
                        {
                        "rel": "docflow",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb"
                        }
                    ]
                    }
                ],
                "links": [
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb"
                    },
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/09da96fe-a21a-4f69-84db-ff9d82c86bde"
                    },
                    {
                    "rel": "reply",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/09da96fe-a21a-4f69-84db-ff9d82c86bde/generate-reply?documentType=fns534-report-receipt",
                    "name": "fns534-report-receipt"
                    },
                    {
                    "rel": "encrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/09da96fe-a21a-4f69-84db-ff9d82c86bde/encrypted-content"
                    },
                    {
                    "rel": "decrypt-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/09da96fe-a21a-4f69-84db-ff9d82c86bde/decrypt-content"
                    }
                ]
                },
                {
                "id": "68ed1449-d420-44df-a0ed-57568a1c7904",
                "description": {
                    "type": "urn:document:fns534-report-acceptance-result-positive",
                    "filename": "KV_NOSRCHIS_7757424860_7757424860_0007_20200422_726d74c3db7d41bbae6527512765b313.xml",
                    "content-type": "application/xml",
                    "encrypted-content-size": 1809,
                    "compressed": true,
                    "requisites": {},
                    "support-recognition": false,
                    "encrypted-certificates": [
                    {
                        "serial-number": "01D0850043AB3C924A605B8D8661E43E"
                    }
                    ]
                },
                "content": {
                    "encrypted": {
                    "rel": "encrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/68ed1449-d420-44df-a0ed-57568a1c7904/encrypted-content"
                    },
                    "docflow-document-contents": [
                    {
                        "content-id": "2213c733-b4a8-413b-a7d5-17a35e0149f4",
                        "encrypted": true,
                        "compressed": true
                    }
                    ]
                },
                "send-date": "2020-04-22T14:16:43.3017428Z",
                "signatures": [
                    {
                    "id": "0f9a8e29-8e55-4e4e-87ed-8d9b685fb585",
                    "title": "Корионов  Илья Валерьянович",
                    "signature-certificate-thumbprint": "344AAD7111FC77ADE2A98FFB5E35F039BC4DD650",
                    "content-link": {
                        "rel": "content",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/68ed1449-d420-44df-a0ed-57568a1c7904/signatures/0f9a8e29-8e55-4e4e-87ed-8d9b685fb585/content"
                    },
                    "links": [
                        {
                        "rel": "self",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/68ed1449-d420-44df-a0ed-57568a1c7904/signatures/0f9a8e29-8e55-4e4e-87ed-8d9b685fb585/content"
                        },
                        {
                        "rel": "docflow",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb"
                        }
                    ]
                    }
                ],
                "links": [
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb"
                    },
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/68ed1449-d420-44df-a0ed-57568a1c7904"
                    },
                    {
                    "rel": "reply",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/68ed1449-d420-44df-a0ed-57568a1c7904/generate-reply?documentType=fns534-report-receipt",
                    "name": "fns534-report-receipt"
                    },
                    {
                    "rel": "encrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/68ed1449-d420-44df-a0ed-57568a1c7904/encrypted-content"
                    },
                    {
                    "rel": "decrypt-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/68ed1449-d420-44df-a0ed-57568a1c7904/decrypt-content"
                    }
                ]
                },
                {
                "id": "bc36f712-32b5-41a3-a8f9-060618385b76",
                "description": {
                    "type": "urn:document:fns534-report-receipt",
                    "filename": "IZ_NOSRCHIS_7757424860_7757424860_0007_20200422_6bbfacb8f7b64520a433d74e709ae4ec.xml",
                    "content-type": "application/xml",
                    "decrypted-content-size": 4961,
                    "compressed": true,
                    "requisites": {},
                    "support-recognition": false,
                    "encrypted-certificates": []
                },
                "content": {
                    "decrypted": {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/bc36f712-32b5-41a3-a8f9-060618385b76/decrypted-content"
                    },
                    "docflow-document-contents": [
                    {
                        "content-id": "7b5ee74a-7a84-4d08-8a3f-a338e301fed2",
                        "encrypted": false,
                        "compressed": true
                    }
                    ]
                },
                "send-date": "2020-04-22T14:16:43.1767308Z",
                "signatures": [
                    {
                    "id": "373d7891-b0ae-4cdd-9ba8-6ee583889cc0",
                    "title": "Корионов  Илья Валерьянович",
                    "signature-certificate-thumbprint": "344AAD7111FC77ADE2A98FFB5E35F039BC4DD650",
                    "content-link": {
                        "rel": "content",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/bc36f712-32b5-41a3-a8f9-060618385b76/signatures/373d7891-b0ae-4cdd-9ba8-6ee583889cc0/content"
                    },
                    "links": [
                        {
                        "rel": "self",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/bc36f712-32b5-41a3-a8f9-060618385b76/signatures/373d7891-b0ae-4cdd-9ba8-6ee583889cc0/content"
                        },
                        {
                        "rel": "docflow",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb"
                        }
                    ]
                    }
                ],
                "links": [
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb"
                    },
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/bc36f712-32b5-41a3-a8f9-060618385b76"
                    },
                    {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/bc36f712-32b5-41a3-a8f9-060618385b76/decrypted-content"
                    }
                ]
                },
                {
                "id": "111f7485-7e2d-4c81-8017-9edc61835684",
                "description": {
                    "type": "urn:document:fns534-report",
                    "filename": "NO_SRCHIS_0007_0007_7757424860680345565_20200129_92425a70-4ac9-4680-bada-3666f0c0514v.xml",
                    "content-type": "application/xml",
                    "decrypted-content-size": 2233,
                    "encrypted-content-size": 2233,
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
                    "decrypted": {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/111f7485-7e2d-4c81-8017-9edc61835684/decrypted-content"
                    },
                    "encrypted": {
                    "rel": "encrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/111f7485-7e2d-4c81-8017-9edc61835684/encrypted-content"
                    },
                    "docflow-document-contents": [
                    {
                        "content-id": "2e1a8085-875a-471c-881e-9600f6ac96ef",
                        "encrypted": true,
                        "compressed": true
                    },
                    {
                        "content-id": "c670c7ab-0849-4536-a7b5-0594ea76212a",
                        "encrypted": false,
                        "compressed": false
                    }
                    ]
                },
                "send-date": "2020-04-22T14:16:36.1338472Z",
                "signatures": [
                    {
                    "id": "920a7f48-9acd-4582-841a-e21df444e06d",
                    "title": "ООО 'Баланс Плюс' (Марков Георгий Эльдарович)",
                    "signature-certificate-thumbprint": "20AACA440F33D0C90FBC052108012D3062D44873",
                    "content-link": {
                        "rel": "content",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/111f7485-7e2d-4c81-8017-9edc61835684/signatures/920a7f48-9acd-4582-841a-e21df444e06d/content"
                    },
                    "links": [
                        {
                        "rel": "self",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/111f7485-7e2d-4c81-8017-9edc61835684/signatures/920a7f48-9acd-4582-841a-e21df444e06d/content"
                        },
                        {
                        "rel": "docflow",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb"
                        }
                    ]
                    },
                    {
                    "id": "0017673e-b8a1-412c-9698-5d2d01a25af9",
                    "title": "Корионов  Илья Валерьянович",
                    "signature-certificate-thumbprint": "344AAD7111FC77ADE2A98FFB5E35F039BC4DD650",
                    "content-link": {
                        "rel": "content",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/111f7485-7e2d-4c81-8017-9edc61835684/signatures/0017673e-b8a1-412c-9698-5d2d01a25af9/content"
                    },
                    "links": [
                        {
                        "rel": "self",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/111f7485-7e2d-4c81-8017-9edc61835684/signatures/0017673e-b8a1-412c-9698-5d2d01a25af9/content"
                        },
                        {
                        "rel": "docflow",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb"
                        }
                    ]
                    }
                ],
                "links": [
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb"
                    },
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/111f7485-7e2d-4c81-8017-9edc61835684"
                    },
                    {
                    "rel": "related-docflow",
                    "href": "https://extern-api.testkontur.ru//v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/111f7485-7e2d-4c81-8017-9edc61835684/related"
                    },
                    {
                    "rel": "encrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/111f7485-7e2d-4c81-8017-9edc61835684/encrypted-content"
                    },
                    {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/111f7485-7e2d-4c81-8017-9edc61835684/decrypted-content"
                    },
                    {
                    "rel": "decrypt-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/111f7485-7e2d-4c81-8017-9edc61835684/decrypt-content"
                    }
                ]
                },
                {
                "id": "6076f7bc-a016-4d22-bb63-221df6582906",
                "description": {
                    "type": "urn:document:fns534-report-date-confirmation",
                    "filename": "PD_NOSRCHIS_7757424860680345565_7757424860680345565_1BM_20200422_b4885f2a-dddb-4484-89f3-e83dc94ea83d.xml",
                    "content-type": "application/xml",
                    "decrypted-content-size": 3023,
                    "compressed": true,
                    "requisites": {},
                    "support-recognition": false,
                    "encrypted-certificates": []
                },
                "content": {
                    "decrypted": {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/6076f7bc-a016-4d22-bb63-221df6582906/decrypted-content"
                    },
                    "docflow-document-contents": [
                    {
                        "content-id": "c5227d5f-7b80-41a3-91a1-34136a99171c",
                        "encrypted": false,
                        "compressed": true
                    }
                    ]
                },
                "send-date": "2020-04-22T14:16:36.1338472Z",
                "signatures": [
                    {
                    "id": "7117bfa4-60b6-4652-942d-7bafe10c476a",
                    "title": "АО \"ПФ \"СКБ Контур\"",
                    "signature-certificate-thumbprint": "ADBB03393A5C3F5402A8EFF8F7AAE859076079F8",
                    "content-link": {
                        "rel": "content",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/6076f7bc-a016-4d22-bb63-221df6582906/signatures/7117bfa4-60b6-4652-942d-7bafe10c476a/content"
                    },
                    "links": [
                        {
                        "rel": "self",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/6076f7bc-a016-4d22-bb63-221df6582906/signatures/7117bfa4-60b6-4652-942d-7bafe10c476a/content"
                        },
                        {
                        "rel": "docflow",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb"
                        }
                    ]
                    }
                ],
                "links": [
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb"
                    },
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/6076f7bc-a016-4d22-bb63-221df6582906"
                    },
                    {
                    "rel": "reply",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/6076f7bc-a016-4d22-bb63-221df6582906/generate-reply?documentType=fns534-report-receipt",
                    "name": "fns534-report-receipt"
                    },
                    {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/6076f7bc-a016-4d22-bb63-221df6582906/decrypted-content"
                    }
                ]
                },
                {
                "id": "79e6d1db-fbe6-4b00-a447-cc9eb1a90571",
                "description": {
                    "type": "urn:document:fns534-report-description",
                    "filename": "TR_DEKL.xml",
                    "content-type": "application/xml",
                    "decrypted-content-size": 364,
                    "compressed": true,
                    "requisites": {},
                    "support-recognition": false,
                    "encrypted-certificates": []
                },
                "content": {
                    "decrypted": {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/79e6d1db-fbe6-4b00-a447-cc9eb1a90571/decrypted-content"
                    },
                    "docflow-document-contents": [
                    {
                        "content-id": "ad34e8ab-4518-47e8-b578-b26adc728d1f",
                        "encrypted": false,
                        "compressed": true
                    }
                    ]
                },
                "send-date": "2020-04-22T14:16:36.1338472Z",
                "signatures": [],
                "links": [
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb"
                    },
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/79e6d1db-fbe6-4b00-a447-cc9eb1a90571"
                    },
                    {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/79e6d1db-fbe6-4b00-a447-cc9eb1a90571/decrypted-content"
                    }
                ]
                }
            ],
            "links": [
                {
                "rel": "self",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb"
                },
                {
                "rel": "organization",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/organizations/988b38f1-5580-4ba9-b9f8-3215e7f392ea"
                },
                {
                "rel": "web-docflow",
                "href": "https://setter.testkontur.ru/?inn=662909960905&forward_to_rel=/ft/transmission/state.aspx?key=cfOOHYSO4USxIIRIMEKAL%2fE4i5iAValLufgyFefzkuqKJpsKOwY6TorTSpphojA7tVBODKxmkkqwUTvJVHLd2w%3d%3d"
                },
                {
                "rel": "reply",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/09da96fe-a21a-4f69-84db-ff9d82c86bde/generate-reply?documentType=fns534-report-receipt",
                "name": "fns534-report-receipt"
                },
                {
                "rel": "reply",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/68ed1449-d420-44df-a0ed-57568a1c7904/generate-reply?documentType=fns534-report-receipt",
                "name": "fns534-report-receipt"
                },
                {
                "rel": "reply",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/6076f7bc-a016-4d22-bb63-221df6582906/generate-reply?documentType=fns534-report-receipt",
                "name": "fns534-report-receipt"
                }
            ],
            "send-date": "2020-04-22T17:16:36.1338472",
            "last-change-date": "2020-04-22T14:17:13.8960679Z"
        }

Сверим полученный в ответе статус документооборота со :ref:`схемой смены статусов для документооборота типа декларация<rst-markup-fnsreport-status>`. В данном случае статус "urn:docflow-common-status:response-arrived". Он означает, что в документообороте уже появилось извещение о получении от налогового органа (или робота на тестовой площадке), а также результаты приема и обработки. Эти документы можно посмотреть в списке документов документооборота, сохранить и напечатать. 

Получение входящих документов от контролирующего органа
-------------------------------------------------------

В нашем документообороте есть три новых документа, у которых в description указаны следующие типы: 

* urn:document:fns534-report-receipt
* urn:document:fns534-report-processing-result-ok
* urn:document:fns534-report-acceptance-result-positive

Это и есть извещение о получении, квитанция о приеме, извещение о вводе. Мы можем их скачать и напечатать. Если на момент проверки статуса документооборота в нем еще не появились результаты обработки, значит нужно отправить ответные документы к подтверждению даты отправки, квитанции о приеме и заново запрашивать статус документооборота. 

Все документы, которые появляются в документообороте, автоматически загружаются в :doc:`сервис контентов</knowledge base/content>`. Идентификатор контента можно посмотреть в информации о документе, в параметре content-id. По этому идентификатору можно скачать документ в сервисе контентов.

Контролирующий орган присылает документы зашифрованными и сжатыми. Для получения документа в расшифрованном и разжатом виде нужно выполнить следующий алгоритм.

Алгоритм получения документа из зашифрованного контента
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Получаем зашифрованный контент файла: скачиваем напрямую или через сервис контентов.
2. Если документ в формате base64, декодируем файл.
3. В метаинформации о документе в параметре encrypted-certificates перечислены сертификаты, на которые контролирующий орган зашифровал отправленный документ. Расшифровываем документ одним из сертификатов.
4. Смотрим в description документа поле compressed, в котором указано, сжат ли зашифрованный файл. 
5. Распаковываем архив, получаем файл.

**Пример получения зашифрованного контента**

Выполним запрос получения документа в документообороте методом `GET Document`_. В ответе необходимо посмотреть значения полей в параметре docflow-document-contents: content-id - идентификатор, по которому можно скачать контент в сервисе контентов, encrypted - признак зашифрованного контента, compressed - признак сжатого контента.

**Запрос GET Download**

.. code-block:: http

    GET /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/contents/d065adea-8b9d-4228-bc17-8f86539e01a3 HTTP/1.1
    Authorization: Bearer <token>
    Content-Type: application/octet-stream

**Ответ**

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/octet-stream
    Content-Length: 727

    "0�*�H����0�1�0��0�0��..."

В ответе мы получили строку с контентом в формате base64. Далее по алгоритму: декодируем файл, расшифровываем его, распаковываем архив. Таким образом, получим файл документа, который сформировал контролирующий орган в ответ на отправленный отчет. Чтобы напечатать файл, :doc:`воспользуйтесь методом Print</knowledge base/print>`. 

Далее нужно сформировать ответные документы согласно порядку работы с документооборотом. 

Формирование ответных документов
--------------------------------

Статус полученного документооборота — "ответ обработан" (urn:docflow-common-status:response-arrived). Значит в документообороте уже сформированы ссылки с типом "rel": "reply". В нашем примере их три, значит нужно сформировать и отправить три ответных документа. Ответным документом является технологический документ "Извещение о получении". Для работы с ответными документами в swagger есть `специальный раздел методов`_. Будьте внимательны, часть методов разработана только для ответных документов в ПФР, они нам пока не нужны.

Порядок работы с ответным документом
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Формирование ответного документа похоже на создание черновика. Но все данные уже есть, API самостоятельно сгенерирует файл ответного документа:

1. Создаем ответный документ (можно по ссылке типа reply) методом `POST CreateReplyDocument`_. В ответе метод вернет печатную форму и контент ответного документа в формате base64.
2. Сформировать к ответному документу подпись. После формирования файла приложить подпись методом `PUT SaveReplyDocumentSignature`_.
3. Отправляем ответный документ `POST SendReplyDocument`_.

Создание ответного документа
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Метод позволяет сгенерировать xml-файл документа установленного формата и печатную форму извещения о получении, в теле запроса передаем контент сертификата подписанта. Контент возвращается в формате base64, он не зашифрован и не сжат. Нужно конвертировать полученный контент в xml файл, подписать его и приложить подпись к файлу. 

**Пример запроса POST CreateReplyDocument**

.. code-block:: http

    POST /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/generate-reply?documentType=fns534-report-receipt HTTP/1.1
    X-Kontur-Apikey: ****
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json

    {
        "certificate-base64": "MIIJcDCCCR2gAwI...NRsAZ8sYpQYKykqopO+/MYE3Xk="
    }

.. container:: toggle

    .. container:: header

        **Пример ответа POST CreateReplyDocument**

    .. code-block:: http

        {
            "id": "9ae00ec3-9b23-48d7-a417-368e24f1c6ca",
            "content": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0id2luZG93cy0xMjUxIj8...zl7fI+DQo8L9Tg6es+",
            "print-content": "JVBERi0xLjQKJdPr6eEKMSAwIG...mVmCjU3Njk0CiUlRU9G",
            "filename": "IZ_IVNOSRCHIS_0007_0007_7757424860680345565_20200421_e6abd9111944426e9956138cbfe16bfc.xml",
            "links": [
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/replies/9ae00ec3-9b23-48d7-a417-368e24f1c6ca"
                    },
                    {
                    "rel": "save-signature",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/replies/9ae00ec3-9b23-48d7-a417-368e24f1c6ca/signature"
                    },
                    {
                    "rel": "send",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/replies/9ae00ec3-9b23-48d7-a417-368e24f1c6ca/send"
                    },
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                    },
                    {
                    "rel": "content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/replies/9ae00ec3-9b23-48d7-a417-368e24f1c6ca/content"
                    }
                ],
            "docflow-id": "7b9edebc-32bc-4317-b4a4-abbc26fe3663",
            "document-id": "70c3746a-28c0-441c-ad5d-cb585cf5ed22"
        }


Подписание документа
~~~~~~~~~~~~~~~~~~~~

Для формирования файла подписи нужно скачать полученный xml-файл. Для этого строку из поля content декодируем из base64 в файл ответного документа. В примере используем обычный сертификат, поэтому файл подписи получили локально. Теперь его нужно приложить к ответному документу методом `PUT SaveReplyDocumentSignature`_.

В теле данного метода необходимо передать сам файл подписи, его не нужно конвертировать в base64. 

**Пример запроса PUT SaveReplyDocumentSignature**

.. code-block:: http

    PUT /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/replies/9ae00ec3-9b23-48d7-a417-368e24f1c6ca/signature HTTP/1.1
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/pgp-signature
    X-Kontur-Apikey: ****
    Host: extern-api.testkontur.ru
    Content-Length: 3353

    "<file contents here>"

.. container:: toggle

    .. container:: header

        **Пример ответа PUT SaveReplyDocumentSignature**

    .. code-block:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=utf-8
        Content-Encoding: gzip

        {
            "id": "9ae00ec3-9b23-48d7-a417-368e24f1c6ca",
            "content": "PD94bWwgdmV...9Tg6es+",
            "print-content": "JVBERi0xLjQKJdPr6e...jk0CiUlRU9G",
            "filename": "IZ_IVNOSRCHIS_0007_0007_7757424860680345565_20200421_e6abd9111944426e9956138cbfe16bfc.xml",
            "signature": "MIINFQYJK...a5U8yWyng=",
            "links": [
                {
                "rel": "self",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/replies/9ae00ec3-9b23-48d7-a417-368e24f1c6ca"
                },
                {
                "rel": "save-signature",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/replies/9ae00ec3-9b23-48d7-a417-368e24f1c6ca/signature"
                },
                {
                "rel": "send",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/replies/9ae00ec3-9b23-48d7-a417-368e24f1c6ca/send"
                },
                {
                "rel": "docflow",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                },
                {
                "rel": "content",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/replies/9ae00ec3-9b23-48d7-a417-368e24f1c6ca/content"
                }
            ],
            "docflow-id": "7b9edebc-32bc-4317-b4a4-abbc26fe3663",
            "document-id": "70c3746a-28c0-441c-ad5d-cb585cf5ed22"
        }

Отправка ответного документа
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Пример запроса POST SendReplyDocument**

.. code-block:: http

    POST /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/replies/9ae00ec3-9b23-48d7-a417-368e24f1c6ca/send HTTP/1.1
    Host: extern-api.testkontur.ru
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json
    X-Kontur-Apikey: ****

    {
        "sender-ip": "8.8.8.8"
    }

.. container:: toggle

    .. container:: header

        **Пример ответа POST SendReplyDocument**

    .. code-block:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=utf-8
        
        {
            "id": "7b9edebc-32bc-4317-b4a4-abbc26fe3663",
            "organization-id": "988b38f1-5580-4ba9-b9f8-3215e7f392ea",
            "type": "urn:docflow:fns534-report",
            "status": "urn:docflow-common-status:finished",
            "success-state": "urn:docflow-state:successful",
            "description": {
                "form-version": {
                "knd": "1110018",
                "version": "100501",
                "form-fullname": "Сведения о среднесписочной численности работников за предшествующий календарный год",
                "form-shortname": "Сведения о среднесписочной численности"
                },
                "recipient": "0007",
                "final-recipient": "0007",
                "correction-number": 0,
                "period-begin": "2018-01-01T00:00:00.0000000",
                "period-end": "2018-12-31T00:00:00.0000000",
                "period-code": "34",
                "payer-inn": "7757424860-680345565",
                "original-draft-id": "7b273c79-e814-424f-a81f-6c4b6f791f85"
            },
            "documents": [
                {
                "id": "9ae00ec3-9b23-48d7-a417-368e24f1c6ca",
                "description": {
                    "type": "urn:document:fns534-report-receipt",
                    "filename": "IZ_IVNOSRCHIS_0007_0007_7757424860680345565_20200421_e6abd9111944426e9956138cbfe16bfc.xml",
                    "content-type": "application/xml",
                    "decrypted-content-size": 2735,
                    "compressed": true,
                    "requisites": {},
                    "support-recognition": false,
                    "encrypted-certificates": []
                },
                "content": {
                    "decrypted": {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/9ae00ec3-9b23-48d7-a417-368e24f1c6ca/decrypted-content"
                    },
                    "docflow-document-contents": [
                    {
                        "content-id": "943e7222-1355-4e71-b095-00a793853bfd",
                        "encrypted": false,
                        "compressed": true
                    }
                    ]
                },
                "send-date": "2020-04-22T08:48:32.0342794Z",
                "signatures": [
                    {
                    "id": "f69b4263-705c-4ad4-a4ee-3c78649798d0",
                    "title": "ООО 'Баланс Плюс' (Марков Георгий Эльдарович)",
                    "signature-certificate-thumbprint": "20AACA440F33D0C90FBC052108012D3062D44873",
                    "content-link": {
                        "rel": "content",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/9ae00ec3-9b23-48d7-a417-368e24f1c6ca/signatures/f69b4263-705c-4ad4-a4ee-3c78649798d0/content"
                    },
                    "links": [
                        {
                        "rel": "self",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/9ae00ec3-9b23-48d7-a417-368e24f1c6ca/signatures/f69b4263-705c-4ad4-a4ee-3c78649798d0/content"
                        },
                        {
                        "rel": "docflow",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                        }
                    ]
                    }
                ],
                "links": [
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                    },
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/9ae00ec3-9b23-48d7-a417-368e24f1c6ca"
                    },
                    {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/9ae00ec3-9b23-48d7-a417-368e24f1c6ca/decrypted-content"
                    }
                ]
                },
                {
                "id": "70c3746a-28c0-441c-ad5d-cb585cf5ed22",
                "description": {
                    "type": "urn:document:fns534-report-processing-result-ok",
                    "filename": "IV_NOSRCHIS_7757424860_7757424860_0007_20200421_d2d2b19bef984e5a821b1cd1c7bbffd4.xml",
                    "content-type": "application/xml",
                    "encrypted-content-size": 1642,
                    "compressed": true,
                    "requisites": {},
                    "support-recognition": false,
                    "encrypted-certificates": [
                    {
                        "serial-number": "01D0850043AB3C924A605B8D8661E43E"
                    }
                    ]
                },
                "content": {
                    "encrypted": {
                    "rel": "encrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/encrypted-content"
                    },
                    "docflow-document-contents": [
                    {
                        "content-id": "4cf756aa-496d-4afc-8b93-7fa4477bed19",
                        "encrypted": true,
                        "compressed": true
                    }
                    ]
                },
                "send-date": "2020-04-21T16:17:24.5827069Z",
                "signatures": [
                    {
                    "id": "aa81d013-c99b-4e71-8deb-67f0beca6c91",
                    "title": "Корионов  Илья Валерьянович",
                    "signature-certificate-thumbprint": "344AAD7111FC77ADE2A98FFB5E35F039BC4DD650",
                    "content-link": {
                        "rel": "content",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/signatures/aa81d013-c99b-4e71-8deb-67f0beca6c91/content"
                    },
                    "links": [
                        {
                        "rel": "self",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/signatures/aa81d013-c99b-4e71-8deb-67f0beca6c91/content"
                        },
                        {
                        "rel": "docflow",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                        }
                    ]
                    }
                ],
                "links": [
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                    },
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22"
                    },
                    {
                    "rel": "encrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/encrypted-content"
                    },
                    {
                    "rel": "decrypt-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/70c3746a-28c0-441c-ad5d-cb585cf5ed22/decrypt-content"
                    }
                ]
                },
                {
                "id": "ad5d5d21-59c2-4365-8b2b-16734f05fb5c",
                "description": {
                    "type": "urn:document:fns534-report-acceptance-result-positive",
                    "filename": "KV_NOSRCHIS_7757424860_7757424860_0007_20200421_373b5c60ba2847a38787e6ab12a881d5.xml",
                    "content-type": "application/xml",
                    "encrypted-content-size": 1809,
                    "compressed": true,
                    "requisites": {},
                    "support-recognition": false,
                    "encrypted-certificates": [
                    {
                        "serial-number": "01D0850043AB3C924A605B8D8661E43E"
                    }
                    ]
                },
                "content": {
                    "encrypted": {
                    "rel": "encrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/ad5d5d21-59c2-4365-8b2b-16734f05fb5c/encrypted-content"
                    },
                    "docflow-document-contents": [
                    {
                        "content-id": "716693b7-68f8-40dd-bdee-17b301f12f0f",
                        "encrypted": true,
                        "compressed": true
                    }
                    ]
                },
                "send-date": "2020-04-21T16:17:24.3326778Z",
                "signatures": [
                    {
                    "id": "3018cdbd-b400-43d3-8d7f-a7970fcbeb5b",
                    "title": "Корионов  Илья Валерьянович",
                    "signature-certificate-thumbprint": "344AAD7111FC77ADE2A98FFB5E35F039BC4DD650",
                    "content-link": {
                        "rel": "content",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/ad5d5d21-59c2-4365-8b2b-16734f05fb5c/signatures/3018cdbd-b400-43d3-8d7f-a7970fcbeb5b/content"
                    },
                    "links": [
                        {
                        "rel": "self",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/ad5d5d21-59c2-4365-8b2b-16734f05fb5c/signatures/3018cdbd-b400-43d3-8d7f-a7970fcbeb5b/content"
                        },
                        {
                        "rel": "docflow",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                        }
                    ]
                    }
                ],
                "links": [
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                    },
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/ad5d5d21-59c2-4365-8b2b-16734f05fb5c"
                    },
                    {
                    "rel": "reply",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/ad5d5d21-59c2-4365-8b2b-16734f05fb5c/generate-reply?documentType=fns534-report-receipt",
                    "name": "fns534-report-receipt"
                    },
                    {
                    "rel": "encrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/ad5d5d21-59c2-4365-8b2b-16734f05fb5c/encrypted-content"
                    },
                    {
                    "rel": "decrypt-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/ad5d5d21-59c2-4365-8b2b-16734f05fb5c/decrypt-content"
                    }
                ]
                },
                {
                "id": "de2402a0-f68c-4b60-9a92-b39b53f49536",
                "description": {
                    "type": "urn:document:fns534-report-receipt",
                    "filename": "IZ_NOSRCHIS_7757424860_7757424860_0007_20200421_55abc6b7229b419481615c202a5f932d.xml",
                    "content-type": "application/xml",
                    "decrypted-content-size": 4961,
                    "compressed": true,
                    "requisites": {},
                    "support-recognition": false,
                    "encrypted-certificates": []
                },
                "content": {
                    "decrypted": {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/de2402a0-f68c-4b60-9a92-b39b53f49536/decrypted-content"
                    },
                    "docflow-document-contents": [
                    {
                        "content-id": "1d702ada-de98-4f05-a00e-798c78f22d37",
                        "encrypted": false,
                        "compressed": true
                    }
                    ]
                },
                "send-date": "2020-04-21T16:17:08.6973832Z",
                "signatures": [
                    {
                    "id": "5c01eb0b-f3b9-440e-b9f3-013aed1a2cfc",
                    "title": "Корионов  Илья Валерьянович",
                    "signature-certificate-thumbprint": "344AAD7111FC77ADE2A98FFB5E35F039BC4DD650",
                    "content-link": {
                        "rel": "content",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/de2402a0-f68c-4b60-9a92-b39b53f49536/signatures/5c01eb0b-f3b9-440e-b9f3-013aed1a2cfc/content"
                    },
                    "links": [
                        {
                        "rel": "self",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/de2402a0-f68c-4b60-9a92-b39b53f49536/signatures/5c01eb0b-f3b9-440e-b9f3-013aed1a2cfc/content"
                        },
                        {
                        "rel": "docflow",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                        }
                    ]
                    }
                ],
                "links": [
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                    },
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/de2402a0-f68c-4b60-9a92-b39b53f49536"
                    },
                    {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/de2402a0-f68c-4b60-9a92-b39b53f49536/decrypted-content"
                    }
                ]
                },
                {
                "id": "eb312e60-6b26-425c-9917-3b8d2bd59fd0",
                "description": {
                    "type": "urn:document:fns534-report",
                    "filename": "NO_SRCHIS_0007_0007_7757424860680345565_20200129_92425a70-4ac9-4680-bada-3666f0c0514f.xml",
                    "content-type": "application/xml",
                    "decrypted-content-size": 2233,
                    "encrypted-content-size": 2233,
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
                    "decrypted": {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/eb312e60-6b26-425c-9917-3b8d2bd59fd0/decrypted-content"
                    },
                    "encrypted": {
                    "rel": "encrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/eb312e60-6b26-425c-9917-3b8d2bd59fd0/encrypted-content"
                    },
                    "docflow-document-contents": [
                    {
                        "content-id": "90ccb811-7a1d-4eaf-8f3e-4a4913167fd8",
                        "encrypted": true,
                        "compressed": true
                    },
                    {
                        "content-id": "f9fc3787-14b5-4d14-aa49-033397c7aa3b",
                        "encrypted": false,
                        "compressed": false
                    }
                    ]
                },
                "send-date": "2020-04-21T16:16:53.1173657Z",
                "signatures": [
                    {
                    "id": "88f38975-9b68-4983-b1f9-a3d32c75d84e",
                    "title": "ООО 'Баланс Плюс' (Марков Георгий Эльдарович)",
                    "signature-certificate-thumbprint": "20AACA440F33D0C90FBC052108012D3062D44873",
                    "content-link": {
                        "rel": "content",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/eb312e60-6b26-425c-9917-3b8d2bd59fd0/signatures/88f38975-9b68-4983-b1f9-a3d32c75d84e/content"
                    },
                    "links": [
                        {
                        "rel": "self",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/eb312e60-6b26-425c-9917-3b8d2bd59fd0/signatures/88f38975-9b68-4983-b1f9-a3d32c75d84e/content"
                        },
                        {
                        "rel": "docflow",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                        }
                    ]
                    },
                    {
                    "id": "493018fa-119d-4aa8-9973-b105742907c3",
                    "title": "Корионов  Илья Валерьянович",
                    "signature-certificate-thumbprint": "344AAD7111FC77ADE2A98FFB5E35F039BC4DD650",
                    "content-link": {
                        "rel": "content",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/eb312e60-6b26-425c-9917-3b8d2bd59fd0/signatures/493018fa-119d-4aa8-9973-b105742907c3/content"
                    },
                    "links": [
                        {
                        "rel": "self",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/eb312e60-6b26-425c-9917-3b8d2bd59fd0/signatures/493018fa-119d-4aa8-9973-b105742907c3/content"
                        },
                        {
                        "rel": "docflow",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                        }
                    ]
                    }
                ],
                "links": [
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                    },
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/eb312e60-6b26-425c-9917-3b8d2bd59fd0"
                    },
                    {
                    "rel": "related-docflow",
                    "href": "https://extern-api.testkontur.ru//v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/eb312e60-6b26-425c-9917-3b8d2bd59fd0/related"
                    },
                    {
                    "rel": "encrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/eb312e60-6b26-425c-9917-3b8d2bd59fd0/encrypted-content"
                    },
                    {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/eb312e60-6b26-425c-9917-3b8d2bd59fd0/decrypted-content"
                    },
                    {
                    "rel": "decrypt-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/eb312e60-6b26-425c-9917-3b8d2bd59fd0/decrypt-content"
                    }
                ]
                },
                {
                "id": "18b6bbc4-ae15-47cb-8ef9-7b5256501845",
                "description": {
                    "type": "urn:document:fns534-report-date-confirmation",
                    "filename": "PD_NOSRCHIS_7757424860680345565_7757424860680345565_1BM_20200421_c0836c44-7a08-41bf-96c1-f8a94f674b2e.xml",
                    "content-type": "application/xml",
                    "decrypted-content-size": 3019,
                    "compressed": true,
                    "requisites": {},
                    "support-recognition": false,
                    "encrypted-certificates": []
                },
                "content": {
                    "decrypted": {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/18b6bbc4-ae15-47cb-8ef9-7b5256501845/decrypted-content"
                    },
                    "docflow-document-contents": [
                    {
                        "content-id": "de76f58b-c24a-4b6d-b6de-0d801f32bdde",
                        "encrypted": false,
                        "compressed": true
                    }
                    ]
                },
                "send-date": "2020-04-21T16:16:53.1173657Z",
                "signatures": [
                    {
                    "id": "0f0b7caf-6d0a-444e-a119-0f65c7b1ffa7",
                    "title": "АО \"ПФ \"СКБ Контур\"",
                    "signature-certificate-thumbprint": "ADBB03393A5C3F5402A8EFF8F7AAE859076079F8",
                    "content-link": {
                        "rel": "content",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/18b6bbc4-ae15-47cb-8ef9-7b5256501845/signatures/0f0b7caf-6d0a-444e-a119-0f65c7b1ffa7/content"
                    },
                    "links": [
                        {
                        "rel": "self",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/18b6bbc4-ae15-47cb-8ef9-7b5256501845/signatures/0f0b7caf-6d0a-444e-a119-0f65c7b1ffa7/content"
                        },
                        {
                        "rel": "docflow",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                        }
                    ]
                    }
                ],
                "links": [
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                    },
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/18b6bbc4-ae15-47cb-8ef9-7b5256501845"
                    },
                    {
                    "rel": "reply",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/18b6bbc4-ae15-47cb-8ef9-7b5256501845/generate-reply?documentType=fns534-report-receipt",
                    "name": "fns534-report-receipt"
                    },
                    {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/18b6bbc4-ae15-47cb-8ef9-7b5256501845/decrypted-content"
                    }
                ]
                },
                {
                "id": "db37a722-de69-4413-992d-216bd1088926",
                "description": {
                    "type": "urn:document:fns534-report-description",
                    "filename": "TR_DEKL.xml",
                    "content-type": "application/xml",
                    "decrypted-content-size": 364,
                    "compressed": true,
                    "requisites": {},
                    "support-recognition": false,
                    "encrypted-certificates": []
                },
                "content": {
                    "decrypted": {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/db37a722-de69-4413-992d-216bd1088926/decrypted-content"
                    },
                    "docflow-document-contents": [
                    {
                        "content-id": "1d9bc226-5b16-4b8e-8cb6-34960230ef51",
                        "encrypted": false,
                        "compressed": true
                    }
                    ]
                },
                "send-date": "2020-04-21T16:16:53.1173657Z",
                "signatures": [],
                "links": [
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                    },
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/db37a722-de69-4413-992d-216bd1088926"
                    },
                    {
                    "rel": "decrypted-content",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/db37a722-de69-4413-992d-216bd1088926/decrypted-content"
                    }
                ]
                }
            ],
            "links": [
                {
                "rel": "self",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663"
                },
                {
                "rel": "organization",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/organizations/988b38f1-5580-4ba9-b9f8-3215e7f392ea"
                },
                {
                "rel": "web-docflow",
                "href": "https://setter.testkontur.ru/?inn=662909960905&forward_to_rel=/ft/transmission/state.aspx?key=cfOOHYSO4USxIIRIMEKAL%2fE4i5iAValLufgyFefzkuqKJpsKOwY6TorTSpphojA7vN6ee7wyF0O0pKu8Jv42Yw%3d%3d"
                },
                {
                "rel": "reply",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/ad5d5d21-59c2-4365-8b2b-16734f05fb5c/generate-reply?documentType=fns534-report-receipt",
                "name": "fns534-report-receipt"
                },
                {
                "rel": "reply",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/7b9edebc-32bc-4317-b4a4-abbc26fe3663/documents/18b6bbc4-ae15-47cb-8ef9-7b5256501845/generate-reply?documentType=fns534-report-receipt",
                "name": "fns534-report-receipt"
                }
            ],
            "send-date": "2020-04-21T19:16:53.1173657",
            "last-change-date": "2020-04-22T08:48:32.0342794Z"
            }

После отправки ответного документа в ответе метода SendReplyDocument возвращается модель документооборота. В данном примере "Извещение о получении" было отправлено к документу "Извещение о вводе". Согласно схеме смены статусов документооборота, после отправки ответного документа к "Извещению о вводе" документооборот завершается. В примере можно увидеть, что появился новый документ типа urn:document:fns534-report-receipt — Извещение о получении, а также после отправки этого документа сменился статус документооборота на "urn:docflow-common-status:finished".