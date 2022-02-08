.. _`CreateDraft`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts
.. _`Add document`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments
.. _`Check`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fcheck
.. _`POST Generate ssch`: https://developer.kontur.ru/doc/extern.test.tools/method?type=post&path=%2Ftest-tools%2Fv1%2Fgenerate-fuf-ssch
.. _`POST AddSignature`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures
.. _`PUT Signature`: https://developer.kontur.ru/doc/extern.drafts/method?type=put&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures%2F%7BsignatureId%7D
.. _`SignDraft`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fcloud-sign
.. _`GET DraftDocument`: https://developer.kontur.ru/doc/extern.drafts/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D
.. _`GET DraftTasks`: https://developer.kontur.ru/doc/extern.drafts/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Ftasks
.. _`GET TaskId`: https://developer.kontur.ru/doc/extern.drafts/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Ftasks%2F%7BapiTaskId%7D

.. _rst-markup-howtodraft:

Работа с черновиком
===================

.. note:: Черновик можно отправить только один раз. После успешной отправки черновик будет храниться в течение 1 года. 

В данном разделе мы описали краткий процесс работы с черновиком на примере отчета о среднесписочной численности. Также объясним зачем нужны многочисленные проверки черновика и как работать с задачами (Tasks). 

.. image:: /_static/howtodraftalg.jpg

**Порядок работы с черновиком:**

    1. `Создание черновика`_.
    2. `Наполнение черновика файлами документов`_.
    3. `Проверка документов`_.
    4. `Наполнение черновика подписями документов`_.
    5. `Проверка, подготовка, отправка черновика с помощью задач`_. 

Для удобства тестирования алгоритма создания и отправки черновика можно скачать файл коллекции Postman:

:download:`файл коллекции Postman <../files/Работа с черновиком.postman_collection.json>`

Прежде чем приступить к созданию черновика, нужно подумать о сценарии: чем наполнить черновик? Нужен файл отчета. 

**Где взять тестовый файл отчета?**

Скорее всего у пользователя уже будут файлы бухгалтерской отчетности, которые он сформирует и заполнит по требованиям контролирующего органа. Но, чтобы настроить отправку, протестировать разные сценарии работы, не нужно обращаться к конечным пользователям за данными файлами. Предлагаем вам взять готовые примеры или сгенерировать свои файлы. 

    На странице :doc:`/manuals/files-for-examples` можно найти и скачать файлы отчетов, но в них нужно будет заполнить данные согласно вашей учетной записи.  

    В сервисе генерации тестовых данных Extern Test Tools можно сгенерировать файл отчета. При помощи метода генерации файлов получим `POST Generate ssch`_ файл отчета ССЧ в формате xml. Файл необходимо сохранить с именем из тега Файл, параметра ИдФайл. И в названии, и в теге имя файла должно полностью совпадать, см. рисунок.

    .. image:: /_static/fileName.png
        :width: 800

Создание черновика
------------------

Прежде чем загрузить отчет, нужно создать контейнер, который будет хранить помимо файлов отчета также и метаинформацию о нем. Данный контейнер — это черновик. Чтобы создать его, вызываем метод `CreateDraft`_. В данном методе необходимо передать метаинформацию о налогоплательщике, отправителе и получателе:

    - Payer — налогоплательщик (НП), организация, за которую отправляется отчетность,
    - Sender — отправитель. Организация, которая общается с контролирующими органами, отправляет и получает документы. Payer и Sender могут совпадать.
    - Recipient — получатель документооборота, т.е. контролирующий орган (КО). 

При создании черновика нужно передать контент сертификата в формате `base64`, который будет использован пользователем для подписания документов.

.. container:: toggle

    .. container:: header

        **Пример запроса POST CreateDraft**

    .. code-block:: http

        POST /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts HTTP/1.1
        Host: extern-api.testkontur.ru
        Authorization: Bearer <token>
        Accept: application/json
        Content-Type: application/json

        {
            "sender": {
            "inn": "7757424860",
            "kpp": "680345565",
            "certificate": {
            "content": "MIIJcDCCCR...+/MYE3Xk=" },
            "is-representative": true, 
            "ipaddress": "8.8.8.8" 
            },
            "recipient": { 
                "ifns-code": "0007"  
            },
            "payer": {
                "inn": "7757424860",
                "organization": {
                "kpp": "680345565"
                    }
            }
        }

