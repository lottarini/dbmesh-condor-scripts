--filter on two datetime
--extract same as q7
select
	l_orderkey,
	l_linenumber,
	extract(year from l_shipdate) as year_duh
from
	lineitem
where
	l_commitdate <= l_receiptdate
;