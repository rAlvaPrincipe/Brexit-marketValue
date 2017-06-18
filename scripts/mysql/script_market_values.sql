USE experiments;

-- create table that will contain all the tweets
CREATE TABLE IF NOT EXISTS tweets (id_tweet bigint, tweet varchar(200), id_source bigint, tweet_date date);


-- Week2
-- alter table
ALTER TABLE brexit_text_w2 ADD tweet_date DATE;

-- 5dec
CREATE TEMPORARY TABLE IF NOT EXISTS 5dec AS (SELECT * FROM brexit_text_w2 ORDER BY id_tweet LIMIT 0,136155);
UPDATE 5dec SET tweet_date = '2016/12/05';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 5dec;
DROP TABLE 5dec;

-- 6dec
CREATE TEMPORARY TABLE IF NOT EXISTS 6dec AS (SELECT * FROM brexit_text_w2 ORDER BY id_tweet LIMIT 136155, 136155);
UPDATE 6dec SET tweet_date = '2016/12/06';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 6dec;
DROP TABLE 6dec;

-- 7dec
CREATE TEMPORARY TABLE IF NOT EXISTS 7dec AS (SELECT * FROM brexit_text_w2 ORDER BY id_tweet LIMIT 272310, 136155);
UPDATE 7dec SET tweet_date = '2016/12/07';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 7dec;
DROP TABLE 7dec;

-- 8dec
CREATE TEMPORARY TABLE IF NOT EXISTS 8dec AS (SELECT * FROM brexit_text_w2 ORDER BY id_tweet LIMIT 408466, 136155);
UPDATE 8dec SET tweet_date = '2016/12/08';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 8dec;
DROP TABLE 8dec;

-- 9dec
CREATE TEMPORARY TABLE IF NOT EXISTS 9dec AS (SELECT * FROM brexit_text_w2 ORDER BY id_tweet LIMIT 544621, 136159);
UPDATE 9dec SET tweet_date = '2016/12/09';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 9dec;
DROP TABLE 9dec;
-- /Week2 ---


-- Week3 ---
-- alter table
ALTER TABLE brexit_text_w3 ADD tweet_date DATE;

-- 12dec
CREATE TEMPORARY TABLE IF NOT EXISTS 12dec AS (SELECT * FROM brexit_text_w3 ORDER BY id_tweet LIMIT 0,100979);
UPDATE 12dec SET tweet_date = '2016/12/12';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 12dec;
DROP TABLE 12dec;

-- 13dec
CREATE TEMPORARY TABLE IF NOT EXISTS 13dec AS (SELECT * FROM brexit_text_w3 ORDER BY id_tweet LIMIT 100979, 100979);
UPDATE 13dec SET tweet_date = '2016/12/13';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 13dec;
DROP TABLE 13dec;

-- 14dec
CREATE TEMPORARY TABLE IF NOT EXISTS 14dec AS (SELECT * FROM brexit_text_w3 ORDER BY id_tweet LIMIT 201958, 100979);
UPDATE 14dec SET tweet_date = '2016/12/14';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 14dec;
DROP TABLE 14dec;

-- 15dec
CREATE TEMPORARY TABLE IF NOT EXISTS 15dec AS (SELECT * FROM brexit_text_w3 ORDER BY id_tweet LIMIT 302937, 100979);
UPDATE 15dec SET tweet_date = '2016/12/15';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 15dec;
DROP TABLE 15dec;

-- 16dec
CREATE TEMPORARY TABLE IF NOT EXISTS 16dec AS (SELECT * FROM brexit_text_w3 ORDER BY id_tweet LIMIT 403916, 100980);
UPDATE 16dec SET tweet_date = '2016/12/16';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 16dec;
DROP TABLE 16dec;

-- /Week3 ---


-- Week4 ---
-- alter table
ALTER TABLE brexit_text_w4 ADD tweet_date DATE;

-- 19dec
CREATE TEMPORARY TABLE IF NOT EXISTS 19dec AS (SELECT * FROM brexit_text_w4 ORDER BY id_tweet LIMIT 0,73212);
UPDATE 19dec SET tweet_date = '2016/12/19';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 19dec;
DROP TABLE 19dec;

-- 20dec
CREATE TEMPORARY TABLE IF NOT EXISTS 20dec AS (SELECT * FROM brexit_text_w4 ORDER BY id_tweet LIMIT 73212, 73212);
UPDATE 20dec SET tweet_date = '2016/12/20';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 20dec;
DROP TABLE 20dec;

-- 21dec
CREATE TEMPORARY TABLE IF NOT EXISTS 21dec AS (SELECT * FROM brexit_text_w4 ORDER BY id_tweet LIMIT 146424, 73212);
UPDATE 21dec SET tweet_date = '2016/12/21';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 21dec;
DROP TABLE 21dec;

-- 22dec
CREATE TEMPORARY TABLE IF NOT EXISTS 22dec AS (SELECT * FROM brexit_text_w4 ORDER BY id_tweet LIMIT 219636, 73212);
UPDATE 22dec SET tweet_date = '2016/12/22';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 22dec;
DROP TABLE 22dec;

-- 23dec
CREATE TEMPORARY TABLE IF NOT EXISTS 23dec AS (SELECT * FROM brexit_text_w4 ORDER BY id_tweet LIMIT 292848, 73216);
UPDATE 23dec SET tweet_date = '2016/12/23';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 23dec;
DROP TABLE 23dec;
-- /Week4 ---


-- Week5 ---
-- alter table
ALTER TABLE brexit_text_w5 ADD tweet_date DATE;

-- 27dec
CREATE TEMPORARY TABLE IF NOT EXISTS 27dec AS (SELECT * FROM brexit_text_w5 ORDER BY id_tweet LIMIT 0,90091);
UPDATE 27dec SET tweet_date = '2016/12/27';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 27dec;
DROP TABLE 27dec;

-- 28dec
CREATE TEMPORARY TABLE IF NOT EXISTS 28dec AS (SELECT * FROM brexit_text_w5 ORDER BY id_tweet LIMIT 90091, 90091);
UPDATE 28dec SET tweet_date = '2016/12/28';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 28dec;
DROP TABLE 28dec;

-- 29dec
CREATE TEMPORARY TABLE IF NOT EXISTS 29dec AS (SELECT * FROM brexit_text_w5 ORDER BY id_tweet LIMIT 180182, 90091);
UPDATE 29dec SET tweet_date = '2016/12/29';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 29dec;
DROP TABLE 29dec;

-- 30dec
CREATE TEMPORARY TABLE IF NOT EXISTS 30dec AS (SELECT * FROM brexit_text_w5 ORDER BY id_tweet LIMIT 270273, 90093);
UPDATE 30dec SET tweet_date = '2016/12/30';
INSERT INTO tweets (id_tweet, tweet, id_source, tweet_date) SELECT id_tweet, tweet, id_source, tweet_date FROM 30dec;
DROP TABLE 30dec;

-- /Week5 ---

-- Add sentiment bit (0-1-NULL):
ALTER TABLE tweets ADD sentiment bit;

-- remove duplicates
SET sql_mode = ''; -- disable Disable ONLY_FULL_GROUP_BY
CREATE TABLE IF NOT EXISTS temporaryTable AS (SELECT * FROM tweets GROUP BY id_tweet, tweet, id_source);
DROP TABLE tweets;
ALTER TABLE temporaryTable RENAME TO tweets;

-- Add PRIMARY KEY
ALTER TABLE tweets
ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY;



-- Add index on Tweet Date
CREATE INDEX tweet_date
ON tweets (tweet_date);
