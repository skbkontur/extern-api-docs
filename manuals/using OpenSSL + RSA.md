Проверено для Windows с версией 1.0.2/

**Команда формирования подписи:** ```openssl.exe cms -sign -signer publickey.pem -inkey private.pem -binary -in data.txt -outform der -out data.sig -passin pass:password```, где:
* publickey.pem - публичная часть ключа RSA (публичный сертификат),
* private.pem - приватная часть ключа RSA,
* password - пароль для контейнера ключа RSA,
* data.txt - файл содержащий строку инициализации доверительной аутентификации,
* data.sig - файл в который будет выведен результат формирования подписи,
