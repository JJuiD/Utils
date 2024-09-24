import atexit
from datetime import datetime
from flask import Flask, jsonify, render_template, url_for, request
from markupsafe import escape

from plugin.manager import PluginManager, PluginType

app = Flask(__name__)

def format_date(date_str):
    # 将字符串转换为日期对象
    date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
    # 格式化为所需的字符串
    return date.strftime("%Y年%m月%d日 %H:%M:%S")

@app.route('/home')
def home():
    css_url = url_for('static', filename='css/home.css')
    js_url = url_for('static', filename='js/home.js')
    return render_template('home.html', css_url=css_url, js_url=js_url)

@app.route('/home/<page>')
def home_page(page):
    css_url = url_for('static', filename=f'css/{page}.css')
    return render_template(f'home/{page}.html', css_url=css_url, format_date=format_date, data=PluginManager.open(page))

@app.route('/json')
def json_get():
    plugin_key = request.args.get('plugin')
    key = request.args.get('key', default='', type=str)
    return PluginManager.get_plugin(plugin_key).get_item(key)

@app.route('/delete', methods=['POST'])
def delete_item():
    data = request.json

    if data:
        PluginManager.get_plugin(data["plugin"]).delete_item(data["key"])
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
    PluginManager.on_app_quit()

# 注册退出时的清理函数
atexit.register(cleanup)

if __name__ == '__main__':
    app.run(debug=True)
