#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import os

# from float import float, getcontext
#
# getcontext().prec = 6

headers = ['mSigma', 'Observed Intens', 'Observed m/z', 'calc. m/z', 'err mDa', 'err ppm', 'sum formula', 'Br', 'C',
           'Cl', 'H', 'N', 'O', 'S', 'rdb', 'DBE', 'H/C', 'O/C', 'intensity', 'N/C', 'KM', 'KMD', 'Z', 'type']

types = ['Br', 'Cl', 'N', 'O', 'S']

input_path = '../resource/30.csv'
with open(input_path) as f:
    f_csv = csv.reader(f)
    # headers = next(f_csv)
    # print headers
    next(f_csv)
    body = list()
    for row in f_csv:
        body.append(row)


def index(fn):
    return headers.index(fn)


def get_str_value(row, fn):
    return str(row[index(fn)])


def get_float_value(row, fn):
    return float(row[index(fn)])


def get_int_value(row, fn):
    return int(row[index(fn)])


def verify(num):
    return ('float', 'int')[round(float(num)) == float(num)]


def gen_dbe():
    print body[0][index('DBE')], body[0][index('H/C')], body[0][index('O/C')], body[0][index('intensity')]

    b = [float(r[index('Observed Intens')]) for r in body]
    max_b = max(b) / 40
    for r in body:
        r[index('DBE')] = get_float_value(r, 'rdb') - 0.5
        r[index('H/C')] = get_float_value(r, 'H') / get_float_value(r, 'C')
        r[index('O/C')] = get_float_value(r, 'O') / get_float_value(r, 'C')
        r[index('N/C')] = get_float_value(r, 'N') / get_float_value(r, 'C')
        r[index('intensity')] = get_float_value(r, 'Observed Intens') / max_b

    HC_filter = [r for r in body if 0.333 <= get_float_value(r, 'H/C') <= 2.25]
    OC_filter = [r for r in HC_filter if 0.1 <= get_float_value(r, 'O/C') <= 1]
    NC_filter = [r for r in OC_filter if get_float_value(r, 'N/C') < 0.5]
    DBE_filter = [r for r in NC_filter if verify(get_str_value(r, 'DBE')) == 'int']

    return DBE_filter


def gen_observers():
    filter8 = list()
    observer_group = dict()

    for r in body_filter:
        key = get_str_value(r, 'Observed m/z')
        if observer_group.get(key):
            observer_group.get(key).append(r)
        else:
            observers = list()
            observers.append(r)
            observer_group.update({key: observers})

    min_abs_obs = dict()
    for k, v in observer_group.iteritems():
        min_abs_ob = min([abs(get_float_value(ob, 'err ppm')) for ob in v])
        min_abs_obs.update({k: min_abs_ob})

    for r in body_filter:
        ob = get_str_value(r, 'Observed m/z')
        if get_int_value(r, 'Br') == 0 \
                and get_int_value(r, 'Cl') == 0 \
                and get_float_value(r, 'Observed m/z') <= 500:
            if abs(get_float_value(r, 'err ppm')) == min_abs_obs.get(ob):
                filter8.append(r)
        else:
            filter8.append(r)
    return filter8


def gen_km():
    for observer in body_observers:
        observer[index('KM')] = get_float_value(observer, 'Observed m/z') * 14 / 14.01565
        observer[index('KMD')] = (round(get_float_value(observer, 'KM')) - get_float_value(observer, 'KM')) * 1000
        observer[index('DBE')] = get_int_value(observer, 'DBE')
        Z = get_int_value(observer, 'DBE') - 2 * get_int_value(observer, 'C')
        observer.append(Z)
        Type = concat_type(observer)
        observer.append(Type)
    return body_observers


def concat_type(observer):
    origin_str = get_str_value(observer, 'Z')
    for i in types:
        if get_int_value(observer, i) == 0:
            continue
        if get_int_value(observer, i) == 1:
            origin_str += " " + i
            continue
        origin_str += " " + i + get_str_value(observer, i)
    return origin_str


if __name__ == '__main__':
    body_filter = gen_dbe()
    body_observers = gen_observers()
    final = gen_km()
    print len(final)
    for f in final:
        print f

    out_dir = "../output"
    # abs_out_dir = os.path.abspath(out_dir)
    # print abs_out_dir
    file_name = os.path.basename(input_path)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(os.path.join(out_dir, file_name), 'w') as ou:
        w_csv = csv.writer(ou)
        w_csv.writerow(headers)
        w_csv.writerows(final)
