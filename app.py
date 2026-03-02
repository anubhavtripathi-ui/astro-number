import streamlit as st
from datetime import datetime
from fpdf import FPDF
import io

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Astro-Number",
    page_icon="🔢",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CSS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
    background-color: #F7F4EF;
    color: #2C2C2C;
}

.stApp {
    background-color: #F7F4EF;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
}

.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #3D2B1F;
    text-align: center;
    letter-spacing: 2px;
    margin-bottom: 4px;
}

.subtitle {
    text-align: center;
    color: #7A6652;
    font-size: 1rem;
    letter-spacing: 1px;
    margin-bottom: 30px;
    font-weight: 300;
}

.divider {
    border: none;
    border-top: 1px solid #D8C9B5;
    margin: 20px 0;
}

.result-card {
    background: #FFFFFF;
    border: 1px solid #E3D9CC;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.result-card h3 {
    color: #3D2B1F;
    margin-bottom: 6px;
    font-size: 1.1rem;
}

.number-badge {
    display: inline-block;
    background: #3D2B1F;
    color: #F7F4EF;
    border-radius: 50%;
    width: 48px;
    height: 48px;
    line-height: 48px;
    text-align: center;
    font-size: 1.4rem;
    font-weight: 700;
    font-family: 'Playfair Display', serif;
    margin-right: 12px;
    vertical-align: middle;
}

.planet-chip {
    display: inline-block;
    background: #F0E9DF;
    border: 1px solid #D8C9B5;
    color: #5C4033;
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.8rem;
    letter-spacing: 1px;
    font-weight: 600;
}

/* Loshu Grid */
.loshu-grid {
    display: grid;
    grid-template-columns: repeat(3, 90px);
    grid-template-rows: repeat(3, 90px);
    gap: 6px;
    justify-content: center;
    margin: 20px auto;
}

.loshu-cell {
    width: 90px;
    height: 90px;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
    font-weight: 700;
    font-family: 'Playfair Display', serif;
    border: 2px solid rgba(0,0,0,0.08);
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}

.loshu-cell .cell-number {
    font-size: 1.8rem;
    font-weight: 700;
    line-height: 1;
}

.loshu-cell .cell-planet {
    font-size: 0.55rem;
    letter-spacing: 1px;
    font-family: 'Lato', sans-serif;
    font-weight: 600;
    margin-top: 4px;
    opacity: 0.8;
}

.cell-present {
    background: #FFFFFF;
    color: #2C2C2C;
}

.cell-missing {
    background: #FDE8E8;
    color: #C0392B;
    border: 2px solid #F5C6C6;
}

.missing-tag {
    font-size: 0.45rem;
    background: #C0392B;
    color: white;
    padding: 1px 4px;
    border-radius: 4px;
    margin-top: 2px;
}

.tag-pill {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 30px;
    font-size: 0.9rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.enemy-box {
    background: #FFF8F0;
    border: 1px solid #F0D9B5;
    border-radius: 10px;
    padding: 14px 18px;
    margin-top: 10px;
}

.stTextInput > div > div > input {
    background: #FFFFFF;
    border: 1px solid #D8C9B5;
    border-radius: 8px;
    color: #2C2C2C;
    font-family: 'Lato', sans-serif;
}

.stButton > button {
    background: #3D2B1F;
    color: #F7F4EF;
    border: none;
    border-radius: 8px;
    font-family: 'Lato', sans-serif;
    font-weight: 600;
    letter-spacing: 1px;
    padding: 10px 28px;
    width: 100%;
    transition: all 0.2s;
}

.stButton > button:hover {
    background: #5C4033;
    color: #FFFFFF;
}

.stDownloadButton > button {
    background: #F0E9DF;
    color: #3D2B1F;
    border: 1px solid #D8C9B5;
    border-radius: 8px;
    font-family: 'Lato', sans-serif;
    font-weight: 600;
    letter-spacing: 1px;
    width: 100%;
    transition: all 0.2s;
}

.stDownloadButton > button:hover {
    background: #E0D0BC;
}

.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #3D2B1F;
    border-bottom: 2px solid #D8C9B5;
    padding-bottom: 6px;
    margin: 24px 0 14px 0;
}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── Data / Logic ───────────────────────────────────────────────────────────

LOSHU_POSITIONS = [4, 9, 2, 3, 5, 7, 8, 1, 6]   # row-major: top-left to bottom-right
LOSHU_PLANETS = {
    1: ("1", "SUN",     "#A8C8E8", "#1A5276"),
    2: ("2", "MOON",    "#D5E8D4", "#1E6B3C"),
    3: ("3", "JUPITER", "#B5EAD7", "#1A6B4A"),
    4: ("4", "RAHU",    "#FFADAD", "#7B1818"),
    5: ("5", "MERCURY", "#B8D4F0", "#1A3A6B"),
    6: ("6", "VENUS",   "#E8C8F0", "#5A1A7B"),
    7: ("7", "KETU",    "#C8E8D8", "#1A5A3A"),
    8: ("8", "SATURN",  "#FFD6A5", "#7B4A00"),
    9: ("9", "MARS",    "#C8D8F0", "#1A2A6B"),
}

