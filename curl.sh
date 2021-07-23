# Инициализация сетки
curl -i -X GET -H 'Accept: application/json; indent=1' http://127.0.0.1:8000/init_grid/

# Добавление огранизаций
curl -i -X POST -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json; indent=1' -d '{
  "name": "ЛифтМастер",
  "email": "liftmaster@mail.ru",
  "phone": "74950000001",
  "address": "г. Москва, ул. Лифтовая, д. 5"
}' http://127.0.0.1:8000/organisations/
curl -i -X POST -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json; indent=1' -d '{
  "name": "РемЛифт",
  "email": "remlift@mail.ru",
  "phone": "74950000002",
  "address": "г. Москва, ул. Лифтовая, д. 15"
}' http://127.0.0.1:8000/organisations/
curl -i -X POST -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json; indent=1' -d '{
  "name": "Водолей",
  "email": "vodolei@mail.ru",
  "phone": "74950000004",
  "address": "г. Москва, ул. Водная, д. 35"
}' http://127.0.0.1:8000/organisations/

# Список огранизаций
curl -i -X GET -H 'Accept: application/json; indent=1' http://127.0.0.1:8000/organisations/
# Информация по огранизации
curl -i -X GET -H 'Accept: application/json; indent=1' http://127.0.0.1:8000/organisation/1/

# Изменение огранизации
curl -i -X PUT -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json; indent=1' -d '{
  "name": "ЛифтМастер",
  "email": "liftmaster@mail.ru",
  "phone": "74950000001",
  "address": "г. Москва, ул. Лифтовая, д. 6"
}' http://127.0.0.1:8000/organisation/1/

# Удаление огранизации
curl -i -X DELETE http://127.0.0.1:8000/organisation/3/


# Услуги
curl -i -X POST -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json; indent=1' -d '{
  "name": "Обслуживание лифтов"
}' http://127.0.0.1:8000/services/
curl -i -X POST -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json; indent=1' -d '{
  "name": "Монтаж лифтов"
}' http://127.0.0.1:8000/services/

# Список услуг
curl -i -X GET -H 'Accept: application/json; indent=1' http://127.0.0.1:8000/services/


# Добавление областей для огранизаций
curl -i -X POST -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json; indent=1' -d '{
  "organisation": 1,
  "name": "Область 1",
  "polygon": {
    "type": "Polygon",
    "coordinates": [
      [
        [
          37.74078369140625,
          55.97072426231743
        ],
        [
          37.59246826171875,
          55.94919982336744
        ],
        [
          37.61993408203125,
          55.85989956952263
        ],
        [
          37.79296875,
          55.85219164310742
        ],
        [
          37.82592773437499,
          55.947661905375064
        ],
        [
          37.74078369140625,
          55.97072426231743
        ]
      ]
    ]
  }
}' http://127.0.0.1:8000/areas/
curl -i -X POST -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json; indent=1' -d '{
  "organisation": 2,
  "name": "Область 2",
  "polygon": {
    "type": "Polygon",
    "coordinates": [
      [
        [
          37.7215576171875,
          55.88917574736247
        ],
        [
          37.606201171875,
          55.76266790754882
        ],
        [
          37.85064697265625,
          55.76112258901995
        ],
        [
          37.7215576171875,
          55.88917574736247
        ]
      ]
    ]
  }
}' http://127.0.0.1:8000/areas/
curl -i -X POST -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json; indent=1' -d '{
  "organisation": 1,
  "name": "Область 3",
  "polygon": {
    "type": "Polygon",
    "coordinates": [
      [
        [
          38.04016113281249,
          56.013737238856876
        ],
        [
          38.11431884765624,
          55.941509622565505
        ],
        [
          38.23516845703124,
          56.02755267625243
        ],
        [
          38.04016113281249,
          56.013737238856876
        ]
      ]
    ]
  }
}' http://127.0.0.1:8000/areas/
curl -i -X POST -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json; indent=1' -d '{
  "organisation": 1,
  "name": "Область 4",
  "polygon": {
    "type": "Polygon",
    "coordinates": [
      [
        [
          37.760009765625,
          55.547280698640805
        ],
        [
          37.694091796875,
          55.49597142581549
        ],
        [
          37.8533935546875,
          55.48352273618202
        ],
        [
          37.760009765625,
          55.547280698640805
        ]
      ]
    ]
  }
}' http://127.0.0.1:8000/areas/

# Удаление области
curl -i -X DELETE http://127.0.0.1:8000/area/4/


# Добавление цен
curl -i -X POST -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json; indent=1' -d '{
  "service": 1,
  "area": 1,
  "value": 500
}' http://127.0.0.1:8000/costs/
curl -i -X POST -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json; indent=1' -d '{
  "service": 1,
  "area": 2,
  "value": 600
}' http://127.0.0.1:8000/costs/
curl -i -X POST -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json; indent=1' -d '{
  "service": 2,
  "area": 2,
  "value": 1600
}' http://127.0.0.1:8000/costs/
curl -i -X POST -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json; indent=1' -d '{
  "service": 2,
  "area": 3,
  "value": 1500
}' http://127.0.0.1:8000/costs/
curl -i -X GET -H 'Accept: application/json; indent=1' http://127.0.0.1:8000/costs/


# Информация по точке, попадающей в две области
curl -i -X GET -H 'Accept: application/json; indent=1' http://127.0.0.1:8000/coordinate_info/latitude=37.7215576171875\&longitude=55.867605966997786/
# Информация по точке, попадающей в две области
curl -i -X GET -H 'Accept: application/json; indent=1' http://127.0.0.1:8000/coordinate_info/latitude=38.11981201171875\&longitude=55.995308966233/
# Информация по точке, находящейся в ячейке сетки с областями, но не попадающей ни в одну из областей
curl -i -X GET -H 'Accept: application/json; indent=1' http://127.0.0.1:8000/coordinate_info/latitude=37.85064697265625\&longitude=55.866064809810105/
# Информация по точке, не попадающей ни в одну из областей
curl -i -X GET -H 'Accept: application/json; indent=1' http://127.0.0.1:8000/coordinate_info/latitude=38.2598876953125\&longitude=55.66054546266747/


# Реинициализация сетки после правки ее параметров в settings.py
curl -i -X GET -H 'Accept: application/json; indent=1' http://127.0.0.1:8000/init_grid/

# Все по прежнему работает.
# Информация по точке, попадающей в две области
curl -i -X GET -H 'Accept: application/json; indent=1' http://127.0.0.1:8000/coordinate_info/latitude=37.7215576171875\&longitude=55.867605966997786/
# Информация по точке, попадающей в две области
curl -i -X GET -H 'Accept: application/json; indent=1' http://127.0.0.1:8000/coordinate_info/latitude=38.11981201171875\&longitude=55.995308966233/
# Информация по точке, находящейся в ячейке сетки с областями, но не попадающей ни в одну из областей
curl -i -X GET -H 'Accept: application/json; indent=1' http://127.0.0.1:8000/coordinate_info/latitude=37.85064697265625\&longitude=55.866064809810105/
# Информация по точке, не попадающей ни в одну из областей
curl -i -X GET -H 'Accept: application/json; indent=1' http://127.0.0.1:8000/coordinate_info/latitude=38.2598876953125\&longitude=55.66054546266747/
