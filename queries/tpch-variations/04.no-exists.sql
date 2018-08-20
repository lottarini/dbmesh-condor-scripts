-- order by priority and count all orders done in a three months interval which contained an item received by the customer (receiptdate) after the expected date (commitdate) 
select
	o_orderpriority,
	count(*) as order_count
from
	orders
where
	o_orderdate >= date '1993-07-01'
	and o_orderdate < date '1993-07-01' + interval '3' month
group by
	o_orderpriority
order by
	o_orderpriority;
