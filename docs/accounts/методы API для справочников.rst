.. _Accounts: https://developer.kontur.ru/doc/extern/method?type=get&path=%2Fv1
.. _`GET ControlUnits`: https://developer.kontur.ru/doc/extern/method?type=get&path=%2Fv1%2Fhandbooks%2Fcontrol-units
.. _`GET ListKND`: https://developer.kontur.ru/doc/extern/method?type=get&path=%2Fv1%2Fhandbooks%2Ffns-forms
.. _`GET ControlCode`: https://developer.kontur.ru/doc/extern/method?type=get&path=%2Fv1%2Fhandbooks%2Fcontrol-units%2F%7Bcode%7D

.. _rst-mrkup-handbooks:

Методы для работы со справочниками
==================================

Подробная спецификация методов представлена в swagger в разделе Accounts_.

Список доступных методов:

* `Получение списка контролирующих органов`_
* `Получение списка КНД`_
* `Получение контролирующего органа по коду`_

Получение списка контролирующих органов
---------------------------------------

Метод: `GET ControlUnits`_

Метод вернет список контролирующих органов с контактной информацией.

Для каждого контролирующего органа могут вернутся свои наборы флагов особенностей работы:

* ``is-active`` – указывает на активность контролирующего органа;
* ``is-test`` – указывает на тестовый статус контролирующего органа;
* ``business-registration`` – ФНС поддерживает регистрацию бизнеса.

Получение списка КНД
--------------------

Метод: `GET ListKND`_

Метод вернет список КНД форм отчетности и требований ФНС.

.. _rst-markup-control-code:

Получение контролирующего органа по коду
----------------------------------------

Метод: `GET ControlCode`_

Метод вернет информацию о контролирующем органе по его коду. 