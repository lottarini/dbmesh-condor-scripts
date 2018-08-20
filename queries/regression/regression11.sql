--this is a variation of tpch14
--tests complex case/select conditions
select
	100.00 * sum(case
		when p_type like 'PROMO%' 
		or p_size = 15
		or l_shipdate = date '1995-09-01'
			then l_extendedprice * (1 - l_discount)
		else 0
	end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
from
	lineitem,
	part
where
	l_partkey = p_partkey
	and l_shipdate >= date '1995-09-01'
	and l_shipdate < date '1995-09-01' + interval '1' month;
