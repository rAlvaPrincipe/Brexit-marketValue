alter table affin
add column dictionary varchar(30);

update affin
set dictionary = "affin";

alter table bing
add column dictionary varchar(30);

update bing
set dictionary = "bing";

create table dictionary_1
(select * from affin)
union
(select * from bing);