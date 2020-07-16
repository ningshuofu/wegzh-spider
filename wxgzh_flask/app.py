# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

from config import my_port, source_page_path
from utils import get_qr_code, get_ips, spider_data, get_dir, get_dir_name, get_zip_file

app = Flask(__name__)
get_dir(source_page_path)
my_ip = get_ips()


@app.route('/')
def login():
    return render_template('index.html', image_data=get_qr_code())


@app.route('/show_time')
def show_time():
    return render_template('show_time.html', name_l=get_dir_name(source_page_path))


@app.route('/spider')
def spider():
    try:
        args = request.args
        path_prefix, gzh_name = f"{source_page_path}/{args['name']}", args['gzh_name']
        start_page, end_page = int(args['start_page']), int(args['end_page'])
        return spider_data(path_prefix, gzh_name, start_page, end_page)
    except Exception:
        return render_template('index.html', image_data=get_qr_code())


@app.route('/download')
def download():
    try:
        args = request.args
        name = args['name']
        return get_zip_file(name)
    except Exception:
        return render_template('show_time.html', name_l=get_dir_name(source_page_path))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=my_port)
