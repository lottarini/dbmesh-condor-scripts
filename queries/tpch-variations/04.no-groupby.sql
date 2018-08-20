select
	o_orderkey,
	count(distinct(o_orderkey))
from
	orders
where
	o_orderdate >= date '1993-07-01'
	and o_orderdate < date '1993-07-01' + interval '3' month
	and exists (
		select
			*
		from
			lineitem
		where
			l_orderkey = o_orderkey
			and l_commitdate < l_receiptdate
	)
group by
	  o_orderkey
having
	count(distinct(o_orderkey)) > 1
order by
	o_orderkey;
