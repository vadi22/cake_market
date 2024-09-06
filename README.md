# Cake Market

## Стек технологий:
- Flask
-- Flask-Login
-- Flask_Migrate
-- Bootstrap
- SQLAlchemy
- PostgreSQL

## Порядок работы:

	1) Взять задачу из Project. Перетащить из Tasks в On going.
	2) git checkout dev_task - создать отдельную ветку вида dev_task, где task - решаемая сейчас задача (карточка в Project)
	3) git pull --rebase origin dev - взять все изменения из ветки dev.
	4) Выполнить задачу
	5) git commit -m "task" - Оставляем комментарий с названием задачи.
	6) git push - Отправляем ветку в GitHub
	7) Сделать pull request на эту новую ветку и скинуть в чат Телеграмм

## Модели проекта

![Структура данных](https://putilych.shn-host.ru/DB_cake_market.jpg)

## Создание и управление миграцией

Активируем и отправляем апдейт из последней версии
```
export FLASK_APP=webapp && export FLASK_ENV=development && flask db stamp head && flask db migrate && flask db upgrade
```
