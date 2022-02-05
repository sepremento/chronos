# Chronos

Простой тайм-трекер для учёта времени и задач. Предназначен для расширения на
различные интерфейсы. Код находится в `src/chronologger.py`. Файл `chronos`
содержит pyrogram-приложение для взаимодействия с API Telegram.

Установка `pyrogram`:

```
pip install pyrogram
```

Настройка параметров для работы приложения описана в разделе [Quick
Start](https://docs.pyrogram.org/intro/quickstart) документации pyrogram. Для
работы нужно получить секреты `API_ID` и `API_HASH`


Секреты подтягиваются из переменных окружения `TELEGRAM_API_ID` и
`TELEGRAM_API_HASH`. 

## Оформление в виде сервиса

Секреты можно прописать в файле в формате `key=value`, а затем прописать
следующую службу systemd в директории `/etc/systemd/system/`:

```
[Unit]
Description=Chronometer for daily tasks
After=multi-user.target

[Service]
Type=simple
Restart=always
EnvironmentFile=<<путь до файла с секретами>>
ExecStart=<<путь до исполняемого файла chronos>>

[Install]
WantedBy=multi-user.target
```

Затем запустить только что созданную службу `chronos`

```bash
sudo systemctl daemon-reload
sudo systemctl start chronos.service
sudo systemctl status chronos.service  # проверяем, что запустилось
```

Для контроля за работой программы можно смотреть журналы systemd:

```bash
journalctl -u chronos.service -f
```
