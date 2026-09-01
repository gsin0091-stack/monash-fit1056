# pst2_main.py - The Persistent Application

import json
import datetime

DATA_FILE = "msms.json"
app_data = {} # This global dictionary will hold ALL our data.

# --- Core Persistence Engine ---
def load_data(path=DATA_FILE):
    """Loads all application data from a JSON file."""
    global app_data
    try:
        with open(path, 'r') as f:
            # TODO: Use json.load(f) to load the file's content into the global 'app_data' variable.
            app_data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        # TODO: If the file doesn't exist, initialize 'app_data' with a default dictionary.
        # It should have keys like: "students", "teachers", "attendance", "next_student_id", "next_teacher_id".
        # The lists should be empty and the IDs should start at 1.
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }

def save_data(path=DATA_FILE):
    """Saves all application data to a JSON file."""
    # TODO: Open the file at 'path' in write mode ('w').
    # Use json.dump() to write the global 'app_data' dictionary to the file.
    # Use the 'indent=4' argument in json.dump() to make the file readable.
    with open(path, 'w') as f:
        json.dump(app_data, f, indent=4)
    print("Data saved successfully.")

# --- Full CRUD for Core Data ---
# Note: We are now working with lists of dictionaries, not lists of objects.

def add_teacher(name, speciality):
    """Adds a teacher dictionary to the data store."""
    # TODO: Get the next teacher ID from app_data['next_teacher_id'].
    teacher_id = app_data['next_teacher_id']
    # TODO: Create a new teacher dictionary with 'id', 'name', and 'speciality' keys.
    new_teacher = {"id": teacher_id, "name": name, "speciality": speciality}
    # TODO: Append the new dictionary to the app_data['teachers'] list.
    app_data['teachers'].append(new_teacher)
    # TODO: Increment the 'next_teacher_id' in app_data.
    app_data['next_teacher_id'] += 1
    print(f"Core: Teacher '{name}' added.")

def update_teacher(teacher_id, **fields):
    """Finds a teacher by ID and updates their data with provided fields."""
    # TODO: Loop through the app_data['teachers'] list.
    for teacher in app_data['teachers']:
        # TODO: If a teacher's 'id' matches teacher_id:
        if teacher['id'] == teacher_id:
            # Use the .update() method on the teacher dictionary to apply the 'fields'.
            teacher.update(fields)
            print(f"Teacher {teacher_id} updated.")
            return
    print(f"Error: Teacher with ID {teacher_id} not found.")

def remove_student(student_id):
    """Removes a student from the data store."""
    # TODO: Find the student dictionary in app_data['students'] with the matching ID.
    # If found, use the .remove() method on the list to delete it.
    # A list comprehension is a clean way to do this:
    for student in app_data['students']:
        if student['id'] == int(student_id):
            app_data['students'].remove(student)
            print(f"Student {student_id} removed.")
            return True
    print(f"Error: Student with ID {student_id} not found.")
    return False

# TODO: Implement remove_teacher() and update_student() using the patterns above.

def remove_teacher(teacher_id):
    """Removes a teacher from the data store."""
    for teacher in app_data['teachers']:
        if teacher['id'] == int(teacher_id):
            app_data['teachers'].remove(teacher)
            print(f"Teacher {teacher_id} removed.")
            return True
    print(f"Error: Teacher with ID {teacher_id} not found.")
    return False


def update_student(student_id, **fields):
    """Finds a student by ID and updates their data with provided fields."""
    for student in app_data['students']:
        if student['id'] == student_id:
            student.update(fields)
            print(f"Student {student_id} updated.")
            return
    print(f"Error: Student with ID {student_id} not found.")

def add_student(name, instrument):
    """Adds a student dictionary to the data store."""
    student_id = app_data['next_student_id']
    new_student = {"id": student_id, "name": name, "instrument": instrument, "enrolled_in": []}
    app_data['students'].append(new_student)
    app_data['next_student_id'] += 1
    print(f"Core: Student '{name}' added with ID {student_id}.")

# --- New Receptionist Features ---
def check_in(student_id, course_id, timestamp=None):
    """Records a student's attendance for a course."""
    if timestamp is None:
        # TODO: Get the current time as a string using datetime.datetime.now().isoformat()
        timestamp = datetime.datetime.now().isoformat()
    
    # TODO: Create a check-in record dictionary.
    # It should contain 'student_id', 'course_id', and 'timestamp'.
    check_in_record = {
        "student_id": student_id,
        "course_id": course_id,
        "timestamp": timestamp
    }
    # TODO: Append this new record to the app_data['attendance'] list.
    app_data['attendance'].append(check_in_record)
    print(f"Receptionist: Student {student_id} checked into {course_id}.")

