.. _`ГОСТу 34.12-2018`: https://normativ.kontur.ru/document?moduleId=9&documentId=388001
.. _`ГОСТу 34.13-2018`: https://normativ.kontur.ru/document?moduleId=9&documentId=383534 
.. _`Контур.Диагностика`: https://help.kontur.ru/

.. _rst-markup-get_report:

Получение входящих и отправка ответных документов в ФНС
=======================================================

После того, как черновик отчета был отправлен, нужно дождаться входящих документов от ФНС и отправить на них ответные документы. Таким образом, работа с документооборотом состоит из следующих шагов:

1. :ref:`Мониторинг статуса документооборота в порядке взаимодействия с ФНС<rst-markup=get_report_poryadok>`.
2. :ref:`Получение входящих документов<rst-markup=get_report_vhdoc>`.
3. :ref:`Формирование ответных документов<rst-markup=get_report_otvet>`. 

Статус документооборота зависит от того, какие документы поступят или будут отправлены. Рассмотрим подробнее процесс смены статусов для типа ДО urn:docflow:fns534-report при получении или отправке документов.

.. _rst-markup=get_report_poryadok:

Порядок взаимодействия
----------------------

1. После отправки черновика с отчетом статус документооборота поменяется на **Отправлен** (urn:docflow-common-status:sent) и поступит документ **Подтверждение даты отправки** (urn:document:fns-534-report-date-confirmation). Документ формирует оператор ЭДО и в нем указаны данные о дате и времени отправки отчета.

2. В течение 4 часов после отправки черновика от ФНС поступит один из документов:

    * **Извещение о получении** (urn:document:fns534-report-receipt). Статус документооборота поменяется на **Доставлен** (urn:docflow-common-status:delivered). Это означает, что отчет поступил в приемный комплекс ФНС и принят в работу.
    * **Сообщение об ошибке** (urn:document:error). Статус документооборота поменяется на **Завершен** (urn:docflow-common-status:finished). Это означает, что отчет не принят. Нужно исправить ошибки, указанные в сообщении, и отправить отчет снова.

Отправлять ответные документы не нужно.

3. После от ФНС поступит один из документов:

    * **Квитанция о приеме** (urn:document:fns534-report-acceptance-result-positive). Поступит в течение одного рабочего дня после отправки черновика. Статус документооборота поменяется на **Получен ответ** (urn:docflow-common-status:response-arrived). Документ подтверждает факт приема отчета. Далее необходимо дождаться результатов ввода данных в базу налогового органа.
    * **Уведомление об отказе** (urn:document:fns534-report-acceptance-result-negative). Поступит в течение 6-12 часов после отправки черновика. Статус документооборота поменяется на **Завершен** (urn:docflow-common-status:finished). Это означает, что отчет не принят. Нужно исправить ошибки, указанные в уведомлении, и отправить отчет снова.

4. На поступившие документы нужно отправить в ответ документ **Извещение о получении** (urn:document:fns534-perort-receipt). Создать документ можно по ссылке ``reply`` из метаинформации документооборота. После отправки документа статус документооборота поменяется на **Ответ обработан** (urn:docflow-common-status:response-processed).  

5. В течение двух рабочих дней после поступления Квитанции о приеме от ФНС поступит один из документов:

* **Извещение о вводе** (urn:document:fns534-report-proccesing-result-ok). Статус документооборота поменяется на **Получен ответ** (urn:docflow-common-status:response-arrived). Это означает, что отчет принят и данные загружены в базу инспекции.
* **Уведомление об уточнении** (urn:document:fns534-report-processing-result-precise). Статус документооборота поменяется на **Получен ответ** (urn:docflow-common-status:response-arrived). Это означает, что отчет принят, но требует уточнений. Необходимо отправить корректирующий отчет, внеся необходимые уточнения.

6. На каждый поступивший документ нужно отправить в ответ документ **Извещение о получении** (urn:document:fns534-report-receipt). Создать документ можно по ссылке ``reply`` из метаинформации документооборота. Статус документооборота поменяется на **Завершен** (urn:docflow-common-status:finished). В работе с документооборотом больше не требуется каких-либо действий. 

