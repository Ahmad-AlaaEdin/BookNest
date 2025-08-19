# 📚 BookNest

BookNest is a web application that helps users **track their reading journey**, manage personal libraries, and save **notes or favorite quotes** for each book.

It allows users to **sign up, log in, add books, update details, delete books, and attach personal notes/quotes**. The app provides a clean dashboard with filters, search functionality, and reading statistics.

---

## ✨ Features

- 🔑 **User Authentication**: Sign up, login, and logout with secure sessions.
- 📖 **Book Management**: Add, update, and delete books with cover image, author, and details.
- 📝 **Notes & Quotes**: Add, update, and delete notes or favorite quotes for each book.
- 🔍 **Search & Filters**: Easily find books in your library.
- 📊 **Stats Dashboard**: Displays reading progress and user insights.
- 💾 **JSON Integration**: Uses a JSON file for saving extra data (e.g., motivational quotes, app settings, or recommendations).

**✨ New Feature:**  
Unlike simple book trackers, BookNest lets users **attach personal notes/quotes to each book** and also integrates a **JSON-powered feature** (such as random daily quotes) for extra interactivity.

---

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Auth**: Flask-Login
- **Storage**: JSON file for additional app data

---

## 📦 Prerequisites

Make sure you have the following installed:

- Python 3.8+
- pip (Python package installer)

### Install dependencies

1. Create and activate a virtual environment:

```bash
   python3 -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python3 main.py
```

## Project Checklist

- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
- [x] It uses at least one module from the Python Standard Library other than the random module.
      Please provide the name of the module you are using in your app.
  - Module name:
- [x] It contains at least one class written by you that has both properties and methods. It uses `__init__()` to let the class initialize the object's attributes (note that `__init__()` doesn't count as a method). This includes instantiating the class and using the methods in your app.
      Please provide below the file name and the line number(s) of at least one example of a class definition in your code as well as the names of two properties and two methods.
  - File name for the class definition: `models/user.py`
  - Line number(s) for the class definition: 1
  - Name of two properties: Name , Email
  - Name of two methods: CheckPassword , Create
  - File name and line numbers where the methods are used:
- [x] It makes use of JavaScript in the front end and uses the localStorage of the web browser.
- [x] It uses modern JavaScript (for example, let and const rather than var).
- [x] It makes use of the reading and writing to the same file feature.
- [x] It contains conditional statements. Please provide below the file name and the line number(s) of at least:

```

```
