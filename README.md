# MSMS - Music School Management System

FIT1056 Problem Solving Tasks (PST1-PST3): a Music School Management System
built up over three stages, each one a direct upgrade of the last.

## Project Structure

```
msms-project/
├── PST1/   The Foundation - simple in-memory prototype
├── PST2/   The Upgrade - file storage (JSON) and validation
└── PST3/   The Architecture - Object-Oriented redesign
```

Each folder is a self-contained stage - later stages build on the ideas of
the earlier ones, but don't depend on their code directly.

---

## PST1: The Foundation (`PST1/MSMS.py`)

A simple in-memory prototype. `Student` and `Teacher` are basic classes, but
all data lives in two global lists (`student_db`, `teacher_db`) that are
wiped every time the program exits - nothing is saved to a file yet.

**Features:** register a new student (and enrol them in an instrument),
enrol an existing student, look up students/teachers by name or speciality,
and list all students/teachers.

**How to run:**
```bash
cd PST1
python MSMS.py
```

---

## PST2: The Upgrade (`PST2/pst2_main.py`)

Adds persistence: all data (students, teachers, attendance) is now stored
in one dictionary (`app_data`) and saved to/loaded from `msms.json`, so
data survives between runs. Students and teachers are still plain
dictionaries at this stage, not objects.

**Features:** everything from PST1, plus check-in/attendance tracking,
printing a student ID card to a text file, and updating/removing
students and teachers.

**How to run:**
```bash
cd PST2
python pst2_main.py
```

---

## PST3: The Architecture (Object-Oriented Redesign)

The main focus of this submission. PST2's single procedural file is
refactored into a proper layered structure:

```
PST3/
├── main.py            The View - handles all user interaction/menus
├── app/
│   ├── user.py          User base class (id, name)
│   ├── student.py        StudentUser(User)
│   ├── teacher.py        TeacherUser(User) and Course
│   └── schedule.py        ScheduleManager - the Controller
└── data/
    └── msms.json           Persisted data
```

- **Model** (`app/user.py`, `app/student.py`, `app/teacher.py`) - the core
  entities as real classes. `StudentUser` and `TeacherUser` both inherit
  from `User`. `Course` holds a list of enrolled student IDs and a list of
  lessons (each a `{day, start_time, room}` dictionary).
- **Controller** (`app/schedule.py`) - `ScheduleManager` is the single
  "brain" of the app. It loads `data/msms.json` and turns the raw
  dictionaries into real `StudentUser`/`TeacherUser`/`Course` objects,
  holds all the business logic (check-in, switching courses, etc.), and
  saves everything back to JSON after every change.
- **View** (`main.py`) - only talks to `ScheduleManager` (referred to as
  `manager`). It never touches the JSON file or object internals directly
  - it calls a method, then formats and prints whatever comes back.

### How to run

`main.py` loads data using the relative path `data/msms.json`, so it must
be run from inside `PST3/`:

```bash
cd PST3
python main.py
```

### Menu

```
1.  View daily roster           - shows every lesson scheduled on a given day
2.  Check in student            - records attendance for a student/course
3.  Switch student's course     - moves a student from one course to another
4.  List students
5.  List teachers
6.  List courses
7.  Add student                 } ported from PST2's add_student/add_teacher,
8.  Add teacher                 } rebuilt to create real objects instead of dicts
9.  Remove student               } ported from PST2's remove_student/remove_teacher
10. Remove teacher                }
11. Update student name           } ported from PST2's update_student/update_teacher
12. Update teacher info            }
13. Add course                   - same add/next-id pattern as add_student/add_teacher
14. List students in a course    - looks up every student enrolled in one course
15. Print student card           - writes a text file badge, same as PST2's version
q.  Quit
```

Options 1-6 are the core PST3 requirements. Options 7-15 go beyond the
brief, porting PST2's student/teacher management features into the new
object-oriented structure.

### Design choices and assumptions

- **`StudentUser` doesn't store an instrument.** Only `Course` does. A
  student's instrument is implied by which course(s) they're enrolled in,
  so it isn't duplicated on the student object.
- **All IDs (students, teachers, courses) are plain integers**, assigned
  from counters (`next_student_id`, etc.) stored in `data/msms.json` so
  they stay unique across restarts.
- **A lesson is a dictionary** with `lesson_id`, `day`, `start_time`, and
  `room` - a course can have any number of lessons per week.
- **Every method that changes data saves immediately** (`self._save_data()`
  at the end of `check_in`, `switch_student_course`, `add_student`, etc.)
  rather than batching saves, so the JSON file is always up to date.
- **No cross-reference validation on delete** - removing a teacher who
  still teaches a course, or a student who's still enrolled somewhere,
  isn't blocked or cleaned up automatically. This matches PST2's original
  behaviour (which had the same gap) and is a known limitation rather
  than an oversight.

### How to test

Run `python main.py` from inside `PST3/` and work through the menu, e.g.:
1. `4` / `5` / `6` to confirm the seed data (from `data/msms.json`) loads
   correctly as students, teachers, and courses.
2. `1`, entering `Monday`, to see the daily roster pull real lesson data.
3. `2` to check a student into a course, then `4` to confirm their record
   is unchanged (attendance is tracked separately) and check
   `data/msms.json` to see the new attendance record was saved.
4. `3` to switch a student between courses, then `6` to confirm both
   courses' enrolment lists updated.
5. `7`/`8`/`13` to add a student, teacher, and course, then `14` to list
   who's enrolled in a course.
