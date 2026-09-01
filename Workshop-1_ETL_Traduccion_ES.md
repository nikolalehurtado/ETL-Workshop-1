# FACULTAD DE INGENIERÍA Y CIENCIAS BÁSICAS

## PROGRAMA ACADÉMICO: INGENIERÍA DE DATOS E INTELIGENCIA ARTIFICIAL

### CURSO: ETL (G01)

### Workshop-1: De los Requisitos de Negocio a un Data Warehouse Dimensional

\---

## 1\. Introducción

Este taller simula un **reto técnico real de Ingeniería de Datos** en el que debes transformar necesidades de negocio y datos operacionales crudos en un sistema de datos analítico.

Trabajarás con datos de candidatos provenientes de procesos de reclutamiento técnico. Tu objetivo no es solo implementar un pipeline ETL, sino **diseñar y construir un Data Warehouse Dimensional que soporte requisitos de negocio específicos y decisiones analíticas**.

A lo largo del taller aplicarás el siguiente flujo de trabajo de ingeniería:

**Requisitos de Negocio → Comprensión de los Datos → Modelado Dimensional → ETL → Data Warehouse → Analítica → Decisiones de Negocio**

Este taller evalúa tu capacidad para:

* Comprender requisitos de negocio analíticos.
* Traducir requisitos de negocio en requisitos de datos.
* Definir el grano apropiado para un modelo analítico.
* Diseñar un Modelo de Datos Dimensional usando un Esquema Estrella.
* Implementar un pipeline ETL reproducible.
* Cargar dimensiones y hechos en un Data Warehouse.
* Generar información analítica directamente desde el Data Warehouse.
* Verificar que el sistema implementado satisface los requisitos de negocio originales.
* Documentar y comunicar decisiones técnicas de forma profesional.

> \\\*\\\*El objetivo no es simplemente construir un Data Warehouse. El objetivo es construir un sistema de datos analítico que satisfaga los requisitos de negocio.\\\*\\\*

\---

## 2\. Escenario

Una empresa de reclutamiento tecnológico quiere mejorar su comprensión de sus procesos de selección de candidatos.

La empresa recibe miles de aplicaciones de candidatos con diferentes perfiles profesionales, niveles de experiencia, países, niveles de seniority y perfiles tecnológicos.

El desempeño de los candidatos se evalúa mediante dos pruebas técnicas:

* Code Challenge Score (Puntaje de Reto de Código)
* Technical Interview Score (Puntaje de Entrevista Técnica)

Actualmente, los datos de las aplicaciones de los candidatos están disponibles como archivos crudos, pero la organización necesita un sistema analítico que permita a los tomadores de decisiones entender los patrones de contratación y evaluar el desempeño del reclutamiento desde diferentes perspectivas.

Se te ha asignado como el Ingeniero(a) de Datos responsable de diseñar e implementar la primera versión de este sistema analítico.

Tu solución debe:

1. Comprender y refinar los requisitos analíticos.
2. Analizar los datos fuente disponibles.
3. Diseñar un Modelo de Datos Dimensional.
4. Implementar las transformaciones ETL requeridas.
5. Cargar el modelo resultante en un Data Warehouse.
6. Generar consultas analíticas y KPIs.
7. Demostrar que el sistema final satisface los requisitos de negocio definidos.

\---

## 3\. Requisitos de Negocio

La organización ha identificado los siguientes requisitos analíticos iniciales:

**R1 — Tendencias de Contratación**
Monitorear las tendencias de contratación a lo largo del tiempo para identificar cambios en los resultados de reclutamiento. El sistema debe permitir a los analistas estudiar el comportamiento de contratación en diferentes periodos.

**R2 — Análisis de Tecnología**
Comparar los resultados de contratación entre tecnologías para identificar qué perfiles técnicos generan el mayor número y proporción de candidatos contratados.

**R3 — Análisis de Perfil del Candidato**
Analizar los resultados de contratación según el seniority del candidato y los años de experiencia profesional, para identificar diferencias en los resultados de reclutamiento entre perfiles de candidatos.

