# Методы для работы с учетными записями
Подробная спецификация методов показана в сваггере в разделе [Accounts](http://extern-api.testkontur.ru/swagger/ui/index#/Accounts).

Список доступных методов:
* [Получение списка доступных учетных записей](#2)
* [Создание новой учетной записи](#3)
* [Получение конкретной учетной записи](#4)

------

<a name="2"></a>
### Получение списка всех доступных учетных записей 
Метод: [GET All](http://extern-api.testkontur.ru/swagger/ui/index#!/Accounts/Accounts_GetAll)

При вызове этого метода можно получить список доступных учетных записей авторизованного пользователя. Пользователь определяется по [auth.sid](https://github.com/skbkontur/extern-api-docs/blob/master/manuals/auth.sid.md) из запроса. 

Для [Компаний-Партнеров Контура](https://github.com/skbkontur/extern-api-docs/blob/master/scenarios/Компания-партнер%20Контура.md) и [дополнительно ещё и УЦ Контура](https://github.com/skbkontur/extern-api-docs/blob/master/scenarios/Компания-партнер%20Удостоверяющего%20центра%20Контура.md) отдельно происходит фильтрация доступных учетных записей согласно переданному в запросе [api-key](https://github.com/skbkontur/extern-api-docs/blob/master/manuals/api-key.md).

------

<a name="3"></a>
### Создание новой учетной записи 
Метод: [POST Account](http://extern-api.testkontur.ru/swagger/ui/index#!/Accounts/Accounts_Create)

**Доступен только** для работы в сценариях [Компаний-Партнеров Контура](https://github.com/skbkontur/extern-api-docs/blob/master/scenarios/Компания-партнер%20Контура.md) и [дополнительно ещё и УЦ Контура](https://github.com/skbkontur/extern-api-docs/blob/master/scenarios/Компания-партнер%20Удостоверяющего%20центра%20Контура.md). С помощью данного метода есть возможность создавать новые учетные записи для пользователей сервис Компаний-Партнеров, если организации этих пользователей ещё не существуют в Контур.Экстерне.

------

<a name="4"></a>
### Получение конкретной учетной записи 
Метод: [GET Account](http://extern-api.testkontur.ru/swagger/ui/index#!/Accounts/Accounts_Get)
