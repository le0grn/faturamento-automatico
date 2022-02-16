import PySimpleGUI as sg
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
valores = text.split('\n')

hoje = format_datetime(datetime.today(), "'Data:' d 'de' MMMM 'de' Y", locale='pt_BR')

layout = [[sg.Text('Digite o mês inicial em número:')],
          [sg.InputText()],
          [sg.Text('Digite o ano inicial:')],
          [sg.InputText()],
          [sg.Checkbox('Inverso', key='inverso')],
          [sg.Submit(), sg.Cancel()]]

window = sg.Window('Faturamento Automático', layout)

event, values = window.read()
window.close()

if values['inverso']:
    valores.reverse()
    del valores[0]

mes_inicial = int(values[0])
ano_inicial = int(values[1])

inicio = datetime(ano_inicial, mes_inicial, 10)
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

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', size = 16)
pdf.cell(200,
         10, 
         txt = "DECLARAÇÃO DE FATURAMENTO", 
         ln = 1,
         align = 'C')
pdf.ln(7)
pdf.set_font('Arial', size = 12)
pdf.write(8, texto)
pdf.ln(15)
col_width = pdf.epw/2
line_height = pdf.font_size*2
for i in range(len(datas)):
    pdf.multi_cell(col_width, line_height, datas[i], border=1, ln=3)
    pdf.multi_cell(col_width, line_height, valores[i], border=1, ln=3)
    pdf.ln(line_height)
pdf.ln(15)
pdf.cell(200,
         10,
         txt = hoje + "\t",
         ln = 1,
         align = 'R') 
pdf.output("Declaração de Faturamento.pdf")