### 3.1 Definir Dos Requisitos de Negocio Adicionales

Tu equipo debe proponer dos requisitos de negocio adicionales (R4 y R5) usando los datos disponibles. Los requisitos deben:

* Abordar una necesidad analítica significativa.
* Soportar una decisión de negocio o proporcionar información útil para la gestión del reclutamiento.
* Poder responderse usando los datos disponibles.
* Ser diferentes de R1–R3.
* Requerir procesamiento analítico, no simplemente la consulta de registros individuales.

|ID|Requisito de Negocio|Pregunta de Negocio|Decisión que Soporta|
|-|-|-|-|
|R4||||
|R5||||

> \\\*\\\*Importante\\\*\\\*
> Una visualización, consulta SQL o dashboard \\\*\\\*no\\\*\\\* es un requisito de negocio.
>
> \\\*\\\*Incorrecto:\\\*\\\* Crear un gráfico de barras de candidatos por país.
> \\\*\\\*Mejor:\\\*\\\* Identificar los países con mayor actividad de reclutamiento y comparar sus resultados de contratación para apoyar estrategias de reclutamiento geográfico.

\---

## 4\. Trazabilidad de Requisitos

Antes de diseñar el Data Warehouse, analiza los cinco requisitos de negocio. Completa la siguiente tabla:

|Requisito|Pregunta de Negocio|Datos Requeridos|Salida Analítica Esperada|
|-|-|-|-|
|R1||||
|R2||||
|R3||||
|R4||||
|R5||||

> \\\*\\\*Esta tabla debe completarse antes de diseñar el modelo dimensional.\\\*\\\*
> \\\*\\\*No empieces diseñando tablas. Empieza por entender qué necesita saber el negocio.\\\*\\\*

\---

## 5\. Descripción de los Datos

El conjunto de datos fuente contiene aproximadamente **50,000 aplicaciones de candidatos**. Cada fila representa una aplicación de un candidato.

Los atributos disponibles son:

* First Name (Nombre)
* Last Name (Apellido)
* Email (Correo electrónico)
* Country (País)
* Application Date (Fecha de aplicación)
* YOE (Years of Experience — Años de Experiencia)
* Seniority (Nivel de seniority)
* Technology (Tecnología)
* Code Challenge Score (Puntaje de reto de código)
* Technical Interview Score (Puntaje de entrevista técnica)

### 5.1 Regla de Negocio — Resultado de Contratación

Un candidato se considera **HIRED (CONTRATADO)** cuando:

**Code Challenge Score ≥ 7 Y Technical Interview Score ≥ 7
De lo contrario: NOT HIRED (NO CONTRATADO)**

Esta regla de negocio debe implementarse durante el proceso de transformación.

La siguiente figura muestra una pequeña muestra de los datos.

*Figura 1. Pequeña muestra de los datos (candidates.csv) — columnas: First Name, Last Name, Email, Application Date, Country, YOE, Seniority, Technology, Code Challenge Score, Technical Interview Score.*

\---

## 6\. Arquitectura de Sistema Propuesta

Tu solución debe seguir el flujo analítico general que se muestra a continuación. La arquitectura representa el sistema a alto nivel. Tu implementación puede organizar los componentes individuales de forma diferente, pero **el flujo completo de datos debe estar claramente documentado**.

*Figura 2. Arquitectura del sistema analítico propuesto:*
**Extract** (CSV → DataFrame, con control de versiones en Git/GitHub y Dataset EDA) → **Transform** → **DW (Data Warehouse)** ← **Load** → **Dashboard**

\---

## 7\. Tecnologías

Debes usar:

* Python
* Pandas
* Jupyter Notebook para el perfilamiento inicial de datos (data profiling)
* SQL
* MySQL o PostgreSQL como Data Warehouse
* Git y GitHub
* Herramienta de BI (Power BI, Tableau, Looker Studio, u otra herramienta aprobada) para visualización analítica

