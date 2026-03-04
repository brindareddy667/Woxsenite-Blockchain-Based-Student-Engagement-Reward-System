from flask import Flask, render_template, request, redirect
import sqlite3, os
from datetime import datetime
from ai_verifier import verify_certificate

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def db():
    return sqlite3.connect("woxsenite.db")

def today():
    return datetime.now().strftime("%A")

EVENT_POINTS = {
"Hackathon":100,
"Certification":30,
"Sports":70,
"Research":200,
"Club":50
}

@app.route("/")
def home():
    return redirect("/student/1")

# ================= STUDENT =================

@app.route("/student/<int:user_id>")
def student(user_id):

    con=db()
    cur=con.cursor()

    cur.execute("SELECT * FROM users")
    students=cur.fetchall()

    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    student=cur.fetchone()

    cur.execute("""
    SELECT day,time,subject FROM timetable
    WHERE user_id=?
    ORDER BY
    CASE day
    WHEN 'Monday' THEN 1
    WHEN 'Tuesday' THEN 2
    WHEN 'Wednesday' THEN 3
    WHEN 'Thursday' THEN 4
    WHEN 'Friday' THEN 5
    END,time
    """,(user_id,))
    timetable=cur.fetchall()

    cur.execute("""
    SELECT time,subject FROM timetable
    WHERE user_id=? AND day=?
    """,(user_id,today()))
    today_classes=cur.fetchall()

    cur.execute("""
    SELECT COUNT(*) FROM requests
    WHERE user_id=? AND type='attendance'
    AND label LIKE ?
    """,(user_id,f"{today()}%"))

    already_marked=cur.fetchone()[0]>0

    cur.execute("""
    SELECT description,tokens,timestamp
    FROM transactions
    WHERE user_id=?
    ORDER BY timestamp DESC
    """,(user_id,))
    transactions=cur.fetchall()

    con.close()

    return render_template(
        "student.html",
        students=students,
        student=student,
        timetable=timetable,
        today_classes=today_classes,
        already_marked=already_marked,
        transactions=transactions,
        today=today()
    )

# ================= ATTENDANCE =================

@app.route("/start_attendance", methods=["POST"])
def start_attendance():

    user_id=request.form["user_id"]
    return redirect(f"/student/{user_id}?marking=1&section=attendance")


@app.route("/mark_today", methods=["POST"])
def mark_today():

    user_id=request.form["user_id"]
    subjects=request.form.getlist("subjects")

    con=db()
    cur=con.cursor()

    for s in subjects:

        cur.execute("""
        INSERT INTO requests
        (user_id,type,label,tokens,status)
        VALUES (?,?,?,?,?)
        """,
        (user_id,"attendance",f"{today()} - {s}",10,"PENDING"))

    con.commit()
    con.close()

    return redirect(f"/student/{user_id}?section=attendance")

# ================= EVENTS =================

@app.route("/submit_event", methods=["POST"])
def submit_event():

    user_id=request.form["user_id"]
    category=request.form["category"]
    title=request.form["title"]
    project=request.form.get("project","")

    doc=request.files.get("doc")
    cert=request.files.get("cert")

    doc_name=""
    cert_name=""

    if doc and doc.filename:
        doc_name=doc.filename
        doc.save(os.path.join(UPLOAD_FOLDER,doc_name))

    if cert and cert.filename:
        cert_name=cert.filename
        cert_path=os.path.join(UPLOAD_FOLDER,cert_name)
        cert.save(cert_path)

    tokens=EVENT_POINTS.get(category,0)

    ai_conf=0
    ai_match=0
    ai_tamper=0

    if cert_name:

        con=db()
        cur=con.cursor()

        cur.execute("SELECT name FROM users WHERE id=?", (user_id,))
        student_name=cur.fetchone()[0]

        con.close()

        ai=verify_certificate(cert_path,student_name,category)

        ai_conf=ai["confidence"]
        ai_match=int(ai["name_match"])
        ai_tamper=int(ai["edited"])

        # if name mismatch give warning
        if not ai_match:
            return f"""
            ⚠ Student name not found on certificate.
            <br><br>
            Please upload a valid certificate with your name.
            <br><br>
            <a href="/student/{user_id}?section=events">Go Back</a>
            """

    con=db()
    cur=con.cursor()

    cur.execute("""
    INSERT INTO event_requests
    (user_id,category,title,project_title,doc_file,certificate_file,
    tokens,ai_confidence,ai_name_match,ai_tamper,status)
    VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """,
    (user_id,category,title,project,doc_name,cert_name,
    tokens,ai_conf,ai_match,ai_tamper,"PENDING"))

    con.commit()
    con.close()

    return redirect(f"/student/{user_id}?event_success=1&section=events")

