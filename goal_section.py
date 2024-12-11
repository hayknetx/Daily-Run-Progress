import os
import json
import numpy as np
from datetime import datetime
import streamlit as st

def get_mean_daily_progress(running_progress_dict):
    if len(running_progress_dict) < 2:
        return False
    progress_durations = list(running_progress_dict.values())
    progress_durations = np.array([datetime.strptime(x, "%H:%M") for x in progress_durations])
    progress_durations_diff = progress_durations[:-1]-progress_durations[1:]
    mean_daily_progress = np.mean(progress_durations_diff).seconds//60
    mean_daily_progress = datetime.strptime(str(mean_daily_progress), "%M")
    return mean_daily_progress


def add_goal_section():
    goal = {}
    if os.path.exists("goal.json"):
        with open("goal.json", "r") as f:
            goal = json.load(f)
    goal_duration = goal.get("running_duration", False)
    if goal_duration:
        goal_duration = datetime.strptime(goal_duration, "%H:%M")
    goal_running_duration = st.time_input("Նպատակ վազելու ժամանակ", step=60, value=goal_duration, key="goal_time")
    goal_button_text = "Ավելացնել նպատակը"
    if goal:
        goal_button_text = "Փոփոխել նպատակը"
    add_goal = st.button(goal_button_text)
    goal["running_duration"] = goal_running_duration.strftime("%H:%M")
    if add_goal:
        with open("goal.json", "w") as f:
            json.dump(goal, f)
        st.rerun()
    return goal.get("running_duration", False)