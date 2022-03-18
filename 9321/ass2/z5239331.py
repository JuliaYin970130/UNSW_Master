import datetime
import json
import math
import sqlite3
import string
import urllib.request as req
from urllib.parse import quote

import matplotlib.pyplot as plt
from flask import Flask, jsonify, make_response, request, send_file
from flask_restx import Resource, Api, fields

app = Flask(__name__)
api = Api(app, title='Data Service for TV Shows',
          description='a Flask-Restx data service that allows a client to read and store some TV Shows, and allow the consumers to access the data.',
          default="Collections")

app.config['JSON_SORT_KEYS'] = False


def create_db():
    con = sqlite3.connect('z5239331.db')
    cur = con.cursor()
    #cur.execute('''DROP TABLE IF EXISTS TvShow''')
    cur.execute('''CREATE TABLE IF NOT EXISTS TvShow
                    (id INTEGER PRIMARY KEY AUTOINCREMENT , tvmaze_id INTEGER,last_update TEXT,name TEXT ,type TEXT ,
                    language TEXT ,genres TEXT ,status TEXT ,premiered REAL ,officialSite TEXT ,schedule TEXT ,
                    rating TEXT ,weight REAL ,network TEXT ,summary TEXT);''')
    con.commit()
    con.close()


def store_in_DB(data):
    con = sqlite3.connect('z5239331.db')
    cur = con.cursor()
    last_update = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
    # print(last_update)
    cur.execute(
        "insert into TvShow (tvmaze_id,last_update,name,type,language,genres,status,premiered,officialSite,schedule,rating,weight,network,summary) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
        (data['show']['id'], last_update, data['show']['name'], data['show']['type'], data['show']['language'],
         str(data['show']['genres']), data['show']['status'], data['show']['premiered'], data['show']['officialSite'],
         str(data['show']['schedule']), str(data['show']['rating']), data['show']['weight'],
         str(data['show']['network']), data['show']['summary']))
    con.commit()
    con.close()


def match(name):
    NAME = name.replace(' ', '-').lower()
    url = 'http://api.tvmaze.com/search/shows?q=' + NAME
    s = quote(url, safe=string.printable)  # utf-8
    resource = req.Request(s)
    data = json.loads(req.urlopen(resource).read())
    return data

def id_list(id,id_):
    id_list = []
    index = 0
    for i in range(len(id_)):
        # print(type(id_[i][0]))
        id_list.append(id_[i][0])
        if id_[i][0] == id:
            index = i
    _links = {}
    _links['self'] = {'href': 'http://' + '127.0.0.1' + ':' + '5000' + '/tv-shows/' + str(id)}
    if index != 0:
        _links['previous'] = {
            'href': 'http://' + '127.0.0.1' + ':' + '5000' + '/tv-shows/' + str(id_list[index - 1])}
    if index != (len(id_)) - 1:
        _links['next'] = {'href': 'http://' + '127.0.0.1' + ':' + '5000' + '/tv-shows/' + str(id_list[index + 1])}
    return _links

post_parser = api.parser()
post_parser.add_argument('name', type=str, help='For Q1 post use only, input a TV show name', location='args')


@api.route('/tv-shows/import')

