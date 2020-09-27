from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import couchdb

from compas_rcf.fab_data import ClayBullet


def _get_client(username, password, url):
    return couchdb.Server("http://{}:{}@{}/".format(username, password, url))


def _get_db(server, db_name, create_db=True):
    if create_db:
        if db_name in server:
            return server[db_name]
        return server.create(db_name)
    else:
        return server[db_name]


def create_fab_elements(username, password, url, db_name, fab_elements):
    client = _get_client(username, password, url)
    db = _get_db(client, db_name, create_db=True)
    for elem in fab_elements:
        id_ = elem.id_
        db[str(id_)] = elem.to_json_str()


def get_fab_elements(username, password, url, db_name, id_list):
    client = _get_client(username, password, url)
    db = _get_db(client, db_name)
    fab_elements = []
    for id_ in id_list:
        fab_elements.append(ClayBullet.from_data(db[str(id)]))

    return fab_elements
