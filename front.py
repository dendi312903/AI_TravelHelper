import streamlit as st
import requests as rq
st.title("AI Travel Helper")
def btnaction():
	a = rq.post("127.0.0.1:8000/places")
	return a
if st.button("get places"):
	a = rq.get("http://127.0.0.1:8000/places")
	st.write(a.json())
