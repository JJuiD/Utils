"use strict";
function showContent(page, element) {
    // 获取主内容区域的元素
    var mainContent = document.getElementById('main-content');
    if (mainContent == null)
        return;
    fetch("/home/".concat(page))
        .then(function (response) { return response.text(); })
        .then(function (html) {
        mainContent.innerHTML = html;
    })
        .catch(function (error) { return console.error('Error loading content:', error); });
    // 移除所有按钮的 active 类
    var links = document.querySelectorAll('.nav-link');
    links.forEach(function (link) { return link.classList.remove('active'); });
    // 给当前点击的按钮添加 active 类
    element.classList.add('active');
}
// 定义一个可复用的邮件组件
function createRSSItem(rss) {
    // 获取模板内容
    var template = document.getElementsByTagName('template');
    if (template.length == 0) {
        return;
    }
    var node = template[0].content.cloneNode(true);
    // 设置邮件项中的数据
    var rssItem = node.querySelector('.rss-item');
    rssItem.setAttribute('onclick', "toggleMessage('".concat(rss.id.toString(), "')"));
    node.querySelector('.rss-web-title').textContent = rss.web_title;
    node.querySelector('.rss-title').textContent = rss.title;
    node.querySelector('.rss-published').textContent = rss.published;
    // 设置邮件内容
    node.querySelector('.rss-summary').id = rss.id.toString();
    node.querySelector('.rss-summary').innerHTML = rss.summary;
    node.querySelector('.rss-summary').style.display = 'none';
    return node;
}
function toggleMessage(id) {
    var content = document.getElementById(id);
    if (content == null) {
        return;
    }
    var isVisible = content.style.display === 'block';
    var allContents = document.querySelectorAll('.rss-summary');
    // 隐藏所有内容
    allContents.forEach(function (item) { return (item.style.display = 'none'); });
    // 切换当前内容
    content.style.display = isVisible ? 'none' : 'block';
}
