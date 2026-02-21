# Задача: Добавить --git-init при инициализации компонентов

## Контекст (Context)
В настоящее время команды `hsm library init` и `hsm service init` создают структуру компонента, но не инициализируют Git-репозиторий. Согласно нашей методологии, многие компоненты разрабатываются как "Nested Repos" (вложенные репозитории). Добавление флага `--git-init` упростит этот процесс.

## Требования (Requirements)
- Добавить опцию `--git-init` в CLI команды `hsm library init` и `hsm service init`.
- Реализовать метод `_init_git(path: Path)` в `HSMCore` для выполнения `git init`.
- Убедиться, что `git init` вызывается только при наличии флага.
- Корректно обрабатывать ошибки (например, если Git не установлен) с логированием.

## Шаги реализации (Implementation Steps)
1.  **Модификация CLI**: Обновить `hsm/src/hyper_stack_manager/cli/project.py`, добавив новую опцию в `project_library_init` и `project_service_init`.
2.  **Обновление Core**: 
    - Обновить сигнатуры `init_library` и `init_service` в `hsm/src/hyper_stack_manager/core/engine.py`.
    - Реализовать `_init_git` в классе `HSMCore`.
    - Вызывать `_init_git` в конце процесса инициализации, если `git_init` равен True.
3.  **Верификация (Verification)**:
    - Выполнить `hsm library init test-lib --git-init` и проверить наличие директории `.git` в `packages/test-lib`.
    - Выполнить `hsm service init test-service --git-init` и проверить наличие директории `.git` в `services/test-service`.

## Критерии готовности (Definition of Done)
- [ ] CLI принимает `--git-init` для инициализации и библиотек, и сервисов.
- [ ] Git-репозиторий инициализируется в директории компонента при использовании флага.
- [ ] Git-репозиторий НЕ инициализируется, если флаг отсутствует.
- [ ] Документация обновлена (уже сделано в режиме architect).
- [ ] Тесты подтверждают корректность поведения.
