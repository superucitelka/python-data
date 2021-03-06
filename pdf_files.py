# P?ipojen? knihovny PyPDF2 pro pr?ci s PDF soubory - pou?it? modul? pro ?ten? a z?pis PDF soubor?
from PyPDF2 import PdfFileReader, PdfFileWriter
# Vygenerov?n? sloupcov?ho grafu
from pathlib import Path

# Na?ten? PDF souboru
pdf = PdfFileReader('data/valka-s-mloky.pdf')
# Vyp??e do konzole po?et str?nek
print(pdf.getNumPages())
# Vyp??e do konzole informaci o PDF dokumentu
print(pdf.documentInfo)
# Na?te druhou str?nku dokumentu
page = pdf.getPage(1)
# Vyp??e do konzoly prost? text z t?to str?nky
print(pdf.getPage(1).extractText())

# Vytvo?? objekt pro zapisov?n? do PDF souboru
pdf_writer = PdfFileWriter()
# P?iprav? novou str?nku v PDF
pdf_writer.addPage(page)
# Ulo?? str?nku do souboru novy.pdf
with Path('output/novy.pdf').open(mode='wb') as output_file:
     pdf_writer.write(output_file)

