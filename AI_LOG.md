# Semana 4 
## Entrada 1
Prompt: "modifica db.py para leer DATABASE_URL del entorno, con SQLite como
default local, y normaliza postgres:// / postgresql:// a postgresql+psycopg://"

La IA propuso una función get_database_url() y agregar connect_args condicional
(check_same_thread solo aplica a SQLite). Acepté la función tal cual. Modifiqué
la sugerencia inicial de connect_args = {} sin tipo: mypy marcaba error porque
disallow_untyped_defs exige anotación explícita. Cambié a
connect_args: dict[str, bool] = {} para que pasara mypy sin desactivar la regla.

## Entrada 2
Prompt: "una línea autogenerada por Alembic en migrations/versions supera el
límite de ruff, ¿la reescribo?"

La IA propuso dos opciones: reformatear la línea a mano, o excluir
migrations/versions del linting vía extend-exclude en pyproject.toml. Rechacé
reformatear a mano porque cada alembic revision --autogenerate futura
regeneraría el archivo con el mismo formato, obligándome a repetir el ajuste
cada vez. Acepté la exclusión: es código generado por una herramienta, no
código que yo mantengo línea por línea, y es la práctica estándar para
carpetas de migraciones autogeneradas.

## Entrada 3
Prompt: "trivy con exit-code 1 puede fallar el pipeline por vulnerabilidades que
yo no puedo arreglar, ¿cómo lo evito sin perder el propósito del escaneo?"

La IA propuso agregar ignore-unfixed: true al step de Trivy, para que el job
solo falle si existe un CVE con parche disponible que aún no apliqué, no por
vulnerabilidades de la imagen base sin parche todavía en ningún lado. Acepté
la sugerencia: evita bloquear la entrega por algo fuera de mi control, sin
convertir el escaneo en un paso decorativo que nunca falla.

## Entrada 4
Prompt: "requirements.txt tiene pytest, ruff, mypy, pre-commit mezclados con
las dependencias de producción, ¿afecta el tamaño de la imagen Docker?"

La IA propuso separar en requirements.txt (solo lo que corre en producción) y
requirements-dev.txt (que incluye al primero más las herramientas de
desarrollo), y ajustar el Dockerfile para copiar solo el primero. Acepté la
separación completa. No me quedé con la palabra de la IA sobre el resultado:
verifiqué el tamaño real con `docker inspect -f "{{.Size}}" sensorhub:slim`
(73MB, bien por debajo del objetivo de 200MB), porque `docker images` con el
nuevo containerd image store mostraba "Disk Usage" y "Content Size" que no
correspondían al tamaño real y me habrían confundido si los hubiera citado
sin más.

## Entrada 5
Prompt: "quiero implementar GitHub Environments con protección de rama,
¿cómo se conecta con mi deploy en Render?"

La IA señaló un hueco real que ya había vivido esta semana: el Auto-Deploy
nativo de Render ignora por completo el estado de GitHub Actions — lo
comprobé cuando hice merge del PR #4 con CI en rojo y Render lo desplegó
igual, sin preguntar nada. Propuso desactivar el Auto-Deploy y disparar el
despliegue desde un job de Actions (environment: production) que llama al
Deploy Hook de Render solo si test, smoke-test y security-scan pasan primero.
Acepté el cambio completo porque cierra exactamente la falla que ya había
experimentado en carne propia, y lo confirmé con evidencia real en el
dashboard de Render ("Triggered via Deploy Hook" en el evento de deploy),
no solo porque el pipeline mostrara verde.

## Entrada 6
Situación real: git push origin main fue rechazado con GH006 después de
activar "Require status checks to pass before merging", aunque mi código
estaba correcto.

Le pregunté a la IA por qué. Me explicó que era un candado circular: los
checks solo pueden correr sobre un commit que ya existe en GitHub, así que un
push directo a main nunca puede cumplir el requisito por sí mismo — necesita
pasar primero por una rama y un PR para que los checks tengan dónde
ejecutarse antes del merge. Entendí la causa (no solo copié el comando de
solución) y apliqué el flujo correcto: crear rama, abrir PR, esperar los tres
checks en verde, mergear desde GitHub.
