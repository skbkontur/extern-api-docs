.. _`CreateDraft`: https://developer.testkontur.ru/extern/post-v1-%7BaccountId%7D-drafts
.. _`Add document`: https://developer.testkontur.ru/extern/post-v1-%7BaccountId%7D-drafts-%7BdraftId%7D-documents
.. _`Check`: https://developer.testkontur.ru/extern/post-v1-%7BaccountId%7D-drafts-%7BdraftId%7D-check
.. _`файл отчета ССЧ`: https://developer.testkontur.ru/extern.test.tools/post-test-tools-v1-generate-fuf-ssch
.. _`Add signature`: https://developer.testkontur.ru/extern/post-v1-%7BaccountId%7D-drafts-%7BdraftId%7D-documents-%7BdocumentId%7D-signatures
.. _`SignDraft`: https://developer.testkontur.ru/extern/post-v1-%7BaccountId%7D-drafts-%7BdraftId%7D-cloud-sign
.. _`GET DraftDocument`: https://developer.testkontur.ru/extern/get-v1-%7BaccountId%7D-drafts-%7BdraftId%7D-documents-%7BdocumentId%7D
.. _`GET DraftTasks`: https://developer.testkontur.ru/extern/get-v1-%7BaccountId%7D-drafts-%7BdraftId%7D-tasks
.. _`GET TaskId`: https://developer.testkontur.ru/extern/get-v1-%7BaccountId%7D-drafts-%7BdraftId%7D-tasks-%7BapiTaskId%7D

.. _rst-markup-howtodraft:

Работа с черновиком
===================

В данном разделе мы описали краткий процесс работы с черновиком на примере отчета о среднесписочной численности. Также объясним зачем нужны многочисленные проверки черновика и как работать с задачами (Task). 

.. image:: /_static/howtodraftalg.jpg

**Порядок работы с черновиком:**

    1. `Создание черновика`_.
    2. `Наполнение черновика файлами документов`_.
    3. `Проверка документов`_.
    4. `Наполнение черновика подписями документов`_.
    5. `Проверка, подготовка, отправка черновика с помощью задач`_. 


Создание черновика
------------------

Прежде чем загрузить отчет, нужно создать контейнер, который будет хранить помимо файлов отчета также и метаинформацию о нем. Данный контейнер — это черновик. Чтобы создать его, вызываем метод `CreateDraft`_. В данном методе необходимо передать метаинформацию о налогоплательщике, отправителе и получателе ("payer", "sender", "recipient").  

    - **Payer** — налогоплательщик (НП), организация, за которую отправляется отчетность,
    - **Sender** — отправитель. Организация, которая общается с контролирующими органами, отправляет и получает документы. Payer и Sender могут совпадать.
    - **Recipient** — получатель документооборота, т.е. контролирующий орган (КО). 

При создании черновика нужно передать контент сертификата в формате `base64`, который будет использован пользователем для подписания документов.

