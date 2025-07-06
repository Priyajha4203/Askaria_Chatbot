from fpdf import FPDF
from io import BytesIO
import datetime
import tempfile
import os

class ChatPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_dir, "fonts", "DejaVuSans.ttf")

        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found at: {font_path}")

        try:
            self.add_font('DejaVu', '', font_path, uni=True)
            self.set_font('DejaVu', '', 12)
        except Exception as e:
            raise RuntimeError(f"Error loading font: {e}")

    def header(self):
        self.set_font('DejaVu', '', 12)
        try:
            self.image("logo/acem_logo.png", x=10, y=8, w=25)
        except Exception:
            pass  # Skip image if not found
        self.ln(20)
        self.cell(0, 10, "AskAria - Chat Transcript", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_chat_message(self, role, time, message):
        self.set_font("DejaVu", size=11)
        role_name = "You" if role == "user" else "AskAria"
        if isinstance(time, datetime.datetime):
            time = time.strftime("%Y-%m-%d %H:%M")
        self.multi_cell(0, 10, f"{role_name} ({time}):\n{message}\n", border=0)
        self.ln(3)


def generate_pdf(chat_history):
    pdf = ChatPDF()
    pdf.add_page()

    for chat in chat_history:
        try:
            role = chat["role"]
            time = chat.get("timestamp", "")
            message = chat["message"].replace("\n", " ")
            pdf.add_chat_message(role, time, message)
        except Exception as e:
            print(f"Skipping chat due to error: {e}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        pdf.output(temp_file.name)
        with open(temp_file.name, "rb") as f:
            buffer = BytesIO(f.read())

    return buffer
