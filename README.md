# python-flask-docker
Итоговый проект курса "Машинное обучение в бизнесе"

Стек:

ML: sklearn, pandas, numpy
API: flask
Данные: https://mlbootcamp.ru/ru/round/12/sandbox/

Задача: предсказать наличие сердечно-сосудистых заболеваний по результатам классического врачебного осмотра. Бинарная классификация

Используемые признаки:

 - Возраст
 - Рост
 - Вес
 - Холестерин
 - Курение
 - Употребление Алкоголя
 - Физическая активность

Преобразования признаков: standardScaler

Модель: logreg

### Клонируем репозиторий и создаем образ
```
$ git clone https://github.com/artcom5/ml_business/tree/lesson9.git
$ cd ml_cardio
$ docker build -t artcom/ml_cardio .
```

### Запускаем контейнер

Здесь Вам нужно создать каталог локально и сохранить туда предобученную модель (<your_local_path_to_pretrained_models> нужно заменить на полный путь к этому каталогу)
```
$ docker run -d -p 8180:8180 -p 8181:8181 -v <your_local_path_to_pretrained_models>:/app/app/models artcom/ml_cardio
```

### Переходим на localhost:8181
