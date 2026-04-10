create table clientes(
	id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
	nome varchar(100) not null,
	instagram varchar(100),
	telefone varchar (15) not null,
	email varchar(110)
);

create table despesa_fixa(
	id_despesa_fixa INTEGER primary key AUTOINCREMENT,
	nome_despesa varchar(100) not null,
	valor_mensal decimal(10,2) not null,
	dia_vencimento date not null,
	categoria varchar(50) not null
);

create table servico(
	id_servico INTEGER primary key AUTOINCREMENT,
	nome_servico varchar(100) not null,
	descricao_padrao varchar(100),
	valor_base decimal(10,2) not null
);

create table contrato(
	id_contrato INTEGER primary key AUTOINCREMENT,
	id_cliente int not null,
	id_servico int not null,
	data_contratacao date not null,
	
	constraint contrato_id_cliente_fk foreign key (id_cliente) references clientes(id_cliente), 
	constraint contrato_id_servico_fk foreign key (id_servico) references servico(id_servico)
);

create table colaboradores(
	id_colaborador INTEGER primary key AUTOINCREMENT,
	id_contrato INT not null,
	nome_colaborador varchar(100) not null,
	funcao varchar(100) not null,
	telefone varchar(100) not null,
	email varchar(100),
	valor_pagar decimal(10,2) not null,
	data_pagamento date not null,
	status_pagamento varchar(100) not null,
	
	constraint colaboradores_id_contrato_fk foreign key (id_contrato) references contrato(id_contrato)
);

create table pagamento(
	id_pagamento INTEGER primary key AUTOINCREMENT,
	id_contrato INT not null,
	valor_pago decimal(10,2) not null,
	data_pagamento date not null,
	forma_pagamento varchar(50) not null,
	status_pagamento varchar(50) not null,

	constraint pagamento_id_contrato_fk foreign key (id_contrato) references contrato(id_contrato)
);

create table despesa_projeto(
	id_despesa INTEGER primary key AUTOINCREMENT,
	id_contrato int not null,
	tipo_despesa varchar(100) not null,
	valor_despesa decimal(10,2) not null,
	data_pagamento date not null,

	constraint despesa_projeto_id_contrato_fk foreign key (id_contrato) references contrato(id_contrato) 
);

insert into servico (nome_servico, descricao_padrao, valor_base) values ('Equipe Criativa-Start', 'Plano-Start', '1200');
insert into servico (nome_servico, descricao_padrao, valor_base) values ('Equipe Criativa Pro', 'Plano Pro', '3500');
insert into servico (nome_servico, descricao_padrao, valor_base) values ('Equipe Criativa Estudio RCC', 'Plano Estudio', '8000');
insert into servico (nome_servico, descricao_padrao, valor_base) values ('Equipe Criativa Estudio Corporate', 'Plano Corporate', '12000');
insert into servico (nome_servico, descricao_padrao, valor_base) values ('Produçao de Conteúdo Start', 'Plano Start', '2000');
insert into servico (nome_servico, descricao_padrao, valor_base) values ('Produçao de Conteúdo Pro', 'Plano Pro', '4000');
insert into servico (nome_servico, descricao_padrao, valor_base) values ('Produçao de Conteúdo Premium', 'Plano Premium', '1000');
insert into servico (nome_servico, descricao_padrao, valor_base) values ('Videoclipe PUNK', 'Plano Punk', '3500');
insert into servico (nome_servico, descricao_padrao, valor_base) values ('Videoclipe SELECT', 'Plano Select', '7000');
insert into servico (nome_servico, descricao_padrao, valor_base) values ('Videoclipe REAL', 'Plano Real', '15000');
insert into servico (nome_servico, descricao_padrao, valor_base) values ('Filme Publicitário Short', 'Short', '30000');
insert into servico (nome_servico, descricao_padrao, valor_base) values ('Filme Publicitário Mid', 'Mid', '80000');
insert into servico (nome_servico, descricao_padrao, valor_base) values ('Filme Publicitário Long', 'Long', '300000');

select * from servico

insert into clientes (nome, instagram, telefone, email) values('Gapes', '@gapesz', '551998361-0390', 'hubnocap@gmail.com');

select * from clientes

insert into contrato(id_cliente, id_servico, data_contratacao) values(1,1,'2025-02-03')

select * from contrato

insert into pagamento(id_contrato, valor_pago, data_pagamento, forma_pagamento, status_pagamento) values(1,3500,'2025-02-05','PIX','Pago');

select * from pagamento