> \\\*\\\*Para este taller debes seguir un enfoque ETL:\\\*\\\*
> \\\*\\\*Las transformaciones requeridas deben realizarse antes de cargar los datos analíticos en el Data Warehouse.\\\*\\\*

\---

## 8\. Tarea 1: Perfilamiento Inicial de Datos (Data Profiling)

Antes de diseñar o transformar los datos, comprende el conjunto de datos fuente. Realiza un perfilamiento básico que incluya al menos:

* Número de filas y columnas.
* Nombres de las columnas.
* Tipos de datos.
* Valores faltantes.
* Registros duplicados.
* Valores únicos en los atributos categóricos relevantes.
* Fechas mínima y máxima de aplicación.
* Rangos de los puntajes.
* Estadísticas descriptivas básicas para los atributos numéricos.

El propósito de esta actividad **no** es realizar un EDA extenso. El objetivo es comprender los datos lo suficiente como para soportar tus decisiones de modelado y transformación.

Documenta los hallazgos más importantes.

\---

## 9\. Tarea 2: Modelo de Datos Dimensional

Diseña un Esquema Estrella capaz de satisfacer los cinco requisitos de negocio. Sigue el proceso de modelado dimensional en el orden correcto.

### Paso 1 — Seleccionar el Proceso de Negocio

Identifica el proceso de negocio que se está analizando y justifica brevemente tu decisión.

### Paso 2 — Declarar el Grano

Antes de definir dimensiones o hechos, establece explícitamente qué representa una fila en la Tabla de Hechos (Fact Table).

Completa la siguiente frase:

**Una fila en \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ representa \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_.**

El grano debe ser preciso y consistente con los requisitos de negocio.
**Todas las dimensiones y medidas incluidas en la Tabla de Hechos deben ser compatibles con el grano declarado.**

### Paso 3 — Identificar las Dimensiones

Identifica las dimensiones necesarias para dar contexto al proceso de negocio. Para cada dimensión, especifica:

|Dimensión|Propósito|Atributos Principales|Requisito(s) que Soporta|
|-|-|-|-|
|||||
|||||
|||||
|||||

No crees dimensiones simplemente porque existan columnas categóricas en los datos fuente.
**Cada dimensión debe tener un propósito analítico claro.**

### Paso 4 — Identificar Hechos y Medidas

Identifica los hechos o medidas necesarios para responder las preguntas de negocio.

|Medida|Significado|Fuente / Cálculo|Requisito(s) que Soporta|
|-|-|-|-|
|||||
|||||
|||||
|||||

**Recuerda: no todo campo numérico es necesariamente una medida aditiva.**

### Paso 5 — Diseñar el Esquema Estrella

Crea el Esquema Estrella completo. El modelo debe incluir:

* Una Tabla de Hechos.
* Las Tablas de Dimensión requeridas.
* Llaves primarias.
* Llaves foráneas.
* Llaves subrogadas (surrogate keys) para las dimensiones.
* Medidas.
* Atributos dimensionales relevantes.

**Importante: No uses las llaves naturales de origen como llaves primarias de las dimensiones. Cada dimensión debe usar una llave subrogada.**

### Paso 6 — Validar el Modelo Contra los Requisitos

Antes de implementar el modelo, verifica que soporte los cinco requisitos.

|Requisito|Dimensión(es) Requerida(s)|Medida(s) Requerida(s)|¿Soportado?|
|-|-|-|-|
|R1|||Sí / No|
|R2|||Sí / No|
|R3|||Sí / No|
|R4|||Sí / No|
|R5|||Sí / No|

**Si uno o más requisitos no pueden satisfacerse, revisa el modelo dimensional antes de continuar.**

\---

## 10\. Tarea 3: Proceso ETL

Implementa un pipeline ETL reproducible en Python. El proceso ETL debe mantenerse relativamente simple. **El enfoque principal de este taller es el modelado dimensional y su conexión con los requisitos de negocio.**

### 10.1 Extract (Extracción)

* Leer los datos fuente.
* Preservar el archivo fuente original.
* Cargar los datos fuente en un DataFrame de Pandas apropiado.

**No realices transformaciones de negocio durante la extracción.**

