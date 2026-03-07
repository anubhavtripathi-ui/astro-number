"""
Complete Astro Number Report PDF Generator with All Features
"""

from fpdf import FPDF
from datetime import datetime


class AstroPDF(FPDF):
    """PDF class for Astro Number Reports"""
    
    def header(self):
        """PDF Header"""
        self.set_font('Arial', 'B', 18)
        self.set_text_color(70, 50, 150)
        self.cell(0, 15, 'Astro Number Report', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """PDF Footer"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def section_title(self, title):
        """Add a section title"""
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(230, 230, 250)
        self.set_text_color(50, 50, 100)
        self.cell(0, 10, title, 0, 1, 'L', True)
        self.ln(2)
    
    def section_body(self, text):
        """Add section body text"""
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, text)
        self.ln(5)


def calculate_moolank(day):
    """Calculate Moolank (Birth Number) from day"""
    total = day
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total


def calculate_bhagyank(day, month, year):
    """Calculate Bhagyank (Destiny Number) from full DOB"""
    total = day + month + year
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total


def get_star_rating(moolank, bhagyank):
    """Get star rating based on Moolank-Bhagyank combination"""
    # Star rating mapping from Excel
    ratings = {
        '1-1': '⭐⭐⭐⭐', '1-2': '⭐⭐⭐⭐½', '1-3': '⭐⭐⭐⭐½', '1-4': '⭐⭐⭐⭐',
        '1-5': '⭐⭐⭐⭐', '1-6': '⭐⭐⭐½', '1-7': '⭐⭐½', '1-8': '(–)', '1-9': '⭐⭐⭐⭐½',
        '2-1': '⭐⭐⭐', '2-2': '⭐⭐⭐', '2-3': '⭐⭐⭐⭐½', '2-4': '⭐⭐½',
        '2-5': '⭐⭐⭐', '2-6': '⭐⭐½', '2-7': '⭐⭐⭐⭐⭐', '2-8': '(–)', '2-9': '⭐⭐½',
        '3-1': '⭐⭐⭐', '3-2': '⭐⭐⭐⭐', '3-3': '⭐⭐⭐⭐½', '3-4': '⭐⭐',
        '3-5': '⭐⭐⭐⭐', '3-6': '(–)', '3-7': '⭐⭐', '3-8': '⭐⭐', '3-9': '⭐⭐⭐⭐½',
        '4-1': '⭐⭐⭐', '4-2': '⭐', '4-3': '⭐⭐', '4-4': '⭐⭐⭐',
        '4-5': '⭐⭐', '4-6': '⭐⭐⭐⭐', '4-7': '⭐⭐⭐⭐', '4-8': '⭐⭐', '4-9': '⭐',
        '5-1': '⭐⭐⭐⭐', '5-2': '⭐⭐⭐', '5-3': '⭐⭐⭐⭐½', '5-4': '⭐⭐',
        '5-5': '⭐⭐⭐⭐½', '5-6': '⭐⭐⭐⭐½', '5-7': '⭐⭐', '5-8': '⭐⭐', '5-9': '⭐⭐⭐',
        '6-1': '⭐⭐', '6-2': '⭐⭐', '6-3': '(–)', '6-4': '⭐⭐⭐⭐½',
        '6-5': '⭐⭐⭐⭐½', '6-6': '⭐⭐⭐⭐½', '6-7': '⭐⭐⭐⭐½', '6-8': '⭐⭐⭐', '6-9': '⭐',
        '7-1': '⭐⭐', '7-2': '⭐⭐⭐⭐⭐', '7-3': '⭐⭐', '7-4': '⭐⭐⭐⭐½',
        '7-5': '⭐⭐', '7-6': '⭐⭐⭐⭐½', '7-7': '⭐⭐⭐⭐½', '7-8': '⭐⭐', '7-9': '⭐⭐',
        '8-1': '(–)', '8-2': '(–)', '8-3': '⭐⭐', '8-4': '⭐⭐',
        '8-5': '⭐⭐', '8-6': '⭐⭐⭐', '8-7': '⭐⭐', '8-8': '⭐⭐⭐⭐', '8-9': '⭐⭐',
        '9-1': '⭐⭐⭐⭐', '9-2': '⭐⭐', '9-3': '⭐⭐⭐⭐½', '9-4': '⭐',
        '9-5': '⭐⭐⭐', '9-6': '⭐', '9-7': '⭐⭐', '9-8': '⭐⭐', '9-9': '⭐⭐⭐⭐⭐',
    }
    key = f'{moolank}-{bhagyank}'
    return ratings.get(key, '⭐⭐⭐')


def get_lucky_numbers(moolank, bhagyank):
    """Get common lucky numbers for both Moolank and Bhagyank"""
    lucky_map = {
        1: [2, 3, 5, 9],
        2: [1, 3, 5],
        3: [1, 2, 3, 5],
        4: [1, 6, 7],
        5: [1, 2, 3, 5, 6],
        6: [4, 5, 6, 7],
        7: [1, 4, 5, 6],
        8: [3, 5, 6],
        9: [1, 3, 5]
    }
    
    moolank_lucky = set(lucky_map.get(moolank, []))
    bhagyank_lucky = set(lucky_map.get(bhagyank, []))
    
    # Common lucky numbers
    common_lucky = sorted(list(moolank_lucky & bhagyank_lucky))
    return common_lucky


def get_enemy_numbers(moolank, bhagyank):
    """Get all enemy + hardcore enemy numbers for both"""
    # Enemy numbers mapping
    enemy_map = {
        1: [],
        2: [4, 9],
        3: [],
        4: [2, 4, 8, 9],
        5: [],
        6: [3],
        7: [],
        8: [1, 2, 4, 8],
        9: [2, 4]
    }
    
    # Hardcore enemy mapping
    hardcore_map = {
        1: [8],
        2: [8],
        3: [6],
        4: [],
        5: [],
        6: [3],
        7: [],
        8: [1, 2],
        9: []
    }
    
    moolank_enemies = set(enemy_map.get(moolank, []) + hardcore_map.get(moolank, []))
    bhagyank_enemies = set(enemy_map.get(bhagyank, []) + hardcore_map.get(bhagyank, []))
    
    # All common enemies
    common_enemies = sorted(list(moolank_enemies & bhagyank_enemies))
    return common_enemies


def generate_pdf(name, birth_date, personality_number, ln=True):
    """
    Generate complete Astro Number Report PDF
    
    Parameters:
    -----------
    name : str
        Person's name
    birth_date : str
        Birth date as "DD-MM-YYYY"
    personality_number : int
        Personality number (same as Bhagyank)
    ln : bool
        Language - True for Hindi, False for English
    
    Returns:
    --------
    bytes
        PDF file content as bytes
    """
    
    pdf = AstroPDF()
    pdf.add_page()
    
    # Parse birth date
    parts = birth_date.split('-')
    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])
    
    # Calculate Moolank and Bhagyank
    moolank = calculate_moolank(day)
    bhagyank = calculate_bhagyank(day, month, year)
    
    # Get star rating
    star_rating = get_star_rating(moolank, bhagyank)
    
    # ====================
    # PERSONAL INFORMATION
    # ====================
    if ln:
        pdf.section_title('Vyaktigat Jaankari (Personal Information)')
    else:
        pdf.section_title('Personal Information')
    
    info_text = f"""Name / Naam: {name}
Birth Date / Janm Tithi: {birth_date}
Moolank (Birth Number): {moolank}
Bhagyank (Destiny Number): {bhagyank}
Star Rating: {star_rating}
Report Date / Report Tarikh: {datetime.now().strftime('%d-%m-%Y %H:%M')}"""
    
    pdf.section_body(info_text)
    
    # ====================
    # LOSHU GRID (TABLE FORMAT)
    # ====================
    if ln:
        pdf.section_title('Lo Shu Grid (लो शू ग्रिड)')
    else:
        pdf.section_title('Lo Shu Grid')
    
    # Get all digits from DOB
    date_str = f"{day:02d}{month:02d}{year}"
    date_digits = [int(d) for d in date_str]
    
    # Add Moolank and Bhagyank to the grid digits
    all_digits = date_digits + [moolank, bhagyank]
    
    # Count occurrences
    digit_count = {}
    for digit in all_digits:
        if digit == 0:
            continue
        digit_count[digit] = digit_count.get(digit, 0) + 1
    
    # Loshu Grid structure
    loshu_grid = [
        [4, 9, 2],
        [3, 5, 7],
        [8, 1, 6]
    ]
    
    # Create table
    pdf.set_fill_color(230, 230, 250)
    pdf.set_line_width(0.3)
    
    cell_width = 60
    cell_height = 20
    
    # Draw grid with borders
    for row_idx, row in enumerate(loshu_grid):
        x_start = pdf.get_x()
        y_start = pdf.get_y()
        
        for col_idx, num in enumerate(row):
            # Determine cell content
            if num in digit_count:
                content = str(num) * digit_count[num]  # e.g., "22", "333"
            else:
                content = "-"
            
            # Draw cell border
            pdf.rect(x_start + (col_idx * cell_width), y_start, cell_width, cell_height)
            
            # Add text centered in cell
            pdf.set_xy(x_start + (col_idx * cell_width), y_start + 7)
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(cell_width, 6, content, 0, 0, 'C')
        
        pdf.ln(cell_height)
    
    pdf.ln(5)
    
    # Grid Analysis
    pdf.set_font('Arial', '', 11)
    
    present_numbers = sorted(list(digit_count.keys()))
    missing_numbers = [i for i in range(1, 10) if i not in digit_count]
    repeated_numbers = {k: v for k, v in digit_count.items() if v > 1}
    
    if ln:
        analysis = f"""Present Numbers / Upasthit Sankhya: {', '.join(map(str, present_numbers)) if present_numbers else 'Koi nahi'}

Missing Numbers / Kami Sankhya: {', '.join(map(str, missing_numbers)) if missing_numbers else 'Koi nahi'}"""
    else:
        analysis = f"""Present Numbers: {', '.join(map(str, present_numbers)) if present_numbers else 'None'}

Missing Numbers: {', '.join(map(str, missing_numbers)) if missing_numbers else 'None'}"""
    
    if repeated_numbers:
        rep_str = ', '.join([f"{k} ({v}x)" for k, v in sorted(repeated_numbers.items())])
        if ln:
            analysis += f"\n\nDohrai Sankhya / Repeated: {rep_str}"
        else:
            analysis += f"\n\nRepeated Numbers: {rep_str}"
    
    pdf.section_body(analysis)
    
    # ====================
    # LUCKY & UNLUCKY NUMBERS
    # ====================
    if ln:
        pdf.section_title('Bhagyashali Aur Abhagyashali Sankhya')
    else:
        pdf.section_title('Lucky & Unlucky Numbers')
    
    lucky_nums = get_lucky_numbers(moolank, bhagyank)
    unlucky_nums = get_enemy_numbers(moolank, bhagyank)
    
    if ln:
        numbers_text = f"""Lucky Numbers (Moolank {moolank} & Bhagyank {bhagyank} ke common friends):
{', '.join(map(str, lucky_nums)) if lucky_nums else 'Koi nahi'}

Unlucky Numbers (Dono ke common enemies):
{', '.join(map(str, unlucky_nums)) if unlucky_nums else 'Koi nahi'}"""
    else:
        numbers_text = f"""Lucky Numbers (Common friends of Moolank {moolank} & Bhagyank {bhagyank}):
{', '.join(map(str, lucky_nums)) if lucky_nums else 'None'}

Unlucky Numbers (Common enemies of both):
{', '.join(map(str, unlucky_nums)) if unlucky_nums else 'None'}"""
    
    pdf.section_body(numbers_text)
    
    # ====================
    # NUMBER MEANINGS
    # ====================
    number_meanings = {
        1: {
            'en': 'Number 1 represents leadership, independence, and new beginnings. Natural-born leader with strong willpower.',
            'hi': 'Sankhya 1 netritva, svatantrata aur nayi shuruaat ka pratinidhitva karti hai.'
        },
        2: {
            'en': 'Number 2 represents cooperation, balance, and diplomacy. Peacemaker who values harmony.',
            'hi': 'Sankhya 2 sahyog, santulan aur kootniti ka pratinidhitva karti hai.'
        },
        3: {
            'en': 'Number 3 represents creativity, self-expression, and communication. Naturally artistic and optimistic.',
            'hi': 'Sankhya 3 rachnatmakta, atma-abhivyakti aur sanchar ka pratinidhitva karti hai.'
        },
        4: {
            'en': 'Number 4 represents stability, hard work, and practicality. Dependable and organized.',
            'hi': 'Sankhya 4 sthirta, kadhi mehnat aur vyavaharikta ka pratinidhitva karti hai.'
        },
        5: {
            'en': 'Number 5 represents freedom, adventure, and versatility. Loves change and new experiences.',
            'hi': 'Sankhya 5 svatantrata, sahasik aur bahumukhi pratibha ka pratinidhitva karti hai.'
        },
        6: {
            'en': 'Number 6 represents harmony, family, and responsibility. Nurturing and caring.',
            'hi': 'Sankhya 6 samanjasy, parivar aur jimmedari ka pratinidhitva karti hai.'
        },
        7: {
            'en': 'Number 7 represents wisdom, spirituality, and introspection. Analytical and thoughtful.',
            'hi': 'Sankhya 7 gyan, adhyatmikta aur atma-nirikshan ka pratinidhitva karti hai.'
        },
        8: {
            'en': 'Number 8 represents power, ambition, and material success. Strong and determined.',
            'hi': 'Sankhya 8 shakti, mahatvakansha aur bhautik safalta ka pratinidhitva karti hai.'
        },
        9: {
            'en': 'Number 9 represents completion, humanitarianism, and wisdom. Compassionate and giving.',
            'hi': 'Sankhya 9 purnta, manavatavad aur vishwa-vyapi gyan ka pratinidhitva karti hai.'
        }
    }
    
    if ln:
        pdf.section_title('Bhagyank Ka Arth (Destiny Number Meaning)')
    else:
        pdf.section_title('Destiny Number Meaning')
    
    if bhagyank in number_meanings:
        meaning = number_meanings[bhagyank]['hi' if ln else 'en']
        pdf.section_body(meaning)
    
    # ====================
    # RECOMMENDATIONS
    # ====================
    if ln:
        pdf.section_title('Sifarishein (Recommendations)')
    else:
        pdf.section_title('Recommendations')
    
    recommendations = {
        'en': f"""Based on your Moolank ({moolank}) and Bhagyank ({bhagyank}):

1. Focus on your lucky numbers: {', '.join(map(str, lucky_nums)) if lucky_nums else 'consult numerologist'}
2. Avoid unlucky numbers: {', '.join(map(str, unlucky_nums)) if unlucky_nums else 'none identified'}
3. Work on developing missing numbers: {', '.join(map(str, missing_numbers[:3])) if missing_numbers else 'all present'}
4. Trust your natural strengths shown by your star rating: {star_rating}""",
        'hi': f"""Aapke Moolank ({moolank}) aur Bhagyank ({bhagyank}) ke aadhar par:

1. Apne bhagyashali sankhyaon par dhyan dein: {', '.join(map(str, lucky_nums)) if lucky_nums else 'ank-shashtri se paramarsh lein'}
2. Abhagyashali sankhyaon se bachen: {', '.join(map(str, unlucky_nums)) if unlucky_nums else 'koi nahi pehchani gayi'}
3. Kami sankhyaon ko viksit karne par kaam karein: {', '.join(map(str, missing_numbers[:3])) if missing_numbers else 'sabhi upasthit'}
4. Apne star rating dwara darshaye gaye prakritik shaktiyon par bharosa karein: {star_rating}"""
    }
    
    pdf.section_body(recommendations['hi' if ln else 'en'])
    
    # ====================
    # DISCLAIMER
    # ====================
    pdf.ln(5)
    pdf.set_font('Arial', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    
    disclaimer = {
        'en': 'Note: This report is based on numerological principles and should be used for guidance purposes only.',
        'hi': 'Dhyan Dein: Yah report ank-shastra ke siddhanton par aadharit hai aur ise margdarshan uddeshyon ke liye upyog kiya jana chahiye.'
    }
    
    pdf.multi_cell(0, 5, disclaimer['hi' if ln else 'en'], 0, 'C')
    
    # Return PDF as bytes
    return bytes(pdf.output())


# Test function
if __name__ == "__main__":
    # Test with Khem Raj example
    pdf_bytes = generate_pdf(
        name="Khem Raj",
        birth_date="12-02-1983",
        personality_number=8,
        ln=False
    )
    
    with open('test_complete_report.pdf', 'wb') as f:
        f.write(pdf_bytes)
    
    print("✓ Complete PDF generated successfully!")
