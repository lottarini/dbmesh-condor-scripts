select
	ps_partkey,
	s_suppkey,
	l_orderkey,
	l_linenumber
from
	part,
	supplier,
	lineitem,
	partsupp
where
	s_suppkey = l_suppkey
	and ps_suppkey = l_suppkey
	and ps_partkey = l_partkey
	and p_partkey = l_partkey
	and p_name like '%green%'
	and s_nationkey = 22  -- supplier from russia
	and l_quantity > 10
order by
	  ps_partkey,
	  l_orderkey,
	  l_linenumber
;
