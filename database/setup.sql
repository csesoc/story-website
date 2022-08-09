DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
    uid      SERIAL PRIMARY KEY,
    email    TEXT UNIQUE NOT NULL,
    github   TEXT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS Competitions;
CREATE TABLE Competitions (
    cid          SERIAL PRIMARY KEY,
    name         TEXT UNIQUE NOT NULL,
    numUsers     INTEGER NOT NULL DEFAULT 0,
    numQuestions INTEGER NOT NULL DEFAULT 0
);

DROP TABLE IF EXISTS Stats;
CREATE TABLE Stats (
    uid         SERIAL REFERENCES Users(uid), 
    cid         SERIAL REFERENCES Competitions(cid),
    numStars    INTEGER NOT NULL DEFAULT 0,
    score       INTEGER NOT NULL DEFAULT 0
);

DROP TABLE IF EXISTS Questions;
CREATE TABLE Questions (
    qid          SERIAL PRIMARY KEY,
    cid          SERIAL REFERENCES Competitions(cid),
    numParts     INTEGER NOT NULL DEFAULT 2,
    name         TEXT NOT NULL,
    pixelArtLine TEXT NOT NULL,
    dayNum       INTEGER UNIQUE NOT NULL
);

-- has two primary keys.
-- pid is so that the solves can reference it, but the real unique identifier is also qid and partNum
DROP TABLE IF EXISTS Parts;
CREATE TABLE Parts (
    pid          SERIAL PRIMARY KEY,
    qid          SERIAL REFERENCES Questions(qid),
    description  TEXT NOT NULL,
    partNum      INTEGER NOT NULL,
    numSolved    INTEGER NOT NULL DEFAULT 0,
    bestTime     TIME
);

DROP TABLE IF EXISTS Inputs;
CREATE TABLE Inputs (
    iid         SERIAL PRIMARY KEY,
    qid         SERIAL REFERENCES Questions(qid),
    uid         SERIAL REFERENCES Users(uid),
    input       TEXT NOT NULL,
    solution    TEXT NOT NULL
);

DROP TABLE IF EXISTS Solves;
CREATE TABLE Solves (
    uid         INTEGER REFERENCES Users(uid),
    pid         INTEGER REFERENCES Parts(pid),
    solveTime   TIME NOT NULL,
    points      INTEGER NOT NULL,
    PRIMARY KEY (uid, pid)
);

CREATE OR REPLACE FUNCTION truncate_tables() RETURNS void AS $$
DECLARE
    statements CURSOR FOR
        SELECT tablename FROM pg_tables WHERE tablename in ('parts', 'users', 'competitions', 'stats', 'questions', 'inputs', 'solves');
BEGIN
    FOR stmt IN statements LOOP
        EXECUTE 'TRUNCATE TABLE ' || quote_ident(stmt.tablename) || ' CASCADE;';
    END LOOP;
END;
$$ LANGUAGE plpgsql;