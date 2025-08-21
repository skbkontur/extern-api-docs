.. _`POST Create draft`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts
.. _`POST Add Document`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments
.. _`POST Add signature`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures 
.. _`POST Check`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fcheck
.. _`POST Prepare`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fprepare
.. _`POST Send`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fsend
.. _`GET Docflow`: https://developer.kontur.ru/doc/extern.docflows/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D
.. _`GET Docflows`: https://developer.kontur.ru/doc/extern.docflows/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows
.. _`GET DraftTask`: https://developer.kontur.ru/doc/extern/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Ftasks%2F%7BapiTaskId%7D 


.. _rst-markup-proactive_algorithm:

Работа с входящими документооборотами
=====================================

.. _rst-markup-sedo-incoming-dc:

Работа с входящими документооборотами от СФР состоит из нескольких этапов:

1. Поиск входящих документооборотов от СФР.
2. Запрос на получение документов в СФР.
3. Отправка ответных документов.

**Особенности документооборотов в СЭДО**

* Для получения документов от СФР нужно выполнить :doc:`подписку оператора на организацию по РНС</scenarios/SFR/FSS/sedo-subscription>`.
* Входящие документообороты от СФР в статусе **received** не содержат документов. Чтобы их получить и поменять статус документооборотов, нужно сформировать запрос на получение документов.
* Все отправляемые в СЭДО документы являются SOAP-запросами.
* Запросы должны быть подписаны подписью в формате :doc:`XMLDsig</manuals/xmldsig>`.

Поиск входящих документооборотов от СФР
---------------------------------------

Найдите входящие документообороты от СФР: :ref:`GET Docflows<rst-markup-get-dcs>`. В запросе укажите фильтр ``type`` и тип нужного ДО согласно :ref:`спецификации<rst-markup_pvso>`, например, ``type=fss-sedo-pvso-notification&type=fss-sedo-sick-report-change-notification&type=fss-sedo-error``.

.. important:: В результатах поиска не будет документооборотов с типами ``fss-sedo-*``, если их тип не был указан в параметре ``type``.

Новые документообороты будут отображаться в статусе **received**. Для получения документов и смены статуса ДО нужно отправить запрос на получение документов от СФР. Далее работайте с каждым ДО по отдельности.

Запрос на получение документов от СФР
-------------------------------------

Если в веб-интерфейсе Контур.Экстерн, в Реквизитах плательщика выбран способ получения входящих документов из СЭДО автоматически с помощью сертификата оператора, то запросы на получения документов через API отправлять не нужно. Входящие документы автоматически будут подгружены в документообороты и в них будут ссылки на reply.

В остальных случаях для получения документов от СФР нужно сформировать, подписать и отправить запрос. Для этого используйте :ref:`методы генерации запроса в СЭДО СФР<rst-markup-sedo>`:

1. Создайте запрос на получение документов от СФР: :ref:`POST GenerateDocumentsRequest<rst-markup-sedo>`. В запросе укажите id найденного входящего документооборота. В ответе метод вернет шаблон запроса и хэш для подписи.
2. Подпишите хэш, который вернется в параметре ``DataToSign`` в формате byte[].
3. Добавьте необработанную подпись к запросу: :ref:`PUT SaveDocumentsRequestSignature<rst-markup-sedosavedocuments>`.
4. Отправьте запрос на получение документов в СФР: :ref:`POST SendDocumentsRequest<rst-markup-sedosavedocuments>`.

Когда СФР обработает запрос, он отправит запрошенный документ и статус ДО поменяется:

1. Для следующих документооборотов документы появятся только во входящих ДО: 

    * urn:docflow:fss-sedo-pvso-notification – извещение ПВСО;
    * urn:docflow:fss-sedo-sick-report-change-notification – уведомление об изменении статуса ЭЛН;
    * urn:docflow:fss-sedo-demand – требование СФР.

