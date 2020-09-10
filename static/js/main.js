const apiPath = '/api'
const loginPath = '/login'
const registerPath = '/register'
const logoutPath = '/logout'
const userHomepagePath = '/home'
const getDashboardsPath = apiPath + '/dashboards'
const createDashboardPath = apiPath + '/dashboards/new'
const getFeedsPath = apiPath + '/feeds'
const createFeedPath = apiPath + '/feeds/new'
const tokensPath = apiPath + '/tokens'
const profilePath = apiPath + '/me'

function logout() {
    axios.delete(logoutPath).then(function () {
        location.href = '/'
    })
}

function toLocaleString(date) {
    return new Date(date).toLocaleString()
}

function timeDiffFromNow(date) {
    let seconds = (new Date().getTime() - new Date(date).getTime()) / 1000
    let d = Math.floor(seconds / (3600 * 24));
    let h = Math.floor(seconds % (3600 * 24) / 3600);
    let m = Math.floor(seconds % 3600 / 60);
    let s = Math.floor(seconds % 60);

    if (d)
        return d + (d == 1 ? " day" : " days")
    if (h)
        return h + (h == 1 ? " hour" : " hours")
    if (m)
        return m + (m == 1 ? " minute" : " minutes")
    if (s)
        return s + (s == 1 ? " second" : " seconds")
}
