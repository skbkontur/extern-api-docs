Использование OpenSSL
=====================

Проверено для Windows с версией 1.0.2

**Команда формирования подписи:** 

``openssl.exe cms -sign -signer publickey.pem -inkey private.pem -binary -in data.txt -outform der -out data.sig -passin pass:password``, где:

* publickey.pem - открытая часть ключа RSA (публичный сертификат);
* private.pem - приватная часть ключа RSA;
* password - пароль для контейнера ключа RSA;
* data.txt - файл содержащий строку инициализации доверительной аутентификации;
* data.sig - файл в который будет выведен результат формирования подписи.

При необходимости можно **объединить закрытую и открытую часть ключа** для удобства работы с помощь команды: 

``openssl.exe pkcs12 -export -in publickey.pem -inkey private.pem -out pkcs12.p12``, где:

* publickey.pem - открытая часть ключа RSA (публичный сертификат),
* private.pem - приватная часть ключа RSA.

**Пример использования системной криптографии Windows (с использованием C#)**

::

  using System.Security.Cryptography.Pkcs;
  using System.Security.Cryptography.X509Certificates;
  using System.Threading.Tasks;
    
   namespace SignerApp
   {
     public class Signer
     {
       public async Task<byte[]> SignData(byte[] contentToSign)
       {
         var certificateWithPassword = new X509Certificate2(@"path\to\PKCS#12\Certificate", "password");
         ContentInfo content = new ContentInfo(contentToSign);
         SignedCms signedCms = new SignedCms(content, true);
         CmsSigner signer = new CmsSigner(SubjectIdentifierType.IssuerAndSerialNumber, certificateWithPassword);
         signedCms.ComputeSignature(signer);
         return signedCms.Encode();
         }
       }
     }

Генерация RSA сертификата
-------------------------

1. Откройте проводник и найдите директорию, где лежит openssl.exe;
2. Правой кнопкой мыши нажмите на файл openssl.exe и выберите пункт "Запуск от имени администратора";
3. Выполните следующую команду, чтобы сгенерировать сертификат и закрытый ключ:

``req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout privateKey.key -out certificate.crt``

4. Нужно будет ввести некоторую информацию для получения сертификата;
5. После выполнения команды файлы certificate.crt и privateKey.key будут лежать в директории с файлом openssl.exe.

После этого нужно **объединить закрытую и открытую часть ключа**  в формат .pfx/.p12, для этого выполните команду:

``pkcs12 -export -out certificate.pfx -inkey privateKey.key -in certificate.crt -certfile certificate.crt``

Полученный certificate.pfx можно использовать для работы. 