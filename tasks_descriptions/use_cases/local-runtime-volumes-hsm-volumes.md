# Use Case: локальные runtime volumes через `.hsm-volumes/`

## Контекст

В некоторых `dev`-сценариях удобно хранить runtime-данные сервисов прямо в директории проекта, например:
- `node_modules` для frontend dev container,
- cache package manager,
- другие ephemeral runtime artifacts.

Базовая практика: использовать `bind mount` на каталог вида `.hsm-volumes/<service>/<purpose>`.

Пример структуры:

```text
.hsm-volumes/
  code-rag-frontend/
    node_modules/
```

## Зачем это нужно

- Повышает portability окружения между разработчиками.
- Упрощает диагностику и локальную очистку runtime-состояния.
- Не требует глобальной установки runtime-зависимостей на host-машину.

## Рекомендации

- Добавлять `.hsm-volumes/` в `.gitignore`.
- Параметризовать путь через `env` в service manifest (например, `HSM_FRONTEND_NODE_MODULES_PATH`).
- Создавать каталоги заранее (`mkdir -p`) в bootstrap-командах.
- Очищать точечно при проблемах с зависимостями, не затрагивая исходники.

## Эволюция

Сейчас это рабочий подход для `dev workflow`.

Планируется platform-level поддержка корректной генерации top-level `volumes:` для named volumes, после чего можно перейти с `bind-mount strategy` на `named volumes strategy`.

Связанная задача: [`support_named_volumes_in_generated_compose.md`](../tasks/support_named_volumes_in_generated_compose.md)

Связанное описание интеграции в code-rag: [`frontend-dev-container-hsm-workflow.md`](../../../services/code-rag/plans/frontend-dev-container-hsm-workflow.md)
