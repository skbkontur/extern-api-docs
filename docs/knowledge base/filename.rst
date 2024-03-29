.. _сервисом генерации тестовых данных: https://developer.kontur.ru/doc/extern.test.tools
.. _`спецификации ФСС`: http://fz122.fss.ru/doc/reglrest.pdf

Наименование файлов
===================

Наименование файлов для отчетов ФНС
-----------------------------------

.. note:: Все файлы отчетов в формате xml, которые вы отправляете в ИФНС должны быть сохранены в кодировке windows-1251.

Для отчетов в ФНС в формате xml имя файла, помимо названия, **дублируется внутри файла** в теге Файл параметр ИдФайл. И в названии, и в теге имя файла должно полностью совпадать. 

Формат имени файла установлен в нормативных документах. Имя файла для ФНС будет состоять из следующих частей:
 
- название формы отчетности по приказу,
- код транзитной инспекции  (код МРИ),
- код конечной инспекции,
- ИНН-КПП слитно без разделителей (если по доверенности, то ИНН-КПП отправителя),
- дата формирования файла,
- идентификатор файла.

Если вы не хотите вручную менять данные внутри файла и в его имени, воспользуйтесь `сервисом генерации тестовых данных`_. В данном API реализованы методы для генерации тестовых файлов на ваших данных.

.. _rst-markup-name-reestr-pvso:

Наименование файлов реестров ПВСО
---------------------------------

Для :doc:`реестров ПВСО</knowledge base/reestr-pvso>` имя файла должно принимать вид согласно `спецификации ФСС`_: 

**E_NUMBER_YYYY_MM_DD_NNNN.xml**

**Литера_Регистрационный номер_Год_Месяц_День_Номер реестра за день**

Описание элементов имени файла:

* **Литера E (Employer)**  — работодатель, он же страхователь для ФСС РФ.
* **Регистрационный номер** — следует за литерой и позволяет определить работодателя на этапе приема реестра порталом ФСС. Для филиалов используется регистрационный номер обособленного подразделения, это последние 10 знаков расширенного регистрационного номера. Если у филиала он отсутствует, то используется регистрационный номер вышестоящей организации.  
* **YYYY**  — год.
* **MM** — месяц, допустимы значения из диапазона 01, 02, …, 12.
* **DD** — день, допустимы значения из диапазона 01, 02, …, 31 в соответствии с количеством дней месяца и годом.
* **Номер в конце наименования** — указывает на очередность реестра при отправке нескольких реестров в один день и состоит их четырех символов.

Максимальная длина имени без расширения не может быть больше 28 символов.

.. note:: После подписания реестра электронно-цифровой подписью расширение файла должно быть: ***.esl**.

Пример названия и файла до подписания:

:download:`E_0000000000_2021_04_14_0002.xml <../files/E_0000000000_2021_04_14_0002 .xml>`

Пример названия и файла после подписания: 

:download:`E_0000000000_2021_04_14_0002.esl <../files/E_0000000000_2021_04_14_0002.esl>`