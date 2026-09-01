## Descripción del Dataset

El dataset `candidates.csv` contiene información de aplicaciones de candidatos
a procesos de reclutamiento técnico. Cada fila representa una aplicación individual.

## Hallazgos del Perfilamiento (Data Profiling)

Perfilamiento realizado en `notebooks/data_profiling.ipynb`, en el siguiente orden:

**1. Forma del dataset (`df.shape`)**
- 50,000 filas × 10 columnas

**2. Tipos de datos (`df.dtypes`)**
- Texto (`str`): First Name, Last Name, Email, Application Date, Country, Seniority, Technology
- Numéricos (`int64`): YOE, Code Challenge Score, Technical Interview Score
- ⚠️ `Application Date` llega como texto, no como fecha — debe convertirse en la preparación de datos.

**3. Valores nulos (`df.isnull().sum()`)**
- 0 valores nulos en todas las columnas.

**4. Duplicados (`df.duplicated()`)**
- Filas duplicadas exactas: 0
- Emails duplicados: 167 (candidatos que aplicaron más de una vez)

**5. Rango de fechas (`Application Date`)**
- Mínima: 2018-01-01
- Máxima: 2022-07-04

**6. Valores únicos en categóricas**
- Seniority (7 valores): Intern, Trainee, Junior, Mid-Level, Senior, Lead, Architect
- Países: 244 valores distintos
- Tecnologías: 24 valores distintas

**7. Rango de los puntajes**
- Code Challenge Score: 0 a 10
- Technical Interview Score: 0 a 10

**8. Estadísticas descriptivas (`df.describe()`)**

| Variable | count | mean | std | min | 25% | 50% | 75% | max |
|---|---|---|---|---|---|---|---|---|
| YOE | 50000 | 15.29 | 8.83 | 0 | 8 | 15 | 23 | 30 |
| Code Challenge Score | 50000 | 5.00 | 3.17 | 0 | 2 | 5 | 8 | 10 |
| Technical Interview Score | 50000 | 5.00 | 3.17 | 0 | 2 | 5 | 8 | 10 |

### Decisiones derivadas del profiling
- No hay valores nulos que tratar.
- No hay filas duplicadas exactas.
- `Application Date` debe convertirse a tipo fecha (`datetime`) más adelante.
- Los 167 emails duplicados no son errores de carga (no son filas idénticas),
  sino candidatos que reaplicaron — se evaluará si sustentan un requisito adicional (R4/R5).