Статус ДО поменяется на **response-arrived**. Для данных документооборотов **потребуется отправка ответных документов**: "Отметка о прочтении" и "Извещение о прочтении".

2. Для остальных входящих документооборотов статус поменяется на **response-arrived**. Документы будут только во входящем ДО. Для данных документооборотов **потребуется отправка ответного документа** "Отметка о прочтении".

.. note:: Рекомендуем для дальнейшей работы каждый документооборот вычитать отдельно методом :ref:`GET Docflow<rst-markup-get-dc>`.

.. _rst-markup-reply-docs: 

Отправка ответных документов
----------------------------

Отметка о прочтении
~~~~~~~~~~~~~~~~~~~

1. Найдите в поле ``documents`` полученного ДО документ с соответствующим типом:

.. csv-table:: 
   :header: "Документооборот", "Тип документа"
   :widths: 28 30

   "urn:docflow:fss-warrant-management", "urn:document:fss-warrant-management-response-message"
   "urn:docflow:fss-sedo-proactive-payments-reply", "urn:document:fss-sedo-proactive-payments-reply-response-result"
   "urn:docflow:fss-sedo-insured-person-registration", "urn:document:urn:document:fss-sedo-insured-person-registration-response-result"
   "urn:docflow:fss-sedo-benefit-payment-initiation", "urn:document:fss-sedo-benefit-payment-initiation-result-document"
   "urn:docflow:fss-sedo-demand-reply", "urn:document:fss-sedo-demand-reply-result-document"
   "urn:docflow:fss-sedo-billing-information-demand", "urn:document:fss-sedo-billing-information-demand-result-document"
   "urn:docflow:fss-sedo-baby-care-vacation-close-notice", "urn:document:fss-sedo-baby-care-vacation-close-notice-result-document"
   "urn:docflow:fss-sedo-pvso-notification", "urn:document:fss-sedo-pvso-notification-notification-message"
   "urn:docflow:fss-sedo-sick-report-change-notification", "urn:document:fss-sedo-sick-report-change-notification-notification-message"
   "urn:docflow:fss-sedo-insured-person-mismatch", "urn:document:fss-sedo-insured-person-mismatch-mismatch-message"
   "urn:docflow:fss-sedo-proactive-payments-benefit", "urn:document:fss-sedo-proactive-payments-benefit-benefit-message"
   "urn:docflow:fss-sedo-proactive-payments-demand", "urn:document:fss-sedo-proactive-payments-demand-demand-message"
   "urn:docflow:fss-sedo-demand", "urn:document:fss-sedo-demand-message"
   "urn:docflow:fss-sedo-billing-information", "urn:document:fss-sedo-billing-information-message"
   "urn:docflow:fss-sedo-employee-salary-information", "urn:document:fss-sedo-employee-salary-information-result-document"
   "urn:docflow:fss-sedo-benefit-payment-status-notice", "urn:document:fss-sedo-benefit-payment-status-notice-benefit-status-notice-message"
   "urn:docflow:fss-sedo-proactive-process-events-notification", "urn:document:fss-sedo-proactive-process-events-notification-proactive-process-events-notification-message"
   "urn:docflow:fss-sedo-proactive-expire-notice", "urn:document:fss-sedo-proactive-expire-notice-document"
   "urn:docflow:fss-sedo-appeal", "urn:document:fss-sedo-appeal-document"
   "urn:docflow:fss-sedo-appeal-reply", "urn:document:fss-sedo-appeal-reply-result-document"
   "urn:docflow:fss-sedo-oved-confirmation", "urn:document:fss-sedo-oved-confirmation-result-document"
   "urn:docflow:fss-sedo-disability-children-demand", "urn:document:fss-sedo-disability-children-demand-result-document"
   "urn:docflow:fss-sedo-payment-details-demand", "urn:document:fss-sedo-payment-details-demand-document"
   "urn:docflow:fss-sedo-payment-details-demand-reply", "urn:document:fss-sedo-payment-details-demand-reply-result-document"
   "urn:docflow:fss-sedo-additional-vacation-statement", "urn:document:fss-sedo-additional-vacation-statement-result-document"
   "urn:docflow:fss-sedo-additional-vacation-statement-need-doc", "urn:document:fss-sedo-additional-vacation-statement-need-doc-document"
   "urn:docflow:fss-sedo-additional-vacation-statement-docs", "urn:document:fss-sedo-additional-vacation-statement-docs-result-document"

