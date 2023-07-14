var updateBtns = document.getElementsByClassName("update-cart");

for (let i=0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener("click", function () {
		var productId = this.dataset.product
		var action = this.dataset.action
		
		//alert(productId)
		//alert(action)
		
		if (user != "AnonymousUser") {
			sendcartItem(productId, action)
		} else {
			window.location = redirect
		}
		
	})
}


function sendcartItem(productId, action) {
	var url = update_url
	fetch(url, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": csrftoken
		},
		body: JSON.stringify({"productId": productId, "action": action})
	})
	.then(response => {
		return response.json()
	})
	.then(data => {
		console.log(data)
	})
	.catch(error => {
		console.log(error)
	})
}