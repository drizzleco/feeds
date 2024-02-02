$(document).ready(function () {
    if (!location.href.match('localhost') && location.href.match('http:'))
        location.href = window.location.href.replace('http', 'https')
    setTimeout(function () {
        M.AutoInit();
    }, 150)
});
