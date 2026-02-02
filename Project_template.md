## Я удалил текстовки заданий, просто чтобы мне было удобнее редачить .md, но я сохранил его копию, для удобства 

```markdown
[Старый Project_template](Project_template_old.md)
```

## Задание 1

__В этом задани надо было спроектировать to be архитектуру КиноБездны__

Моя схема немного отличается от того что пришлось реализовать в данном спринте
А именно:
  - В качестве сервиса с которым стоит общаться по "очереди" у меня Recommendation Service, а в задании просто events
  - Добавлены сервисы отвечающие за свою область: Subscription, Payment, User
В целом схема относительно простая, так что это скорее To-Be (MVP) для  желаемого продукта
```markdown
[ссылка на файл](schemas/index.puml)
```


## Задание 2
__В этом задани надо было реализовать MVP сервис events который общается с кафкой и proxy__


[Логи из postman я запустил в копознике, просто мне так было удобнее]

<img src="screenshots/Логи для задания 2 - postman.png" width="600" alt="Описание">

[Топики Kafka movie-events]

<img src="screenshots/Топики Kafka-1.png" width="600" alt="Описание">

[Топики Kafka payment-events]

<img src="screenshots/Топики Kafka-2.png" width="600" alt="Описание">
Есть еще топик user-events - но там все тоже самое, что и в первых двух скриншотах, имеется ввиду, все работает, поэтому для удобства я приложил всего 2 скриншота

## Задание 3
__В этом задани надо было создать CI/CD для github и поднять кубер запустить там все и вызвать api-tests__

Результат работы github\workflows можно глянуть в пулреквесте

[Логи из кубера]

<img src="screenshots/Логи из кубера.png" width="600" alt="Описание">

Логи из постмана для "movies", хост неймспейса cinemaabyss.example.com - типа кубер

<img src="screenshots/Вывод мувиков из постман.png" width="600" alt="Описание">

## Задание 4
__В этом задани надо было поднять кубер и заполнить его манифестами Helm-chart и просто обратиться с запросом get:api/movies__

Логи из helm

<img src="screenshots/Логи из helm.png" width="600" alt="Описание">

Логи из постмана для "movies", хост неймспейса cinemaabyss.example.com

<img src="screenshots/Вывод мувиков из постман для задания 4.png" width="600" alt="Описание">

# Задание 5
__В этом задани надо было поднять istio и создать circuit breaker, после чего вывести логи того как работают правила__

Метрика из istio

<img src="screenshots/Метрика из istio.png" width="600" alt="Описание">

Логи из istio с circuit breaker

<img src="screenshots/Логи istio.png" width="600" alt="Описание">

Еще логи из istio с circuit breaker

<img src="screenshots/Еще логи istio.png" width="600" alt="Описание">