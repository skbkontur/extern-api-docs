.. _`Черновики и конструктор черновиков (draftsbuilder)`: https://developer.kontur.ru/doc/extern.drafts
.. _`DELETE Document`: https://developer.kontur.ru/doc/extern.drafts/method?type=delete&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D
.. _`GET Document`: https://developer.kontur.ru/doc/extern.drafts/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D
.. _`PUT Document`: https://developer.kontur.ru/doc/extern.drafts/method?type=put&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D
.. _`POST Document`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments
.. _`GET DocumentContent`: https://developer.kontur.ru/doc/extern.drafts/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fdecrypted-content
.. _`GET EncryptedDocumentContent`: https://developer.kontur.ru/doc/extern.drafts/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fencrypted-content
.. _`GET SignatureContent`: https://developer.kontur.ru/doc/extern.drafts/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignature
.. _`PUT DocumentSignature`: https://developer.kontur.ru/doc/extern.drafts/method?type=put&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures%2F%7BsignatureId%7D
.. _`GET DocumentPrint`: https://developer.kontur.ru/doc/extern.drafts/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fprint
.. _`GET DraftDocumentTask`: https://developer.kontur.ru/doc/extern.drafts/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Ftasks%2F%7BapiTaskId%7D

Методы для работы c документами в черновике
===========================================

Данный раздел посвящен методам, с помощью которых можно работать с документами в черновике. Для работы с этими методами черновик должен быть предварительно создан :doc:`→ </drafts/методы работы с черновиками>`.

Подробная спецификация методов показана в Swagger в разделе `Черновики и конструктор черновиков (draftsbuilder)`_.

.. contents:: Список доступных методов
   :depth: 2

.. _rst-markup-addDocument:

Добавление документа 
--------------------

Метод: `POST Document`_

Допускается добавление документа без подписи. Например, вы не уверены в валидности сформированного xml-файла документа, и чтобы не генерировать лишний раз подпись к нему, хотите сначала его проверить отдельно. И если проверка прошла успешно, то подпись можно отдельно добавить к документу с помощью метода :doc:`Создание подписи к документу</drafts/DraftSignaturesController>`.

Удаление документа 
------------------

Метод: `DELETE Document`_

Получение документа 
-------------------

Метод: `GET Document`_

С помощью данного метода можно получить конкретный документ из черновика, с его мета-информацией и контентами самого документа и подписи, если она уже была добавлена

Редактирование документа 
------------------------

Метод: `PUT Document`_

Используется для добавления каких-либо данных в документ, например, добавление подписи к нему. Если документ с переданным идентификатором не существует, метод создаст его.

Получение подписи под документом 
--------------------------------

Метод: `GET SignatureContent`_


Добавление подписи под документ 
-------------------------------

Метод: `PUT DocumentSignature`_

.. _rst-markup-draft-print:

Печать документа
----------------

Метод: `GET DocumentPrint`_

Метод позволяет получить печатную форму формализованного документа в черновике. Метод поддерживает печать не всех типов документов и контентов. Ограничения, особенности работы метода и пример работы описаны в :doc:`Базе знаний</knowledge base/print>`.

Особенности печати в черновике:

    * Если черновик не отправлен, то документ будет напечатан без штампов.
    * Если черновик отправлен и найден документооборот, то документ будет напечатан как в документообороте — со штампами.

**Параметры запроса**

``deferred`` — флаг :ref:`асинхронного выполнения запроса<rst-markup-print-async>`. Рекомендуется выполнять запрос асинхронно, т.е. использовать флаг в значении true. Если флаг deferred = false или не передан, нужно будет ожидать завершение выполнения запроса. Так как операция печати может быть трудоемкой, вы можете не дождаться ее окончания. 

**Возможные коды ответов**

* 200 OK — печатная форма документа успешно сформирована, результат печати возвращается в виде строки base64.
* 202 Accepted — поставлена задача на печать документа, результат можно получить в методе :ref:`Get DraftDocumentTask<rst-markup-DraftDocumentTask>`.
* 400 documentPrintUnsupported — печать невозможна: тип контента или тип документа не поддерживается.
.. * 400 contentIsTooLarge — превышено ограничение на размер передаваемого контента для синхронного выполнения запроса. Выполните запрос асинхронно, см. описание параметра deferred.

.. _rst-markup-DraftDocumentTask:

Проверка статуса задачи документа черновика по TaskId
-----------------------------------------------------

Метод: `GET DraftDocumentTask`_

Метод возвращает результат выполнения задачи печати, если печать была запущена асинхронно. Если задача успешно выполнена, в ответе вернется идентификатор контента, по которому можно получить печатную форму документа в :doc:`сервисе контентов</contents/content_methods>`.

Получение расшифрованного контента документа (deprecated)
---------------------------------------------------------

Метод: `GET DocumentContent`_

.. attention:: **Метод устарел.** Вместо него используйте :doc:`Сервис контентов</knowledge base/content>`. Идентификатор контента лежит в параметре content-id.

Максимальный размер возвращаемого контента 32 МБ для тестовой и 64 МБ для рабочей площадки.

Получение зашифрованного контента документа (deprecated)
--------------------------------------------------------

Метод: `GET EncryptedDocumentContent`_

.. attention:: **Метод устарел.** Вместо него используйте :doc:`Сервис контентов</knowledge base/content>`. Идентификатор контента лежит в параметре content-id.

Если над черновиком был вызван метод :ref:`Подготовка документов в черновике к отправке<rst-markup-prepare>`, то в черновике появился зашифрованный контент документа, с помощью данного метода его можно получить. Максимальный размер возвращаемого контента 32 МБ для тестовой и 64 МБ для рабочей площадки.
