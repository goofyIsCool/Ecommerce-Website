// var updateBtns = document.getElementsByClassName('update-cart')
//
// for (var i = 0; i < updateBtns.length; i++) {
//     updateBtns[i].addEventListener('click', function (){
//         var productId = this.dataset.product
//         var action = this.dataset.action
//         var pack = parseInt(this.dataset.pack)
//
//         console.log("pack: " + pack)
//         try {
//             var inputVal = parseInt(document.getElementById("quantity").value);
//             if (inputVal%pack != 0){
//                 inputVal += pack - inputVal%pack
//             }
//         } catch {
//             var inputVal = pack
//         }
//
//         console.log("inputVal: " + inputVal)
//         console.log("pack: " + pack)
//         if (user == 'AnonymousUser') {
//             addCookieItem(productId, action, inputVal)
//         }
//         else {
//             updateUserOrder(productId, action, inputVal)
//         }
//     })
// }
//
// function addCookieItem(productId, action, quantity) {
//     console.log('User is not authenticated')
//     if (action === 'add'){
//         if (cart[productId] == undefined) {
//             cart[productId] = {'quantity': quantity}
//         }else{
//             cart[productId]['quantity'] += quantity
//         }
//     }
//
//     if (action === 'remove'){
//         cart[productId]['quantity'] -= quantity
//
//         if (cart[productId]['quantity'] <= 0){
//             delete cart[productId]
//         }
//     }
//     else if (action === 'removeAll'){
//         cart[productId]['quantity'] = 0
//         delete cart[productId]
//     }
//
//     console.log("Cart:", cart)
//     document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
//     location.reload()
// }
//
//
// function updateUserOrder(productId, action, inputVal){
// 	console.log('User is authenticated, sending data...')
//
// 		var url = '/update_item/'
//
// 		fetch(url, {
// 			method:'POST',
// 			headers:{
// 				'Content-Type':'application/json',
//                 'X-csrftoken': csrftoken,
//             },
// 			body:JSON.stringify({'productId':productId, 'action':action, 'inputVal':inputVal})
// 		})
//
// 		.then((response) =>{
// 		   return response.json();
// 		})
// 		.then((data) => {
// 		    console.log('Data:', data)
//             location.reload()
// 		});
// }


$('.update-cart').click(function(){
    var productId = $(this).attr("data-productId");
    var action = $(this).attr("data-action");
    var pack = parseInt(this.dataset.pack);
    console.log(pack)

    try {
        var inputVal = parseInt(document.getElementById("quantity"+productId).value);
        console.log("quantity"+productId)
        console.log(inputVal)
        if (inputVal%pack != 0){
            inputVal += pack - inputVal%pack
        }
    } catch {
        var inputVal = pack
    }

    console.log(pack)
    console.log(inputVal)
    var url = '/add_to_cart/'
    $.ajax(
    {
        type:'GET',
        url: url,
        data:{
             productId: productId,
             action: action,
             inputVal: inputVal,
        },
        success: function( data )
        {
            $( '#cartItems' ).text(data);
            console.log(data)
        }
     })
});
