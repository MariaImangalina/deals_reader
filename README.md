_Веб-сервис для обработки csv-файлов со списком сделок_

## Запуск проекта

1. Клонировать репозиторий
```
git clone https://github.com/MariaImangalina/deals_reader.git
```
2. Запустить сборку контейнеров
```
docker-compose up
```

## Работа с проектом

### URL http://localhost:8000/api/deal/ принимает два метода:

1. POST принимает единственный аргумент data: csv-файл для занесения данных в БД. 
    Возвращает статус операции
2. GET не требует аргументов, возвращает список из 5 клиентов, потративших наибольшую сумму за весь период и их данные:
```
{
    "response": [
        {
            "username": "resplendent",
            "spent_money": 451731,
            "gems": [
                "Сапфир",
                "Танзанит",
                "Рубин"
            ]
        },
        {
            "username": "bellwether",
            "spent_money": 217794,
            "gems": [
                "Сапфир",
                "Петерсит"
            ]
        },
        {
            "username": "uvulaperfly117",
            "spent_money": 120419,
            "gems": [
                "Танзанит",
                "Петерсит"
            ]
        },
        {
            "username": "braggadocio",
            "spent_money": 108957,
            "gems": [
                "Изумруд"
            ]
        },
        {
            "username": "turophile",
            "spent_money": 100132,
            "gems": [
                "Изумруд",
                "Рубин"
            ]
        }
    ]
}
```

