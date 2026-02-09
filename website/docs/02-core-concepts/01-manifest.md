---
sidebar_position: 1
---

# Манифест проекта (hsm.yaml)

Этот документ детализирует структуру манифестов и логику работы рантайма HSM (Hyper Stack Manager) для обеспечения декларативного управления стеком проекта.

## 1. Структура Манифестов (Manifest Definitions)

HSM оперирует двумя типами манифестов: **Манифест проекта** (`hsm.yaml`) и **Манифесты компонентов** в Реестре.

### 1.1. Манифест проекта (`hsm.yaml`)
Является Single Source of Truth для конкретного проекта. Описывает *намерения* пользователя.

```yaml
project:
  name: "my-rag-platform"
  version: "0.1.0"

libraries:
  package_manager: "uv"
  groups:
    # Group for vector database clients
    vector-db-client:
      strategy: "1-of-N"
      selection: "qdrant-adapter"
  standalone:
    - name: "langchain"
      mode: "prod"

services:
  groups:
    # Group for vector database servers
    vector-db-server:
      strategy: "1-of-N"
      selection: "qdrant"
  standalone: []

modes:
  qdrant-adapter: "dev"
  qdrant: "prod"
```

#### Работа с комментариями
HSM использует `ruamel.yaml` для сохранения комментариев пользователя. Если в манифесте группы в Реестре указано поле `comment`, HSM автоматически вставит его как комментарий над соответствующей группой в `hsm.yaml` при добавлении или обновлении.

### 1.2. Манифесты компонентов (Registry)
Реестр (`hsm-registry/`) содержит базу знаний о доступных компонентах. В HSM на один проект полагается **ровно один реестр**.

#### Типы компонентов:
*   **Library**: Python-библиотека.
*   **Service**: Автономный сервис с поддержкой различных рантаймов (Docker, UV, Podman).
*   **Group**: Логическое объединение (1-of-N или M-of-N) для выбора реализаций. Содержит поле `comment` для описания назначения группы.

## 2. Примеры компонентов (Vector DB)

### 2.1. Группа выбора (`library_groups/vector-db-client.yaml`)
```yaml
name: "vector-db-client"
type: "library_group"
strategy: "1-of-N"
comment: "Group for vector database clients" # This will appear in hsm.yaml
options:
  - name: "qdrant-adapter"
    description: "Client for Qdrant"
  - name: "milvus-adapter"
    description: "Client for Milvus"
```

### 2.2. Манифест библиотеки (`libraries/qdrant-adapter.yaml`)
```yaml
name: "qdrant-adapter"
version: "1.0.0"
sources:
  prod:
    type: "git"
    url: "https://github.com/my-org/qdrant-adapter.git"
    ref: "v1.0.0"
  dev:
    type: "local"
    path: "./packages/qdrant-adapter"
    editable: true
```

### 2.3. Манифест сервиса (`services/qdrant.yaml`)
```yaml
name: "qdrant"
type: "service"
container_name: "vector-db" # Logical service name in compose
sources:
  prod:
    type: "docker-image"
    image: "qdrant/qdrant:latest"
  dev:
    type: "git"
    url: "https://github.com/qdrant/qdrant.git"
    volumes:
      - "./qdrant_data:/var/lib/qdrant"
```

## 3. HSM Runtime Logic

Рантайм HSM отвечает за синхронизацию (Reconciliation) состояния проекта с манифестом.

### 3.1. Процесс синхронизации (`hsm sync`)
1.  **Resolution**: HSM обходит `hsm.yaml`, запрашивает метаданные выбранных компонентов из Реестра.
2.  **Implication Merging**: Если несколько компонентов требуют один и тот же сервис, HSM объединяет их параметры в единую конфигурацию.
3.  **Validation**: Проверка разрешимости зависимостей (через `uv lock` для Python).
4.  **Materialization**:
    *   Обновление `pyproject.toml` (инъекция путей или git-ссылок).
    *   Генерация `docker-compose.hsm.yml` (для Docker/Podman рантаймов).
    *   Инициализация и синхронизация изолированных venv (для UV рантайма).
    *   Применение `container_name` и `alias` для выбранных сервисов.
5.  **Execution**: Вызов системных команд (`uv sync`, `docker compose`).

### 3.2. Атомарность и Транзакционность
HSM гарантирует, что артефакты проекта (`pyproject.toml`) не будут изменены, если процесс синхронизации прервется ошибкой.

### 3.3. Управление режимами (Dev/Prod)
HSM автоматически подставляет нужный источник (`source`) из манифеста компонента в зависимости от режима. В режиме `dev` приоритет всегда отдается локальным путям и editable-установкам.