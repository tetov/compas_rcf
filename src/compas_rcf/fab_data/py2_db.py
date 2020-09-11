from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import couchdb


def _create_server(url, port, username, password):
    return couchdb.Server("http://{}:{}@{}:{}/".format(username, password, url, port))


def update_cylinders(
    cylinders, url, port, db_name, username, password, fix_underscores=True
):
    server = _create_server(url, port, username, password)

    if db_name in server:
        db = server[db_name]
    else:
        db = server.create(db_name)

    cylinders_data = [cylinder.to_data() for cylinder in cylinders]

    if fix_underscores:
        upload_data = []
        for data in cylinders_data:
            new_data = {}
            for key in data.keys():
                if key.startswith("_"):
                    new_key = key[1:] + "_"
                    new_data[new_key] = data[key]
                else:
                    new_data[key] = data[key]
            upload_data.append(new_data)
    else:
        upload_data = cylinders_data

    for data in upload_data:
        id_ = data.pop("id_", None) or data.pop("bullet_id", None)
        db[id_] = data
