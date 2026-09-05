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

def list_students_in_course(manager, course_id):
    """Shows every student enrolled in a given course."""
    course = manager.find_course_by_id(course_id)
    if not course:
        print(f"Error: Course with ID {course_id} not found.")
        return
    if not course.enrolled_student_ids:
        print("No students enrolled in this course.")
        return
    print(f"\n--- Students Enrolled in {course.name} ---")
    # a course only stores student ids, so look each one up to get their name
    for student_id in course.enrolled_student_ids:
        student = manager.find_student_by_id(student_id)
        if student:
            print(f"  ID: {student.id}, Name: {student.name}")

def print_student_card(manager, student_id):
    """Creates a text file badge for a student, same idea as PST2."""
    student = manager.find_student_by_id(student_id)
    if not student:
        print(f"Error: Could not print card, student {student_id} not found.")
        return
    filename = f"{student_id}_card.txt"
    with open(filename, 'w') as f:
        f.write("========================\n")
        f.write("  MUSIC SCHOOL ID BADGE\n")
        f.write("========================\n")
        f.write(f"ID: {student.id}\n")
        f.write(f"Name: {student.name}\n")
    print(f"Printed student card to {filename}.")

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
        print("7. Add student")
        print("8. Add teacher")
        print("9. Remove student")
        print("10. Remove teacher")
        print("11. Update student name")
        print("12. Update teacher info")
        print("13. Add course")
        print("14. List students in a course")
        print("15. Print student card")
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
        elif choice == '7':
            name = input("Enter student name: ").strip()
            manager.add_student(name)
        elif choice == '8':
            name = input("Enter teacher name: ").strip()
            spec = input("Enter speciality: ").strip()
            manager.add_teacher(name, spec)
        elif choice == '9':
            s_id = input("Enter student ID to remove: ").strip()
            if s_id.isdigit():
                manager.remove_student(int(s_id))
            else:
                print("Error: Student ID must be a number.")
        elif choice == '10':
            t_id = input("Enter teacher ID to remove: ").strip()
            if t_id.isdigit():
                manager.remove_teacher(int(t_id))
            else:
                print("Error: Teacher ID must be a number.")
        elif choice == '11':
            s_id = input("Enter student ID to update: ").strip()
            new_name = input("Enter new name: ").strip()
            if s_id.isdigit():
                manager.update_student(int(s_id), name=new_name)
            else:
                print("Error: Student ID must be a number.")
        elif choice == '12':
            t_id = input("Enter teacher ID to update: ").strip()
            new_name = input("Enter new name (leave blank to skip): ").strip()
            new_spec = input("Enter new speciality (leave blank to skip): ").strip()
            if t_id.isdigit():
                manager.update_teacher(int(t_id), name=new_name, speciality=new_spec)
            else:
                print("Error: Teacher ID must be a number.")
        elif choice == '13':
            name = input("Enter course name: ").strip()
            inst = input("Enter instrument: ").strip()
            t_id = input("Enter teacher ID: ").strip()
            if t_id.isdigit():
                manager.add_course(name, inst, int(t_id))
            else:
                print("Error: Teacher ID must be a number.")
        elif choice == '14':
            c_id = input("Enter course ID: ").strip()
            if c_id.isdigit():
                list_students_in_course(manager, int(c_id))
            else:
                print("Error: Course ID must be a number.")
        elif choice == '15':
            s_id = input("Enter student ID: ").strip()
            if s_id.isdigit():
                print_student_card(manager, int(s_id))
            else:
                print("Error: Student ID must be a number.")
        elif choice.lower() == 'q':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()