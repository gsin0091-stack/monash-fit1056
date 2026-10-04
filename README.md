# MSMS - Music School Management System

FIT1056 Problem Solving Tasks (PST1-PST4): a Music School Management System
built up over four stages, each one a direct upgrade of the last.

## Project Structure

```
msms-project/
├── PST1/   The Foundation - simple in-memory prototype
├── PST2/   The Upgrade - file storage (JSON) and validation
├── PST3/   The Architecture - Object-Oriented redesign
└── PST4/   The User Interface - Streamlit GUI on top of PST3
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
```
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
```
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

```
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
7.  Add student                 } from PST2's add_student/add_teacher,
8.  Add teacher                 } rebuilt to create real objects instead of dicts
9.  Remove student               } from PST2's remove_student/remove_teacher
10. Remove teacher                }
11. Update student name           } from PST2's update_student/update_teacher
12. Update teacher info            }
13. Add course                   - same add/next-id pattern as add_student/add_teacher
14. List students in a course    - looks up every student enrolled in one course
15. Print student card           - writes a text file badge, same as PST2's version
16. Enrol student in course      - enrols a student in a course for the first time
q.  Quit
```

Options 1-6 are the core PST3 requirements. Options 7-16 go beyond the
brief, taking PST2's student/teacher management features into the new
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
- **Removing a student cleans up after them, removing a teacher doesn't.**
  `remove_student` strips the student's ID out of every course's
  `enrolled_student_ids` before deleting them.
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
5. `7`/`8`/`13` to add a student, teacher, and course, then `16` to enrol
   the new student in a course, and `14` to confirm they show up as
   enrolled.
6. `9` to remove a student who's enrolled in a course, then `6` to
   confirm they're gone from that course's enrolled list too.

---

## PST4: The User Interface (Streamlit GUI)

Replaces the text console with a web-based GUI, using
[Streamlit](https://streamlit.io/) (pure Python, no HTML/CSS/JS needed).
`PST4/app/` is carried forward from the completed PST3 (`ScheduleManager`
and the Model classes aren't rebuilt - the GUI just calls the same
methods), plus two new methods the GUI needed: `register_new_student`
(for the registration form) and `find_students_by_name` (for search).

```
PST4/
├── main.py                 2 lines: imports and calls gui.main_dashboard.launch()
├── app/                     carried forward from PST3 (+ register_new_student, find_students_by_name)
│   ├── user.py
│   ├── student.py
│   ├── teacher.py
│   └── schedule.py
├── gui/
│   ├── main_dashboard.py    entry point: page config, sidebar nav, session-state manager
│   ├── student_pages.py     Student Management page (search, register, add, add to course, remove)
│   └── roster_pages.py      Daily Roster page (view + check-in form)
└── data/
    └── msms.json             persisted data (separate copy from PST3's)
```

- **`gui/main_dashboard.py`'s `launch()`** sets up the page, then does the
  one thing that matters most in Streamlit: `if 'manager' not in
  st.session_state: st.session_state.manager = ScheduleManager()`.
  Streamlit reruns the *entire* script top-to-bottom on every click, so
  without this check a new `ScheduleManager` (and a fresh reload of the
  JSON file) would be created on every single interaction, wiping out
  anything not yet saved. `st.session_state` is Streamlit's way of
  keeping one object alive across reruns - the manager is created once,
  the first time the app loads, and reused after that.
- **`gui/student_pages.py`** renders the Student Management page. The
  registration form (from the template) calls
  `manager.register_new_student(name, instrument)` - a new method, not
  from PST3 (see below). **Find a Student**, which was a stub in the
  template, is filled in: type part of a name and the matching students
  appear, using the new `find_students_by_name` method. Three more forms
  reuse PST3's manager methods: **Add Student** (`add_student`),
  **Add Student to Course** (`enroll_student`, built the same way as the
  template's check-in form) and **Remove Student** (`remove_student`, with
  a confirmation tick box). Their dropdowns show `id - name` so two
  students with the same name can be told apart.
- **`gui/roster_pages.py`** has two parts: a day picker that displays that
  day's lessons in a table (built from PST3's `get_lessons_for_day`,
  rendered with `st.dataframe`), and a check-in form with dropdowns
  populated from `manager.students`/`manager.courses`, calling PST3's
  existing `manager.check_in(student_id, course_id)`.

### How to run

Needs `streamlit` and `pandas` installed (`pip install streamlit pandas`).
Like PST3, it loads `data/msms.json` using a path relative to wherever
it's launched from, so run it from inside `PST4/`:

```
cd PST4
streamlit run main.py
```

This starts a local web server and opens the app in your browser
(normally at `http://localhost:8501`).

### `register_new_student` - a method not given in any PST3 template

The GUI's registration form calls `manager.register_new_student(name,
instrument)`, expecting it to return the new student on success, or
`None`/falsy if "a teacher for that instrument might not be available."
This method doesn't exist anywhere in PST1-PST3 - it had to be designed
from scratch to match what the GUI expects:

```python
def register_new_student(self, name, instrument):
    # look for a course that already teaches this instrument
    matching_course = None
    for course in self.courses:
        if course.instrument.strip().lower() == instrument.strip().lower():
            matching_course = course
            break
    if not matching_course:
        return None   # nothing created - no half-registered student left behind
    student = StudentUser(self.next_student_id, name)
    ...
    return student