class Q1(Resource):
    @api.response(200, 'Ok')
    @api.response(201, 'Created')
    @api.response(404, 'Not Found')
    @api.response(400, 'Bad Request')
    # The @api.expect() decorator allows you to specify the expected input fields.
    @api.expect(post_parser)
    @api.doc(params={'name': 'input a TV show name'})
    def post(self):
        name = post_parser.parse_args()['name']
        if name == None:
            message = {'message': 'Bad Request'}
            return make_response(jsonify(message), 400)
        # create database
        create_db()
        # connect db
        con = sqlite3.connect('z5239331.db')
        cur = con.cursor()
        # check #record in db
        cur.execute("select count(*) from TvShow ")
        i = cur.fetchall()[0][0]
        # hasRecord
        if i != 0:
            # check whether this name has already in db
            query = "select name from TvShow"
            cur.execute(query)
            isExist = cur.fetchall()
            seek_name = ''
            for i in range(len(isExist)):
                if name.lower() == isExist[i][0].lower():
                    seek_name = isExist[i][0]
            # isExist
            if seek_name:
                cur.execute("select id,tvmaze_id,last_update from TvShow where name = ?;", (seek_name,))
                value = cur.fetchall()
                cur.execute("select id from TvShow;")
                id_ = cur.fetchall()
                _links = id_list(value[0][0],id_)

                message = {
                    "id": int(value[0][0]),
                    "tvmaze_id": int(value[0][1]),
                    "last_update": value[0][2],
                    "_links": _links
                }
                con.commit()
                con.close()
                response = jsonify(message)
                return make_response(response, 200)
            else:  # isNotExist, insert a new record
                data = match(name)
                first_match = data[0]['show']['name']
                if name.lower() != first_match.lower():
                    response = {'message': 'Not found'}
                    con.close()
                    return make_response(jsonify(response), 404)
                store_in_DB(data[0])
                cur.execute("select id,tvmaze_id,last_update from TvShow where name = ?;", (first_match,))
                value = cur.fetchall()
                cur.execute("select id from TvShow;")
                id_ = cur.fetchall()
                _links = id_list(value[0][0],id_)
                message = {
                    "id": int(value[0][0]),
                    "tvmaze_id": int(value[0][1]),
                    "last_update": value[0][2],
                    "_links": _links
                }
                con.commit()
                con.close()
                response = jsonify(message)
                return make_response(response, 201)
        else:
            # DB is empty, insert a new record
            data = match(name)
            first_match = data[0]['show']['name']
            if name.lower() != first_match.lower():
                con.close()
                return {'message': 'Not found'}, 404
            store_in_DB(data[0])
            cur.execute("select id,tvmaze_id,last_update from TvShow where name = ?;", (first_match,))
            value = cur.fetchall()
            cur.execute("select id from TvShow;")
            id_ = cur.fetchall()
            _links = id_list(value[0][0], id_)
            message = {
                "id": int(value[0][0]),
                "tvmaze_id": int(value[0][1]),
                "last_update": value[0][2],
                "_links": _links
            }
            con.commit()
            con.close()
            response = jsonify(message)
            return make_response(response, 201)


put_model = api.model('PATCH Payload', {
    'name': fields.String,
    'language': fields.String
})


