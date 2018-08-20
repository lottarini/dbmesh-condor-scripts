-- for every part that satisfies the conditions list the number of suppliers providing it w/o customer complaints
select
		p_partkey,
		p_brand,
		p_type,
		p_size,
		--count(distinct ps_suppkey) as supplier_cnt
		ps_suppkey
from
	partsupp,
	part
where
	p_partkey = ps_partkey
	and p_brand in ('Brand#14', 'Brand#22', 'Brand#35')
	and p_type not like 'MEDIUM POLISHED%'
	and p_size in (49, 14, 23, 45, 19, 3, 36, 9)
	and ps_suppkey not in (
		select
			s_suppkey
		from
			supplier
		where
			s_comment like '%Customer%Complaints%'
	)
-- group by
-- 	p_brand,
-- 	p_type,
-- 	p_size
order by
	-- supplier_cnt desc,
	p_brand,
	p_type,
	p_size,
	ps_suppkey
;
