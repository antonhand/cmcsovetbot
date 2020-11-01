import mysql.connector
import settings

def connect():
    return mysql.connector.connect(**settings.db_connect)

########################################## ЗАПРОСЫ ПОЛЬЗОВАТЕЛЕЙ ##########################################

def get_state(vk_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT state from user_state where vk_id = " + str(vk_id))
    state = cursor.fetchone()
    cursor.close()
    cursor = conn.cursor()
    if state is None:
        cursor.execute("insert into user_state (vk_id, state) values (" + str(vk_id) + ",'-1')")
        state = '-1'
    else:
        state = state[0]
    cursor.close()
    conn.commit()
    conn.close()
    return state

def set_state(vk_id, state):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("update user_state set state = '" + state + "' where vk_id = " + str(vk_id))
    cursor.close()
    conn.commit()
    conn.close()

def get_prev_user(vk_id):
    conn = connect()
    cursor = conn.cursor()

    close_y_cond = ""

    if settings.close_years:
        close_y_cond = "and year not in " + str(settings.close_years)

    cursor.execute("""select fullname, year, v.stud_num
                      from
                        (select stud_num from prev_users
                         where vk_id = """  + str(vk_id) + """) pr
                    	inner join
                        voter v ON pr.stud_num = v.stud_num
                        where v.voter_num is null
                        """ + close_y_cond)
    res = cursor.fetchall()
    cursor.close()
    if res:
        studnum = res[0][2]
        cursor = conn.cursor()
        cursor.execute("update voter set vk_id = " + str(vk_id) + """,
                        is_self_named = 0
                        where stud_num = """ +  str(studnum))
        cursor.close()
        conn.commit()
        conn.close()
        return res[0]
    else:
        return res

def get_simular_voter_by_fn(fullname, vk_id, insert = False, is_self_named = False):
    is_self_named = '1' if is_self_named else '0'

    fullname = fullname.strip().upper().replace('Ё', 'Е').replace("'", "").replace('"', '')
    conn = connect()
    cursor = conn.cursor()

    close_y_cond = ""

    if settings.close_years:
        close_y_cond = "and year not in " + str(settings.close_years)

    cursor.execute("""select distinct fullname from voter
                        where replace(upper(fullname), 'Ё', 'Е') like '""" + fullname +'''%'
                        and voter_num is null
                        ''' + close_y_cond + '''
                        order by fullname''')
    res = cursor.fetchall()
    cursor.close()

    if insert and res:
        cursor = conn.cursor()

        cursor.execute("""insert into user_voter_vars (vk_id, voter_id, is_self_named)
                          select """ + str(vk_id) + ", voter_id, " + is_self_named + """ from voter
                            where voter_id not in (select voter_id from user_voter_vars
                                                    where vk_id = """ + str(vk_id) + """)
                            and voter_num is null
                            """ + close_y_cond + """
                            and replace(upper(fullname), 'Ё', 'Е') like '""" + fullname +"%'")
        cursor.close()

    conn.commit()
    conn.close()
    return res

def get_simular_voter(name, surname, vk_id, insert = False):
    name = name.strip()
    surname = surname.strip()
    return get_simular_voter_by_fn(surname + " " + name, vk_id, insert)

def get_voter_vars(vk_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""select distinct fullname from voter
                        where voter_id in (select voter_id from user_voter_vars where vk_id = """ + str(vk_id) + '''
                        order by fullname''')
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

def delete_vars(vk_id, except_fn = 'NoneExcept'):
    fullname = except_fn.strip().upper().replace('Ё', 'Е')
    conn = connect()

    cursor = conn.cursor()
    cursor.execute("""delete from user_voter_vars
                      where vk_id = """ + str(vk_id) + """
                      and voter_id not in (select voter_id from voter where replace(upper(fullname), 'Ё', 'Е') like '""" + fullname +"%')")
    cursor.close()
    conn.commit()
    conn.close()

def is_self_named(vk_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""select distinct is_self_named from user_voter_vars
                        where vk_id = """ + str(vk_id))
    res = cursor.fetchall()

    cursor.close()
    conn.close()

    if res[0][0] == 1:
        return True
    else:
        return False

def attemts_count(vk_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""select studnum_attempts from user_state
                        where vk_id = """ + str(vk_id))
    res = cursor.fetchall()
    cursor.close()

    if res[0][0] < 3:
        cursor = conn.cursor()
        cursor.execute("update user_state set studnum_attempts = " + str(res[0][0] + 1) + """
                        where vk_id = """ + str(vk_id))
        cursor.close()
        conn.commit()
        conn.close()
        return res[0][0]

    conn.close()
    return res[0][0]

def check_studnum(vk_id, studnum):
    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""select fullname, year, vk_id from voter
                        where voter_id in (select voter_id from user_voter_vars where vk_id = """ + str(vk_id) + """)
                        and voter_num is null
                        and stud_num = """ + str(studnum))
    res = cursor.fetchall()
    cursor.close()

    if res:
        if not res[0][2]:
            cursor = conn.cursor()
            cursor.execute("update voter set vk_id = " + str(vk_id) + """,
                            is_self_named = (select distinct is_self_named from user_voter_vars
                                                where vk_id = """ + str(vk_id) + """)
                            where voter_id in (select voter_id from user_voter_vars where vk_id = """ + str(vk_id) + """)
                            and stud_num = """ +  str(studnum))
            cursor.close()
            conn.commit()
            conn.close()
            return 'good', res[0]
        else:
            return 'already', None


    conn.close()
    at_cnt = attemts_count(vk_id)
    if at_cnt < 2:
        return 'bad', at_cnt
    else:
        return 'end', None


def get_candidates(vk_id):
    conn = connect()
    cursor = conn.cursor()

    year = "(select year from voter where vk_id = " + str(vk_id) + ")"
    if settings.is_test:
        year = "7"

    cursor.execute("""select surname, name, COALESCE(midname, ''), description, vk_id, program, COALESCE(video, ''), t1.cand_id, COALESCE(t2.cand_id, 0) as is_vote
                        from (select * from candidate
                                where year = """ + year + """
                                and surname <> 'Против'
                             ) t1
                        left join (select * from vote
                        			where voter_id = (select voter_id from voter where vk_id = """ + str(vk_id) + """)) t2 on t1.cand_id = t2.cand_id
                        order by surname, name, midname""")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

def make_choice(vk_id, cand_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""select * from vote
                        where voter_id = (select voter_id from voter where vk_id = """ + str(vk_id) + """)
                        and cand_id = """ + str(cand_id))
    res = cursor.fetchall()
    cursor.close()
    cursor = conn.cursor()

    if res:
        cursor.execute("""delete from vote
                            where voter_id = (select voter_id from voter where vk_id = """ + str(vk_id) + """)
                            and cand_id = """ + str(cand_id))
    else:
        cursor.execute("""insert into vote (voter_id, cand_id)
                          select voter_id, """ + str(cand_id) + " from voter where vk_id = " + str(vk_id))

    cursor.close()
    conn.commit()
    conn.close()
    return res

def vote_against(vk_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("set time_zone = '" + settings.timezone + "'")
    cursor.close()

    cursor = conn.cursor()

    year = "(select year from voter where vk_id = " + str(vk_id) + ")"
    if settings.is_test:
        year = "7"

    cursor.execute("""insert into vote (voter_id, cand_id, is_confirm, conf_date)
                        values
                        ( (select voter_id from voter
                            where vk_id = """ + str(vk_id) + """)
                         ,(select cand_id from candidate
                             where surname = 'Против'
                             and year = """ + year + """)
                         , 1, current_timestamp)""")

    cursor.close()
    conn.commit()
    conn.close()

def add_voter_num(vk_id):
    conn = connect()
    conn.start_transaction(consistent_snapshot=False,
                      isolation_level='SERIALIZABLE',
                      readonly=False)
    cursor = conn.cursor()

    cursor.execute("""update voter
                        join (select coalesce(max(t1.voter_num) + 1, t1.year * 1000 + 501) num
                                from voter t1
                                where t1.year = (select t2.year from voter t2
                                                    where t2.vk_id = """ + str(vk_id) + """)) t
                        set voter.voter_num = t.num
                        where voter.vk_id = """ + str(vk_id))

    cursor.close()
    conn.commit()
    conn.close()

def get_voter_num(vk_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""select voter_num from voter
                              where vk_id = """ + str(vk_id))

    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res

def confirm_votes(vk_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("set time_zone = '" + settings.timezone + "'")
    cursor.close()

    cursor = conn.cursor()

    cursor.execute("""update vote set is_confirm = 1,
                        conf_date = current_timestamp
                        where voter_id = (select voter_id from voter
                                            where vk_id = """ + str(vk_id) + ")")

    cursor.close()
    conn.commit()
    conn.close()

'''
def is_proccessed(vk_id, msg_id):
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""select msg_id
                        from user_msgs
                        where vk_id = """ + str(vk_id) + """
                        and msg_id = """ + str(msg_id))

    res = cursor.fetchall()
    cursor.close()
    conn.close()

    if res:
        return True
    else:
        return False


def add_proccessed(vk_id, msg_id):
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""insert into user_msgs (vk_id, msg_id)
                        values
                        (""" + str(vk_id) + "," + str(msg_id) + ")")

    cursor.close()
    conn.commit()
    conn.close()'''

########################################## ЗАПРОСЫ АДМИНИСТРАТОРОВ ##########################################

def get_stat():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""select year, coalesce(count(voter_num), 0) as vote_cnt, count(*)
                        from  voter
                        group by year""")

    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res

def get_active_users():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""select vk_id from user_state""")

    res = cursor.fetchall()

    cursor.close()
    conn.close()

    fin_res = list(map(lambda x: x[0], res))

    return fin_res

def insert_users(users):
    conn = connect()
    cursor = conn.cursor()


    ex = 'insert into user_state (vk_id, state) values '
    for usr in users:
        ex += '('+ str(usr) + ",'0'),"

    ex = ex[:-1]

    cursor.execute(ex)

    cursor.close()
    conn.commit()
    conn.close()

def get_groups_stat():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""select year, `group`, count(voter_num), count(*), count(*) - count(voter_num) delta
                        from voter
                        group by year, `group`
                        order by year, delta desc""")

    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res

def get_streams_stat():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""select year, stream, count(voter_num), count(*)
                        from voter
                        group by year, stream""")

    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res

def get_voters():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""select distinct fullname, conf_date, year
                        from voter
                        left join vote
                        using(voter_id)
                        where voter_num is not null
                        and voter_num <> -1""")

    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res

def get_all_voters():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""select distinct fullname, conf_date, year
                        from voter
                        left join vote
                        using(voter_id)
                        where voter_num is not null""")

    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res

def get_users_by_state(state):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""select vk_id
                        from user_state
                        where state ='""" + state + "'")

    res = cursor.fetchall()

    cursor.close()
    conn.close()

    res = list(map(lambda x: x[0], res))

    return res

def get_results():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""select v.voter_num,  coalesce(concat(cn.surname, ' ', cn.name, ' ', coalesce(cn.midname, '')), 'Воздержался'), v.year
                        from voter v left join vote vt
                        on v.voter_id = vt.voter_id and vt.is_confirm = 1
                        left join candidate cn on vt.cand_id = cn.cand_id
                        where voter_num is not null
                        and voter_num > -1""")

    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res

def get_not_finalized_voters():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""select vk_id
                        from voter
                        where voter_id in (select distinct voter_id
                                                from vote
                                                where is_confirm = 0)""")

    res = cursor.fetchall()

    res = list(map(lambda x: x[0], res))

    cursor.close()
    conn.close()

    return res

def select(query):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(query)

    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res

def get_prev_novote_users(year):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""select pr.vk_id
                        from prev_users pr
                        inner join voter v
                        	on pr.stud_num = v.stud_num
                        	and v.voter_num is null
                        where pr.vk_id not in (select vk_id from user_state)
                        and v.year = """ + str(year))
    res = cursor.fetchall()
    cursor.close()

    res = list(map(lambda x: x[0], res))

    cursor = conn.cursor()

    cursor.execute("""insert into user_state
                        select pr.vk_id, '0', 0
                        from prev_users pr
                        inner join voter v
                        	on pr.stud_num = v.stud_num
                        	and v.voter_num is null
                        where pr.vk_id not in (select vk_id from user_state)
                        and v.year = """ + str(year))

    cursor.close()
    conn.commit()
    conn.close()

    return res
