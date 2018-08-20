		select
				ps_partkey,
				ps_suppkey
		from
			partsupp
		where
		 ps_availqty > (
				select
					100*sum(l_quantity)
				from
					lineitem
				where
					l_partkey = ps_partkey
					and l_suppkey = ps_suppkey
					and l_shipdate >= date '1994-01-01'
					and l_shipdate < date '1994-01-01' + interval '1' year
			);