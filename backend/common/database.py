import os
import psycopg2

from models.user import User

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
host = os.environ["POSTGRES_HOST"]
port = os.environ["POSTGRES_PORT"]
database = os.environ["POSTGRES_DB"]

def get_connection():
    conn = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )

    return conn

conn = get_connection()
cur = conn.cursor()

# IMPORTANT: executing a query is expensive, so we would rather write more functions than write more execute queries.

# # DO NOT EVER EXECUTE THIS FUNCTION BRUH
# def dropDatabase():
#     query = f"""
#         SELECT 'DROP TABLE IF EXISTS "' || tablename || '" CASCADE;'
#         from
#         pg_tables WHERE schemaname = 'advent';
#     """
#     cur.execute(query)
#     conn.commit()

# IMPORTANT: executing a query is expensive, so we would rather write more functions than write more execute queries.

# Get all the information about a question given its day number
# Returns all information in the form of a dictionary
# You might want to use this function to find the total number of parts in a question, and then use getPartInfo
def getQuestionInfo(compName, dayNum):
    query = f"""
        select * from Questions q
        join Competitions c on q.cid = c.cid
        where q.dayNum = {dayNum} and c.name = '{compName}';
    """
    cur.execute(query)

    # only one entry should be returned since day number is unique
    t = cur.fetchone()
    return t

# Get all the parts given a day number of a question
# Returns all information in the form of a list of dictionaries
def getQuestionParts(compName, dayNum):
    query = f"""
        select * from Parts p
        join Questions q on p.qid = q.qid
        join Competitions c on q.cid = c.cid
        where q.dayNum = {dayNum} and c.name = '{compName}';
    """
    cur.execute(query)

    partsList = []
    for t in cur.fetchall():
        partsList.append(t)

    # sort the list based off the part number
    sortedList = sorted(partsList, key=lambda x: x['partNum'])
    return sortedList

# Get all the information about a part of a question (e.g. day 1 part 2) given the day number and part number
# Same as above but more specific
# Returns all information in the form of a dictionary
def getPartInfo(compName, dayNum, partNum):
    query = f"""
        select * from Parts p
        join Questions q on p.qid = q.qid
        join Competitions c on q.cid = c.cid
        where q.dayNum = {dayNum} and p.partNum = {partNum} and c.name = '{compName}';
    """
    cur.execute(query)

    # only one entry should be returned since day number is unique
    t = cur.fetchone()
    return t

# Get all the questions that pertain to a certain competition, by name
# Returns None if the competition does not exist
def getCompetitionQuestions(compName):
    query = f"""
        select * from Parts p
        join Questions q on p.qid = q.qid
        join Competitions c on q.cid = c.cid
        where c.name = '{compName}';
    """
    cur.execute(query)

    # only one entry should be returned since day number is unique
    return cur.fetchall()

# Gets a competition
def getCompetition(compName):
    query = f"""
        select * from Competitions c
        where c.name = '{compName}';
    """
    cur.execute(query)

    # only one entry should be returned since day number is unique
    return cur.fetchall()

# Unfinished function.
# Dynamically generates a new input for a user and day number
def generateInput(dayNum, uid):
    pass

# Gets the input for a day number and user, if it exists
# Returns the input string, else returns None
def getInput(compName, dayNum, uid):
    query = f"""
        select i.input from Inputs i
        join Questions q on i.qid = q.qid
        join Competitions c on q.cid = c.cid
        where q.dayNum = {dayNum} and i.uid = {uid} and c.name = '{compName}';
    """
    cur.execute(query)

    t = cur.fetchone()
    return t['input'] if t is not None else t

# Gets the input for a day number and user, if it exists
# Returns a tuple:
#   the tuple is None if the value does not exist
#   the first entry of the tuple is True if the solution is correct (and exists), False otherwise
#   the second entry of the tuple is a string outlining the reason if the solution was incorrect
#       not sure what to put here so just leaving as empty string for now
def checkInput(compName, dayNum, uid, solution):
    query = f"""
        select i.input, i.solution from Inputs i
        join Questions q on i.qid = q.qid
        join Competitions c on q.cid = c.cid
        where q.dayNum = {dayNum} and i.uid = {uid} and c.name = '{compName}';
    """
    cur.execute(query)

    t = cur.fetchone()
    if t is None:
        return None
    elif t['solution'].lower() == solution.strip().lower():
        # can change this later, but iirc advent of code is also not case sensitive
        return (True, "")
    else:
        return (False, "")

    # note: for more advanced processing, we might consider having a timeout if a user tries too many things too quickly
    # but idk how to implement this too well

# Get all the information about a user's stats in a certain competition
# Returns all information in the form of a list of 'solved objects'
def getUserStatsPerComp(compName, uid):

    # A right outer join returns all the results from the parts table, even if there is no solves
    # Best to look up examples :D
    # Use this information to deduce whether a user has solved a part or not
    query = f"""
        select u.username, u.github, q.dayNum, p.partNum, s.points, s.solveTime from Users u
        join Solves s on s.uid = u.uid
        right outer join Parts p on s.pid = p.pid
        join Questions q on p.qid = q.qid
        join Competitions c on q.cid = c.cid
        where s.uid = {uid} and c.name = '{compName}';
    """
    cur.execute(query)

    return cur.fetchall()

# Get only the number of stars and points for a user.
# Returns extremely simple info
def getBasicUserStatsPerComp(compName, uid):

    # A right outer join returns all the results from the parts table, even if there is no solves
    # Best to look up examples :D
    # Use this information to deduce whether a user has solved a part or not
    query = f"""
        select u.username, u.github, s.numStars, s.score from Stats s
        right outer join Users u
        where s.uid = {uid} and c.name = '{compName}';
        join Questions q on p.qid = q.qid
        join Competitions c on q.cid = c.cid
        where i.uid = {uid} and c.name = {compName};
    """
    cur.execute(query)

    return cur.fetchall()

