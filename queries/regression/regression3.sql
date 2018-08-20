--filtering condition on phone ( string )
--simple arithmetic (*,-) on the select

select
		s_suppkey,s_phone,2*(s_nationkey-1)
from
		supplier
where
		s_nationkey = 17
		and s_phone = '27-918-335-1736'
;