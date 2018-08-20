--double join and simple filter condition

select s_name
from nation,region,supplier
where r_regionkey = n_regionkey
	  and s_nationkey = n_nationkey
	  and r_name = 'AFRICA'
;