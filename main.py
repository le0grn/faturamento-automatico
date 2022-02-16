from fpdf import FPDF
from datetime import datetime
from babel.dates import format_datetime
from dateutil.rrule import rrule, MONTHLY
import cv2
import pytesseract
from sys import platform
if platform == "linux":
    import os
    os.system(f"xclip -selection clipboard -target image/png -out > temp.png")
else:
    from PIL import ImageGrab
    ImageGrab.grabclipboard().save('temp.png', 'PNG')

img = cv2.imread('breakingnews.png')

text = pytesseract.image_to_string('temp.png')
print(text)

mes_inicial = 1
ano_inicial = 2021

inicio = datetime(ano_inicial, mes_inicial, 1)
datas = []

for dt in rrule(freq=MONTHLY, count=12, dtstart=inicio):
    datas.append(format_datetime(dt,'MMMM/Y' ,locale='pt_BR').capitalize())

print(datas)

nome = "Cristiane Homma"
cnpj = "00.000.000/0001-00"

texto = (
    "Declaração de Faturamento de " + nome + ""
    ", inscrito no CNPJ " + cnpj + " para o "
    "período de " + datas[0] + " a " + datas[-1]
)

print(texto)

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', size = 16)
pdf.cell(200,
         10, 
         txt = "DECLARAÇÃO DE FATURAMENTO", 
         ln = 1,
         align = 'C')

pdf.set_font('Arial', size = 14)
pdf.write(8, texto)

pdf.output("Declaração de Faturamento.pdf") 