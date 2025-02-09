# 🛒 FlowerDelivery - Интернет-магазин цветов на Django

## 📌 О проекте
FlowerDelivery — это backend интернет-магазин для заказа и доставки цветов. Сайт поддерживает регистрацию пользователей, оформление заказов  и управление корзиной. Frontend - css, Bootstrap.

## 🚀 Функциональность
- 📦 Каталог товаров (букетов)
- 🛒 Корзина покупок
- ✅ Оформление заказа
- 🔑 Регистрация и авторизация пользователей
- ⚙️ Админ-панель Django для управления товарами и заказами


## 📂 Структура проекта

```
shop1
            
├───cart                # Приложение корзины
│   ├───migrations
│   ├───templates
│   │   └───cart
│   ├───tests
│   └───[...]         
├───catalog             # Приложение каталога товаров
│   ├───migrations
│   ├───static
│   │   └───catalog
│   ├───templates
│   │   └───catalog
│   └───[...]        
├───media               # Медиафайлы (изображения товаров)
│   └───products      
├───orders              # Приложение заказов
│   ├───migrations
│   ├───templates
│   │   └───orders
│   ├───tests
│   └───[...]         
├───shop1               # Основной конфигурационный каталог
│   ├───settings.py
│   ├───tests
│   └───[...]         
├───static              # Статические файлы (CSS, JS, изображения)    
│       
├───user   # Приложение пользователей
│   ├───migrations
│   ├───templates
│   │   └───user
│   ├───tests
│   └───[...]   └
│        
└───.env_example        # Пример файла с переменными окружения
```




## 🛠️ Установка и запуск
### 1️⃣ Клонирование репозитория
```bash
git clone https://github.com/your-repository/shop1.git
cd shop1
```

### 2️⃣ Создание виртуального окружения
```bash
python -m venv .venv
source .venv/bin/activate  # Для macOS/Linux
.venv\Scripts\activate     # Для Windows
```

### 3️⃣ Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4️⃣ Применение миграций и запуск сервера
```bash
python manage.py migrate
python manage.py runserver
```

## 🔑 Переменные окружения
Создайте файл `.env` на основе `.env_example` и укажите свои настройки базы данных, email-сервиса и т. д.

## 🛍️ Основные URL
| Раздел | URL |
|--------|----------------------|
| Главная страница | `/` |
| Каталог | `/catalog/` |
| Корзина | `/cart/` |
| Оформление заказа | `/orders/create/` |
| Личный кабинет | `/user/profile/` |

## 🏗️ Разработчики
👤 **Nora Serdyukova**  
✉️ Email: nora.serdyukova@gmail.com  
🔗 GitHub: [Noras2001](https://github.com/Noras2001)
