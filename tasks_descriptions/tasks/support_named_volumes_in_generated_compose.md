# Задача: Поддержка named volumes в generated compose manifest

## Контекст
Во время интеграции frontend dev runtime для code-rag HSM сгенерировал compose service с mounted named volume, но не добавил top-level `volumes:` declaration. Из-за этого `docker compose` падает на валидации.

Observed error:
`service "code-rag-frontend" refers to undefined volume code-rag-frontend-node-modules: invalid compose project`

## Проблема
Сейчас compose generator в HSM объединяет только дерево `services:` и не собирает named volume declarations из service volume mounts. В результате generated compose manifest невалиден для кейсов с named volumes.

## Цель
Доработать HSM compose generation так, чтобы named volumes, используемые в `services.*.volumes`, автоматически детектировались и объявлялись в top-level `volumes:`.

## Scope
- Детектировать named volumes в mount-записях формата `<name>:/path`.
- Игнорировать bind mounts (`./path:/path`, `/abs/path:/path`) и anonymous volumes.
- Генерировать детерминированный top-level `volumes:` block с найденными named volume keys.
- Сохранить backward compatibility для проектов без named volumes.

## Candidate implementation points
- `src/hyper_stack_manager/adapters/container_docker.py`
- при необходимости helper в core sync/generation слое.

## Acceptance Criteria
- `docker compose -f docker-compose.hsm.yml config` проходит для service, где используются named volumes.
- В generated compose есть:
  - `services.<service>.volumes` как раньше,
  - top-level `volumes.<named_volume>:` declarations.
- Для проектов без named volumes effective config не меняется.

## Notes
В code-rag временно применён quick fix через bind-mounted host path для `node_modules`, но platform-level fix должен быть реализован в HSM для чистого portable workflow.
