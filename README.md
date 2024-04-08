# mysql-indexes-config
MySQL profiling
We have random birth_date from 1950-01-01 to 2000-12-31

## No index performance

Query: `SELECT SQL_NO_CACHE * FROM users WHERE birth_date = '1972-02-03';`

2129 rows in set, 1 warning (23.95 sec)  
2129 rows in set, 1 warning (23.18 sec)  
2129 rows in set, 1 warning (24.35 sec)

Query: `SELECT SQL_NO_CACHE * FROM users WHERE birth_date > '1990-01-01';`

8624519 rows in set, 1 warning (27.29 sec)

Query: `SELECT SQL_NO_CACHE * FROM users WHERE birth_date > '1972-02-03' AND birth_date <= '1973-02-03';`

785050 rows in set, 1 warning (27.39 sec)  
785050 rows in set, 1 warning (25.77 sec)  
785050 rows in set, 1 warning (24.65 sec)

## Index performance

CREATE INDEX idx_birth_date ON users (birth_date)

Query OK, 0 rows affected (1 min 12.80 sec)

Query: `SELECT SQL_NO_CACHE * FROM users WHERE birth_date = '1972-02-03';`

2129 rows in set, 1 warning (0.07 sec)  
2129 rows in set, 1 warning (0.01 sec)  
2129 rows in set, 1 warning (0.01 sec)

Query: `SELECT SQL_NO_CACHE * FROM users WHERE birth_date > '1990-01-01';`

8624519 rows in set, 1 warning (23.37 sec)  
8624519 rows in set, 1 warning (28.59 sec)  
8624519 rows in set, 1 warning (23.87 sec)

Query: `SELECT SQL_NO_CACHE count(id) FROM users WHERE birth_date > '1990-01-01';`

1 row in set, 1 warning (3.43 sec)  
1 row in set, 1 warning (2.89 sec)  
1 row in set, 1 warning (2.76 sec)

Query: `SELECT SQL_NO_CACHE * FROM users WHERE birth_date > '1972-02-03' AND birth_date <= '1973-02-03';`

785050 rows in set, 1 warning (7.55 sec)  
785050 rows in set, 1 warning (7.56 sec)  
785050 rows in set, 1 warning (8.78 sec)  
785050 rows in set, 1 warning (9.01 sec)  
785050 rows in set, 1 warning (8.23 sec)

## Hash index performance

Query: `CREATE INDEX idx_birth_date ON users (birth_date) USING HASH;`

Query OK, 0 rows affected, 1 warning (1 min 20.30 sec)

Query: `SELECT SQL_NO_CACHE * FROM users WHERE birth_date = '1972-02-03';`

2129 rows in set (0.01 sec)

Query: `SELECT SQL_NO_CACHE * FROM users WHERE birth_date > '1990-01-01';`

8624519 rows in set, 1 warning (27.42 sec)  
8624519 rows in set, 1 warning (21.11 sec)  
8624519 rows in set, 1 warning (20.11 sec)

Query: `SELECT SQL_NO_CACHE count(id) FROM users WHERE birth_date > '1990-01-01';`

1 row in set, 1 warning (3.20 sec)  
1 row in set, 1 warning (2.55 sec)  
1 row in set, 1 warning (3.00 sec)  

Query: `SELECT SQL_NO_CACHE * FROM users WHERE birth_date > '1972-02-03' AND birth_date <= '1973-02-03';`

785050 rows in set, 1 warning (29.46 sec)  
785050 rows in set, 1 warning (8.39 sec)  
785050 rows in set, 1 warning (9.20 sec)  

## InnoDB write performance
`docker-compose exec python python parallel_inserts.py` command with different configurations of `records_to_insert` variable value

## innodb_flush_log_at_trx_commit = 1

200 records with concurrency 50 - 4.63 seconds  
2000 records with concurrency 50 - 53.86 seconds

## innodb_flush_log_at_trx_commit = 2

200 records with concurrency 50 - 5.45 seconds  
2000 records with concurrency 50 - 58.47 seconds

## innodb_flush_log_at_trx_commit = 0

200 records with concurrency 50 - 5.38 seconds  
2000 records with concurrency 50 - 57.89 seconds
