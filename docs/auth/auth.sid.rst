auth.sid (obsolete)
===================

.. important:: Данный способ аутентификации через auth.sid будет поддерживаться для реализованных интеграций. Для новых интеграций нужно использовать :doc:`аутентификацию по протоколу OpenId Connect </auth_oidc/index>`.

Что это такое?
--------------

* Когда пользователь аутентифицируется, API аутентификации создает на сервере запись о сессии и ставит куку auth.sid на домен kontur.ru.
* Сервис по sid из куки получает информацию о сессии и идентификатор пользователя. 

Есть два способа передачи auth.sid на сервер. Рекомендуется поддерживать оба способа.

HTTP-заголовок Authorization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  GET /drive/documents?skip=10&take=10
  Host: api.kontur.ru
  Accept: application/json
  Authorization: auth.sid FE6CFF8BE5E5B548AB1971874886D5C30E85D9BFA41978478FD26D5FD6B66D81  

Cookie
^^^^^^

::

  GET /drive/documents?skip=10&take=10
  Host: api.kontur.ru
  Accept: application/json
  Cookie: auth.sid=FE6CFF8BE5E5B548AB1971874886D5C30E85D9BFA41978478FD26D5FD6B66D81

Примечания
^^^^^^^^^^

* Передачу через заголовок Authorization рекомендуется считать приоритетней, чем через Cookie.  
* Параметры auth.sid следует считать регистронезависимыми в каждом способе.

