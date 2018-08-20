select
count(*)		
from
	part
where
	(
		p_brand = 'Brand#12'
		and p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
		and p_size between 1 and 5
	)
	or
	(
		p_brand = 'Brand#23'
		and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
		and p_size between 1 and 10
	)
	or
	(
		 p_brand = 'Brand#34'
		and p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
		and p_size between 1 and 15
	);
