--simple join

select r_name,n_name
from nation,region
where r_regionkey = n_regionkey
;