# ================= ADMIN =================

@app.route("/admin")
def admin():

    con=db()
    cur=con.cursor()

    cur.execute("""
    SELECT u.id,u.name,u.roll_no,COUNT(x.user_id)
    FROM users u
    JOIN (
        SELECT user_id FROM requests WHERE status='PENDING'
        UNION ALL
        SELECT user_id FROM event_requests WHERE status='PENDING'
    ) x ON u.id=x.user_id
    GROUP BY u.id
    """)

    students=cur.fetchall()

    con.close()

    return render_template("admin.html",students=students)

# ================= ADMIN STUDENT =================

@app.route("/admin/student/<int:user_id>")
def admin_student(user_id):

    con=db()
    cur=con.cursor()

    cur.execute("""
    SELECT name,roll_no,course,balance
    FROM users
    WHERE id=?
    """,(user_id,))
    student=cur.fetchone()

    cur.execute("""
    SELECT id,label,tokens
    FROM requests
    WHERE user_id=? AND status='PENDING'
    """,(user_id,))
    attendance=cur.fetchall()

    cur.execute("""
    SELECT id,category,title,project_title,doc_file,certificate_file,
    tokens,ai_confidence,ai_name_match,ai_tamper
    FROM event_requests
    WHERE user_id=? AND status='PENDING'
    """,(user_id,))
    events=cur.fetchall()

    con.close()

    return render_template(
        "admin_student.html",
        student=student,
        attendance=attendance,
        events=events,
        user_id=user_id
    )

# ================= APPROVE ATTENDANCE =================

@app.route("/approve_attendance/<int:req_id>/<int:user_id>")
def approve_attendance(req_id,user_id):

    con=db()
    cur=con.cursor()

    cur.execute("SELECT label,tokens FROM requests WHERE id=?", (req_id,))
    label,tokens=cur.fetchone()

    cur.execute("UPDATE requests SET status='APPROVED' WHERE id=?", (req_id,))

    cur.execute("""
    UPDATE users
    SET balance = balance + ?
    WHERE id=?
    """,(tokens,user_id))

    cur.execute("""
    INSERT INTO transactions
    (user_id,description,tokens)
    VALUES (?,?,?)
    """,(user_id,f"{label} approved",tokens))

    con.commit()
    con.close()

    return redirect(f"/admin/student/{user_id}")

# ================= APPROVE EVENT =================

@app.route("/approve_event/<int:req_id>/<int:user_id>")
def approve_event(req_id,user_id):

    con=db()
    cur=con.cursor()

    cur.execute("""
    SELECT category,title,tokens
    FROM event_requests
    WHERE id=?
    """,(req_id,))
    cat,title,tokens=cur.fetchone()

    cur.execute("""
    UPDATE event_requests
    SET status='APPROVED'
    WHERE id=?
    """,(req_id,))

    cur.execute("""
    UPDATE users
    SET balance = balance + ?
    WHERE id=?
    """,(tokens,user_id))

    cur.execute("""
    INSERT INTO transactions
    (user_id,description,tokens)
    VALUES (?,?,?)
    """,(user_id,f"{cat}: {title} approved",tokens))

    con.commit()
    con.close()

    return redirect(f"/admin/student/{user_id}")

app.run(debug=True,port=5001)