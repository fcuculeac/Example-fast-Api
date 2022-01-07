select p.*, u.email from posts p
join users u on u.id = p.user_id
where user_id = 7;

delete from users where id = 8

alter table posts drop column user_id;

select p.title, p.content, u.email, v.Total as total_votes 
from posts p
join users u on u.Id = p.owner_id
left join (select post_id, sum(1) as Total
		   from votes
		   group by post_id) v
		   on v.post_id = p.id

