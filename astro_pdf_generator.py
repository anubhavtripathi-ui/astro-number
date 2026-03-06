"""
Astro Number Report PDF Generator
Simple and working solution for Streamlit deployment
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


def generate_pdf(name, birth_date, personality_number, ln=True):
    """
    Generate Astro Number Report PDF
    
    Parameters:
    -----------
    name : str
        Person's name (use English/Roman script only)
    birth_date : str
        Birth date as string
    personality_number : int
        Personality number (0-9)
    ln : bool
        Language - True for Hindi (transliterated), False for English
    
    Returns:
    --------
    bytes
        PDF file content as bytes
    """
    
    pdf = AstroPDF()
    pdf.add_page()
    
    # ====================
    # PERSONAL INFORMATION
    # ====================
    if ln:
        pdf.section_title('Vyaktigat Jaankari (Personal Information)')
    else:
        pdf.section_title('Personal Information')
    
    info_text = f"""Name / Naam: {name}
Birth Date / Janm Tithi: {birth_date}
Personality Number / Vyaktitva Sankhya: {personality_number}
Report Date / Report Tarikh: {datetime.now().strftime('%d-%m-%Y %H:%M')}"""
    
    pdf.section_body(info_text)
    
    # ====================
    # NUMBER MEANINGS
    # ====================
    number_meanings = {
        0: {
            'en': 'Number 0 represents infinity, wholeness, and limitless potential. It amplifies the energies of numbers it appears with and signifies both nothing and everything - the beginning and the end.',
            'hi': 'Sankhya 0 anantata, purnata aur asimit sambhavna ka pratinidhitva karti hai. Yah un sankhyaon ki urja ko badhati hai jinke sath yah dikhai deti hai.'
        },
        1: {
            'en': 'Number 1 represents leadership, independence, and new beginnings. You are a natural-born leader with strong willpower and determination. You prefer to work independently and have pioneering spirit.',
            'hi': 'Sankhya 1 netritva, svatantrata aur nayi shuruaat ka pratinidhitva karti hai. Aap ek prakritik neta hain jo majboot ichchha shakti aur dridh nishchay rakhte hain.'
        },
        2: {
            'en': 'Number 2 represents cooperation, balance, and diplomacy. You are a peacemaker who values harmony and partnership. You excel in teamwork and have strong intuitive abilities.',
            'hi': 'Sankhya 2 sahyog, santulan aur kootniti ka pratinidhitva karti hai. Aap ek shanti-doot hain jo samrasta aur saath ko mahatva dete hain.'
        },
        3: {
            'en': 'Number 3 represents creativity, self-expression, and communication. You are naturally artistic, optimistic, and love to express yourself through various creative outlets.',
            'hi': 'Sankhya 3 rachnatmakta, atma-abhivyakti aur sanchar ka pratinidhitva karti hai. Aap prakritik roop se kalakar, aashavadi hain.'
        },
        4: {
            'en': 'Number 4 represents stability, hard work, and practicality. You are dependable, organized, and value security. You build strong foundations and are highly disciplined.',
            'hi': 'Sankhya 4 sthirta, kadhi mehnat aur vyavaharikta ka pratinidhitva karti hai. Aap bharosemand, vyavasthit hain aur suraksha ko mahatva dete hain.'
        },
        5: {
            'en': 'Number 5 represents freedom, adventure, and versatility. You love change, travel, and new experiences. You are adaptable and possess strong curiosity about life.',
            'hi': 'Sankhya 5 svatantrata, sahasik aur bahumukhi pratibha ka pratinidhitva karti hai. Aap parivartan, yatra aur naye anubhavon se pyar karte hain.'
        },
        6: {
            'en': 'Number 6 represents harmony, family, and responsibility. You are nurturing, caring, and have a strong sense of duty towards loved ones. You create peaceful environments.',
            'hi': 'Sankhya 6 samanjasy, parivar aur jimmedari ka pratinidhitva karti hai. Aap palan-poshan karne wale, dekhbhal karne wale hain.'
        },
        7: {
            'en': 'Number 7 represents wisdom, spirituality, and introspection. You are analytical, thoughtful, and seek deeper truths. You possess strong intuitive and mystical abilities.',
            'hi': 'Sankhya 7 gyan, adhyatmikta aur atma-nirikshan ka pratinidhitva karti hai. Aap vishleshanatmak, vichaarshil hain aur gehri satya ki khoj karte hain.'
        },
        8: {
            'en': 'Number 8 represents power, ambition, and material success. You are strong, determined, and have excellent business acumen. You understand material world and financial matters.',
            'hi': 'Sankhya 8 shakti, mahatvakansha aur bhautik safalta ka pratinidhitva karti hai. Aap majboot, dridh nishchayi hain aur uttam vyavasayik samajh rakhte hain.'
        },
        9: {
            'en': 'Number 9 represents completion, humanitarianism, and universal wisdom. You are compassionate, giving, and care deeply about making the world better. You possess old soul wisdom.',
            'hi': 'Sankhya 9 purnta, manavatavad aur vishwa-vyapi gyan ka pratinidhitva karti hai. Aap dayalu, dene wale hain aur duniya ko behtar banane ki gehri chinta rakhte hain.'
        }
    }
    
    if ln:
        pdf.section_title('Sankhya Ka Arth (Number Meaning)')
    else:
        pdf.section_title('Number Meaning')
    
    if personality_number in number_meanings:
        meaning = number_meanings[personality_number]['hi' if ln else 'en']
        pdf.section_body(meaning)
    else:
        pdf.section_body('Personality number should be between 0-9.')
    
    # ====================
    # KEY CHARACTERISTICS
    # ====================
    if ln:
        pdf.section_title('Mukhy Visheshtayen (Key Characteristics)')
    else:
        pdf.section_title('Key Characteristics')
    
    characteristics_text = {
        'en': """Your personality number reveals several key aspects:

