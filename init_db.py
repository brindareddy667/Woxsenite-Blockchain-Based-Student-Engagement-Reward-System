import sqlite3, os

if os.path.exists("woxsenite.db"):
    os.remove("woxsenite.db")

if not os.path.exists("uploads"):
    os.makedirs("uploads")

conn = sqlite3.connect("woxsenite.db")
cur = conn.cursor()

# USERS
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    roll_no TEXT,
    course TEXT,
    wallet TEXT,
    balance INTEGER
)
""")

# TIMETABLE
cur.execute("""
CREATE TABLE timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    day TEXT,
    time TEXT,
    subject TEXT
)
""")

# ATTENDANCE REQUESTS
cur.execute("""
CREATE TABLE requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT,
    label TEXT,
    tokens INTEGER,
    status TEXT
)
""")

# EVENTS
cur.execute("""
CREATE TABLE event_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    category TEXT,
    title TEXT,
    project_title TEXT,
    doc_file TEXT,
    certificate_file TEXT,
    tokens INTEGER,
    ai_confidence REAL,
    ai_name_match INTEGER,
    ai_tamper INTEGER,
    status TEXT
)
""")

# TRANSACTIONS
cur.execute("""
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    description TEXT,
    tokens INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

students = [
(1,"Student One","23WU0101001","B.Tech CSE","0xWALLET001",0),
(2,"Student Two","23WU0101002","B.Tech AI","0xWALLET002",0),
(3,"Student Three","23WU0101003","B.Tech DS","0xWALLET003",0)
]

cur.executemany("INSERT INTO users VALUES (?,?,?,?,?,?)", students)

week = {
"Monday":[("9-10","DSA"),("10-11","OS"),("11-12","Maths"),("2-3","CN"),("3-4","AI")],
"Tuesday":[("9-10","ML"),("10-11","DSA"),("11-12","OS"),("2-3","CN"),("3-4","AI")],
"Wednesday":[("9-10","Maths"),("10-11","ML"),("11-12","DSA"),("2-3","CN"),("3-4","AI")],
"Thursday":[("9-10","OS"),("10-11","Maths"),("11-12","ML"),("2-3","Lab"),("3-4","AI")],
"Friday":[("9-10","DSA"),("10-11","OS"),("11-12","Maths"),("2-3","Seminar"),("3-4","AI")]
}

for s in students:
    uid=s[0]
    for day,slots in week.items():
        for time,subject in slots:
            cur.execute(
            "INSERT INTO timetable (user_id,day,time,subject) VALUES (?,?,?,?)",
            (uid,day,time,subject))

conn.commit()
conn.close()

print("Database initialized")