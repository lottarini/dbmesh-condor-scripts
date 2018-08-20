select
	ps_partkey,
	ps_suppkey,
	l_orderkey,
	l_linenumber,
	l_linestatus
from
	partsupp,
	lineitem
where
	l_partkey = ps_partkey
	and l_suppkey = ps_suppkey
	and ps_availqty > 15
order by
	ps_partkey
;

