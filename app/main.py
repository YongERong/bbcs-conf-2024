import streamlit as st

# Get emojis
n = 5
emojis = ["😀", "😆", "😂", "🤨", "🤓"]


# Setup state
if 'is_pressed' not in st.session_state:
    st.session_state.is_pressed = ["secondary"] * n

# Buttons
cols = st.columns(n)
def setState(key):
    st.session_state.is_pressed[key] = "primary" if st.session_state.is_pressed[key] == "secondary" else "secondary"
    print(st.session_state.is_pressed)

for i in range(n):
    col = cols[i]
    with col:
        st.button(emojis[i], use_container_width=True, type=st.session_state.is_pressed[i], args=i)

# TODO: On click

st.button("GOO")