В ответе метод возвращает метаинформацию черновика, которую вы передали, а также его идентификатор и ссылки для работы с черновиком. В данном случае можно перейти по ссылке и выполнить запрос, чтобы посмотреть содержимое черновика.

.. container:: toggle

    .. container:: header

        **Ответ GET DraftDocument**

    .. code-block:: http
   
        HTTP/1.1 200 OK
        Content-Type: application/json; charset=utf-8

        {
            "id": "d9622b9d-aa31-477b-a399-fc676588bfb5",
            "docflows": [],
            "documents": [],
            "meta": {
                "sender": {
                "inn": "7757424860",
                "kpp": "680345565",
                "name": "Тестовая организация",
                "certificate": {
                    "content": "MIIJcDCCCR...ykqopO+/MYE3Xk="
                },
                "is-representative": true,
                "ipaddress": "8.8.8.8"
                },
                "recipient": {
                "ifns-code": "0007"
                },
                "payer": {
                "inn": "7757424860",
                "name": "Тестовая организация",
                "organization": {
                    "kpp": "680345565"
                }
                }
            },
            "status": "new",
            "links": [
                {
                "rel": "self",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/d9622b9d-aa31-477b-a399-fc676588bfb5"
                }
            ]
        }

Наполнение черновика файлами документов
---------------------------------------

Черновик необходимо наполнить файлом отчета, приложениями к отчету и подписями. Главный файл отчета — это всегда xml-файл. К отчету могут идти также приложения и другие связанные файлы, например, доверенность. Каждый файл в черновике нужно загрузить в сервис контентов, а также для каждого файла нужно создавать отдельный документ в черновике при помощи метода `Add document`_. 

Для более гибкой работы с файлами предусмотрена возможность также создать пустой документ в черновике, чтобы в дальнейшем методом PUT положить контент файла.  


**Пример запроса POST UploadContent**

.. code-block:: http


    POST /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/contents HTTP/1.1
    Authorization: Bearer <token>
    Content-Type: application/octet-stream
    Host: extern-api.testkontur.ru
    Accept-Encoding: gzip, deflate, br
    Content-Length: 727

    Контент передан в теле запроса 

В ответе метод загрузки контента вернет идентификатор загруженного контента, который нужно передать в методе создания документа. 

**Пример запроса POST AddDocument:**

.. code-block:: json
   
    POST /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/d9622b9d-aa31-477b-a399-fc676588bfb5/documents HTTP/1.1
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json
    Host: extern-api.testkontur.ru

    {
        "content-id": "719a73dc-ecf8-49d1-b6be-b4251fd90553"
    }

Мы намеренно не заполняем метаинформацию об отчете в запросе. Если файл корректный, то метод сам распознает нужную метаинформацию и вернет ее в ответе.

.. container:: toggle

    .. container:: header

        **Ответ POST AddDocument:**

    .. code-block:: http
    
        HTTP/1.1 200 OK
        Content-Type: application/json; charset=utf-8

        {
            "id": "4b3046fe-cabd-42e5-8618-8e9d9b2466a0",
            "decrypted-content-link": {
                "rel": "",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/d9622b9d-aa31-477b-a399-fc676588bfb5/documents/4b3046fe-cabd-42e5-8618-8e9d9b2466a0/decrypted-content"
            },
            "description": {
                "filename": "NO_SRCHIS_0007_0007_7757424860680345565_20200129_92425a70-4ac9-4680-bada-3666f0c0514v.xml",
                "content-type": "application/xml",
                "properties": {
                "Encoding": "windows-1251",
                "FormName": "Сведения о среднесписочной численности работников за предшествующий календарный год",
                "КНД": "1110018",
                "CorrectionNumber": "0",
                "IsPrintable": "True",
                "Period": "2018 год",
                "OriginalFilename": null,
                "SvdregCode": null,
                "contentType": "Xml",
                "AccountingPeriodBegin": "01.01.2018",
                "AccountingPeriodEnd": "12.31.2018"
                }
            },
            "contents": [
                {
                "content-id": "a1c26991-1ce9-4d51-8ee2-83303b7dd31d",
                "encrypted": false
                }
            ]
        }

