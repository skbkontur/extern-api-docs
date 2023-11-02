.. _`OpenID Connect`: https://openid.net/specs/openid-connect-core-1_0.html
.. _`открытый`: https://identity.testkontur.ru/.well-known/openid-configuration/jwks

.. _rst-markup-access-token:

Аутентификация OpenID Connect
=============================

.. toctree::
   :maxdepth: 2
   :hidden:
   
   api-key
   authorization_code_flow
   device_flow
   trusted

Для работы с API Контур.Экстерна необходимо:

* :doc:`api-key</auth_oidc/api-key>`;
* :doc:`client_id</auth_oidc/api-key>`;
* Access Token.

Аутентификация в API происходит с помощью сервиса OpenID Провайдер. Сервис реализует протокол аутентификации OpenID Connect и помогает получить Access Token.

**Что такое OpenID Connect**

Аутентификация – подтверждение личности конечного пользователя и его свойств. В Контуре аутентификация основана на протоколе OpenID Connect.

Почему OpenID:

* аутентификация конечного пользователя происходит с помощью Access Token;
* OpenID Connect поддерживает несколько способов получения токенов:

    * :doc:`аутентификация по коду подтверждения</auth_oidc/authorization_code_flow>` через authorization code flow;
    * :doc:`аутентификация по веб-ссылке</auth_oidc/device_flow>` через device flow.

* OpenID Connect не работает с cookies на домене конечного пользователя.

В Контуре процесс аутентификации обеспечивает OpenID Провайдер.

**Что такое OpenID Провайдер**

OpenID Провайдер – аутентификационный сервер, который реализует протокол OpenID Connect и выдает Access Token.

Стоит отметить, что аутентификация для всех продуктов Контура единая. Получение Access Token происходит вне API Контур.Экстерна, а в отдельном API OpenID Провайдера:

* рабочая площадка: https://identity.kontur.ru ;
* тестовая площадка: https://identity.testkontur.ru .

**Что такое Access Token**

Access Token – некоторый идентификатор, который позволяет идентифицировать пользователя и выполнять действия от его имени в API. Для получения Access Token нужен :doc:`api-key и client_id</auth_oidc/api-key>`.

Токен передается в **header parametres**:

::

    Authorization: Bearer <token>

Access Token можно получить с помощью API OpenID Провайдера. Есть несколько способов получения токенов:

* :doc:`authorization code flow</auth_oidc/authorization_code_flow>` – для приложений с серверной частью; 
* :doc:`device flow</auth_oidc/device_flow>` – для приложений, которые не имеют серверной части или напрямую взаимодействуют с API Контур.Экстерна, например, модуль 1С.

Для интеграции мы рекомендуем использовать **authorization code flow**.

**Порядок взаимодействия**

1. Авторизация приложения в OpenID Провайдер.
2. Получение Access Token.
3. Передача приложением токена в API Контур.Экстерн с каждым запросом.
4. Получение ответа на запрос от API Контур.Экстерна.

.. image:: /_static/auth_oidc.png
    :width: 700px
