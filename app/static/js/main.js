const searchInput = document.getElementById("search-input");
const searchForm = document.getElementById("search-form");
const bookSearch = document.getElementById("book-search");
const statusBtn = document.getElementById("status");
const statusBtns = document.querySelectorAll(".status-btn");
const resultsList = document.querySelector(".results-list");
const modal2 = document.getElementById("exampleModalToggle2");
const addBookForm = document.getElementById("add-book-form");

addBookForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = new FormData(addBookForm);
  console.log(data);
  const response = await fetch("/books", {
    method: "POST",
    body: data,
  });

  const parsedRes = await response.json();
  if (response.ok) {
    location.reload(true);
  } else {
    alert(parsedRes.message)
  }
});

let timeout = null;
bookSearch.addEventListener("input", () => {
  clearTimeout(timeout);

  timeout = setTimeout(() => {
    let query = bookSearch.value.trim();
    if (query.length > 3) {
      fetchBooks(query);
    } else {
      console.log("empty");
    }
  }, 500);
});

bookSearch.addEventListener("focus", () => {
  resultsList.style.display = "block";
});
document.querySelector(".results-list").addEventListener("click", (e) => {
  const btn = e.target.closest("button.list-item");
  console.log(btn);
  if (!btn) return;

  const bookData = {
    title: btn.dataset.title,
    author: btn.dataset.author,
    pages: btn.dataset.pages,
    image: btn.dataset.image,
  };

  localStorage.setItem("selectedBook", JSON.stringify(bookData));

  const modal1 = bootstrap.Modal.getInstance(
    document.getElementById("exampleModalToggle")
  );
  if (modal1) modal1.hide();

  const modal2 = new bootstrap.Modal(
    document.getElementById("exampleModalToggle2")
  );
  modal2.show();
});
document.addEventListener("pointerdown", (e) => {
  const clickedInside =
    e.target === bookSearch ||
    e.target.closest(".results-list") ||
    e.target.closest("#exampleModalToggle");

  if (!clickedInside) {
    resultsList.style.display = "none";
  }
});

async function fetchBooks(query) {
  try {
    const data = await fetch(
      `https://www.googleapis.com/books/v1/volumes?q=${encodeURIComponent(
        query
      )}`
    );
    const books = await data.json();

    resultsList.innerHTML = books.items
      .map((vol, idx) => {
        const title = vol.volumeInfo.title || "No title";
        const author = vol.volumeInfo.authors
          ? vol.volumeInfo.authors[0]
          : "Unknown";
        const pages = vol.volumeInfo.pageCount || "";
        const img =
          vol.volumeInfo.imageLinks?.thumbnail || "static/images/default.png";

        return `
          <button type="button" class="list-item btn w-100"  data-title="${title}" 
        data-author="${author}" 
        data-pages="${pages}" data-image=${img}>
           <img src="${img}"/>
<div>
                <p>Title : ${title}</p>
                <p>Author : ${author}</p>
                <p>Pages : ${pages}</p>
              </div>
          </button>
        `;
      })
      .join("");
  } catch (err) {
    console.log(err);
  }
}

modal2.addEventListener("show.bs.modal", function () {
  const saved = localStorage.getItem("selectedBook");
  if (!saved) return;

  const book = JSON.parse(saved);
  const inputs = modal2.querySelectorAll("input.form-control");

  inputs[0].value = book.title || "";
  inputs[1].value = book.author || "";
  inputs[2].value = book.pages || "";
  inputs[3].value = book.image || "";
});

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
