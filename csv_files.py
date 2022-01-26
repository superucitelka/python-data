# Připojí modul pandas pod aliasem pd (umožňuje import a export dat mezi různými datovými zdroji)
import pandas as pd
# Připojí modul json (práce s formátem JSON)
import json

# Načtení dat z CSV souboru do datových rámců (DataFrames)
# https://realpython.com/python-csv/
dfa = pd.read_csv('data/drinks.csv', index_col='country')
dfb = pd.read_csv('data/drinks.csv', index_col='total_litres_of_pure_alcohol')

# Export dat do excelovského souboru
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html
with pd.ExcelWriter('output/drinks.xlsx') as writer:
    # Vytvoření listu s názvem All obsahujícího uspořádaná data
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html#pandas.DataFrame.sort_values
    dfa.sort_values(by=['total_litres_of_pure_alcohol'], ascending=False).to_excel(writer, sheet_name='All')
    # Vytvoření listu s názvem Filter obsahující vybraná a seřazená data
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.filter.html
    dfb.filter(regex='^0\.0$', axis=0).sort_values(by=['country'], ascending=False).to_excel(writer, sheet_name='Filter')

# Převedení dat do formátu JSON
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html
#result = dfa.to_json(orient="index")
result = dfb.filter(regex='^0\.0$', axis=0).sort_values(by=['country'], ascending=False).to_json(orient='records')
# Parsování JSON dat a jejich zformátování s odsazením dvou mezer
parsed = json.loads(result)
json_str = json.dumps(parsed, indent=2)
# print(json_str)
# Uložení JSON dat do samostatného souboru
with open('output\drinks.json', 'w', encoding='utf8') as writer:
    writer.write(json_str)


# https://www.worldometers.info/