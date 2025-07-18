.. _`3 причины`: https://normativ.kontur.ru/document?moduleId=1&documentId=191490
.. _`xsd-схеме`: https://normativ.kontur.ru/document?moduleId=1&documentId=191882&rangeId=377678

.. _rst-markup-fns-check-demand:

Проверка требования ФНС
=======================

Процесс работы с поступившим требованием подробнее описан в статье :ref:`Требования<rst-markup-FNS-demand>`. В API Контур.Экстерн есть вспомогательные методы для работы с требованием. Это методы распознавания и проверки требования. Рассмотрим подробнее процесс проверки требования. 

**Зачем нужно проверять требования?** Согласно :ref:`порядку документооборота<rst-markup-demand-status>` в ответ на требование из ФНС налогоплательщик должен отправить извещение о получении, после которого сформировать квитанцию о приеме или уведомление об отказе. При этом существует только `3 причины`_, по которым можно отправить отказ от приема требования:

1. ошибочное направление налогоплательщику,
2. несоответствие утвержденному формату,
3. отсутствие (несоответствие) электронной подписи уполномоченного должностного лица налогового органа.

В файле отказа указывается перечень выявленных нарушений и коды ошибок. При получении уведомления об отказе в приеме налоговый орган устраняет указанные в этом уведомлении ошибки и повторяет процедуру направления Требования.

Чтобы выявить нарушения в полученном требовании и соответствующие им коды ошибок, нужно выполнить проверки. Если у интегратора есть такая возможность, он может реализовать проверку требований на своей стороне. В API был добавлен метод проверки требования для автоматизации данного процесса. Использование метода упростит работу с требованием и поможет корректно сформировать ответный документ.

Сценарий использования проверки требования
------------------------------------------

1. Получить требование. 
2. Отправить извещение о получении. :doc:`См. Методы для работы с ответными документами </dc/ответный документ>`.
3. Проверить требование на валидность. Метод :ref:`POST Check-Demand<rst-markup-check-demand>`.
4. Если требование корректное — отправить квитанцию о приеме fns534-demand-acceptance-result-positive. Следующим шагом, в зависимости от вида требования, :ref:`отправить ответ на него<rst-markup-FNS-inventory>`, уплатить штраф или явиться в налоговую. 
5. Если требование некорректное — отправить уведомление об отказе fns534-demand-acceptance-result-negative. В файле необходимо указать причину и код ошибки. На данном этапе работа с требованием завершена.


Проверки по причинам отказа и коды ошибок
-----------------------------------------

.. |br| raw:: html

    <br />

.. table::

    +--------------------------+-------------------------------------------------+-------------------------------------------------------------+
    | Проверка по причине      | Перечень выявленных нарушений                   | Реализация проверки                                         |
    | отказа                   |                                                 |                                                             |
    +==========================+=================================================+=============================================================+
    | Ошибочное |br|           | ИНН/КПП налогоплательщика не соответствует |br| | Сравнение ИНН/КПП в документе fns534-demand с |br|          |
    | направление |br|         | ИНН/КПП в отправленном транспортном   |br|      | организациями пользователя                                  |
    | налогоплательщику        | контейнере |br|                                 |                                                             | 
    |                          |                                                 |                                                             |
    |                          | Код ошибки ``0400100005``                       |                                                             |
    +--------------------------+-------------------------------------------------+-------------------------------------------------------------+
    | Соответствие  |br|       | Файл не соответствует xsd-схеме   |br|          | Проверка Документа fns534-demand по `xsd-схеме`_            |
    | утвержденному формату    |                                                 |                                                             |
    |                          | Код ошибки ``0300300001``                       |                                                             |   
    |                          +-------------------------------------------------+-------------------------------------------------------------+
    |                          | Нарушено условие  присутствия (отсутствия) |br| | Проверка присутствия/отсутствия приложений |br|             |
    |                          | элемента |br|                                   | fns534-demand-attachment к требованию.                      |
    |                          |                                                 |                                                             |
    |                          | Код ошибки ``0300300030``                       | Количество приложений, указанных в документе |br|           |
    |                          |                                                 | fns534-demand, должно совпадать с фактическим |br|          |
    |                          |                                                 | числом поступивших приложений |br|                          |
    |                          |                                                 | fns534-demand-attachment                                    |
    +--------------------------+-------------------------------------------------+-------------------------------------------------------------+
    | Расшифровываемость  |br| | Контейнер зашифрован для другого получателя     | Проверка реализуется на стороне пользователя или |br|       |
    | и соответствие ЭП        |                                                 | интегратора. При формировании уведомления об отказе |br|    |
    |                          | Код ошибки ``0100300003``                       | есть возможность указать соответствующий код ошибки         |
    |                          +-------------------------------------------------+-------------------------------------------------------------+
    |                          | ЭП не соответствует подписанному документу |br| | Успешная проверка подтверждает авторство подписи |br|       |
    |                          | (ЭП искажена или в документ были внесены  |br|  | и гарантирует, что после подписания в документ |br|         |
    |                          | изменения уже после его подписания) |br|        | не вносились изменения и сертификат не был отозван          |
    |                          |                                                 |                                                             |
    |                          | Код ошибки ``0100100004``                       |                                                             |     
    +--------------------------+-------------------------------------------------+-------------------------------------------------------------+
