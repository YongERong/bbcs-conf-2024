import streamlit as st
import streamlit.components.v1 as components
from annotated_text import annotated_text
from back.story_generation import main as story_gen

# custom styles
st.markdown(
# increase height of buttons
    """
<style>
button {
    height: 5em;
}
</style>
""",
    unsafe_allow_html=True,
)


default_states = {
    "curr_screen":"selection",
    "prompts":[]
}
for state_name, default_value in default_states.items():
     if state_name not in st.session_state:
          st.session_state[state_name] = default_value
     

# Selection Container
if st.session_state.curr_screen == "selection":
    with st.container(border=False):

        # Get emojis
        emojis = ["😀", "😆", "😂", "🤨", "🤓"]
        n = len(emojis)

        # local states
        if '_is_pressed' not in st.session_state:
            st.session_state._is_pressed = [False] * n

        def setState(key):
            st.session_state._is_pressed[key] = False if st.session_state._is_pressed[key] else True

        # Buttons
        cols = st.columns(n)

        for i in range(n):
            col = cols[i]
            with col:
                st.button(label=f":{"red" if st.session_state._is_pressed[i] == True else "black"}-background[{emojis[i]}]", use_container_width=True, on_click=setState, kwargs={"key":i}, key=i)
        
        def startReading():
            prompts = [emojis[i] for i in range(n) if st.session_state._is_pressed[i] == True]

            if len(prompts) >= 1:
                st.session_state.prompts = prompts
                st.session_state.curr_screen = "reading"
            else:
                st.error("Choose at least one emoji")

        st.button(label="Go", use_container_width=True, on_click=startReading)

# Output Container
if st.session_state.curr_screen == "reading":
    with st.container(border=False):
        
        st.button("🔊Read")
        data = story_gen("".join(st.session_state.prompts), 9)
        paragraphs = data["paragraphs"]
        images = data["images"]
        words_used = data["words_used"]

        for img, para in zip(images, paragraphs):
            # TODO: Locate difficult words
            st.image(img, use_column_width=True)
            st.markdown(para)
            # annotated_text(

            # )
