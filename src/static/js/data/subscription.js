function changeSubscriptionLoader(name, cards_count) {
    const counter = `<span id="eventdata">0/${cards_count}</span>`;

    if (document.getElementById(`loading_after_submit_button_${name}`)) {
        const submit_button = document.getElementById(`loading_after_submit_button_${name}`);
        submit_button.classList.remove("dark:bg-blue-600 bg-blue-400", "hover:bg-blue-700");
        submit_button.classList.add("cursor-not-allowed", "bg-blue-500");
        submit_button.disabled = true;
        submit_button.innerHTML = counter;
    }

    let abort_buttons = document.getElementsByClassName("abort_button");
    for (let i = 0; i < abort_buttons.length; i++) {
        abort_buttons[i].setAttribute('disabled', 'disabled');
        abort_buttons[i].classList.remove("dark:bg-gray-800 bg-white ", "dark:hover:bg-gray-700 hover:bg-gray-100 ");
        abort_buttons[i].classList.add("cursor-not-allowed", "bg-gray-700");
    }

    if (document.getElementById(`loading_after_submit_delete_button_${name}`)) {
        const delete_button = document.getElementById(`loading_after_submit_delete_button_${name}`);
        delete_button.classList.remove("hover:bg-red-700", "bg-red-600");
        delete_button.classList.add("cursor-not-allowed", "bg-red-400");
        delete_button.setAttribute('disabled', 'disabled');
        delete_button.innerHTML = counter;
    }

    let eventsource;
    const eventdata = document.getElementById('eventdata');
    eventsource = new EventSource('stream');

    eventsource.onopen = function () {
        console.log("We have an open connection.");
    };
    eventsource.onmessage = event => {
        if (event.data != "has expired") {
            eventdata.innerHTML = event.data + "/" + `${cards_count}`;
        } else {
            eventsource.close();
            console.log("Connection closed.");
        }
    };

    eventsource.onerror = function (e) {
        console.log(`error`, e);
    };
}
