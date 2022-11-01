
//返回计算出的authorization
function get_token(access_token, modules_path) {
    var CryptoJS = require(modules_path);
    var token_encrypt_password = 'h9zvh6szfeuwnhlg14i';
    return CryptoJS.enc.Utf8.stringify(CryptoJS.AES.decrypt(access_token, token_encrypt_password));
}