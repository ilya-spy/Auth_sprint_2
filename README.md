# Проектная работа 7 спринта

Упростите регистрацию и аутентификацию пользователей в Auth-сервисе, добавив вход через социальные сервисы. Список сервисов выбирайте исходя из целевой аудитории онлайн-кинотеатра — подумайте, какими социальными сервисами они пользуются. Например, использовать [OAuth от Github](https://docs.github.com/en/free-pro-team@latest/developers/apps/authorizing-oauth-apps){target="_blank"} — не самая удачная идея. Ваши пользователи не разработчики и вряд ли имеют аккаунт на Github. А вот добавить Twitter, Facebook, VK, Google, Yandex или Mail будет хорошей идеей.

Вам не нужно делать фронтенд в этой задаче и реализовывать собственный сервер OAuth. Нужно реализовать протокол со стороны потребителя.

Информация по OAuth у разных поставщиков данных: 

- [Twitter](https://developer.twitter.com/en/docs/authentication/overview){target="_blank"},
- [Facebook](https://developers.facebook.com/docs/facebook-login/){target="_blank"},
- [VK](https://vk.com/dev/access_token){target="_blank"},
- [Google](https://developers.google.com/identity/protocols/oauth2){target="_blank"},
- [Yandex](https://yandex.ru/dev/oauth/?turbo=true){target="_blank"},
- [Mail](https://api.mail.ru/docs/guides/oauth/){target="_blank"}.

## Дополнительное задание

Реализуйте возможность открепить аккаунт в соцсети от личного кабинета. 

Решение залейте в репозиторий текущего спринта и отправьте на ревью.
## Разворачивание приложения для разработки

```
git clone git@github.com:merkushov/Auth_sprint_2.git

cd Auth_sprint_2

export ENV=dev
make dev/setup

# запуск интеграционных тестов
make test/run_integration

# доступные опции
make help
```

## Ручное тестирование интеграции AsyncAPI и AuthAPI

Два сервиса подняты в докер-контейнерах. Общаемся с ними через сервис Nginx

```shell
export ENV=dev

 # скачать и развернуть 4 репозитория микросервисов
 
# Админка
git clone git@github.com:merkushov/Admin_panel_sprint_2.git
cd Admin_panel_sprint_2
make dev/setup
make app/fake_data

cd ..

# ETL
git clone git@github.com:merkushov/ETL.git
cd ETL
make dev_setup

cd ..

# АПИ фильмов
git clone git@github.com:merkushov/Async_API_sprint_2.git
cd Async_API_sprint_2
make dev/setup

cd ..

# АПИ Авторизации
git clone git@github.com:merkushov/Auth_sprint_2.git
cd Auth_sprint_2
make dev/setup

cd ..

# после этого будет доступна единая точка входа к 3м интерфейсам 
# (Админка, АПИ фильмов, АПИ авторизации) на хостовой системе
#   localhost:80

# создать нового пользователя и залогиниться
curl -XPOST -H "Content-Type: application/json" http://localhost/auth_api/v1/user -d '{"username": "test_user","email": "test@gmail.com","password": "12345"}'

export AUTH_API_ACCESS_TOKEN=$(curl -s -XPOST -H "Content-Type: application/json" http://localhost/auth_api/v1/login -d '{"username": "test_user", "password": "12345"}' | jq '.access' | xargs -L 1)

# получить информацию по авторизованному пользователю, т.е. собственные данные
curl -XGET -H "Content-Type: application/json" -H "Authorization: Bearer $AUTH_API_ACCESS_TOKEN" http://localhost/auth_api/v1/me

# создать роли и привязать роль subscriber к пользователю
curl -XPOST -H "Content-Type: application/json" -H "Authorization: Bearer $AUTH_API_ACCESS_TOKEN" http://localhost/auth_api/v1/role -d '{"name": "user"}'
curl -XPOST -H "Content-Type: application/json" -H "Authorization: Bearer $AUTH_API_ACCESS_TOKEN" http://localhost/auth_api/v1/role -d '{"name": "subscriber"}'
curl -XPOST -H "Content-Type: application/json" -H "Authorization: Bearer $AUTH_API_ACCESS_TOKEN" http://localhost/auth_api/v1/user/0986e476-60c4-4d39-b59e-4927dd5f18c1/role/d71820c9-a053-4e1b-ad33-4b69c3f9d32e

# убедиться, что роль пользователю выдана
curl -XGET -H "Content-Type: application/json" -H "Authorization: Bearer $AUTH_API_ACCESS_TOKEN" http://localhost/auth_api/v1/me/roles

# запросить список фильмов
#   Ограничения: 
#    - неавторизованному пользователю будет доступны только первые 10 фильмов из списка
#    - авторизованный пользователь с ролью subscriber будет иметь доступ к полному списку
curl -XGET -H "Content-Type: application/json" -H "Authorization: Bearer $AUTH_API_ACCESS_TOKEN" http://localhost/async_api/v1/film/

# запрос с пэйджингом, доступным только авторизованному пользователю
curl -s -XGET  -H "Authorization: Bearer $AUTH_API_ACCESS_TOKEN" "http://localhost/async_api/v1/film/?page\[size\]=30&page\[number\]=2" | jq -r '.[].title'
```
