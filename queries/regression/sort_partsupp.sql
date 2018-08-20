select
	ps_partkey,
	ps_suppkey,
	ps_availqty
from
	partsupp
where
	ps_availqty > 15
order by
	ps_partkey, ps_suppkey
;

