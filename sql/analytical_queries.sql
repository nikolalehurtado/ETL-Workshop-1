-- ============================================================
-- R1 - Tendencias de Contratación en el Tiempo
-- Pregunta: ¿Cómo varía la tasa de contratación mes a mes?
-- ============================================================
SELECT
    d.year,
    d.month,
    SUM(f.application_count) AS total_aplicaciones,
    SUM(f.is_hired) AS total_contratados,
    ROUND(SUM(f.is_hired) / SUM(f.application_count) * 100, 2) AS tasa_contratacion_pct
FROM FactApplications f
JOIN DimDate d ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;



-- ============================================================
-- R2 - Comparación de Tecnologías
-- Pregunta: ¿Qué tecnologías generan mayor número y proporción de contratados?
-- ============================================================
SELECT
    t.technology_name,
    SUM(f.application_count) AS total_aplicaciones,
    SUM(f.is_hired) AS total_contratados,
    ROUND(SUM(f.is_hired) / SUM(f.application_count) * 100, 2) AS tasa_contratacion_pct
FROM FactApplications f
JOIN DimTechnology t ON f.technology_key = t.technology_key
GROUP BY t.technology_name
ORDER BY tasa_contratacion_pct DESC;



-- ============================================================
-- R3 - Perfil del Candidato (Seniority + Años de Experiencia)
-- Pregunta: ¿Existen diferencias en la tasa de contratación según el perfil?
-- ============================================================
SELECT
    p.seniority,
    p.yoe_range,
    SUM(f.application_count) AS total_aplicaciones,
    SUM(f.is_hired) AS total_contratados,
    ROUND(SUM(f.is_hired) / SUM(f.application_count) * 100, 2) AS tasa_contratacion_pct
FROM FactApplications f
JOIN DimCandidateProfile p ON f.profile_key = p.profile_key
GROUP BY p.seniority, p.yoe_range
ORDER BY p.seniority, p.yoe_range;



-- ============================================================
-- R4 - País de Origen (Top 10 por volumen de aplicaciones)
-- Pregunta: ¿Qué países tienen mayor volumen y cuál es su tasa de contratación?
-- ============================================================
SELECT
    c.country_name,
    SUM(f.application_count) AS total_aplicaciones,
    SUM(f.is_hired) AS total_contratados,
    ROUND(SUM(f.is_hired) / SUM(f.application_count) * 100, 2) AS tasa_contratacion_pct
FROM FactApplications f
JOIN DimCountry c ON f.country_key = c.country_key
GROUP BY c.country_name
ORDER BY total_aplicaciones DESC
LIMIT 10;

-- ============================================================
-- R5 - Efecto de la Reaplicación
-- Pregunta: ¿Los candidatos que reaplican tienen distinta tasa de contratación?
-- ============================================================
SELECT
    CASE
        WHEN app_count_per_candidate > 1 THEN 'Reaplicó'
        ELSE 'Aplicó una sola vez'
    END AS grupo,
    COUNT(DISTINCT candidate_key) AS total_candidatos,
    SUM(is_hired) AS total_contratados_aplicaciones,
    ROUND(SUM(is_hired) / COUNT(*) * 100, 2) AS tasa_contratacion_pct
FROM (
    SELECT
        f.candidate_key,
        f.is_hired,
        COUNT(*) OVER (PARTITION BY f.candidate_key) AS app_count_per_candidate
    FROM FactApplications f
) sub
GROUP BY grupo;