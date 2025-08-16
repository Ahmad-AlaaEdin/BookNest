const searchInput = document.getElementById("search-input");
const searchForm = document.getElementById("search-form");
const bookSearch = document.getElementById("book-search");
const statusBtn = document.getElementById("status");
const statusBtns = document.querySelectorAll(".status-btn");


let timeout = null;
bookSearch.addEventListener(
  "input",
  () => {
    clearTimeout(timeout);

    timeout = setTimeout(() => {
      let query = bookSearch.value.trim();
      if (query.length > 3) {
        fetchBooks(query);
      } else {
        console.log("empty");
      }
    });
  },
  5000
);

async function fetchBooks(query) {
  try {
    const data = await fetch(
      `https://www.googleapis.com/books/v1/volumes?q=${encodeURIComponent(
        query
      )}`
    );
    const books = await data.json();
    const titles = books.items.map((vol) => vol.volumeInfo.title);
    console.log(titles);
  } catch (err) {
    console.log(err);
  }
}
statusBtns.forEach((element) => {
  element.addEventListener("click", function (event) {
    const url = new URL(window.location.href);
    url.searchParams.set("status", event.target.value);
    window.location.href = url;
  });
});
searchForm.addEventListener("submit", function (event) {
  event.preventDefault();
  let searchInput = document.getElementById("search-input");
  const url = new URL(window.location.href);
  url.searchParams.set("title", searchInput.value);
  window.location.href = url;
});
