import atexit
from datetime import datetime
from flask import Flask, jsonify, render_template, url_for, request
# from flask_cors import CORS
from markupsafe import escape


from module.manager import ModuleManager
from module.net import AppNet

app = Flask(__name__)

# CORS(app)

@app.route('/')
def home():
    css_url = url_for('static', filename='css/home.css')
    js_url = url_for('static', filename='js/home.js')
    return render_template('home.html', css_url=css_url, js_url=js_url)

@app.route('/home/<page>')
def home_page(page):
    css_url = url_for('static', filename=f'css/{page}.css')
    return render_template(f'home/{page}.html', css_url=css_url, data=ModuleManager.open(page))

@app.route('/rss/page')
def rss_page():
    index = request.args.get('index', type=int)
    return jsonify(ModuleManager.get_module('rss').get_history(index))

@app.route('/json')
def json_get():
    module_key = request.args.get('module')
    key = request.args.get('key', default='', type=str)
    return jsonify(ModuleManager.get_module(module_key).get_item(key))

@app.route('/delete', methods=['POST'])
def delete_item():
    data = request.json

    if request.remote_addr == '127.0.0.1' and data:
        ModuleManager.get_module(data["module"]).delete_item(data["key"])
        return jsonify({"message": "Post successful"}), 204  # 204 No Content
    else:
        return jsonify({"error": "No data received"}), 400  # 返回错误状态码

@app.route('/data')
def data():
    # 构造数据
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    items = [{"title": "Item 1"}, {"title": "Item 2"}]  # 示例项

    # 创建要传递的数据字典
    context = {
        "updatetime": update_time,
        "list": ["1", "2"]  # 确保这个是一个列表
    }

    return render_template('home/rss.html', data=context)  # 这里传递的变量名为 data


def cleanup():
    ModuleManager.on_app_quit()

# 注册退出时的清理函数
atexit.register(cleanup)

if __name__ == '__main__':
    # debug=True 会执行两次
    AppNet.run(app, debug=False)
