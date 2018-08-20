--testing filtering conditions that involve operations with columns
--groupby on two columns (that can be solved with concat)

select
	l_returnflag,
	l_linestatus,
	count(*) as count_order
from
	lineitem
where
	1.2 * l_quantity > 20
group by
	l_returnflag,
	l_linestatus
order by
	l_returnflag,
	l_linestatus;

-- select * from optimizer_stats() stats;
