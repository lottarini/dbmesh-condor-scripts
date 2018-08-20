
				select
					0.5 * sum(l_quantity)
				from
					lineitem
				where
						l_shipdate >= date '1994-01-01'
					and l_shipdate < date '1994-01-01' + interval '1' year;