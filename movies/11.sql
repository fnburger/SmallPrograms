select title from movies left outer join stars on movies.id = stars.movie_id left outer join people on stars.person_id = people.id left outer join ratings on movies.id = ratings.movie_id where name="Chadwick Boseman" order by rating DESC limit 5;