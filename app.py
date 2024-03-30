import tkinter as tk
import customtkinter
from PIL import Image, ImageTk
import cv2
import cx_Oracle
import datetime
import os
from tkinter import messagebox
import pyttsx3
import keyboard
from deepface import DeepFace
import pandas as pd

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.title('Smart AI Attendance System')
root.geometry('1920x1080')
text1 = customtkinter.StringVar()
text2 = customtkinter.StringVar()
text3 = customtkinter.StringVar()
text4 = customtkinter.StringVar()
text5 = customtkinter.StringVar()
text6 = customtkinter.StringVar()
dt = datetime.datetime.now()


#################################################################################################################################################################################

def dbcreate():
    subname = text1.get()
    subcode = text2.get()
    fname = text3.get()
    fphone = text4.get()
    fdep = text5.get()
    facid = text6.get()
    datedata = dt.date()
    time = dt.time()
    stats = 'Absent'

    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 130)

    connstr = 'system/manager@localhost:1521/xe'
    conn = cx_Oracle.connect(connstr)
    cur = conn.cursor()

    engine.say("Database Connected Succesfully")
    engine.runAndWait()

    # SQL QUERIES
    try:
        cur.execute(""" CREATE TABLE students(
                        susn varchar(10) PRIMARY KEY,
                        sname varchar(20),
                        sphone int,
                        sdep varchar(5),
                        smail varchar(15)) """)

        cur.execute("""CREATE TABLE parents(
                        pphone int PRIMARY KEY,
                        pname varchar(20),
                        pmail varchar(20),
                        susn varchar(10),
                        FOREIGN KEY (susn) REFERENCES students(susn)) """)

        cur.execute("""CREATE TABLE faculty(
                        facid varchar(5) PRIMARY KEY,
                        fname varchar(20),
                        fphone int,
                        fdep varchar(5),
                        susn varchar(10),
                        FOREIGN KEY (susn) REFERENCES students(susn)) """)

        cur.execute("""CREATE TABLE subjects(
                        subcode varchar(7) PRIMARY KEY,
                        subname varchar(10),
                        susn varchar(10),
                        FOREIGN KEY (susn) REFERENCES students(susn)) """)

        cur.execute("""CREATE TABLE status(
                        statvalue varchar(10),
                        susn varchar(10),
                        FOREIGN KEY (susn) REFERENCES students(susn)) """)

        cur.execute("""CREATE TABLE dayz(
                        datez DATE,
                        timez varchar(10),
                        susn varchar(10),
                        FOREIGN KEY (susn) REFERENCES students(susn)) """)

        #insert value query
        susn = ['USN1', 'USN2', 'USN3', 'USN4', 'USN5', 'USN6', 'USN7', 'USN8']
        sname = ['John', 'Belli', 'Mark', 'Jennifer', 'Dev', 'Akhilesh', 'Susantha', 'Shashank']
        sphone = [9988774455, 9966772255, 9966553355, 9866553322, 9877553322, 9988552211, 9986652211, 9986652299]
        smail = ['john@gmail.com', 'Belli@gmail.com', 'Mark@gmail.com', 'Jenni@gmail.com', 'Dev@gmail.com',
                 'Akhi@gmail.com', 'Sus@gmail.com', 'Shash@gmail.com']
        for i in range(len(susn)):
            cur.execute("INSERT INTO students (susn, sname, sphone, sdep, smail) VALUES (:1, :2, :3, :4, :5)",
                        (susn[i], sname[i], sphone[i], fdep, smail[i]))

        pphone = [9988554411, 9988556644, 6655889977, 8877445522, 8877441122, 7755441122, 5544555522, 7788994455]
        pname = ['Albert', 'Joseph', 'marina', 'Leena', 'james', 'jayson', 'rubina', 'sameer']
        pmail = ['alb@gmail.com', 'jos@gmail.com', 'maria@gmail.com', 'leen@gmail.com', 'jam@gmail.com',
                 'json@gmail.com', 'rubi@gmail.com', 'sma@gmail.com']
        for i in range(len(susn)):
            cur.execute("INSERT INTO parents (pphone, pname, pmail, susn) VALUES (:1, :2, :3, :4)",
                        (pphone[i], pname[i], pmail[i], susn[i]))

        for i in range(len(susn)):
            cur.execute("INSERT INTO faculty (facid, fname, fphone, fdep, susn) VALUES (:1, :2, :3, :4, :5) ",
                        (facid, fname, fphone, fdep, susn[i]))

        for i in range(len(susn)):
            cur.execute("INSERT INTO subjects (subcode, subname, susn) VALUES (:1, :2, :3) ",
                        (subcode, subname, susn[i]))

        for i in range(len(susn)):
            cur.execute("INSERT INTO status (statvalue, susn) VALUES (:1, :2) ", (stats, susn[i]))

        for i in range(len(susn)):
            cur.execute("INSERT INTO dayz (datez, timez, susn) VALUES (:1, :2, :3) ", (datedata, str(time), susn[i]))

        engine.say("Database Tables Created")
        engine.runAndWait()
        messagebox.showinfo(message="Database Tables Created")

    except ConnectionError as ee:
        messagebox.showinfo(message="DBMS ERROR")
    camopen()


