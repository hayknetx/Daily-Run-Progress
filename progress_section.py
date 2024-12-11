import os
import json
import streamlit as st

running_progress_dict = {}

def remove_progress(key):
    global running_progress_dict
    del running_progress_dict[key]
    with open("running_progress.json", "w") as f:
        json.dump(running_progress_dict, f)

def add_progress_section(running_progress):
    global running_progress_dict
    running_progress_dict = running_progress
    for i, (key, value) in enumerate(running_progress_dict.items()):
        col1, col2 = st.columns([3, 1])  # Adjust column widths as needed
        col1.write(f"Ամսի {key.split(' ')[0]}-ին, ժամը {key.split(' ')[1]}-ին, {value.split(':')[0]} րոպե {value.split(':')[1]} վայրկյան")
        if col2.button("Ջնջել", key=f"progress_{key}"):
            remove_progress(key)
            st.rerun()