# Task: Реализация UvRuntimeAdapter и команды service init

## Контекст
Для поддержки VES нам нужен адаптер, умеющий создавать изолированные venv и выполнять в них sync.

## Шаги реализации
1.  **Adapter (`src/hyper_stack_manager/adapters/python_uv.py`)**:
    - [x] Реализовать `init_service(path)`: вызов `uv init --no-workspace`.
    - [x] Реализовать `sync_service(path)`: вызов `uv sync` внутри указанной папки.
2.  **CLI (`src/hyper_stack_manager/cli/project.py`)**:
    - [x] Добавить группу команд `hsm service`.
    - [x] Реализовать `hsm service init <name> --runtime uv`.
3.  **Core (`src/hyper_stack_manager/core/engine.py`)**:
    - [x] Добавить метод `init_service` в `HSMCore`.

## Критерии готовности
- [x] Команда `hsm service init` создает папку с изолированным `pyproject.toml`.
- [x] В реестре появляется запись о новом сервисе.

## Отчет о реализации
- **Что сделано**: Реализована поддержка изолированных сервисов (VES) через рантайм `uv`.
- **Как реализовано**:
    - В `BasePackageManagerAdapter` добавлены абстрактные методы `init_service` и `sync_service`.
    - В `UvAdapter` реализованы эти методы с использованием `uv init --no-workspace` и `uv sync`.
    - В `HSMCore` добавлен метод `init_service`, который оркестрирует создание папки, инициализацию рантайма и регистрацию в реестре.
    - В `RegistryManager.add_service` добавлена поддержка `deployment_profiles`.
    - В CLI добавлена команда `hsm service init`.
- **Отклонения от плана**: Нет.