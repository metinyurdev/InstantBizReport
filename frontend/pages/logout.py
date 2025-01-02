import streamlit as st

# Logout işlevi
def logout():
    st.session_state.token = None
    st.session_state.current_page = "login"
    st.rerun()