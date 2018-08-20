--simple nested query - parent filters son results

select 
	   nation
from
		(
		select
				n_name as nation,
				r_regionkey as nested_regionkey 
		from   
			   nation,
			   region
		where			
			   n_regionkey = r_regionkey
			   and r_regionkey < 3  --funny but it works, these are the first three regions
		) as a_nations,
		region
where
		nested_regionkey = r_regionkey
		and r_name = 'AMERICA'
;