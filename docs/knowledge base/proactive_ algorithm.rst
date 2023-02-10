.. _`POST Create draft`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts
.. _`POST Add Document`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments
.. _`POST Add signature`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures 
.. _`POST Check`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fcheck
.. _`POST Prepare`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fprepare
.. _`POST Send`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fsend
.. _`GET Docflow`: https://developer.kontur.ru/doc/extern.docflows/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D
.. _`GET Docflows`: https://developer.kontur.ru/doc/extern.docflows/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows
.. _`GET DraftTask`: https://developer.kontur.ru/doc/extern/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Ftasks%2F%7BapiTaskId%7D 



Алгоритм работы с методами в проактивных выплатах
=================================================

Особенности документооборотов в СЭДО
------------------------------------

* Для получения документов от ФСС нужно выполнить :doc:`подписку оператора на организацию по РНС</knowledge base/sedo-subscription>`.
* Входящие документообороты от ФСС в статусе **received** не содержат документов. Чтобы их получить и поменять статус документооборотов, нужно сформировать запрос на получение документов.
* Все отправляемые в СЭДО документы являются SOAP-запросами.
* Запросы должны быть подписаны подписью в формате :doc:`XMLDsig</manuals/xmldsig>`.
* Результат приема отчета "Сведения о застрахованном лице" нужно смотреть в документе "Результат регистрации сведений о застрахованных лицах" (urn:document:fss-sedo-insured-person-registration-result-response-result) по каждому СНИЛС отдельно.
* В проактивных выплатах сохраняется отправка :doc:`реестров ПВСО</knowledge base/reestr-pvso>`, подробнее о порядке взаимодействия с ФСС читайте в статье :doc:`Проактивные выплаты</knowledge base/proactiv>`.

Работа с исходящими документооборотами
--------------------------------------

В схеме проактивных выплат работодатель направляет в ФСС следующие исходящие документообороты:
    
    * urn:docflow:fss-sedo-insured-person-registration – сведения о застрахованных лицах;
    * urn:docflow:fss-sedo-proactive-payments-reply – ответ на запрос проверки, подтверждения, корректировки сведений проактивной выплаты страхового обеспечения;
    * urn:docflow:fss-sedo-benefit-payment-initiation – инициация выплат пособия;
    * urn:docflow:fss-warrant-management – запрос на регистрацию и отзыв доверенности ФСС;
    * urn:docflow:fss-sedo-demand-reply – ответ на требование ФСС;
    * urn:docflow:fss-sedo-billing-information-demand – запрос на формирование справки о расчетах ФСС.

Далее для каждого документооборота создайте черновик и отправьте его. 

**Создание и отправка черновика**

1. Создайте черновик: :ref:`POST Create draft<rst-markup-createdraft>`. При создании черновика в теле запроса обязательно укажите:
    
    a. в ``payer`` параметр ``registration-number-fss``;
    b. в ``recipient`` параметр ``fss-code``.
    
    Для формирования МЧД в ``payer`` укажите следующие параметры:

    c. ``ogrn`` – ОГРН, заполняется юридическими лицами и индивидуальными предпринимателями;
    d. ``snils`` – СНИЛС, заполняется индивидуальными предпринимателями и физическими лицами. 

2. Загрузите файл документа в :ref:`Сервис контентов<rst-markup-load>`.
3. Создайте документ в черновике: :ref:`POST Add Document<rst-markup-addDocument>`. При создании укажите ссылку на документ в виде идентификатора из :ref:`Сервиса контентов<rst-markup-load>`.
4. Возьмите идентификатор контента для подписания из метаинформации ответа метода ``Add Document`` в поле ``data-to-sign-content-id`` и получите данные через :ref:`Сервис контентов<rst-markup-dowload>`. 
5. Подпишите эти данные необработанной (raw) подписью. 
6. Приложите подпись к документу: :ref:`POST Add signature<rst-markup-AddSignature>`.
7. Когда черновик готов, запустите последовательность методов: :ref:`POST Check<rst-markup-check>` -> :ref:`POST Prepare<rst-markup-prepare>` -> :ref:`POST Send<rst-markup-send>`. Укажите флаг ``deferred = true`` для отложенного выполнения задач. 
8. Проверьте статус выполнения задач для методов ``Check``, ``Prepare``, ``Send``: :ref:`GET DraftTask<rst-markup-DraftTasks>`. Если запрос по методу ``Send`` завершился успешно, то в ответе вернется информация о созданном документообороте (ДО).

