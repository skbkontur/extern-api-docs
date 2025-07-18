.. _`Как самостоятельно подписать документ электронной подписью`: https://ca.kontur.ru/articles/podpisanie-dokumenta-ehlektronnoj-podpisyu
.. _`Контур.Крипто`: https://crypto.kontur.ru/
.. _`Extern Test Tools`: https://developer.kontur.ru/doc/extern.test.tools
.. _`как установить сертификат, если у Вас есть КриптоПро CSP`: https://ca.kontur.ru/faq/signature/kak-ustanovit-lichnyy-sertifikat
.. _`Создание подписи документа`: https://developer.kontur.ru/doc/extern.drafts/method?type=post&path=%2Fv1%2F%7BaccountId%7D%2Fdrafts%2F%7BdraftId%7D%2Fdocuments%2F%7BdocumentId%7D%2Fsignatures
.. _`Добавление подписи к ответному документу`: https://developer.kontur.ru/doc/extern.docflows/method?type=put&path=%2Fv1%2F%7BaccountId%7D%2Fdocflows%2F%7BdocflowId%7D%2Fdocuments%2F%7BdocumentId%7D%2Freplies%2F%7BreplyId%7D%2Fsignature

Криптография
============

Терминология
------------
**Электронная подпись (ЭП)** — это атрибут электронного документа, который позволяет установить его авторство и неизменность после подписания. ЭП формируется для каждого подписываемого электронного документа индивидуально с помощью закрытого ключа электронной подписи, а так же с помощью средств криптографической защиты информации (СКЗИ).

    Сертификат электронной подписи подтверждает принадлежность электронной подписи владельцу и содержит: закрытый ключ — для генерации электронных подписей; открытый ключ — для проверки подлинности подписи получателем; сведения о владельце — для проверки получателем информации об авторе документа.

**Ключевая пара** — закрытый ключ (ЗК) и открытый ключ (ОК). С помощью закрытого ключа происходит подписание и дешифрование документов. ЗК является секретным, к нему имеет доступ только владелец сертификата ЭП. С помощью открытого ключа происходит проверка подписи и шифрование документов. ОК доступен любому и включен в сертификат ЭП.

**Сертификат ЭП** — документ, содержащий в себе информацию о владельце сертификата и его ОК. Сертификат подтверждает, что ОК принадлежит именно этому владельцу.

**Отсоединенная подпись** — ЭП, которая создается при подписании отдельным файлом и отделена от подписываемого документа. При использовании такого типа подписи сам документ не меняется. Например, используется в отчетах в ФНС.

**Встроенная (присоединенная) подпись** — ЭП, которая является частью подписываемого документа. При использовании этого типа подписи документ изменится, т.к. подпись будет прикреплена к нему.  Например, используется в заявлении на подключение к ЭДОК в СФР. 

**Отпечаток сертификата** — уникальный код, хеш файла сертификата. Отпечаток однозначно идентифицирует конкретный сертификат. Состоит из 40 символов шестнадцатеричной системы счисления (0-9, A-F).

----------------

Подписание и дешифрование контента с использованием сертификата
---------------------------------------------------------------
Для отправки отчета в контролирующий орган файлы нужно подписать сертификатом пользователя. Для подписания нужен закрытый ключ сертификата, поэтому *подпись к файлам пользователь создает самостоятельно*. 
При создании черновика в данных отправителя нужно передавать сертификат в формате base64. Именно этим сертификатом должна быть создана подпись. На этапе подготовки в методе Prepare в API будет сверяться соответствие сертификата и подписей файлов. 

Файлы отчета и подпись к ним нужно загрузить и отправить в контролирующий орган с помощью методов API. Шифрование отправляемых в контролирующие органы файлов происходит в момент отправки на стороне оператора ЭДО. 

Входящие документы и документообороты шифрует контролирующий орган. При получении, чтобы посмотреть документы, их нужно дешифровать при помощи закрытого ключа пользователя. Поэтому *пользователь самостоятельно должен дешифровать файлы*.

