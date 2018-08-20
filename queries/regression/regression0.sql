--filter on datetime
select
	l_orderkey,
	l_linenumber,
	l_shipdate
from
	lineitem
where
	l_shipdate <= date '1998-12-01' - interval '90' day (3)
;