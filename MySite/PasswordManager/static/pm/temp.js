// temp JS file

function get_token(account_id) {
    alert("Enter get_token js");
    alert("{% url 'pm:token' 1 %}");
//    $.get("'{% url pm:token " + account_id + " %}'", function (data) {
//        alert(data);
//    });
}

function get_random_token(complexity, length)
{
    // complex 0 = Numbers only
    // complex 1 = Numbers + lower
    // complex 2 = Numbers + lower + upper lettes
    // complex 3 = Numbers + lower + upper lettes + special
    var possible = "";
    if (complexity == 0) {
        possible = '0123456789';
    } else if (complexity == 1) {
        possible = '0123456789abcdefghijklmnopqrstuvwxyz';
    } else if (complexity == 2) {
        possible = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    } else if (complexity == 3) {
        possible = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+{}:"<>?\|[];\',./`~';
    }

    var text = "";
    for( var i=0; i < length; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}