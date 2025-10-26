# Smart File Organizer

A Python tool that automatically organizes your files into folders like **Images**, **Documents**, **Archives**, etc.  
You can run one command (or use a simple GUI), and your files will be sorted automatically.  

---
### What it does:
- Sorts files by extension (automatically detects the type)
- Dry Run — see what would happen without actually changing anything
- Undo — revert the last organization if you messed up
- Configurable conflict handling (rename or skip)
- **GUI with Tkinter** — if you don't wanna deal with terminal stuff
- Logs everything to .csv and .json — so you know exactly what got moved

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Kurai-bit/Smart-File-Organizer.git
cd Smart-File-Organizer
```

## Usage (Command Line):
### Organize a folder
```bash
python organizer.py <path_to_folder>
```

### Preview changes (Dry Run)
```bash
python organizer.py <path_to_folder> --dry-run
```

### Undo last operation
```bash
python organizer.py <path_to_folder> --undo
```

### Handle conflicts
```bash
python organizer.py <path_to_folder> --conflict-mode skip
python organizer.py <path_to_folder> --conflict-mode rename
```

---

Run the graphical interface:
```bash
python gui.py
```

The GUI allows you to:
- Select a folder  
- Choose operation mode (Normal / Dry Run / Undo)  
- Organize files visually and view logs in real time  

---

## Log Files:

- **organizer_log.csv** — records timestamp, source, and destination for each move  
- **organizer_undo.json** — stores data needed to revert the last operation  

---

## Configuration:

You can edit **config.json** to customize which file extensions belong to each category.

Example:
```json
{
  "Images": [".jpg", ".jpeg", ".png"],
  "Documents": [".pdf", ".docx", ".txt"],
  "Archives": [".zip", ".rar", ".7z"]
}
```

---

## GUI Interface

![GUI Screenshot](screenshots/gui.png)

---

## Before Organization

![Before GUI](screenshots/guibefore.png)

![Before Example](screenshots/exbef.png)

---

## After Organization

![After GUI](screenshots/guiafter.png)

![After Example](screenshots/exafter.png)

---

## Author

**Eligia Raileanu**  
Developed as part of an internship practical project.  
Year: 2025


