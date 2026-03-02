import streamlit as st
from datetime import date
from personality_logic import get_personality_and_enemy
from pdf_generator import generate_pdf
from collections import Counter

st.set_page_config(page_title="Astro-Number", layout="centered")

# ---------- CLEAN DARK THEME ----------
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: white;
}

.block-container {
    padding-top: 1rem;
}

h1, h2, h3 {
    color: #38bdf8;
}

.grid-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    max-width: 400px;
}

.grid-item {
    border: 1px solid #334155;
    height: 80px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:22px;
    font-weight:bold;
    background-color:#1e293b;
}

.highlight {
    background-color:#0ea5e9;
}

.missing {
    background-color:#7c3aed;
}
</style>
""", unsafe_allow_html=True)

st.title("ASTRO-NUMBER")
st.caption("Your Personal Numerology Snapshot")

name = st.text_input("Enter Your Name")
dob = st.date_input("Enter Your Date of Birth", min_value=date(1900, 1, 1))

st.caption(f"Selected DOB (DD-MM-YYYY): {dob.strftime('%d-%m-%Y')}")

def reduce_to_single(num):
    while num > 9:
        num = sum(int(d) for d in str(num))
    return num

if st.button("Generate Report"):
    if not name:
        st.warning("Please enter your name.")
    else:

        # --- STRICT DOB STRING ---
        dob_str = dob.strftime("%d%m%Y")

        day = dob.day

        # Core numbers
        mulank = reduce_to_single(day)
        bhagyank = reduce_to_single(sum(int(d) for d in dob_str))

        current_year = date.today().year
        personal_year = reduce_to_single(
            sum(int(d) for d in dob.strftime("%d%m") + str(current_year))
        )

        # --- Correct Lo Shu Count ---
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

        grid_layout = [4,9,2,3,5,7,8,1,6]

        st.markdown('<div class="grid-container">', unsafe_allow_html=True)

        for num in grid_layout:
            if num in count:
                st.markdown(
                    f'<div class="grid-item highlight">{num} ({count[num]})</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="grid-item missing">{num}</div>',
                    unsafe_allow_html=True
                )

        st.markdown('</div>', unsafe_allow_html=True)

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
