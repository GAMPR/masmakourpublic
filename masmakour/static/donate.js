

console.log("Sanity check!");

// Get Stripe publishable key
fetch("/config/")
	.then((result) => { return result.json(); })
	.then((data) => {
		// Initialize Stripe.js
		const stripe = Stripe(data.publicKey);

		// new
		// Event handler
		let submitBtn = document.querySelector("#donBtn");
		if (submitBtn !== null) {
			submitBtn.addEventListener("click", () => {
				// Get Checkout Session ID
				fetch("/donate_checkout/")
					.then((result) => { return result.json(); })
					.then((data) => {
						console.log(data);
						// Redirect to Stripe Checkout
						return stripe.redirectToCheckout({sessionId: data.sessionId})
					})
					.then((res) => {
						console.log(res);
					});
			});
		}
	});

