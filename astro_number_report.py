"""
Astro Number Report Generator with Unicode Support
This script generates PDF reports with proper support for Hindi/Devanagari characters
"""

from fpdf import FPDF
import os
from datetime import datetime

class UnicodeAstroPDF(FPDF):
    """Extended FPDF class with Unicode support"""
    
    def __init__(self):
        super().__init__()
        self.setup_unicode_fonts()
    
    def setup_unicode_fonts(self):
        """Setup Unicode fonts for Hindi/Devanagari text"""
        try:
            # Try to add a Unicode font that supports Devanagari
            # You may need to download and provide the font file path
            # For now, we'll use DejaVu Sans which supports many Unicode characters
            self.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
            self.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', uni=True)
            self.font_available = True
        except:
            # Fallback: use core fonts (won't support Hindi)
            self.font_available = False
            print("Warning: Unicode fonts not available. Hindi text may not display correctly.")
    
    def header(self):
        """PDF Header"""
        if self.font_available:
            self.set_font('DejaVu', 'B', 16)
        else:
            self.set_font('Arial', 'B', 16)
        
        self.set_text_color(70, 50, 150)
        self.cell(0, 10, 'Astro Number Report', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """PDF Footer"""
        self.set_y(-15)
        if self.font_available:
            self.set_font('DejaVu', '', 8)
        else:
            self.set_font('Arial', '', 8)
        
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title):
        """Add a chapter title"""
        if self.font_available:
            self.set_font('DejaVu', 'B', 14)
        else:
            self.set_font('Arial', 'B', 14)
        
        self.set_fill_color(230, 230, 250)
        self.set_text_color(50, 50, 100)
        self.cell(0, 10, title, 0, 1, 'L', True)
        self.ln(3)
    
    def chapter_body(self, body):
        """Add chapter body text"""
        if self.font_available:
            self.set_font('DejaVu', '', 11)
        else:
            self.set_font('Arial', '', 11)
        
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 7, body)
        self.ln()


def generate_astro_report(name, birth_date, personality_number, ln=True):
    """
    Generate an astrology number report PDF
    
    Args:
        name (str): Person's name
        birth_date (str): Birth date
        personality_number (int): Calculated personality/destiny number (0-9)
        ln (bool): Language - True for Hindi, False for English
    
    Returns:
        bytes: PDF file bytes
    """
    
    pdf = UnicodeAstroPDF()
    pdf.add_page()
    
    # Title Section
    pdf.chapter_title('Personal Information' if not ln else 'व्यक्तिगत जानकारी')
    
    info_text = f"""
Name / नाम: {name}
Birth Date / जन्म तिथि: {birth_date}
Personality Number / व्यक्तित्व संख्या: {personality_number}
Report Generated / रिपोर्ट जनरेट: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    pdf.chapter_body(info_text.strip())
    
    # Number Meanings
    number_meanings = {
        0: {
            'en': 'Number 0 represents infinity, wholeness, and new beginnings. It amplifies the energies of other numbers.',
            'hi': 'संख्या 0 अनंतता, पूर्णता और नई शुरुआत का प्रतिनिधित्व करती है।'
        },
        1: {
            'en': 'Number 1 represents leadership, independence, and new beginnings. You are a natural leader.',
            'hi': 'संख्या 1 नेतृत्व, स्वतंत्रता और नई शुरुआत का प्रतिनिधित्व करती है।'
        },
        2: {
            'en': 'Number 2 represents cooperation, balance, and diplomacy. You are a peacemaker.',
            'hi': 'संख्या 2 सहयोग, संतुलन और कूटनीति का प्रतिनिधित्व करती है।'
        },
        3: {
            'en': 'Number 3 represents creativity, self-expression, and communication. You are artistic and expressive.',
            'hi': 'संख्या 3 रचनात्मकता, आत्म-अभिव्यक्ति और संचार का प्रतिनिधित्व करती है।'
        },
        4: {
            'en': 'Number 4 represents stability, hard work, and practicality. You are dependable and organized.',
            'hi': 'संख्या 4 स्थिरता, कड़ी मेहनत और व्यावहारिकता का प्रतिनिधित्व करती है।'
        },
        5: {
            'en': 'Number 5 represents freedom, adventure, and versatility. You love change and new experiences.',
            'hi': 'संख्या 5 स्वतंत्रता, साहसिक और बहुमुखी प्रतिभा का प्रतिनिधित्व करती है।'
        },
        6: {
            'en': 'Number 6 represents harmony, family, and responsibility. You are nurturing and caring.',
            'hi': 'संख्या 6 सामंजस्य, परिवार और जिम्मेदारी का प्रतिनिधित्व करती है।'
        },
        7: {
            'en': 'Number 7 represents wisdom, spirituality, and introspection. You are analytical and thoughtful.',
            'hi': 'संख्या 7 ज्ञान, आध्यात्मिकता और आत्मनिरीक्षण का प्रतिनिधित्व करती है।'
        },
        8: {
            'en': 'Number 8 represents power, ambition, and material success. You are strong and determined.',
            'hi': 'संख्या 8 शक्ति, महत्वाकांक्षा और भौतिक सफलता का प्रतिनिधित्व करती है।'
        },
        9: {
            'en': 'Number 9 represents completion, humanitarianism, and wisdom. You are compassionate and giving.',
            'hi': 'संख्या 9 पूर्णता, मानवतावाद और ज्ञान का प्रतिनिधित्व करती है।'
        }
    }
    
    # Add meaning section
    pdf.chapter_title('Number Meaning' if not ln else 'संख्या का अर्थ')
    
    if personality_number in number_meanings:
        meaning = number_meanings[personality_number]['hi' if ln else 'en']
        pdf.chapter_body(meaning)
    
    # Characteristics
    pdf.chapter_title('Key Characteristics' if not ln else 'मुख्य विशेषताएं')
    
    characteristics = f"""
