import streamlit as st
from datetime import datetime, date
from personality_logic import get_personality_and_enemy
from pdf_generator import generate_pdf
from collections import Counter

st.set_page_config(page_title="Astro-Number", layout="centered")

# Remove default padding
st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}
.stApp {
    background-color: #0b1120;
    color: white;
}
.block-container {
    padding-top: 1rem;
}
h1 {
    text-align: center;
}
div.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 100%;
    font-weight: bold;
}
div.stButton > button:hover {
    background-color: #1d4ed8;
}
.grid-box {
    height:70px;
    display:flex;
    align-items:center;
    justify-content:center;
    border:1px solid #334155;
    background-color:#1e293b;
    font-weight:bold;
    font-size:20px;
}
</style>
""", unsafe_allow_html=True)

st.title("ASTRO-NUMBER")
st.caption("Your Personal Numerology Snapshot")

name = st.text_input("Enter Your Name")

dob_input = st.text_input("Enter DOB (DD-MM-YYYY)")

def reduce_to_single(num):
    while num > 9:
        num = sum(int(d) for d in str(num))
    return num

if st.button("Generate Report"):

    if not name or not dob_input:
        st.warning("Please enter all fields.")
    else:
        try:
            dob = datetime.strptime(dob_input, "%d-%m-%Y")
        except:
            st.error("DOB format must be DD-MM-YYYY")
            st.stop()

        dob_str = dob.strftime("%d%m%Y")

        mulank = reduce_to_single(dob.day)
        bhagyank = reduce_to_single(sum(int(d) for d in dob_str))

        current_year = date.today().year
        personal_year = reduce_to_single(
            sum(int(d) for d in dob.strftime("%d%m") + str(current_year))
        )

        digits = [int(d) for d in dob_str if d != "0"]
        count = Counter(digits)
        missing = [n for n in range(1,10) if n not in count]

        personality, enemy = get_personality_and_enemy(mulank)

        st.markdown("### Core Numbers")
        col1, col2, col3 = st.columns(3)
        col1.metric("Mulank", mulank)
        col2.metric("Bhagyank", bhagyank)
        col3.metric("Personal Year", personal_year)

        st.markdown("### Lo Shu Grid")

        grid = [4,9,2,3,5,7,8,1,6]

        for i in range(0,9,3):
            cols = st.columns(3)
            for j in range(3):
                num = grid[i+j]
                if num in count:
                    cols[j].markdown(
                        f'<div class="grid-box">{num} ({count[num]})</div>',
                        unsafe_allow_html=True
                    )
                else:
                    cols[j].markdown(
                        f'<div class="grid-box">{num}</div>',
                        unsafe_allow_html=True
                    )

        st.write(f"Missing Numbers: {', '.join(map(str, missing))}")

        st.markdown("### Personality Insight")
        st.info(personality)

        st.markdown("### Enemy Number")
        st.error(enemy)

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
