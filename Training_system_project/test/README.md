---

Student Course Management System

By: Shahinda Ibrahim Ahmed


---

Table of Contents

1. Introduction
2. Why I Built This System
3. System Overview
4. Core Concepts & Structure
5. Class Descriptions and Functions
6. How to Run the System
7. Important Notes & Edge Cases
8. Future Improvements
9. Final Words

---

Introduction

This is a fully object-oriented student-course management system designed and implemented from scratch in Python. It simulates how a real academic institution manages students, courses, grades, and enrollment, using clean code, separation of concerns, and modular design.

Whether you're a beginner or a professional, this system showcases the power of OOP (Object-Oriented Programming) using real-world entities and logic.

---

Why I Built This System

The primary goal of building this system was to:

Apply object-oriented concepts in a realistic academic context.
Learn how to design scalable and maintainable code.
Build a strong foundation in class design, relationships, and data handling.
Challenge myself to create a terminal-based "GUI" experience for the user.
Go beyond standard assignments and impress instructors by showing full ownership of the logic and implementation.

---

System Overview

The system allows a user to:

Add or remove students and courses.
Enroll students into courses.
Record grades.
Search for courses.
List all students and courses.
Display all recorded data via a simple command-line interface.

The system is divided into 3 main components:

1. Student class – represents the student object.
2. Course class – represents a course.
3. SystemManager class – the core engine that links everything together.


---

Core Concepts & Structure

This system follows best practices in OOP:

Encapsulation: Every entity (student, course) has its own logic and attributes.
Modular Design: Functions are split into dedicated modules.
Separation of Concerns: The CLI logic is separated from the data logic.
ID generation: Each student and course gets a unique, auto-incremented ID.
User Input Validations (and will be expanded in future improvements).


Folder structure:

project/
│
├── core/
│   └── system_manager.py
│
│__ model/
│   ├── student.py
│   ├── course.py
│
├── test/
│   └── README.md      # (This file)
│
└── main.py    # Entry point

---

Class Descriptions and Functions

---

Student Class

File: model/student.py

This class models a student object. It stores:
The student’s name.
A unique student_id (auto-incremented).
A dictionary of grades {course_id: grade}.
A list of enrolled course IDs.


Key Methods:

def init(self, name)
Initializes a new student with a unique ID and stores their name.

def add_grade(self, course_id, grade)
Records or updates a student's grade for a specific course.

def enrolled_in_course(self, course)
Adds a course to the student's list of enrolled courses.

def str() and repr()
Represent student details as readable text when printed.

---

Course Class

File: model/course.py
Represents a single course in the system.
Contains a unique course_id.
Name of the course.
List of enrolled students.

Key Methods:

def init(self, name)
Assigns a unique ID and stores the course name.

def enroll_student(self, student)
Adds a student to the course (only if not already enrolled).

def remove_student(self, student)
Removes a student from this course (currently under refinement).

def str()
Prints a readable representation of the course and number of enrolled students.

---

SystemManager Class

File: core/system_manager.py

This is the brain of the application. It handles all data operations and coordinates between students and courses.

Attributes:

self.students: a dictionary of students {student_id: student}
self.courses: a dictionary of courses {course_id: course}

Key Functions:

def add_student(self, name)
Creates and stores a new student.

def remove_student(self, student_id)
Removes a student only if they are not enrolled in any course.

def add_course(self, name)
Creates and stores a new course.

def enroll_course(self, student_id, course_id)
Enrolls a student in a course if both exist and not already enrolled.

def record_grade(self, student_id, course_id, grade)
Records the student's grade for a course.

def get_all_students() / get_all_courses()
Returns a list of all student/course objects for display.

---

CLI Menu Interface

File: main.py

A simple terminal-based UI that makes it easy to interact with the system. It displays a menu of options and calls the appropriate functions.

Main commands:
Add/remove students or courses
Enroll students
Record grades
Search courses
View all data
Exit

if name == "main":
    core()
This ensures the interface only runs when the file is executed directly.

---

How to Run the System

Requirements

Python 
Terminal / CMD / VSCode / PyCharm

Steps
1. Clone the repo or download the files.
2. Make sure the structure is like:

project/
├── core/
│__model/
│__ test/
└── main.py

3. Navigate to the interface folder.
4. Run:
python main.py

5. Start using the system through the menu

---

Important Notes & Edge Cases

Integer Inputs: Always input valid integers for student/course IDs.
Grades: Must be valid numbers (preferably float).
Unique Enrollments: A student cannot be enrolled in the same course twice.
Student Removal: Students cannot be deleted if enrolled in courses.

---

Future Improvements

To make the system even better:

Add file saving (json/csv) for student/course data.
Build a GUI with Tkinter or PyQt.
Add input validation with exception handling.
Add average grade calculator per student.
Create unit tests for each function.
Search students by name or ID.

---

Final Words

This project was built with care, clarity, and code quality in mind. Every function, class, and structure was chosen to reflect real-world thinking and logical architecture, not just code that "works".
I didn’t just write this to pass a task – I built it to showcase my skills, challenge myself, and create something I’m genuinely proud of.
Hope you enjoy using it as much as I enjoyed building it

— Shahinda

---
