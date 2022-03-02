.. _`от 01.07.2021 № 1110`: https://normativ.kontur.ru/document?utm_source=google&utm_medium=organic&utm_referer=www.google.com&utm_startpage=kontur.ru%2Farticles%2F6085&utm_orderpage=kontur.ru%2Farticles%2F6170&moduleId=1&documentId=395805
.. _`сайте налогового органа`: https://www.nalog.gov.ru/rn77/service/traceability/
.. _`от 09.11.2020 № 371-ФЗ`: https://normativ.kontur.ru/document?moduleId=1&documentId=375041&p=1210&utm_source=google&utm_medium=organic&utm_referer=www.google.com&utm_startpage=kontur.ru%2Farticles%2F6085&utm_orderpage=kontur.ru%2Farticles%2F6085
.. _`POST Create draft`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts
.. _`POST AddDocument`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments
.. _`POST Add Signature`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures
.. _`POST Check`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fcheck
.. _`POST Prepare`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fprepare
.. _`POST Send`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fsend
.. _`GET DraftTask`: https://developer.kontur.ru/doc/extern.drafts/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Ftasks%2F%7BapiTaskId%7D
.. _`GET Docflows`: https://developer.kontur.ru/doc/extern.docflows/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows

.. _`PUT ReplyDocumentSignature`: https://developer.kontur.ru/doc/extern.docflows/method?type=put&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D%2Fdocuments%2F%7BdocumentId%7D%2Freplies%2F%7BreplyId%7D%2Fsignature
.. _`POST SendReplyDocument`: https://developer.kontur.ru/doc/extern.docflows/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D%2Fdocuments%2F%7BdocumentId%7D%2Freplies%2F%7BreplyId%7D%2Fsend
.. _`POST SignReplyDocument`: https://developer.kontur.ru/doc/extern.docflows/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D%2Fdocuments%2F%7BdocumentId%7D%2Freplies%2F%7BreplyId%7D%2Fcloud-sign
.. _`POST SignConfirmReplyDocument`: https://developer.kontur.ru/doc/extern.docflows/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D%2Fdocuments%2F%7BdocumentId%7D%2Freplies%2F%7BreplyId%7D%2Fcloud-sign-confirm


Прослеживаемость товаров. РНПТ
==============================

Прослеживаемость товаров – это мера контроля импорта со стороны государства. Контролю подлежат партии товаров, входящих в перечень прослеживаемых согласно постановлению Постановление Правительства РФ `от 01.07.2021 № 1110`_ «Об утверждении перечня товаров, подлежащих прослеживаемости».

Проверить входит ли товар в перечень прослеживаемых, проверить идентификатор товара можно на `сайте налогового органа`_.

Все налогоплательщики, осуществляющие операции с товарами, должны предоставить в налоговый орган отчеты в электронном виде, согласно Федеральному закону `от 09.11.2020 № 371-ФЗ`_.

**Новый реквизит системы прослеживаемости — это РНПТ.**

РНПТ — регистрационный номер партии товара. С его помощью налоговые органы будут прослеживать движение товара. Его нужно указывать в счетах-фактурах, УПД, отчете об операциях и декларации по НДС и во всех новых формах системы прослеживаемости.

**Как получить РНПТ**

1. При ввозе партии товара из стран ЕАЭС, налогоплательщик должен отправить Уведомление о ввозе в течение 5 дней с даты принятия товаров на учет. В ответ, в течение 1 рабочего дня, контролирующий орган отправит квитанцию с присвоенным номером РНПТ.
2. При ввозе партии товара из третьих стран, налогоплательщик формирует номер самостоятельно.
3. Если товар находится у налогоплательщика в остатках, он должен отправить Уведомление об остатках перед тем, как совершить операцию с таким товаром.

**Формы системы прослеживаемости:**

