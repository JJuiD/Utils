'use strict';
function showContent(page, element) {
    // 获取主内容区域的元素
    var mainContent = document.getElementById('main-content');
    if (mainContent == null) return;
    fetch('/'.concat(page))
        .then(function (response) {
            return response.text();
        })
        .then(function (html) {
            mainContent.innerHTML = html;
            if (page == 'rss') {
                showRSSContente(0);
            }
        })
        .catch(function (error) {
            return console.error('Error loading content:', error);
        });
    // 移除所有按钮的 active 类
    var links = document.querySelectorAll('.nav-link');
    links.forEach(function (link) {
        return link.classList.remove('active');
    });
    // 给当前点击的按钮添加 active 类
    element.classList.add('active');
}

function showRSSContente(index) {
    // 获取模板内容
    var template = document.getElementsByTagName('template');
    const content = document.getElementsByClassName('rss-list');

    fetch('/rss_page?index='.concat(index)).then(function (data) {
        for (const item in data) {
            var node = template[0].content.cloneNode(true);
            // 设置邮件项中的数据
            var rssItem = node.querySelector('.item');
            rssItem.setAttribute('onclick', `onUpdateDisplay('rss', 'rss-display', ${item.md5})`);
            rssItem.setAttribute('id', item.md5);
            node.querySelector('.web').textContent = item.web_title;
            node.querySelector('.title').textContent = item.title;
            node.querySelector('.published').textContent = item.published;
            node.querySelector('.jbutton').setAttribute('onclick', `jumpTo('rss', ${item.md5}); event.stopPropagation();`);
            node.querySelector('.cbutton').setAttribute('onclick', `deleteItem('rss', ${item.md5}); event.stopPropagation();`);
            content.appendChild(node);
        }

        if (data.length > 0) {
            showRSSContente(index + 1);
        }
    });
}
// 定义一个可复用的邮件组件
// function createRSSItem(rss) {
//     // 获取模板内容
//     var template = document.getElementsByTagName('template');
//     if (template.length == 0) {
//         return;
//     }
//     var node = template[0].content.cloneNode(true);
//     // 设置邮件项中的数据
//     var rssItem = node.querySelector('.rss-item');
//     rssItem.setAttribute('onclick', "toggleMessage('".concat(rss.id.toString(), "')"));
//     node.querySelector('.rss-web-title').textContent = rss.web_title;
//     node.querySelector('.rss-title').textContent = rss.title;
//     node.querySelector('.rss-published').textContent = rss.published;
//     // 设置邮件内容
//     node.querySelector('.rss-summary').id = rss.id.toString();
//     node.querySelector('.rss-summary').innerHTML = rss.summary;
//     node.querySelector('.rss-summary').style.display = 'none';
//     return node;
// }
// function toggleMessage(id) {
//     const content = document.querySelector('rss-display');
//     var isVisible = content.style.display === 'block';
//     var allContents = document.querySelectorAll('.summary');
//     // 隐藏所有内容
//     allContents.forEach(function (item) { return (item.style.display = 'none'); });
//     // 切换当前内容
//     content.style.display = isVisible ? 'none' : 'block';
//     content.innerHTML = rss.summary;
// }

var display_now_key = '';
var display_next_key = [];
function onUpdateDisplay(module, display_name, key) {
    const content = document.getElementById(display_name);

    var display_key = `${module}_${display_name}_${key}`;
    if (display_now_key == display_key) {
        return;
    } else if (display_now_key != '') {
        display_next_key = [module, display_name, key];
        return;
    }

    display_now_key = display_key;
    console.log('module', module, display_name, key);
    fetch(`/json?module=${module}&key=${key}`)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log('comment', data.summary, data.comment);
            content.innerHTML = data.summary;
            if (typeof data.comment === 'string' && data.comment.length > 0) {
                const iframe = document.createElement('iframe');
                iframe.classList.add('rss-iframe');
                iframe.src = data.comment; // 替换为你想要加载的 URL
                iframe.onload = () => {
                    console.log('Iframe 加载完成!');
                    // iframe.contentWindow.scrollTo(0, 0); // 滚动到顶部
                    // iframe.style.height = '3000px';
                };

                content.appendChild(iframe);
            }
            display_now_key = '';
            content.scrollTop = 0;
            if (display_next_key.length > 0) {
                var args = display_next_key;
                display_next_key = [];
                onUpdateDisplay(args[0], args[1], args[2]);
            }
        });
}

function deleteItem(module, md5) {
    // if (confirm(`确定要删除 ${md5} 吗？`)) {}
    const item = document.getElementById(md5);
    if (item) {
        item.classList.add('fade-out'); // 添加动画类
        // 动画结束后删除元素
        item.addEventListener(
            'transitionend',
            () => {
                fetch(`/delete`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ module: module, key: md5 }),
                }).then(function (data) {
                    item.remove(); // 从 DOM 中删除元素
                });
            },
            { once: true }
        );
    }
}

function jumpTo(module, md5) {}

function onClickModeToggleSwitch() {
    const body = document.querySelector('body');
    var modeText = body.querySelector('.mode-text');
    // 切换body元素的dark类
    body.classList.toggle('dark');
    // 如果body元素包含dark类
    if (body.classList.contains('dark')) {
        modeText.innerText = '白日模式';
    } else {
        modeText.innerText = '夜间模式';
    }
}
