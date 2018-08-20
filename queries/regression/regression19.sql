		select
		ps_partkey,
		ps_suppkey,
		l_orderkey,
		l_linenumber
		from
			lineitem,
			partsupp
		where
			ps_suppkey = l_suppkey
			and ps_partkey = l_partkey
		order by
		ps_partkey,
		ps_suppkey,
		l_orderkey,
		l_linenumber
;