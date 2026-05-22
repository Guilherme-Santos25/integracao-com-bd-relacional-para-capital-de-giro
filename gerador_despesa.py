import sqlite3 as sql
import random
import os
from faker import Faker

fake = Faker('pt_BR')

# Conectando ao banco
caminho = os.path.join(os.path.dirname(__file__), 'bdsqlite.db')
conexao = sql.connect(caminho)
cursor = conexao.cursor()

# ── Despesas Fixas ──
despesas_fixas = [
    ('Aluguel do estúdio',   3500.00, 'Infraestrutura'),
    ('Internet',              250.00, 'Infraestrutura'),
    ('Adobe Creative Cloud',  450.00, 'Software'),
    ('Energia elétrica',      800.00, 'Infraestrutura'),
    ('Contador',              900.00, 'Administrativo'),
]

for nome, valor, categoria in despesas_fixas:
    dia = random.randint(1, 28)
    vencimento = f"2025-{random.randint(1, 12):02d}-{dia:02d}"
    cursor.execute(
        "INSERT INTO despesa_fixa (nome_despesa, valor_mensal, dia_vencimento, categoria) VALUES (?,?,?,?)",
        (nome, valor, vencimento, categoria)
    )

print("Despesas fixas inseridas!")

# ── Despesas de Projeto ──
cursor.execute("SELECT id_contrato FROM contrato")
ids_contratos = [row[0] for row in cursor.fetchall()]

tipos_despesa = [
    'Locação de equipamento',
    'Transporte',
    'Alimentação da equipe',
    'Material de cenografia',
    'Locação de espaço',
    'Edição externa',
]

for id_contrato in ids_contratos:
    qtd = random.randint(0, 3)
    for _ in range(qtd):
        tipo = random.choice(tipos_despesa)
        valor = round(random.uniform(200, 2000), 2)
        data = fake.date_between(start_date='-1y', end_date='today')
        cursor.execute(
            "INSERT INTO despesa_projeto (id_contrato, tipo_despesa, valor_despesa, data_pagamento) VALUES (?,?,?,?)",
            (id_contrato, tipo, valor, data)
        )

print("Despesas de projeto inseridas!")

conexao.commit()
conexao.close()

print("Concluído! Tabelas despesa_fixa e despesa_projeto populadas.")