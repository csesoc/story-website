DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
    uid SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    github TEXT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS Questions;
CREATE TABLE Questions (
    qid SERIAL PRIMARY KEY,
    cid FOREIGN KEY references Competitions(cid),
    numParts INTEGER NOT NULL,
    name TEXT NOT NULL,
    pixelArtLine TEXT NOT NULL,
    dayNum INTEGER UNIQUE NOT NULL
);

DROP TABLE IF EXISTS Parts;
CREATE TABLE Parts (
    qid FOREIGN KEY references Questions(qid),
    description TEXT NOT NULL,
    partNum INTEGER NOT NULL,
    numSolved INTEGER NOT NULL,
    bestTime TIME,
    PRIMARY KEY (qid, partNum)
);

DROP TABLE IF EXISTS Competitions;
CREATE TABLE Competitions (
    cid SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    numUsers INTEGER NOT NULL,
    numQuestions INTEGER NOT NULL
);

DROP TABLE IF EXISTS Inputs;
CREATE TABLE Inputs (
    iid SERIAL PRIMARY KEY,
    qid FOREIGN KEY references Questions(qid),
    uid FOREIGN KEY references Users(id),
    input TEXT NOT NULL,
    solution TEXT NOT NULL
);

DROP TABLE IF EXISTS Solves;
CREATE TABLE Solves (
    uid INTEGER,
    pid INTEGER,
    solveTime TIME NOT NULL,
    points INTEGER NOT NULL,
    PRIMARY KEY (uid, pid),
    FOREIGN KEY (uid) REFERENCES Users(uid),
    FOREIGN KEY (pid) REFERENCES Parts(pid)
);
