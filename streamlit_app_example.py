"""
Streamlit App Example for Astro Number Calculator
Replace your existing PDF generation code with this
"""

import streamlit as st
from datetime import datetime
# Import the PDF generator
from astro_pdf_generator import generate_pdf

# Page configuration
st.set_page_config(
    page_title="Astro Number Calculator",
    page_icon="⭐",
    layout="centered"
)

# Title
st.title("⭐ Astro Number Calculator")
st.markdown("Discover your personality through numerology")

# Input section
st.subheader("Enter Your Details")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name", placeholder="Enter your name")

with col2:
    birth_date = st.date_input("Birth Date", min_value=datetime(1900, 1, 1))

# Language selection
language = st.radio(
    "Select Language / Bhasha Chunein",
    options=["English", "Hindi (Transliterated)"],
    horizontal=True
)

ln = True if language == "Hindi (Transliterated)" else False

# Calculate button
if st.button("Calculate Personality Number", type="primary"):
    if name:
        # Simple calculation (you can use your own logic here)
        # Example: Sum of birth date digits
        date_str = birth_date.strftime("%d%m%Y")
        total = sum(int(digit) for digit in date_str)
        
        # Reduce to single digit
        while total > 9:
            total = sum(int(digit) for digit in str(total))
        
        personality_number = total
        
        # Display result
        st.success(f"Your Personality Number: **{personality_number}**")
        
        # Generate PDF button
        st.markdown("---")
        st.subheader("📄 Download Your Report")
        
        try:
            pdf_bytes = generate_pdf(
                name=name,
                birth_date=birth_date.strftime("%d-%m-%Y"),
                personality_number=personality_number,
                ln=ln
            )
            
            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name=f"astro_report_{name.replace(' ', '_')}.pdf",
                mime="application/pdf",
                type="primary"
            )
            
            st.success("✅ Report generated successfully! Click the button above to download.")
            
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
            st.info("Please check if fpdf2 is installed: pip install fpdf2==2.7.9")
    else:
        st.warning("Please enter your name to continue.")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Made with ❤️ using Streamlit</p>",
    unsafe_allow_html=True
)
