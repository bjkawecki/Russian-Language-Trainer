fetch("/stripe-config/")
  .then((result) => {
    return result.json();
  })
  .then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    let buttons = document.getElementsByClassName("submitSubscriptionButton");

    // Create a Checkout Session
    const checkoutSubscription = async (event) => {
      let priceId = event.target.getAttribute("price-id");

      const fetchClientSecret = async () => {
        const response = await fetch("/create-checkout-session/?price=" + priceId, {
          method: "POST",
        });
        const { clientSecret } = await response.json();
        return clientSecret;
      };

      const checkout = await stripe.initEmbeddedCheckout({
        fetchClientSecret,
      });

      // Mount Checkout
      checkout.mount("#checkout");
    };

    for (let button of buttons) {
      button.addEventListener("click", () => {
        let empty_modal = document.getElementById("empty-checkout-modal");
        empty_modal.innerHTML = `
                <div data-modal-backdrop="static" tabindex="-1" id="checkout-modal" aria-hidden="true" class="overflow-y-auto overflow-x-hidden fixed inset-0 top-0 right-0 left-0 z-50 w-full bg-white dark:bg-gray-900 /80">
                    <div class="flex flex-col justify-center items-center">
                        <div class="p-4 mt-0 w-full h-full bg-white rounded-lg border border-gray-200 md:w-1/3 md:h-1/2 md:mt-20 dark:bg-gray-950 dark:border-gray-700">
                            <div id="checkout"></div>
                                <div class="flex justify-end pt-8">
                                    <button type="button" id="close-button" class="px-3 py-2.5 mb-2 text-sm font-semibold bg-white rounded-lg border-gray-200 dark:text-white text-gray-800 focus:outline-none focus:ring-2 me-2 dark:bg-gray-800 dark:hover:bg-gray-700 hover:bg-gray-100 dark:focus:ring-gray-600 focus:ring-gray-300dark:border-gray-700">Abbrechen</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                `;
        let checkout_modal = document.getElementById("checkout-modal");
        let close_button = document.getElementById("close-button");
        checkout_modal.addEventListener("click", () => {
          location.reload();
        });
      });
      button.addEventListener("click", checkoutSubscription);
    }
  });