В спецификации можно посмотреть :ref:`список всех документов<rst-markup-type_document>` и :ref:`процесс смены статусов<rst-markup-fnsreport-status>`.

На схеме мы показали порядок взаимодействия и очередность вызовов методов:

.. image:: /_static/get_report.png


Алгоритм проверки статуса документооборота
------------------------------------------

Есть два способа посмотреть текущий статус документооборота: 

1. Запросите документооборот по его идентификатору ``docflowId``: :ref:`GET Docflow<rst-markup-get-dc>`.

2. Если идентификатор ``docflowId`` был утерян или неизвестен, то запросите список всех документооборотов учетной записи: :ref:`GET Docflows<rst-markup-get-dcs>`. В запросе укажите фильтр ``type`` = urn:docflow:fns534-report. Метод вернет список всех существующих ДО, в модели ``docflows-page-item`` будет представлена краткая информация о ДО, в том числе и статус.  

Сверьте статус документооборота в параметре ``status`` со схемой смены статуса для ДО с типом urn:docflow:fns534-report.

.. _rst-markup=get_report_vhdoc:

Алгоритм получения входящих документов
--------------------------------------

1. Запросите документооборот по его идентификатору ``docflowId``: :ref:`GET Docflow<rst-markup-get-dc>`. Метод вернет модель ``documents``, в которой будут описаны все документы. Обратите внимание на следующие параметры в моделе ``docflow-document-contents``:

    * ``content-id`` — идентификатор входящего контента для скачивания его из Сервиса контентов.
    * ``encrypted`` — признак зашифрованного контента
    * ``encrypted-certificates`` — список сертификатов, на которые контролирующий орган зашифровал отправленный документ;
    * ``compressed`` — признак сжатости контента.

Каждый конкретный документ можно получить по его идентификатору ``documentId``: :ref:`GET Document<rst-markup-get-dc-document>`.

2. Скачайте контент документа из :ref:`Сервиса контентов<rst-markup-get-content>`.
3. Расшифруйте документ одним из сертификатов, если признак ``encrypted=true``.  
4. Разархивируйте документ, если признак ``compressed=true``.

.. important:: С июля 2024 года действует новый алгоритм расшифровки документов по `ГОСТу 34.12-2018`_ и `ГОСТу 34.13-2018`_ для документов ФНС. Для работы с новым алгоритмом обновите программное обеспечение для работы с электронными подписями до следующих версий:

    * КриптоПРО 5.0 R2;
    * Контур.Плагин 4.4;
    * Рутокен 3.0.
    
    Обновить программное обеспечение можно с помощью сервиса `Контур.Диагностика`_.

.. _rst-markup=get_report_otvet:

Алгоритм создания и отправки ответных документов
------------------------------------------------

1. Создайте ответный документ: :ref:`POST CreateReplyDocument<rst-markup-CreateReplyDocument>`. Документ можно также сформировать по ссылке с типом ``rel: reply`` из метаинформации документооборота. В запросе укажите параметры:

    * ``docflowId`` — идентификатор документооборота;
    * ``documentId`` — идентификатор документа, на который нужно отправить ответный документ;
    * ``documentType`` — тип ответного документа без указания “urn:document” . Для отчетов ФНС это ``documentType`` = fns534-report-receipt.

В ответ метод вернет печатную форму и контент ответного документа.

2. Скачайте контент документа из :ref:`Сервиса контентов<rst-markup-get-content>`.
3. Подпишите полученный xml файл закрытой частью электронной подписи.
4. Сформируйте к ответному документу подпись и приложите ее: :ref:`PUT ReplyDocumentSignature<rst-markup-repliSignature>`.
5. Отправьте ответный документ: :ref:`POST SendReplyDocument<rst-markup-sendreply>`.

Тестирование сценария
---------------------

