--simple aggregate

select r_regionkey,sum(n_regionkey)
from nation,region
where r_regionkey = n_regionkey
group by r_regionkey	  
;