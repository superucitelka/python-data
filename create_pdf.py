# Import modulu pandas (analýza dat v tabulkách)
# * https://naucse.python.cz/lessons/intro/pandas/
# * https://pandas.pydata.org/
import pandas as pd
# Import modulu sqlalchemy
# * https://www.sqlalchemy.org/
# * https://www.tutorialspoint.com/sqlalchemy/index.htm
from sqlalchemy import create_engine
# Import modulů reportlab - PDF Library pro Python
# * https://www.reportlab.com/docs/reportlab-userguide.pdf
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, Table, TableStyle, Image, SimpleDocTemplate
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.units import cm

# Načtení dat z databáze pomocí pandas
# Vytvoření SQLite engine
# engine = create_engine('sqlite:///output/covid.sql', echo=False)
# Vytvoření MySQL / MariaDB engine
engine = create_engine('mysql+pymysql://root:@localhost/python?charset=utf8mb4', encoding='utf-8', echo=True)
# Vytvoření DataFrame pomocí Pandas z databázové tabulky s využitím seskupovacího dotazu
dfc = pd.read_sql_query('SELECT location AS `Stát`, MAX(total_deaths)+0 AS `Mrtví celkem` FROM `stat` WHERE location NOT LIKE "World" AND total_deaths IS NOT NULL GROUP BY location ORDER BY `Mrtví celkem` DESC LIMIT 5', con=engine, index_col='Stát')

# Příprava parametrů pro PDF výstup:
# Zaregistrování externího fontu TTF
pdfmetrics.registerFont(TTFont('Tahoma', 'data/tahoma.ttf', 'UTF-8'))
# Načtení předdefinovaných stylů pro PDF dokument
styles = getSampleStyleSheet()
# Vložení vlastních stylů - Normal_CENTER a New Style
styles.add(ParagraphStyle(name='Normal_CENTER',
                          parent=styles['Normal'],
                          fontName='Helvetica',
                          wordWrap='LTR',
                          alignment=TA_CENTER,
                          fontSize=12,
                          leading=13,
                          textColor=colors.black,
                          borderPadding=0,
                          leftIndent=0,
                          rightIndent=0,
                          spaceAfter=0,
                          spaceBefore=0,
                          splitLongWords=True,
                          spaceShrinkage=0.05,
                          ))

styles.add(ParagraphStyle(name='New Style',
                          alignment=TA_LEFT,
                          fontName='Helvetica',
                          fontSize=7,
                          textColor=colors.darkgray,
                          leading=8,
                          textTransform='uppercase',
                          wordWrap='LTR',
                          splitLongWords=True,
                          spaceShrinkage=0.05,
                          ))

# Proměnné odkazující na vybrané styly dokumentu
styleN = styles['Normal']
styleH2 = styles['Heading2']
styleH1 = styles['Heading1']
newStyle = styles['New Style']

# Úprava stylu nadpisu H1
styleH1.alignment = TA_CENTER
styleH1.textColor = colors.darkblue
styleH1.spaceAfter = 0.5*cm

# Úprava stylu nadpisu H2
styleH2.spaceBefore = 1*cm
styleH2.borderColor = colors.gray
styleH2.borderWidth = 0.01*cm
styleH2.backColor = colors.lightsteelblue
styleH2.borderPadding = 0.1*cm

# Vytvoření prázdného listu pro vkládání bloků PDF dokumentu
story = []

# Vložení odstavcového bloku - hlavní nadpis
story.append(Paragraph('Pandemie COVID-19', styleH1))

# Příprava záhlaví tabulky
data = [['Stát', 'Celkový počet mrtvých']]
# Načtení datové části tabulky ze získaných dat - dfc
for record in dfc.to_records():
    data.append(list(record))
# Vytvoření objektu tabulky a předání dat
table = Table(data)
# Nastavení stylu tabulky
table.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Tahoma', 12),
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                       ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                       ('ALIGN', (1, 1), (-1, -1), 'RIGHT')]))
# Připojení tabulky jako samostatného bloku do PDF dokumentu
story.append(table)

# Připojení samostatného bloku nadpisu H2 do PDF dokumentu
story.append(Paragraph(f'<para align="center"><font name="Tahoma"><b>Státy s nejvyšším počtem zemřelých</b></font></para>', styleH2))

# Příprava externího obrázku
image = Image('output/covid.png', width=10*cm, height=10*cm)
# Připojení samostatného bloku obrázku do PDF dokumentu
story.append(image)

# Vytvoření objektu nového dokumentu na základě jednoduché šablony - standardní velikost stránky (A4)
doc = SimpleDocTemplate('output/covid.pdf', pagesize = letter)
# Vložení připravených bloků do dokumentu PDF a jeho uložení
doc.build(story)