--2 columns in select, basic filtering (int) on supplier

select
		s_suppkey,s_phone
from
		supplier
where
		s_nationkey = 17
;