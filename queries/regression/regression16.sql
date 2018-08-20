--complex and/or pre filter
--notice how or has precedence over and 
select
	l_orderkey,
	l_linenumber,
	extract(year from l_shipdate) as year_duh
from
	lineitem
where
	l_commitdate <= l_receiptdate and l_quantity > 10 
	or l_returnflag = 'N'
;