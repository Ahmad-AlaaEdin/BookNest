const searchInput = document.getElementById("search-input");
const searchForm = document.getElementById("search-form");
const bookSearch = document.getElementById("book-search");
const statusBtn = document.getElementById("status");
const statusBtns = document.querySelectorAll(".status-btn");
const resultsList = document.querySelector(".results-list");
const modal2 = document.getElementById("exampleModalToggle2");
const addBookForm = document.getElementById("add-book-form");
const deleteNoteBtn = document.getElementById("delete-note-btn");

document.addEventListener("click", async function (e) {
  if (e.target.classList.contains("note-delete-btn")) {
    const noteId = e.target.dataset.noteId;

    if (!confirm("Are you sure you want to delete this note?")) return;

    try {
      const response = await fetch(`/notes/${noteId}`, {
        method: "DELETE",
      });
      console.log(response);
      if (!response.ok) throw new Error("Request failed");

      const noteItem = e.target.closest("li");
      if (noteItem) {
        noteItem.remove();
      }
    } catch (err) {
      console.error(err);
      alert("Could not delete note. Try again.");
    }
  }

  if (e.target.classList.contains("note-delete-btn")) {
    const noteId = e.target.dataset.noteId;
    console.log("Delete note:", noteId);
  }
});

document
  .getElementById("note-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const input = document.getElementById("note-input");
    const noteContent = input.value.trim();
    if (!noteContent) return;

    try {
      const response = await fetch(this.action, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content: noteContent }),
      });
      console.log(response);
      if (!response.ok) throw new Error("Request failed");

      const data = await response.json();
      const notesList = document.getElementById("notes-list");
      const li = document.createElement("li");
      li.className =
        "list-group-item d-flex justify-content-between align-items-center";
      li.dataset.noteId = data.id;
      li.innerHTML = `
      <span>${data.content}</span>
      <small class="text-muted">${data.created_at}</small>
      <div class="btn-group">
        <button class="btn btn-outline-secondary btn-sm note-update-btn" data-note-id="${data.id}">Update</button>
        <button class="btn btn-outline-danger btn-sm note-delete-btn" data-note-id="${data.id}">Delete</button>
      </div>
    `;
      notesList.appendChild(li);

      input.value = "";
    } catch (err) {
      console.error(err);
      alert("Could not add note. Try again.");
    }
  });
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
    alert(parsedRes.message);
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
