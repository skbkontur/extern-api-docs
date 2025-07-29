.. _`Extern Test Tools`: https://developer.kontur.ru/doc/extern.test.tools
.. _`налог на прибыль`: https://developer.kontur.ru/doc/extern.test.tools/method?type=post&path=%2Ftest-tools%2Fv1%2Fgenerate-fuf-profit-tax
.. _`НДС с приложениями`: https://developer.kontur.ru/doc/extern.test.tools/method?type=post&path=%2Ftest-tools%2Fv1%2Fgenerate-fuf-nds-with-attachments
.. _`РСВ`: https://developer.kontur.ru/doc/extern.test.tools/method?type=post&path=%2Ftest-tools%2Fv1%2Fgenerate-fuf-rsv
.. _`3-НДФЛ`: https://developer.kontur.ru/doc/extern.test.tools/method?type=post&path=%2Ftest-tools%2Fv1%2Fgenerate-fuf-3ndfl

Отправка отчетности в ФНС
=========================

С помощью API Контур.Экстерн можно передавать отчетность в контролирующие органы (КО) сразу из своей учетной системы. Мы проверим файлы отчета на наличие ошибок перед отправкой их в ФНС. Для этого потребуется готовый файл отчета и электронная подпись, которой будут подписаны файлы отчета и его приложения.

В ФНС можно отправить:

* декларации, 2-НДФЛ и 6-НДФЛ (urn:docflow:fns534-report);
* заявления в ФНС (urn:docflow:fns534-application);
* представления в ФНС (urn:docflow:fns534-submission).

Особенности файлов отчетов:

* файл отчета должен быть сформирован и заполнен по требованиям контролирующего органа;
* файл отчета должен быть в формате xml;
* приложения, дополнения к отчету или файл доверенности могут быть в форматах xml, txt, xsl;
* :ref:`наименование файлов<rst-markup-namefileFNS>` отчета должно совпадать с именем внутри файла в параметре ИдФайл тега Файл.

Для отправки отчета в КО необходимо создать черновик и наполнить его документами. Подробнее об этом в разделе Алгоритм работы с методами. 

Подписание документов
---------------------

Каждый файл в отправляемом черновике должен быть подписан закрытым ключом сертификата отправителя. Электронная подпись должна быть выпущена на организацию. Если подпись выпущена на физическое лицо, то потребуется доверенность на это лицо от организации. 

Алгоритм работы с методами
--------------------------

1. Создайте черновик: :ref:`POST Create draft<rst-markup-createdraft>`. В метаинформации укажите:

    * ``payer`` — сведения о налогоплательщике или организации, за которую отправляется отчетность;
    * ``sender`` — отправитель или организация, которая общается с КО, отправляет и получает документы;
    * ``recipeint`` — сведения о получателе документооборота, то есть о контролирующем органе.

        Метод вернет идентификатор черновика ``draftId``, метаинформацию черновика и ссылки для работы с ним.


2. Загрузите файл отчета и приложения к нему в :ref:`Сервис контентов<rst-markup-load>`. В ответ метод загрузки вернет идентификатор загруженного контента ``content-id``.

3. Создайте для каждого файла отдельный документ в черновике: :ref:`POST Add Document<rst-markup-addDocument>`. Укажите идентификатор контента в параметре ``content-id``.

4. Проверьте документы: :ref:`POST Check<rst-markup-check>`.

5. Добавьте подпись к документам: :ref:`POST Add signature<rst-markup-AddSignature>`.

6. Запустите последовательность методов, когда черновик будет готов: :ref:`POST Check<rst-markup-check>` -> :ref:`POST Prepare<rst-markup-prepare>` -> :ref:`POST Send<rst-markup-send>`. Укажите флаг ``deferred = true`` для отложенного выполнения задач.

7. Проверьте статус выполнения задач для методов ``Check``, ``Prepare``, ``Send``: :ref:`GET DraftTask<rst-markup-DraftTasks>`. Если задача по методу ``Send`` завершилась успешно, то в ответе вернется информация о созданном документообороте (ДО).

