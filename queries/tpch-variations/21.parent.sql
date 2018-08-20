select
	l1.l_orderkey,
	l1.l_suppkey
--	count(distinct(l1.l_suppkey))
--	,count(*) as numwait
--	l1.l_orderkey
from
	supplier,
	lineitem l1,
	orders,
	nation
where
	s_suppkey = l1.l_suppkey
	and o_orderkey = l1.l_orderkey
	and o_orderstatus = 'F'
	and l1.l_receiptdate > l1.l_commitdate
	and s_nationkey = n_nationkey
	and n_name = 'CHINA'
		
-- group by
-- 	  l1.l_orderkey
-- 	s_name
-- order by
-- 	numwait desc,
-- 	s_name

-- group by
-- 	  l1.l_orderkey
-- having
-- 		count(*) > 2

--limit 100
;