def print_student_card(student_id):
    """Creates a text file badge for a student."""
    # TODO: Find the student dictionary in app_data['students'].
    student_to_print = None
    for s in app_data['students']:
        if s['id'] == student_id:
            student_to_print = s
            break
    
    if student_to_print:
        # TODO: Create a filename, e.g., f"{student_id}_card.txt".
        filename = f"{student_id}_card.txt"
        # TODO: Open the file in write mode ('w').
        with open(filename, 'w') as f:
            # Write the student's details to the file in a nice format.
            f.write("========================\n")
            f.write(f"  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student_to_print['id']}\n")
            f.write(f"Name: {student_to_print['name']}\n")
            f.write(f"Instrument: {student_to_print.get('instrument', '')}\n")
        print(f"Printed student card to {filename}.")
    else:
        print(f"Error: Could not print card, student {student_id} not found.")

def list_students():
    """Prints all students in the database."""
    print("\n--- Student List ---")
    if not app_data['students']:
        print("No students in the system.")
        return
    for s in app_data['students']:
        print(f"  ID: {s['id']}, Name: {s['name']}, Instrument: {s['instrument']}")

def list_teachers():
    """Prints all teachers in the database."""
    print("\n--- Teacher List ---")
    if not app_data['teachers']:
        print("No teachers in the system.")
        return
    for t in app_data['teachers']:
        print(f"  ID: {t['id']}, Name: {t['name']}, Speciality: {t['speciality']}")

# --- Main Application Loop ---
def main():
    """Main function to run the MSMS application."""
    load_data() # Load all data from file at startup.

    while True:
        print("\n===== MSMS v2 (Persistent) =====")
        print("1. Check-in Student")
        print("2. Print Student Card")
        print("3. Update Student Info")
        print("4. Update Teacher Info")
        print("5. Remove Student")
        print("6. Remove Teacher")
        print("7. Add Student")
        print("8. Add Teacher")
        print("9. List all students")
        print("10. List all teachers")
        print("q. Quit and Save")
        
        choice = input("Enter your choice: ").strip()
        
        made_change = False # A flag to track if we need to save
        if choice == '1':
            # TODO: Get student_id and course_id from user, then call check_in().
            s_id = input("Enter student ID to check in: ").strip()
            c_id = input("Enter course ID: ").strip()
            if s_id.isdigit():
                check_in(int(s_id), c_id)
                made_change = True
            else:
                print("Error: Student ID must be a valid number.")
        elif choice == '2':
            # TODO: Get student_id, then call print_student_card().
            s_id = input("Enter student ID to print card: ").strip()
            if s_id.isdigit():
                print_student_card(int(s_id))
            else:
                print("Error: Student ID must be a valid number.")
            pass # No change made, so no save needed
        elif choice == '3':
            # TODO: Get student_id and new details, then call update_student().
            # Example: update_student(1, instrument="Flute")
            s_id = input("Enter student ID to update: ").strip()
            if not s_id.isdigit():
                print("Error: Student ID must be a valid number.")
                continue
            new_inst = input("Enter new instrument (leave blank to skip): ").strip()
            new_name = input("Enter new name (leave blank to skip): ")
            details = {}
            if new_inst: details['instrument'] = new_inst
            if new_name: details['name'] = new_name
            update_student(int(s_id), **details)
            made_change = True
        elif choice == '4':
            # TODO: Get teacher_id and new details, then call update_teacher().
            # Example: update_teacher(1, speciality="Advanced Piano")
            t_id = input("Enter teacher ID to update: ").strip()
            if not t_id.isdigit():
                print("Error: Teacher ID must be a valid number.")
                continue
            new_spec = input("Enter new speciality (leave blank to skip): ").strip()
            new_name = input("Enter new name (leave blank to skip): ")
            details = {}
            if new_spec: details['speciality'] = new_spec
            if new_name: details['name'] = new_name
            update_teacher(int(t_id), **details)
            made_change = True
        elif choice == '5':
            # TODO: Get student_id, then call remove_student().
            s_id = input("Enter student ID to remove: ").strip()
            if s_id.isdigit():
                remove_student(int(s_id))
                made_change = True
            else:
                print("Error: Student ID must be a valid number.")
        elif choice == '6':
            t_id = input("Enter teacher ID to remove: ").strip()
            if t_id.isdigit():
                remove_teacher(int(t_id))
                made_change = True
            else:
                print("Error: Teacher ID must be a valid number.")
        elif choice == '7':
            name = input("Enter student name: ").strip()
            inst = input("Enter instrument: ").strip()
            add_student(name, inst)
            made_change = True
        elif choice == '8':
            name = input("Enter teacher name: ").strip()
            spec = input("Enter speciality: ").strip()
            add_teacher(name, spec)
            made_change = True
        elif choice == '9':
            list_students()
        elif choice == '10':
            list_teachers()
        elif choice.lower() == 'q':
            print("Saving final changes and exiting.")
            break
        else:
            print("Invalid choice.")
            
        if made_change:
            save_data() # Save the data immediately after any change.

    save_data() # One final save on exit.

# --- Program Start ---
if __name__ == "__main__":
    main()
