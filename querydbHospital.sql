use marmarasco07;
--potresti dover ricalcolare le pw
-- ============================================
-- DROP TABELLE (ORDINE CORRETTO)
-- ============================================
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS appuntamenti;
DROP TABLE IF EXISTS dottori;
DROP TABLE IF EXISTS pazienti;
DROP TABLE IF EXISTS admin;
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- TABELLA PAZIENTI
-- ============================================
CREATE TABLE pazienti (
    cf VARCHAR(16) PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    nascita DATE NOT NULL,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255)
);
--password: pass123
INSERT INTO pazienti (cf, nome, cognome, nascita, username, password) VALUES
('VRDLGI75A22H501P', 'Luigi', 'Verdelli', STR_TO_DATE('22/01/1975','%d/%m/%Y'), 'luigi75', 'scrypt:32768:8:1$S3chas4gwniZQot7$394145266eff4f32239998d5094c664cb90c2691b7127460e982cd7d146f70c37bce87ef18868e392487cef353220badd1c8ff8a49166d64f367adddb6493999'),
('SPNLRA81D09H501E', 'Lara', 'Spinelli', STR_TO_DATE('09/04/1981','%d/%m/%Y'), 'lara81', 'scrypt:32768:8:1$S3chas4gwniZQot7$394145266eff4f32239998d5094c664cb90c2691b7127460e982cd7d146f70c37bce87ef18868e392487cef353220badd1c8ff8a49166d64f367adddb6493999'),
('MNTRRT78E25H501S', 'Roberto', 'Monti', STR_TO_DATE('25/05/1978','%d/%m/%Y'), 'rob78', 'scrypt:32768:8:1$S3chas4gwniZQot7$394145266eff4f32239998d5094c664cb90c2691b7127460e982cd7d146f70c37bce87ef18868e392487cef353220badd1c8ff8a49166d64f367adddb6493999'),
('CNTMRA88C30H501R', 'Maria', 'Conti', STR_TO_DATE('30/03/1988','%d/%m/%Y'), 'maria88', 'scrypt:32768:8:1$S3chas4gwniZQot7$394145266eff4f32239998d5094c664cb90c2691b7127460e982cd7d146f70c37bce87ef18868e392487cef353220badd1c8ff8a49166d64f367adddb6493999'),
('FRRMNL92B14H501F', 'Manuela', 'Ferrari', STR_TO_DATE('14/02/1992','%d/%m/%Y'), 'manu92', 'scrypt:32768:8:1$S3chas4gwniZQot7$394145266eff4f32239998d5094c664cb90c2691b7127460e982cd7d146f70c37bce87ef18868e392487cef353220badd1c8ff8a49166d64f367adddb6493999'),
('RSSLNZ93F11H501G', 'Lorenzo', 'Rossi', STR_TO_DATE('11/06/1993','%d/%m/%Y'), 'lorenz93', 'scrypt:32768:8:1$S3chas4gwniZQot7$394145266eff4f32239998d5094c664cb90c2691b7127460e982cd7d146f70c37bce87ef18868e392487cef353220badd1c8ff8a49166d64f367adddb6493999'),
('BLTNNA99G05H501C', 'Anna', 'Bellucci', STR_TO_DATE('05/07/1999','%d/%m/%Y'), 'anna99', 'scrypt:32768:8:1$S3chas4gwniZQot7$394145266eff4f32239998d5094c664cb90c2691b7127460e982cd7d146f70c37bce87ef18868e392487cef353220badd1c8ff8a49166d64f367adddb6493999');

-- ============================================
-- TABELLA DOTTORI
-- ============================================
CREATE TABLE dottori (
    codice VARCHAR(10) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    specializzazione VARCHAR(50) NOT NULL,
    img VARCHAR(100),
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255)
);
--password: pass123
INSERT INTO dottori (codice, nome, specializzazione, img, username, password) VALUES
('DOC001', 'Dr. Marco Rossi', 'Cardiologia', 'Dott.Marco.jpg', 'marcorossi', 'scrypt:32768:8:1$S3chas4gwniZQot7$394145266eff4f32239998d5094c664cb90c2691b7127460e982cd7d146f70c37bce87ef18868e392487cef353220badd1c8ff8a49166d64f367adddb6493999'),
('DOC002', 'Dr.ssa Laura Bianchi', 'Pediatria', 'Dott.sa Laura.png', 'laurabianchi', 'scrypt:32768:8:1$S3chas4gwniZQot7$394145266eff4f32239998d5094c664cb90c2691b7127460e982cd7d146f70c37bce87ef18868e392487cef353220badd1c8ff8a49166d64f367adddb6493999');

-- ============================================
-- TABELLA APPUNTAMENTI
-- ============================================
CREATE TABLE appuntamenti (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codice_dottore VARCHAR(10),
    codice_fiscale VARCHAR(16),
    specializzazione VARCHAR(50),
    data DATE NOT NULL,
    ora TIME NOT NULL,
    FOREIGN KEY (codice_dottore) REFERENCES dottori(codice),
    FOREIGN KEY (codice_fiscale) REFERENCES pazienti(cf)
);

INSERT INTO appuntamenti (codice_dottore, specializzazione, codice_fiscale, data, ora) VALUES
('DOC001', 'Cardiologia', 'VRDLGI75A22H501P', STR_TO_DATE('12/11/2025','%d/%m/%Y'), '08:30'),
('DOC002', 'Pediatria', 'CNTMRA88C30H501R', STR_TO_DATE('12/11/2025','%d/%m/%Y'), '10:00'),
('DOC002', 'Pediatria', 'FRRMNL92B14H501F', STR_TO_DATE('13/11/2025','%d/%m/%Y'), '14:00'),
('DOC001', 'Cardiologia', 'SPNLRA81D09H501E', STR_TO_DATE('13/11/2025','%d/%m/%Y'), '16:00'),
('DOC001', 'Cardiologia', 'MNTRRT78E25H501S', STR_TO_DATE('14/11/2025','%d/%m/%Y'), '09:30'),
('DOC002', 'Pediatria', 'RSSLNZ93F11H501G', STR_TO_DATE('14/11/2025','%d/%m/%Y'), '11:15'),
('DOC002', 'Pediatria', 'BLTNNA99G05H501C', STR_TO_DATE('15/11/2025','%d/%m/%Y'), '15:45');

CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nome VARCHAR(50) NOT NULL
);
--passord: Admin1
INSERT INTO admin (username, password, nome) 
VALUES ('admin', 'scrypt:32768:8:1$f6mdzvHjnS4bPMYN$022257f0b180611ad6a93e4fefb6f7d53190a06af2018fedf623e6c9f74a0ba27e3823c98c35170e6c1e9424754987f9a653960e643697c1ad5014116c64f030', 'Amministratore');

COMMIT;
