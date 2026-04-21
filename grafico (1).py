import pandas as pd
import matplotlib.pyplot as plt
import sqlite3 as sql
import os


# Conexão com o banco (igual você já fez antes)
caminho = os.path.join(os.path.dirname(__file__), 'bdsqlite.db')
conexao = sql.connect(caminho)

# Puxando dados do banco
query = """
SELECT 
    data_pagamento as data,
    valor_pago as valor,
    'Entrada' as tipo
FROM pagamento

UNION ALL

SELECT 
    data_pagamento as data,
    valor_pagar as valor,
    'Saída' as tipo
FROM colaboradores
"""

df = pd.read_sql_query(query, conexao)

# Fecha conexão
conexao.close()

# 2. TRANSFORMANDO EM SÉRIE TEMPORAL (O passo crucial)
df['data'] = pd.to_datetime(df['data'])
df.set_index('data', inplace=True)

# 3. LÓGICA FINANCEIRA
# Convertemos saídas em números negativos para o cálculo
df['valor_liquido'] = df.apply(lambda x: x['valor'] if x['tipo'] == 'Entrada' else -x['valor'], axis=1)

# Cálculo do Saldo Acumulado (Running Total)
df['saldo_acumulado'] = df['valor_liquido'].cumsum()

# 4. AGRUPAMENTO (Resampling)
# Vamos ver o saldo final de cada semana
resumo_semanal = df['valor_liquido'].resample('W').sum()

df = df.sort_index()

# 5. VISUALIZAÇÃO
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['saldo_acumulado'], label='Saldo Acumulado', color='blue', linewidth=2)
plt.axhline(0, color='red', linestyle='--', alpha=0.5) # Linha do "zero" (perigo)
plt.title('Evolução do Fluxo de Caixa - T1 2026')
plt.xlabel('Tempo')
plt.ylabel('Saldo em Conta (R$)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Exibir as primeiras linhas do resultado
print("--- Primeiras 5 Transações ---")
print(df.head())