-- dictionary is the union of

alter table affin add column dictionary varchar(30);
update affin set dictionary = "affin";

alter table bing add column dictionary varchar(30);
update bing set dictionary = "bing";

create table dictionary
(select * from affin)
union
(select * from bing);





--

create table total select * from dictionary;

DELETE FROM total
where word in (
				select word from
								(select word, count(*) as num
								from dictionary
								group by word
								having num = 2)
                                as table_1
				)
and dictionary = "affin"
