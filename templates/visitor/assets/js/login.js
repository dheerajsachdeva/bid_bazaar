//JavaScript source code

function validate_form()
{
    var uname = document.forms["login_form"]["uname"].value;
    var pass = document.forms["login_form"]["pass"].value;
    //var atpos = email.indexOf("@");
    //var dotpos = email.lastIndexOf(".");
    // alert("Hello");

    if (uname == null || uname == "") {
        alert("Username field cannot be left blank");
        return false;
    }
    else
        if (pass == null || pass == "") {
            alert("Password field cannot be left blank");
            return false;
        }
        else
            if (uname == "admin" && pass == "admin") {
                window.open("D:/Bid Bazaar/prj_BidBazaar/admin/index.html")
                return true
            }
            else
                if(uname == "user" && pass == "user"){
                    window.open("D:/Bid Bazaar/prj_BidBazaar/user/index.html")
                    return true;
                }
                else{
                    alert("Invalid Credentials");
                    return false;
                }
                

                
}


