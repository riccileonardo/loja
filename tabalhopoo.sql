-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Tempo de geração: 23-Nov-2023 às 20:38
-- Versão do servidor: 8.0.31
-- versão do PHP: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `tabalhopoo`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `clientes`
--

DROP TABLE IF EXISTS `clientes`;
CREATE TABLE IF NOT EXISTS `clientes` (
  `IdCliente` int NOT NULL AUTO_INCREMENT,
  `NomCliente` varchar(100) NOT NULL,
  `cpf` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `telefone` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `idade` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`IdCliente`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Extraindo dados da tabela `clientes`
--

INSERT INTO `clientes` (`IdCliente`, `NomCliente`, `cpf`, `telefone`, `idade`) VALUES
(4, 'carlos roseros', '(66) 9 9955 4455', '123.123.123-58 ', '34'),
(3, 'corss', '898989898', '8598989898', '31'),
(5, 'rose', '123456', '061.254.973-18', '64'),
(6, 'marcos', '7897879', '98798798', '48'),
(7, 'carlos', '897979', '987987', '22'),
(8, 'carlos', '87979879', '12334', '28'),
(9, 'micael', '123654', '654987', '18'),
(10, 'marocos', '654', '987654', '18'),
(11, 'marco aurelio', '6699951020', '123', '22');

-- --------------------------------------------------------

--
-- Estrutura da tabela `estoque`
--

DROP TABLE IF EXISTS `estoque`;
CREATE TABLE IF NOT EXISTS `estoque` (
  `IdProduto` int NOT NULL AUTO_INCREMENT,
  `nomeProduto` varchar(100) NOT NULL,
  `quantidade` int NOT NULL,
  `valorCompra` float NOT NULL,
  `valorVenda` float NOT NULL,
  PRIMARY KEY (`IdProduto`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Extraindo dados da tabela `estoque`
--

INSERT INTO `estoque` (`IdProduto`, `nomeProduto`, `quantidade`, `valorCompra`, `valorVenda`) VALUES
(1, 'parafuso', 10, 50, 0),
(2, 'mangueira', 150, 1000, 0);

-- --------------------------------------------------------

--
-- Estrutura da tabela `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `IdUsuario` int NOT NULL AUTO_INCREMENT,
  `NomeUsuario` varchar(20) NOT NULL,
  `Senha` varchar(9) NOT NULL,
  PRIMARY KEY (`IdUsuario`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `venda`
--

DROP TABLE IF EXISTS `venda`;
CREATE TABLE IF NOT EXISTS `venda` (
  `IdVenda` int NOT NULL AUTO_INCREMENT,
  `nomeProduto` varchar(100) NOT NULL,
  `quantidade` int NOT NULL,
  `valorVenda` float NOT NULL,
  `cliente` varchar(100) NOT NULL,
  PRIMARY KEY (`IdVenda`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
