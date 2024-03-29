Документооборот регистрации бизнеса
===================================

Данный раздел посвящен документообороту представления в налоговый орган документов для регистрации юридического лица (ЮЛ), физического лица в качестве индивидуального предпринимателя (ИП), внесении изменений в учредительные документы, ликвидации ЮЛ и прекращении деятельности ИП.

.. note:: Данный документооборот отличается от остальных тем, что он не требует отправки ответных документов, так как на момент отправки документов организации еще не существует. 

Допустимые форматы документов, которые пользователь может прикладывать к заявлению:

* TIFF/TIF;
* JPG/JPEG; 
* PNG;
* PDF.

Процесс работы с документооборотом
----------------------------------

Для регистрации физического лица в качестве ИП, регистрации ЮЛ, ликвидации ИП необходимо:

1. Создать в учетной записи новую организацию с ИНН физического лица. Метод :doc:`POST Organization</accounts/методы API для организаций>`. 

2. Подготовить файлы документов к отправке с помощью :doc:`DraftsBuilder</knowledge base/DraftsBuilder>` (сформировать черновик). Если все файлы уже приведены к нужному формату и есть файл описи, шаг можно пропустить.

3. Подготовить черновик к отправке, см. :doc:`Работа с черновиками</drafts/порядок работы с черновиками>`.

4. Отслеживать документооборот, см. :ref:`Статусы и порядок документооборота<rst-markup-business-reg-status>`. 
   Документы о регистрации либо отказе появятся в документообороте. Также они будут направлены на E-mail физического лица.

.. important:: Реквизиты Sender и Payer нужно заполнить данными физического лица, а документы подписывать его сертификатом. 

