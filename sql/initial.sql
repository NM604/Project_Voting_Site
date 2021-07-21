DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS poll CASCADE;
DROP TABLE IF EXISTS allpolls CASCADE;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  pass TEXT NOT NULL
  );
  
CREATE TABLE allpolls (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  oid INTEGER,
  cdate DATE,
  description TEXT,
  FOREIGN KEY (oid) references users(id) ON DELETE CASCADE
  );

CREATE TABLE poll (
  id SERIAL PRIMARY KEY,
  item TEXT NOT NULL,
  votes INTEGER,
  own INTEGER,
  description TEXT NOT NULL,
  pid INTEGER,
  FOREIGN KEY (pid) references allpolls(id) ON DELETE CASCADE,
  FOREIGN KEY (own) references users(id) ON DELETE CASCADE
  );