# Could be very large
def getAllUsers():
    query = f"""
        select * from Users;
    """
    cur.execute(query)

    return cur.fetchall()

# Could be very large
def getAllCompetitions():
    query = f"""
        select * from Competitions;
    """
    cur.execute(query)

    return cur.fetchall()

# Pre conditions assume we have already checked that noone has that username
# TODO: No idea whether this works lol never done something like this before
def updateUsername(username, uid):
    query = f"""
        update Users
        set username = {username}
        where uid = {uid};
    """
    cur.execute(query)
    conn.commit()

# Finds top N of a leaderboard, where N is a positive integer
# Assumes comp name is legit

# TODO: fix tiebreakers in rankings
def getNLeaderboard(compName, n):
    query = f"""
        select u.github, u.username, s.numStars, s.score from Users u
        join Stats s on s.uid = u.uid
        join Competitions c on s.cid = c.cid
        where c.name = '{compName}'
        order by s.score DESC
        limit {n};
    """
    cur.execute(query)

    return cur.fetchall()


# Finds top N of a leaderboard of all users who begin with prefix
# Assumes comp name is legit
# TODO: left outer join may not work! Needs to be tested on people with no puzzle input.
def searchLeaderboard(compName, prefix, n):
    query = f"""
        select u.github, u.username, s.numStars, s.score from Users u
        left outer join Stats s on s.uid = u.uid
        join Competitions c on s.cid = c.cid
        where c.name = '{compName}' and (u.username like '{prefix}%' or u.github like '{prefix}%')
        order by s.score DESC
        limit {n};
    """
    cur.execute(query)

    return cur.fetchall()


# Finds your ranking in a certain competition

# TODO: not sure if this even works
def getRankLeaderboard(compName, uid):
    query = f"""
        select position
        from (
            select u.uid as bigUid, *, row_number() over(
                order by s.score DESC
                )
            as position
        from Users u
        left outer join Stats s on s.uid = u.uid
        join Competitions c on s.cid = c.cid
        where c.name = '{compName}'
        ) result where bigUid = {uid};
    """
    cur.execute(query)

    return cur.fetchall()

def addCompetition(compName):
    query = f""" 
        insert into Competitions
        values (1, '{compName}', 0, 0);
    """
    cur.execute(query)
    conn.commit()

def addSolve(uid, pid, timeSolved, pointsGained):
    query = f""" 
        insert into Solves
        values ({uid}, {pid}, {timeSolved}, {pointsGained});
    """
    cur.execute(query)
    conn.commit()

def addUser(uid, username, email, githubLink, password):
    query = f""" 
        INSERT INTO Users VALUES ({uid}, '{email}', '{githubLink}', '{username}', '{password}');
    """
    cur.execute(query)
    conn.commit()

def addReplica(compName, questionName, dayNum, partDescription, username, email, githubLink, password):
    query = f""" 
        INSERT INTO Users VALUES (42, '{email}', '{githubLink}', '{username}', '{password}');
    """
    cur.execute(query)
    conn.commit()

    query = f""" 
        insert into Competitions
        values (1, '{compName}', 0, 0);
    """
    cur.execute(query)
    conn.commit()

    query = f""" 
        insert into Questions
        values (1, 1, 0, '{questionName}', '.-.', {dayNum});
    """
    cur.execute(query)
    conn.commit()

    query = f""" 
        insert into Parts
        values (1, 1, '{partDescription}', 1, 0, '2008-11-11 13:23:44');
    """
    cur.execute(query)
    conn.commit()

    query = f""" 
        insert into Solves
        values (42, 1, 100, 100);
    """
    cur.execute(query)
    conn.commit()

# Check if they've solved
def checkSolve(compName, dayNum, partNum, uid):
    query = f""" 
        select * from Solves s 
        join Parts p on p.pid = s.pid
        join Questions q on p.qid = q.qid
        join Competitions c on q.cid = c.cid
        where c.name = '{compName}' and s.uid = {uid} and p.partNum = {partNum} and q.dayNum = {dayNum};
    """
    cur.execute(query)

    return (len(cur.fetchall()) == 1)

# Create a solve.
# This requires you to know the part id, solve time and number of points
def createSolve(uid, pid, solveTime, points):
    query = f""" 
        insert into Solves s 
        values ({uid}, {pid}, {solveTime}, {points});
    """
    cur.execute(query)
    conn.commit()

# Gets the pid given compName, dayNum, partNum
def findPid(compName, dayNum, partNum):
    query = f""" 
        select p.pid from Parts p
        join Questions q on p.qid = q.qid
        join Competitions c on q.cid = c.cid
        where c.name = '{compName}' and p.partNum = {partNum} and q.dayNum = {dayNum};
    """
    cur.execute(query)

    return cur.fetchall()

# Get number of people who have already solved
def getNumSolved(compName, dayNum, partNum, uid):
    query = f""" 
        select count(*) from Solves s 
        join Parts p on p.pid = s.pid
        join Questions q on p.qid = q.qid
        join Competitions c on q.cid = c.cid
        where c.name = '{compName}' and s.uid = {uid} and p.partNum = {partNum} and q.dayNum = {dayNum};
    """
    cur.execute(query)

    return cur.fetchall()

def add_user_with_uid(uid, email, username, password):
    """Adds a user to the database, returning their ID."""
    query = f""" 
        INSERT INTO Users VALUES ({uid}, '{email}', 'blah', '{username}', '{User.hash_password(password)}');
    """
    cur.execute(query)
    conn.commit()
