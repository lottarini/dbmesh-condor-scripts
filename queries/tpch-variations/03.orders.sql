select
	count(*)
from
	orders
where
	o_orderdate < date '1995-03-15'
group by
	o_orderkey
;