В рамках проактивных выплат ДО считается завершенным после отправки черновика. Когда ФСС обработает данные, отправит документ с результатом обработки или приема сообщения. На него нужно отправить ответный документ "Отметка о прочтении". О том, как сформировать и отправить отметку о прочтении читайте в разделе :ref:`Отправка ответных документов<rst-markup-reply-docs>`.  

Для каждого документооборота поступит соответствующий входящий документооборот от ФСС. Документы отобразятся в исходящем и входящем ДО. 

.. _rst-markup-sedo-incoming-dc:

Работа с входящими документооборотами от ФСС
--------------------------------------------

Работа с входящими документооборотами от ФСС состоит из нескольких этапов:

1. Поиск входящих документооборотов от ФСС.
2. Запрос на получение документов в ФСС.
3. Отправка ответных документов.

Поиск входящих документооборотов от ФСС
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Найдите входящие документообороты от ФСС: :ref:`GET Docflows<rst-markup-get-dcs>`. В запросе укажите фильтр ``type`` и тип нужного ДО согласно :ref:`спецификации<rst-markup-cbrf>`, например, ``type=fss-sedo-pvso-notification&type=fss-sedo-sick-report-change-notification&type=fss-sedo-error``.

.. important:: В результатах поиска не будет документооборотов с типами ``fss-sedo-*``, если их тип не был указан в параметре ``type``.

Новые документообороты будут отображаться в статусе **received**. Для получения документов и смены статуса ДО нужно отправить запрос на получение документов от ФСС. Далее работайте с каждым ДО по отдельности.

Запрос на получение документов от ФСС
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Для получения документов от ФСС нужно сформировать, подписать и отправить запрос. Для этого используйте :ref:`методы генерации запроса в СЭДО ФСС<rst-markup-sedo>`:

1. Создайте запрос на получение документов от ФСС: :ref:`POST GenerateDocumentsRequest<rst-markup-sedo>`. В запросе укажите id найденного входящего документооборота. В ответе метод вернет шаблон запроса и хэш для подписи.
2. Подпишите хэш, который вернется в параметре ``DataToSign`` в формате byte[].
3. Добавьте необработанную подпись к запросу: :ref:`PUT SaveDocumentsRequestSignature<rst-markup-sedosavedocuments>`.
4. Отправьте запрос на получение документов в ФСС: :ref:`POST SendDocumentsRequest<rst-markup-sedosavedocuments>`.

Когда ФСС обработает запрос, он отправит запрошенный документ и статус ДО поменяется:

1. Для следующих документооборотов документы появятся во входящих ДО:

    * urn:docflow:fss-sedo-insured-person-registration-result – результат регистрации сведений о застрахованном лице;
    * urn:docflow:fss-sedo-proactive-payments-reply-result – результат обработки ответа на запрос проверки;
    * urn:docflow:fss-warrant-management-result – результат создания или отзыва доверенности ФСС;
    * urn:docflow:fss-sedo-demand-reply-result – резульат ответа на требование ФСС;
    * urn:docflow:fss-sedo-billing-information-demand-result – результат обработки запроса справки о расчетах ФСС.

Документы также отобразятся в соответствующих исходящих документооборотах. 

Статус ДО поменяется на **finished** и **они будут считаться завершенными**.

2. Для следующих документооборотов документы появятся только во входящих ДО: 

    * urn:docflow:fss-sedo-pvso-notification – извещение ПВСО;
    * urn:docflow:fss-sedo-sick-report-change-notification – уведомление об изменении статуса ЭЛН;
    * urn:docflow:fss-sedo-demand – требование ФСС.

Статус ДО поменяется на **response-arrived**. Для данных документооборотов **потребуется отправка ответных документов**: "Отметка о прочтении" и "Извещение о прочтении".

3. Для остальных входящих документооборотов статус поменяется на **response-arrived**. Документы будут только во входящем ДО. Для данных документооборотов **потребуется отправка ответного документа** "Отметка о прочтении".

