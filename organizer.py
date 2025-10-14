import os
import shutil
import argparse
import json
from datetime import datetime

class SmartOrganizer:
    def __init__(self, base_path, dry_run=False, conflict_mode="rename"):
        self.base_path = base_path
        self.dry_run = dry_run
        self.conflict_mode = conflict_mode
        self.log_file = os.path.join(base_path, "organizer_log.csv")
        self.undo_file = os.path.join(base_path, "organizer_undo.json")
        self.config_file = os.path.join(os.path.dirname(__file__), "config.json")

        self.stats = {"Processed": 0, "Moved": 0, "Skipped": 0, "Errors": 0}
        self.load_config()

        # initialize undo list
        self.undo_data = []

    def load_config(self):
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.categories = json.load(f)["categories"]
        except Exception as e:
            print(f"Eroare la încarcarea config.json: {e}")
            self.categories = {}

    def get_category(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        for category, extensions in self.categories.items():
            if ext in extensions:
                return category
        return "Others"

    def organize(self):
        for root, _, files in os.walk(self.base_path):
            for file in files:
                if file in ["organizer_log.csv", "organizer_undo.json"]:
                    continue

                src = os.path.join(root, file)
                category = self.get_category(file)
                dest_dir = os.path.join(self.base_path, category)
                os.makedirs(dest_dir, exist_ok=True)
                dst = os.path.join(dest_dir, file)

                self.stats["Processed"] += 1
                self.move_file(src, dst)

        self.save_log()
        self.save_undo()
        self.show_report()

    def move_file(self, src, dst):
        try:
            if os.path.abspath(src) == os.path.abspath(dst):
                return

            if os.path.exists(dst):
                if self.conflict_mode == "skip":
                    print(f"[SKIP - conflict] {src} deja exista la destinație")
                    self.stats["Skipped"] += 1
                    return
                elif self.conflict_mode == "rename":
                    name, ext = os.path.splitext(dst)
                    i = 1
                    while os.path.exists(f"{name} ({i}){ext}"):
                        i += 1
                    dst = f"{name} ({i}){ext}"

            if self.dry_run:
                print(f"[DRY-RUN] {src} -> {dst}")
            else:
                shutil.move(src, dst)
                print(f"Mutat: {src} -> {dst}")

            # register undo info
            self.undo_data.append({
                "src": src,
                "dst": dst,
                "timestamp": datetime.now().isoformat()
            })
            self.stats["Moved"] += 1

        except Exception as e:
            print(f"[EROARE] {src}: {e}")
            self.stats["Errors"] += 1

    def save_log(self):
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("timestamp,src,dst\n")
            for entry in self.undo_data:
                f.write(f"{entry['timestamp']},{entry['src']},{entry['dst']}\n")
        print(f"Log salvat: {self.log_file}")

    def save_undo(self):
        with open(self.undo_file, "w", encoding="utf-8") as f:
            json.dump(self.undo_data, f, indent=2)
        print(f"Undo salvat: {self.undo_file}")

    def undo(self):
        if not os.path.exists(self.undo_file):
            print("Nu exista fișier undo.json.")
            return

        with open(self.undo_file, "r", encoding="utf-8") as f:
            undo_data = json.load(f)

        for entry in reversed(undo_data):
            try:
                if os.path.exists(entry["dst"]):
                    shutil.move(entry["dst"], entry["src"])
                    print(f"[UNDO] {entry['dst']} -> {entry['src']}")
            except Exception as e:
                print(f"[EROARE UNDO] {e}")

        print("Toate mutarile au fost anulate cu succes.")

    def show_report(self):
        print("\n RAPORT FINAL ")
        for k, v in self.stats.items():
            print(f"{k}: {v}")
        print("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart File Organizer cu config.json și undo")
    parser.add_argument("path", help="Calea catre folderul ce va fi organizat")
    parser.add_argument("--dry-run", action="store_true", help="Simuleaza mutarile fara a le efectua")
    parser.add_argument("--conflict-mode", choices=["rename", "skip"], default="rename", help="Cum se trateaza conflictele de fișiere")
    parser.add_argument("--undo", action="store_true", help="Anuleaza ultima organizare")

    args = parser.parse_args()
    organizer = SmartOrganizer(args.path, args.dry_run, args.conflict_mode)

    if args.undo:
        organizer.undo()
    else:
        organizer.organize()