2. Чтобы получить файл документа, возьмите идентификатор ``content-id`` в метаинформации документа, в модели ``docflow-document-contents`` и скачайте документ из :ref:`Сервиса контентов<rst-markup-dowload>`.

3. Создайте ответный документ «Отметка о прочтении» к полученным документам. Это можно сделать несколькими способами:

    a. Сгенерирйте ответный документ: :ref:`POST CreateReplyDocument<rst-markup-post-reply-doc>`. Используйте идентификатор найденного документа для поля ``documentId``. Укажите в поле ``documentType`` тип документа для нужного ДО из таблицы ниже.
    b. Перейдите по ссылке из поля ``links`` в параметре ``rel``, содержащей тип нужного ответного документа. 

    Типы ответных документов для генерации отметки о прочтении:

.. csv-table:: 
    :header: "Тип входящего документа", "Тип ответного документа"
    :widths: 20 30
    
    "urn:document:fss-warrant-management-response-message", "urn:document:fss-warrant-management-response-read-receipt"
    "urn:document:fss-sedo-proactive-payments-reply-response-result", "urn:document:fss-sedo-proactive-payments-reply-read-receipt"
    "urn:document:urn:document:fss-sedo-insured-person-registration-response-result", "urn:document:fss-sedo-insured-person-registration-read-receipt"
    "urn:document:fss-sedo-benefit-payment-initiation-result-document", "urn:document:fss-sedo-benefit-payment-initiation-read-receipt"
    "urn:document:fss-sedo-demand-reply-result-document", "urn:document:fss-sedo-demand-reply-read-receipt"
    "urn:document:fss-sedo-billing-information-demand-result-document", "urn:document:fss-sedo-billing-information-demand-read-receipt"
    "urn:document:fss-sedo-baby-care-vacation-close-notice-result-document", "urn:document:fss-sedo-baby-care-vacation-close-notice-read-receipt"
    "urn:document:fss-sedo-pvso-notification-notification-message", "urn:document:fss-sedo-pvso-notification-receipt"
    "urn:document:fss-sedo-sick-report-change-notification-notification-message", "urn:document:fss-sedo-sick-report-change-notification-receipt"
    "urn:document:fss-sedo-insured-person-mismatch-mismatch-message", "urn:document:fss-sedo-insured-person-mismatch-receipt-receipt"
    "urn:document:fss-sedo-proactive-payments-benefit-benefit-message", "urn:document:fss-sedo-proactive-payments-benefit-receipt"
    "urn:document:fss-sedo-proactive-payments-demand-demand-message", "urn:document:fss-sedo-proactive-payments-demand-receipt"
    "urn:document:fss-sedo-demand-message", "urn:document:fss-sedo-demand-read-receipt"
    "urn:document:fss-sedo-billing-information-message", "urn:document:fss-sedo-billing-information-read-receipt"
    "urn:document:fss-sedo-benefit-payment-status-notice-benefit-status-notice-message", "urn:document:fss-sedo-benefit-payment-status-notice-receipt"
    "urn:document:fss-sedo-proactive-process-events-notification-proactive-process-events-notification-message", "urn:document:fss-sedo-proactive-process-events-notification-read-receipt"
    "urn:document:fss-sedo-proactive-expire-notice-document", "urn:document:fss-sedo-proactive-expire-notice-read-receipt"
    "urn:document:fss-sedo-appeal-document", "urn:document:fss-sedo-appeal-read-receipt"
    "urn:document:fss-sedo-appeal-reply-result-document", "urn:document:fss-sedo-appeal-reply-read-receipt"
    "urn:document:fss-sedo-oved-confirmation-result-document", "urn:document:fss-sedo-oved-confirmation-read-receipt"
    "urn:document:fss-sedo-disability-children-demand-result-document", "urn:document:fss-sedo-disability-children-demand-read-receipt"
    "urn:document:fss-sedo-payment-details-demand-document", "urn:document:fss-sedo-payment-details-demand-read-receipt"
    "urn:document:fss-sedo-payment-details-demand-reply-result-document", "urn:document:fss-sedo-payment-details-demand-reply-read-receipt"
    "urn:document:fss-sedo-additional-vacation-statement-result-document", "urn:document:fss-sedo-additional-vacation-statement-read-receipt"
    "urn:document:fss-sedo-additional-vacation-statement-need-doc-document", "urn:document:fss-sedo-additional-vacation-statement-need-doc-read-receipt"
    "urn:document:fss-sedo-additional-vacation-statement-docs-result-document", "urn:document:fss-sedo-additional-vacation-statement-docs-read-receipt"

