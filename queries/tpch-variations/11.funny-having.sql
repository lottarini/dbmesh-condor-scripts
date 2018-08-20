select
	ps_partkey,
	count(*),
	sum(ps_supplycost * ps_availqty) as value
from
	partsupp,
	supplier,
	nation
where
	ps_suppkey = s_suppkey
	and s_nationkey = n_nationkey
	and n_name = 'GERMANY'
group by
	ps_partkey 
having
	1.2 * avg(ps_supplycost * ps_availqty) > 2000000
	-- and sum(ps_supplycost * ps_availqty) > 3000000
	-- and
	--count(*) > 2	  
;