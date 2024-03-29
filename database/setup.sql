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
    numParts     INTEGER NOT NULL DEFAULT 0,
    name         TEXT NOT NULL,
    pixelArtLine TEXT,
    dayNum       INTEGER UNIQUE NOT NULL
);

-- has two primary keys.
-- pid is so that the solves can reference it, but the real unique identifier is also qid and partNum
DROP TABLE IF EXISTS Parts;
CREATE TABLE Parts (
    pid          SERIAL PRIMARY KEY,
    qid          SERIAL REFERENCES Questions(qid),
    description  TEXT,
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
    uid         SERIAL REFERENCES Users(uid),
    pid         SERIAL REFERENCES Parts(pid),
    solveTime   BIGINT NOT NULL,
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


-- TODO: Fix triggers! -----------------------------------------------------------------------------------------------------------------------

create unique index statsIndex on Stats (uid, cid);

-- Creates a trigger to update stats whenever solves is updated
CREATE OR REPLACE FUNCTION update_stats() RETURNS trigger AS $$
BEGIN
    insert into Stats as s
    values (new.uid, (select c.cid from Competitions c join Questions q on q.cid = c.cid join Parts p on p.qid = q.qid where p.pid = new.pid), 1, new.points)
    on conflict (uid, cid)
    do
        update set  score = s.score + new.points, numStars = s.numStars + 1
        where       s.uid = new.uid and s.cid = 
            (select c.cid from Competitions c join Questions q on q.cid = c.cid join Parts p on p.qid = q.qid where p.pid = new.pid);
    return  new;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER update_stats
AFTER INSERT ON Solves
for each ROW EXECUTE PROCEDURE update_stats();

-- Creates a trigger to update numQuestions whenever a question is added
CREATE OR REPLACE FUNCTION update_comp_questions() RETURNS trigger AS $$
BEGIN
    update  Competitions
    set     numQuestions = numQuestions + 1
    where   Competitions.cid = new.cid;
    return  new;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER update_comp_questions
AFTER INSERT ON Questions
for each ROW EXECUTE PROCEDURE update_comp_questions();

-- Creates a trigger to update numParts whenever a part is added
CREATE OR REPLACE FUNCTION update_question_parts() RETURNS trigger AS $$
BEGIN
    update  Questions
    set     numParts = numParts + 1
    where   Questions.qid = new.qid;
    return  new;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER update_question_parts
AFTER INSERT ON Parts
for each ROW EXECUTE PROCEDURE update_question_parts();

-- Creates a trigger to update numSolved whenever a part is added
CREATE OR REPLACE FUNCTION update_parts_solved() RETURNS trigger AS $$
BEGIN
    update  Parts
    set     numSolved = numSolved + 1
    where   Parts.pid = new.pid;
    return  new;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER update_parts_solved
AFTER INSERT ON Solves
for each ROW EXECUTE PROCEDURE update_parts_solved();