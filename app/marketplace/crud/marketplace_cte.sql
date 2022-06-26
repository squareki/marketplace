with recursive query as (
    select id, name, date, "parentId", type, price, array[id] path
    from shopunits
    where id='{id}'
    union all
    select it.id, it.name, it.date, it."parentId", it.type, it.price, array_append(path, it.id)
    from shopunits it inner join query q on q.id = it."parentId"
)
select  t1.id, t1.name, t1.date, t1."parentId", t1.type, cast(floor(avg(t2.price)) as integer) price
from query t1
left join query t2 on t2.path @> Array[t1.id]
group by t1.id, t1.name, t1.type, t1.date, t1."parentId";