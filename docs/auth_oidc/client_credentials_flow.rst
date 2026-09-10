.. _`документации OpenID Провайдера`: https://developer.kontur.ru/Docs/html/schemes/client_credentials_flow.html
.. _`api-key и service_name приложения`: https://developer.kontur.ru/doc/extern-api/auth_oidc/api-key.html
.. _`OpenID-провайдера`: https://developer.kontur.ru/doc/extern-api/auth_oidc/index.html
.. _`описании параметров Client Credentials Flow`: https://developer.kontur.ru/Docs/html/schemes/client_credentials_flow.html
.. _`разделе об аутентификации`: https://developer.kontur.ru/doc/extern-api/auth_oidc/index.html
.. _`документации Client Credentials Flow`: https://developer.kontur.ru/Docs/html/schemes/client_credentials_flow.html

Аутентификация через Client Credentials Flow
============================================

Для взаимодействия между сервисами можно получить Access Token с помощью **client credentials flow**. Для этого нужны реквизиты приложения: ``service_name`` и API-ключ. Участие пользователя для получения токена не требуется.

Приложение получает доступ в рамках выданных ему разрешений. Подробнее об алгоритме читайте в `документации OpenID Провайдера`_.

Получение Access Token
----------------------

Перед началом работы получите `api-key и service_name приложения`_.

Для получения токена отправьте запрос. Метод: POST /connect/token.

Адрес запроса зависит от площадки `OpenID-провайдера`_:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Площадка
     - Адрес запроса
   * - Боевая
     - `https://identity.kontur.ru/connect/token <https://identity.kontur.ru/connect/token>`_
   * - Тестовая
     - `https://identity.testkontur.ru/connect/token <https://identity.testkontur.ru/connect/token>`_

Используйте реквизиты приложения, выданные для выбранной площадки. 

**Параметры запроса**

Все параметры обязательные. Передавайте их в теле запроса с заголовком ``Content-Type: application/x-www-form-urlencoded``.

* ``grant_type`` — тип аутентификации. Укажите значение ``client_credentials``;
* ``client_id`` — сервисное имя приложения. Максимальная длина — 300 символов;
* ``client_secret`` — API-ключ приложения. Максимальная длина — 300 символов;
* ``scope`` — разрешения API, которые запрашивает приложение. Несколько значений укажите через пробел.

В ``scope`` можно передавать только разрешения API, доступные приложению. Пользовательские ``scope``, например ``openid``, ``profile`` и ``email``, передавать нельзя. Доступ к ``scope`` выдают владельцы API в Контур.Интеграторе. Подробнее смотрите в `описании параметров Client Credentials Flow`_.

**Пример запроса без scope**

.. code-block:: text

    POST /connect/token HTTP/1.1
    Host: identity.kontur.ru
    Content-Type: application/x-www-form-urlencoded

    grant_type=client_credentials&client_id={{service_name}}&client_secret={{api_key}}&scope={{scope}}

Замените ``{{service_name}}``, ``{{api_key}}`` и ``{{scope}}`` реквизитами приложения. Передавайте значения параметров в формате ``application/x-www-form-urlencoded``.

**Пример ответа**

При успешной аутентификации OpenID-провайдер вернет HTTP 200 и JSON с токеном.

.. code-block:: json

    {
      "access_token": "example_access_token",
      "token_type": "Bearer",
      "expires_in": 3600
    }

**Параметры ответа**

* ``access_token`` — токен доступа;
* ``token_type`` — тип токена. Всегда имеет значение ``Bearer``;
* ``expires_in`` — срок действия токена в секундах.

Значение ``3600`` приведено для примера. Используйте срок, который вернул OpenID-провайдер.

Использование токена
--------------------

При вызове методов API передавайте токен в HTTP-заголовке ``Authorization``, как описано в `разделе об аутентификации`_:

.. code-block:: text

    Authorization: Bearer <access_token>

Используйте токен в течение его срока действия. Чтобы получить новый токен, повторите запрос с ``grant_type=client_credentials``, сервисным именем и API-ключом.

Возможные ошибки
----------------

Если получить токен не удалось, OpenID-провайдер вернет JSON с полем ``error``. В `документации Client Credentials Flow`_ описаны следующие ошибки:

.. list-table::
   :header-rows: 1
   :widths: 15 30 55

   * - HTTP-код
     - ``error``
     - Причина
   * - 400
     - ``invalid_request``
     - Ошибка в составе или формате запроса.
   * - 400
     - ``invalid_client``
     - Не указаны либо неверны ``client_id`` или ``client_secret``.
   * - 400
     - ``invalid_scope``
     - Запрошенные ``scope`` некорректны или не подходят для выбранной схемы.

**Пример ответа с ошибкой**

.. code-block:: json

    {
      "error": "invalid_client"
    }
