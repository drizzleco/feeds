const apiPath = '/api'
const loginPath = '/login'
const registerPath = '/register'
const logoutPath = '/logout'
const userHomepagePath = '/home'

document.onload = function () {
    $('.sidenav').sidenav();
};

function logout() {
    axios.delete(logoutPath).then(function () {
        location.href = '/'
    })
}
