import streamlit as st
import pandas as pd
import calendar
from datetime import date

st.set_page_config(layout="wide")
st.title("📅 Project Daily Tracking Calendar testtt")

uploaded_file = st.file_uploader("📤 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Convert 'date' to datetime safely
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])  # Drop invalid dates
    df['date'] = df['date'].dt.date  # Convert to plain date

    # Get most common year
    year = pd.Series(df['date']).apply(lambda d: d.year).mode()[0]
    cal = calendar.Calendar(firstweekday=0)
    months = list(calendar.month_name)[1:]

    # Group data by date (per project)
    date_project_dict = {}
    for _, row in df.iterrows():
        day = row['date']
        if day not in date_project_dict:
            date_project_dict[day] = []
        date_project_dict[day].append({
            'project': row['project'],
            'progress': row['progress'],
            'total_bugs': row['total_bugs'],
            'solved_bugs': row['solved_bugs']
        })

    for month_index, month_name in enumerate(months, start=1):
        st.subheader(f"📅 {month_name} {year}")
        weeks = cal.monthdayscalendar(year, month_index)

        # Day names
        cols = st.columns(7)
        for i, day_name in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
            cols[i].markdown(f"**{day_name}**")

        # Calendar rows
        for week in weeks:
            cols = st.columns(7)
            for i, day in enumerate(week):
                if day == 0:
                    cols[i].markdown("")
                else:
                    current_date = date(year, month_index, day)
                    content = f"**{day}**"
                    if current_date in date_project_dict:
                        for proj in date_project_dict[current_date]:
                            content += (
                                f"\n\n🧩 {proj['project']}  \n"
                                f"🔵 {proj['progress']}%  \n"
                                f"🔴 {proj['total_bugs']}  \n"
                                f"🟢 {proj['solved_bugs']}"
                            )
                    cols[i].markdown(content)
else:
    st.info("👆 Upload an Excel file to see the calendar.")