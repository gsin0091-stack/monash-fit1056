import json
import datetime

from app.student import StudentUser
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        # TODO: Initialize the new attendance_log attribute as an empty list.
        self.attendance_log = []
        # ... (next_id counters) ...
        self.next_student_id = 1
        self.next_teacher_id = 1
        self.next_course_id = 1
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                # TODO: Load students, teachers, and courses as before.
                # ...
                # go through each student dictionary and turn it into a real StudentUser
                self.students = []
                for s in data.get('students', []):
                    student = StudentUser(s['id'], s['name'])
                    student.enrolled_course_ids = s.get('enrolled_course_ids', [])
                    self.students.append(student)

                # same idea for teachers
                self.teachers = []
                for t in data.get('teachers', []):
                    teacher = TeacherUser(t['id'], t['name'], t['speciality'])
                    self.teachers.append(teacher)

                # and for courses - the constructor only takes the basic info,
                # so the enrolled students and lessons get added on after
                self.courses = []
                for c in data.get('courses', []):
                    course = Course(c['id'], c['name'], c['instrument'], c['teacher_id'])
                    course.enrolled_student_ids = c.get('enrolled_student_ids', [])
                    course.lessons = c.get('lessons', [])
                    self.courses.append(course)

                # TODO: Correctly load the attendance log.
                # Use .get() with a default empty list to prevent errors if the key doesn't exist.
                self.attendance_log = data.get("attendance", [])
                self.next_student_id = data.get("next_student_id", 1)
                self.next_teacher_id = data.get("next_teacher_id", 1)
                self.next_course_id = data.get("next_course_id", 1)
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")

    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        # TODO: Create a 'data_to_save' dictionary.
        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            # TODO: Add the attendance_log to the dictionary to be saved.
            # Since it's already a list of dicts, no conversion is needed.
            "attendance": self.attendance_log,
            # ... (next_id counters) ...
            "next_student_id": self.next_student_id,
            "next_teacher_id": self.next_teacher_id,
            "next_course_id": self.next_course_id,
        }
        # TODO: Write 'data_to_save' to the JSON file.
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def check_in(self, student_id, course_id):
        """Records a student's attendance for a course after validation."""
        # This implementation remains the same, but it will now function correctly.
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)

        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False

        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {"student_id": student_id, "course_id": course_id, "timestamp": timestamp}

        # This line will now work without causing an AttributeError.
        self.attendance_log.append(check_in_record)
        self._save_data() # This will now correctly save the attendance log.
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True

    # TODO: Also implement find_student_by_id and find_course_by_id helper methods.
    def find_student_by_id(self, student_id):
        # go through every student and return the one with a matching id
        for student in self.students:
            if student.id == student_id:
                return student
        return None  # nobody had that id

    def find_course_by_id(self, course_id):
        for course in self.courses:
            if course.id == course_id:
                return course
        return None

    def find_teacher_by_id(self, teacher_id):
        # same pattern as above, just for teachers
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                return teacher
        return None

    def get_lessons_for_day(self, day):
        """Returns a list of dictionaries, each holding a course and one of its lessons, for the given day."""
        day = day.strip().lower()  # so "monday" and "Monday" both match
        results = []
        # check every lesson of every course, keep the ones on the right day
        for course in self.courses:
            for lesson in course.lessons:
                if lesson.get("day", "").lower() == day:
                    results.append({"course": course, "lesson": lesson})
        return results

    def switch_student_course(self, student_id, from_course_id, to_course_id):
        """Moves a student's enrollment from one course to another."""
        student = self.find_student_by_id(student_id)
        from_course = self.find_course_by_id(from_course_id)
        to_course = self.find_course_by_id(to_course_id)

        if not student or not from_course or not to_course:
            print("Error: Switch failed. Invalid student or course ID.")
            return False

        # can't switch out of a course the student was never in
        if student_id not in from_course.enrolled_student_ids:
            print(f"Error: Student {student_id} is not enrolled in course {from_course_id}.")
            return False

        # remove from the old course's list, add to the new course's list
        from_course.enrolled_student_ids.remove(student_id)
        to_course.enrolled_student_ids.append(student_id)

        # do the same update on the student's own side so both match
        if from_course_id in student.enrolled_course_ids:
            student.enrolled_course_ids.remove(from_course_id)
        student.enrolled_course_ids.append(to_course_id)

        self._save_data()
        print(f"Success: {student.name} switched from {from_course.name} to {to_course.name}.")
        return True

    def add_student(self, name):
        """Adds a student dictionary to the data store."""
        # use the current counter as the new id, then bump it up for next time
        student = StudentUser(self.next_student_id, name)
        self.students.append(student)
        self.next_student_id += 1
        self._save_data()
        print(f"Core: Student '{name}' added with ID {student.id}.")

    def add_teacher(self, name, speciality):
        """Adds a teacher dictionary to the data store."""
        teacher = TeacherUser(self.next_teacher_id, name, speciality)
        self.teachers.append(teacher)
        self.next_teacher_id += 1
        self._save_data()
        print(f"Core: Teacher '{name}' added.")

    def remove_student(self, student_id):
        """Removes a student from the data store."""
        student = self.find_student_by_id(student_id)
        if not student:
            print(f"Error: Student with ID {student_id} not found.")
            return False
        # .remove() takes the object itself out of the list
        self.students.remove(student)
        self._save_data()
        print(f"Student {student_id} removed.")
        return True

    def remove_teacher(self, teacher_id):
        """Removes a teacher from the data store."""
        teacher = self.find_teacher_by_id(teacher_id)
        if not teacher:
            print(f"Error: Teacher with ID {teacher_id} not found.")
            return False
        self.teachers.remove(teacher)
        self._save_data()
        print(f"Teacher {teacher_id} removed.")
        return True

    def update_student(self, student_id, name=None):
        """Finds a student by ID and updates their name if a new one is given."""
        student = self.find_student_by_id(student_id)
        if not student:
            print(f"Error: Student with ID {student_id} not found.")
            return False
        # only change the name if the caller actually gave us a new one
        if name:
            student.name = name
        self._save_data()
        print(f"Student {student_id} updated.")
        return True

    def update_teacher(self, teacher_id, name=None, speciality=None):
        """Finds a teacher by ID and updates their info if new values are given."""
        teacher = self.find_teacher_by_id(teacher_id)
        if not teacher:
            print(f"Error: Teacher with ID {teacher_id} not found.")
            return False
        if name:
            teacher.name = name
        if speciality:
            teacher.speciality = speciality
        self._save_data()
        print(f"Teacher {teacher_id} updated.")
        return True

    def add_course(self, name, instrument, teacher_id):
        """Adds a new course to the data store."""
        # same idea as add_student/add_teacher, just for courses
        course = Course(self.next_course_id, name, instrument, teacher_id)
        self.courses.append(course)
        self.next_course_id += 1
        self._save_data()
        print(f"Course '{name}' added with ID {course.id}.")
        return course
