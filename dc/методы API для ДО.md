# Методы API Контур.Экстерна для работы с документооборотами
Подробная спецификация методов показана в сваггере в разделе [Docflows](http://extern-api.testkontur.ru/swagger/ui/index#/Docflows).

Список доступных методов:
* [Получение списка документооборотов](#get-dcs)
* [Получение документооборота](#get-dc)
* [Получение списка документов документооборота](#get-docs)
* [Получение документа](#get-doc)
* [Получение описания документа](#get-doc-desc)
* [Получение зашифрованного контента документа](#get-enc-doc-content)
* [Получение расшифрованного контента документа](#get-dec-doc-content)
* [Получение подписей под документом](#get-doc-signs)
* [Получение конкретной подписи под документом](#get-doc-sign)
* [Получение контента конкретной подписи под документом](#get-doc-sign-content)
* [Генерация ответного документа](#get-reply-doc)
* [Отправка ответного документа](#post-reply-doc)
* [Печать документов](#get-print-doc)

------

<a name="get-dcs"></a>
### Получение списка документооборотов 
Метод: [GET DocflowsAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocflowsAsync).

С помощью этого метода можно получить список всех документооборотов учетной записи, при этом можно применить различные фильтры, чтобы получить необходимую выборку интересных на данный момент документооборотов. В ответе получает список документооборотов с необходимой мета-информацией по ним.

------

<a name="get-dc"></a>
### Получение документооборота 
Метод: [GET DocflowAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocflowAsync).

С помощью этого метода можно получить всю информацию о документообороте, такую как:
* его текущий статус
* мета-информацию документооборота
* перечень всех документов, созданных в ходе документооборота, на данный момент
* и многое другое, полный ответ можно посмотреть в сваггере

Если текущий статус документооборота подразумевает необходимость отправки ответного документа в контролирующий орган, среди ссылок в ответе этого метода будет ссылка на метод [GET ReplyDocumentAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetReplyDocumentAsync).

------

<a name="get-docs"></a>
### Получение списка документов документооборота 
Метод: [GET DocumentsAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocumentsAsync).

С помощью этого метода можно получить данные всех документов, созданных и полученных в ходе документооборота.

------

<a name="get-doc"></a>
### Получение документа 
Метод: [GET DocumentAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocumentAsync).

C помощью этого метода можно получить отдельный документ, созданный или полученный в ходе документооборота, с его описанием и контентами.

------

<a name="get-doc-desc"></a>
### Получение описания документа 
Метод: [GET DocumentDescriptionAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocumentDescriptionAsync).

Данный метод позволяет отдельно получить описание документа, входящего в документооборот.

------

<a name="get-enc-doc-content"></a>
### Получение зашифрованного контента документа 
Метод: [GET EncryptedDocumentContentAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetEncryptedDocumentContentAsync).

------

<a name="get-dec-doc-content"></a>
### Получение расшифрованного контета документа 
Метод: [GET DecryptedDocumentContentAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDecryptedDocumentContentAsync).

Наличие расшифрованного контента возможно не для всех документов.

------

<a name="get-doc-signs"></a>
### Получение подписей под документом 
Метод: [GET DocumentSignaturesAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocumentSignaturesAsync).

В некоторых случаях у документа может быть несколько подписей. В ответе будут возвращены все подписи под запрашиваемым документом.

------

<a name="get-doc-sign"></a>
### Получение конкретной подписи под документом 
Метод: [GET DocumentSignatureAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocumentSignatureAsync).

В ответе будет метаинфомарция подписи и ссылка на её контент.

------

<a name="get-doc-sign-content"></a>
### Получение контента конкретной подписи под документом 
Метод: [GET DocumentSignatureContentAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocumentSignatureContentAsync).

------

<a name="get-reply-doc"></a>
### Генерация ответного документа 
Метод: [GET ReplyDocumentAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetReplyDocumentAsync).

Документооборот подразумевает под собой последовательный обмен определенными документами согласно регламенту. Поэтому в ответ на получаемые от контролирующего органа документы необходимо отправлять определенные ответные документы. Этот метод помогает формировать подобные документы. Также необходимые ссылки для формирования нужных документов будут появляться в работе с методом [GET DocflowAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocflowAsync).

------

<a name="post-reply-doc"></a>
### Отправка ответного документа 
Метод: [POST ReplyDocumentAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_SendReplyDocumentAsync).

После работы с методом [GET ReplyDocumentAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetReplyDocumentAsync) полученный в результате документ необходимо подписать, и вместе с подписью направить в контролирующий орган. С помощью этого метода это можно сделать. Также ссылка на этот метод будет в ответе предыдущего метода [GET ReplyDocumentAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetReplyDocumentAsync).

------

<a name="get-print-doc"></a>
### Печать документов 
Метод: [GET DocumentPrintAsync](http://extern-api.testkontur.ru/swagger/ui/index#!/Docflows/Docflows_GetDocumentPrintAsync)

Можно получить печатную форму любого формализованного документа в документообороте. Печать документов происходит только после проверки подписей под печатаемыми документами, тем самым подтверждается валидность и неизменность печатаемых документов.
