.. _`подписание черновика`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fcloud-sign
.. _`проверка (Check)`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fcheck
.. _`подготовка (Prepare)`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fprepare
.. _`отправка (Send)`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fsend
.. _`печать`: https://developer.kontur.ru/doc/extern.drafts/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fprint 
.. _`изменение`: https://developer.kontur.ru/doc/extern.drafts/method?type=put&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D
.. _`удаление`: https://developer.kontur.ru/doc/extern.drafts/method?type=delete&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D
.. _`добавление подписи`: https://developer.kontur.ru/doc/extern.drafts/method?type=put&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignature
.. _`POST Build`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2Fbuilders%2F%7BdraftsBuilderId%7D%2Fbuild

Блокировки
==========
.. contents:: 
   :depth: 2

Зачем нужны блокировки
----------------------

Блокировка запрещает выполнять действия с черновиком, DraftsBuilder или документооборотом, пока не закончил выполняться запрос, который вызвал блокировку. Блокируется при этом объект, для которого вызван метод (черновик, документ, подпись и т.д.). Это уберегает от возможных коллизий при одновременном, параллельном выполнении запросов, связанных с одним объектом, или при ошибках и повторной отправке запроса. При выполнении запросов, ограниченных блокировками, возвращается ошибка с кодом 409. 

Блокировки в черновиках
-----------------------

Блокировки в черновиках запрещают одновременно выполнять:

* POST, PUT, DELETE запросы параллельно с одним из методов: `подписание черновика`_, `проверка (Check)`_, `подготовка (Prepare)`_, `отправка (Send)`_. *Примечание*: разрешено параллельно выполнять запрос на `печать`_ документа в черновике;
* `печать`_ одного и того же документа;
* запрос на `изменение`_ или `удаление`_ документа, `добавление подписи`_ (put signature) к документу в черновике пока не завершился запрос печати документа.

Блокировки в документооборотах
------------------------------

Блокировки в документооборотах запрещают одновременно выполнять:

* печать одного и того же документа из документооборота;
* подписание сертификатом разных ответных документов (с разными reply-id) в одном документообороте;
* дешифрование сертификатом разных документов в одном документообороте .

Блокировки в DraftsBuilder
--------------------------

Блокировки в DraftsBuilder запрещают:

* одновременно выполнять метод `POST Build`_ одного и того же конструктора черновиков (сборка DraftsBuilder в черновик). 
* выполнять POST, PUT, DELETE запросы по завершении работы метода `POST Build`_. 
    
    Данные ограничения можно отслеживать по статусу DraftsBuilder. Пока статус в значении New — можно выполнять любые операции. Когда запускается сборка, статус меняется на Building, запрещаются любые запросы к собираемому DraftsBuilder кроме GET.

    Если по завершении сборки попробовать запустить любой метод на изменение сущностей DraftsBuilder, вернется ошибка. *Исключение*: повторное выполнение запроса сборки, если метод завершился ошибкой с кодом **500**. 

Ошибка 409 Conflict
-------------------

При попытке одновременного выполнения запросов, ограниченных блокировками, API возвращает ошибку с кодом **409 Conflict**. Тело ответа содержит ошибку с идентификатором ``urn:error:externapi:concurrentApiTaskActive``. Дополнительно ошибка может содержать идентификатор и тип параллельно выполняющейся операции.

**Пример ошибки**

.. code-block:: json

    {
        "id": "urn:error:externapi:concurrentApiTaskActive",
        "status-code": 409,
        "track-id": "m4n3ggqtoxgge78q93go",
        "message": "There is an active concurrent operation",
        "trace-id": "[T-587660f5(-)] ",
        "context": {
            "concurrent-task": {
            "id": "5b35fae5-e429-43c5-befe-6a4aa3cfceda",
            "task-type": "urn:task-type:send"
            }
        }
    }