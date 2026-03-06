"""
Astro Number Calculator - Streamlit App
Discover your personality through numerology
"""

import streamlit as st
from datetime import datetime
from astro_pdf_generator import generate_pdf

# Page configuration
st.set_page_config(
    page_title="Astro Number Calculator",
    page_icon="⭐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.75rem;
        font-size: 1.1rem;
        border-radius: 8px;
        border: none;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    h1 {
        color: #4B0082;
        text-align: center;
    }
    .result-box {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("⭐ Astro Number Calculator")
st.markdown("<p style='text-align: center; color: gray;'>Discover your personality through numerology</p>", unsafe_allow_html=True)
st.markdown("---")

# Input Section
st.subheader("📝 Enter Your Details")

# Name input
name = st.text_input("Full Name", placeholder="Enter your full name", key="name_input")

# Birth date input
col1, col2 = st.columns(2)

with col1:
    birth_date = st.date_input(
        "Birth Date",
        min_value=datetime(1900, 1, 1),
        max_value=datetime.now(),
        value=datetime(2000, 1, 1),
        key="birth_date_input"
    )

with col2:
    # Language selection
    language = st.selectbox(
        "Report Language",
        options=["English", "Hindi (Transliterated)"],
        key="language_input"
    )

# Convert language to boolean
ln = True if language == "Hindi (Transliterated)" else False

# Calculate button
st.markdown("---")
calculate_clicked = st.button("🔮 Calculate My Number", type="primary")

if calculate_clicked:
    if name:
        # Calculate personality number from birth date
        date_str = birth_date.strftime("%d%m%Y")
        total = sum(int(digit) for digit in date_str)
        
        # Reduce to single digit (1-9)
        while total > 9:
            total = sum(int(digit) for digit in str(total))
        
        personality_number = total
        
        # Display result
        st.markdown("---")
        st.markdown(f"""
        <div class="result-box">
            <h2 style="text-align: center; color: #4B0082;">Your Personality Number: {personality_number}</h2>
            <p style="text-align: center; font-size: 1.1rem;">This number reveals your unique traits and life path!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Number meanings
        meanings = {
            1: "Leadership & Independence - You are a natural-born leader!",
            2: "Cooperation & Balance - You are a peacemaker and diplomat!",
            3: "Creativity & Expression - You are artistic and optimistic!",
            4: "Stability & Hard Work - You are dependable and organized!",
            5: "Freedom & Adventure - You love change and new experiences!",
            6: "Harmony & Family - You are nurturing and caring!",
            7: "Wisdom & Spirituality - You are analytical and thoughtful!",
            8: "Power & Ambition - You are strong and determined!",
            9: "Humanitarianism & Wisdom - You are compassionate and giving!"
        }
        
        st.info(f"✨ {meanings.get(personality_number, 'Discover your unique traits!')}")
        
        # Generate PDF Report
        st.markdown("---")
        st.subheader("📄 Download Your Detailed Report")
        
        try:
            # Generate PDF
            pdf_bytes = generate_pdf(
                name=name,
                birth_date=birth_date.strftime("%d-%m-%Y"),
                personality_number=personality_number,
                ln=ln
            )
            
            # Download button
            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name=f"astro_report_{name.replace(' ', '_')}.pdf",
                mime="application/pdf",
                type="primary"
            )
            
            st.success("✅ Your report is ready! Click the button above to download.")
            
        except Exception as e:
            st.error(f"❌ Error generating PDF: {str(e)}")
            st.info("Please make sure all required files are present in the repository.")
    else:
        st.warning("⚠️ Please enter your name to continue.")

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center; color: gray; font-size: 0.9rem;'>
    Made with ❤️ using Streamlit | © 2024 Astro Number Calculator
</p>
""", unsafe_allow_html=True)
