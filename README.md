# Receipt Manager

Telegram Mini App для автоматического справедливого разделения расходов в команде. Приложение упрощает процесс разделения счётов, объединяя OCR-распознавание, обработку на основе ИИ и интуитивное управление комнатами.

## Описание

Receipt Manager решает проблему справедливого разделения общих расходов в группе. Пользователи загружают фото чека, система автоматически извлекает позиции и цены с помощью OCR, а участники выбирают, что они заказывали. Приложение затем автоматически рассчитывает индивидуальные доли расходов.

Весь процесс работает в Telegram, что исключает необходимость установки отдельного приложения.

## Процесс работы

1. **Загрузить чек** - Пользователь фотографирует чек и загружает его через Telegram
2. **OCR-распознавание** - Система автоматически извлекает позиции, количество и цены
3. **Создать комнату** - Пользователь создаёт комнату и приглашает других участников
4. **Выбрать позиции** - Каждый участник отмечает, что он заказывал
5. **Автоматический расчёт** - Система рассчитывает доли каждого участника и считает долги

## Основные возможности

- Загрузка фото чека и автоматическое извлечение текста через OCR
- Интеллектуальное редактирование на основе ИИ ("удалить позицию X", "добавить чай 500р")
- Разделение расходов по комнатам с несколькими участниками
- Автоматический расчёт долгов и рекомендации по расчётам
- Поддержка преобразования речи в текст для голосовых заметок
- Интеграция с платформой Telegram Mini App

## Архитектура

Проект использует микросервисную архитектуру со следующими компонентами:

### Frontend
- **Технологии**: React, TypeScript, Vite
- **Назначение**: UI приложения Telegram Mini App для взаимодействия с пользователем

### Backend-сервисы
- **DB Service**: FastAPI + SQLAlchemy + PostgreSQL
  - Управление пользователями и комнатами
  - Хранение информации о чеках и позициях
  - Отслеживание состояния комнаты

- **ASR Service**: Преобразование речи в текст
  - Модель: Voxtral Mini (через OpenRouter)

- **OCR Service**: Обработка изображений и извлечение текста
  - Модель: Qwen 3.5 Vision Language
  - Конвейер предварительной обработки изображений

- **Executor Service**: Обработка запросов на основе ИИ
  - Оркестрация агентов на основе LangGraph
  - Модели: Qwen 3.5, x:AI Grok 3 (через OpenRouter)
  - Нечёткий поиск для интеллектуального сопоставления позиций
  - Аутентификация и авторизация через Telegram

### Инфраструктура
- **Message Broker**: Redis
- **База данных**: PostgreSQL
- **Контейнеризация**: Docker Compose для локальной разработки и развёртывания

## Требования

- Docker и Docker Compose
- Python 3.10+ (для локальной разработки)
- Node.js 18+ (для разработки frontend)
- API ключ OpenRouter
- Telegram Bot Token

## Установка и настройка

### Docker Compose

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd ReceiptManager
```

2. Создайте файл окружения для frontend:
```bash
cd apps/frontend
cp .env.example .env
```

3. Конфигурируйте переменные окружения:
```
VITE_API_URL=http://localhost:8000
VITE_ASR_API_URL=http://localhost:8002
```

4. Создайте файл окружения для DB service:
```bash
cd ../db-service
cp .env.example .env
```

Конфигурируйте:
```
DATABASE_URL=postgresql://user:password@db:5432/receipt_manager
REDIS_URL=redis://redis:6379
```

5. Создайте файл окружения для Executor service:
```bash
cd ../executor-service
cp .env.example .env
```

Конфигурируйте:
```
OPENROUTER_API_KEY=<your-api-key>
DATABASE_URL=postgresql://user:password@db:5432/receipt_manager
REDIS_URL=redis://redis:6379
TELEGRAM_BOT_TOKEN=<your-bot-token>
```

6. Создайте файл окружения для ASR service:
```bash
cd ../asr-service
cp .env.example .env
```

Конфигурируйте:
```
OPENROUTER_API_KEY=<your-api-key>
REDIS_URL=redis://redis:6379
```

7. Запустите все сервисы:
```bash
cd ../../
docker-compose up -d
```

Сервисы будут доступны по адресам:
- Frontend: http://localhost:5173
- DB Service API: http://localhost:8001
- ASR Service API: http://localhost:8002
- Executor Service API: http://localhost:8003

## Мониторинг и логи

Логи хранятся в директориях сервисов в папке `logs/`. Каждый сервис выводит логи как в консоль, так и в файл.

Для мониторинга сервисов:
```bash
docker-compose logs -f db-service
docker-compose logs -f executor-service
docker-compose logs -f asr-service
```
