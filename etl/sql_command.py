select_film_count = """select count(*) as count from (
                                select f.id
                                from content.film_work f
                                where f.modified > to_timestamp(cast({0} AS TEXT),'YYYY-MM-DD HH24:MI:SS')
                                union
                                select pf.film_work_id
                                from content.person pr
                                join content.person_film_work pf on pr.id = pf.person_id
                                where pr.modified > to_timestamp(cast({0} AS TEXT) ,'YYYY-MM-DD HH24:MI:SS')
                                union
                                select gf.film_work_id
                                FROM content.genre gr
                                join content.genre_film_work gf on gr.id = gf.genre_id
                                where gr.modified > to_timestamp(cast({0} AS TEXT),'YYYY-MM-DD HH24:MI:SS') )"""

select_film = """select f.id
                                from content.film_work f
                                where f.modified > to_timestamp(cast({0} AS TEXT),'YYYY-MM-DD HH24:MI:SS')
                                union
                                select pf.film_work_id
                                from content.person pr
                                join content.person_film_work pf on pr.id = pf.person_id
                                where pr.modified > to_timestamp(cast({0} AS TEXT),'YYYY-MM-DD HH24:MI:SS')
                                union
                                select gf.film_work_id
                                FROM content.genre gr
                                join content.genre_film_work gf on gr.id = gf.genre_id
                                where gr.modified > to_timestamp(cast({0} AS TEXT),'YYYY-MM-DD HH24:MI:SS')"""


select_one_film = """select id, title, description, rating, modified from content.film_work where id = '{0}'"""

select_film_person = 'select p.id, pfw.role, p.full_name, p.modified, p.created from person_film_work pfw join person p on p.id = pfw.person_id where pfw.film_work_id = %s'

select_film_genre = 'select distinct g.name from genre_film_work gf join genre g on g.id = gf.genre_id where film_work_id = %s'


def get_batch_count(raws: int, batch_size: int) -> int:
    batch_count = round(raws / batch_size)
    if raws < batch_size:
        batch_count = 1
    if ((raws / batch_size) - batch_count) > 0:
        batch_count += 1
    return batch_count


def get_first(item: tuple):
    return item[0]
