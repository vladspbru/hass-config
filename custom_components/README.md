# ha-rhvoice-tts

Для работы необходимо иметь запущенный инстанс докер-контейнера git@github.com:mgarmash/rhvoice-rest.git

Запускать можно где угодно (но с пересборкой контейнера). По ресурсам на R-PI и прочих мелких железках может быть тяжко.

Пример запуска на одной машине с HA

`docker run -d -p 8080:8080 mgarmash/rhvoice-rest`

Проверить можно вот так (должно вернуть mp3-поток)

http://localhost:8080/say?text=123

Принимаются только два параметра: 
`text` - URL-encoded строка  
`voice` - имя голоса для RHVoice (полный список тут https://github.com/Olga-Yakovleva/RHVoice/wiki/Latest-version-%28Russian%29)

Каталог `tts` из этого репозитория складываем в поддиректорию где расположен конфиг HA `custom_components` 

Пример конфига для HA:

```
tts:
  - platform: rhvoice
    voice: anna
    url: http://localhost:8080/say 
```

# TODO
 - Написать нормальную доку
 - Сделать PR в home-assistant.io
 
# Links
 - https://github.com/vantu5z/RHVoice-dictionary
 - https://github.com/Olga-Yakovleva/RHVoice