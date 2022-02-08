.. _`POST Create draft`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts
.. _`POST AddSignature`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures
.. _`POST Check`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fcheck
.. _`POST Prepare`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fprepare
.. _`POST Send`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fsend

Подписки СЭДО ФСС на получение извещений и уведомлений
======================================================

Для получения уведомлений и извещений от ФСС необходимо выполнить **подписку оператора на организацию по РНС** (тип документооборота urn:docflow:fss-sedo-provider-subscription).


Данная подписка является отдельными документооборотом. Процесс смены статусов документооборотов см. в разделе :ref:`спецификация<rst-markup_subscription>`.

Создание и отправка подписок
----------------------------

**Алгоритм создания и отправки черновика подписок**

#. Создать черновик. Метод `POST Create draft`_. В мета-информации черновика необходимо заполнить поле registration-number-fss — регистрационный номер, по которому производится подписка.
#. Создать документ в черновике по :doc:`json контракту</manuals/contracts>`. Метод :doc:`POST BuildDocumentContent</drafts/DraftDocumentBuildController>`. В ответе метод возвращает информацию о документе.
#. Проверить черновик `POST Check`_. 
#. Подготовить черновик `POST Prepare`_.
#. Отправить черновик `POST Send`_.

После отправки подписки, ФСС пришлет результат. 

.. important:: **Для тестирования отправки подписок** есть специальный робот, который эмулирует работу приемного комплекса на тестовой площадке. Для этого  нужно в п.1 при создании черновика указать в recipient значение **fss-code: SEDO-TEST**.

Получение результата подписки
-----------------------------

Для подписки оператора положительный результат от ФСС поступит в виде документа в отправленном документообороте. 

Для получения результата подписки оператора вам нужно **найти документооборот и ожидать появления в нем результата подписки**:

    1. Найти документооборот методом :ref:`GET Docflows<rst-markup-get-dcs>` с фильтром ``type=fss-sedo-provider-subscription``. 
    2. В полученной метаинформации документооборота в поле ``success-state`` будет отображаться статус подписки. Если подписка выполнена успешно, то статус будет ``successful``.

На этом документооборот завершится и подписка будет считаться выполненной.
