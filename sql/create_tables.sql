CREATE DATABASE recruitment_dw;

USE recruitment_dw;

CREATE TABLE DimDate (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    quarter INT NOT NULL
);

CREATE TABLE DimTechnology (
    technology_key INT PRIMARY KEY,
    technology_name VARCHAR(100) NOT NULL
);

CREATE TABLE DimCandidateProfile (
    profile_key INT PRIMARY KEY,
    seniority VARCHAR(50) NOT NULL,
    yoe_range VARCHAR(20) NOT NULL
);

CREATE TABLE DimCountry (
    country_key INT PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL
);

CREATE TABLE DimCandidate (
    candidate_key INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL
);

CREATE TABLE FactApplications (
    application_key INT PRIMARY KEY,
    date_key INT NOT NULL,
    technology_key INT NOT NULL,
    profile_key INT NOT NULL,
    country_key INT NOT NULL,
    candidate_key INT NOT NULL,
    code_challenge_score INT NOT NULL,
    technical_interview_score INT NOT NULL,
    is_hired INT NOT NULL,
    application_count INT NOT NULL,
    FOREIGN KEY (date_key) REFERENCES DimDate(date_key),
    FOREIGN KEY (technology_key) REFERENCES DimTechnology(technology_key),
    FOREIGN KEY (profile_key) REFERENCES DimCandidateProfile(profile_key),
    FOREIGN KEY (country_key) REFERENCES DimCountry(country_key),
    FOREIGN KEY (candidate_key) REFERENCES DimCandidate(candidate_key)
);