.. container:: toggle

    .. container:: header

        **Пример тела запроса метода CreateDraft в формате json:**

    .. code-block:: json

        {
            "sender": {
                "inn": "7757424860",
                "kpp": "680345565", 
                "certificate": { 
                    "content": "MIINFQYJKoZIhvcNAQcCoIINBjCCDQICAQExDDAKB...CzAJ" // контент сертификата в формате base64
                }, 
                "is-representative": "true",
                "ipaddress": "8.8.8.8" 
            },
            "recipient": { 
                "ifns-code": "0087" // работаем на тестовой, поэтому код тестового робота
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

    .. code-block:: json
   
        {    
            "id": "990176b7-f9ba-4b63-8b89-43cf4493b24b", //идентификатор черновика
            "docflows": [],
            "documents": [],
            "meta": { //метаинформация черновика, которая была передана в запросе
                "sender": {
                    "inn": "7757424860",
                    "kpp": "680345565",
                    "name": "Тестовая организация",
                    "certificate": {
                        "content": "тут будет контент выбранного сертификата в формате base64"
                    },
                    "is-representative": true,
                    "ipaddress": "8.8.8.8"
                },
                "recipient": {
                    "ifns-code": "0087"
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
            "links": [ // ссылки, см. ниже
                {
                    "rel": "self",
                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/990176b7-f9ba-4b63-8b89-43cf4493b24b"
                }
            ]
        }

Наполнение черновика файлами документов
---------------------------------------

Черновик необходимо наполнить файлом отчета, приложениями к отчету и подписями. Главный файл отчета — это всегда xml-файл. К отчету могут идти также приложения и другие связанные файлы, например, доверенность. Каждый файл отчета нужно конвертировать в `base64`. Для каждого файла в черновике нужно создавать документ при помощи метода `Add document`_. 

При помощи метода генерации тестовых файлов получим `файл отчета ССЧ`_ в формате xml. Файл необходимо сохранить с именем из тега Файл, параметра ИдФайл. И в названии, и в теге имя файла должно полностью совпадать, см. рисунок.

.. image:: /_static/fileName.png
   :width: 800

Для более гибкой работы с файлами предусмотрена возможность создать пустой документ в черновике, чтобы в дальнейшем методом PUT положить контент файла. В примере мы создаем документ и сразу передаем в него контент файла отчета в формате `base64`. 

**Тело запроса Add document:**

.. code-block:: json
   
   {
    "base64-content": "PD94bWwgdmVyc2lvbj...s5e3yPg0KPC/U4OnrPg=="
   }

Мы намеренно не заполняем метаинформацию об отчете в запросе. Если файл корректный, то метод сам распознает нужную метаинформацию и вернет ее в ответе.

.. container:: toggle

    .. container:: header

        **Ответ Add document:**

    .. code-block:: json
    
        {
            "id": "6ea75127-abc8-4866-b67d-464f1e678273", //идентификатор документа в черновике
            "decrypted-content-link": {
                "rel": "",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/ca50c708-4405-45cb-a594-b9ca7bc1a4ca/documents/6ea75127-abc8-4866-b67d-464f1e678273/decrypted-content"
            },
            "signature-content-link": {
                "rel": "",
                "href": ""
            },
            "description": {
                "filename": "NO_SRCHIS_0007_0007_7757424860680345565_20200129_92425a70-4ac9-4680-bada-3666f0c0514d.xml",
                "content-type": "application/xml",
                "properties": {
                    "Encoding": "windows-1251",
                    "FormName": "Сведения о среднесписочной численности работников за предшествующий календарный год",
                    "КНД": "1110018",
                    "CorrectionNumber": "0",
                    "IsPrintable": "True",
                    "Period": "2012 год",
                    "OriginalFilename": null,
                    "SvdregCode": null,
                    "contentType": "Xml",
                    "AccountingPeriodBegin": "01.01.2012",
                    "AccountingPeriodEnd": "12.31.2012"
                }
            }
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

Под каждым файлом клиент ставит свою подпись, чтобы подтвердить свою личность как отправителя. Если при добавлении документов подпись не была приложена, ее можно добавить к документу отдельно методом `Add signature`_. 

Если у пользователя DSS сертификат, то подписи прикладывать не нужно. Все документы подписываются одним методом `SignDraft`_.

.. warning:: Если документы в черновике изменятся, то подписи станут недействительными.


Порядок работы с подписью
~~~~~~~~~~~~~~~~~~~~~~~~~

    1. Подписываем файл отчета закрытым ключом электронной подписи. 
    2. Конвертируем полученную подпись в base64.
    3. Добавляем подпись в формате base64 в черновик. 

**Тело запроса Add signature:**

.. code-block:: json

   {
    "signature": "MIINFQYJKoZIhvcNAQcCoIINBjCCDQICAQExDDAKB...CzAJ",
   }

После добавления подписи документ черновика будет выглядеть следующим образом:

.. container:: toggle

    .. container:: header

        **Ответ GET DraftDocument:**

    .. code-block:: json
         
        {
            "id": "6ea75127-abc8-4866-b67d-464f1e678273", //идентификатор документа в черновике
            "decrypted-content-link": {
                "rel": "",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/ca50c708-4405-45cb-a594-b9ca7bc1a4ca/documents/6ea75127-abc8-4866-b67d-464f1e678273/decrypted-content"
            },
            "signature-content-link": {
                "rel": "",
                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/ca50c708-4405-45cb-a594-b9ca7bc1a4ca/documents/6ea75127-abc8-4866-b67d-464f1e678273/signature"
            },
            "description": {
                "filename": "NO_SRCHIS_0007_0007_7757424860680345565_20200129_92425a70-4ac9-4680-bada-3666f0c0514d.xml",
                "content-type": "application/xml",
                "properties": {
                    "Encoding": "windows-1251",
                    "FormName": "Сведения о среднесписочной численности работников за предшествующий календарный год",
                    "КНД": "1110018",
                    "CorrectionNumber": "0",
                    "IsPrintable": "True",
                    "Period": "2012 год",
                    "OriginalFilename": null,
                    "SvdregCode": null,
                    "contentType": "Xml",
                    "AccountingPeriodBegin": "01.01.2012",
                    "AccountingPeriodEnd": "12.31.2012"
                }
            }
        }

Мы убедились, что файл отчета корректный, и подпись документа лежит в черновике. Можно переходить к подготовке черновика и отправке. 

Проверка, подготовка, отправка черновика  с помощью задач
---------------------------------------------------------

Перед отправкой отчетности в налоговый орган необходимо прогнать черновик через три метода в строгом порядке: **Check -> Prepare -> Send**. Если хотя бы в одном из методов произошла ошибка, черновик не будет отправлен в налоговый орган. 

Существует возможность не вызывать методы последовательно, а вызвать сразу подготовку и отправку, или только отправку. При этом стоит понимать, что внутри каждого метода будут вызваны и предыдущие методы тоже. Это необходимо, чтобы предотвратить отправку непроверенных и неподготовленных документов к контролирующие органы.

Если операция Send прошла успешно, черновик будет отправлен и превратится в документооборот, его идентификатор вернется в ответе. 

Асинхронное выполнение методов
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Все три метода имеют флаг deferrer, который включает асинхронное выполнение методов.

- Если флаг `deferrer = false` (по умолчанию), то вы будете ожидать выполнения операции. 
- Если флаг `deferrer = true`, то метод будет выполняться асинхронно. Для выполнения метода будет создана задача (Task). Статус ее выполнения необходимо смотреть по taskId. 

.. note:: Работа с черновиком через задачи является более предпочтительным методом, так как мы не можем предсказать объемы отправляемых пользователем данных. 

Задачи черновиков (Tasks)
~~~~~~~~~~~~~~~~~~~~~~~~~

Некоторые методы могут принимать большие объемы данных. Чтобы не нагружать сервер, а вам не нужно было ждать ответа продолжительное время, перечисленные методы могут переводить работу с данными в режим задач: 

- подписание черновика, 
- проверка,  
- подготовка, 
- отправка.

Данные методы возвращают в ответе модель ApiTaskResult. Важно знать id задачи и ее task-state — состояние, которое помогает понять статус выполнения задачи. Вы можете посмотреть все запущенные задачи черновика методом `GET DraftTasks`_. 

Пример работы с Check, Prepare, Send через Tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Запрос Check

::

   https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/74b6e8b9-290a-4d12-b874-c7fb35cad54f/check?deferred=true

Ответ:

.. code-block:: json

   {
    "id": "ce0bfb2a-c5db-4b99-92da-9b332bf1073e",
    "task-state": "running",
    "task-type": "urn:task-type:check"
   }

2. Проверка статуса задачи

Запрос `GET TaskId`_:

::

   https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/74b6e8b9-290a-4d12-b874-c7fb35cad54f/tasks/ce0bfb2a-c5db-4b99-92da-9b332bf1073e

.. container:: toggle

    .. container:: header

        Ответ GET TaskId:

    .. code-block:: json

        {
            "id": "ce0bfb2a-c5db-4b99-92da-9b332bf1073e",
            "task-state": "succeed",
            "task-type": "urn:task-type:check",
            "task-result": {
                "data": {
                    "documents-errors": {
                        "b32171d6-9ebc-4c73-b557-5a203b68f8df": []
                    },
                    "common-errors": []
                }
            }
        }

3. Запрос Prepare

.. code-block:: json

  https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/74b6e8b9-290a-4d12-b874-c7fb35cad54f/prepare?deferred=true

Ответ:

.. code-block:: json

   {
    "id": "02ce6882-2765-457e-aca3-9384f9d3c558",
    "task-state": "running",
    "task-type": "urn:task-type:prepare"
   }

4. Проверка статуса задачи подготовки черновика. 

.. container:: toggle

    .. container:: header

        Ответ GET TaskId:

    .. code-block:: json

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

:: 

  https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/drafts/74b6e8b9-290a-4d12-b874-c7fb35cad54f/send?deferred=true

Ответ:

.. code-block:: json

   {
    "id": "1ad1ee85-6346-4bb5-88de-c83536a08784",
    "task-state": "running",
    "task-type": "urn:task-type:send"
   }

6. Проверка статуса задачи отправки черновика. 

.. container:: toggle

    .. container:: header

       Ответ GET TaskId:

    .. code-block:: json

         {
            "id": "1ad1ee85-6346-4bb5-88de-c83536a08784",
            "task-state": "succeed",
            "task-type": "urn:task-type:send",
            "task-result": {
                "id": "a9bc74bd-311b-43f0-aff7-faba24ce35d9",
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
                    "recipient": "0087",
                    "final-recipient": "0087",
                    "correction-number": 0,
                    "period-begin": "2012-01-01T00:00:00.0000000",
                    "period-end": "2012-12-31T00:00:00.0000000",
                    "period-code": 34,
                    "payer-inn": "7757424860-680345565",
                    "original-draft-id": "74b6e8b9-290a-4d12-b874-c7fb35cad54f"
                },
                "documents": [
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
                    },
                    {
                        "id": "4007e30b-0fb4-4acf-ba11-9ac513f51ca0",
                        "description": {
                            "type": "urn:document:fns534-report-date-confirmation",
                            "filename": "PD_NOSRCHIS_7757424860680345565_7757424860680345565_1BM_20200226_af133042-f8c5-490c-ac5a-54b0e5e0fa9a.xml",
                            "content-type": "application/xml",
                            "decrypted-content-size": 3024,
                            "compressed": true,
                            "requisites": {},
                            "support-recognition": false,
                            "encrypted-certificates": []
                        },
                        "content": {
                            "decrypted": {
                                "rel": "decrypted-content",
                                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/4007e30b-0fb4-4acf-ba11-9ac513f51ca0/decrypted-content"
                            },
                            "docflow-document-contents": [
                                {
                                    "content-id": "8df55933-2cbd-42b2-945c-2a1aa4386ee6",
                                    "encrypted": false,
                                    "compressed": true
                                }
                            ]
                        },
                        "send-date": "2020-02-26T06:51:08.4636938Z",
                        "signatures": [
                            {
                                "id": "f506582c-f228-415b-844e-a78fbb7e645f",
                                "title": "АО \"ПФ \"СКБ Контур\"",
                                "signature-certificate-thumbprint": "A875B626A7D182CDCA85164FC0EF15068487A6EF",
                                "content-link": {
                                    "rel": "content",
                                    "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/4007e30b-0fb4-4acf-ba11-9ac513f51ca0/signatures/f506582c-f228-415b-844e-a78fbb7e645f/content"
                                },
                                "links": [
                                    {
                                        "rel": "self",
                                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/4007e30b-0fb4-4acf-ba11-9ac513f51ca0/signatures/f506582c-f228-415b-844e-a78fbb7e645f/content"
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
                                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/4007e30b-0fb4-4acf-ba11-9ac513f51ca0"
                            },
                            {
                                "rel": "reply",
                                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/4007e30b-0fb4-4acf-ba11-9ac513f51ca0/generate-reply?documentType=fns534-report-receipt",
                                "name": "fns534-report-receipt"
                            },
                            {
                                "rel": "decrypted-content",
                                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/4007e30b-0fb4-4acf-ba11-9ac513f51ca0/decrypted-content"
                            }
                        ]
                    },
                    {
                        "id": "2ad464ce-5348-444b-a1c2-d96c73aa1100",
                        "description": {
                            "type": "urn:document:fns534-report-description",
                            "filename": "TR_DEKL.xml",
                            "content-type": "application/xml",
                            "decrypted-content-size": 366,
                            "compressed": true,
                            "requisites": {},
                            "support-recognition": false,
                            "encrypted-certificates": []
                        },
                        "content": {
                            "decrypted": {
                                "rel": "decrypted-content",
                                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/2ad464ce-5348-444b-a1c2-d96c73aa1100/decrypted-content"
                            },
                            "docflow-document-contents": [
                                {
                                    "content-id": "6a6adf01-c138-48c8-b1fa-432fce4e5c03",
                                    "encrypted": false,
                                    "compressed": true
                                }
                            ]
                        },
                        "send-date": "2020-02-26T06:51:08.4636938Z",
                        "signatures": [],
                        "links": [
                            {
                                "rel": "docflow",
                                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9"
                            },
                            {
                                "rel": "self",
                                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/2ad464ce-5348-444b-a1c2-d96c73aa1100"
                            },
                            {
                                "rel": "decrypted-content",
                                "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/2ad464ce-5348-444b-a1c2-d96c73aa1100/decrypted-content"
                            }
                        ]
                    }
                ],
                "links": [
                    {
                        "rel": "self",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9"
                    },
                    {
                        "rel": "organization",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/organizations/988b38f1-5580-4ba9-b9f8-3215e7f392ea"
                    },
                    {
                        "rel": "web-docflow",
                        "href": "https://setter.testkontur.ru/?inn=662909960905&forward_to_rel=/ft/transmission/state.aspx?key=cfOOHYSO4USxIIRIMEKAL%2fE4i5iAValLufgyFefzkuqKJpsKOwY6TorTSpphojA7vXS8qRsx8EOv9%2fq6JM412Q%3d%3d"
                    },
                    {
                        "rel": "reply",
                        "href": "https://extern-api.testkontur.ru/v1/bd0cd3f6-315d-4f03-a9cc-3507f63265ed/docflows/a9bc74bd-311b-43f0-aff7-faba24ce35d9/documents/4007e30b-0fb4-4acf-ba11-9ac513f51ca0/generate-reply?documentType=fns534-report-receipt",
                        "name": "fns534-report-receipt"
                    }
                ],
                "send-date": "2020-02-26T09:51:08.4636938",
                "last-change-date": "2020-02-26T06:51:08.4636938Z"
            }
        }

В ответе метода в task-result/id лежит идентификатор созданного документооборота. Работа с черновиком завершена, он отправлен в ФНС. 