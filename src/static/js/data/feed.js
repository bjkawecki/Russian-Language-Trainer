var eventSource = new EventSource("/feed/update/");

eventSource.onopen = function () {
  console.log("We have an open connection.");
};

eventSource.onmessage = (e) => {
  try {
    const finalData = JSON.parse(e.data); // Parse data safely
    const content = finalData.map((item) => buildDeckList(item)).join(""); // Use map and join for better readability

    const dueCards = finalData.reduce((sum, item) => sum + parseInt(item.due_cards, 10), 0); // Compute total due cards

    // Update DOM elements efficiently
    updateContent("#sse-content", content);
    updateContent("#due_cards", `(${dueCards})`);
  } catch (err) {
    console.error("Failed to process message", err);
  }
};

function updateContent(selector, content) {
  const element = document.querySelector(selector);
  if (element) {
    element.innerHTML = content;
  } else {
    console.warn(`Element not found for selector: ${selector}`);
  }
}

function buildDeckList(item) {
  const {
    id,
    name,
    initial_cards: initialCards,
    due_in_progress_cards: dueInProgressCards,
    due_mastered_cards: dueMasteredCards,
    course__name: courseName,
  } = item;

  return `
  <a href="/review/${id}"
     class="flex justify-between px-3 w-full text-base font-medium bg-white rounded-full border-gray-100 shadow-sm cursor-pointer start-review hover:dark:bg-gray-800 dark:bg-gray-950 hover:bg-white hover:shadow">
      <div class="flex items-center w-full">
          <div class="p-3 text-white dark:text-blue-500">
              <div class="flex overflow-hidden justify-center items-center w-9 h-9 font-extrabold bg-blue-400 rounded-full dark:bg-white">
              ${courseName}
              </div>
          </div>
          <div class="py-3 text-gray-800 dark:text-gray-100">${name}</div>
      </div>
      <div class="flex justify-between items-center">
          <div class="w-10 font-semibold text-center text-blue-500 px-auto">${initialCards}</div>
          <div class="w-10 font-semibold text-center text-red-500 px-auto">${dueInProgressCards}</div>
          <div class="w-10 font-semibold text-center text-green-400 px-auto">${dueMasteredCards}</div>
      </div>
  </a>
`;
}
