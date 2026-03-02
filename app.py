import streamlit as st
from datetime import date
from personality_logic import get_personality_and_enemy
from pdf_generator import generate_pdf
from collections import Counter

st.set_page_config(page_title="Astro-Number", layout="centered")

# ---------- MODERN DARK UI CSS ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.glass-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(15px);
    padding: 30px;
    border-radius: 18px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    margin-bottom: 25px;
}

.title-text {
    text-align: center;
    font-size: 38px;
    font-weight: 700;
    background: linear-gradient(90deg, #00f5ff, #7b2ff7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle-text {
    text-align: center;
    font-size: 18px;
    color: #cccccc;
    margin-bottom: 30px;
}

.grid-box {
    height: 75px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: bold;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.2);
}

.stButton>button {
    width: 100%;
    background: linear-gradient(90deg,#00f5ff,#7b2ff7);
    color: white;
    border: none;
    padding: 12px;
    border-radius: 10px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="title-text">ASTRO-NUMBER</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Your Personal Numerology Snapshot</div>', unsafe_allow_html=True)

# ---------- INPUT SECTION ----------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

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

        # ---------- RESULTS ----------
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

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
                            f'<div class="grid-box" style="background:rgba(0,255,150,0.15);">{num} ({count[num]})</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="grid-box" style="background:rgba(255,0,100,0.15);">{num}</div>',
                            unsafe_allow_html=True
                        )

        st.markdown(f"**Missing Numbers:** {', '.join(map(str, missing))}")

        st.markdown("---")
        st.markdown("### Personality Insight")
        st.info(personality)

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
