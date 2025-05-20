# ♻️ COLETRON – Gerenciador de Descartes Sustentáveis

Este projeto é uma aplicação Python com interface via terminal, conectada a um banco de dados MySQL, que permite o gerenciamento de usuários, resíduos e descartes.

O sistema está preparado para rodar em dois cenários com Docker:

- ✅ **Cenário A**: Executar a aplicação completa com `docker-compose`
- ✅ **Cenário B**: Rodar apenas o container do banco de dados e realizar operações SQL diretamente

Cenário A:

para rodar o coletron em python

docker-compose build

docker-compose up -d db    

docker-compose run --rm app


Cenário B:

# 1. Construir a imagem do banco
docker build -t banco_mysql db/

# 2. Rodar o container do banco isoladamente
docker run -d --name banco_isolado -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=coletron -e MYSQL_USER=user -e MYSQL_PASSWORD=senha -p 3308:3306 banco_mysql

# 3. Acessar o MySQL no terminal
docker exec -it banco_isolado mysql -u user -p

# 4. digite a senha do banco

# 5. Dentro do MySQL:
USE coletron;
SELECT * FROM Usuario;

# 5. Encerrar (opcional):
docker stop banco_isolado
docker rm banco_isolado