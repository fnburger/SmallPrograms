select name from people left outer join stars on people.id = stars.person_id left outer join movies on stars.movie_id = movies.id where title="Toy Story";