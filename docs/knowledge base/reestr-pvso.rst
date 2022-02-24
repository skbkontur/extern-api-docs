.. _`POST Create draft`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts
.. _`POST AddDocument`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments
.. _`POST Add signature`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures 
.. _`POST Check`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fcheck
.. _`POST Prepare`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fprepare
.. _`POST Send`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fsend
.. _`GET Docflow`: https://developer.kontur.ru/doc/extern.docflows/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D
.. _`GET Docflows`: https://developer.kontur.ru/doc/extern.docflows/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows
.. _`портале ФСС`: http://portal.fss.ru/fss/analytics/gate/error-description
.. _`спецификации ФСС`: http://fz122.fss.ru/doc/reglrest.pdf
.. _`GET DraftTask`: https://developer.kontur.ru/doc/extern.drafts/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Ftasks%2F%7BapiTaskId%7D 

Реестр ПВСО
===========

Что такое реестр ПВСО
---------------------

Реестр прямых выплат социального обеспечения работодатель направляет в ФСС для назначения и выплаты пособия в рамках схемы прямых выплат. Отправка реестра ПВСО сохраняется и в новой схеме :doc:`проактивных выплат</knowledge base/proactiv>`. Она действует с 1 января 2022 года.  

Порядок работы с реестрами и размер пособий не меняется. Работодатель по-прежнему вносит сведения в реестр ПВСО и направляет его в течение 5 рабочих дней в ФСС. Региональное отделение ФСС назначает и выплачивает пособие сотруднику в течение 10 календарных дней с момента получения реестра. Пособие за первые три дня назначает и выплачивает работодатель, удерживая НДФЛ. Остальную часть сотрудник получает от ФСС, поэтому с нее НДФЛ удерживает ФСС. 

Для компаний с численностью сотрудников более 25 человек отправка реестра ПВСО происходит в электронном виде с использованием электронно-цифровой подписи. Сведения направляются в xml-формате через портал ФСС.

Алгоритм работы с реестрами ПВСО
--------------------------------

**Особенности документооборота:**

    * подпись документа передается вместе с содержимым документа;
    * в данном виде документооборота нет ответных документов;
    * у документооборота нет статусов. Необходимо работать со стадиями и статусами стадий;
    * стадии документооборота и статусы стадий аналогичны стадиям 4-ФСС и описаны в :ref:`спецификации<rst-markup_4fss>`;
    * наименование подписанного реестра должно соответствовать :ref:`спецификации ФСС<rst-markup-name-reestr-pvso>`.

**Как отправить реестр ПВСО**

    1.  Создайте черновик: `POST Create draft`_. При создании черновика в теле запроса обязательно укажите:

        * в ``payer`` параметр ``registration-number-fss``;
        * в ``recipient`` параметр ``fss-code``.

    2. Загрузите файл реестра в :doc:`Сервис контентов</contents/content_methods>`.
    3. Создайте документ в черновике: `POST AddDocument`_. При создании укажите ссылку на документ в виде идентификатора из :doc:`Сервиса контентов</contents/content_methods>`.
    4. Приложите подпись к документу: `POST Add signature`_.
    5. Когда черновик готов, запустите последовательность методов: `POST Check`_ -> `POST Prepare`_ -> `POST Send`_. Метод ``Prepare`` объединит подпись и документ.
    6. Проверьте результат выполнения методов Check, Prepare, Send в задачах: `GET DraftTask`_.

**Как отслеживать документооборот**

    1. Найдите документооборот: `GET Docflows`_. В запросе укажите фильтр: ``type=fss-sick-report``.

    .. note:: Результатов поиска не будет, если использовать в запросе параметры ``updatedFrom`` и ``updatedTo``.

    2. Запросите документооборот по идентификатору: `GET Docflow`_.

**Как получить результат обработки реестра ПВСО**

Результат документооборота можно определить по :ref:`стадиям и их статусам<rst-markup_4fss>`. Для этого проверьте поле ``description`` и параметры ``fss-stage-type`` и ``fss-stage-status``:

1. Если стадия **FormingReceipt** имеет статус **success**, поле ``documents`` будет содержать документ с типом urn:document:fss-sick-report-receipt.

2. Если любая из стадий имеет статус **error**:

    * параметр ``fss-stage-error-code`` вернет код ошибки. Все коды ошибок представлены на `портале ФСС`_;
    * параметр ``fss-stage-error-extend`` вернет описание ошибки в html-формате;
    * поле ``documents``  будет содержать документы с типами urn:document:fss-sick-report-error или urn:document:fss-sick-report-error-receipt.

Чтобы скачать документ, воспользуйтесь :doc:`Сервисом контентов</contents/content_methods>`. Идентификатор документа смотрите в параметрах ``docflow-document-contents`` -> ``content-id``.



