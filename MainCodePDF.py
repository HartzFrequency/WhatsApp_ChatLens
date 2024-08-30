import os
import base64
from fpdf import FPDF
from PIL import Image

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'WhatsApp Chat Log', ln=True, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_message(self, time, sender, message):
        self.set_font('Arial', '', 12)
        message = message.encode('latin-1', 'replace').decode('latin-1')  # Replace unsupported characters
        self.multi_cell(0, 10, f'[{time}] {sender}: {message}', align='L')
        self.ln(2)

    def add_image(self, img_path):
        try:
            img = Image.open(img_path)
            img_rgb_path = img_path.replace('.webp', '.png')  # Convert .webp to .png for PDF compatibility
            img.save(img_rgb_path, 'PNG')
            self.image(img_rgb_path, w=100)
            os.remove(img_rgb_path)  # Clean up the temporary image file
        except Exception as e:
            self.set_font('Arial', 'I', 10)
            error_message = f'[Error displaying image: {e}]'
            error_message = error_message.encode('latin-1', 'replace').decode('latin-1')
            self.multi_cell(0, 10, error_message, align='L')

def format_whatsapp_chat_to_pdf(input_folder='Input_dataWMedia', output_folder='Output2'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            output_pdf_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.pdf")
            
            pdf = PDF()
            pdf.add_page()
            
            with open(input_path, 'r', encoding='utf-8') as infile:
                previous_date = None
                previous_sender = None
                
                for line in infile:
                    try:
                        date_time_part, message_part = line.split(' - ', 1)
                        date_str, time_str = date_time_part.split(', ')
                        
                        if date_str != previous_date:
                            if previous_date is not None:
                                pdf.ln(10)  # Add space between dates
                            pdf.set_font('Arial', 'B', 12)
                            pdf.cell(0, 10, date_str, ln=True)
                            previous_date = date_str
                            previous_sender = None
                        
                        sender, message = message_part.split(': ', 1)
                        
                        if sender != previous_sender:
                            if previous_sender is not None:
                                pdf.ln(5)  # Add space between different senders
                            previous_sender = sender
                        
                        if message.endswith('.webp (file attached)'):
                            webp_filename = message.split(' (file attached)')[0]
                            webp_path = os.path.join(input_folder, webp_filename)
                            if os.path.exists(webp_path):
                                pdf.add_message(time_str, sender, "[Image attached below]")
                                pdf.add_image(webp_path)
                        else:
                            pdf.add_message(time_str, sender, message)
                    
                    except ValueError:
                        continue

            pdf.output(output_pdf_path)

# Run the function
format_whatsapp_chat_to_pdf()
