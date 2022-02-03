DROP TABLE IF EXISTS artist;

DROP TABLE IF EXISTS track;

CREATE TABLE IF NOT EXISTS artist (
	id VARCHAR (22) PRIMARY KEY,
	name VARCHAR (50),
	popularity SMALLINT CHECK (popularity >= 0 AND popularity <= 100),
	genre VARCHAR (50),
	followers INTEGER,
  update TIMESTAMP
);

--COPY artist FROM '/var/postgres/RU.csv' WITH (FORMAT csv, HEADER True);
--DELETE FROM artist;

--SELECT * FROM artist;

CREATE TABLE IF NOT EXISTS track (
	id VARCHAR (22) PRIMARY KEY,
	name VARCHAR (50),
  artist_id VARCHAR (22),
	popularity SMALLINT CHECK (popularity >= 0 AND popularity <= 100),
  release_date TIMESTAMP,
  update TIMESTAMP,
  danceability FLOAT(3) CHECK (danceability >= 0.000 AND danceability <= 1.000),
  energy FLOAT(3) CHECK (energy >= 0.000 AND energy <= 1.000),
  key SMALLINT CHECK (key >= -1 AND key <= 11),
  loudness FLOAT(3) CHECK (loudness >= -60.000 AND loudness <= 0.000),
  mode BOOLEAN,
  speechiness FLOAT(3) CHECK (speechiness >= 0.000 AND speechiness <= 1.000),
  acousticness FLOAT(3) CHECK (acousticness >= 0.000 AND acousticness <= 1.000),
  instrumentalness FLOAT(3) CHECK (instrumentalness >= 0.000 AND instrumentalness <= 1.000),
  liveness FLOAT(3) CHECK (liveness >= 0.000 AND liveness <= 1.000),
  valence FLOAT(3) CHECK (valence >= 0.000 AND valence <= 1.000),
  tempo FLOAT(3) CHECK (tempo >= 0.000 AND tempo <= 1000.000),
  duration_ms INT CHECK (duration_ms > 0), 
  time_signature SMALLINT CHECK (time_signature >= 3 AND time_signature <= 7),
  CONSTRAINT fk_artist
  	FOREIGN KEY(artist_id) 
	  	REFERENCES artist(id)
); 
