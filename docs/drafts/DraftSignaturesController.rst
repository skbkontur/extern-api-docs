.. _`Черновики и конструктор черновиков (draftsbuilder)`: https://developer.kontur.ru/doc/extern.drafts
.. _`POST AddSignature`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures
.. _`GET Signature`: https://developer.kontur.ru/doc/extern.drafts/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignature
.. _`PUT Signature`: https://developer.kontur.ru/doc/extern.drafts/method?type=put&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures%2F%7BsignatureId%7D
.. _`DELETE Signature`: https://developer.kontur.ru/doc/extern.drafts/method?type=delete&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures%2F%7BsignatureId%7D
.. _`GET SignatureContent`: https://developer.kontur.ru/doc/extern.drafts/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures%2F%7BsignatureId%7D%2Fcontent

Методы для работы c подписью в черновике
========================================

Данный раздел посвящен методам, с помощью которых можно работать с подписями документа в черновике. Для работы с этими методами черновик и документ должны быть предварительно созданы.

Подробная спецификация методов показана в Swagger в разделе `Черновики и конструктор черновиков (draftsbuilder)`_.

Список доступных методов:

* `Создание подписи документа в черновике`_
* `Получение подписи документа в черновике`_
* `Редактирование подписи документа в черновике`_
* `Удаление подписи документа в черновике`_
* `Получение содержимого подписи документа в черновике`_

.. _rst-markup-AddSignature:

Создание подписи документа в черновике 
--------------------------------------

Метод: `POST AddSignature`_

Получение подписи документа в черновике
---------------------------------------

Метод: `GET Signature`_

Редактирование подписи документа в черновике
--------------------------------------------

Метод: `PUT Signature`_

Метод обновляет подпись документа черновика на переданную в запросе. Если подпись с переданным идентификатором не существует, метод создаст ее в черновике.

Удаление подписи документа в черновике 
--------------------------------------

Метод: `DELETE Signature`_

Получение содержимого подписи документа в черновике
---------------------------------------------------

Метод: `GET SignatureContent`_

