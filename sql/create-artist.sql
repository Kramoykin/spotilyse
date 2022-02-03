--CREATE TABLE IF NOT EXISTS artist (
--	id VARCHAR (22) PRIMARY KEY,
--	name VARCHAR (50),
--	popularity SMALLINT CHECK (popularity >= 0 AND popularity <= 100),
--	genre VARCHAR (50),
--	followers INTEGER,
--  update TIMESTAMP
--);

--COPY artist FROM '/var/postgres/RU.csv' WITH (FORMAT csv, HEADER True);

--SELECT * FROM artist; 
