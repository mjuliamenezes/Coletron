# ♻️ COLETRON – Gerenciador de Descartes Sustentáveis
Este projeto é uma aplicação Python com interface via terminal, conectada a um banco de dados MySQL, que permite o gerenciamento de usuários, resíduos e descartes de forma sustentável.

## 📋 Pré-requisitos

- Docker
- Docker Compose
- Python 3.8+

## 🚀 Como Executar

O sistema pode ser executado em dois cenários:

### ✅ Cenário A: Aplicação Completa com Docker Compose

```bash
# 1. Construir as imagens
docker-compose build

# 2. Iniciar o banco de dados em segundo plano
docker-compose up -d db

# 3. Executar a aplicação
docker-compose run --rm app
```

### ✅ Cenário B: Apenas Banco de Dados

```bash
# 1. Construir a imagem do banco
docker build -t banco_mysql db/

# 2. Executar o container do banco
docker run -d --name banco_isolado -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=coletron -e MYSQL_USER=user -e MYSQL_PASSWORD=senha -p 3308:3306 banco_mysql

# 3. Acessar o MySQL
docker exec -it banco_isolado mysql -u user -p

# 4. Comandos úteis no MySQL
USE coletron;

SELECT * FROM Usuario;

INSERT INTO Residuo (tipo, pontos_residuo) VALUES ("pilha", 10);


# 5. Parar e remover o container (opcional)
docker stop banco_isolado
docker rm banco_isolado
```

<h3>Desenvolvedores:</h3>
<p><a href="https://github.com/igorfwds">Igor Wanderley</a> | Ifws@cesar.school</p>
<p><a href="https://github.com/JoaovfGoncalves">João Victor Ferraz</a> | jvfg@cesar.school</p>
<p><a href="https://github.com/mjuliamenezes">Maria Júlia Menezes</a> | mjotm@cesar.school</p>
<p><a href="https://github.com/Malucoimbr">Maria Luísa Coimbra</a> | mlcl@cesar.school</p>
<p><a href="https://github.com/LuizaCalife">Maria Luiza Calife</a> | mlcdf@cesar.school</p>