.. note:: Рекомендуем для дальнейшей работы каждый документооборот вычитать отдельно методом :ref:`GET Docflow<rst-markup-get-dc>`.

.. _rst-markup-reply-docs: 

Отправка ответных документов
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Отметка о прочтении**

1. Найдите в поле ``documents`` полученного ДО документ с соответствующим типом:

.. csv-table:: 
   :header: "Документооборот", "Тип документа"
   :widths: 28 30

   "urn:docflow:fss-sedo-pvso-notification", "urn:document:fss-sedo-pvso-notification-notification-message"
   "urn:docflow:fss-sedo-sick-report-change-notification", "urn:document:fss-sedo-sick-report-change-notification-notification-message"
   "urn:docflow:fss-sedo-insured-person-mismatch", "urn:document:fss-sedo-insured-person-mismatch-mismatch-message"
   "urn:docflow:fss-sedo-proactive-payments-benefit", "urn:document:fss-sedo-proactive-payments-benefit-benefit-message"
   "urn:docflow:fss-sedo-proactive-payments-demand", "urn:document:fss-sedo-proactive-payments-demand-demand-message"
   "urn:docflow:fss-sedo-insured-person-registration", "urn:document:urn:document:fss-sedo-insured-person-registration-response-result"
   "urn:docflow:fss-sedo-proactive-payments-reply", "urn:document:fss-sedo-proactive-payments-reply-response-result"
   "urn:docflow:fss-sedo-benefit-payment-initiation", "urn:document:fss-sedo-benefit-payment-initiation-result-document"
   "urn:docflow:fss-warrant-management", "urn:document:fss-warrant-management-response-message"
   "urn:docflow:fss-sedo-demand", "urn:document:fss-sedo-demand-message"
   "urn:docflow:fss-sedo-demand-reply", "urn:document:fss-sedo-demand-reply-result-document"
   "urn:docflow:fss-sedo-billing-information-demand", "urn:document:fss-sedo-billing-information-demand-result-document"
   "urn:docflow:fss-sedo-billing-information", "urn:document:fss-sedo-billing-information-message"

2. Чтобы получить файл документа, возьмите идентификатор ``content-id`` в метаинформации документа, в модели ``docflow-document-contents`` и скачайте документ из :ref:`Сервиса контентов<rst-markup-dowload>`.

3. Создайте ответный документ «Отметка о прочтении» к полученным документам. Это можно сделать несколькими способами:

    a. Сгенерирйте ответный документ: :ref:`POST CreateReplyDocument<rst-markup-post-reply-doc>`. Используйте идентификатор найденного документа для поля ``documentId``. Укажите в поле ``documentType`` тип документа для нужного ДО из таблицы ниже.
    b. Перейдите по ссылке из поля ``links`` в параметре ``rel``, содержащей тип нужного ответного документа. 

    Типы ответных документов для генерации отметки о прочтении:

.. csv-table:: 
    :header: "Тип входящего документа", "Тип ответного документа"
    :widths: 20 30
    
    "urn:document:fss-sedo-pvso-notification-notification-message", "urn:document:fss-sedo-pvso-notification-receipt"
    "urn:document:fss-sedo-sick-report-change-notification-notification-message", "urn:document:fss-sedo-sick-report-change-notification-receipt"
    "urn:document:fss-sedo-insured-person-mismatch-mismatch-message", "urn:document:fss-sedo-insured-person-mismatch-receipt-receipt"
    "urn:document:fss-sedo-proactive-payments-benefit-benefit-message", "urn:document:fss-sedo-proactive-payments-benefit-receipt"
    "urn:document:fss-sedo-proactive-payments-demand-demand-message", "urn:document:fss-sedo-proactive-payments-demand-receipt"
    "urn:document:fss-sedo-benefit-payment-initiation-result-document", "urn:document:fss-sedo-benefit-payment-initiation-read-receipt"
    "urn:document:fss-sedo-insured-person-registration-receipt", "urn:document:fss-sedo-insured-person-registration-read-receipt"
    "urn:document:fss-sedo-proactive-payments-reply-receipt", "urn:document:fss-sedo-proactive-payments-reply-read-receipt"
    "urn:document:fss-warrant-management-response-message", "urn:document:fss-warrant-management-response-read-receipt"
    "urn:document:fss-sedo-demand-message", "urn:document:fss-sedo-demand-read-receipt"
    "urn:document:fss-sedo-demand-reply-result-document", "urn:document:fss-sedo-demand-reply-read-receipt"
    "urn:document:fss-sedo-billing-information-demand-result-document", "urn:document:fss-sedo-billing-information-demand-read-receipt"
    "urn:document:fss-sedo-billing-information-message", "urn:document:fss-sedo-billing-information-read-receipt"

