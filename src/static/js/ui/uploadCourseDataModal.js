function open_create_course_modal() {
  modal = document.getElementById("upload_courses_modal");
  modal.classList.remove("hidden");
  modal.classList.add("flex");

  let eventsource;
  let eventdata = document.getElementById("eventdata");
  let create_course_modal_content = document.getElementById("create_course_modal_content");
  eventsource = new EventSource("create-course/stream/");

  eventsource.onopen = function () {
    console.log("We have an open connection.");
  };
  eventsource.onmessage = (event) => {
    parsed_data = JSON.parse(event.data);
    if (parsed_data["course_progress"] != "has expired") {
      eventdata.innerHTML = parsed_data["course_progress"];
    } else {
      create_course_modal_content.innerHTML = "Daten werden gespeichert. Einen Moment, bitte...";
      eventsource.close();
      console.log("Connection closed.");
    }
  };
  eventsource.onerror = function (e) {
    console.log(`error`, e);
  };
}