PERSONALITY = {
    1: ("☀️ The Leader",      "Natural born leader — confident, independent, ambitious. You chart your own path and inspire others."),
    2: ("🌙 The Empath",      "Emotionally intelligent, intuitive, and caring. You feel deeply and nurture those around you."),
    3: ("✨ The Creator",      "Creative, expressive, and joyful. You bring art, communication, and enthusiasm wherever you go."),
    4: ("🏗️ The Builder",     "Practical, disciplined, and reliable. You build solid foundations and get things done."),
    5: ("🌀 The Explorer",    "Adventurous, versatile, and freedom-loving. Change excites you; routine bores you."),
    6: ("🏡 The Nurturer",    "Responsible, loving, and harmony-seeking. Family and community mean everything to you."),
    7: ("🔭 The Seeker",      "Analytical, introspective, and wise. You seek truth beneath the surface of things."),
    8: ("⚖️ The Powerhouse",  "Ambitious, authoritative, and material-minded. You understand power and how to wield it."),
    9: ("🌍 The Humanitarian","Compassionate, idealistic, and generous. You exist to serve a higher purpose."),
}

ENEMIES = {
    1: [6, 8],
    2: [9],
    3: [6, 8],
    4: [1, 9],
    5: [],          # Mercury is neutral / universal
    6: [1, 3],
    7: [1, 2],
    8: [1, 3],
    9: [2, 4],
}

MISSING_REMEDIES = {
    1: "Meditate on Sunday mornings. Use more orange/gold in your surroundings.",
    2: "Spend time near water. Wear white or silver. Strengthen your Moon.",
    3: "Journal daily. Explore creative hobbies. Chant Thursday mantras.",
    4: "Ground yourself with structure. Avoid impulsive decisions.",
    5: "Improve communication skills. Read and travel more.",
    6: "Cultivate harmony at home. Appreciate beauty and art.",
    7: "Develop spiritual practice. Trust your intuition more.",
    8: "Build financial discipline. Think long-term.",
    9: "Practice selfless service. Connect with Mars energy.",
}

def reduce_to_single(n: int) -> int:
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def calculate_mulank(dob: str) -> int:
    day = int(dob.split("-")[0])
    return reduce_to_single(day)

def calculate_bhagyank(dob: str) -> int:
    digits = [int(c) for c in dob if c.isdigit()]
    return reduce_to_single(sum(digits))

def get_missing_numbers(dob: str) -> list:
    digits_present = set(int(c) for c in dob if c.isdigit() and c != '0')
    all_numbers = set(range(1, 10))
    return sorted(all_numbers - digits_present)

def get_present_numbers(dob: str) -> set:
    return set(int(c) for c in dob if c.isdigit() and c != '0')

# ─── UI ─────────────────────────────────────────────────────────────────────

