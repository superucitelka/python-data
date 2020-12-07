# Pøipojení knihovny PyPDF2 pro práci s PDF soubory - použití modulù pro ètení a zápis PDF souborù
from PyPDF2 import PdfFileReader, PdfFileWriter
# Vygenerování sloupcového grafu
from pathlib import Path

# Naètení PDF souboru
pdf = PdfFileReader('data/valka-s-mloky.pdf')
# Vypíše do konzole poèet stránek
print(pdf.getNumPages())
# Vypíše do konzole informaci o PDF dokumentu
print(pdf.documentInfo)
# Naète druhou stránku dokumentu
page = pdf.getPage(1)
# Vypíše do konzoly prostý text z této stránky
print(pdf.getPage(1).extractText())

# Vytvoøí objekt pro zapisování do PDF souboru
pdf_writer = PdfFileWriter()
# Pøipraví novou stránku v PDF
pdf_writer.addPage(page)
# Uloží stránku do souboru novy.pdf
with Path('output/novy.pdf').open(mode='wb') as output_file:
     pdf_writer.write(output_file)