- Core Strengths: Natural talents and abilities you possess
- Life Purpose: The path you are meant to follow
- Challenges: Areas that require conscious development
- Compatible Numbers: Numbers that harmonize well with yours
- Career Paths: Professions where you naturally excel
- Relationship Style: How you connect with others""",
        'hi': """Aapki vyaktitva sankhya kai mukhy pehluon ko pradarshit karti hai:

- Mukhy Shaktiyan: Prakritik pratibha aur kshamtayen jo aap rakhte hain
- Jeevan Uddeshya: Vah marg jise aapko follow karna chahiye
- Chunautiyan: Aise kshetra jinhe chetna-poorvak vikas ki zaroorat hai
- Sangat Sankhyayen: Aise sankhya jo aapke sath achhe se mel khati hain
- Vyavsay Marg: Vyavasay jahan aap prakritik roop se uttam hain
- Sambandh Shaili: Aap doosron se kaise jude hain"""
    }
    
    pdf.section_body(characteristics_text['hi' if ln else 'en'])
    
    # ====================
    # LUCKY ELEMENTS
    # ====================
    if ln:
        pdf.section_title('Bhagyashali Tatva (Lucky Elements)')
    else:
        pdf.section_title('Lucky Elements')
    
    lucky_elements = {
        0: {'color': 'White/Silver', 'day': 'Sunday', 'stone': 'Diamond'},
        1: {'color': 'Gold/Orange', 'day': 'Sunday', 'stone': 'Ruby'},
        2: {'color': 'White/Cream', 'day': 'Monday', 'stone': 'Pearl'},
        3: {'color': 'Yellow', 'day': 'Thursday', 'stone': 'Yellow Sapphire'},
        4: {'color': 'Blue/Grey', 'day': 'Saturday', 'stone': 'Blue Sapphire'},
        5: {'color': 'Green', 'day': 'Wednesday', 'stone': 'Emerald'},
        6: {'color': 'Pink/Blue', 'day': 'Friday', 'stone': 'Diamond'},
        7: {'color': 'Purple/Violet', 'day': 'Monday', 'stone': 'Cat\'s Eye'},
        8: {'color': 'Black/Dark Blue', 'day': 'Saturday', 'stone': 'Blue Sapphire'},
        9: {'color': 'Red/Maroon', 'day': 'Tuesday', 'stone': 'Red Coral'}
    }
    
    if personality_number in lucky_elements:
        elem = lucky_elements[personality_number]
        if ln:
            lucky_text = f"""Bhagyashali Rang / Lucky Color: {elem['color']}
