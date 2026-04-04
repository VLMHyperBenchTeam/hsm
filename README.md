# Hyper Stack Manager (hsm) 🚀

**Environment Hypervisor for Modern Hybrid Stacks**

HSM — это мета-оркестратор, который позволяет декларативно собирать рабочее окружение проекта из независимых компонентов (Python-пакетов и Docker-контейнеров) на основе единого манифеста `hsm.yaml`. Он оркестрирует разработку сложных систем, бесшовно объединяя миры Python и Docker.

> [!WARNING]
> Проект находится на **самой ранней стадии разработки** (Alpha). Возможны критические изменения API и структуры манифестов между версиями.

## 💡 Концепция: Intent vs Artifacts

HSM разделяет "желаемое состояние" и "техническую реализацию":
*   **Intent (Намерение)**: Описывается в `hsm.yaml`. Вы указываете компоненты, их версии и режимы (`dev`/`prod`).
*   **Artifacts (Артефакты)**: Результат `hsm sync`. Это конфиги `pyproject.toml` (для Python) и `docker-compose.hsm.yml` (для Docker), которые HSM генерирует автоматически.

## ✨ Основные фишки

- **🧩 LEGO-архитектура**: Собирайте стек из независимых компонентов. Легко меняйте реализации (например, Qdrant на Milvus) одной командой.
- **🔗 Hybrid Orchestration**: Единое управление кодом (через `uv`) и инфраструктурой (через `docker compose`).
- **⚡ Atomic Sync**: Транзакционное обновление конфигов. Если зависимости не сошлись, ваши `pyproject.toml` и `docker-compose.yml` останутся нетронутыми.
- **🛠 Native Dev/Prod Bridge**: Мгновенное переключение между стабильными артефактами и локальной разработкой (editable installs + build contexts). Поддерживает создание **гибридных наборов**, где часть компонентов находится в `prod`, а часть в `dev` режиме.
- **🧠 Dependency Implication**: Умный учет зависимостей. Например, выбор клиента БД автоматически настроит и поднимет нужный Docker-контейнер.

## 🔄 Гибридный воркфлоу (Hybrid Stack)

Главная сила HSM — в одновременном управлении кодом и инфраструктурой.

**Пример:** Вы хотите заменить Qdrant на Milvus.
1. **Команда:** `hsm group add vector-db-adapter --option milvus-adapter`.
2. **Действие HSM:** В `pyproject.toml` прописывается клиент для Milvus, а в `docker-compose.hsm.yml` — запуск контейнера Milvus.
3. **Sync:** Один вызов `hsm sync` полностью перестраивает всё окружение.

## 🚀 Быстрый старт

### 1. Установка (через uv)
```bash
uv tool install git+https://github.com/VLMHyperBenchTeam/hsm.git
```

### 2. Инициализация проекта
```bash
hsm init --name my-awesome-project
```

### 3. Добавление компонента
```bash
hsm group add vector-db-adapter --option qdrant-adapter
```

### 4. Синхронизация стека
```bash
hsm sync
```

## 📦 Локальные runtime volumes (`.hsm-volumes/`)

Подробное описание вынесено в use case:
[`tasks_descriptions/use_cases/local-runtime-volumes-hsm-volumes.md`](tasks_descriptions/use_cases/local-runtime-volumes-hsm-volumes.md)

## 📚 Документация
 
Для глубокого погружения в концепции, воркфлоу и архитектуру посетите наш сайт:
👉 **[https://vlmhyperbenchteam.github.io/hsm/](https://vlmhyperbenchteam.github.io/hsm/)**
 
### 🌐 Поддержка браузеров
Сайт документации и лендинг тестируются исключительно в браузерах **Google Chrome** и **Mozilla Firefox**. Мы рекомендуем использовать их для наилучшего отображения всех визуальных эффектов.
 
Ввиду отсутствия аппаратного обеспечения Apple, поддержка Safari не гарантируется. Если вы обнаружите баги в Safari, мы будем рады вашим Pull Requests!
 
---
*Built with ❤️ for modular systems developers.*
