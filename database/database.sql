-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema univap
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema univap
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `univap` DEFAULT CHARACTER SET utf8 ;
USE `univap` ;

-- -----------------------------------------------------
-- Table `univap`.`disciplinas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `univap`.`disciplinas` (
  `codigodisc` INT NOT NULL,
  `nomedisc` VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY (`codigodisc`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `univap`.`professores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `univap`.`professores` (
  `registro` INT NOT NULL,
  `nomeprof` VARCHAR(50) NULL DEFAULT NULL,
  `telefoneprof` VARCHAR(30) NULL DEFAULT NULL,
  `idadeprof` INT NULL DEFAULT NULL,
  `salarioprof` FLOAT NULL DEFAULT NULL,
  PRIMARY KEY (`registro`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `univap`.`disciplinasxprofessores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `univap`.`disciplinasxprofessores` (
  `codigodisciplinanocurso` INT NOT NULL,
  `coddisciplina` INT NULL DEFAULT NULL,
  `codprofessor` INT NULL DEFAULT NULL,
  `curso` INT NULL DEFAULT NULL,
  `cargahoraria` INT NULL DEFAULT NULL,
  `anoletivo` INT NULL DEFAULT NULL,
  PRIMARY KEY (`codigodisciplinanocurso`),
  INDEX `fk_disciplina_idx` (`coddisciplina` ASC),
  INDEX `fk_professor_idx` (`codprofessor` ASC),
  CONSTRAINT `fk_disciplina`
    FOREIGN KEY (`coddisciplina`)
    REFERENCES `univap`.`disciplinas` (`codigodisc`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_professor`
    FOREIGN KEY (`codprofessor`)
    REFERENCES `univap`.`professores` (`registro`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
