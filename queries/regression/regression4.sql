--simple date comparison, no interval

select o_orderkey
from orders
where o_orderdate > date '1996-9-3'
;