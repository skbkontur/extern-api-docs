.. _Drafts: http://extern-api.testkontur.ru/swagger/ui/index#/Drafts
.. _`POST Draft`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/Drafts_Create
.. _`DELETE Draft`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/Drafts_DeleteDraft
.. _`GET Draft`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/Drafts_GetDraft
.. _`GET Meta`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/Drafts_GetMeta
.. _`PUT Meta`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/Drafts_UpdateDraftMeta
.. _`POST Check`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/Drafts_Check
.. _`POST Prepare`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/Drafts_Prepare
.. _`POST Send`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/Drafts_Send
.. _`DELETE Document`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/DraftDocuments_DeleteDocument
.. _`GET DocumentAsync`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/DraftDocuments_GetDocumentAsync
.. _`PUT Document`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/DraftDocuments_PutDocument
.. _`GET DocumentPrint`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/DraftDocuments_GetDocumentPrint
.. _`POST Document`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/DraftDocuments_AddDocument
.. _`GET DocumentContent`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/DraftDocuments_GetDocumentContent
.. _`PUT DocumentContent`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/DraftDocuments_PutDocumentContent
.. _`GET EncryptedDocumentContent`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/DraftDocuments_GetEncryptedDocumentContent
.. _`GET SignatureContent`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/DraftDocuments_GetSignatureContent
.. _`PUT DocumentSignature`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/DraftDocuments_PutDocumentSignature
.. _`GET DocumentPrintAsync`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/DraftDocuments_GetDocumentPrintAsync
.. _`POST BuildContentFromFormat-V1`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/DraftDocuments_BuildContentFromFormat
.. _`POST BuildContentFromFormat-V2`: http://extern-api.testkontur.ru/swagger/ui/index#!/Drafts/DraftDocuments_BuildContentFromFormat_0


Методы для работы с черновиками
===============================

Подробная спецификация методов показана в сваггере в разделе Drafts_.

Список доступных методов:

* `Создание черновика`_
* `Удаление черновика`_
* `Получение черновика`_
* `Получение описания черновика`_
* `Редактирование описания черновика`_
* `Проверка документов в черновике`_
* `Подготовка документов в черновике к отправке`_
* `Отправка документов из черновика`_
* `Удаление документа`_
* `Получение документа`_
* `Редактирование документа`_
* `Получение печатной формы документа`_
* `Добавление документа`_
* `Получение расшифрованного контента документа`_
* `Запись контента документа`_
* `Получение зашифрованного контента документа`_
* `Получение подписи под документом`_
* `Добавление подписи под документ`_
* `Печать документа`_
* `Формирование декларации`_

Создание черновика 
^^^^^^^^^^^^^^^^^^

Метод: `POST Draft`_

С помощью этого метода создается черновик с минимально необходимым набором мета-информации, который в будущем можно при необходимости отредактировать или дополнить, используя метод `Редактирование описания черновика`_

Удаление черновика 
^^^^^^^^^^^^^^^^^^

Метод: `DELETE Draft`_

Получение черновика 
^^^^^^^^^^^^^^^^^^^

Метод: `GET Draft`_

В ответ на вызов данного метода можно получить всю актуальную информацию по черновику:

* заполненную на данный момент мета-инфомарцию;
* перечень находящихся в черновике документов;
* статус черновика (новый, проверен, готов к отправке или отправлен).

Если черновик уже был отправлен, то будет ссылка на созданный документооборот.

Получение описания черновика 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `GET Meta`_

Получение только мета-информации черновика.

Редактирование описания черновика 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Метод: `PUT Meta`_

Проверка документов в черновике 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `POST Check`_

Вызовом данного метода можно проверить все документы, находящиеся в черновике. Документы проходят форматно-логические контроли по отдельности, но при наличии нескольких документов в черновике или подписей к документам возможно проведение кросс-проверок, то есть проверок на соответствие документов и подписей между собой.

Подготовка документов в черновике к отправке 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `POST Prepare`_

С помощью данного метода документы подготавливаются к транспортировке их в контролирующий орган: происходит их шифрование и сжатие согласно транспортным протоколам.

Отправка документов из черновика 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `POST Send`_

На выходе данного метода получается документооборот, с которым продолжается работа с помощью методов блока :docs:`Docflow </dc/index>`.

Удаление документа 
^^^^^^^^^^^^^^^^^^
Метод: `DELETE Document`_

Получение документа 
^^^^^^^^^^^^^^^^^^^

Метод: `GET DocumentAsync`_

С помощью данного метода можно получить конкретный документ из черновика, с его мета-информацией и контентами самого документа и подписи, если она уже была добавлена

Редактирование документа 
^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `PUT Document`_

Используется для добавления каких-либо данных в документ, например, добавление подписи к нему.

Получение печатной формы документа 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `GET DocumentPrint`_

Добавление документа 
^^^^^^^^^^^^^^^^^^^^

Метод: `POST Document`_

Допускается добавление документа без подписи. Например, вы не уверены в валидности сформированного xml-файла документа, и чтобы не генерировать лишний раз подпись к нему, хотите сначала его проверить отдельно. И если проверка прошла успешно, то подпись можно отдельно добавить к документу с помощью метода `Добавление подписи под документ`_

Получение расшифрованного контента документа 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `GET DocumentContent`_

Запись контента документа 
^^^^^^^^^^^^^^^^^^^^^^^^^
Метод: `PUT DocumentContent`_

Получение зашифрованного контента документа 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `GET EncryptedDocumentContent`_

Если над черновиком был вызван метод `Подготовка документов в черновике к отправке`_, то в черновике появился зашифрованный контент документа, с помощью данного метода его можно получить

Получение подписи под документом 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `GET SignatureContent`_

Добавление подписи под документ 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `PUT DocumentSignature`_

Печать документа
^^^^^^^^^^^^^^^^

Метод: `GET DocumentPrintAsync`_

Метод позволяет получить печатную форму любого формализованного документа в черновике.

Формирование декларации
^^^^^^^^^^^^^^^^^^^^^^^

Методы: 

* `POST BuildContentFromFormat-V1`_
* `POST BuildContentFromFormat-V2`_

С помощью метода возможно получить xml-файл деклараций по Упрощенной системы налогообложения по ставке 6% и 15%, передав определенный контракт с данными, на основе которых необходимо сформировать декларацию. 

Контракты:

* V1 - :doc:`УСН-6 /_static/usn6-v1.json`, :doc:`УСН-15 /_static/usn15-v1.json`.
* V2 - :doc:`УСН-6 /_static/usn6-v2.json`, :doc:`УСН-15 /_static/usn15-v2.json`.
