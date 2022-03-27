import pandas as pd

df = pd.read_excel(
    io='vendas_supermercado.xlsx',
    engine='openpyxl',
    sheet_name='Vendas',
    usecols='B:R',
    nrows=1000,
)

print(df)