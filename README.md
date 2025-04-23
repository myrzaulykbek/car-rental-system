Car Rental System — Django проект по аренде авто

Car Rental System — это веб-приложение, вдохновлённое Yandex Drive,
позволяющее пользователям арендовать автомобили онлайн по классам 
(Стандарт, Люкс, Электро). Проект создан в рамках финальной работы по Python в IITU.


📌 Краткий обзор

1 Аутентификация и регистрация пользователей (JWT)

2 Фильтрация по дате, времени и классу авто

3 Система бронирования с защитой от двойной аренды

4 Поддержка оплаты (Kaspi, Halyk, Stripe, наличные)

5 Уникальный UI для клиентов (стили Tailwind)

6 Админ-панель для управления машинами, заказами и отзывами

7 Реализация REST API с фильтрацией и CRUD


Установка проекта

1)Клонируй репозиторий

git clone https://github.com/myrzaulykbek/car-rental-system.git
cd car-rental-system

2)Создай виртуальное окружение и активируй его

python -m venv venv
venv\Scripts\activate  # Windows

3)Установи зависимости

pip install -r requirements.txt

4)Выполни миграции и создай суперпользователя

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

5)Запусти сервер
python manage.py runserver



Структура проекта (основное)

car_rental/
├── main/
│   ├── models.py      # Модели: Car, Booking, Rental, Payment
│   ├── views.py       # Представления (UI + API)
│   ├── serializers.py # DRF сериализаторы
│   ├── urls.py        # Роутинг приложения
│   ├── templates/     # HTML-шаблоны с Tailwind
├── car_rental/        # Настройки Django
├── media/             # Фото машин
├── manage.py
└── README.md

Уникальные фишки проекта

1 Подключение платёжных систем: Stripe, Kaspi, Halyk

2 Фильтрация машин по занятости (анализ даты и брони)

3 Система отзывов и рейтингов на каждую машину

4️ Роли пользователей: клиент, админ

5 Отчёты и аналитика для админов (в разработке)

Авторы проекта
Ернар Тагабай — Backend, UI клиентской части, документация

Мырзаулыбек Тагабай — Бронирование, база данных, система рейтингов

Лицензия

Проект создан в образовательных целях для защиты в IITU — Python (2025).

