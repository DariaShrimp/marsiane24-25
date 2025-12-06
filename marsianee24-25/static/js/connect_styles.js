const cssFiles = [
    '/static/css/base.css',
    '/static/css/body.css',
    '/static/css/button.css',
    '/static/css/cards.css',
    '/static/css/color.css',
    '/static/css/nav.css',
    '/static/css/text.css'
];

cssFiles.forEach(file => {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = file;
    document.head.appendChild(link);
});