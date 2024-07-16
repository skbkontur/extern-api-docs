.. _`кода ОКПО`: https://www.b-kontur.ru/profi/okpo-po-inn-ili-ogrn
.. _`POST Create draft`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts
.. _`POST Add document`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments
.. _`POST Add signature`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures
.. _`POST Check`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fcheck
.. _`POST Prepare`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fprepare
.. _`POST Send`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fsend
.. _`GET Docflow`: https://developer.kontur.ru/doc/extern.docflows/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D

Письма в Росстат
================

Особенности документооборота
----------------------------

1. В черновике письма в Росстат при добавлении документа нужно в обязательном порядке указывать тип этого документа. Причина проста: письмо в Росстат — это .txt, к нему могут идти любые приложения (например, тоже .txt).
2. Для отправки письма в Росстат обязательно указание `кода ОКПО`_ — это реквизит организации, который присваивает орган государственной статистики при регистрации. 
3. Для уполномоченных представителей в рамках документооборота с ТОГС не предусмотрена отправка доверенности, поэтому дополнительно прикладывать файл Сообщения о представительстве не нужно.  
4. В спецификации есть актуальная информация по :ref:`статусам документооборотов<rst-markup-stat-letter-status>` и по :ref:`типам документов<rst-markup-stat-letter-documents>`. Ответных документов в данном документообороте нет. 

Алгоритм работы с методами API
------------------------------

Алгоритм работы с черновиком:

1. Создать черновик: `POST Create draft`_. При создании черновика в теле запроса обязательно указать:

    * ``subject`` — тему письма,
    * ``okpo`` – код ОКПО,
    * и если это ответ на входящее письмо из Росстат, то передать в ``related-docflow-id`` идентификатор входящего документооборота (передавать в related-document-id идентификатор главного документа при этом не нужно). 

2. Создать документ с указанием типа: `POST Add document`_. :ref:`Типы документов для писем в Росстат<rst-markup-stat-letter-documents>`.
3. Приложить подпись к каждому документу: `POST Add signature`_.
4. Когда черновик готов, запускаем последовательность методов:  `POST Check`_ -> `POST Prepare`_ -> `POST Send`_. 

Далее нужно отлеживать статус документооборота: `GET Docflow`_.
