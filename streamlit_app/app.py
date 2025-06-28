import streamlit as st
import requests

st.title(" TailorTalk Assistant")

user_input = st.text_input("Type your message...")

if st.button("Send") and user_input.strip():
    try:
        response = requests.post(
            "http://localhost:8000/chat", 
            json={"input": user_input}
        )

        if response.status_code == 200:
            result = response.json()
            st.markdown(result.get("output", " No output returned."))
        else:
            st.error(f" Server error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f" Could not connect to backend: {e}")
    except requests.exceptions.JSONDecodeError:
        st.error(" Response was not valid JSON.")