После отправки черновика появляется документооборот. Дальнейшая работа с ДО состоит в мониторинге статусов ДО, получение входящих документов и отправке ответных документов. Подробнее об этом в :ref:`следующей статье<rst-markup-get_report>`. 

Тестирование сценария
---------------------

Для тестирования сценария отправки отчета в ФНС можно сгенерировать тестовые файлы отчетов с помощью сервиса `Extern Test Tools`_:

* `налог на прибыль`_;
* `НДС с приложениями`_;
* `РСВ`_;
* `3-НДФЛ`_.

Для удобства тестирования алгоритма создания и отправки черновика можно скачать файл коллекции Postman:

:download:`Файл коллекции Postman. </files/Коллекция для черновика.postman_collection.json>` 


Примеры запросов и ответов
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Создание черновика**

.. container:: toggle

    .. container:: header

        Пример запроса POST CreateDraft

    .. code-block:: http

        POST /v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/drafts HTTP/1.1
        Host: extern-api.testkontur.ru
        Authorization: Bearer <token>
        Accept: application/json
        Content-Type: application/json
 
        {
            "sender": {
                "inn": "6676130154",
                "kpp": "667601001",
                "certificate": {
                    "content": "MIIJoDCCCU2...+gkMb1HXNfNc="
                },
                "is-representative": "true",
                "ipaddress": "8.8.8.8"
            },
            "recipient": {
                "ifns-code": "0087"
            },
            "payer": {
                "inn": "6676130154",
                "organization": {
                    "kpp": "667601001"
                },
            }
            
        }

.. container:: toggle

    .. container:: header

        Ответ POST CreateDraft

    .. code-block:: http
   
        HTTP/1.1 201 Created
        Content-Type: application/json; charset=utf-8
 
        {
            "id": "57a3c02c-45bd-48f2-9d68-bfaac4a7bb26",
            "docflows": [],
            "documents": [],
            "meta": {
                "sender": {
                    "inn": "6676130154",
                    "kpp": "667601001",
                    "name": "Тестовая Коннектор АО",
                    "certificate": {
                        "content": "MIIJ...+gkMb1HXNfNc="
                    },
                    "is-representative": true,
                    "ipaddress": "8.8.8.8"
                },
                "recipient": {
                    "ifns-code": "0087"
                },
                "payer": {
                    "inn": "6676130154",
                    "name": "Тестовая Коннектор АО",
                    "organization": {
                        "kpp": "667601001"
                    }
                }
            },
            "status": "new",
            "links": [
                {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/drafts/57a3c02c-45bd-48f2-9d68-bfaac4a7bb26"
                }
            ]
        }

**Загрузка файла отчета в Сервис контентов**

Запрос POST UploadContent

.. code-block:: json

    POST /v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/contents HTTP/1.1
    Authorization: Bearer <token>
    Content-Type: application/octet-stream
    Host: extern-api.testkontur.ru
    Accept-Encoding: gzip, deflate, br
    Content-Length: 52
    Content-Range: bytes 0-1901/1902
    
    Контент передан в теле запроса

Ответ POST UploadContent

.. code-block:: json

    HTTP/1.1 201 Created
    Content-Type: application/json; charset=utf-8
    Content-Length: 100
    
    {
        "id": "1816fdca-e743-4eb9-8221-b26b0762e015"
    }

**Создания документа в черновике**

Запрос POST Add Document

.. code-block:: json

    POST /v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/drafts/57a3c02c-45bd-48f2-9d68-bfaac4a7bb26/documents HTTP/1.1
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json
    Host: extern-api.testkontur.ru
    
    {
        "content-id": "1816fdca-e743-4eb9-8221-b26b0762e015"
    }


