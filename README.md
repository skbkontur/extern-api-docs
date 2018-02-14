# extern-api-docs
Документация по работе с API Контур.Экстерна

## Назначение
API Контур.Экстерна состоит из нескольких частей: работы с учетными данными, с черновиками документооборота и документооборотами.
В документации описаны схемы работы для каждой части и приведены примеры. Методы API подробнее рассмотрены в сваггере.

## Схема работы
Работа с API состоит из следующих частей:
1. [Аутентификация и заведение учетных данных](https://github.com/skbkontur/extern-api-docs/blob/master/%D0%90%D1%83%D1%82%D0%B5%D0%BD%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F%20%D0%B8%20%D0%B7%D0%B0%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%83%D1%87%D0%B5%D1%82%D0%BD%D1%8B%D1%85%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85.md)
2. [Черновик документооборота](https://github.com/skbkontur/extern-api-docs/blob/master/%D0%A7%D0%B5%D1%80%D0%BD%D0%BE%D0%B2%D0%B8%D0%BA%20%D0%94%D0%9E.md)
3. [Работа с документооборотами](https://github.com/skbkontur/extern-api-docs/blob/master/%D0%A0%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%20%D1%81%20%D0%94%D0%9E.md)
4. [Входящий документооборот](https://github.com/skbkontur/extern-api-docs/blob/master/%D0%92%D1%85%D0%BE%D0%B4%D1%8F%D1%89%D0%B8%D0%B9%20%D0%94%D0%9E.md)  

![Схема](https://github.com/skbkontur/extern-api-docs/blob/master/keapi.png)


## Примеры работы с API
- [Организация отправляет отчет сама за себя](https://github.com/skbkontur/extern-api-docs/blob/master/examples/%D0%9F%D1%80%D0%BE%D1%81%D1%82%D0%B0%D1%8F%20%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0%20%22%D0%A1%D0%B0%D0%BC%20%D0%B7%D0%B0%20%D1%81%D0%B5%D0%B1%D1%8F%22.md)
- [Отправитель и налогоплательщик разные лица, прикладывается несколько документов, возникает ошибка при отправке](https://github.com/skbkontur/extern-api-docs/blob/master/examples/%D0%9E%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0%20%D0%B7%D0%B0%20%D0%B4%D1%80%D1%83%D0%B3%D1%83%D1%8E%20%D0%BE%D1%80%D0%B3%D0%B0%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8E%20%D1%81%20%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F%D0%BC%D0%B8%20%D0%B8%20%D0%BE%D1%88%D0%B8%D0%B1%D0%BA%D0%BE%D0%B9%20%D0%BF%D1%80%D0%B8%20%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B5.md)
- [Отправка с поэтапным прохождением проверки и подготовки, падение при подготовке](https://github.com/skbkontur/extern-api-docs/blob/master/examples/%D0%9E%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0%20%D0%B7%D0%B0%20%D0%B4%D1%80%D1%83%D0%B3%D1%83%D1%8E%20%D0%BE%D1%80%D0%B3%D0%B0%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8E%20%D0%BF%D0%BE%D1%8D%D1%82%D0%B0%D0%BF%D0%BD%D0%BE%20%D1%81%20%D0%BE%D1%88%D0%B8%D0%B1%D0%BA%D0%BE%D0%B9%20%D0%BF%D1%80%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%B3%D0%BE%D1%82%D0%BE%D0%B2%D0%BA%D0%B5.md)
- [Работа со списком документооборотов, применение фильтров](https://github.com/skbkontur/extern-api-docs/blob/master/examples/%D0%A0%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%20%D1%81%D0%BE%20%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%B0%D0%BC%D0%B8%20%D0%94%D0%9E.md)
- [Работа с отдельным документооборотом](https://github.com/skbkontur/extern-api-docs/blob/master/examples/%D0%A0%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%20%D1%81%20%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%BE%D0%B1%D0%BE%D1%80%D0%BE%D1%82%D0%BE%D0%BC.md)


## Терминология
Документооборот — регламентированная последовательность обмена документами между субъектом и контролирующим органом.  
 Например, документооборот появляется, когда организация сдаёт отчеты в ФНС или другие контролирующие органы.
