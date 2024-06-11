import streamlit as st

# Get emojis
emojis = ["😀", "😆", "😂", "🤨", "🤓"]
n = len(emojis)

# Setup state
if 'is_pressed' not in st.session_state:
    st.session_state.is_pressed = [False] * n

def setState(key):
    st.session_state.is_pressed[key] = False if st.session_state.is_pressed[key] else True

# Buttons
cols = st.columns(n)

for i in range(n):
    col = cols[i]
    with col:
        st.button(label=f":{"red" if st.session_state.is_pressed[i] == True else "black"}-background[{emojis[i]}]", use_container_width=True, on_click=setState, kwargs={"key":i}, key=i)


st.button("GOO")