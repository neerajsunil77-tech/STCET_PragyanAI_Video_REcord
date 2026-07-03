import streamlit as st
import sqlite3
import pandas as pd

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    department TEXT,
    semester INTEGER,
    email TEXT,
    phone TEXT
)
""")
conn.commit()

# -------------------------------
# FUNCTIONS
# -------------------------------

def add_student(name, age, gender, department, semester, email, phone):
    cursor.execute("""
    INSERT INTO students
    (name, age, gender, department, semester, email, phone)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (name, age, gender, department, semester, email, phone))
    conn.commit()


def get_students():
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()


def update_student(id, name, age, gender, department, semester, email, phone):
    cursor.execute("""
    UPDATE students
    SET
    name=?,
    age=?,
    gender=?,
    department=?,
    semester=?,
    email=?,
    phone=?
    WHERE id=?
    """,
    (name, age, gender, department, semester, email, phone, id))
    conn.commit()


def delete_student(id):
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()


# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="Student Record Management",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Record Management System")

menu = [
    "Home",
    "Add Student",
    "View Students",
    "Update Student",
    "Delete Student"
]

choice = st.sidebar.selectbox("Navigation", menu)

# -------------------------------
# HOME
# -------------------------------

if choice == "Home":

    st.subheader("Dashboard")

    students = get_students()

    st.metric("Total Students", len(students))

    st.markdown("---")

    st.write("""
    ### Features

    - Add Student
    - View Students
    - Update Student
    - Delete Student
    - SQLite Database
    - Deployable on Streamlit Cloud
    """)

# -------------------------------
# ADD STUDENT
# -------------------------------

elif choice == "Add Student":

    st.subheader("Add New Student")

    with st.form("student_form"):

        name = st.text_input("Student Name")

        age = st.number_input(
            "Age",
            min_value=15,
            max_value=40,
            value=18
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        department = st.selectbox(
            "Department",
            [
                "Computer Science",
                "Mechanical",
                "Civil",
                "Electrical",
                "Electronics",
                "MBA"
            ]
        )

        semester = st.selectbox(
            "Semester",
            list(range(1, 9))
        )

        email = st.text_input("Email")

        phone = st.text_input("Phone")

        submitted = st.form_submit_button("Add Student")

        if submitted:

            add_student(
                name,
                age,
                gender,
                department,
                semester,
                email,
                phone
            )

            st.success("Student Added Successfully")

# -------------------------------
# VIEW STUDENTS
# -------------------------------

elif choice == "View Students":

    st.subheader("Student Records")

    students = get_students()

    if students:

        df = pd.DataFrame(
            students,
            columns=[
                "ID",
                "Name",
                "Age",
                "Gender",
                "Department",
                "Semester",
                "Email",
                "Phone"
            ]
        )

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False)

        st.download_button(
            "Download CSV",
            csv,
            "students.csv",
            "text/csv"
        )

    else:
        st.warning("No records found.")

# -------------------------------
# UPDATE
# -------------------------------

elif choice == "Update Student":

    st.subheader("Update Student")

    students = get_students()

    if students:

        ids = [student[0] for student in students]

        selected_id = st.selectbox(
            "Select Student ID",
            ids
        )

        student = None

        for s in students:
            if s[0] == selected_id:
                student = s
                break

        if student:

            name = st.text_input("Name", student[1])

            age = st.number_input(
                "Age",
                min_value=15,
                max_value=40,
                value=student[2]
            )

            gender = st.selectbox(
                "Gender",
                ["Male", "Female", "Other"],
                index=["Male","Female","Other"].index(student[3])
            )

            departments = [
                "Computer Science",
                "Mechanical",
                "Civil",
                "Electrical",
                "Electronics",
                "MBA"
            ]

            department = st.selectbox(
                "Department",
                departments,
                index=departments.index(student[4])
            )

            semester = st.selectbox(
                "Semester",
                list(range(1,9)),
                index=student[5]-1
            )

            email = st.text_input(
                "Email",
                student[6]
            )

            phone = st.text_input(
                "Phone",
                student[7]
            )

            if st.button("Update"):

                update_student(
                    selected_id,
                    name,
                    age,
                    gender,
                    department,
                    semester,
                    email,
                    phone
                )

                st.success("Student Updated Successfully")

    else:
        st.warning("No student records available.")

# -------------------------------
# DELETE
# -------------------------------

elif choice == "Delete Student":

    st.subheader("Delete Student")

    students = get_students()

    if students:

        df = pd.DataFrame(
            students,
            columns=[
                "ID",
                "Name",
                "Age",
                "Gender",
                "Department",
                "Semester",
                "Email",
                "Phone"
            ]
        )

        st.dataframe(df, use_container_width=True)

        ids = df["ID"].tolist()

        selected = st.selectbox(
            "Select Student ID",
            ids
        )

        if st.button("Delete Student"):

            delete_student(selected)

            st.success("Student Deleted Successfully")

    else:
        st.warning("No records found.")

# -------------------------------
# FOOTER
# -------------------------------

st.markdown("---")
st.caption("Student Record Management System using Streamlit + SQLite")
