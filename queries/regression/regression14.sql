--filter on two datetime
--filter on float constant

select
	l_orderkey,
	l_linenumber,
	l_shipdate
from
	lineitem
where
	l_commitdate <= l_receiptdate
	and l_extendedprice < 10000.12
;