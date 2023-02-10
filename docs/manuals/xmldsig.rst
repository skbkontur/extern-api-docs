.. _`Описание стандарта подписи`: https://www.w3.org/TR/2013/REC-xmldsig-core1-20130411/ 
.. _`POST Check`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fcheck
.. _`GET DraftDocument`: https://developer.kontur.ru/doc/extern.drafts/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D
.. _`PUT DocumentSignature`: https://developer.kontur.ru/doc/extern.drafts/method?type=put&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignature
.. _`POST Prepare`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fprepare

Подпись XMLDsig
===============

При работе с документооборотами ПФР и ФСС некоторые отчеты должны быть подписаны подписью в формате xmlDsig. Для этого соответствующий блок Signature выносится по w3c в корень.

В рамках ПФР необходимо использовать необработанную (raw) подпись для следующих документооборотов:

* заявление на подключение к ЭДОК;
* отчет СЗВ-ТД.

Подпись xmlDsig является подписью по правилам СМЭВ 3. `Описание стандарта подписи`_ (см. Enveloped or enveloping signatures).

В рамках ФСС необработанная(raw) подпись используется для :doc:`документооборотов СЭДО</knowledge base/proactiv>`. Стандарт подписи по правилам СМЭВ 3 также сохраняется и для ФСС. 

Если вы испытываете трудности в добавлении подписи в документ черновика на своей стороне, в методах API реализована функция помощи в подписании.


.. _rst-markup-apiForXmlDsig:

Формирование XMLDsig подписи на стороне API 
-------------------------------------------

Порядок вызова методов для формирования подписи XMLDsig:

#. Загрузить в черновик XML-документ отчета. Заявление на подключение к ЭДОК можно сформировать с помощью :doc:`методов формирования файлов documentBuilder</drafts/DraftDocumentBuildController>`.
#. Проверить черновик `POST Check`_.
#. Если в загруженном документе не было XMLDsig, то на шаге Check в документ будет добавлено поле dataToSignContentId.
#. После Check необходимо получить документ `GET DraftDocument`_.
#. Через сервис контентов по dataToSignContentId получить данные для подписи :ref:`GET Download<rst-markup-get-content>`.
#. Подписать эти данные необработанной (raw) подписью.
#. Загрузить в черновик подпись `PUT DocumentSignature`_.
#. Вызвать для черновика шаг `POST Prepare`_. На этом шаге подпись XMLDsig будет добавлена в XML-документ.