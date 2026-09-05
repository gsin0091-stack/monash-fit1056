# main.py - The View Layer
from app.schedule import ScheduleManager

def front_desk_daily_roster(manager, day):
    """Displays a pretty table of all lessons on a given day."""
    print(f"\n--- Daily Roster for {day} ---")
    # Notice: This code does not need to change. It doesn't care where the Course class lives.
    # It only talks to the manager.
    # TODO: Call a method on the manager to get the day's lessons and print them.
    lessons = manager.get_lessons_for_day(day)
    if not lessons:
        print("No lessons scheduled.")
        return
    # each entry has a course and one of its lessons, print them together
    for entry in lessons:
        course = entry["course"]
        lesson = entry["lesson"]
        teacher = manager.find_teacher_by_id(course.teacher_id)
        if teacher:
            teacher_name = teacher.name
        else:
            teacher_name = "Unknown"  # just in case the teacher_id doesn't match anyone
        print(f"  {lesson.get('start_time', '?')} - {course.name} ({course.instrument}) with {teacher_name} in {lesson.get('room', '?')}")

def switch_course(manager, student_id, from_course_id, to_course_id):
    # TODO: Implement the logic to switch a student by calling methods on the manager.
    # the manager does all the actual work, this just passes the details along
    manager.switch_student_course(student_id, from_course_id, to_course_id)

def check_in_student(manager, student_id, course_id):
    # named differently from manager.check_in so the two don't get confused
    manager.check_in(student_id, course_id)

def list_students(manager):
    print("\n--- Student List ---")
    if not manager.students:
        print("No students in the system.")
        return
    for s in manager.students:
        print(f"  ID: {s.id}, Name: {s.name}, Courses: {s.enrolled_course_ids}")

def list_teachers(manager):
    print("\n--- Teacher List ---")
    if not manager.teachers:
        print("No teachers in the system.")
        return
    for t in manager.teachers:
        print(f"  ID: {t.id}, Name: {t.name}, Speciality: {t.speciality}")

def list_courses(manager):
    print("\n--- Course List ---")
    if not manager.courses:
        print("No courses in the system.")
        return
    for c in manager.courses:
        print(f"  ID: {c.id}, Name: {c.name}, Instrument: {c.instrument}, "
              f"Teacher ID: {c.teacher_id}, Enrolled: {c.enrolled_student_ids}")

def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager() # Create ONE instance of the application brain.

    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        # TODO: Create a menu for the new PST3 functions.
        # Get user input and call the appropriate view function, passing 'manager' to it.
        print("1. View daily roster")
        print("2. Check in student")
        print("3. Switch student's course")
        print("4. List students")
        print("5. List teachers")
        print("6. List courses")
        print("q. Quit")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            day = input("Enter day (e.g., Monday): ")
            front_desk_daily_roster(manager, day)
        elif choice == '2':
            s_id = input("Enter student ID: ").strip()
            c_id = input("Enter course ID: ").strip()
            # only continue if both inputs are actually whole numbers
            if s_id.isdigit() and c_id.isdigit():
                check_in_student(manager, int(s_id), int(c_id))
            else:
                print("Error: Student ID and Course ID must both be numbers.")
        elif choice == '3':
            s_id = input("Enter student ID: ").strip()
            from_id = input("Enter current course ID: ").strip()
            to_id = input("Enter new course ID: ").strip()
            if s_id.isdigit() and from_id.isdigit() and to_id.isdigit():
                switch_course(manager, int(s_id), int(from_id), int(to_id))
            else:
                print("Error: Student ID and Course IDs must all be numbers.")
        elif choice == '4':
            list_students(manager)
        elif choice == '5':
            list_teachers(manager)
        elif choice == '6':
            list_courses(manager)
        elif choice.lower() == 'q':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
