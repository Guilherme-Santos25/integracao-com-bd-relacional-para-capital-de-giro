import os
import sqlite3 as sql

import matplotlib.pyplot as plt
import pandas as pd


def carregar_dados():
    caminho = os.path.join(os.path.dirname(__file__), 'bdsqlite.db')
    conexao = sql.connect(caminho)

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
        'Saida' as tipo
    FROM colaboradores
    """

    df = pd.read_sql_query(query, conexao)
    conexao.close()

    df['data'] = pd.to_datetime(df['data'])
    return df


def filtrar_dados_por_periodo(df, ano=None, mes=None):
    if ano is not None:
        df = df[df['data'].dt.year == ano]

    if mes is not None:
        df = df[df['data'].dt.month == mes]

    return df.copy()


def preparar_dados(df):
    if df.empty:
        return df

    df.set_index('data', inplace=True)
    df = df.sort_index()

    df['valor_liquido'] = df.apply(
        lambda x: x['valor'] if x['tipo'] == 'Entrada' else -x['valor'],
        axis=1
    )
    df['saldo_acumulado'] = df['valor_liquido'].cumsum()
    df['entrada'] = df.apply(lambda x: x['valor'] if x['tipo'] == 'Entrada' else 0, axis=1)
    df['saida'] = df.apply(lambda x: x['valor'] if x['tipo'] == 'Saida' else 0, axis=1)
    df['entrada_acumulada'] = df['entrada'].cumsum()
    df['saida_acumulada'] = df['saida'].cumsum()

    return df


def obter_periodos_disponiveis(df):
    periodos = (
        df['data']
        .dt.to_period('M')
        .drop_duplicates()
        .sort_values()
        .astype(str)
        .tolist()
    )
    return periodos


def configurar_grafico(grafico, titulo, rotulo_y):
    grafico.set_title(titulo)
    grafico.set_ylabel(rotulo_y)
    grafico.legend()
    grafico.grid(True, alpha=0.3)


def plotar_fluxo_liquido(df, grafico=None):
    if grafico is None:
        _, grafico = plt.subplots(figsize=(12, 6))
        grafico.set_xlabel('Tempo')

    grafico.plot(df.index, df['saldo_acumulado'], label='Saldo acumulado', color='blue', linewidth=2)
    grafico.axhline(0, color='red', linestyle='--', alpha=0.5)
    configurar_grafico(grafico, 'Evolucao do Fluxo de Caixa', 'Saldo em conta (R$)')


def plotar_entradas(df, grafico=None):
    if grafico is None:
        _, grafico = plt.subplots(figsize=(12, 6))
        grafico.set_xlabel('Tempo')

    grafico.plot(df.index, df['entrada_acumulada'], label='Entradas acumuladas', color='green', linewidth=2)
    configurar_grafico(grafico, 'Entradas de Caixa', 'Entradas (R$)')


def plotar_saidas(df, grafico=None):
    if grafico is None:
        _, grafico = plt.subplots(figsize=(12, 6))
        grafico.set_xlabel('Tempo')

    grafico.plot(df.index, df['saida_acumulada'], label='Saidas acumuladas', color='red', linewidth=2)
    configurar_grafico(grafico, 'Saidas de Caixa', 'Saidas (R$)')


def plotar_todos(df):
    _, graficos = plt.subplots(3, 1, figsize=(12, 12), sharex=True)

    plotar_fluxo_liquido(df, graficos[0])
    plotar_entradas(df, graficos[1])
    plotar_saidas(df, graficos[2])

    graficos[2].set_xlabel('Tempo')


def mostrar_menu():
    print("\nEscolha qual grafico voce quer ver:")
    print("1 - Fluxo de caixa liquido (entradas - saidas)")
    print("2 - Entradas de caixa")
    print("3 - Saidas de caixa")
    print("4 - Todos os 3 graficos")

    return input("Digite a opcao desejada: ").strip()


def escolher_periodo(df):
    periodos = obter_periodos_disponiveis(df)
    print("\nPeriodos disponiveis no banco:")
    print(", ".join(periodos))

    while True:
        mes_texto = input("Digite o mes (1 a 12): ").strip()
        ano_texto = input("Digite o ano (ex: 2025): ").strip()

        if not mes_texto.isdigit() or not ano_texto.isdigit():
            print("Mes e ano precisam ser numericos. Tente novamente.\n")
            continue

        mes = int(mes_texto)
        ano = int(ano_texto)

        if not 1 <= mes <= 12:
            print("Mes invalido. Digite um valor entre 1 e 12.\n")
            continue

        periodo_escolhido = f"{ano:04d}-{mes:02d}"
        if periodo_escolhido not in periodos:
            print("Nao ha movimentacoes para esse mes/ano. Escolha um dos periodos listados.\n")
            continue

        return ano, mes


def main():
    dados = carregar_dados()
    
    while True:
        opcao = mostrar_menu()

        if opcao == '1':
            df = preparar_dados(dados.copy())
            plotar_fluxo_liquido(df)
        elif opcao == '2':
            ano, mes = escolher_periodo(dados)
            df = preparar_dados(filtrar_dados_por_periodo(dados, ano=ano, mes=mes))
            plotar_entradas(df)
        elif opcao == '3':
            ano, mes = escolher_periodo(dados)
            df = preparar_dados(filtrar_dados_por_periodo(dados, ano=ano, mes=mes))
            plotar_saidas(df)
        elif opcao == '4':
            df = preparar_dados(dados.copy())
            plotar_todos(df)
        else:
            print("Opcao invalida. Rode o programa novamente e escolha uma opcao de 1 a 4.")
            return
        
        plt.tight_layout()
        plt.show()

        nova_analise = input("\nDeseja fazer uma nova analise? (s/n): ").strip().lower()
        if nova_analise != 's':
            print("Encerrando o programa. Obrigado!")
            break

if __name__ == '__main__':
    main()