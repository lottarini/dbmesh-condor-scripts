--simple nested query - parent filters son results

select 
	   nation
from
		(
		select
				n_name as nation,
				r_name as region  -- this surprisingly works
		from   
			   nation,
			   region
		where			
			   n_regionkey = r_regionkey
			   and r_regionkey < 3  --funny but it works, these are the first three regions
		) as a_nations
where
		region = 'AMERICA'
;