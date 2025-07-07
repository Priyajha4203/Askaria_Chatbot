from fpdf import FPDF
from io import BytesIO
import datetime
import tempfile
import os

class ChatPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # No need to add external font

    def header(self):
        self.set_font('Helvetica', '', 12)
        
        # Use safe absolute path for logo
        logo_path = os.path.join(os.path.dirname(__file__), "logo", "acem_logo.png")
        if os.path.exists(logo_path):
            self.image(logo_path, x=10, y=8, w=25)
        
        self.ln(20)
        self.set_font("Helvetica", size=12)
        self.cell(0, 10, "AskAria - Chat Transcript", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_chat_message(self, role, time, message):
        self.set_font("Helvetica", size=11)
        role_name = "You" if role == "user" else "AskAria"
        if isinstance(time, datetime.datetime):
            time = time.strftime("%Y-%m-%d %H:%M")
        self.multi_cell(0, 10, f"{role_name} ({time}):\n{message}\n", border=0)
        self.ln(3)

def generate_pdf(chat_history):
    pdf = ChatPDF()
    pdf.add_page()

    for chat in chat_history:
        role = chat["role"]
        time = chat.get("timestamp", "")
        message = chat["message"].replace("\n", " ")
        pdf.add_chat_message(role, time, message)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        pdf.output(temp_file.name)
        with open(temp_file.name, "rb") as f:
            buffer = BytesIO(f.read())

    return buffer