```

The key design decision: the instrument check happens **before** creating
the student, not after. If no course teaches that instrument, the method
returns `None` immediately without touching `self.students` at all - so a
failed registration never leaves a "ghost" student sitting in the data
with nowhere to be enrolled.

### Design choices and assumptions

- **The PST3 `app/` folder is reused, not rewritten.** The spec says to
  build on "the `ScheduleManager` you perfected in PST3" - the GUI is a
  new layer on top, not a redo of the business logic.
- **`register_new_student` matches by course instrument, not teacher
  directly**, even though the GUI's error message mentions "a teacher."
  Since every `Course` requires a `teacher_id`, "a course exists for this
  instrument" and "a teacher is available for this instrument" are
  effectively the same check here - there's no course without a teacher.
- **PST4 has its own copy of `data/msms.json`**, separate from PST3's.
  Running PST4 does not affect your PST3 data or vice versa.
- **"Find a Student" was a stub in the given template** (just a heading
  and `# ...`). The brief only requires the registration form, but the
  search was filled in so the page isn't left with an empty section.
  "Payments (stub)" is left as the template has it - explicitly deferred
  to PST5.
- **The search results are drawn last.** Streamlit draws the page top to
  bottom, so a table drawn above the registration form would not show a
  student registered a moment later. A `st.container()` reserves the spot
  under the search box and is filled in after the form has run.
- **The GUI files follow the given templates closely.** The template code
  and comments are kept as they were, with additions only where the
  template left a gap (the roster table and the search).

### How to test

Run `streamlit run main.py` from inside `PST4/`, then in the browser:
1. On **Student Management**, register a student with an instrument that
   has a matching course (e.g. "Piano") - should show a success message.
2. Try registering with an instrument that has no course (e.g. "Drums")
   - should show an error and *not* create a student (check
   `data/msms.json` to confirm `next_student_id` didn't advance).
3. Switch to **Daily Roster**, pick a day with lessons (e.g. Monday) -
   confirm the table shows the right course/teacher/room.
4. Use the check-in form to check a student into a course they're
   enrolled in - confirm the success message and that `data/msms.json`
   gained a new attendance record.
5. On **Student Management**, type part of a name into "Search by name"
   - matching students (and their course IDs) should appear below it.
6. With a name still in the search box, register a student with that name
   - the search results should update to include them.
7. Use **Add Student**, then **Add Student to Course** to put them in a
   course, then **Remove Student** (tick the box) and confirm they are gone
   from the search and from that course in `data/msms.json`.
