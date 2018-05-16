#!/usr/bin/env python
#-*- coding:utf8 -*-

import pymongo

PREFIX_MAP = {
    'announcement': 'ANNC',
    'area': 'AREA',
    'bankaccount': 'BNKA',
    'casebook': 'CASB',
    'cashflow': 'CSHF',
    'session': 'SESS',
    'department': 'DEPA',
    'diagnose': 'DIAG',
    'discount_catagory': 'DCNT',
    'discount_flow': 'DCTF',
    'doctor': 'DOCA',
    'doctor_title': 'DOCT',
    'feedback': 'FDBK',
    'followup': 'FLUP',
    'good': 'GOOD',
    'hospital': 'HOSP',
    'medicine': 'MEDA',
    'medtemplate': 'MEDT',
    'music': 'MUSC',
    'notice': 'NOTA',
    'notice_status': 'NOTS',
    'notification': 'NOTF',
    'nxapp': 'NAPP',
    'nxauth': 'NATH',
    'nxbutton': 'NBTN',
    'nxevent': 'NEVN',
    'nxgroup': 'NGRP',
    'nxpage': 'NPAG',
    'nxtask': 'NTSK',
    'order': 'ORDA',
    'order_status': 'ORDS',
    'patient': 'PATA',
    'patient_update': 'PATU',
    'personal_account': 'PSAC',
    'prescription': 'PSCR',
    'record': 'RECD',
    'test_result': 'TSTR',
    'test_question': 'TSTQ',
    'test_set': 'TSTS',
    'virtual_flow': 'VRTF',
    'wechatset': 'WCHT',
    'withdrawal': 'WTHD',
    'wxmessage_template': 'WMST',
    'wxmessage': 'WMSG',
    # 我的记录
    'symptom': 'SYMP',
    'recordtpl': 'REPL',
    'text_content': 'TEXT',
    'chat': 'CHAT',
    'nxuser': 'NXUS',
    'im': 'IMUS',

    # 访问记录
    'visit_session': 'VISE',
    'visit_record': 'VIRE',

    # 机器人的消息记录
    'robot_msg': 'RBMS',

    'banner': 'BANN',
    'subscribe_info': 'SUBS',
    'precheck': 'PREC',
    'clinic': 'CLNC',
    'custom_diag': 'CDIG',
    'temp_user': 'TMPU',
    'sleep_record': 'SPRD',
    'archive': 'ARCH',
    'temp_archive': 'TARC',
    'home_doctor': 'HDOC',
    'temp_home_doctor': 'TDOC'
}


class NXMongo(object):

    def init_app(self, dburl=''):
        self.conn = pymongo.MongoClient(dburl, waitQueueTimeoutMS=100)
        self.db = self.conn.get_default_database()
        self.rationalize()

    @property
    def collection_names(self):
        return [t for t in PREFIX_MAP]

    def regist(self, name):
        if name in self.db.nxtable.distinct('name'):
            self.db.nxtable.update({'name': name}, {'$inc': {'max': 1}})
            return {'code': 0, 'msg': '该表单注册信息更新完成'}
        else:
            return {'code': 1, 'msg': '该表不存在，请先创建该表单再注册'}

    def rationalize(self):
        # 若nxtable注册表丢失
        if 'nxtable' not in self.db.collection_names():
            self.db.create_collection('nxtable')

        # 更新各文档的注册信息
        for name in self.collection_names:
            if name not in self.db.collection_names():
                self.add_collection(name)
            ids_dict = list(self.db[name].find({}, {'id': 1, '_id': 0}))
            ids = [item['id'] for item in ids_dict if item is not None and 'id' in item]
            maxid = max(ids) if ids else 0
            self.db.nxtable.update({'name': name}, {'$set': {'name': name, 'max': maxid,
                                                        'prefix': PREFIX_MAP[name]}}, True)

    def gen_nxid(self, name, id):
        # 根据表名和id来生成nxid字符串, 还得进一步考虑特殊的情况
        table = self.db.nxtable.find_one({'name': name}, {'_id': 0, 'prefix': 1})
        if not table:
            # 若表不存在则返回空
            return None
        return table['prefix'].upper() + str(id).zfill(16-len(table['prefix']))

    def new_id(self, name):
        # 生成下一个id
        if name in self.collection_names:
            maxid = self.db.nxtable.find_one({'name': name}, {'_id': 0, 'max': 1})
            return maxid['max']+1 if maxid else 1

    def new_nxid(self, name):
        # 生成下一个nxid, nxuser使用的是doctor和patient的nxid, 所以不要另外生成nxid
        return self.gen_nxid(name, self.new_id(name)) if name != 'nxuser' else None

    def add_collection(self, name):
        # 添加一个文档,这里应该需要有一个过滤的表单，不让随便添加新的表
        if 'nxtable' not in self.db.collection_names():
            self.db.create_collection('nxtable')
        if name not in self.db.collection_names():
            self.db.create_collection(name)
            self.db[name].ensure_index([('id', pymongo.ASCENDING)], unique=True, background=True)
            self.db.nxtable.insert({'name': name, 'max': 0, 'prefix': PREFIX_MAP[name]})
            return {'code': 0, 'msg': '创建成功'}
        else:
            # 若表已经存在，则更新注册信息
            ids_dict = list(self.db[name].find({}, {'id': 1, '_id': 0}))
            ids = [item['id'] for item in ids_dict]
            maxid = max(ids) if ids else 0
            self.db.nxtable.insert({'name': name, 'max': maxid, 'prefix': PREFIX_MAP[name]})
            return {'code': 1, 'msg': '该表已经存在'}

    def clear_collections(self):
        # 清空数据库
        for item in self.collection_names:
            self.db.drop_collection(item)
        # 清空注册信息
        self.db.nxtable.remove({})
        return {'code': 0, 'msg': '清空数据库成功'}

    def drop_collection(self, name):
        # 若文档存在,则删除一个文档
        if name in self.collection_names:
            self.db.drop_collection(name)


if __name__ == '__main__':
    pass