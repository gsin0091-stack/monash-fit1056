# gui/student_pages.py
import streamlit as st
import pandas as pd

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")

    # --- Search Section (remains the same) ---
    st.subheader("Find a Student")
    # ...
    search_term = st.text_input("Search by name")
    # Keep a spot here for the results, but fill it in at the end of the page,
    # after the form below has run, so the results always show the latest data.
    search_results = st.container()

    # --- Registration Section (now works correctly) ---
    st.subheader("Register New Student")
    with st.form("registration_form"):
        reg_name = st.text_input("New Student Name")
        reg_instrument = st.text_input("First Instrument")
        submitted = st.form_submit_button("Register Student")

        if submitted:
            # This call now works because we implemented the method in PST3.
            # TODO: Add a check for blank name/instrument.
            if reg_name and reg_instrument:
                new_student = manager.register_new_student(reg_name, reg_instrument)
                if new_student:
                    st.success(f"Successfully registered {reg_name}!")
                    # You can use st.balloons() for extra flair.
                else:
                    st.error(f"Could not register student. A teacher for {reg_instrument} might not be available.")
            else:
                st.warning("Please enter both a name and an instrument.")

    # --- Add Student (without a course) ---
    st.subheader("Add Student")
    with st.form("add_student_form"):
        new_name = st.text_input("Student Name")
        if st.form_submit_button("Add Student"):
            # don't accept a blank name
            if new_name.strip():
                manager.add_student(new_name.strip())
                st.success(f"Added {new_name.strip()}!")
            else:
                st.warning("Please enter a name.")

    # The dropdowns show "id - name" so two students with the same name can be told apart.
    student_list = {f"{s.id} - {s.name}": s.id for s in manager.students}
    course_list = {f"{c.id} - {c.name}": c.id for c in manager.courses}

    # --- Add Student to Course ---
    st.subheader("Add Student to Course")
    if student_list and course_list:
        with st.form("enrol_form"):
            chosen_student = st.selectbox("Select Student", student_list.keys())
            chosen_course = st.selectbox("Select Course", course_list.keys())
            if st.form_submit_button("Add to Course"):
                if manager.enroll_student(student_list[chosen_student], course_list[chosen_course]):
                    st.success(f"Added {chosen_student} to {chosen_course}!")
                else:
                    st.error("Could not add them. (Are they already in that course?)")
    else:
        st.info("You need at least one student and one course first.")

    # --- Remove Student ---
    st.subheader("Remove Student")
    if student_list:
        with st.form("remove_form"):
            student_to_remove = st.selectbox("Select Student to remove", student_list.keys())
            confirm = st.checkbox("Yes, remove this student")
            if st.form_submit_button("Remove Student"):
                if not confirm:
                    st.warning("Please tick the box to confirm.")
                # remove_student also takes them out of every course they were in
                elif manager.remove_student(student_list[student_to_remove]):
                    st.success(f"Removed {student_to_remove}.")
                else:
                    st.error("Could not remove that student.")
    else:
        st.info("No students to remove.")

    # Fill in the search results now (they appear under the search box).
    with search_results:
        if search_term:
            matches = manager.find_students_by_name(search_term)
            if matches:
                rows = []
                for s in matches:
                    rows.append({"ID": s.id, "Name": s.name, "Course IDs": s.enrolled_course_ids})
                st.dataframe(pd.DataFrame(rows), hide_index=True)
            else:
                st.info("No students found with that name.")
