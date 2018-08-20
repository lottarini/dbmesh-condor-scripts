-- order by priority and count all orders done in a three months interval which contained an item received by the customer (receiptdate) after the expected date (commitdate) 
select
	o_orderpriority,
	count(*) as order_count
from
	orders
where
	 exists (
		select
			*
		from
			lineitem
		where
			l_orderkey = o_orderkey
			and l_commitdate < l_receiptdate
	)
group by
	o_orderpriority
order by
	o_orderpriority;


