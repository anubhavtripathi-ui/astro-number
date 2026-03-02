import streamlit as st
from datetime import date
from personality_logic import get_personality
from pdf_generator import generate_pdf
from collections import Counter

st.set_page_config(page_title="Astro-Number", layout="centered")

st.title("🔢 Astro-Number")
st.subheader("Your Personal Numerology Snapshot")

name = st.text_input("Enter Your Name")
dob = st.date_input("Enter Your Date of Birth", min_value=date(1900, 1, 1))

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

        # Mulank
        mulank = reduce_to_single(day)

        # Bhagyank
        total = sum(int(d) for d in f"{day}{month}{year}")
        bhagyank = reduce_to_single(total)

        # Personal Year
        current_year = date.today().year
        py_total = sum(int(d) for d in f"{day}{month}{current_year}")
        personal_year = reduce_to_single(py_total)

        # Lo Shu Grid
        digits = [int(d) for d in f"{day}{month}{year}" if d != "0"]
        count = Counter(digits)

        lo_shu_positions = [4,9,2,3,5,7,8,1,6]
        missing = [num for num in range(1,10) if num not in count]

        st.markdown("---")
        st.markdown("### Core Numbers")
        st.write(f"**Mulank:** {mulank}")
        st.write(f"**Bhagyank:** {bhagyank}")
        st.write(f"**Personal Year:** {personal_year}")

        st.markdown("---")
        st.markdown("### Lo Shu Grid")

        cols = st.columns(3)
        for i, num in enumerate(lo_shu_positions):
            with cols[i % 3]:
                if num in count:
                    st.success(f"{num} ({count[num]})")
                else:
                    st.error(f"{num}")

        st.markdown(f"**Missing Numbers:** {', '.join(map(str, missing))}")

        st.markdown("---")
        st.markdown("### Strength Meter")
        for num, freq in count.items():
            st.write(f"{num} appears {freq} time(s)")

        personality = get_personality(mulank)
        st.markdown("---")
        st.markdown("### Personality Insight")
        st.info(personality)

        pdf = generate_pdf(name, dob, mulank, bhagyank, personal_year, missing, count, personality)

        st.download_button(
            label="Download Professional PDF",
            data=pdf,
            file_name="Astro-Number_Report.pdf",
            mime="application/pdf"
        )