Для удобства тестирования работы с документооборотом можно скачать файл коллекции Postman:

:download:`Файл коллекции Postman. </files/Коллекция для ДО.postman_collection.json>`

Примеры запросов и ответов
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Получение документооборота**

Запрос GET Docflow

.. code-block:: json

    GET /v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4 HTTP/1.1
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json


.. container:: toggle

    .. container:: header

        Ответ GET Docflow

    .. code-block:: http

        {
        "id": "351b56d1-5d81-4086-8763-0dd3ce55bcd4",
        "organization-id": "493fae9e-bb7e-4083-92b8-dbf0d3fe251f",
        "type": "urn:docflow:fns534-report",
        "status": "urn:docflow-common-status:response-arrived",
        "success-state": "urn:docflow-state:successful",
        "description": {
            "form-version": {
            "knd": "1151006",
            "version": "101420",
            "form-fullname": "Налоговая декларация по налогу на прибыль организаций",
            "form-shortname": "Налог на прибыль"
            },
            "recipient": "0087",
            "final-recipient": "0087",
            "correction-number": 0,
            "period-begin": "2024-01-01T00:00:00.0000000",
            "period-end": "2024-03-31T00:00:00.0000000",
            "period-code": "21",
            "payer-inn": "6676130154-667601001",
            "original-draft-id": "57a3c02c-45bd-48f2-9d68-bfaac4a7bb26"
        },
        "documents": [
            {
            "id": "70cfb8c2-dc31-4934-b711-790e000d435d",
            "description": {
                "type": "urn:document:fns534-report-processing-result-ok",
                "filename": "IV_NOPRIB_6676130154_6676130154_0087_20240605_6af5b7a175594e87b4d09976d89f4998.xml",
                "content-type": "application/xml",
                "encrypted-content-size": 5697,
                "compressed": true,
                "requisites": {},
                "support-recognition": false,
                "encrypted-certificates": [
                {
                    "serial-number": "0162F46C0052B049B7479E873C7CD2D53A"
                },
                {
                    "serial-number": "01D898980078AE9F924ECAFB68847A2FDD"
                },
                {
                    "serial-number": "01E5FEBA0066AE19A54714533E85B12D21"
                },
                {
                    "serial-number": "019AD8430015B1AAB345942CB5AB07ACCA"
                },
                {
                    "serial-number": "4EE4CA00AFAC11BD41775A5155DB8E9A"
                },
                {
                    "serial-number": "04C159D1006CB072A9427FC80ACEF59366"
                },
                {
                    "serial-number": "02A00CAD0060AD64A2469313549DA6BADC"
                },
                {
                    "serial-number": "03FDF18100C5AEF981425D21F40EA98169"
                }
                ],
                "support-print": "yes"
            },
            "content": {
                "encrypted": {
                "rel": "encrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/70cfb8c2-dc31-4934-b711-790e000d435d/encrypted-content"
                },
                "docflow-document-contents": [
                {
                    "content-id": "dcc87694-57e9-4100-8370-7bd7b58a8f2c",
                    "encrypted": true,
                    "compressed": true,
                    "compression-type": "zip"
                }
                ]
            },
            "send-date": "2024-06-05T07:29:41.8642330Z",
            "signatures": [
                {
                "id": "fb43aa47-238c-4526-9375-ded49afeb257",
                "title": "Тестовая инспекция",
                "signature-certificate-thumbprint": "C7163E8DA1D42FA6ECE315D4EA452A0710931586",
                "content-link": {
                    "rel": "content",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/70cfb8c2-dc31-4934-b711-790e000d435d/signatures/fb43aa47-238c-4526-9375-ded49afeb257/content"
                },
                "links": [
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/70cfb8c2-dc31-4934-b711-790e000d435d/signatures/fb43aa47-238c-4526-9375-ded49afeb257/content"
                    },
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4"
                    }
                ],
                "signer-type": "cu-representative"
                }
            ],
            "links": [
                {
                "rel": "docflow",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4"
                },
                {
                "rel": "self",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/70cfb8c2-dc31-4934-b711-790e000d435d"
                },
                {
                "rel": "reply",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/70cfb8c2-dc31-4934-b711-790e000d435d/generate-reply?documentType=fns534-report-receipt",
                "name": "fns534-report-receipt"
                },
                {
                "rel": "encrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/70cfb8c2-dc31-4934-b711-790e000d435d/encrypted-content"
                }
            ]
            },
            {
            "id": "9da55a39-c851-4433-88d6-d1c27ce425d2",
            "description": {
                "type": "urn:document:fns534-report-acceptance-result-positive",
                "filename": "KV_NOPRIB_6676130154_6676130154_0087_20240605_6603f82aaf374dc8af1e247f7c78068d.xml",
                "content-type": "application/xml",
                "encrypted-content-size": 5877,
                "compressed": true,
                "requisites": {},
                "support-recognition": false,
                "encrypted-certificates": [
                {
                    "serial-number": "0162F46C0052B049B7479E873C7CD2D53A"
                },
                {
                    "serial-number": "01D898980078AE9F924ECAFB68847A2FDD"
                },
                {
                    "serial-number": "01E5FEBA0066AE19A54714533E85B12D21"
                },
                {
                    "serial-number": "019AD8430015B1AAB345942CB5AB07ACCA"
                },
                {
                    "serial-number": "4EE4CA00AFAC11BD41775A5155DB8E9A"
                },
                {
                    "serial-number": "04C159D1006CB072A9427FC80ACEF59366"
                },
                {
                    "serial-number": "02A00CAD0060AD64A2469313549DA6BADC"
                },
                {
                    "serial-number": "03FDF18100C5AEF981425D21F40EA98169"
                }
                ],
                "support-print": "yes"
            },
            "content": {
                "encrypted": {
                "rel": "encrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/9da55a39-c851-4433-88d6-d1c27ce425d2/encrypted-content"
                },
                "docflow-document-contents": [
                {
                    "content-id": "56e689da-6826-4c54-8251-4ddb94ef40ed",
                    "encrypted": true,
                    "compressed": true,
                    "compression-type": "zip"
                }
                ]
            },
            "send-date": "2024-06-05T07:29:41.4579732Z",
            "signatures": [
                {
                "id": "848c5841-33a0-4d8a-9413-37463625cfcc",
                "title": "Тестовая инспекция",
                "signature-certificate-thumbprint": "C7163E8DA1D42FA6ECE315D4EA452A0710931586",
                "content-link": {
                    "rel": "content",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/9da55a39-c851-4433-88d6-d1c27ce425d2/signatures/848c5841-33a0-4d8a-9413-37463625cfcc/content"
                },
                "links": [
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/9da55a39-c851-4433-88d6-d1c27ce425d2/signatures/848c5841-33a0-4d8a-9413-37463625cfcc/content"
                    },
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4"
                    }
                ],
                "signer-type": "cu-representative"
                }
            ],
            "links": [
                {
                "rel": "docflow",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4"
                },
                {
                "rel": "self",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/9da55a39-c851-4433-88d6-d1c27ce425d2"
                },
                {
                "rel": "reply",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/9da55a39-c851-4433-88d6-d1c27ce425d2/generate-reply?documentType=fns534-report-receipt",
                "name": "fns534-report-receipt"
                },
                {
                "rel": "encrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/9da55a39-c851-4433-88d6-d1c27ce425d2/encrypted-content"
                }
            ]
            },
            {
            "id": "c244bee0-5d2c-47a3-b673-9621a9eb4cd4",
            "description": {
                "type": "urn:document:fns534-report-receipt",
                "filename": "IZ_NOPRIB_6676130154_6676130154_0087_20240605_7ff54fe418274bbe9f5cf63bd31fadf9.xml",
                "content-type": "application/xml",
                "decrypted-content-size": 5280,
                "compressed": true,
                "requisites": {},
                "support-recognition": false,
                "encrypted-certificates": [],
                "support-print": "yes"
            },
            "content": {
                "decrypted": {
                "rel": "decrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/c244bee0-5d2c-47a3-b673-9621a9eb4cd4/decrypted-content"
                },
                "docflow-document-contents": [
                {
                    "content-id": "016d8a15-6a25-4e7d-8a8c-29a4194f9cf8",
                    "encrypted": false,
                    "compressed": true,
                    "compression-type": "zip"
                },
                {
                    "content-id": "3c359e25-938a-443d-b110-3266edaf789f",
                    "encrypted": false,
                    "compressed": false,
                    "compression-type": "none"
                }
                ]
            },
            "send-date": "2024-06-05T07:29:41.2860963Z",
            "signatures": [
                {
                "id": "ddacb971-a109-4faa-ba11-4a9d24ebce90",
                "title": "Тестовая инспекция",
                "signature-certificate-thumbprint": "C7163E8DA1D42FA6ECE315D4EA452A0710931586",
                "content-link": {
                    "rel": "content",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/c244bee0-5d2c-47a3-b673-9621a9eb4cd4/signatures/ddacb971-a109-4faa-ba11-4a9d24ebce90/content"
                },
                "links": [
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/c244bee0-5d2c-47a3-b673-9621a9eb4cd4/signatures/ddacb971-a109-4faa-ba11-4a9d24ebce90/content"
                    },
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4"
                    }
                ],
                "signer-type": "cu-representative"
                }
            ],
            "links": [
                {
                "rel": "docflow",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4"
                },
                {
                "rel": "self",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/c244bee0-5d2c-47a3-b673-9621a9eb4cd4"
                },
                {
                "rel": "decrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/c244bee0-5d2c-47a3-b673-9621a9eb4cd4/decrypted-content"
                }
            ]
            },
            {
            "id": "e4069c18-e7a6-46dc-83f2-c2ac00ed6acf",
            "description": {
                "type": "urn:document:fns534-report",
                "filename": "NO_PRIB_0087_0087_6676130154667601001_20240605_d6d369c3-2cbc-4090-b3ad-ea69ce62f74d.xml",
                "content-type": "application/xml",
                "decrypted-content-size": 1902,
                "encrypted-content-size": 2758,
                "compressed": true,
                "requisites": {},
                "related-docflows-count": 0,
                "support-recognition": false,
                "encrypted-certificates": [
                {
                    "serial-number": "0162F46C0052B049B7479E873C7CD2D53A"
                },
                {
                    "serial-number": "019AD8430015B1AAB345942CB5AB07ACCA"
                },
                {
                    "serial-number": "19CCC7C800010000215D"
                }
                ],
                "support-print": "yes"
            },
            "content": {
                "decrypted": {
                "rel": "decrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/e4069c18-e7a6-46dc-83f2-c2ac00ed6acf/decrypted-content"
                },
                "encrypted": {
                "rel": "encrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/e4069c18-e7a6-46dc-83f2-c2ac00ed6acf/encrypted-content"
                },
                "docflow-document-contents": [
                {
                    "content-id": "622a2575-cb6e-456d-b62f-f2795bcb63f3",
                    "encrypted": true,
                    "compressed": true,
                    "compression-type": "zip"
                },
                {
                    "content-id": "8ee4656b-534d-48c9-a829-82602e962a63",
                    "encrypted": false,
                    "compressed": false,
                    "compression-type": "none"
                }
                ]
            },
            "send-date": "2024-06-05T07:27:58.5805863Z",
            "signatures": [
                {
                "id": "536d1a44-3469-48aa-99db-b19e012d2906",
                "title": "Тестовая Коннектор АО (Коннект АО Коннекторович)",
                "signature-certificate-thumbprint": "0778B8EFD8B4C49040494C15355B2556D2957774",
                "content-link": {
                    "rel": "content",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/e4069c18-e7a6-46dc-83f2-c2ac00ed6acf/signatures/536d1a44-3469-48aa-99db-b19e012d2906/content"
                },
                "links": [
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/e4069c18-e7a6-46dc-83f2-c2ac00ed6acf/signatures/536d1a44-3469-48aa-99db-b19e012d2906/content"
                    },
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4"
                    }
                ],
                "signer-type": "organization-representative"
                },
                {
                "id": "f584030f-134b-4a22-8fa5-67b6ac1c07a7",
                "title": "Тестовая инспекция (Прескарьян Никита Владимирович)",
                "signature-certificate-thumbprint": "C7163E8DA1D42FA6ECE315D4EA452A0710931586",
                "content-link": {
                    "rel": "content",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/e4069c18-e7a6-46dc-83f2-c2ac00ed6acf/signatures/f584030f-134b-4a22-8fa5-67b6ac1c07a7/content"
                },
                "links": [
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/e4069c18-e7a6-46dc-83f2-c2ac00ed6acf/signatures/f584030f-134b-4a22-8fa5-67b6ac1c07a7/content"
                    },
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4"
                    }
                ],
                "signer-type": "cu-representative"
                }
            ],
            "links": [
                {
                "rel": "docflow",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4"
                },
                {
                "rel": "self",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/e4069c18-e7a6-46dc-83f2-c2ac00ed6acf"
                },
                {
                "rel": "related-docflow",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/e4069c18-e7a6-46dc-83f2-c2ac00ed6acf/related"
                },
                {
                "rel": "encrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/e4069c18-e7a6-46dc-83f2-c2ac00ed6acf/encrypted-content"
                },
                {
                "rel": "decrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/e4069c18-e7a6-46dc-83f2-c2ac00ed6acf/decrypted-content"
                }
            ]
            },
            {
            "id": "7b089709-0e76-40fd-96e1-f5155ed069ea",
            "description": {
                "type": "urn:document:fns534-report-date-confirmation",
                "filename": "PD_NOPRIB_6676130154667601001_6676130154667601001_1BM_20240605_c333f747-7c26-44cc-bc47-1057f7716eed.xml",
                "content-type": "application/xml",
                "decrypted-content-size": 2808,
                "compressed": true,
                "requisites": {},
                "support-recognition": false,
                "encrypted-certificates": [],
                "support-print": "yes"
            },
            "content": {
                "decrypted": {
                "rel": "decrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/7b089709-0e76-40fd-96e1-f5155ed069ea/decrypted-content"
                },
                "docflow-document-contents": [
                {
                    "content-id": "63513998-d1d7-4211-a6c4-3880a8d3a1e8",
                    "encrypted": false,
                    "compressed": true,
                    "compression-type": "zip"
                },
                {
                    "content-id": "141d879a-7077-4708-bced-d43539d12b9a",
                    "encrypted": false,
                    "compressed": false,
                    "compression-type": "none"
                }
                ]
            },
            "send-date": "2024-06-05T07:27:58.5805863Z",
            "signatures": [
                {
                "id": "2f1c98e2-559f-4b15-a5fa-e7d861a55575",
                "title": "АО «ПФ «СКБ Контур»",
                "signature-certificate-thumbprint": "DE32892038096F6A1932EEC6316AF05C7EF042B3",
                "content-link": {
                    "rel": "content",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/7b089709-0e76-40fd-96e1-f5155ed069ea/signatures/2f1c98e2-559f-4b15-a5fa-e7d861a55575/content"
                },
                "links": [
                    {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/7b089709-0e76-40fd-96e1-f5155ed069ea/signatures/2f1c98e2-559f-4b15-a5fa-e7d861a55575/content"
                    },
                    {
                    "rel": "docflow",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4"
                    }
                ],
                "signer-type": "provider-representative"
                }
            ],
            "links": [
                {
                "rel": "docflow",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4"
                },
                {
                "rel": "self",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/7b089709-0e76-40fd-96e1-f5155ed069ea"
                },
                {
                "rel": "reply",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/7b089709-0e76-40fd-96e1-f5155ed069ea/generate-reply?documentType=fns534-report-receipt",
                "name": "fns534-report-receipt"
                },
                {
                "rel": "decrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/7b089709-0e76-40fd-96e1-f5155ed069ea/decrypted-content"
                }
            ]
            },
            {
            "id": "6383d098-8ad7-4641-8eb6-dee07ff8508d",
            "description": {
                "type": "urn:document:fns534-report-description",
                "filename": "TR_DEKL.xml",
                "content-type": "application/xml",
                "decrypted-content-size": 348,
                "compressed": true,
                "requisites": {},
                "support-recognition": false,
                "encrypted-certificates": [],
                "support-print": "no"
            },
            "content": {
                "decrypted": {
                "rel": "decrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/6383d098-8ad7-4641-8eb6-dee07ff8508d/decrypted-content"
                },
                "docflow-document-contents": [
                {
                    "content-id": "9a8fe739-6b91-47e0-b25c-9e9d3de9ef86",
                    "encrypted": false,
                    "compressed": false,
                    "compression-type": "none"
                },
                {
                    "content-id": "65d567b8-c814-4c80-921d-f7198ecbe1c6",
                    "encrypted": false,
                    "compressed": true,
                    "compression-type": "zip"
                }
                ]
            },
            "send-date": "2024-06-05T07:27:58.5805863Z",
            "signatures": [],
            "links": [
                {
                "rel": "docflow",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4"
                },
                {
                "rel": "self",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/6383d098-8ad7-4641-8eb6-dee07ff8508d"
                },
                {
                "rel": "decrypted-content",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/6383d098-8ad7-4641-8eb6-dee07ff8508d/decrypted-content"
                }
            ]
            }
        ],
        "links": [
            {
            "rel": "self",
            "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4"
            },
            {
            "rel": "organization",
            "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/organizations/493fae9e-bb7e-4083-92b8-dbf0d3fe251f"
            },
            {
            "rel": "web-docflow",
            "href": "https://setter.testkontur.ru/?inn=6676130154-667601001&forward_to_rel=/ft/transmission/state.aspx?key=jtxgDj59ckiXMjZoszIOU56uP0l%2bu4NAkrjb8NP%2bJR9tfCHF%2fajPSpl8baZKm1900VYbNYFdhkCHYw3TzlW81A%3d%3d"
            },
            {
            "rel": "reply",
            "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/70cfb8c2-dc31-4934-b711-790e000d435d/generate-reply?documentType=fns534-report-receipt",
            "name": "fns534-report-receipt"
            },
            {
            "rel": "reply",
            "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/9da55a39-c851-4433-88d6-d1c27ce425d2/generate-reply?documentType=fns534-report-receipt",
            "name": "fns534-report-receipt"
            },
            {
            "rel": "reply",
            "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/7b089709-0e76-40fd-96e1-f5155ed069ea/generate-reply?documentType=fns534-report-receipt",
            "name": "fns534-report-receipt"
            }
        ],
        "send-date": "2024-06-05T10:27:58.5805863",
        "last-change-date": "2024-06-05T07:29:41.8642330Z"
        }

**Скачивание контента**

Запрос GET Download

.. code-block:: json

    GET /v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/contents/56e689da-6826-4c54-8251-4ddb94ef40ed HTTP/1.1
    Authorization: Bearer <token>
    Content-Type: application/octet-stream

Ответ GET Dowload

.. code-block:: json

    HTTP/1.1 200 OK
    Content-Type: application/octet-stream
    Content-Length: 727
    
    "0�*�H����0�1�0��0�0��..."

**Создание ответного документа**

Запрос POST CreateReplyDocument

.. code-block:: json

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

        Ответ POST CreateReplyDocument

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

**Подписание ответного документа**

Запрос PUT ReplyDocumentSignature

.. code-block:: json

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

        Ответ PUT ReplyDocumentSignature

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

**Отправка ответного документа**

Запрос POST SendReplyDocument

.. code-block:: json

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

        Ответ POST SendReplyDocument

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


