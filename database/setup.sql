DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
    uid SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    numStars INTEGER NOT NULL,
    score INTEGER NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS Questions;
CREATE TABLE Questions (
    qid SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    partNum INTEGER NOT NULL,
    numParts INTEGER NOT NULL,
    numSolved INTEGER NOT NULL,
    bestTime TIME,
    dayNum INTEGER UNIQUE NOT NULL
);

DROP TABLE IF EXISTS Competitions;
CREATE TABLE Competitions (
    cid SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    numUsers INTEGER NOT NULL,
    questions TEXT 
);

DROP TABLE IF EXISTS Inputs;
CREATE TABLE Inputs (
    iid SERIAL PRIMARY KEY,
    qid INTEGER,
    solution TEXT NOT NULL,
    FOREIGN KEY (qid) REFERENCES Questions(qid)
);

DROP TABLE IF EXISTS Solves;
CREATE TABLE Solves (
    uid INTEGER,
    qid INTEGER,
    solveTime TIME NOT NULL,
    points INTEGER NOT NULL,
    PRIMARY KEY (uid, qid),
    FOREIGN KEY (uid) REFERENCES Users(uid),
    FOREIGN KEY (qid) REFERENCES Questions(qid)
);
