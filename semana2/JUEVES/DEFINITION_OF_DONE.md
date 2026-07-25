# Definicion de Done (DoD) 

Para que cualquier User Story o tarea técnica que sea movida a la columna "Done"del tablero ágil, debe cumplir obligatoriamente con ciertos estandares como :

 **Criterios de Aceptación (TDD):** Todos los criterios de aceptación definidos en formato Gherkin (Given/When/Then) han sido implementados como tests automatizados usando `pytest` y todos pasan exitosamente en color verde.
 
 **Cobertura de Pruebas (Coverage):** El código nuevo o modificado mantiene o supera el **80% de cobertura** de pruebas automatizadas.

 **Análisis Estático Limpio:** - `ruff` se ejecuta sin advertencias ni errores (el código cumple con el estándar PEP 8). 
 **Análisis Estático Limpio:** - `mypy` se ejecuta sin advertencias ni errores (el tipado estático es 100% estricto y coherente).
 
 **Auto-revisión y Pull Request:** El código no se subió directamente a la rama principal (`main`). Se creó a través de una rama secundaria, se abrió un Pull Request (PR), y el desarrollador realizó una auto-revisión de su propio código antes de fusionarlo.

 **Documentación Actualizada:** Se ha actualizado cualquier documentación relevante (Docstrings en el código, README.md, o diagramas) que haya sido afectada por esta nueva funcionalidad.
