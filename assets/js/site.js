const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".site-nav");

if (menuButton && navigation) {
  menuButton.addEventListener("click", () => {
    const isOpen = navigation.dataset.open === "true";
    navigation.dataset.open = String(!isOpen);
    menuButton.setAttribute("aria-expanded", String(!isOpen));
  });

  navigation.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      navigation.dataset.open = "false";
      menuButton.setAttribute("aria-expanded", "false");
    }
  });
}

document.querySelectorAll("[data-current-year]").forEach((node) => {
  node.textContent = String(new Date().getFullYear());
});

const dialog = document.querySelector(".lightbox");
const galleryButtons = [...document.querySelectorAll(".gallery-open")];

if (dialog && galleryButtons.length) {
  const image = dialog.querySelector("img");
  const caption = dialog.querySelector("figcaption");
  const closeButton = dialog.querySelector(".lightbox-close");
  const previousButton = dialog.querySelector(".lightbox-prev");
  const nextButton = dialog.querySelector(".lightbox-next");
  let activeIndex = 0;

  const showImage = (index) => {
    activeIndex = (index + galleryButtons.length) % galleryButtons.length;
    const selected = galleryButtons[activeIndex];
    image.src = selected.dataset.full;
    image.alt = selected.dataset.alt;
    caption.textContent = selected.dataset.title;
  };

  galleryButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
      showImage(index);
      dialog.showModal();
      document.body.style.overflow = "hidden";
    });
  });

  const closeDialog = () => {
    dialog.close();
    document.body.style.overflow = "";
  };

  closeButton.addEventListener("click", closeDialog);
  previousButton.addEventListener("click", () => showImage(activeIndex - 1));
  nextButton.addEventListener("click", () => showImage(activeIndex + 1));

  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) closeDialog();
  });

  dialog.addEventListener("close", () => {
    document.body.style.overflow = "";
  });

  dialog.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") showImage(activeIndex - 1);
    if (event.key === "ArrowRight") showImage(activeIndex + 1);
  });
}
