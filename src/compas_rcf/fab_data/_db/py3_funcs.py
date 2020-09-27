from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from cloudant import couchdb
from cloudant.document import Document

from compas_rcf.fab_data import ClayBullet
from compas_rcf.utils import CompasObjEncoder


def create_fab_elements(
    username, password, url, db_name, fab_elements, create_db=False
):
    with couchdb(username, password, url=url, encoder=CompasObjEncoder) as client:
        if create_db:
            if db_name in client:
                db = client[db_name]
            else:
                db = client.create_database(db_name)
        else:
            db = client[db_name]

        for elem in fab_elements:
            if isinstance(elem, dict):
                id_ = elem["id_"]
            else:
                id_ = elem.id_
            with Document(db, id_) as doc:
                for key, value in elem.items():
                    doc[key] = value


def update_fab_elements(username, password, url, db_name, ids, new_data):
    with couchdb(username, password, url=url, encoder=CompasObjEncoder) as client:
        db = client[db_name]
        for id_ in ids:
            with Document(db, id_) as elem:
                for key, value in new_data.items():
                    elem[key] = value


def get_fab_elements(username, password, url, db_name, id_list):
    fab_elements = []
    with couchdb(username, password, url=url) as client:
        db = client[db_name]
        for id_ in id_list:
            with Document(db, document_id=id_) as doc:
                fab_elements.append(ClayBullet.from_data(doc))

    return fab_elements
