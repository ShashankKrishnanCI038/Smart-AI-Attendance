import cx_Oracle
import datetime
import pandas as pd

dt = datetime.datetime.now()

user = 'system'
passw = 'manager'
connstr = 'system/manager@localhost:1521/xe'


conn = cx_Oracle.connect(connstr)
cur = conn.cursor()


#SQL QUERIES
try:
    cur.execute("""DROP TABLE Students CASCADE CONSTRAINTS""")
    cur.execute("""DROP TABLE Parents CASCADE CONSTRAINTS""")
    cur.execute("""DROP TABLE Faculty CASCADE CONSTRAINTS""")
    cur.execute("""DROP TABLE Subjects CASCADE CONSTRAINTS""")
    cur.execute("""DROP TABLE Status CASCADE CONSTRAINTS""")
    cur.execute("""DROP TABLE Dayz CASCADE CONSTRAINTS """)
    cur.execute("""DROP VIEW datanode """)
    cur.execute("""DROP VIEW absentees """)
    # cur.execute(""" CREATE TABLE students(
    #                         susn varchar(10) PRIMARY KEY,
    #                         sname varchar(20),
    #                         sphone int,
    #                         sdep varchar(5),
    #                         smail varchar(15)) """)
    #
    # cur.execute("""CREATE TABLE parents(
    #                         pphone int PRIMARY KEY,
    #                         pname varchar(20),
    #                         pmail varchar(20),
    #                         susn varchar(10),
    #                         FOREIGN KEY (susn) REFERENCES students(susn)) """)
    #
    # cur.execute("""CREATE TABLE faculty(
    #                         facid varchar(5),
    #                         fname varchar(20),
    #                         fphone int,
    #                         fdep varchar(5),
    #                         susn varchar(10),
    #                         FOREIGN KEY (susn) REFERENCES students(susn)) """)
    #
    # cur.execute("""CREATE TABLE subjects(
    #                         subcode varchar(7),
    #                         subname varchar(10),
    #                         susn varchar(10),
    #                         FOREIGN KEY (susn) REFERENCES students(susn)) """)
    #
    # cur.execute("""CREATE TABLE status(
    #                         statvalue varchar(10),
    #                         susn varchar(10),
    #                         FOREIGN KEY (susn) REFERENCES students(susn)) """)
    #
    # cur.execute("""CREATE TABLE dayz(
    #                         datez DATE,
    #                         timez varchar(16),
    #                         susn varchar(10),
    #                         FOREIGN KEY (susn) REFERENCES students(susn)) """)
    # ###################################################################################################################################
    # facid = str(input('Enter the Faculty ID: '))
    # fname = str(input('Enter the Faculty Name: '))
    # fphone = int(input('Enter the Phone Number: '))
    # fdep = str(input('Enter the department: '))
    # subname = str(input('Enter the Subject Name: '))
    # subcode = str(input('Enter the Subject Code: '))
    # susn = ['USN1', 'USN2', 'USN3', 'USN4', 'USN5', 'USN6', 'USN7', 'USN8']
    # sname = ['John', 'Belli', 'Mark', 'Jennifer', 'Dev', 'Akhilesh', 'Susantha', 'Shashank']
    # sphone = [9988774455, 9966772255, 9966553355, 9866553322, 9877553322, 9988552211, 9986652211, 9986652299]
    # smail = ['john@gmail.com', 'Belli@gmail.com', 'Mark@gmail.com', 'Jenni@gmail.com', 'Dev@gmail.com', 'Akhi@gmail.com', 'Sus@gmail.com', 'Shash@gmail.com']
    # for i in range(len(susn)):
    #     cur.execute("INSERT INTO students (susn, sname, sphone, sdep, smail) VALUES (:1, :2, :3, :4, :5)", (susn[i], sname[i], sphone[i], fdep, smail[i]))
    #
    # pphone = [9988554411, 9988556644, 6655889977, 8877445522, 8877441122, 7755441122, 5544555522, 7788994455]
    # pname = ['Albert', 'Joseph', 'marina', 'Leena', 'james', 'jayson', 'rubina', 'sameer']
    # pmail = ['alb@gmail.com', 'jos@gmail.com', 'maria@gmail.com', 'leen@gmail.com', 'jam@gmail.com', 'json@gmail.com', 'rubi@gmail.com', 'sma@gmail.com']
    # for i in range(len(susn)):
    #     cur.execute("INSERT INTO parents (pphone, pname, pmail, susn) VALUES (:1, :2, :3, :4)", (pphone[i], pname[i], pmail[i], susn[i]))
    #
    #
    # for i in range(len(susn)):
    #     cur.execute("INSERT INTO faculty (facid, fname, fphone, fdep, susn) VALUES (:1, :2, :3, :4, :5) ", (facid, fname, fphone, fdep, susn[i]))
    #
    # for i in range(len(susn)):
    #     cur.execute("INSERT INTO subjects (subcode, subname, susn) VALUES (:1, :2, :3) ", (subcode, subname, susn[i]))
    #
    # stats = 'Absent'
    # for i in range(len(susn)):
    #     cur.execute("INSERT INTO status (statvalue, susn) VALUES (:1, :2) ", (stats, susn[i]))
    #
    # datedata = dt.date()
    # time = dt.time()
    # for i in range(len(susn)):
    #     cur.execute("INSERT INTO dayz (datez, timez, susn) VALUES (:1, :2, :3) ", (datedata, str(time), susn[i]))
    # stud = 'USN8'
    # cur.execute("UPDATE status SET statvalue='Absent' WHERE susn='%s' " % (stud))
    # cur.execute(""" create view datanode as
    #                         select e.susn, a.sname, a.sphone, c.facid, c.fname, d.subname, d.subcode, f.datez, f.timez, e.statvalue
    #                             from students a, faculty c, subjects d, status e, dayz f
    #                                 where e.susn = a.susn
    #                                     and a.susn = c.susn
    #                                     and c.susn = d.susn
    #                                     and d.susn = f.susn """)
    #
    # cur.execute(""" create view absentees as
    #                     select a.susn, a.sname, a.sphone, b.pname, b.pphone, b.pmail, d.subname, f.datez, f.timez, e.statvalue
    #                         from students a, parents b, subjects d, dayz f, status e
    #                             where a.susn = b.susn
    #                                 and b.susn = d.susn
    #                                 and d.susn = f.susn
    #                                 and f.susn = e.susn
    #                                 and e.statvalue = 'Absent' """)

except ConnectionError as ee:
    print("DBMS ERROR")

conn.commit()
cur.close()
conn.close()



