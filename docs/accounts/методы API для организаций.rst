.. _`Organizations`: https://developer.kontur.ru/doc/extern/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Forganizations
.. _`GET Organizations`: https://developer.kontur.ru/doc/extern/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Forganizations
.. _`POST Organization`: https://developer.kontur.ru/doc/extern/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Forganizations
.. _`PUT Organization`: https://developer.kontur.ru/doc/extern/method?type=put&path=%2Fv1%2F%7BaccountId%7D%2Forganizations%2F%7BorgId%7D
.. _`GET Organization`: https://developer.kontur.ru/doc/extern/method?type=get&path=%2Fv1%2F%7BaccountId%7D%2Forganizations%2F%7BorgId%7D
.. _`DELETE Organization`: https://developer.kontur.ru/doc/extern/method?type=delete&path=%2Fv1%2F%7BaccountId%7D%2Forganizations%2F%7BorgId%7D

Методы для работы с организациями
=================================

В данном разделе пойдет речь о работе с организациями в указанной учетной записи. 

Подробная спецификация методов показана в сваггере в разделе Organizations_.

Список доступных методов:

* `Получение списка доступных организаций`_
* `Получение конкретной организации`_
* `Добавление организации`_
* `Редактирование организации`_
* `Удаление организации`_

Получение списка доступных организаций
--------------------------------------

Метод: `GET Organizations`_

Метод используется для получения списка всех организаций, за которые возможна работа из-под указанной учетной записи. 

.. _rst-markup-organization:

Получение конкретной организации
--------------------------------

Метод: `GET Organization`_ 

Добавление организации
----------------------

Метод: `POST Organization`_

Метод позволяет добавить новую организацию в учетную запись Контур.Экстерн.

Редактирование организации
--------------------------

Метод: `PUT Organization`_

Допускается изменение только названия организации.

Удаление организации
--------------------

Метод: `DELETE Organization`_

Метод позволяет удалить организацию из учетной записи Контур.Экстерна.

Организацию можно удалить при следующих условиях:

* если прошло больше 12 месяцев со дня регистрации организации в Контур.Экстерн;
* если прошло меньше 12 месяцев со дня регистрации организации, но в текущем отчетном периоде не отправлялись отчеты, письма и запросы в контролирующие органы;
* если организация ликвидирована по данным ЕГРЮЛ.
