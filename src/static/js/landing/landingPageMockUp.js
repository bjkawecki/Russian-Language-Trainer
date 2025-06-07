// let studybutton = document.getElementById("studybutton");
// let input = document.getElementById("input");

// let spinner = `<div class="w-5 h-5 dark:fill-white fill-white spinner"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
//     <path d="M12 19C13.1 19 14 19.9 14 21S13.1 23 12 23 10 22.1 10 21 10.9 19 12 19M12 1C13.1 1 14 1.9 14 3S13.1 5 12 5 10 4.1 10 3 10.9 1 12 1M6 16C7.1 16 8 16.9 8 18S7.1 20 6 20 4 19.1 4 18 4.9 16 6 16M3 10C4.1 10 5 10.9 5 12S4.1 14 3 14 1 13.1 1 12 1.9 10 3 10M6 4C7.1 4 8 4.9 8 6S7.1 8 6 8 4 7.1 4 6 4.9 4 6 4M18 16C19.1 16 20 16.9 20 18S19.1 20 18 20 16 19.1 16 18 16.9 16 18 16M21 10C22.1 10 23 10.9 23 12S22.1 14 21 14 19 13.1 19 12 19.9 10 21 10M18 4C19.1 4 20 4.9 20 6S19.1 8 18 8 16 7.1 16 6 16.9 4 18 4Z" /></svg></div>`;

// let blueButton = `<button type="button" id="studybutton" class="flex justify-center items-center px-3 py-2.5 w-24 h-10 text-sm font-semibold text-center text-white bg-blue-400 rounded-lg shadow dark:text-white dark:bg-blue-600 dark:hover:bg-blue-500 hover-blue-400 active:text-gray-300 focus:ring-2 focus:outline-none dark:focus:ring-blue-800 focus:ring-blue-600">Prüfen</button>`;

// let greenButton = `<button id="greenbutton" class="px-3 py-2.5 h-10 text-sm font-semibold text-white bg-green-400 rounded-lg dark:bg-green-500 hover:bg-green-500 dark:text-white focus:outline-none focus:ring-2 dark:focus:ring-green-800 focus:ring-green-600">Nächste Karte</button>`;

// let redButton = `<button id="redbutton" class="px-3 py-2.5 h-10 text-sm font-semibold text-white rounded-lg dark:text-white dark:bg-red2-500 bg-red2-500 hover:bg-red2-400 focus:outline-none focus:ring-2 dark:focus:ring-red2-800 focus:ring-red2-600">Nächste Karte</button>`;

// let startInput = `<input id="input" class="block p-2.5 my-2 w-full text-lg text-gray-800 bg-white rounded-lg border border-gray-200 placeholder:text-gray-300 dark:text-white dark:bg-gray-700 ps-2.5 dark:focus:ring-blue-500 dark:focus:border-blue-500 focus:ring-blue-600 focus:border-blue-400" type="text" name="card_word_name" maxlength="15" required autocomplete="off">`;

// let correctInput = `<input id="correctinput" disabled class="block p-2.5 my-2 w-full text-lg placeholder-gray-400 text-gray-800 bg-white rounded-lg border-2 border-green-500 ring-green-500 dark:text-white dark:bg-gray-800 ps-2.5 disabled" type="text" name="card_word_name" autocomplete="off" >
//  <span id="icon" class="-ml-9 w-6 h-6 fill-green-500"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
//     <path d="M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M12 20C7.59 20 4 16.41 4 12S7.59 4 12 4 20 7.59 20 12 16.41 20 12 20M16.59 7.58L10 14.17L7.41 11.59L6 13L10 17L18 9L16.59 7.58Z" />
// </svg></span>
// `;

// let showButton = `<button type="button" id="showanswerbutton" class="px-3 py-2.5 text-sm font-semibold text-center text-gray-800 bg-white rounded-lg border border-gray-200 shadow dark:border-gray-600 dark:text-gray-400 dark:bg-gray-900 focus:ring-2 focus:outline-none hover:dark:text-white hover:dark:bg-gray-800 dark:focus:ring-gray-700 focus:ring-gray-100 dark:active:bg-gray-700 active:bg-gray-100 hover:bg-gray-50"><div class="w-5 h-5 dark:fill-gray-400 fill-gray-600"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 22"><title>Lösung zeigen</title><path d="M13 14H9V13H8V9H9V8H13V9H14V13H13M15 17H7V16H5V15H3V14H2V13H1V9H2V8H3V7H5V6H7V5H15V6H17V7H19V8H20V9H21V13H20V14H19V15H17V16H15M12 12V10H10V12M15 15V14H17V13H18V12H19V10H18V9H17V8H15V7H7V8H5V9H4V10H3V12H4V13H5V14H7V15Z" /></svg></div></button>`;

