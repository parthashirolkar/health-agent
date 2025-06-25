from profiles import create_profile, get_notes, get_profile
from ai import get_macros, ask_ai, check_langflow_connection
from form_submit import update_personal_info, add_note, delete_note
import streamlit as st


st.title("Personal Fitness Tool")


@st.fragment
def personal_data_form():
    with st.form("Personal Data"):
        st.header("Personal Data")

        profile = st.session_state.profile


        name = st.text_input("Name", value=profile["general"]["name"])
        age = st.number_input("Age", min_value=1, max_value=120, step=1, value=profile["general"]["age"])
        weight = st.number_input(
            "Weight (kg)", min_value=0.0, max_value=300.0, step=0.1, value=float(profile["general"]["weight"])
        )
        height = st.number_input(
            "Height (cm)", min_value=0.0, max_value=250.0, step=0.1, value=float(profile["general"]["height"])
        )
        genders = ["Male", "Female", "Other"]
        gender = st.radio("Gender", genders, genders.index(profile["general"].get("gender", "Male")))
        activities = (
            "Sedentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active",
            "Super Active",
        )
        activity_level = st.selectbox("Activity Level", activities, index=activities.index(profile["general"].get("activity_level", "Sedentary")))

        personal_data_submitted = st.form_submit_button("Save")

        if personal_data_submitted:
            if all([name, age, weight, height, gender, activity_level]):
                with st.spinner("Saving..."):
                    update_personal_info(profile, "general", name=name, weight=weight, height=height, gender=gender, age=age, activity_level=activity_level)
                    st.success("Personal data saved successfully!")

            else:
                st.warning("Please fill in all fields.")

@st.fragment
def goals_form():
    profile = st.session_state.profile
    with st.form("Goals"):
        st.header("Goals")

        goals = st.multiselect("Select your goals:", ["Muscle Gain", "Fat Loss", "Stay Active"],
                               default=profile.get("goals", []))

        goals_sumbit = st.form_submit_button("Save")
        if goals_sumbit:
            if goals:
                with st.spinner("Saving..."):
                    st.session_state.profile = update_personal_info(profile, "goals", goals=goals)
                    st.success("Goals saved successfully!")

            else:
                st.warning("Please select at least one goal.")



@st.fragment
def macros():
    profile = st.session_state.profile
    nutrition = st.container(border=True)
    nutrition.header("Macros")
    
    # Check Langflow connection status
    is_connected = check_langflow_connection()
    if is_connected:
        nutrition.success("🟢 AI Service: Connected")
    else:
        nutrition.warning("🔴 AI Service: Disconnected (Langflow not running on localhost:7860)")
    
    if nutrition.button("Generate with AI", disabled=not is_connected):
        if is_connected:
            result = get_macros(profile.get("general"), profile.get("goals"))
            profile["nutrition"] = result
            nutrition.success("AI has generated results.")
        else:
            nutrition.error("Cannot generate macros: AI service is not available.")

    with nutrition.form("nutrition_form", border=False):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            calories = st.number_input("Calories", min_value=0, step=1, value=int(profile["nutrition"].get("calories", 0)))

        with col2:
            protein = st.number_input("Protein", min_value=0, step=1, value=int(profile["nutrition"].get("protein", 0)))

        with col3:
            fat = st.number_input("Fat", min_value=0, step=1, value=int(profile["nutrition"].get("fat", 0)))

        with col4:
            carbs = st.number_input("Carbs", min_value=0, step=1, value=int(profile["nutrition"].get("carbs", 0)))

        if st.form_submit_button("Save"):
            with st.spinner("Saving..."):
                st.session_state.profile = update_personal_info(profile, "nutrition", calories=calories, protein=protein, fat=fat, carbs=carbs)
                st.success("Information Saved")



@st.fragment
def notes():
    st.subheader("Notes: ")
    
    # Display notes
    if st.session_state.notes:
        for i, note in enumerate(st.session_state.notes):
            cols = st.columns([5, 1])
            with cols[0]:
                st.text(note.get("text"))
            with cols[1]:
                if st.button("Delete", key=f"del_{note.get('_id')}"):
                    delete_note(note.get("_id"))
                    # Update session state without full rerun
                    st.session_state.notes = [n for n in st.session_state.notes if n.get("_id") != note.get("_id")]
                    st.rerun()
    else:
        st.info("No notes yet. Add your first note below!")
    
    # Add new note form
    with st.form("add_note_form", clear_on_submit=True):
        new_note = st.text_input("Add a new note: ")
        if st.form_submit_button("Add Note"):
            if new_note.strip():
                note = add_note(new_note, st.session_state.profile_id)
                st.session_state.notes.append(note)
                st.success("Note added successfully!")
                st.rerun()
            else:
                st.warning("Please enter a note before adding.")


@st.fragment
def ask_ai_func():
    st.subheader('Ask AI')
    
    with st.form("ask_ai_form", clear_on_submit=True):
        user_question = st.text_input("Ask AI a question: ")
        if st.form_submit_button("Ask AI"):
            if user_question.strip():
                with st.spinner("Getting AI response..."):
                    result = ask_ai(st.session_state.profile, user_question)
                    st.success("AI Response:")
                    st.write(result)
            else:
                st.warning("Please enter a question before asking AI.")

def forms():
    if "profile" not in st.session_state:
        profile_id = 1
        profile = get_profile(profile_id)
        if not profile:
            profile_id, profile = create_profile(profile_id)

        st.session_state.profile = profile
        st.session_state.profile_id = profile_id

    if "notes" not in st.session_state:
        st.session_state.notes = get_notes(st.session_state.profile_id)

        
    personal_data_form()
    goals_form()
    macros()
    notes()
    ask_ai_func()


if __name__ == "__main__":
    forms()