.. note:: Для подписания и дешифрования файлов нужно использовать закрытый ключ пользователя, который может быть на отдельном носителе, ПК пользователя или сервере. Поэтому все криптографические операции возможны только на стороне интегратора. 

Какие инструменты нужны для подписания и дешифрования
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Для подписания документов можно использовать любой криптопровайдер, который поддерживает ГОСТ шифрование и подписание. В статье `Как самостоятельно подписать документ электронной подписью`_ есть сравнение программ для создания электронной подписи. 

Помимо перечисленных в статье готовых решений, также можно выбрать любые модули или библиотеки, которые поддерживают текущий ГОСТ. Выбирайте самостоятельно, что Вам подходит по стеку технологий. 

Для ручного тестирования методов API можно использовать бесплатный сервис `Контур.Крипто`_. Также у КриптоПро есть плагин для браузера и утилита для работы в командной строке. 

Тестовый сертификат
~~~~~~~~~~~~~~~~~~~

Для тестирования методов API Контур.Экстерна вместе с api-key вам выдается тестовый сертификат. Также можно сгенерировать сертификат самостоятельно в сервисе `Extern Test Tools`_.

Как установить тестовый сертификат
""""""""""""""""""""""""""""""""""
Если Вы используете сертификат в формате PFX, сделайте двойной клик по сертификату. Запустится мастер импорта сертификатов, следуйте его инструкции.

Если у Вас есть сертификат не в формате PFX, например .cer, используйте инструкцию: `как установить сертификат, если у Вас есть КриптоПро CSP`_.

Как подписать и дешифровать контент вручную
-------------------------------------------

Создание отсоединенной подписи файла
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

В данном примере использован тестовый сертификат, установленный на компьютере, и xml-файл отчета ССЧ.

1. Возьмите файл, который нужно подписать.
2. Перейдите на сайт `Контур.Крипто`_. 
3. Нажмите кнопку **Начать пользоваться**. 
4. Перейдите в раздел **Подписать**. 
5. Приложите файл отчета. 
6. Выберите сертификат, которым будете подписывать файл. 
7. Нажмите кнопку **Подписать**. Будет сформирована подпись. 
8. Нажмите кнопку **Cкачать подпись**.

.. image:: /_static/sign.png
   :width: 600

.. image:: /_static/download_sign.png
   :width: 600

Вам на компьютер будет скачан файл подписи с расширением .sig. Этот файл подписи нужно передать в запросе в АПИ, в том формате, который указан в контракте.
Например, метод `Создание подписи документа`_ в черновике требует приложить файл подписи в формате base64. А в ответных документах документооборота метод `Добавление подписи к ответному документу`_ требует приложить сам файл непосредственно. 

Дешифрование файла
~~~~~~~~~~~~~~~~~~

Например, пользователь отправил отчет в ИФНС. В документообороте появился новый документ от контролирующего органа. В модели docflow, в параметре documents у каждого документа будет поле encrypted-certificates. Здесь перечислены серийные номера всех сертификатов, на которые был зашифрован документ, в том числе сертификат пользователя. 

1. Возьмите зашифрованный файл.
2. Перейдите на сайт `Контур.Крипто`_. 
3. Нажмите кнопку **Начать пользоваться**. 
4. Перейдите в раздел **Расшифровать**. 
5. Приложите файл. Для дешифрования файл должен иметь расширение .enc. Если Вы скачали файл через API и он будет называться response.bin, допишите расширение .enc. Пример: response.bin.enc.
6. Нажмите кнопку **Расшифровать документ**.
7. Программа предложит выбрать путь, куда сохранить дешифрованный файл response.bin.

.. image:: /_static/encrypt.png
   :width: 600

.. image:: /_static/encrypt_doc.png
   :width: 600

Работа с дешифрованным контентом, который получили через API
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. note:: Если у файла, который Вы скачали через API, есть флаг сжатости, после дешифрования Вы получите архив. 

1. Допишите к полученному файлу расширение .zip. Пример: response.bin.zip. 
2. Разархивируйте архив. В папке будет лежать текстовый файл. 
3. Если у него расширение .bin, поменяйте его на тип контента из параметра content-type модели DocflowDocumentDescription. 