// let wrongInput = `<input id="wronginput" disabled class="block p-2.5 my-2 w-full text-lg placeholder-gray-400 text-gray-400 bg-white rounded-lg border-2 dark:bg-gray-900 border-red2-500 ring-red2-500 ps-2.5 disabled" type="text" autocomplete="off"><span id="icon" class="-ml-9 w-6 h-6 fill-red2-500"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
//     <path d="M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2C6.47,2 2,6.47 2,12C2,17.53 6.47,22 12,22C17.53,22 22,17.53 22,12C22,6.47 17.53,2 12,2M14.59,8L12,10.59L9.41,8L8,9.41L10.59,12L8,14.59L9.41,16L12,13.41L14.59,16L16,14.59L13.41,12L16,9.41L14.59,8Z" />
// </svg>
// </span>`;

// function showSpinner() {
//     let studybutton = document.getElementById("studybutton");
//     studybutton.innerHTML = spinner;
//     setTimeout(processAnswer, 500);
// }

// function showSpinnerKeyboard(event) {
//     if (event.keyCode === 13) {
//         let studybutton = document.getElementById("studybutton");
//         studybutton.innerHTML = spinner;
//         setTimeout(processAnswer, 500);
//     }
// }

// function restart(buttonid, inputid) {
//     let icon = document.getElementById("icon");
//     icon.remove();
//     let greenbutton = document.getElementById(buttonid);
//     greenbutton.outerHTML = blueButton;
//     let studybutton = document.getElementById("studybutton");
//     studybutton.addEventListener("keypress", showSpinner);
//     let startinput = document.getElementById(inputid);
//     startinput.outerHTML = startInput;
//     let showanswerbutton = document.getElementById("showanswerbutton");
//     showanswerbutton.outerHTML = showButton;
//     let newshowanswerbutton = document.getElementById("showanswerbutton");
//     newshowanswerbutton.addEventListener("click", showAnswer);
//     let nextReview = document.getElementById("nextReview");
//     nextReview.innerHTML = "";
// }

// function processAnswer() {
//     let inputValue = document.getElementById("input").value;
//     let input = document.getElementById("input");
//     let studybutton = document.getElementById("studybutton");
//     let nextReview = document.getElementById("nextReview");
//     if (!input.checkValidity()) {
//         input.reportValidity();
//         studybutton.outerHTML = blueButton;
//         let startbutton = document.getElementById("studybutton");
//         startbutton.addEventListener("click", showSpinner);
//         return;
//     }
//     if (inputValue === "учиться") {
//         studybutton.outerHTML = greenButton;
//         input.outerHTML = correctInput;
//         let correctInputElement = document.getElementById("correctinput");
//         correctInputElement.value = inputValue;
//         let greenbutton = document.getElementById("greenbutton");
//         greenbutton.addEventListener("click", restart.bind(null, "greenbutton", "correctinput"));
//         greenbutton.focus();
//         nextReview.innerHTML = "Nächste Abfrage: 10 Minuten";
//     } else {
//         studybutton.outerHTML = redButton;
//         input.outerHTML = wrongInput;
//         document.getElementById("wronginput").value = inputValue || "";
//         let redbutton = document.getElementById("redbutton");
//         redbutton.addEventListener("click", restart.bind(null, "redbutton", "wronginput"));
//         redbutton.focus();
//         nextReview.innerHTML = "Nächste Abfrage: 0 Minuten";
//     }

// }

// studybutton.addEventListener("click", showSpinner);
// input.addEventListener("keydown", showSpinnerKeyboard);
// let showAnswerButton = document.getElementById("showanswerbutton");
// showAnswerButton.addEventListener("click", showAnswer);

// function showAnswer() {
//     let input = document.getElementById("input");
//     let studybutton = document.getElementById("studybutton");
//     studybutton.outerHTML = redButton;
//     input.outerHTML = wrongInput;
//     document.getElementById("wronginput").value = "учи́ться";
//     let redbutton = document.getElementById("redbutton");
//     redbutton.addEventListener("click", restart.bind(null, "redbutton", "wronginput"));
//     redbutton.focus();
//     let showAnswerButton = document.getElementById("showanswerbutton");
//     showAnswerButton.setAttribute("disabled", true);
//     showAnswerButton.classList.add("cursor-not-allowed");
//     showAnswerButton.classList.remove("dark:active:bg-gray-700 active:bg-gray-100");
//     showAnswerButton.removeEventListener("click", showAnswer);
//     let nextReview = document.getElementById("nextReview");
//     nextReview.innerHTML = "Nächste Abfrage: 0 Minuten";
// }
