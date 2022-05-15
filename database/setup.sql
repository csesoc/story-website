DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
    uid SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    numStars INTEGER NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS Questions;
CREATE TABLE Questions (
    qid SERIAL PRIMARY KEY,
    numParts INTEGER NOT NULL,
    numSolved INTEGER NOT NULL,
    bestTime TIME,
    dayNum INTEGER UNIQUE NOT NULL
);

DROP TABLE IF EXISTS Questions;
CREATE TABLE Questions (
    qid SERIAL PRIMARY KEY,
    numParts INTEGER NOT NULL,
    numSolved INTEGER NOT NULL,
    bestTime TIME,
    dayNum INTEGER UNIQUE NOT NULL
);

DROP TABLE IF EXISTS Inputs;
CREATE TABLE Inputs (
    iid SERIAL PRIMARY KEY,
    qid FOREIGN KEY references Questions(qid),
    solution TEXT NOT NULL
);

DROP TABLE IF EXISTS Solves;
CREATE TABLE Solves (
    uid INTEGER,
    qid INTEGER,
    solveTime TIME NOT NULL,
    PRIMARY KEY (uid, qid),
    FOREIGN KEY (uid) REFERENCES Users(uid),
    FOREIGN KEY (qid) REFERENCES Questions(qid)
);