st.markdown('<div class="main-title">✦ ASTRO-NUMBER ✦</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Numerology · Loshu Grid · Planetary Insights</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Full Name", placeholder="e.g. Anubhav Tripathi")
    with col2:
        dob = st.text_input("Date of Birth (DD-MM-YYYY)", placeholder="e.g. 15-08-1995")

    calculate = st.button("✦ REVEAL MY NUMBERS")

if calculate:
    # Validation
    if not name.strip():
        st.error("Please enter your name.")
        st.stop()
    try:
        parsed = datetime.strptime(dob.strip(), "%d-%m-%Y")
    except ValueError:
        st.error("Invalid date format. Please use DD-MM-YYYY.")
        st.stop()

    mulank = calculate_mulank(dob)
    bhagyank = calculate_bhagyank(dob)
    missing = get_missing_numbers(dob)
    present = get_present_numbers(dob)
    personality = PERSONALITY[mulank]
    enemy_numbers = ENEMIES[mulank]

    # ── Core Numbers ──────────────────────────────────────────────────────
    st.markdown(f'<div class="section-header">✦ Reading for {name.strip()}</div>', unsafe_allow_html=True)

    col_m, col_b = st.columns(2)
    with col_m:
        planet_m = LOSHU_PLANETS[mulank]
        st.markdown(f"""
        <div class="result-card">
            <h3>Mulank (Birth Number)</h3>
            <span class="number-badge">{mulank}</span>
            <span class="planet-chip">{planet_m[1]}</span>
            <p style="margin-top:10px; color:#5C4033; font-size:0.9rem;">
            Your Mulank is derived from your birth day ({int(dob.split('-')[0])}).
            It reflects your innate personality and natural tendencies.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        planet_b = LOSHU_PLANETS[bhagyank]
        st.markdown(f"""
        <div class="result-card">
            <h3>Bhagyank (Destiny Number)</h3>
            <span class="number-badge">{bhagyank}</span>
            <span class="planet-chip">{planet_b[1]}</span>
            <p style="margin-top:10px; color:#5C4033; font-size:0.9rem;">
            Sum of all digits in your DOB. It reveals your life path,
            karmic mission and long-term destiny.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── Personality ───────────────────────────────────────────────────────
    st.markdown('<div class="section-header">✦ Personality Archetype</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="result-card">
        <span class="tag-pill" style="background:#F0E9DF; color:#3D2B1F; border:1px solid #D8C9B5;">
            {personality[0]}
        </span>
        <p style="margin-top:12px; color:#3D2B1F;">{personality[1]}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Enemy Numbers ─────────────────────────────────────────────────────
    st.markdown('<div class="section-header">✦ Enemy Numbers</div>', unsafe_allow_html=True)
    if enemy_numbers:
        enemy_planets = ", ".join([f"{n} ({LOSHU_PLANETS[n][1]})" for n in enemy_numbers])
        st.markdown(f"""
        <div class="result-card enemy-box">
            <p style="color:#7B1818; font-weight:600;">
            ⚠️ Numbers that create friction with your Mulank {mulank}:
            <strong>{enemy_planets}</strong>
            </p>
            <p style="color:#5C4033; font-size:0.88rem; margin-top:8px;">
            In numerology, enemy numbers can create challenges in partnerships, 
            career, or relationships. Be mindful when dealing with people 
            whose Mulank or Bhagyank matches these numbers.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-card">
            <p style="color:#1E6B3C;">✅ Number 5 (Mercury) is universally compatible — no enemy numbers!</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Loshu Grid ────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">✦ Loshu Grid</div>', unsafe_allow_html=True)

    # Build 3×3 grid HTML
    cells_html = ""
    for num in LOSHU_POSITIONS:
        _, planet, bg_present, fg_present = LOSHU_PLANETS[num]
        if num in present:
            cells_html += f"""
            <div class="loshu-cell cell-present" style="background:{bg_present}; color:{fg_present};">
                <div class="cell-number">{num}</div>
                <div class="cell-planet">{planet}</div>
            </div>"""
        else:
            cells_html += f"""
            <div class="loshu-cell cell-missing">
                <div class="cell-number">{num}</div>
                <div class="cell-planet">{planet}</div>
                <div class="missing-tag">MISSING</div>
            </div>"""

    st.markdown(f"""
    <div style="display:flex; flex-direction:column; align-items:center;">
        <div class="loshu-grid">{cells_html}</div>
        <div style="display:flex; gap:20px; margin-top:6px; font-size:0.8rem;">
            <span>🟩 Present in DOB</span>
            <span>🟥 Missing (shown in red)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Missing Numbers Analysis ──────────────────────────────────────────
    st.markdown('<div class="section-header">✦ Missing Numbers & Remedies</div>', unsafe_allow_html=True)
    if missing:
        for m in missing:
            remedy = MISSING_REMEDIES[m]
            planet_info = LOSHU_PLANETS[m]
            st.markdown(f"""
            <div class="result-card" style="border-left: 4px solid #C0392B;">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                    <span class="number-badge" style="background:#C0392B; width:36px; height:36px; line-height:36px; font-size:1.1rem;">{m}</span>
                    <span class="planet-chip">{planet_info[1]}</span>
                    <strong style="color:#3D2B1F;">Missing {m}</strong>
                </div>
                <p style="color:#5C4033; font-size:0.88rem; margin:0;">💡 <em>{remedy}</em></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-card">
            <p style="color:#1E6B3C;">🌟 All numbers 1–9 are present in your DOB — a rare and powerful chart!</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Name Number (Bonus) ───────────────────────────────────────────────
    PYTHAGOREAN = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,
                   'j':1,'k':2,'l':3,'m':4,'n':5,'o':6,'p':7,'q':8,'r':9,
                   's':1,'t':2,'u':3,'v':4,'w':5,'x':6,'y':7,'z':8}
    name_val = sum(PYTHAGOREAN.get(c.lower(), 0) for c in name if c.isalpha())
    name_number = reduce_to_single(name_val) if name_val else None

    if name_number:
        st.markdown('<div class="section-header">✦ Name Number (Bonus)</div>', unsafe_allow_html=True)
        name_planet = LOSHU_PLANETS[name_number]
        st.markdown(f"""
        <div class="result-card">
            <span class="number-badge">{name_number}</span>
            <span class="planet-chip">{name_planet[1]}</span>
            <p style="margin-top:10px; color:#5C4033; font-size:0.9rem;">
            Calculated using Pythagorean method from your name.
            Your name vibrates at number <strong>{name_number}</strong>.
            {PERSONALITY[name_number][0]} energy flows through your identity.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── PDF Generation ────────────────────────────────────────────────────
    st.markdown('<div class="section-header">✦ Download Report</div>', unsafe_allow_html=True)

    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Title
        pdf.set_font("Helvetica", "B", 22)
        pdf.set_text_color(61, 43, 31)
        pdf.cell(0, 12, "ASTRO-NUMBER REPORT", ln=True, align="C")
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(122, 102, 82)
        pdf.cell(0, 7, "Numerology | Loshu Grid | Planetary Insights", ln=True, align="C")
        pdf.ln(4)
        pdf.set_draw_color(216, 201, 181)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(6)

        # Personal Info
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(61, 43, 31)
        pdf.cell(0, 8, f"Name: {name.strip()}", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 7, f"Date of Birth: {dob}", ln=True)
        pdf.ln(4)

        # Core Numbers
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(61, 43, 31)
        pdf.cell(0, 8, "Core Numbers", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 7, f"Mulank (Birth Number): {mulank}  |  Planet: {LOSHU_PLANETS[mulank][1]}", ln=True)
        pdf.cell(0, 7, f"Bhagyank (Destiny Number): {bhagyank}  |  Planet: {LOSHU_PLANETS[bhagyank][1]}", ln=True)
        if name_number:
            pdf.cell(0, 7, f"Name Number: {name_number}  |  Planet: {LOSHU_PLANETS[name_number][1]}", ln=True)
        pdf.ln(3)

        # Personality
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(61, 43, 31)
        pdf.cell(0, 8, "Personality Archetype", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 7, personality[0], ln=True)
        pdf.multi_cell(0, 6, personality[1])
        pdf.ln(3)

        # Enemy Numbers
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(61, 43, 31)
        pdf.cell(0, 8, "Enemy Numbers", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(60, 60, 60)
        if enemy_numbers:
            ep = ", ".join([f"{n} ({LOSHU_PLANETS[n][1]})" for n in enemy_numbers])
            pdf.multi_cell(0, 6, f"Numbers creating friction with your Mulank {mulank}: {ep}")
        else:
            pdf.cell(0, 7, "No enemy numbers - Mercury (5) is universally compatible.", ln=True)
        pdf.ln(3)

        # Loshu Grid
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(61, 43, 31)
        pdf.cell(0, 8, "Loshu Grid", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(60, 60, 60)
        
        grid_data = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
        cell_w, cell_h = 40, 18
        start_x = (210 - 3 * cell_w - 2 * 3) / 2
        
        for row in grid_data:
            x = start_x
            y = pdf.get_y()
            for num in row:
                if num in present:
                    pdf.set_fill_color(240, 233, 223)
                    pdf.set_text_color(44, 44, 44)
                else:
                    pdf.set_fill_color(253, 232, 232)
                    pdf.set_text_color(192, 57, 43)
                pdf.set_xy(x, y)
                pdf.set_font("Helvetica", "B", 14)
                pdf.cell(cell_w, cell_h, str(num), border=1, align="C", fill=True)
                x += cell_w + 3
            pdf.ln(cell_h + 3)
        
        pdf.set_text_color(60, 60, 60)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, "White/Beige = Present  |  Pink/Red = Missing", ln=True, align="C")
        pdf.ln(3)

        # Missing Numbers
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(61, 43, 31)
        pdf.cell(0, 8, "Missing Numbers & Remedies", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(60, 60, 60)
        if missing:
            for m in missing:
                pdf.set_font("Helvetica", "B", 11)
                pdf.cell(0, 7, f"Missing {m} ({LOSHU_PLANETS[m][1]})", ln=True)
                pdf.set_font("Helvetica", "", 10)
                pdf.multi_cell(0, 6, f"  Remedy: {MISSING_REMEDIES[m]}")
                pdf.ln(1)
        else:
            pdf.cell(0, 7, "All numbers present - a rare and powerful chart!", ln=True)

        # Footer
        pdf.ln(6)
        pdf.set_draw_color(216, 201, 181)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(4)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(150, 130, 110)
        pdf.cell(0, 6, "Generated by Astro-Number | For guidance purposes only", ln=True, align="C")

        return pdf.output(dest='S').encode('latin-1')

    pdf_bytes = generate_pdf()
    st.download_button(
        label="📄 Download My Numerology Report (PDF)",
        data=pdf_bytes,
        file_name=f"AstroNumber_{name.strip().replace(' ','_')}.pdf",
        mime="application/pdf"
    )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <p style="text-align:center; color:#A08060; font-size:0.8rem; font-style:italic;">
    ✦ Astro-Number · For spiritual guidance only · Results are based on classical numerology traditions ✦
    </p>
    """, unsafe_allow_html=True)
