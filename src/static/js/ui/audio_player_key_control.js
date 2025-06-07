var clickOrTouchEvent = "ontouchstart" in window ? "touchstart" : "click";
var play_button = document.getElementById("audio_player");

play_button.addEventListener(clickOrTouchEvent, playWordAudio, false);
window.addEventListener("keydown", playWordAudio, false);

function playWordAudio(event) {
  if (event.pointerId === 1 || event.pointerType === "touch" || event.keyCode === 80) {
    play_button.play();
  }
}
