function testAPI(callback) {
    user = facebookAPI();
    callback(user);
}

function photoAPI(user, callback) {
    callback(user.userid);
}

function facebookAPI() {
    x = {};
    x.userid = '12345' ;
    return x;
}