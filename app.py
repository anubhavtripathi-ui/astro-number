import streamlit as st
from datetime import date
from personality_logic import get_personality_and_enemy
from pdf_generator import generate_pdf
from collections import Counter

st.set_page_config(page_title="Astro-Number", layout="centered")

# ---------- Custom CSS ----------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    margin-bottom: 20px;
}
.title-text {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    color: white;
}
.subtitle-text {
    text-align: center;
    font-size: 18px;
    color: #dddddd;
    margin-bottom: 30px;
}
.grid-box {
    border: 2px solid #444;
    height: 75px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: bold;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<div class="title-text">🔢 Astro-Number</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Your Personal Numerology Snapshot</div>', unsafe_allow_html=True)

# ---------- Input Card ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

name = st.text_input("Enter Your Name")
dob = st.date_input("Enter Your Date of Birth", min_value=date(1900, 1, 1))

st.markdown('</div>', unsafe_allow_html=True)

def reduce_to_single(num):
    while num > 9:
        num = sum(int(d) for d in str(num))
    return num

if st.button("Generate Report"):
    if not name:
        st.warning("Please enter your name.")
    else:
        day = dob.day
        month = dob.month
        year = dob.year

        mulank = reduce_to_single(day)
        total = sum(int(d) for d in f"{day}{month}{year}")
        bhagyank = reduce_to_single(total)

        current_year = date.today().year
        py_total = sum(int(d) for d in f"{day}{month}{current_year}")
        personal_year = reduce_to_single(py_total)

        digits = [int(d) for d in f"{day}{month}{year}" if d != "0"]
        count = Counter(digits)
        missing = [num for num in range(1, 10) if num not in count]

        personality, enemy = get_personality_and_enemy(mulank)

        # ---------- Results Card ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("### Core Numbers")
        col1, col2, col3 = st.columns(3)
        col1.metric("Mulank", mulank)
        col2.metric("Bhagyank", bhagyank)
        col3.metric("Personal Year", personal_year)

        st.markdown("---")
        st.markdown("### Lo Shu Grid")

        grid_layout = [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ]

        for row in grid_layout:
            cols = st.columns(3)
            for i, num in enumerate(row):
                with cols[i]:
                    if num in count:
                        st.markdown(
                            f'<div class="grid-box" style="background-color:#d4edda;">{num} ({count[num]})</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="grid-box" style="background-color:#f8d7da;">{num}</div>',
                            unsafe_allow_html=True
                        )

        st.markdown(f"**Missing Numbers:** {', '.join(map(str, missing))}")

        st.markdown("---")
        st.markdown("### Strength Meter")
        for num, freq in count.items():
            st.write(f"{num} appears {freq} time(s)")

        st.markdown("---")
        st.markdown("### Personality Insight")
        st.success(personality)

        st.markdown("### Enemy Number")
        st.error(f"{enemy}")

        st.markdown('</div>', unsafe_allow_html=True)

        pdf = generate_pdf(
            name,
            dob.strftime("%d-%m-%Y"),
            mulank,
            bhagyank,
            personal_year,
            missing,
            count,
            personality,
            enemy
        )

        st.download_button(
            label="Download Professional PDF",
            data=pdf,
            file_name="Astro-Number_Report.pdf",
            mime="application/pdf"
        )

