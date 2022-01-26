# Připojení knihovny PyPDF2 pro práci s PDF soubory - použití modulu pro čtení a zápis PDF souboru
# * https://www.analyticsvidhya.com/blog/2021/09/pypdf2-library-for-working-with-pdf-files-in-python/
from PyPDF2 import PdfFileReader, PdfFileWriter
# Import třídy Path z modulu pathlib (umožňuje pracovat s cestami k souborům a složkám jako s objekty)
# * https://towardsdatascience.com/10-examples-to-master-python-pathlib-1249cc77de0b
from pathlib import Path


# Načtení PDF souboru
pdf = PdfFileReader('data/progit.pdf')
# Vypíše do konzole počet stránek
print(f'Počet stran: {pdf.getNumPages()}')
# Vypíše do konzole meta informace o PDF dokumentu
print(f'Autor: {pdf.documentInfo.author}')
print(f'Vytvořeno: {pdf.documentInfo.creator}')
# Načte druhou stránku dokumentu
page = pdf.getPage(333)
# Vypíše do konzole prostý text z této stránky
print(page.extractText())

# Vytvoří objekt pro zapisování do PDF souboru
pdf_writer = PdfFileWriter()
# Připraví novou stránku v PDF
pdf_writer.addPage(page)
# Uloží stránku do souboru novy.pdf
with Path('output/novy.pdf').open(mode='wb') as output_file:
     pdf_writer.write(output_file)

# Další zajímavé zdroje informací o práci s PDF v Pythonu:
# * Jak extrahovat data z nestrukturovaného PDF: https://www.analyticsvidhya.com/blog/2021/06/data-extraction-from-unstructured-pdfs/
# * Jak extrahovat data z tabulek v PDF: https://www.analyticsvidhya.com/blog/2020/08/how-to-extract-tabular-data-from-pdf-document-using-camelot-in-python/
