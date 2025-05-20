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
('Joao Silva', '11111111111', 'joao@email.com', '123456'),
('Maria Souza', '22222222222', 'maria@email.com', 'abcdef'),
('Carlos Lima', '33333333333', 'carlos@email.com', '654321'),
('Ana Paula', '44444444444', 'ana@email.com', '1a2b3c'),
('Pedro Rocha', '55555555555', 'pedro@email.com', 'p12345'),
('Lucia Alves', '66666666666', 'lucia@email.com', '6x5y4z');

-- Inserções em Residuo
INSERT INTO Residuo (tipo, pontos_residuo) VALUES
('pequeno', 5),
('medio', 10),
('grande', 20),
('mouse', 30),
('teclado', 40),
('fone', 50);

-- Inserções em Descarte
INSERT INTO Descarte (data_hora, pontos_descarte, fk_usuario_id, fk_residuo_id) VALUES
(NOW(), 5, 1, 1),
(NOW(), 10, 2, 2),
(NOW(), 15, 3, 3),
(NOW(), 20, 4, 3),
(NOW(), 8, 5, 2),
(NOW(), 3, 6, 1);
