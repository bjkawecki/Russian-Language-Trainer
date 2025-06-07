fetch("/stripe-config/")
    .then((result) => { return result.json(); })
    .then((data) => {
        // Initialize Stripe.js
        const stripe = Stripe(data.publicKey);

        let buttons = document.getElementsByClassName("submitSubscriptionButton");

        const checkoutSubscription = event => {
            let priceId = event.target.getAttribute("price-id");
            fetch("/create-checkout-session/?price=" + priceId)
                .then((result) => { return result.json(); })
                .then((data) => {
                    console.log(data);
                    // Redirect to Stripe Checkout
                    return stripe.redirectToCheckout({ sessionId: data.sessionId });
                })
                .then((res) => {
                    console.log(res);
                });
        };

        for (let button of buttons) {
            button.addEventListener("click", checkoutSubscription);
        }

    });
