let countdown = 5;
setInterval(() => {
    countdown = countdown - 1;
    let seconds = document.getElementById("seconds");
    seconds.innerHTML = countdown;
    if (countdown < 1) {
        location.href = "/";
    }
}, 1_000);
