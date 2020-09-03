const apiPath = '/api'
const loginPath = '/login'
const registerPath = '/register'
const logoutPath = '/logout'
const userHomepagePath = '/home'
const getDashboardsPath = apiPath + '/dashboards'

function logout() {
    axios.delete(logoutPath).then(function () {
        location.href = '/'
    })
}