### 10.2 Data Preparation (Preparación de Datos)

Realiza únicamente la preparación requerida por los datos y el modelo analítico. Esto puede incluir:

* Corregir tipos de datos.
* Estandarizar formatos relevantes.
* Manejar valores faltantes cuando sea necesario.
* Manejar registros duplicados cuando esté justificado.
* Preparar fechas y atributos categóricos.

**Todas las decisiones relevantes de preparación deben estar documentadas.**

### 10.3 Business Transformation (Transformación de Negocio)

Implementa la regla de negocio de contratación:

**HIRED = (Code Challenge Score ≥ 7) Y (Technical Interview Score ≥ 7)**

Crea cualquier atributo derivado adicional requerido por tus cinco requisitos de negocio.
**No crees transformaciones que no tengan un propósito analítico.**

\---

## 11\. Tarea 4: Transformación Dimensional

Transforma los datos fuente preparados en las estructuras dimensionales definidas en la Tarea 2. Tu proceso debe:

1. Crear los conjuntos de datos de las dimensiones.
2. Eliminar miembros de dimensión duplicados cuando corresponda.
3. Generar llaves subrogadas.
4. Mapear cada aplicación a las llaves subrogadas de dimensión correspondientes.
5. Crear la Tabla de Hechos según el grano declarado.
6. Incluir solo hechos y relaciones justificados por los requisitos analíticos.

**Conceptualmente:**
Datos de Candidatos Preparados → Registros de Dimensión → Llaves Subrogadas → Mapeo de Llaves → Tabla de Hechos

\---

## 12\. Tarea 5: Cargar el Data Warehouse

Crea el esquema del Data Warehouse en MySQL o PostgreSQL.

**Carga las tablas en el orden apropiado:
Dimensiones → Tabla de Hechos**

Valida:

* Llaves primarias.
* Llaves foráneas.
* Integridad referencial.
* Número de registros cargados.
* Ausencia de referencias de dimensión inválidas.

**La Tabla de Hechos final debe contener llaves foráneas que referencien registros de dimensión válidos.**

\---

## 13\. Tarea 6: Consultas Analíticas y KPIs

**Una vez cargado el Data Warehouse, todos los resultados analíticos deben generarse desde el Data Warehouse, no desde el archivo fuente ni desde DataFrames intermedios.**

Para cada uno de los cinco requisitos de negocio, implementa al menos una consulta analítica SQL o KPI. Por lo tanto, tu solución debe contener al menos **cinco salidas analíticas** — una por cada requisito de negocio.

Para cada salida analítica, identifica:

* Requisito de negocio.
* Pregunta de negocio.
* Consulta SQL.
* Resultado.
* Interpretación breve.

\---

## 14\. Tarea 7: Visualización e Interpretación en BI

Conecta una herramienta de Business Intelligence **directamente al Data Warehouse implementado** y crea visualizaciones analíticas que soporten los requisitos de negocio definidos.

Crea al menos **tres visualizaciones**, incluyendo:

* Al menos un análisis temporal.
* Al menos un análisis comparativo.
* Al menos un análisis asociado con R4 o R5 propuestos por tu equipo.

Las visualizaciones deben crearse usando una herramienta de BI como Power BI, Tableau, Looker Studio, u otra herramienta previamente aprobada por el docente.

Cada visualización debe identificar claramente:

* El requisito de negocio que soporta.
* La pregunta de negocio que responde.
* El KPI o medida representada.
* Una interpretación breve del resultado.

**Importante:** La herramienta de BI debe obtener los datos analíticos desde el Data Warehouse, no directamente desde el CSV fuente.

**Una visualización no se evalúa solo por su apariencia. Debe proporcionar información que soporte una decisión de negocio.** Para cada una, explica brevemente: ¿Qué le dice este resultado a la organización y por qué podría importar?

\---

## 15\. Tarea 8: Validación Final de Requisitos

Regresa a los cinco requisitos de negocio definidos al inicio del taller y completa la siguiente tabla:

