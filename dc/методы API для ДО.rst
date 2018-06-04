.. _Docflows: http://extern-api.testkontur.ru/swagger/ui/index#/Docflows
.. _`GET DocflowsAsync`: http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocflowsAsync
.. _`GET DocflowAsync`: http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocflowAsync
.. _`GET DocumentsAsync`: http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocumentsAsync
.. _`GET DocumentAsync`: http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocumentAsync
.. _`GET DocumentDescriptionAsync`: http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocumentDescriptionAsync
.. _`GET EncryptedDocumentContentAsync`: http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetEncryptedDocumentContentAsync
.. _`GET DecryptedDocumentContentAsync`: http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDecryptedDocumentContentAsync
.. _`GET DocumentSignaturesAsync`: http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocumentSignaturesAsync
.. _`GET DocumentSignatureAsync`: http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocumentSignatureAsync
.. _`GET DocumentSignatureContentAsync`: http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocumentSignatureContentAsync
.. _`GET ReplyDocumentAsync`: http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetReplyDocumentAsync
.. _`POST ReplyDocumentAsync`: http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_SendReplyDocumentAsync
.. _`GET DocumentPrintAsync`: http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocumentPrintAsync

Методы для работы с документооборотами
======================================

Подробная спецификация методов показана в сваггере в разделе Docflows_.

Список доступных методов:

* `Получение списка документооборотов`_
* `Получение документооборота`_
* `Получение списка документов документооборота`_
* `Получение документа`_
* `Получение описания документа`_
* `Получение зашифрованного контента документа`_
* `Получение расшифрованного контента документа`_
* `Получение подписей под документом`_
* `Получение конкретной подписи под документом`_
* `Получение контента конкретной подписи под документом`_
* `Генерация ответного документа`_
* `Отправка ответного документа`_
* `Печать документов`_

Получение списка документооборотов 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `GET DocflowsAsync`_

С помощью этого метода можно получить список всех документооборотов учетной записи, при этом можно применить различные фильтры, чтобы получить необходимую выборку интересных на данный момент документооборотов. В ответе получает список документооборотов с необходимой мета-информацией по ним.

Получение документооборота
^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `GET DocflowAsync`_

С помощью этого метода можно получить всю информацию о документообороте, такую как:

* его текущий статус;
* мета-информацию документооборота;
* перечень всех документов, созданных в ходе документооборота, на данный момент;
* и многое другое, полный ответ можно посмотреть в сваггере.

Если текущий статус документооборота подразумевает необходимость отправки ответного документа в контролирующий орган, среди ссылок в ответе этого метода будет ссылка на метод `Генерация ответного документа`_.

Получение списка документов документооборота 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `GET DocumentsAsync`_

С помощью этого метода можно получить данные всех документов, созданных и полученных в ходе документооборота.

Получение документа 
^^^^^^^^^^^^^^^^^^^

Метод: `GET DocumentAsync`_

C помощью этого метода можно получить отдельный документ, созданный или полученный в ходе документооборота, с его описанием и контентами.

Получение описания документа 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `GET DocumentDescriptionAsync`_

Данный метод позволяет отдельно получить описание документа, входящего в документооборот.

Получение зашифрованного контента документа 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `GET EncryptedDocumentContentAsync`_

Получение расшифрованного контента документа 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `GET DecryptedDocumentContentAsync`_

Наличие расшифрованного контента возможно не для всех документов.

Получение подписей под документом 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `GET DocumentSignaturesAsync`_

В некоторых случаях у документа может быть несколько подписей. В ответе будут возвращены все подписи под запрашиваемым документом.

Получение конкретной подписи под документом 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `GET DocumentSignatureAsync`_

В ответе будет мета-инфомарция подписи и ссылка на её контент.

Получение контента конкретной подписи под документом 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `GET DocumentSignatureContentAsync`_

Генерация ответного документа 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `GET ReplyDocumentAsync`_

Документооборот подразумевает под собой последовательный обмен определенными документами согласно регламенту. Поэтому в ответ на получаемые от контролирующего органа документы необходимо отправлять определенные ответные документы. Этот метод помогает формировать подобные документы. Также необходимые ссылки для формирования нужных документов будут появляться в работе с методом `Получение документооборота`_.

Отправка ответного документа 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Метод: `POST ReplyDocumentAsync`_

После работы с методом `Генерация ответного документа`_  полученный в результате документ необходимо подписать, и вместе с подписью направить в контролирующий орган. С помощью этого метода это можно сделать. Также ссылка на этот метод будет в ответе предыдущего метода.

Печать документов 
^^^^^^^^^^^^^^^^^

Метод: `GET DocumentPrintAsync`_

Можно получить печатную форму любого формализованного документа в документообороте. Печать документов происходит только после проверки подписей под печатаемыми документами, тем самым подтверждается валидность и неизменность печатаемых документов.
