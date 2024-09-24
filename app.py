from datetime import datetime
from flask import Flask, jsonify, render_template, url_for
from markupsafe import escape

from plugin.manager import PluginManager, PluginType

app = Flask(__name__)

@app.route('/home')
def home():
    css_url = url_for('static', filename='css/home.css')
    js_url = url_for('static', filename='js/home.js')
    return render_template('home.html', css_url=css_url, js_url=js_url)

@app.route('/home/<page>')
def home_page(page):
    css_url = url_for('static', filename=f'css/{page}.css')
    return render_template(f'home/{page}.html', css_url=css_url, data=PluginManager.open(page))

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

if __name__ == '__main__':
    app.run(debug=True)
