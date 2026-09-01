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
- `Application Date` llega como texto, no como fecha — debe convertirse en la preparación de datos.

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

## Requisitos de Negocio Adicionales (R4, R5)

| ID | Requisito de Negocio | Pregunta de Negocio | Decisión que Soporta |
|----|----------------------|----------------------|------------------------|
| R4 | Analizar el país de origen de las aplicaciones y su tasa de contratación desglosada por nivel de seniority. | ¿Qué países de origen tienen mayor volumen de aplicaciones y mejor tasa de contratación para cada nivel de seniority? | Priorizar en qué países enfocar campañas de reclutamiento dirigidas a perfiles específicos. |
| R5 | Analizar si los candidatos que aplican más de una vez tienen una tasa de contratación distinta a los que aplican una sola vez. | ¿Los candidatos que reaplican tienen mayor o menor tasa de contratación que los que aplican una sola vez? | Decidir si vale la pena animar a los candidatos no contratados a volver a aplicar. |


## Trazabilidad de Requisitos

| Requisito | Pregunta de Negocio | Datos Requeridos | Salida Analítica Esperada |
|---|---|---|---|
| R1 | Monitorear las tendencias de contratación a lo largo del tiempo para identificar cambios en los resultados de reclutamiento. | Application Date, Code Challenge Score, Technical Interview Score | Tabla agrupada por mes: total de aplicaciones, total de contratados, tasa de contratación. |
| R2 | Comparar los resultados de contratación entre tecnologías para identificar qué perfiles técnicos generan el mayor número y proporción de candidatos contratados. | Technology, Code Challenge Score, Technical Interview Score | Tabla agrupada por Technology: total de aplicaciones, total de contratados, tasa de contratación. |
| R3 | Analizar los resultados de contratación según el seniority del candidato y los años de experiencia profesional. | Seniority, YOE, Code Challenge Score, Technical Interview Score | Tabla agrupada por Seniority y rango de YOE: total de aplicaciones, total de contratados, tasa de contratación. |
| R4 | Analizar el país de origen de las aplicaciones y su tasa de contratación desglosada por nivel de seniority. | Country, Seniority, Code Challenge Score, Technical Interview Score | Tabla agrupada por Country y Seniority: total de aplicaciones, total de contratados, tasa de contratación. |
| R5 | Analizar si los candidatos que aplican más de una vez tienen una tasa de contratación distinta a los que aplican una sola vez. | Email, Code Challenge Score, Technical Interview Score | Tabla agrupada por "reaplicó: sí/no": total de candidatos, total de contratados, tasa de contratación. |



## Modelo Dimensional

### Proceso de Negocio
Proceso de Aplicación de Candidatos (Candidate Application Process). Cada fila del
dataset representa una aplicación individual de un candidato a un proceso de
reclutamiento técnico — este es el evento central sobre el cual giran los 5
requisitos de negocio (R1-R5).

### Grano
Una fila en la Tabla de Hechos (FactApplications) representa una aplicación
individual de un candidato a un proceso de reclutamiento, en una fecha específica,
para una tecnología específica.


### Dimensiones

| Dimensión | Propósito | Atributos Principales | Requisito(s) que Soporta |
|---|---|---|---|
| DimDate | Contextualizar el tiempo de cada aplicación | full_date, year, month, quarter | R1 |
| DimTechnology | Contextualizar la tecnología a la que aplicó | technology_name | R2 |
| DimCandidateProfile | Contextualizar el perfil (seniority + experiencia) | seniority, yoe_range | R3 |
| DimCountry | Contextualizar el país de origen | country_name | R4 |
| DimCandidate | Identificar al candidato (para detectar reaplicaciones) | first_name, last_name, email | R5 |

### Hechos y Medidas

| Medida | Significado | Fuente / Cálculo | Requisito(s) que Soporta |
|---|---|---|---|
| code_challenge_score | Puntaje del reto de código (0-10) | Directo del CSV | Todos (para calcular is_hired) |
| technical_interview_score | Puntaje de la entrevista técnica (0-10) | Directo del CSV | Todos (para calcular is_hired) |
| is_hired | 1 si fue contratado, 0 si no | Calculado: 1 si code_challenge_score >= 7 Y technical_interview_score >= 7, si no 0 | R1, R2, R3, R4, R5 |
| application_count | Cuenta de aplicaciones (siempre 1 por fila) | Constante = 1 | Todos |

### Esquema Estrella

**Tabla de Hechos: FactApplications**
- application_key (PK, surrogate)
- date_key (FK -> DimDate)
- technology_key (FK -> DimTechnology)
- profile_key (FK -> DimCandidateProfile)
- country_key (FK -> DimCountry)
- candidate_key (FK -> DimCandidate)
- code_challenge_score (medida)
- technical_interview_score (medida)
- is_hired (medida)
- application_count (medida)

### Esquema Estrella (Diagrama)

mermaid
erDiagram
    DIMDATE {
        int date_key PK
        date full_date
        int year
        int month
        int quarter
    }

    DIMTECHNOLOGY {
        int technology_key PK
        string technology_name
    }

    DIMCANDIDATEPROFILE {
        int profile_key PK
        string seniority
        string yoe_range
    }

    DIMCOUNTRY {
        int country_key PK
        string country_name
    }

    DIMCANDIDATE {
        int candidate_key PK
        string first_name
        string last_name
        string email
    }

    FACTAPPLICATIONS {
        int application_key PK
        int date_key FK
        int technology_key FK
        int profile_key FK
        int country_key FK
        int candidate_key FK
        int code_challenge_score
        int technical_interview_score
        int is_hired
        int application_count
    }

    DIMDATE ||--o{ FACTAPPLICATIONS : "date_key"
    DIMTECHNOLOGY ||--o{ FACTAPPLICATIONS : "technology_key"
    DIMCANDIDATEPROFILE ||--o{ FACTAPPLICATIONS : "profile_key"
    DIMCOUNTRY ||--o{ FACTAPPLICATIONS : "country_key"
    DIMCANDIDATE ||--o{ FACTAPPLICATIONS : "candidate_key"




Cada dimensión se conecta a la Tabla de Hechos mediante su llave subrogada (FK).
Cada dimensión usa una llave subrogada como llave primaria (no se usan llaves
naturales del CSV como PK).

Las 5 dimensiones se conectan alrededor de una única Tabla de Hechos central
(FactApplications), cada una mediante su llave subrogada — esta forma de
"estrella" (una tabla central rodeada de dimensiones) es lo que le da nombre
al Esquema Estrella.



### Validación del Modelo

| Requisito | Dimensión(es) Requerida(s) | Medida(s) Requerida(s) | Soportado? |
|---|---|---|---|
| R1 | DimDate | is_hired, application_count | Si |
| R2 | DimTechnology | is_hired, application_count | Si |
| R3 | DimCandidateProfile | is_hired, application_count | Si |
| R4 | DimCountry, DimCandidateProfile | is_hired, application_count | Si |
| R5 | DimCandidate | is_hired, application_count | Si |