• {'Positive traits associated with your number' if not ln else 'आपकी संख्या से जुड़े सकारात्मक गुण'}
• {'Areas of natural talent and ability' if not ln else 'प्राकृतिक प्रतिभा और क्षमता के क्षेत्र'}
• {'Life path guidance' if not ln else 'जीवन पथ मार्गदर्शन'}
• {'Compatible numbers' if not ln else 'संगत संख्याएं'}
"""
    pdf.chapter_body(characteristics.strip())
    
    # Recommendations
    pdf.chapter_title('Recommendations' if not ln else 'सिफारिशें')
    
    recommendations = f"""
{'Based on your personality number, here are some recommendations:' if not ln else 'आपकी व्यक्तित्व संख्या के आधार पर, यहां कुछ सिफारिशें हैं:'}

• {'Focus on your natural strengths' if not ln else 'अपनी प्राकृतिक शक्तियों पर ध्यान दें'}
• {'Be aware of potential challenges' if not ln else 'संभावित चुनौतियों के बारे में जागरूक रहें'}
• {'Cultivate balance in all areas of life' if not ln else 'जीवन के सभी क्षेत्रों में संतुलन बनाएं'}
• {'Trust your intuition' if not ln else 'अपनी अंतर्ज्ञान पर भरोसा करें'}
"""
    pdf.chapter_body(recommendations.strip())
    
    # Return PDF as bytes
    return pdf.output(dest='S').encode('latin-1')


def save_report_to_file(pdf_bytes, filename='astro_report.pdf'):
    """
    Save PDF bytes to a file
    
    Args:
        pdf_bytes (bytes): PDF content
        filename (str): Output filename
    """
    with open(filename, 'wb') as f:
        f.write(pdf_bytes)
    print(f"Report saved to: {filename}")


# Example usage
if __name__ == "__main__":
    # Example 1: Generate report in Hindi
    pdf_content = generate_astro_report(
        name="राहुल शर्मा",
        birth_date="15-08-1990",
        personality_number=7,
        ln=True
    )
    save_report_to_file(pdf_content, 'astro_report_hindi.pdf')
    
    # Example 2: Generate report in English
    pdf_content = generate_astro_report(
        name="Rahul Sharma",
        birth_date="15-08-1990",
        personality_number=7,
        ln=False
    )
    save_report_to_file(pdf_content, 'astro_report_english.pdf')
    
    print("\nReports generated successfully!")
    print("\nTo use this script in your Streamlit app, call:")
    print("pdf_bytes = generate_astro_report(name, birth_date, personality_number, ln=True)")
