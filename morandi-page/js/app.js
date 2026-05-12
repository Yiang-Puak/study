/**
 * 莫兰迪面试手册 SPA
 * 路由系统 + Markdown 内容加载 + 莫兰迪阅读体验
 */

(function() {
    'use strict';

    // ===================== 全局状态 =====================
    let contentIndex = [];
    let currentRoute = '';

    // DOM 缓存
    const app = document.getElementById('app');
    const navbar = document.getElementById('navbar');
    const navMenu = document.getElementById('navMenu');
    const navToggle = document.getElementById('navToggle');
    const backToTop = document.getElementById('backToTop');
    const pageLoader = document.getElementById('pageLoader');
    const mainFooter = document.getElementById('mainFooter');
    const navLinks = document.querySelectorAll('.nav-link');

    // ===================== 配置 =====================
    const MD_BASE = (() => {
        const host = window.location.hostname;
        const path = window.location.pathname;
        if (host.includes('github.io') || path.includes('/study/')) {
            return '/study/content-md';
        }
        return '../docs';
    })();

    const CATEGORIES = {
        'ai-agent': {
            label: 'AI Agent 面试实践',
            filter: item => item.path.includes('AI Agent') || item.path.includes('agent'),
            accent: '#8FA3AD',
            bg: 'rgba(143, 163, 173, 0.12)'
        },
        'python': {
            label: 'Python 面试实践',
            filter: item => item.path.includes('Python'),
            accent: '#B0A3B8',
            bg: 'rgba(176, 163, 184, 0.12)'
        },
        'git': {
            label: 'Git 面试实践',
            filter: item => item.path.includes('Git'),
            accent: '#9CA896',
            bg: 'rgba(156, 168, 150, 0.12)'
        },
        'overview': {
            label: '综合',
            filter: item => !item.path.includes('AI Agent') && !item.path.includes('Python') && !item.path.includes('Git'),
            accent: '#B8A898',
            bg: 'rgba(184, 168, 152, 0.12)'
        }
    };

    // ===================== 工具函数 =====================
    function showLoader() { pageLoader.classList.add('active'); }
    function hideLoader() { pageLoader.classList.remove('active'); }

    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // ===================== 内容索引 =====================
    async function loadContentIndex() {
        try {
            const res = await fetch('content-index.json');
            contentIndex = await res.json();
        } catch (e) {
            console.error('加载索引失败:', e);
            contentIndex = [];
        }
    }

    // ===================== 路由系统 =====================
    const router = {
        navigate(path) {
            window.location.hash = path;
        },

        parse() {
            const hash = window.location.hash.slice(1) || '/';
            const [route, query] = hash.split('?');
            const params = {};
            if (query) {
                query.split('&').forEach(pair => {
                    const [k, v] = pair.split('=');
                    params[decodeURIComponent(k)] = decodeURIComponent(v || '');
                });
            }
            return { route, params };
        },

        resolve() {
            const { route, params } = this.parse();
            currentRoute = route;

            // 更新导航高亮
            navLinks.forEach(link => {
                link.classList.remove('active');
                const linkRoute = link.dataset.route;
                if (linkRoute && (route === linkRoute || route.startsWith(linkRoute + '/'))) {
                    link.classList.add('active');
                }
            });

            // 显示/隐藏页脚
            if (route === '/read') {
                mainFooter.style.display = 'none';
            } else {
                mainFooter.style.display = '';
            }

            // 渲染视图
            app.innerHTML = '';
            window.scrollTo(0, 0);

            if (route === '/' || route === '') {
                renderHome();
            } else if (route === '/browse') {
                renderBrowse('all');
            } else if (route.startsWith('/category/')) {
                const cat = route.replace('/category/', '');
                renderBrowse(cat);
            } else if (route === '/read') {
                renderRead(params.path || '');
            } else {
                renderHome();
            }
        }
    };

    // ===================== 首页视图 =====================
    function renderHome() {
        const view = document.createElement('div');
        view.className = 'view';
        view.innerHTML = `
            <section class="hero" id="hero">
                <div class="hero-bg-shape shape-1"></div>
                <div class="hero-bg-shape shape-2"></div>
                <div class="hero-bg-shape shape-3"></div>
                <div class="hero-content">
                    <div class="hero-badge">◐ 持续更新中 · 43 篇文章</div>
                    <h1 class="hero-title">
                        <span class="title-line">AI 面试</span>
                        <span class="title-line accent">冲刺手册</span>
                    </h1>
                    <p class="hero-subtitle">
                        Python · AI Agent · Git · 数据结构<br>
                        以莫兰迪般的沉静，构建知识的厚度
                    </p>
                    <div class="hero-actions">
                        <a href="#/browse" class="btn btn-primary" onclick="router.navigate('/browse'); return false;">开始学习</a>
                        <a href="https://yiang-puak.github.io/study/" target="_blank" class="btn btn-secondary">MkDocs 版</a>
                    </div>
                    <div class="hero-stats">
                        <div class="stat-item"><span class="stat-number">30+</span><span class="stat-label">核心章节</span></div>
                        <div class="stat-divider"></div>
                        <div class="stat-item"><span class="stat-number">3</span><span class="stat-label">知识模块</span></div>
                        <div class="stat-divider"></div>
                        <div class="stat-item"><span class="stat-number">43</span><span class="stat-label">学习文章</span></div>
                    </div>
                </div>
                <div class="scroll-indicator">
                    <span class="scroll-text">向下滚动</span>
                    <div class="scroll-line"></div>
                </div>
            </section>

            <section class="categories" id="categories">
                <div class="section-container">
                    <div class="section-header">
                        <span class="section-tag">知识分类</span>
                        <h2 class="section-title">系统化的面试知识体系</h2>
                        <p class="section-desc">点击分类，开始你的面试冲刺之旅</p>
                    </div>
                    <div class="category-grid">
                        <div class="category-card" data-category="ai-agent" onclick="router.navigate('/category/ai-agent')">
                            <div class="card-accent" style="background: #9CAFB7;"></div>
                            <div class="card-icon">
                                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                    <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>
                                    <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                                    <line x1="12" x2="12" y1="19" y2="22"/>
                                </svg>
                            </div>
                            <h3 class="card-title">AI Agent 面试实践</h3>
                            <p class="card-desc">Agent 架构、ReAct 模式、记忆系统、RAG 检索、LangChain / LangGraph、Harness 工程</p>
                            <div class="card-meta">
                                <span class="meta-tag">${contentIndex.filter(CATEGORIES['ai-agent'].filter).length} 篇文章</span>
                                <span class="meta-tag">代码实践</span>
                            </div>
                            <ul class="card-list">
                                <li>ReAct Agent 与 MultiAgent 协作</li>
                                <li>记忆系统与 Context 压缩</li>
                                <li>RAG 完整链路实现</li>
                                <li>Harness Subagent 与 DispatchMap</li>
                            </ul>
                        </div>

                        <div class="category-card" data-category="python" onclick="router.navigate('/category/python')">
                            <div class="card-accent" style="background: #B8A9C9;"></div>
                            <div class="card-icon">
                                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                    <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
                                    <polyline points="14 2 14 8 20 8"/>
                                    <path d="m9 13 2 2 4-4"/>
                                </svg>
                            </div>
                            <h3 class="card-title">Python 面试实践</h3>
                            <p class="card-desc">语言特性、数据结构、标准库、高频手撕算法、进阶 asyncio 与内存管理</p>
                            <div class="card-meta">
                                <span class="meta-tag">${contentIndex.filter(CATEGORIES['python'].filter).length} 篇文章</span>
                                <span class="meta-tag">手撕代码</span>
                            </div>
                            <ul class="card-list">
                                <li>零基础入门到语言特性</li>
                                <li>LRU 缓存、快排、TopK、BST</li>
                                <li>asyncio 异步编程</li>
                                <li>GIL 与内存管理深入</li>
                            </ul>
                        </div>

                        <div class="category-card" data-category="git" onclick="router.navigate('/category/git')">
                            <div class="card-accent" style="background: #A8B5A0;"></div>
                            <div class="card-icon">
                                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                    <circle cx="12" cy="18" r="3"/>
                                    <circle cx="6" cy="6" r="3"/>
                                    <circle cx="18" cy="6" r="3"/>
                                    <path d="M6 9v3c0 1.1.9 2 2 2h4"/>
                                    <path d="M18 9v3c0 1.1-.9 2-2 2h-4"/>
                                </svg>
                            </div>
                            <h3 class="card-title">Git 面试实践</h3>
                            <p class="card-desc">核心概念、常用命令、进阶操作、团队协作与冲突解决策略</p>
                            <div class="card-meta">
                                <span class="meta-tag">${contentIndex.filter(CATEGORIES['git'].filter).length} 篇文章</span>
                                <span class="meta-tag">实战导向</span>
                            </div>
                            <ul class="card-list">
                                <li>Git 核心原理与对象模型</li>
                                <li>分支策略与 Rebase 工作流</li>
                                <li>Cherry-pick 与 Stash 高级用法</li>
                                <li>团队协作最佳实践</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            <section class="features" id="features">
                <div class="section-container">
                    <div class="section-header">
                        <span class="section-tag">学习特性</span>
                        <h2 class="section-title">为深度阅读而设计</h2>
                        <p class="section-desc">每一个细节都经过打磨，让长时间学习成为一种享受</p>
                    </div>
                    <div class="feature-list">
                        <div class="feature-item">
                            <div class="feature-number">01</div>
                            <div class="feature-content">
                                <h3>莫兰迪配色方案</h3>
                                <p>低饱和度色彩减少视觉疲劳，柔和对比让文字清晰易读，适合数小时连续学习。</p>
                            </div>
                        </div>
                        <div class="feature-item">
                            <div class="feature-number">02</div>
                            <div class="feature-content">
                                <h3>代码即文档</h3>
                                <p>每个知识点都配有可运行代码实践，从理论到实战无缝衔接，拒绝纸上谈兵。</p>
                            </div>
                        </div>
                        <div class="feature-item">
                            <div class="feature-number">03</div>
                            <div class="feature-content">
                                <h3>即时渲染阅读</h3>
                                <p>Markdown 即时渲染，代码高亮、表格美化，无需跳转即可沉浸阅读。</p>
                            </div>
                        </div>
                        <div class="feature-item">
                            <div class="feature-number">04</div>
                            <div class="feature-content">
                                <h3>结构化导航</h3>
                                <p>侧边目录树快速切换文章，面包屑定位当前位置，学习路径清晰可控。</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="timeline-section" id="timeline">
                <div class="section-container">
                    <div class="section-header">
                        <span class="section-tag">学习路线</span>
                        <h2 class="section-title">推荐学习路径</h2>
                    </div>
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-dot" style="background: #9CAFB7;"></div>
                            <div class="timeline-content">
                                <span class="timeline-phase">第一阶段</span>
                                <h4>夯实基础</h4>
                                <p>Python 语言特性、数据结构、Git 核心概念。建立扎实的编程基础与工具链认知。</p>
                            </div>
                        </div>
                        <div class="timeline-item">
                            <div class="timeline-dot" style="background: #B8A9C9;"></div>
                            <div class="timeline-content">
                                <span class="timeline-phase">第二阶段</span>
                                <h4>算法进阶</h4>
                                <p>高频手撕代码题：LRU、快排、TopK、BST、动态规划。掌握面试算法核心。</p>
                            </div>
                        </div>
                        <div class="timeline-item">
                            <div class="timeline-dot" style="background: #C4B7A6;"></div>
                            <div class="timeline-content">
                                <span class="timeline-phase">第三阶段</span>
                                <h4>Agent 体系</h4>
                                <p>深入 ReAct、记忆系统、RAG、LangGraph、Harness。构建完整 AI Agent 知识树。</p>
                            </div>
                        </div>
                        <div class="timeline-item">
                            <div class="timeline-dot" style="background: #A8B5A0;"></div>
                            <div class="timeline-content">
                                <span class="timeline-phase">第四阶段</span>
                                <h4>模拟冲刺</h4>
                                <p>综合模拟题库、面试问答准备、遗漏检查。查漏补缺，自信上阵。</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        `;
        app.appendChild(view);
    }

    // ===================== 浏览页视图 =====================
    function renderBrowse(category) {
        const view = document.createElement('div');
        view.className = 'view browse-section';

        const catKeys = ['all', 'ai-agent', 'python', 'git', 'overview'];
        const catLabels = { 'all': '全部', 'ai-agent': 'AI Agent', 'python': 'Python', 'git': 'Git', 'overview': '综合' };

        let items = contentIndex;
        if (category !== 'all' && CATEGORIES[category]) {
            items = contentIndex.filter(CATEGORIES[category].filter);
        }

        const filtersHtml = catKeys.map(k =>
            `<button class="filter-btn ${k === category ? 'active' : ''}" onclick="router.navigate('/category/${k}')">${catLabels[k]}</button>`
        ).join('');

        const articlesHtml = items.map((item, i) => `
            <a class="article-item" href="#/read?path=${encodeURIComponent(item.path)}" onclick="router.navigate('/read?path=${encodeURIComponent(item.path)}'); return false;">
                <span class="article-number">${String(i + 1).padStart(2, '0')}</span>
                <div class="article-info">
                    <h4>${escapeHtml(item.title)}</h4>
                    <p>${escapeHtml(item.path)}</p>
                </div>
            </a>
        `).join('');

        view.innerHTML = `
            <div class="section-container">
                <nav class="breadcrumb">
                    <a href="#/" onclick="router.navigate('/'); return false;">首页</a>
                    <span class="breadcrumb-sep">/</span>
                    <span>${catLabels[category] || '全部文章'}</span>
                </nav>
                <div class="section-header" style="text-align: left; margin-bottom: var(--space-xl);">
                    <h2 class="section-title">${catLabels[category] || '全部文章'}</h2>
                    <p class="section-desc" style="margin: 0;">共 ${items.length} 篇文章</p>
                </div>
                <div class="category-filter">${filtersHtml}</div>
                <div class="article-list">${articlesHtml}</div>
            </div>
        `;
        app.appendChild(view);
    }

    // ===================== 阅读页视图 =====================
    async function renderRead(path) {
        if (!path) {
            router.navigate('/browse');
            return;
        }

        showLoader();

        const view = document.createElement('div');
        view.className = 'view reader-section';

        // 找到当前文章信息
        const currentItem = contentIndex.find(item => item.path === path);
        const title = currentItem ? currentItem.title : path.split('/').pop().replace('.md', '');

        // 侧边栏目录（同分类文章）
        let relatedItems = contentIndex;
        for (const [key, cat] of Object.entries(CATEGORIES)) {
            if (cat.filter(currentItem || { path })) {
                relatedItems = contentIndex.filter(cat.filter);
                break;
            }
        }

        const sidebarHtml = `
            <div class="reader-sidebar" id="readerSidebar">
                <div class="sidebar-title">目录</div>
                <ul class="sidebar-tree">
                    ${relatedItems.map(item => `
                        <li>
                            <a href="#/read?path=${encodeURIComponent(item.path)}"
                               class="${item.path === path ? 'active' : ''}"
                               onclick="router.navigate('/read?path=${encodeURIComponent(item.path)}'); return false;"
                               title="${escapeHtml(item.title)}">
                                ${escapeHtml(item.title)}
                            </a>
                        </li>
                    `).join('')}
                </ul>
            </div>
            <button class="reader-sidebar-toggle" id="sidebarToggle" onclick="document.getElementById('readerSidebar').classList.toggle('open')">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12h16M4 6h16M4 18h16"/></svg>
            </button>
        `;

        // 加载并渲染 Markdown
        let markdownHtml = '<p style="color: var(--text-tertiary);">加载内容失败，请返回重试。</p>';
        try {
            const mdPath = `${MD_BASE}/${path}`;
            const res = await fetch(mdPath);
            if (res.ok) {
                const mdText = await res.text();
                if (typeof marked !== 'undefined') {
                    markdownHtml = marked.parse(mdText);
                } else {
                    markdownHtml = `<pre>${escapeHtml(mdText)}</pre>`;
                }
            } else {
                markdownHtml = `<p style="color: var(--text-tertiary);">无法加载文件：<code>${escapeHtml(mdPath)}</code> (HTTP ${res.status})</p>`;
            }
        } catch (e) {
            markdownHtml = `<p style="color: var(--text-tertiary);">加载异常：${escapeHtml(e.message)}</p>`;
        }

        view.innerHTML = sidebarHtml + `
            <div class="reader-content">
                <nav class="breadcrumb" style="margin-bottom: var(--space-md);">
                    <a href="#/" onclick="router.navigate('/'); return false;">首页</a>
                    <span class="breadcrumb-sep">/</span>
                    <a href="#/browse" onclick="router.navigate('/browse'); return false;">文章</a>
                    <span class="breadcrumb-sep">/</span>
                    <span>${escapeHtml(title)}</span>
                </nav>
                <div class="reader-header">
                    <h1 class="reader-title">${escapeHtml(title)}</h1>
                    <div class="reader-meta">${escapeHtml(path)}</div>
                </div>
                <div class="markdown-body">${markdownHtml}</div>
            </div>
        `;

        app.appendChild(view);
        hideLoader();

        // 代码高亮
        if (typeof hljs !== 'undefined') {
            view.querySelectorAll('pre code').forEach(block => {
                hljs.highlightElement(block);
            });
        }

        // 点击外部关闭移动端侧边栏
        view.addEventListener('click', (e) => {
            const sidebar = document.getElementById('readerSidebar');
            const toggle = document.getElementById('sidebarToggle');
            if (sidebar && sidebar.classList.contains('open') && !sidebar.contains(e.target) && !toggle.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        });
    }

    // ===================== UI 交互 =====================
    function handleScroll() {
        const y = window.scrollY;
        navbar.classList.toggle('scrolled', y > 60);
        backToTop.classList.toggle('visible', y > 400);
    }

    function toggleMobileMenu() {
        navMenu.classList.toggle('active');
        navToggle.classList.toggle('active');
    }

    function scrollToTop() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // ===================== 初始化 =====================
    async function init() {
        await loadContentIndex();

        // 路由监听
        window.addEventListener('hashchange', () => router.resolve());

        // 滚动监听
        window.addEventListener('scroll', throttle(handleScroll, 100));

        // 移动端菜单
        if (navToggle) {
            navToggle.addEventListener('click', toggleMobileMenu);
        }

        // 回到顶部
        backToTop.addEventListener('click', scrollToTop);

        // 初始路由
        router.resolve();
        handleScroll();
    }

    // DOM Ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // 暴露 router 到全局供 HTML 内联事件使用
    window.router = router;
})();
