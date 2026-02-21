# Task: Добавить поддержку `env_file` для сервисов HSM

## Контекст
Сейчас в HSM переменные окружения для сервисов задаются через поля `env` и через `implies` с последующим `merge`, а затем напрямую пробрасываются в runtime-конфигурацию.

Актуальные места в коде:
- модели `ServiceManifest` и `Source` в [`models.py`](../../src/hyper_stack_manager/models.py)
- materialization сервисов в [`sync_engine.py`](../../src/hyper_stack_manager/core/sync_engine.py)
- генерация Docker-конфигурации в [`container_docker.py`](../../src/hyper_stack_manager/adapters/container_docker.py)
- передача env в UV-сервисы в [`python_uv.py`](../../src/hyper_stack_manager/adapters/python_uv.py)

На текущий момент отсутствует first-class поддержка `env_file` в модели манифестов и нет автоматической генерации/подключения сервисных `.env` файлов.

## Цель
Реализовать first-class поддержку `env_file` для сервисов HSM, чтобы конфигурацией можно было управлять через `.env` файлы, сохранив совместимость с текущими `env` и `implies`.

## Scope
1. Добавить поддержку `env_file` на уровне manifest model (`service` и `source`).
2. Добавить materialization merged env в сервисные `.env` файлы во время `hsm sync`.
3. Добавить поддержку `env_file` при генерации `docker-compose`.
4. Добавить загрузку env из `.env` файлов для UV/VES сервисов.
5. Сохранить backward compatibility с существующим inline `env`.

## Шаги реализации
1. Расширить model layer:
   - добавить `env_file: Optional[List[str]]` в релевантные структуры в [`models.py`](../../src/hyper_stack_manager/models.py)
   - нормализовать single path и list path в единый формат

2. Реализовать materialization `.env` в sync engine:
   - в [`sync_engine.py`](../../src/hyper_stack_manager/core/sync_engine.py) добавить utility для генерации `.env.<service>` в корне проекта
   - предложенный порядок merge:
     1) базовые значения из `env_file`
     2) `manifest.env`
     3) `source.env`
     4) merged `implies params`
   - обеспечить deterministic порядок ключей

3. Обновить Docker path:
   - в [`_resolve_container_config()`](../../src/hyper_stack_manager/core/sync_engine.py) включить `env_file` в service config
   - в [`container_docker.py`](../../src/hyper_stack_manager/adapters/container_docker.py) убедиться, что `env_file` корректно попадает в `docker-compose.hsm.yml`

4. Обновить UV path:
   - в [`python_uv.py`](../../src/hyper_stack_manager/adapters/python_uv.py) добавить загрузку значений из сгенерированного `.env`
   - сохранить приоритет явных env overrides над значениями из файла

5. Обновить CLI и registry UX:
   - добавить CLI-параметры для управления `env_file` в [`registry.py`](../../src/hyper_stack_manager/cli/registry.py)
   - задокументировать path semantics и conflict resolution

6. Добавить тесты:
   - `docker-compose` содержит `env_file`
   - UV/VES сервис получает значения из `.env`
   - `implies` корректно override значения по precedence
   - старые `env-only` манифесты остаются рабочими

7. Обновить документацию HSM:
   - [`01-manifest.md`](../../website/docs/02-core-concepts/01-manifest.md)
   - [`03-dependency-implication.md`](../../website/docs/02-core-concepts/03-dependency-implication.md)
   - [`03-ves-workflow.md`](../../website/docs/03-guides/03-ves-workflow.md)

## Критерии готовности
- Манифест HSM поддерживает `env_file` для сервисов без поломки текущих конфигураций.
- `hsm sync` генерирует и подключает сервисные `.env` файлы для `docker` и `uv` runtime.
- Значения из `implies` отражаются в effective runtime env по зафиксированному precedence.
- Проекты с текущей `env-only` схемой работают без изменений.
- Тесты на новый функционал проходят.

## Примечание
Задача критична для модели `Obsidian Assistant`, где runtime-конфигурация должна жить в `.env` и автоматически распространяться через `dependencies` и `implies`.
