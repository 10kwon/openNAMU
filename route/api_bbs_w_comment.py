from .tool.func import *

def api_bbs_w_comment(sub_code : str = '') -> typing.Union[str, flask.Response, werkzeug.wrappers.response.Response]:
    conn : typing.Union[sqlite3.Connection, pymysql.connections.Connection]
    with get_db_connect() as conn:
        curs : typing.Union[sqlite3.Cursor, pymysql.cursors.Cursor] = conn.cursor()

        curs.execute(db_change('select set_name, set_data, set_code, set_id from bbs_data where (set_name = "comment" or set_name = "comment_date" or set_name = "comment_user_id") and set_id = ? order by set_code + 0 asc'), [sub_code])
        db_data : typing.Optional[typing.List[typing.Tuple[str, str, str]]] = curs.fetchall()
        if not db_data:
            return flask.jsonify({})
        else:
            temp_id : str = ''
            temp_dict : dict[str, str] = {}
            temp_list : typing.List[dict[str, str]] = []

            for_a : typing.Tuple[str, str, str]
            for for_a in db_data:
                if temp_id != for_a[2]:
                    if temp_dict != {}:
                        temp_list += [dict(temp_dict)]

                    temp_id = for_a[2]
                    temp_dict['code'] = for_a[2]

                temp_dict[for_a[0]] = for_a[1]

            if temp_dict != {}:
                temp_list += [dict(temp_dict)]

            return flask.jsonify(temp_list)