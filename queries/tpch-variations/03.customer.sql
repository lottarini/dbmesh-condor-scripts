select
		count(*)
from
	customer
where
	c_mktsegment = 'BUILDING'
group by
	  c_custkey
;