Подписывать «Отметку о прочтении» не нужно.

4. Отправьте ответный документ: :ref:`POST SendReplyDocument<rst-markup-sendreply>`. После отправки отметки о прочтении статус документооборота поменяется на **finished**.

Извещение о прочтении
~~~~~~~~~~~~~~~~~~~~~

Помимо отметки о прочтении для документооборотов urn:docflow:fss-sedo-pvso-notification, urn:docflow:fss-sedo-sick-report-change-notification и urn:docflow:fss-sedo-demand нужно дополнительно создать, подписать и отправить в СФР ответный документ "Извещение о прочтении". 

1. Создайте ответный документ. Это можно сделать несколькими способами:

    a. Сгенерируйте ответный документ: :ref:`POST CreateReplyDocument<rst-markup-post-reply-doc>`. При запросе указывает в поле ``documentType`` тип документа, который имеет вид ``fss-sedo-*-receipt-notification-message``, где * - наименование документооборота.

    b. Перейдите по ссылке из поля ``links`` в параметре ``rel``, содержащей тип нужного ответного документа. 

2. Возьмите контент подписи из метаинформации созданного документа в параметре ``data-to-sign``.
3. Подпишите эти данные необработанной (raw) подписью.
4. Добавьте подпись к ответному документу: :ref:`PUT ReplyDocumentSignature<rst-markup-repliSignature>`.
5. Отправьте ответный документ: :ref:`POST SendReplyDocument<rst-markup-sendreply>`. После отправки отметки о прочтении  статус документооборота поменяется на **finished**. 

Результат принятия извещения о прочтения появится в текущем и во входящем документообороте urn:docflow:fss-sedo-receipt-notification-result – результат подтверждения прочтения.

Работа с ошибками
-----------------

Если в ходе документооборота с СЭДО СФР появится ошибка, то она может поступить в виде документа в исходном ДО. В этом случае статус документооборота поменяется на **finished**. Типы документов об ошибке будут иметь вид ``fss-sedo-*-exchange-error``, где * - :ref:`наименование документооборота<rst-markup-typedocumentFSS>`. 


Тестирование сценариев
----------------------

Если для тестирования вы используете сертификаты Контура, то они уже готовы для работы с СЭДО. Если вы используете другие сертификаты, то сертификаты удостоверяющих центров должны быть добавлены в список доверенных сертификатов со стороны СФР. 

Для удобства тестирования сценариев работы в СЭДО СФР используйте коллекцию Postman: 

:download:`Коллекция Postman для работы с входящими документооборотами </files/sedo/Работа_с_входящими_документооборотами_postman_collection.json>`.



