--renamed table (this is taken from the nested query in q7)
--wit between and or conditions removed

		select
				l_orderkey,
				l_quantity
		from
			supplier,
			customer,
			nation n1,
			nation n2,
			orders,
			lineitem	
		where
			s_suppkey = l_suppkey
			and o_orderkey = l_orderkey
			and c_custkey = o_custkey
			and s_nationkey = n1.n_nationkey
			and c_nationkey = n2.n_nationkey
			and n1.n_name = 'FRANCE' 
			and n2.n_name = 'GERMANY'
		order by
			  l_orderkey,
			  l_quantity
;