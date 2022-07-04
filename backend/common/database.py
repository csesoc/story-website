import os
import psycopg2

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
host = os.environ["POSTGRES_HOST"]
port = os.environ["POSTGRES_PORT"]
database = os.environ["POSTGRES_DB"]

TABLES = ["Users", "Questions", "Competitions", "Inputs", "Solves"]

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

# Get all the information about a question given its day number
# Returns all information in the form of a dictionary
# You might want to use this function to find the total number of parts in a question, and then use getPartInfo
def getQuestionInfo(compName, dayNum):
    query = f"""
        select * from Questions q
        join Competitions c on q.cid = c.cid 
        where q.dayNum = {dayNum} and c.name = {compName};
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
        where q.dayNum = {dayNum} and c.name = {compName};
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
        where q.dayNum = {dayNum} and p.partNum = {partNum} and c.name = {compName};
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
        where c.name = {compName};
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
        where q.dayNum = {dayNum} and i.uid = {uid} and c.name = {compName};
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
        where q.dayNum = {dayNum} and i.uid = {uid} and c.name = {compName};
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

# Get all the information about a user given their uid
# Returns all information in the form of a dictionary
def getUserInfo(uid):
    query = f"""
        select * from Users where uid = {uid};
    """
    cur.execute(query)

    # only one entry should be returned since day number is unique
    t = cur.fetchone()
    return t

# Get all the information about a user's stats in a certain competition
# Returns all information in the form of a list of 'solved objects'
def getUserStatsPerComp(compName, uid):

    # A right outer join returns all the results from the parts table, even if there is no solves
    # Best to look up examples :D 
    # Use this information to deduce whether a user has solved a part or not
    query = f"""
        select q.dayNum, p.partNum, s.points, s.solveTime from Solves s
        right outer join Parts p on s.pid = p.pid
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
# No idea whether this works lol never done something like this before
def updateUsername(username, uid):
    query = f"""
        update Users
        set username = {username}
        where uid = {uid};
    """
    cur.execute(query)
    conn.commit()

# DO NOT EVER EXECUTE THIS FUNCTION BRUH
def dropDatabase():
    query = f"""
        SELECT 'DROP TABLE IF EXISTS "' || tablename || '" CASCADE;' 
        from
        pg_tables WHERE schemaname = 'advent';
    """
    cur.execute(query)
    conn.commit()

def clear_database():
    conn = get_connection()
    cursor = conn.cursor()

    for table in TABLES:
        cursor.execute(f"TRUNCATE TABLE {table} CASCADE")

    conn.commit()

    cursor.close()
    conn.close()