* Уведомление о ввозе (КНД 1169008).
* Уведомление об остатках (КНД 1169011).
* Уведомление о перемещении (КНД 1169009).
* Отчет об операциях с товарами (КНД 1169010).

Алгоритм получения РНПТ на примере формы Уведомление о ввозе
------------------------------------------------------------

.. note:: Для других форм системы прослеживаемости алгоритм аналогичен. Порядок вызова методов не будет отличаться. 

Уведомление о ввозе — это представление, которое отправляется с каждой партией на каждый вид товара. Уведомление о ввозе подают импортёры прослеживаемых товаров из ЕАЭС в Россию и территории под её юрисдикцией в течение 5 дней с даты постановки товаров на учёт. 

:download:`пример файла Уведомления о ввозе <../files/rnpt/ON_UVOSTTOV_0088_0089_6676130154667601001_20210727_e8f5886e_494e.xml>`

Создание и отправка черновика
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Создать черновик: `POST Create draft`_.  Обязательно указать ``ifns-code`` — код ИФНС.
2. Загрузить файл уведомления в Сервис контентов :ref:`POST Upload<rst-markup-post-content>`.
3. Создать документ в черновика `POST AddDocument`_ и указать в ``content-id`` идентификатор из Сервиса контентов. 
4. Приложить подпись к документу `POST Add Signature`_.
5. Когда черновик готов, запускаем последовательность методов: `POST Check`_ -> `POST Prepare`_ -> `POST Send`_ с флагом ``deferred`` равным true. 
6. Результат выполнения методов Check, Prepare, Send нужно проверять в задачах: `GET DraftTask`_.

Если операция Send завершилась успешно, при получении задачи в ответе вернется информация о созданном документообороте типа представление (urn:docflow:fns534-submission). Далее нужно отслеживать данный документооборот и формировать ответные документы согласно :ref:`статусам<rst-markup-submission-status>`. 

Работа с документооборотом представления
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Чтобы завершить работу с документоооборотом нужно:

1. :ref:`Отслеживать статус документооборота<rst-markup-track-docflow-status>`. 

    1. Когда статус документооборота сменится с sent на delivered, это означает, что контролирующий орган отправил Извещение о получении электронного уведомления о ввозе.
    2. Когда статус документооборота сменится на response-arrived, это означает, что контролирующий орган обработал Уведомление о ввозе и отправил либо Квитанцию о приеме, либо Уведомление об отказе.

2. На квитанцию о приеме (или уведомление об отказе) необходимо отправить ответный документ — Извещение о получении. Для этого:

    1. Создать ответный документ :ref:`POST CreateReplyDocument<rst-markup-post-reply-doc>`. В ответе метод вернет информацию о сгенерированном документе и контент квитанции о приеме. 
    2. Подписать квитанцию о приеме при помощи сертификата, установленного на компьютере пользователя. Либо при помощи сертификата методами `POST SignReplyDocument`_ и `POST SignConfirmReplyDocument`_.
    3. Если подпись была сгенерирована на компьютере пользователя, ее нужно приложить к ответному документу методом `PUT ReplyDocumentSignature`_.
    4. Отправить ответный документ методом `POST SendReplyDocument`_.

3. После отправки Извещения о получении статус документооборота сменится на finished. Документооборот завершен. 

Работа с документооборотом требования
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

На основании уведомления о ввозе налоговая присвоит РНПТ на каждую партию товара. Его налоговый орган отправит в требовании с КНД 1184002 не позднее дня, следующего за днём получения уведомления. Алгоритм работы с требованием в API описан в статье :doc:`Требование</knowledge base/demand>`. 

:download:`пример пакета входящего документа<../files/rnpt/пример пакета входящего документа.zip>`

В данном архиве лежат примеры файлов, которые придут от контролирующего органа. Присвоенный номер РНПТ находится в файле  IU_KVREGNOM_6699000000669901001_6699000000669901001_0000_20210629_c5e428db97a2015ee0530afd911111.xml
