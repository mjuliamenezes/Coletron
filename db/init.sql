-- coletron_init.sql

DROP DATABASE IF EXISTS coletron;
CREATE DATABASE coletron;
USE coletron;

-- Tabela Usuario
CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    cpf VARCHAR(14) UNIQUE,
    email VARCHAR(100),
    senha VARCHAR(6),
    pontos_acum INT DEFAULT 0
);

-- Tabela Residuo
CREATE TABLE Residuo (
    id_residuo INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(20),
    pontos_residuo INT
);

-- Tabela Descarte
CREATE TABLE Descarte (
    id_descarte INT AUTO_INCREMENT PRIMARY KEY,
    data_hora DATETIME,
    pontos_descarte INT,
    fk_usuario_id INT,
    fk_residuo_id INT,
    FOREIGN KEY (fk_usuario_id) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (fk_residuo_id) REFERENCES Residuo(id_residuo)
);

-- Inserções em Usuario
INSERT INTO Usuario (nome, cpf, email, senha) VALUES
('João Silva', '111.111.111-11', 'joao@email.com', '123456'),
('Maria Souza', '222.222.222-22', 'maria@email.com', 'abcdef'),
('Carlos Lima', '333.333.333-33', 'carlos@email.com', '654321'),
('Ana Paula', '444.444.444-44', 'ana@email.com', '1a2b3c'),
('Pedro Rocha', '555.555.555-55', 'pedro@email.com', 'p12345'),
('Lúcia Alves', '666.666.666-66', 'lucia@email.com', '6x5y4z');

-- Inserções em Residuo
INSERT INTO Residuo (tipo, pontos_residuo) VALUES
('pequeno', 5),
('médio', 10),
('grande', 20),
('eletrônico', 15),
('orgânico', 3),
('reciclável', 8);

-- Inserções em Descarte
INSERT INTO Descarte (data_hora, pontos_descarte, fk_usuario_id, fk_residuo_id) VALUES
(NOW(), 5, 1, 1),
(NOW(), 10, 2, 2),
(NOW(), 15, 3, 4),
(NOW(), 20, 4, 3),
(NOW(), 8, 5, 6),
(NOW(), 3, 6, 5);