Подписывать «Отметку о прочтении» не нужно.

4. Отправьте ответный документ: :ref:`POST SendReplyDocument<rst-markup-sendreply>`. После отправки отметки о прочтении статус документооборота поменяется на **finished**.

**Извещение о прочтении**

Помимо отметки о прочтении для документооборотов urn:docflow:fss-sedo-pvso-notification, urn:docflow:fss-sedo-sick-report-change-notification и urn:docflow:fss-sedo-demand нужно дополнительно создать, подписать и отправить в ФСС ответный документ "Извещение о прочтении". 

1. Создайте ответный документ. Это можно сделать несколькими способоми:

    a. Сгенерируйте ответный документ: :ref:`POST CreateReplyDocument<rst-markup-post-reply-doc>`. При запросе указывает в поле ``documentType`` тип документа, который имеет вид ``fss-sedo-*-receipt-notification-message``, где * - наименование документооборота.

    b. Перейдите по ссылке из поля ``links`` в параметре ``rel``, содержащей тип нужного ответного документа. 

2. Возьмите контент подписи из метаинформации созданного документа в параметре ``data-to-sign``.
3. Подпишите эти данные необработанной (raw) подписью.
4. Добавьте подпись к ответному документу: :ref:`PUT ReplyDocumentSignature<rst-markup-repliSignature>`.
5. Отправьте ответный документ: :ref:`POST SendReplyDocument<rst-markup-sendreply>`. После отправки отметки о прочтении  статус документооборота поменяется на **finished**. 

Результат принятия извещения о прочтения появится в текущем и во входящем документообороте urn:docflow:fss-sedo-receipt-notification-result – результат подтверждения прочтения.

Работа с ошибками
-----------------

Если в ходе документооборота с СЭДО ФСС появится ошибка, то она может поступить:

    * в виде документа в исходном ДО. В этом случае статус документооборота поменяется на **finished**. Типы документов об ошибке будут иметь вид ``fss-sedo-*-exchange-error``, где * - :ref:`наименование документооборота<rst-markup-typedocumentFSS>`;
    * в виде отдельного документооборота urn:docflow:fss-sedo-error.  В этом случае перейдите к алгоритму работы с входящими документооборотами от ФСС. Документ с ошибкой от ФСС отобразится во входящем и в исходящем ДО. Статус входящего ДО поменяется на **finished**. Типы документов об ошибке будут иметь вид ``fss-sedo-*-error-massage``, где * - :ref:`наименование документооборота<rst-markup-typedocumentFSS>`. 


Тестирование сценариев
----------------------

Если для тестирования вы используете сертификаты Контура, то они уже готовы для работы с СЭДО. Если вы используете другие сертификаты, то сертификаты удостоверяющих центров должны быть добавлены в список доверенных сертификатов со стороны ФСС. 

Для удобства тестирования сценариев работы в СЭДО ФСС используйте коллекции Postman:

    * :download:`Работа с исходящими документооборотами. <../files/СЭДО Работа с исходящими документами.postman_collection.json>`
    * :download:`Работа с входящими документооборотами. <../files/СЭДО Работа с входящими документооборотами.postman_collection.json>`

В примерах xml-файлов ниже укажите данные из вашей учетной записи. Обратите внимание, что данные в сертификате должны совпадать с данными вашей учетной записи. 

    * :download:`Сведения о застрахованных лицах, пример.xml <../files/Сведения о застрахованных лицах, пример.xml>`
    * :download:`Ответ на запрос проверки подтверждения, корректировки сведений проактивной выплаты страхового обеспечения, пример.xml <../files/Ответ на запрос проверки, пример.xml>`





