.. _`шлюз ФСС`: http://f4.fss.ru/fss/office
.. _`инструкции`: https://www.kontur-extern.ru/support/faq/31/157
.. _`POST Create draft`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts
.. _`POST AddDocument`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments
.. _`POST Add signature`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures
.. _`POST Check`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fcheck
.. _`POST Prepare`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fprepare
.. _`POST Send`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fsend
.. _`GET Docflow`: https://developer.kontur.ru/doc/extern.docflows/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D

Документооборот с ФСС
=====================

.. _rst-markup-dc-fss:

Через API Контур.Экстерна в Фонд социального страхования можно отправить следующие формы отчетности:

  * 4-ФСС (тип документооборота urn:docflow:fss-report). 

Также от Фонда социального страхования через сервис электронного документооборота (СЭДО) можно получать:

  * Извещения ПВСО;
  * Уведомления об изменении статуса ЭЛН. 

  Подробнее про документообороты через СЭДО см. в статье :doc:`Уведомления и извещения СЭДО ФСС</knowledge base/sedo-fss>`.

Создание и отправка черновика по форме 4-ФСС
--------------------------------------------

**Особенности документооборота 4-ФСС**:

* подробное описание документов доступно в `инструкции`_;
* подпись документа передается вместе с содержимым документа;
* в данном виде документооборота нет ответных документов;
* помимо статусов важную роль имеют стадии. Подробное описание представлено в разделе :ref:`спецификация<rst-markup_4fss>`;
* со стороны контролирующего органа отчетность принимает `шлюз ФСС`_, на котором вы можете найти отправленный отчет по его идентификатору.


**Алгоритм работы с черновиком:**

1. Создать черновик: `POST Create draft`_. При создании черновика в теле запроса обязательно указать:

  * в payer параметр registration-number-fss;
  * в recipient параметр fss-code.

2. Загрузить файл отчета по форме 4-ФСС в :doc:`Сервис контентов</contents/content_methods>`.
3. Создать документ в черновике `POST AddDocument`_. При создании указать ссылку на документ в виде идентификатора из Сервиса контентов. 
4. Приложить подпись к документу `POST Add signature`_. 
5. Когда черновик готов, запускаем последовательность методов: `POST Check`_ -> `POST Prepare`_ -> `POST Send`_. Метод ``Prepare`` объединит подпись и документ. 

После отправки отчета требуется дождаться получения квитанции или протокола обработки. Для этого нужно отлеживать статус и стадию документооборота: `GET Docflow`_. Статусы и стадии документооборота по форме 4-ФСС описаны в :ref:`спецификации<rst-markup_4fss>`. 