import os
import json
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
from goal_section import add_goal_section, get_mean_daily_progress
from progress_section import add_progress_section

running_progress_dict = {}
if os.path.exists("running_progress.json"):
    with open("running_progress.json", "r") as f:
        running_progress_dict = json.load(f)
col1, col2, col3 = st.columns(3)
running_date = col1.date_input("Վազելու օր", datetime.today())
running_time = col2.selectbox("Վազելու ժամ", ["07:00", "15:00", "18:00"])
running_duration = col3.time_input("Վազելու ժամանակ", step=60)
running_date_time = running_date.strftime('%Y-%m-%d ') + running_time
save_progress = st.button("Ավելացնել")
if save_progress:
    running_progress_dict[running_date_time] = running_duration.strftime("%H:%M")
    with open("running_progress.json", "w") as f:
        json.dump(running_progress_dict, f)
x = running_progress_dict.keys()
y = [datetime.strptime(i, "%H:%M").time() for i in running_progress_dict.values()]
timedeltas_y = [t.hour*60+t.minute for t in y]
if x:
    fig = px.scatter(x=x, y=timedeltas_y)
    fig.add_trace(px.line(x=x, y=timedeltas_y ).data[0])
    mean_daily_progress = get_mean_daily_progress(running_progress_dict)
    goal_time_delta = []
    goal_time = []
    if mean_daily_progress:
        goal_time = add_goal_section()
        if goal_time:
            goal_time = datetime.strptime(goal_time, "%H:%M")
            goal_achive_date = list(running_progress_dict.keys())[-1].split(' ')[0]
            goal_achive_date = datetime.strptime(goal_achive_date, '%Y-%m-%d')
            last_running_duration = list(running_progress_dict.values())[-1]
            last_running_duration = datetime.strptime(last_running_duration, "%H:%M")
            last_diff = (last_running_duration-goal_time).seconds//60
            st.write(f"Միջինում հաջորդ վազքը լինում է {mean_daily_progress.minute} վայրկյան ավելի արագ։")
            while last_diff - mean_daily_progress.minute > 0:
                goal_achive_date += timedelta(days=1)
                last_running_duration = last_running_duration - mean_daily_progress
                last_running_duration = datetime.strptime(str(last_running_duration), "%H:%M:%S")
                last_diff = (last_running_duration-goal_time).seconds//60
            goal_achive_date += timedelta(days=1)
            goal_achive_date = [goal_achive_date.strftime('%Y-%m-%d')]
            goal_time_delta = [goal_time.hour*60+goal_time.minute]
            goal_time = [goal_time.strftime("%H:%M")]
            fig.add_trace(px.scatter(x=goal_achive_date, y=goal_time_delta, color_discrete_sequence=['red']).data[0])
    fig.update_xaxes(title_text='Ամսաթիվ')
    fig.update_yaxes(title_text='Վազքի Ժամանակ', tickvals=timedeltas_y + goal_time_delta, ticktext=list(running_progress_dict.values()) + goal_time)
    st.plotly_chart(fig)
add_progress_section(running_progress_dict)