# AtomicHabits

В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и
искоренению старых плохих привычек.
<br/>
Данный проект представляет из себя бэкенд-часть SPA веб-приложения, реализующая напоминания пользователям о
необходимости выполнения действий для выработки привычек
<br/><br/>
<h4>В проекте реализован следующий функционал:</h4>

- Регистрация<br/>
- Авторизация посредством bearer токена<br/>
- Создание привычки<br/>
- Вывод списка привычек текущего пользователя с пагинацией<br/>
- Просмотр привычки (для создателя или для всех зарегистрированных если привычка публичная)<br/>
- Вывод списка публичных привычек<br/>
- Редактирование привычки (для создателя)<br/>
- Удаление привычки (только для создателя)<br/>
  <br/><br/>
  В проекте предусмотренны настройки безопасности CORS. По умолчанию, доступ к приложению только с localhost
  <br/><br/>

<h4>Ограничения:</h4>

- Исключен одновременный выбор связанной привычки и указания вознаграждения<br/>
- При обновлении значений "вознаграждение" и "связанная привычка", будет сохранено только одно из этих значений.
  Сохранится введенное, существующее будет очищено<br/>
- Время выполнения должно быть не больше 120 секунд<br/>
- В связанные привычки могут попадать только привычки с признаком приятной привычки<br/>
- У приятной привычки не может быть вознаграждения или связанной привычки<br/>
- Нельзя выполнять привычку реже, чем 1 раз в 7 дней<br/>
  <br/><br/>

<h3>Запуск проекта:</h3>

1. Клонируйте репозиторий;
2. Создайте Telegram бота и получите его токен;
3. Создайте в корне проекта и заполните файл .env:

    ```
    SECRET_KEY=
    
    USER_NAME=
    PASSWORD=
    HOST=
    PORT=
    
    REDIS_LOCATIO=
    
    BOT_HOST=
    BOT_TOKEN=
    ```
4. Установите docker или проверьте его наличие командой, также перейдите в файл проекта:

   ```
   docker --version
   ```
   ```
   cd backend_habits
   ```

5. Запустите проект командой:

   ```
   docker compose -d --build
   ```

6. Для получения документации, запустите проект и при помощи браузера перейдите по адресу:
   http://127.0.0.1:8000/api/schema/swagger-ui/ или http://127.0.0.1:8000/api/schema/redoc/
   <br/><br/>

Проект готов к заполнению базы данных.

<h3>Инструкция для быстрого заполнения базы данных:</h3>

<h4>Заполнение базы данных из фикстур</h4>

```bash
python3 manage.py loaddata dumpdata_30-06-2024.json
```

<h3>Описание логики проекта</h3>

При создании привычки, если указана tg_mailing = True,
создаётся периодическая задача рассылки напоминаний в телеграм через бота,
токен от которого надо получить у [BotFather](https://t.me/BotFather).

tg_mailing отвечает за рассылку пользователю пуш сообщений. Если True - рассылка есть, иначе - нет.
Можно менять tg_mailing, от чего меняется или удаляется периодическая задача.
Например при смене времени старта в привычке, изменится и время старта в периодической задаче привычки

<h3>Пункты, реализованные в проекте</h3>

- Настроили CORS.
- Настроили интеграцию с Телеграмом.
- Реализовали пагинацию.
- Использовали переменные окружения.
- Все необходимые модели описаны или переопределены.
- Все необходимые эндпоинты реализовали.
- Настроили все необходимые валидаторы.
- Описанные права доступа заложены.
- Настроили отложенную задачу через Celery.
- Проект покрыли тестами как минимум на 80%.
- Код оформили в соответствии с лучшими практиками.
- Имеется список зависимостей.
- Результат проверки Flake8 равен 100%, при исключении миграций.
- Решение выложили на GitHub.
