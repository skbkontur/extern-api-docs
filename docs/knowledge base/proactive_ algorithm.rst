.. _`POST Create draft`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts
.. _`POST AddDocument`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments
.. _`POST Add signature`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures 
.. _`POST Check`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fcheck
.. _`POST Prepare`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fprepare
.. _`POST Send`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fsend
.. _`GET Docflow`: https://developer.kontur.ru/doc/extern.docflows/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D
.. _`GET Docflows`: https://developer.kontur.ru/doc/extern.docflows/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows
.. _`GET DraftTask`: https://developer.kontur.ru/doc/extern/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Ftasks%2F%7BapiTaskId%7D 



Алгоритм работы с методами в проактивных выплатах
=================================================

Особенности документооборотов в СЭДО:
-------------------------------------

* Для получения документов от ФСС нужно выполнить :doc:`подписку оператора на организацию по РНС</knowledge base/sedo-subscription>`.
* Входящие документообороты от ФСС в статусе **received** не содержат документов. Чтобы их получить и поменять статус документооборотов нужно сформировать запрос на получение документов.
* Все отправляемые в СЭДО документы являются SOAP-запросами.
* Запросы должны быть подписаны подписью в формате :doc:`XMLDsig</manuals/xmldsig>`.
* Результат приема отчета "Сведения о застрахованном лице" нужно смотреть в документе "Результат регистрации сведений о застрахованных лицах" (urn:document:fss-sedo-insured-person-registration-result-response-result) по каждому СНИЛС отдельно.
* В проактивных выплатах сохраняется отправка :doc:`реестров ПВСО</knowledge base/reestr-pvso>`, подробнее о порядке взаимодействия с ФСС читайте в статье :doc:`Проактивные выплаты</knowledge base/proactiv>`.

Работа с исходящими документооборотами
--------------------------------------

В схеме проактивных выплат работодатель направляет в ФСС следующие исходящие документообороты:
    
    * сведения о застрахованных лицах (urn:docflow:fss-sedo-insured-person-registration);
    * ответ на запрос проверки, подтверждения, корректировки сведений проактивной выплаты страхового обеспечения (urn:docflow:fss-sedo-proactive-payments-reply).

**Создание и отправка черновика**

1. Создайте черновик: :ref:`POST Create draft<rst-markup-createdraft>`. При создании черновика в теле запроса обязательно укажите:
    
    a. в ``payer`` параметр ``registration-number-fss``;
    b. в ``recipient`` параметр ``fss-code``.

2. Загрузите файл документа в :ref:`Сервис контентов<rst-markup-load>`.
3. Создайте документ в черновике: :ref:`POST AddDocument<rst-markup-addDocument>`. При создании укажите ссылку на документ в виде идентификатора из :ref:`Сервиса контентов<rst-markup-load>`.
4. Возьмите идентификатор подписи из метаинформации ответа метода ``AddDocument`` в поле ``data-to-sign-content-id`` и получите данные для подписи через :ref:`Сервис контентов<rst-markup-dowload>`. 
5. Подпишите эти данные сырой (raw) подписью. 
6. Приложите подпись к документу: :ref:`POST Add signature<rst-markup-AddSignature>`.
7. Когда черновик готов, запустите последовательность методов: :ref:`POST Check<rst-markup-check>` -> :ref:`POST Prepare<rst-markup-prepare>` -> :ref:`POST Send<rst-markup-send>`. Укажите флаг ``deferred = true`` для отложенного выполнения задач. 
8. Проверьте результат выполнения методов ``Check``, ``Prepare``, ``Send`` в задачах: :ref:`GET DraftTask<rst-markup-DraftTasks>`. Если запрос по методу ``Send`` завершился успешно, то в ответе вернется информация о созданном документообороте (ДО).

В рамках проактивных выплат ДО считается завершенным после отправки черновика. Необходимо ожидать входящие документообороты от ФСС. Документы входящих ДО также будут отображаться в исходящих ДО. 

.. _rst-markup-sedo-incoming-dc:

Работа с входящими документооборотами от ФСС
--------------------------------------------

