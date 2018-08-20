		select
		ps_partkey,
			min(ps_supplycost)
		from
			partsupp,
			supplier,
			nation,
			region
		where
			s_suppkey = ps_suppkey
			and s_nationkey = n_nationkey
			and n_regionkey = r_regionkey
			and r_name = 'EUROPE'
		group by
			ps_partkey
;