.. container:: toggle

    .. container:: header

        Ответ POST Add Document

    .. code-block:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=utf-8
 
        {
            "id": "ea7cdf3e-6f80-4b94-be0d-e36f1ff84d8e",
            "decrypted-content-link": {
                "rel": "",
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/drafts/57a3c02c-45bd-48f2-9d68-bfaac4a7bb26/documents/ea7cdf3e-6f80-4b94-be0d-e36f1ff84d8e/decrypted-content"
            },
            "description": {
                "filename": "NO_PRIB_0087_0087_6676130154667601001_20240605_d6d369c3-2cbc-4090-b3ad-ea69ce62f74d.xml",
                "content-type": "application/xml",
                "properties": {
                    "Encoding": "windows-1251",
                    "FormName": "Налоговая декларация по налогу на прибыль организаций",
                    "КНД": "1151006",
                    "CorrectionNumber": "0",
                    "IsPrintable": "True",
                    "Period": "I кв. 2024",
                    "OriginalFilename": null,
                    "SvdregCode": null,
                    "contentType": "Xml",
                    "AccountingPeriodBegin": "01.01.2024",
                    "AccountingPeriodEnd": "03.31.2024"
                }
            },
            "contents": [
                {
                    "content-id": "1804ef59-ba18-4f4c-bfcc-7f4134ae429f",
                    "encrypted": false
                }
            ]
        }

**Добавление подписи к документам**

Запрос POST AddSignature

.. code-block:: json

    POST /v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/drafts/57a3c02c-45bd-48f2-9d68-bfaac4a7bb26/documents/ea7cdf3e-6f80-4b94-be0d-e36f1ff84d8e/signatures HTTP/1.1
    Host: extern-api.testkontur.ru
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json
    Content-Type: application/pgp-signature
    
    {
    "base64-content": "MIINYQYJK...JmPNEqCaE+h",
    "is-third-party-signature": false
    }

.. container:: toggle

    .. container:: header

        Ответ POST AddSignature

    .. code-block:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=utf-8

        {
        "id": "536d1a44-3469-48aa-99db-b19e012d2906",
        "signature-certificate-thumbprint": "0778B8EFD8B4C49040494C15355B2556D2957774",
        "content-link": {
            "rel": "content",
            "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/drafts/57a3c02c-45bd-48f2-9d68-bfaac4a7bb26/documents/ea7cdf3e-6f80-4b94-be0d-e36f1ff84d8e/signatures/536d1a44-3469-48aa-99db-b19e012d2906/content"
        },
        "links": [
            {
            "rel": "self",
            "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/drafts/57a3c02c-45bd-48f2-9d68-bfaac4a7bb26/documents/ea7cdf3e-6f80-4b94-be0d-e36f1ff84d8e/signatures/536d1a44-3469-48aa-99db-b19e012d2906"
            },
            {
            "rel": "document",
            "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/drafts/57a3c02c-45bd-48f2-9d68-bfaac4a7bb26/documents/ea7cdf3e-6f80-4b94-be0d-e36f1ff84d8e"
            },
            {
            "rel": "draft",
            "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/drafts/57a3c02c-45bd-48f2-9d68-bfaac4a7bb26"
            }
        ],
        "signer-type": "organization-representative"
        }

**Проверка черновика**

Запрос POST Check

.. code-block:: json

    POST /v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/drafts/57a3c02c-45bd-48f2-9d68-bfaac4a7bb26/check?deferred=true HTTP/1.1
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json

Ответ POST Check

.. code-block:: json

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=utf-8  
    
    {
        "id": "4e686a8a-5dce-4dd0-ba51-d474cc0e20b1",
        "task-state": "running",
        "task-type": "urn:task-type:check"
    }

**Подготовка черновика**

Запрос POST Prepare

.. code-block:: json

    POST /v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/drafts/57a3c02c-45bd-48f2-9d68-bfaac4a7bb26/prepare?deferred=true HTTP/1.1
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json

Ответ POST Prepare

.. code-block:: json

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=utf-8
    
    {
        "id": "cace972c-b3b5-420c-ac4f-c7074080ec48",
        "task-state": "running",
        "task-type": "urn:task-type:prepare"
    }

**Отправка черновика**

Запрос POST Send

.. code-block:: json

    POST /v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/drafts/57a3c02c-45bd-48f2-9d68-bfaac4a7bb26/send?deferred=true HTTP/1.1
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json