1. Найдите входящие документообороты от ФСС: :ref:`GET Docflows<rst-markup-get-dcs>`. В запросе укажите фильтр ``type`` и тип нужного ДО согласно :ref:`спецификации<rst-markup-cbrf>`, например, ``type=fss-sedo-pvso-notification&type=fss-sedo-sick-report-change-notification&type=fss-sedo-error``. Новые документообороты будут отображаться в статусе **received**. Для получения документов и смены статуса ДО нужно отправить запрос на получение документов от ФСС. Далее работайте с каждым ДО по отдельности. 

.. important:: В результатах поиска не будет документооборотов с типами ``fss-sedo-*``, если их тип не был указан в параметре ``type``.

2. Для получения документов от ФСС нужно сформировать, подписать и отправить запрос. Для этого используйте :ref:`методы генерации запроса в СЭДО ФСС<rst-markup-sedo>`:

    a. Создайте запрос на получение документов от ФСС: :ref:`POST GenerateDocumentsRequest<rst-markup-sedo>`. В запросе укажите id найденного входящего документооборота. В ответе метод вернет шаблон запроса и хэш для подписи.
    b. Подпишите хэш, который вернется в параметре ``DataToSign`` в формате byte[].
    c. Добавьте необработанную подпись к запросу: :ref:`PUT SaveDocumentsRequestSignature<rst-markup-sedosavedocuments>`.
    d. Отправьте запрос на получение документов в ФСС: :ref:`POST SendDocumentsRequest<rst-markup-sedosavedocuments>`. 

3. Когда ФСС обработает запрос, он отправит запрошенный документ и статус ДО поменяется:

    a. Для документооборотов urn:docflow:fss-sedo-insured-person-registration-result и urn:docflow:fss-sedo-proactive-payments-reply-result документы появятся в текущих и исходящих ДО. Статус документооборотов поменяется на **finished** и **они будут считаться завершенными**. 
    b. Для остальных входящих документооборотов статус поменяется на **response-arrived**. Документы будут только во входящем ДО. Для данных документооборотов **потребуется отправка ответного документа** "Извещение о прочтении".

.. note:: Рекомендуем для дальнейшей работы каждый документооборот вычитать отдельно методом :ref:`GET Docflow<rst-markup-get-dc>`.

4. Найдите в поле ``documents`` полученного ДО документ с соответствующим типом:

.. csv-table:: 
   :header: "Документооборот", "Тип документа"
   :widths: 20 30

   "urn:docflow:fss-sedo-pvso-notification", "urn:document:fss-sedo-pvso-notification-notification-message"
   "urn:docflow:fss-sedo-sick-report-change-notification", "urn:document:fss-sedo-sick-report-change-notification-notification-message"
   "urn:docflow:fss-sedo-insured-person-registration-result", "urn:document:fss-sedo-insured-person-registration-result-response-result"
   "urn:docflow:fss-sedo-insured-person-mismatch", "urn:document:fss-sedo-insured-person-mismatch-mismatch-message"
   "urn:docflow:fss-sedo-proactive-payments-reply-result", "urn:document:fss-sedo-proactive-payments-reply-result-response-result"
   "urn:docflow:fss-sedo-proactive-payments-benefit", "urn:document:fss-sedo-proactive-payments-benefit-benefit-message"

5. Чтобы получить файл документа, возьмите идентификатор ``content-id`` в метаинформации документа, в модели ``docflow-document-contents`` и скачайте документ из :ref:`Сервиса контентов<rst-markup-dowload>`.

6. Сгенерируйте ответный документ «Извещение о прочтении» к полученным документам в следующих ДО:

    * urn:docflow:fss-sedo-pvso-notification;
    * urn:docflow:fss-sedo-sick-report-change-notification;
    * urn:docflow:fss-sedo-insured-person-mismatch;
    * urn:docflow:fss-sedo-proactive-payments-benefit.

Это можно сделать несколькими способами:

    a. Сгенерируйте ответный документ: :ref:`POST CreateReplyDocument<rst-markup-post-reply-doc>`. Используйте id найденного документа. В поле ``documentType`` укажите тип документа, который имеет вид ``fss-sedo-*-notification-receipt``, где * - наименование документооборота.
    b. Перейдите по ссылке из поля ``links`` в параметре ``rel``, содержащей тип нужного ответного документа. 

Подписывать «Извещение о прочтении» не нужно.

7. Отправьте ответный документ: :ref:`POST SendReplyDocument<rst-markup-sendreply>`. После отправки извещения о прочтении статус документооборота поменяется на **finished**.

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





