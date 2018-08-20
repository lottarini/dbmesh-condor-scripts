select
	s_suppkey
from
	supplier,
	nation
where
	s_nationkey = n_nationkey
	and n_name = 'GERMANY'
;