@api.route('/tv-shows/<int:id>')
@api.doc(params={'id': 'input an existing ID'})
class Q2_Q3_Q4(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Not Found')
    def get(self, id):
        if id == None:
            message = {'message': 'Bad Request'}
            return make_response(jsonify(message), 400)
        #print(type(id))
        con = sqlite3.connect('z5239331.db')
        cur = con.cursor()
        cur.execute("select * from TvShow where id = {};".format(id))
        values = cur.fetchall()
        # not found id
        if not values:
            massage = "id " + str(id) + " does not exist."
            resp = {"massage": massage, "id": id}
            con.close()
            return make_response(jsonify(resp), 404)
        # print(values)
        # build message
        cur.execute("select id from TvShow;")
        id_ = cur.fetchall()
        _links = id_list(values[0][0], id_)
        con.commit()
        con.close()
        message = {}
        key = ('id', 'tvmaze_id', 'last_update', 'name', 'type', 'language', 'genres', 'status', 'premiered',
               'officialSite', 'schedule', 'rating', 'weight', 'network', 'summary')
        for i in range(len(key)):
            if isinstance(values[0][i], str):
                if '[' in values[0][i] or '{' in values[0][i]:
                    message[key[i]] = json.loads(values[0][i].replace("'", "\""))
                else:
                    message[key[i]] = values[0][i]
            else:
                message[key[i]] = values[0][i]
        message['_links'] = _links

        return make_response(jsonify(message), 200)

    @api.response(200, 'OK')
    @api.response(404, 'Not Found')
    def delete(self, id):
        if id == None:
            message = {'message': 'Bad Request'}
            return make_response(jsonify(message), 400)

        con = sqlite3.connect('z5239331.db')
        cur = con.cursor()
        cur.execute("select id from TvShow where id={};".format(id))
        isid = cur.fetchall()
        # check id is exist
        if not isid:
            massage = "id " + str(id) + " does not exist."
            resp = {"massage": massage, "id": id}
            con.close()
            return make_response(jsonify(resp), 404)

        cur.execute("delete from TvShow where id = {};".format(id))
        con.commit()
        con.close()

        massage = "The tv show with id " + str(id) + " was removed from the database!"
        resp = {"message": massage, "id": id}
        return make_response(jsonify(resp), 200)

    @api.expect(put_model)
    def patch(self, id):
        if id == None:
            message = {'message': 'Bad Request, please input value'}
            return make_response(jsonify(message), 400)

        data = request.get_json(force='True')
        key = [i for i in data.keys()]
        if data:
            con = sqlite3.connect('z5239331.db')
            cur = con.cursor()
            cur.execute("select id from TvShow where id={};".format(id))
            isid = cur.fetchall()
            if not isid:
                massage = "id " + str(id) + " does not exist."
                resp = {"massage": massage, "id": id}
                con.close()
                return make_response(jsonify(resp), 404)

            for i in range(len(data.keys())):
                cur.execute("update TvShow set\"{}\"=\"{}\"where id = {}".format(key[i], data[key[i]], id))

            last_update = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
            cur.execute("update TvShow set last_update = ? where id = ?",(last_update, id))

            cur.execute("select id from TvShow;")
            id_ = cur.fetchall()
            _links = id_list(id, id_)

            message = {
                'id': id,
                'last_update': last_update,
                '_links': _links
            }
            con.commit()
            con.close()
            return make_response(jsonify(message), 200)
        else:
            message = {'message': 'Bad Request, please check input value.'}
            return make_response(jsonify(message), 400)


order_by_parser = api.parser()
order_by_parser.add_argument('order_by', type=str, help='For Q5 use only, input order by', location='args')
order_by_parser.add_argument('page', type=str, help='For Q5 use only, input page which is a positive number', location='args')
order_by_parser.add_argument('page_size', type=str, help='For Q5 use only, input page size which is a positive number', location='args')
order_by_parser.add_argument('filter', type=str, help='For Q5 use only, input filter', location='args')


@api.route('/tv-shows')
class Q5(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Not Found')
    @api.response(400, 'Bad Request')
    @api.expect(order_by_parser)
    def get(self):
        order_by = order_by_parser.parse_args()['order_by']
        page = order_by_parser.parse_args()['page']
        page_size = order_by_parser.parse_args()['page_size']
        filter_ = order_by_parser.parse_args()['filter']

        if order_by and page.isdigit() and page_size.isdigit() and filter_:
            page_size = int(page_size)
            page = int(page)
            if page <= 0 or int(page_size) <= 0:
                message = {'message': 'input should be positive integer.'}
                return make_response(jsonify(message), 400)
            filter_s = filter_.replace(' ', '')
            filter_split = filter_s.split(',')
            # +rating-average,+id
            order_by_s = order_by.replace(' ', '')
            order_by_split = order_by_s.split(',')
            for i in range(len(order_by_split)):
                if order_by_split[i][0] == '+' or order_by_split[i][0] == '-':
                    continue
                else:
                    message = {'message': 'Missing symbol'}
                    return make_response(jsonify(message), 400)

            con = sqlite3.connect('z5239331.db')
            cur = con.cursor()
            cur.execute("select count(*) from TvShow")
            total_record = cur.fetchall()[0][0]


            max_page = math.ceil(total_record / page_size)
            temp = {}
            # input page is over the max pages
            if page > max_page:
                message = {'message': 'Not Found, please check page input value'}
                con.close()
                return make_response(jsonify(message), 404)
            else:
                rest_record = total_record % page_size
                record_start, record_end, record_num = 0, page_size, page_size
                # page full up with page size
                if rest_record == 0:
                    if page != 1:
                        record_start = page_size * (page - 1)
                # can not full up with rest records
                elif rest_record != 0:
                    # the last page or the first page
                    if page == max_page:
                        record_start = page_size * (page - 1)
                        record_end = rest_record
                        record_num = rest_record
                    # other pages with page sizes
                    elif page < max_page:
                        if page != 1:
                            record_start = page_size * (page - 1)
                # print('record_start', record_start, 'record_end', record_end, 'rest_record', rest_record,
                #        'record_num',
                #        record_num)
                # 拼query
                order_col = ''
                for i in range(len(order_by_split)):
                    order_col += ''
                    if order_by_split[i][0] == '+':
                        if order_by_split[i][1:] == 'rating-average':
                            order_col += 'rating'
                        else:
                            order_col += order_by_split[i][1:]
                        order_col += ' asc'
                    if order_by_split[i][0] == '-':
                        if order_by_split[i][1:] == 'rating-average':
                            order_col += 'rating'
                        else:
                            order_col += order_by_split[i][1:]
                        order_col += ' desc'
                    if i != len(order_by_split) - 1:
                        order_col += ','
                # print(order_col)
                for i in filter_split:
                    temp[i] = []
                    cur.execute("select\"{}\"from TvShow order by {} limit {},{};".format(i, order_col,
                                                                                          record_start, record_end))
                    value = cur.fetchall()
                    for j in range(record_num):
                        temp[i].append(value[j][0])

                cur.execute("select id from TvShow;")
                id_ = cur.fetchall()
                id_lst =[]
                for i in range(len(id_)):
                    id_lst.append(id_[i][0])
                result_ = {}

                for id in id_lst:

                    cur.execute("select * from TvShow where id ={}".format(id))
                    value = cur.fetchall()

                    result_[id] = {value[0][0]}
                    print(result_)
                # print(temp)
                tv_shows = []
                result = {}
                for j in range(record_num):
                    for i in filter_split:
                        if isinstance(temp[i][j], str):
                            if '[' in temp[i][j] or '{' in temp[i][j]:
                                result[i] = json.loads(temp[i][j].replace("'", "\""))
                            else:
                                result[i] = temp[i][j]
                        else:
                            result[i] = temp[i][j]
                    tv_shows.append(result)
                    result = {}
                # print(tv_shows)
                con.close()
                # order_by=+id&page=1&page_size=1000&filter=id,name"
                _links = {}
                _links['self'] = {"href": "http://127.0.0.1:5000/tv-shows?order_by="+order_by+"&page=" + str(page) + "&page_size=" + str(
                    page_size) + "&filter=" + filter_}
                if page > 1:
                    _links['previous'] = {
                        "href": "http://127.0.0.1:5000/tv-shows?order_by="+order_by+"&page=" + str(page - 1) + "&page_size=" + str(
                            page_size) + "&filter=" + filter_}
                if page < max_page:
                    _links['next'] = {
                        "href": "http://127.0.0.1:5000/tv-shows?order_by="+order_by+"&page=" + str(page + 1) + "&page_size=" + str(
                            page_size) + "&filter=" + filter_}
                message = {
                    "page": page,
                    "page-size": page_size,
                    "tv-shows": tv_shows,
                    "_links": _links
                }
                return make_response(jsonify(message), 200)
        else:
            message = {'message': 'Bad Request, please check input value.'}
            return make_response(jsonify(message), 400)


get_parser = api.parser()
get_parser.add_argument('format', type=str, help='For Q6 use only, input json or image', location='args')
get_parser.add_argument('by', type=str, help='For Q6 use only, input a category', location='args')


@api.route('/tv-shows/statistics')
class Q6(Resource):
    @api.response(200, 'OK')
    @api.response(404, 'Not Found')
    @api.response(404, 'Bad Request')
    @api.expect(get_parser)
    def get(self):
        format_ = get_parser.parse_args()['format']
        by_ = get_parser.parse_args()['by']
        list_ = ["language", "genres", "status", "type"]
        if format_ and by_ and (by_ in list_):
            con = sqlite3.connect('z5239331.db')
            cur = con.cursor()
            # count tv-shows updated within 24 hours
            cur.execute("select last_update from TvShow;")
            time_ = cur.fetchall()
            time_count = 0
            day_ = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
            t_ = datetime.datetime.strptime(day_, '%Y-%m-%d %H:%M:%S')
            for i in range(len(time_)):
                t = datetime.datetime.strptime(time_[i][0], '%Y-%m-%d %H:%M:%S')
                yes_time = t + datetime.timedelta(hours=24)
                if t_ < yes_time:
                    time_count += 1
                    # print('ok')

            # select which value need to statistics
            statistics = {}
            cur.execute("select\"{}\"from TvShow;".format(by_))
            value = cur.fetchall()
            total_num = len(value)  # total tv-shows
            for i in range(len(value)):
                if by_ == "genres":
                    list = json.loads(value[i][0].replace("'", "\""))
                    for item in list:
                        if item not in statistics.keys():
                            statistics[item] = 1
                        else:
                            statistics[item] += 1
                else:
                    if value[i][0] not in statistics.keys():
                        statistics[value[i][0]] = 1
                    else:
                        statistics[value[i][0]] += 1
            con.close()
            for i in statistics.keys():
                statistics[i] = (statistics[i] / total_num) * 100

            if format_ == 'json':
                for i in statistics.keys():
                    statistics[i] = format(statistics[i], '.2f')
                message = {
                    "total": total_num,
                    "total-updated": time_count,
                    "values": statistics
                }
                return make_response(jsonify(message), 200)

            elif format_ == "image":
                labels = [i for i in statistics.keys()]
                values = [k for k in statistics.values()]
                plt.figure(figsize=(15, 8))
                plt.barh(labels, values, height=0.5)
                for i, v in enumerate(values):
                    plt.text(v + .2, i, str(format(v, '.2f')), color='red', fontweight='bold')
                plt.title('Percentage of {} in total TvShows\n\n Total Number of TV shows is {} , {} TV shows updated in the last 24 hours '.format(by_,total_num,time_count))
                plt.ylabel(by_)
                plt.xlabel("Percentage (%)")
                plt.savefig("Q6_z5239331.jpg")
                plt.close()
                filename = 'Q6_z5239331.jpg'
                return send_file(filename, mimetype='image/jpg', cache_timeout=0)
        else:
            message = {'message': 'Bad Request, please check input value.'}
            return make_response(jsonify(message), 400)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