Ответ POST Send

.. code-block:: json

    HTTP/1.1 200 OK
    
    {
        "id": "408b2dcf-bc6e-45da-907e-43ec90b92d0e",
        "task-state": "running",
        "task-type": "urn:task-type:send"
    }

**Проверка задачи Check**

Запрос GET TaskId

.. code-block:: json

    GET /v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/drafts/57a3c02c-45bd-48f2-9d68-bfaac4a7bb26/tasks/4e686a8a-5dce-4dd0-ba51-d474cc0e20b1 HTTP/1.1
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json
    Host: extern-api.testkontur.ru

Ответ GET TaskId

.. code-block:: json

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=utf-8
    Content-Length: 285
    
    {
        "id": "4e686a8a-5dce-4dd0-ba51-d474cc0e20b1",
        "task-state": "succeed",
        "task-type": "urn:task-type:check",
        "task-result": {
            "data": {
            "documents-errors": {
                "4b3046fe-cabd-42e5-8618-8e9d9b2466a0": []
            },
            "common-errors": []
            }
        }
    }

**Проверка задачи Prepare**

Запрос GET TaskId

.. code-block:: json

    GET /v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/drafts/57a3c02c-45bd-48f2-9d68-bfaac4a7bb26/tasks/cace972c-b3b5-420c-ac4f-c7074080ec48 HTTP/1.1
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json
    Host: extern-api.testkontur.ru


.. container:: toggle

    .. container:: header

        Ответ GET TaskId

    .. code-block:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=utf-8
        
        {
            "id": "cace972c-b3b5-420c-ac4f-c7074080ec48",
            "task-state": "succeed",
            "task-type": "urn:task-type:prepare",
            "task-result": {
                "check-result": {
                    "documents-errors": {
                        "b32171d6-9ebc-4c73-b557-5a203b68f8df": []
                    },
                    "common-errors": []
                },
                "links": [
                    {
                        "rel": "next",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/74b6e8b9-290a-4d12-b874-c7fb35cad54f/send?force=false"
                    }
                ],
                "status": "ok"
            }
        }

**Проверка задачи Send**

Запрос GET TaskId

.. code-block:: json

    GET /v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/drafts/57a3c02c-45bd-48f2-9d68-bfaac4a7bb26/tasks/8be51112-d4ee-4c8c-8bc6-7cd46e369a68 HTTP/1.1
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json
    Host: extern-api.testkontur.ru


.. container:: toggle

    .. container:: header

        Ответ GET TaskId

    .. code-block:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=utf-8

        {
        "id": "8be51112-d4ee-4c8c-8bc6-7cd46e369a68",
        "task-state": "succeed",
        "task-type": "urn:task-type:send",
        "task-result": {
            "id": "351b56d1-5d81-4086-8763-0dd3ce55bcd4",
            "organization-id": "493fae9e-bb7e-4083-92b8-dbf0d3fe251f",
            "type": "urn:docflow:fns534-report",
            "status": "urn:docflow-common-status:sent",
            "success-state": "urn:docflow-state:neutral",
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
                    "content-id": "65d567b8-c814-4c80-921d-f7198ecbe1c6",
                    "encrypted": false,
                    "compressed": true,
                    "compression-type": "zip"
                    },
                    {
                    "content-id": "9a8fe739-6b91-47e0-b25c-9e9d3de9ef86",
                    "encrypted": false,
                    "compressed": false,
                    "compression-type": "none"
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
                "href": "https://extern-api.testkontur.ru/v1/c5217c6d-a8fd-4acf-997c-6da64a9b5f74/docflows/351b56d1-5d81-4086-8763-0dd3ce55bcd4/documents/7b089709-0e76-40fd-96e1-f5155ed069ea/generate-reply?documentType=fns534-report-receipt",
                "name": "fns534-report-receipt"
            }
            ],
            "send-date": "2024-06-05T10:27:58.5805863",
            "last-change-date": "2024-06-05T07:27:58.5805863Z"
        }
        }

