function showContent(page: string, element: HTMLElement) {
    // 获取主内容区域的元素
    let mainContent = document.getElementById('main-content');
    if (mainContent == null) return;

    fetch(`/home/${page}`)
        .then((response) => response.text())
        .then((html) => {
            mainContent.innerHTML = html;
        })
        .catch((error) => console.error('Error loading content:', error));

    // 移除所有按钮的 active 类
    let links = document.querySelectorAll('.nav-link');
    links.forEach((link) => link.classList.remove('active'));

    // 给当前点击的按钮添加 active 类
    element.classList.add('active');
}

// 定义一个可复用的邮件组件
function createRSSItem(rss: { id: number; web_title: string; title: string; published: string; summary: string }) {
    // 获取模板内容
    let template = document.getElementsByTagName('template');
    if (template.length == 0) {
        return;
    }

    let node = template[0].content.cloneNode(true) as HTMLElement;

    // 设置邮件项中的数据
    let rssItem = node.querySelector('.rss-item');
    rssItem!.setAttribute('onclick', `toggleMessage('${rss.id.toString()}')`);
    node.querySelector('.rss-web-title')!.textContent = rss.web_title;
    node.querySelector('.rss-title')!.textContent = rss.title;
    node.querySelector('.rss-published')!.textContent = rss.published;
    // 设置邮件内容
    node.querySelector('.rss-summary')!.id = rss.id.toString();
    node.querySelector('.rss-summary')!.innerHTML = rss.summary;
    node.querySelector<HTMLElement>('.rss-summary')!.style.display = 'none';

    return node;
}

function toggleMessage(id: string) {
    let content = document.getElementById(id);
    if (content == null) {
        return;
    }
    let isVisible = content.style.display === 'block';
    let allContents = document.querySelectorAll<HTMLElement>('.rss-summary');

    // 隐藏所有内容
    allContents.forEach((item) => (item.style.display = 'none'));

    // 切换当前内容
    content.style.display = isVisible ? 'none' : 'block';
}
