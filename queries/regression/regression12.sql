-- simple synchronized query
-- this (should) return only the parts that are of size 10 and are the cheapest part for some supplier

select
		p_partkey,p_name,ps_supplycost
from
		part,
		partsupp
where
		p_partkey = ps_partkey
		and ps_supplycost = (
				  select min(ps_supplycost)
				  from 
				  	   supplier,
				  	   partsupp
				  where
				  s_suppkey = ps_suppkey	
				  and p_partkey = ps_partkey --p_partkey is external here
		)
		and p_size = 10
;