		select
			p_name,
			s_name,
			l_orderkey,
			l_linenumber
		from
			part,
			supplier,
			partsupp,
			lineitem
		where
			s_suppkey = l_suppkey
			and ps_partkey = l_partkey
			and ps_suppkey = l_suppkey
			and p_partkey = l_partkey
			and p_name like '%green%';