Проверка документов
-------------------

Прежде чем подписывать файлы, лучше выполнить проверку документов черновика методом `Check`_. Данный метод выполняет:

    * проверку на соответствие формату, то есть xml-файл документа проходит проверку по xsd-схеме;
    * проверки правильности контрольных соотношений согласно формату документа;
    * кросс-проверки между документами черновика, например, соответствие подписантов в доверенности и документе.

**Ответ метода Check:**

.. code-block:: json
    
   {
	"data": {
    	"documents-errors": {
            "6ea75127-abc8-4866-b67d-464f1e678273": []
    	},
    	"common-errors": []
	}
   }

Мы убедились, что файл отчета корректный, Check не выявил ошибок. Можно подписывать файл, который положили в черновик. У нас в примере в черновике лежит только один файл отчета, соответственно нам нужно приложить подпись только к нему.

Наполнение черновика подписями документов
-----------------------------------------

Под каждым файлом клиент ставит свою подпись, чтобы подтвердить свою личность как отправителя. Подпись можно добавить к документу методом `POST AddSignature`_. 

.. warning:: Если документы в черновике изменятся, то подписи станут недействительными.

Если документ изменится, то подпись также нужно будет заменить. Для редактирования подписи текущего документа используйте метод `PUT Signature`_.

Порядок работы с подписью
~~~~~~~~~~~~~~~~~~~~~~~~~

    1. Подписываем файл отчета закрытым ключом электронной подписи. 
    2. Конвертируем полученную подпись в base64.
    3. Добавляем подпись в формате base64 в черновик. 

**Запрос POST AddSignature:**

.. code-block:: http

    POST /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/d9622b9d-aa31-477b-a399-fc676588bfb5/documents/4b3046fe-cabd-42e5-8618-8e9d9b2466a0/signatures HTTP/1.1
    Host: extern-api.testkontur.ru
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json
    Content-Type: application/pgp-signature

    {
        "base64-content":"MIINFQYJKoZIhvcNAQcCoIINBjCCD...nOfRonWQdDi4Tavb9CLvI="
    }

Мы убедились, что файл отчета корректный, и подпись документа лежит в черновике. Можно переходить к подготовке черновика и отправке. 

Проверка, подготовка, отправка черновика  с помощью задач
---------------------------------------------------------

Перед отправкой отчетности в налоговый орган необходимо прогнать черновик через три метода в строгом порядке: **Check -> Prepare -> Send**. Если хотя бы в одном из методов произошла ошибка, черновик не будет отправлен в налоговый орган. 

Существует возможность не вызывать методы последовательно, а вызвать сразу подготовку и отправку, или только отправку. При этом стоит понимать, что внутри каждого метода будут вызваны и предыдущие методы тоже. Это необходимо, чтобы предотвратить отправку непроверенных и неподготовленных документов в контролирующие органы.

Если операция Send прошла успешно, черновик будет отправлен и превратится в документооборот, его идентификатор вернется в ответе. 

Асинхронное выполнение методов
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Все три метода имеют флаг deferred, который включает асинхронное выполнение методов.

- Если флаг `deferred = false` (по умолчанию), то вы будете ожидать выполнения операции. 
- Если флаг `deferred = true`, то метод будет выполняться асинхронно. Для выполнения метода будет создана задача (Task). Статус ее выполнения необходимо смотреть по taskId. 

.. note:: Работа с черновиком через задачи является более предпочтительной стратегией, так как невозможно предсказать объем отправляемых пользователем данных. 

Задачи черновиков (Tasks)
~~~~~~~~~~~~~~~~~~~~~~~~~

