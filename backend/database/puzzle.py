from database.database import db

def add_question(name, dayNum, numParts):
    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Questions (name, dayNum, numParts) VALUES (%s, %s, %s)",
                       (name, dayNum, numParts))
        conn.commit()

        cursor.execute("SELECT qid FROM Questions WHERE name = %s", (name,))
        qid = cursor.fetchone()[0]
    db.putconn(conn)

    return qid

def add_part(qid, partNum):
    conn = db.getconn()

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Parts (qid, dayNum) VALUES (%s, %s, %s)",
                       (qid, partNum))
        conn.commit()

    db.putconn(conn)
