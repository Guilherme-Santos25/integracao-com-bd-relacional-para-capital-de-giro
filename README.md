Fábrica de Dados: Real Creative Club (RCC)

## Sobre o Projeto
Este projeto é um **Gerador de Dados Relacionais (Mock Data Factory)** desenvolvido em Python. O objetivo principal é simular o ecossistema completo de uma produtora audiovisual (Real Creative Club), gerando um banco de dados estruturado do zero para fins de análise de dados, testes de estresse em relatórios financeiros e estudos de BI (Business Intelligence).

O script não apenas gera dados aleatórios, mas aplica **regras de negócio reais**, como:
- Variação cambial/descontos sobre o valor base de serviços (tabela de preços).
- Prazos de pagamento distintos para clientes (Entradas) e freelancers (Saídas) utilizando lógicas de deslocamento temporal (`timedelta`).
- Integridade referencial completa (Foreign Keys) amarrando Clientes -> Contratos -> Movimentações Financeiras e Equipe.

## Tecnologias Utilizadas
* **Python 3.x:** Linguagem base para a lógica e ETL.
* **SQLite3:** Banco de dados relacional leve e nativo.
* **Faker:** Biblioteca para geração de dados sensíveis fictícios (Nomes, Emails, Telefones).
* **Datetime / Timedelta:** Para simulação de fluxo de caixa no tempo (DRE e DFC).

## Estrutura do Banco de Dados
O script gera dinamicamente milhares de registros distribuídos em 5 tabelas principais:
1. `clientes`: Cadastro de clientes da produtora.
2. `servico`: Cardápio de serviços (ex: Edição, Direção, Captação) com valor base.
3. `contrato`: A "máquina do tempo" que amarra um Cliente a um Serviço em uma data específica.
4. `pagamento`: O fluxo de Entradas (Revenue), simulando pagamentos via PIX, Boleto, etc.
5. `colaboradores`: O fluxo de Saídas (Despesas), distribuindo o orçamento do projeto entre freelancers (Diretores, Gaffers, Editores, etc.).

## Como Executar
1. Clone este repositório.
2. Crie um ambiente virtual (recomendado): `python -m venv .venv`
3. Instale as dependências: `pip install faker`
4. Execute o script de geração: `python meu_gerador.py`
5. O arquivo `bdsqlite.db` será gerado automaticamente com todo o histórico financeiro populado e pronto para consumo via Pandas/Power BI.

## Próximos Passos
- [ ] Integração com `Pandas` para extração e tratamento dos dados gerados.
- [ ] Criação de painéis de análise financeira (Fluxo de Caixa Acumulado) utilizando `Matplotlib`/`Seaborn`.
- [ ] Modelagem preditiva para análise de Churn e MRR.