Некоторые методы могут принимать большие объемы данных. Чтобы не нагружать сервер, а вам не нужно было ждать ответа продолжительное время, перечисленные методы могут переводить работу с данными в режим задач: 

- подписание черновика, 
- проверка,  
- подготовка, 
- отправка,
- печать.

Данные методы возвращают в ответе модель ApiTaskResult. Важно знать id задачи и ее task-state — состояние, которое помогает понять статус выполнения задачи. Вы можете посмотреть все запущенные задачи черновика методом `GET DraftTasks`_. 

Пример работы с Check, Prepare, Send через Tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Запрос Check

.. code-block:: http

    POST /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/d9622b9d-aa31-477b-a399-fc676588bfb5/check?deferred=true HTTP/1.1
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json

Ответ:

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=utf-8

    {
        "id": "c0620f2f-ea43-465a-ab87-96995e0adcf8",
        "task-state": "running",
        "task-type": "urn:task-type:check"
    }

2. Проверка статуса задачи

Запрос `GET TaskId`_:

.. code-block:: http

    GET /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/d9622b9d-aa31-477b-a399-fc676588bfb5/tasks/c0620f2f-ea43-465a-ab87-96995e0adcf8 HTTP/1.1
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json
    Host: extern-api.testkontur.ru

Ответ GET TaskId:

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=utf-8
    Content-Length: 285

    {
        "id": "c0620f2f-ea43-465a-ab87-96995e0adcf8",
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

3. Запрос Prepare

.. code-block:: http

    POST /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/d9622b9d-aa31-477b-a399-fc676588bfb5/prepare?deferred=true HTTP/1.1
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json

Ответ:

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=utf-8

   {
        "id": "02ce6882-2765-457e-aca3-9384f9d3c558",
        "task-state": "running",
        "task-type": "urn:task-type:prepare"
   }

4. Проверка статуса задачи подготовки черновика. 

.. container:: toggle

    .. container:: header

        Ответ GET TaskId:

    .. code-block:: http

        HTTP/1.1 200 OK
        Content-Type: application/json; charset=utf-8

        {
            "id": "02ce6882-2765-457e-aca3-9384f9d3c558",
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

5. Запрос Send

.. code-block:: http

    POST /v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/d9622b9d-aa31-477b-a399-fc676588bfb5/send?deferred=true HTTP/1.1
    Authorization: Bearer <token>
    Accept: application/json
    Content-Type: application/json

Ответ:

.. code-block:: http

    HTTP/1.1 200 OK

    {
        "id": "1ad1ee85-6346-4bb5-88de-c83536a08784",
        "task-state": "running",
        "task-type": "urn:task-type:send"
    }

6. Проверка статуса задачи отправки черновика. 

.. _rst-markup-draftTask:
.. container:: toggle

    .. container:: header

       Ответ GET TaskId:

    .. code-block:: http

        HTTP/1.1 200 OK
        Date: Wed, 22 Apr 2020 14:17:35 GMT
        Content-Type: application/json; charset=utf-8

        {
            "id": "b54a8c6d-e1f1-4e93-841f-9863f6a90aeb",
            "task-state": "succeed",
            "task-type": "urn:task-type:send",
            "task-result": {
                "id": "0c4e50b5-66ac-4a92-b051-3bc95472dddb",
                "organization-id": "988b38f1-5580-4ba9-b9f8-3215e7f392ea",
                "type": "urn:docflow:fns534-report",
                "status": "urn:docflow-common-status:sent",
                "success-state": "urn:docflow-state:neutral",
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
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/0c4e50b5-66ac-4a92-b051-3bc95472dddb/documents/6076f7bc-a016-4d22-bb63-221df6582906/generate-reply?documentType=fns534-report-receipt",
                    "name": "fns534-report-receipt"
                }
                ],
                "send-date": "2020-04-22T17:16:36.1338472",
                "last-change-date": "2020-04-22T14:16:36.1338472Z"
            }
        }

В ответе метода в task-result/id лежит идентификатор созданного документооборота. Работа с черновиком завершена, он отправлен в ФНС. 