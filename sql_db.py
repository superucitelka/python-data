# Načtení modulu pandas a jeho registrace pod aliasem pd
# * https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
import pandas as pd
# Import metody create_engine z modulu SQLAlchemy
# * https://docs.sqlalchemy.org/en/14/core/engines.html#mysql
from sqlalchemy import create_engine
# Import pyplot z knihovny matplotlib pod aliasem plt
# * https://matplotlib.org/api/
import matplotlib.pyplot as plt

# Konfigurace a vytvoření SQL enginů
# Engine pro souborovou databázi SQLLite
# engine = create_engine('sqlite:///output/covid.sql', echo=False)
# Engine pro databázový systém MySQL / MariaDB
engine = create_engine('mysql+pymysql://root:@localhost/python?charset=utf8mb4', encoding='utf-8', echo=True)

# Dotaz odstraní tabulku stat, pokud už existuje
engine.execute("DROP TABLE IF EXISTS `stat`")

# Vytvoření datového rámce (DataFrame) z CSV souboru pomocí modulu pandas
dfa = pd.read_csv('data\covid.csv', encoding='utf-8')
# Migrace dat do SQL databáze podle připojeného enginu
dfa.to_sql('stat', con=engine)
# Ověření, zda databázová tabulka obsahuje potřebná data
print(engine.execute('SELECT * FROM stat').fetchall())

# Vytvoření datového rámce z databáze na základě SQL dotazu
dfb = pd.read_sql_query('SELECT location AS `Stát`, MAX(new_deaths) AS `Mrtví za den` FROM `stat` WHERE location NOT LIKE "World" GROUP BY location ORDER BY `Mrtví za den` DESC', con=engine)
# Export připravených dat (dfb) do excelovského souboru na list COVID-19
with pd.ExcelWriter('output/covid.xlsx') as writer:
    dfb.to_excel(writer, sheet_name='COVID-19')

# Vytvoření jiného datového rámce z databáze na základě SQL dotazu
dfc = pd.read_sql_query('SELECT location AS `Stát`, MAX(total_deaths)+0 AS `Mrtví celkem` FROM `stat` WHERE location NOT LIKE "World" AND total_deaths IS NOT NULL GROUP BY location ORDER BY `Mrtví celkem` DESC LIMIT 5', con=engine, index_col='Stát')
# Vygenerování výsečového ("koláčového") grafu
dfc.plot.pie(y='Mrtví celkem', figsize=(5, 5), autopct='%1.1f%%', startangle=90)
# Vykreslení grafu v okně
plt.show()

# Vytvoření dalšího datového formátu z databáze na základě SQL dotazu
dfd = pd.read_sql_query('SELECT location AS `Stát`, MAX(total_deaths)+0 AS `Mrtví celkem` FROM `stat` WHERE location NOT LIKE "World" AND total_deaths IS NOT NULL GROUP BY location ORDER BY `Mrtví celkem` DESC LIMIT 5', con=engine)
# Vygenerování sloupcového grafu
dfd.plot.bar(x='Stát', y='Mrtví celkem', figsize=(8, 8), rot='0', color=['red', 'green', 'blue', 'yellow', 'pink'],
             width=1)
# Uložení grafu do grafického souboru
plt.savefig('output/covid.png')



