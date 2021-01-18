var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function (){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log('USER:', user)
        if (user == 'AnonymousUser') {
            addCookieItem()
        }
        else {
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productId, action) {
    console.log('User is not authenticated')

    if (action =='add'){
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'add'){
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0){
            console.log("Remove Item")
            delete cart[productId]
        }
    }

    console.log("Cart:", cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
}
