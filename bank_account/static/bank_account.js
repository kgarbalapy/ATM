var cardIdLengthDashed = 19,
    pinLength = 4 ;


function addDashes(){
    var cardNumber = document.getElementById('number');
    var foo = cardNumber.value.split("-").join("");
    if (foo.length > 0) {
        cardNumber.value = foo.match(new RegExp('.{1,4}', 'g')).join("-");
    }
    cardNumber.textContent = cardNumber.value;
}

function deleteDashes(){
    var cardNumber = document.getElementById('number');
    cardNumber.value = cardNumber.value.split("-").join("");
    cardNumber.textContent = cardNumber.value;
    confirm();

}

function confirm() {
    document.getElementById('number').disabled = false
}
function addCode(key, param){
    var number = document.getElementById('number');
    number.value += key;
    if (param==="Dash"){
        if (number.value.length >= cardIdLengthDashed){
            number.value = number.value.slice(0, cardIdLengthDashed);
            document.getElementById('submit').disabled = false;
            return
        }
        addDashes()
    }
    else if (param==="PIN" && number.value.length >= pinLength){
        number.value = number.value.slice(0, pinLength);
        document.getElementById('submit').disabled = false;
    }
}

function validCash(){
    document.getElementById("account").addEventListener("click", function(e){
        var cash = document.getElementById("number").value;
        var msg = document.getElementById("msg");
        if (cash <= 0 ){
            e.preventDefault();
            msg.textContent = 'Message: must be more than 0'
        }else{
            confirm();
        }
    });
}

function reset(){
    document.getElementById('number').value = '';
    document.getElementById('number').disabled = true;
}
