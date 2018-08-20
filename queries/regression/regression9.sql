--simple nested query - no work done in the parent query

select 
	   nation
from
		(
		select
				n_name as nation
		from   
			   nation,
			   region
		where			
			   n_regionkey = r_regionkey
			   and r_name = 'AFRICA'
		) as african_nations
;