|Requisito|¿Implementado?|Tablas del DW Usadas|Consulta / KPI|Hallazgo Principal|
|-|-|-|-|-|
|R1|Sí / No||||
|R2|Sí / No||||
|R3|Sí / No||||
|R4|Sí / No||||
|R5|Sí / No||||

Luego responde:

* ¿El Data Warehouse final proporciona suficiente información para satisfacer los cinco requisitos de negocio?
* ¿El modelo dimensional contiene elementos que no están justificados por los requisitos analíticos?
* ¿Qué decisiones de negocio pueden soportarse ahora con el sistema analítico implementado?

\---

## 16\. Repositorio de GitHub

El proyecto completo debe estar disponible en un repositorio de GitHub. Una estructura recomendada es:

```
workshop-1/
│
├── data/
│   └── raw/
│       └── candidates.csv
│
├── notebooks/
│   └── data\\\_profiling.ipynb
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── dimensional\\\_model.py
│   ├── load.py
│   └── main.py
│
├── sql/
│   ├── create\\\_tables.sql
│   └── analytical\\\_queries.sql
│
├── database/
│   └── recruitment\\\_dw.db
│
├── diagrams/
│   └── star\\\_schema.png
│
├── results/
│
├── README.md
├── requirements.txt
└── .gitignore
```

\---

## 17\. Requisitos del README

El README debe permitir que otra persona comprenda y reproduzca el proyecto. Debe incluir:

* Objetivo del proyecto.
* Contexto de negocio.
* Los cinco requisitos de negocio.
* Trazabilidad de requisitos.
* Descripción del conjunto de datos.
* Principales hallazgos del perfilamiento.
* Proceso de negocio.
* Definición del grano.
* Diagrama del Esquema Estrella.
* Explicación de dimensiones y hechos.
* Arquitectura ETL.
* Principales decisiones de transformación.
* Tecnologías.
* Instrucciones para ejecutar el proyecto.
* Consultas analíticas y KPIs.
* Principales hallazgos de negocio.
* Validación final de requisitos.

\---

## 18\. Entregable

**Enviar únicamente la URL del repositorio de GitHub a través del LMS.**

El repositorio debe contener todo el código fuente, los scripts SQL, la documentación, el diagrama, los resultados y las instrucciones necesarias para reproducir el proyecto.

\---

## 19\. Rúbrica de Evaluación

### Parte A — Repositorio de GitHub: 80%

|Criterio|Evidencia|Peso|
|-|-|-|
|Requisitos de Negocio y Trazabilidad|R4–R5 son significativos y los cinco requisitos están conectados con los datos, los componentes del modelo y las salidas analíticas.|10%|
|Diseño del Modelo Dimensional|Proceso de negocio, grano, dimensiones, hechos, llaves subrogadas, relaciones, Esquema Estrella y justificación del diseño correctos.|20%|
|ETL y Transformación Dimensional|Extracción correcta, preparación requerida, regla de negocio, transformación dimensional, mapeo de llaves subrogadas y pipeline reproducible.|15%|
|Implementación del Data Warehouse|Esquema correcto, carga de dimensiones/hechos, llaves e integridad referencial.|10%|
|Consultas Analíticas y KPIs|Cinco salidas analíticas correctas generadas desde el DW y alineadas con R1–R5.|10%|
|Análisis e Interpretación de Negocio|Las visualizaciones y hallazgos interpretan correctamente los resultados analíticos y los conectan con decisiones de negocio.|10%|
|Repositorio, Reproducibilidad y Documentación|Repositorio de GitHub organizado, README, requirements, .gitignore, instrucciones de ejecución claras y documentación profesional.|5%|
|**Total**||**80%**|

### Parte B — Presentación y Sustentación: 20%

|Criterio|Peso|
|-|-|
|Comprensión de la solución propuesta|5%|
|Explicación y justificación de las decisiones técnicas|5%|
|Interpretación de negocio de los resultados|4%|
|Respuesta a preguntas / dominio individual|4%|
|Claridad, organización y comunicación profesional|2%|
|**Total Presentación**|**20%**|