def camopen():
    # define a video capture object
    vid = cv2.VideoCapture(0)

    destpath = r"C:\Users\SHASHANK K\Pictures\example"

    try:
        while True:
            if keyboard.is_pressed('z'):
                exit()
            if keyboard.is_pressed('o'):
                while True:
                    # Capture the video frame
                    # by frame
                    ret, frame = vid.read()

                    # Display the resulting frame
                    cv2.imshow('frame', frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    if keyboard.is_pressed('p'):
                        cv2.imwrite(r"C:\Users\SHASHANK K\Pictures\Camera Roll\Student.png", frame)
                        try:
                            for img in os.listdir(destpath):
                                stud = img.split('.')[0]
                                photo = cv2.imread(os.path.join(destpath, img))
                                result = DeepFace.verify(
                                    img1_path=r"C:\Users\SHASHANK K\Pictures\Camera Roll\Student.png", img2_path=photo)
                                if result['verified']:
                                    print(stud)
                                    cur.execute("UPDATE status SET statvalue = 'Present' WHERE susn = '%s' " % (stud))
                        except KeyboardInterrupt as ee:
                            pass

                # Destroy all the windows
                cv2.destroyAllWindows()

    except KeyboardInterrupt as error:
        pass

    cur.execute(""" create view datanode as
                        select e.susn, a.sname, a.sphone, c.facid, c.fname, d.subname, d.subcode, f.datez, f.timez, e.statvalue
                            from students a, faculty c, subjects d, status e, dayz f
                                where e.susn = a.susn
                                    and a.susn = c.susn
                                    and c.susn = d.susn
                                    and d.susn = f.susn """)

    cur.execute(""" create view absentees as
                    select a.susn, a.sname, a.sphone, b.pname, b.pphone, b.pmail, d.subname, f.datez, f.timez, e.statvalue
                        from students a, parents b, subjects d, dayz f, status e
                            where a.susn = b.susn
                                and b.susn = d.susn
                                and d.susn = f.susn
                                and f.susn = e.susn
                                and e.statvalue = 'Absent' """)

def dbclose():
    connstr = 'system/manager@localhost:1521/xe'
    conn = cx_Oracle.connect(connstr)
    cur = conn.cursor()

    view1 = pd.read_sql_query(" select * from datanode ", conn)
    view1.to_csv(r"C:\Users\SHASHANK K\Desktop\Total_Data.csv", index=False)

    view2 = pd.read_sql_query("select * from absentees", conn)
    view2.to_csv(r"C:\Users\SHASHANK K\Desktop\Absentees.csv", index=False)

    #fetch the Absentees_Data.csv file extract parent email and send them the mail who are absent

    try:
        cur.execute("""DROP TABLE Students CASCADE CONSTRAINTS""")
        cur.execute("""DROP TABLE Parents CASCADE CONSTRAINTS""")
        cur.execute("""DROP TABLE Faculty CASCADE CONSTRAINTS""")
        cur.execute("""DROP TABLE Subjects CASCADE CONSTRAINTS""")
        cur.execute("""DROP TABLE Status CASCADE CONSTRAINTS""")
        cur.execute("""DROP TABLE Dayz CASCADE CONSTRAINTS """)
        cur.execute("""DROP VIEW datanode """)
        cur.execute("""DROP VIEW absentees """)

        cur.close()
        conn.close()
    except cx_Oracle.DatabaseError as dbe:
        messagebox.showerror(message="Error in Database Connection")

    engine.say("Database Disconnected Succesfully")
    engine.runAndWait()
    messagebox.showinfo(message="Database Disconnected")
    exit()


#################################################################################################################################################################################
frame = customtkinter.CTkFrame(master=root, height=350, width=600).pack()

photo = Image.open('img.jpg')
photo = ImageTk.PhotoImage(photo)
bgimg = customtkinter.CTkLabel(master=frame, image=photo, text=None).place(x=1, y=1)

label1 = customtkinter.CTkLabel(master=bgimg, height=32, width=60, text="Smart AI Attendance System",
                                font=("Cambria", 40), bg_color="#00007A", text_color="#FFFFFF").place(x=70, y=200)

entry1 = customtkinter.CTkEntry(master=bgimg, height=30, width=300, placeholder_text="Enter the Subject Name",
                                textvariable=text1, corner_radius=10, bg_color="#00007A", font=("Cambria", 20)).place(
    x=850, y=300)
entry2 = customtkinter.CTkEntry(master=bgimg, height=30, width=300, placeholder_text="Enter the Subject Code",
                                textvariable=text2, corner_radius=10, bg_color="#00007A", font=("Cambria", 20)).place(
    x=850, y=350)

entry3 = customtkinter.CTkEntry(master=bgimg, height=30, width=300, placeholder_text="Enter the Faculty Name",
                                textvariable=text3, corner_radius=10, bg_color="#00007A", font=("Cambria", 20)).place(
    x=850, y=400)
entry4 = customtkinter.CTkEntry(master=bgimg, height=30, width=300, placeholder_text="Enter the Faculty Phone",
                                textvariable=text4, corner_radius=10, bg_color="#00007A", font=("Cambria", 20)).place(
    x=850, y=450)
entry5 = customtkinter.CTkEntry(master=bgimg, height=30, width=300, placeholder_text="Enter the Faculty Department",
                                textvariable=text5, corner_radius=10, bg_color="#00007A", font=("Cambria", 20)).place(
    x=850, y=500)
entry6 = customtkinter.CTkEntry(master=bgimg, height=30, width=300, placeholder_text="Enter the Faculty ID",
                                textvariable=text6, corner_radius=10, bg_color="#00007A", font=("Cambria", 20)).place(
    x=850, y=550)

button1 = customtkinter.CTkButton(master=bgimg, command=dbcreate, height=15, width=20, fg_color="#00FFFF",
                                  text="Start Attendance", text_color="#000000", font=("Cambria", 20),
                                  bg_color="#0000FF", corner_radius=10, hover_color="#FFFFFF").place(x=100, y=500)
button2 = customtkinter.CTkButton(master=bgimg, command=dbclose, height=15, width=20, fg_color="#00FFFF", text="Stop Attendance",
                                  text_color="#000000", font=("Cambria", 20), bg_color="#0000FF", corner_radius=10,
                                  hover_color="#FFFFFF").place(x=300, y=500)
#################################################################################################################################################################################

root.mainloop()
