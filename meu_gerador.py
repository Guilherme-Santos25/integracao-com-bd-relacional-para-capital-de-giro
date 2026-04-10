#importando as ferramentas/bibliotecas utilizadas para criar o gerador de clientes
import sqlite3 as sql #Para conseguirmos utilizar os arquivos tipo .db
import random #para gerarmos dados aleatorios
from faker import Faker #Para criarmos dados falsos
from datetime import timedelta #aqui estamos importando uma ferramenta que nos permite somar dias em uma data

# inicializa o gerador de dados falsos com em português
fake = Faker('pt_BR')

# Conectando com o banco de dados
conexao = sql.connect('bdsqlite.db') # fazendo a conexão com o banco de dados utilizando o "Connect()" e alocando em uma váriavel chamada "Conexão"
cursor = conexao.cursor() # o cursor é oq faz mudarmos para o bd dentro do python, entao sempre que chamarmos essa variável, estaremos dentro do bd

#Utilizando o faker para criar dados falsos para 50 clientes
for _ in range(50):
    nome_falso = fake.name()
    insta_falso = f"@{fake.user_name()}"
    tel_falso = fake.phone_number()
    email_falso = fake.email()
    cursor.execute("INSERT INTO clientes (nome, instagram, telefone, email) VALUES (?,?,?,?)", (nome_falso, insta_falso, tel_falso, email_falso)) 

#criando novos contratos dentro do bd
for _ in range(200):
    id_cli = random.randint(1,51) #sortando os clientes dentro do bd de 1 - 51, pq ja tinhamos 1 cliente cadastrado.
    id_serv = random.randint(1,13) #sorteando um dos 13 serviços criados dentro do bd.
    cursor.execute("SELECT valor_base FROM servico WHERE id_servico = ?", (id_serv,))
    resultado = cursor.fetchone()
    valor_tabela = resultado[0]
    valor_recebido = round(valor_tabela * random.uniform(0.9, 1.2), 2)
    data_contrato = fake.date_between(start_date='-1y', end_date='today')

    # execultando o insert dos contrato e pegando o id gerado dentro do bd
    cursor.execute("INSERT INTO contrato (id_cliente, id_servico, data_contratacao) VALUES (?,?,?)", (id_cli, id_serv, data_contrato))
    id_contrato_gerado = cursor.lastrowid #pegando qual o id do ultimo contrato gerado
    data_pagto_cliente = data_contrato + timedelta(days=random.randint(0,15)) #aqui estamos criando datas de pagamento aleatórias entre 0 a 15 dias
    forma_pagto = random.choice(['PIX','Boleto', 'Tranferência']) #criando uma lista com as formmas de pagamento e randomizando elas de acordo com o produto
    cursor.execute("INSERT INTO pagamento (id_contrato, valor_pago, data_pagamento, forma_pagamento, status_pagamento) VALUES (?,?,?,?,?)", (id_contrato_gerado, valor_recebido, data_pagto_cliente, forma_pagto, 'Pago'))
    for _ in range(random.randint(1, 4)): #laço para criamos os pagamentos para freelancers
        valor_freela = round(random.uniform(500, 4000), 2) #sorteando um valor aleatorio para freelance de 500 a 4000
        data_pagto_equipe = data_contrato + timedelta(days=random.randint(15, 45)) #sorteando uma data aleatoria de pagamento para a equipe de 15 a 45 dias
        funcao_freela = random.choice(['Produtor Executivo','Assistente de Direção (AD)', 'Assistente de Produção', 'Diretor de Fotografia (DOP)', 'Operador de Câmera', 'Gaffer', 'Editor', 'Motion Designer', 'Maquiador(a)', 'Figurinista', 'Diretor de Arte'])
        cursor.execute("INSERT INTO colaboradores (id_contrato, nome_colaborador, funcao, telefone, email, valor_pagar, data_pagamento, status_pagamento) VALUES (?,?,?,?,?,?,?,?)", (id_contrato_gerado, fake.name(), funcao_freela, fake.phone_number(), fake.email(), valor_freela, data_pagto_equipe,'Pago'))
#Salvando o banco de dados
conexao.commit() 

#fechando o banco de dados
conexao.close()

print('Fabrica de dados concluída!')