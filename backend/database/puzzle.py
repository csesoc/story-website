from database.database import db

def add_competition(name):
    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Competitions (name) VALUES ('%s')" % (name))
        conn.commit()

        cursor.execute("SELECT cid FROM Competitions WHERE name = '%s'" % (name,))
        cid = cursor.fetchone()[0]
    db.putconn(conn)

    return cid

def add_question(cid, name, dayNum, numParts):
    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Questions (cid, name, dayNum, numParts) VALUES (%d, '%s', %d, %d)" % (cid, name, dayNum, numParts))
        conn.commit()

        cursor.execute("SELECT qid FROM Questions WHERE name = '%s'" % (name,))
        qid = cursor.fetchone()[0]
    db.putconn(conn)

    return qid

def add_part(qid, partNum):
    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Parts (qid, partNum) VALUES (%d, %d)" % (qid, partNum))
        conn.commit()

    db.putconn(conn)
