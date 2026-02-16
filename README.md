# ENCS3320 Computer Networks — Project 1

Project 1 covers network commands and Wireshark (Task 1), a TCP socket-based web server with English/Arabic pages (Task 2), and a UDP client–server trivia game (Task 3).

## Overview

**Task 1 — Network commands and Wireshark**  
Explains and uses commands (`ipconfig`, `ping`, `tracert`, `nslookup`, `telnet`) and Wireshark for DNS capture. Documented in the report only; no code in this repo.

**Task 2 — Web server**  
TCP socket server (Python) listening on port **5698**. Serves HTML pages (English and Arabic), supporting material, and CSS. Routes: `/`, `/en`, `/ar` → main pages; `/supporting_material_en.html`, `/supporting_material_ar.html`; `style.css`; `/process_request?fileName=...` for images (local file or 307 redirect to Google Images / YouTube). Returns 404 for missing files and 400 for unsupported types. Implemented in **task2/task2/Driver.py**; web assets (HTML, CSS) used by the server live under **task2/task2/** (path set in `file_path_base`). The **templates/** and **static/** folders at the project root contain the same or similar content for reference or deployment.

**Task 3 — UDP trivia game**  
UDP server (**task3/server.py**) on port **5689**: sends questions, accepts answers from clients, tracks scores, and announces winners. Client (**task3/cliant.py**): enter server IP, port, and username; receive questions and send answers; type `quit` to exit. Requires at least 2 players to run a round.

---

## Project structure

```
.
├── README.md
├── report.pdf                              # Full report (Task 1–3 theory, commands, code, screenshots)
├── static/
│   └── css/
│       └── style.css                       # CSS (copy/reference; server uses task2/task2/style.css)
├── templates/                              # HTML (copy/reference; server uses task2/task2/*.html)
│   ├── main_en.html
│   ├── main_ar.html
│   ├── supporting_material_en.html
│   └── supporting_material_ar.html
├── task2/
│   ├── Driver.sln                          # Visual Studio solution (optional)
│   └── task2/
│       ├── Driver.py                       # TCP web server (port 5698)
│       ├── main_en.html
│       ├── main_ar.html
│       ├── supporting_material_en.html
│       ├── supporting_material_ar.html
│       └── style.css
└── task3/
    ├── server.py                           # UDP trivia server (port 5689)
    └── cliant.py                           # UDP trivia client
```

---

## Requirements

- **Python 3.x** (no extra packages; uses only `socket`, `threading`, `time`, `random`, `os`, `sys`).
- **Task 2:** In **task2/task2/Driver.py**, `file_path_base` is set to a full path (e.g. `C:/Users/USER/.../task2/task2/`). Change it to the folder where your HTML/CSS (and any images) actually live, or run the script from that directory and use a relative path.
- **Task 3:** Server and clients must be able to reach each other (same machine: 127.0.0.1; same LAN: use the server’s IP). Open port 5689 (UDP) if behind a firewall.

---

## Usage

### Task 2 — Web server

1. Set `file_path_base` in **task2/task2/Driver.py** to the directory containing `main_en.html`, `main_ar.html`, `supporting_material_*.html`, and `style.css`.
2. Run the server:

```bash
cd task2/task2
python Driver.py
```

3. In a browser or with a client (e.g. `curl`), open:
   - `http://<server_ip>:5698/` or `http://<server_ip>:5698/en` — English main page
   - `http://<server_ip>:5698/ar` — Arabic main page
   - `http://<server_ip>:5698/supporting_material_en.html` (or `_ar`)
   - `http://<server_ip>:5698/style.css`
   - `http://<server_ip>:5698/process_request?fileName=some_image.png` — image or redirect

### Task 3 — UDP trivia game

1. Start the server (default 127.0.0.1:5689):

```bash
cd task3
python server.py
```

2. Start at least two clients (each on a terminal or machine that can reach the server):

```bash
cd task3
python cliant.py
```

Enter server IP, port (5689), and a username. Answer questions by typing in the terminal; type `quit` to exit.

---

## Report

Theory, task descriptions, code snippets, and screenshots:  
**`report.pdf`**