Bhagyashali Din / Lucky Day: {elem['day']}
Bhagyashali Ratna / Lucky Stone: {elem['stone']}"""
        else:
            lucky_text = f"""Lucky Color: {elem['color']}
Lucky Day: {elem['day']}
Lucky Stone: {elem['stone']}"""
        pdf.section_body(lucky_text)
    
    # ====================
    # RECOMMENDATIONS
    # ====================
    if ln:
        pdf.section_title('Sifarishein (Recommendations)')
    else:
        pdf.section_title('Recommendations')
    
    recommendations = {
        'en': """Based on your personality number, here are personalized recommendations:

1. Personal Growth: Focus on developing your natural strengths while being mindful of potential challenges. Regular self-reflection will help you stay aligned with your life purpose.

2. Career Guidance: Choose professions that align with your core traits. Your number indicates specific fields where you will naturally excel and find fulfillment.

3. Relationships: Understanding your relationship style helps build stronger connections. Be aware of compatible numbers for harmonious partnerships.

4. Daily Practices: Incorporate your lucky color, day, and elements into daily life. Wearing your lucky stone may enhance positive energies.

5. Balance: Cultivate balance in all areas - work, relationships, health, and spirituality. Your number provides clues about areas needing more attention.

6. Intuition: Trust your inner guidance. Your personality number enhances certain intuitive abilities - learn to recognize and follow them.""",
        'hi': """Aapki vyaktitva sankhya ke aadhar par, yahan vyaktigat sifarishein hain:

1. Vyaktigat Vikas: Apni prakritik shaktiyon ko viksit karne par dhyan dein jabki sambhavit chunautiyon ke prati satark rahein. Niyamit atma-chintan aapko apne jeevan uddeshya ke sath sanjoe rakhne mein madad karega.

2. Vyavsay Margdarshan: Aise vyavasayon ka chayan karein jo aapke mukhy gunon ke sath mel khate hain. Aapki sankhya vishisht kshetron ko darshati hai jahan aap prakritik roop se uttam honge.

3. Sambandh: Apni sambandh shaili ko samajhna majboot jodne mein madad karta hai. Susamjasya-poorn saathi ke liye sangat sankhyaon ke baare mein jaan lein.

4. Dainik Abhyas: Apne bhagyashali rang, din aur tatvon ko dainik jeevan mein shamil karein. Apna bhagyashali ratna pahanana sakaratmak urja ko badha sakta hai.

5. Santulan: Sabhi kshetron mein santulan banayein - kaam, sambandh, swasthya aur adhyatmikta. Aapki sankhya un kshetron ke baare mein sanket deti hai jinhe adhik dhyan ki zaroorat hai.

6. Antargyan: Apni aantarik margdarshan par bharosa karein. Aapki vyaktitva sankhya kuch antargyani kshamtaon ko badhati hai - unhe pehchanna aur unka palan karna seekhein."""
    }
    
    pdf.section_body(recommendations['hi' if ln else 'en'])
    
    # ====================
    # DISCLAIMER
    # ====================
    pdf.ln(5)
    pdf.set_font('Arial', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    
    disclaimer = {
        'en': 'Note: This report is based on numerological principles and should be used for guidance and self-reflection purposes only.',
        'hi': 'Dhyan Dein: Yah report ank-shastra ke siddhanton par aadharit hai aur ise kevalmargdarshan aur atma-chintan uddeshyon ke liye upyog kiya jana chahiye.'
    }
    
    pdf.multi_cell(0, 5, disclaimer['hi' if ln else 'en'], 0, 'C')
    
    # Return PDF as bytes
    return pdf.output()


# Test function
if __name__ == "__main__":
    # Test the PDF generation
    pdf_bytes = generate_pdf(
        name="Rahul Sharma",
        birth_date="15-08-1990",
        personality_number=7,
        ln=False
    )
    
    # Save to file for testing
    with open('test_astro_report.pdf', 'wb') as f:
        f.write(pdf_bytes)
    
    print("✓ Test PDF generated successfully: test_astro_report.pdf")
