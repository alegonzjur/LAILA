window.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".genre-button").forEach((btn, i) => {
        btn.classList.add("fade-in");
        btn.style.animationDelay = `${i * 0.2}s`;
    });
});
