create table total
select * from dictionary;

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
                
