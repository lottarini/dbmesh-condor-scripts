		select		
			count(*)
		from
			lineitem
		where
			l_commitdate < l_receiptdate
		group by
			  l_orderkey
;