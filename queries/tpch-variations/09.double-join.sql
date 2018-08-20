		select
			ps_partkey,
			ps_suppkey,
			l_orderkey,
			l_linenumber
		from
			partsupp,
			lineitem
		where
			ps_partkey = l_partkey
			and ps_suppkey = l_suppkey
	;