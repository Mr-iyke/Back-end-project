document.addEventListener("DOMContentLoaded", () => {
  const messages = document.querySelector(".messages");

  // Initially apply the scaler-open class
  if (messages.textContent.trim() !== '') {
    messages.style.display = "flex";
    messages.classList.add("scaler-open");
    messages.classList.remove("scaler-close");

    // After 3 seconds, remove scaler-open and add scaler-close
    setTimeout(() => {
        messages.style.display = "none";
        messages.classList.remove("scaler-open");
        messages.classList.add("scaler-close");
  }, 5000);
 } // 3000 milliseconds = 3 seconds
});
