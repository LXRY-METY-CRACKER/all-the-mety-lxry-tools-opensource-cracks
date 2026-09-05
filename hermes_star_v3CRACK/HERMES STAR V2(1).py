import os
import sys
import time
import math
import msvcrt
import shutil
import subprocess
import ctypes
import json
import re
import glob
import random

# ==============================================================================
# PERCORSO BASE
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==============================================================================
# CONFIGURAZIONE — MODIFICA QUI LE TUE CATEGORIE E TOOL
# ==============================================================================

CONFIG_FILE = os.path.join(BASE_DIR, "options.json")

DEFAULT_OPTIONS = {
    "SPYWARE PC": ["Spyware Builder V12"],
    "RAT Computer": ["Apocalypse RAT v3", "Rasomware Builder", "Key logger v5 PRO", "Crypto Miner Builder"],
    "TOOLS": ["EXE To Image", "Brute force zip", "Grabber Builder v1", "CC Validator", "Discord Bot Pannel", "Web Scanner"],
    "EXPLOITS": ["Exploit DB", "Metasploit Helper", "Payload Generator"],
    "OSINT": ["OSINT RS"],
    "MISC": ["Tool 1", "Tool 2"]
    # AGGIUNGI QUI NUOVE CATEGORIE, ES: "NEW": ["Opzione1", "Opzione2"]
}

def load_options():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key in DEFAULT_OPTIONS:
                if key not in data:
                    data[key] = DEFAULT_OPTIONS[key][:]
            return data
        except:
            return DEFAULT_OPTIONS.copy()
    else:
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_OPTIONS, f, indent=4, ensure_ascii=False)
        except:
            pass
        return DEFAULT_OPTIONS.copy()

OPTIONS = load_options()

# ==============================================================================
# LAYOUT DELLE BOX — MODIFICA QUI PER RIDISPORRE LE CATEGORIE
# ==============================================================================
LAYOUT = [
    ["SPYWARE PC", "RAT Computer", "TOOLS", "EXPLOITS"],
    ["OSINT", "MISC"]
]

# ==============================================================================
# Costruzione automatica delle liste di opzioni e conteggi
# ==============================================================================
CATEGORY_OPTIONS = {}
for cat, items in OPTIONS.items():
    CATEGORY_OPTIONS[cat] = items

TUTTE_LE_OPZIONI = []
for row in LAYOUT:
    for cat in row:
        TUTTE_LE_OPZIONI.extend(CATEGORY_OPTIONS.get(cat, []))

OFFSETS = {}
cum = 0
for cat, items in CATEGORY_OPTIONS.items():
    OFFSETS[cat] = cum
    cum += len(items)

# ==============================================================================
# WINDOWS ANSI / VT
# ==============================================================================
def enable_windows_vt():
    if sys.platform == "win32":
        try:
            kernel32 = ctypes.windll.kernel32
            hOut = kernel32.GetStdHandle(-11)
            out_mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(hOut, ctypes.byref(out_mode))
            out_mode.value |= 0x0004
            kernel32.SetConsoleMode(hOut, out_mode)
        except:
            pass

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    os.system("chcp 65001 > nul")
    try:
        subprocess.run(f"mode con: cols=180 lines=50", shell=True, capture_output=True)
    except:
        pass
    os.system("title HERMES STAR V2 - RAIN")
    enable_windows_vt()

# ==============================================================================
# BLUE COLOR ENGINE
# ==============================================================================
BLUE_HUE = 0.6667

def hsv_to_rgb(h, s, v):
    h = BLUE_HUE
    if s == 0.0:
        return int(v*255), int(v*255), int(v*255)
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q
    return int(r*255), int(g*255), int(b*255)

def rainbow(hue, sat=1.0, val=1.0):
    r, g, b = hsv_to_rgb(BLUE_HUE, sat, val)
    return f"\033[38;2;{r};{g};{b}m"

RESET = "\033[0m"
BOLD = "\033[1m"

# ==============================================================================
# RAIN ENGINE
# ==============================================================================
class RainEngine:
    def __init__(self, cols, lines, num_drops=120):
        self.cols = cols
        self.lines = lines
        self.num_drops = num_drops
        self.drops = []
        self.grid = []
        self.grid_colors = []
        self._resize(cols, lines)
        for _ in range(num_drops):
            self._new_drop(init=True)

    def _resize(self, cols, lines):
        self.cols = cols
        self.lines = lines
        self.grid = [[' ' for _ in range(cols)] for _ in range(lines)]
        self.grid_colors = [[RESET for _ in range(cols)] for _ in range(lines)]
        self.drops = [d for d in self.drops if 0 <= d['x'] < cols]
        while len(self.drops) < self.num_drops:
            self.drops.append(self._new_drop(init=True))
        if len(self.drops) > self.num_drops:
            self.drops = self.drops[:self.num_drops]

    def _new_drop(self, init=False):
        drop = {
            'x': random.randint(0, self.cols - 1),
            'y': random.randint(-self.lines, self.lines) if init else random.randint(-10, 0),
            'speed': random.uniform(1.5, 3.5),
            'length': random.randint(8, 18),
            'char': random.choice(['|', '/', '\\', '•', '·'])
        }
        return drop

    def update(self):
        for drop in self.drops[:]:
            drop['y'] += drop['speed']
            if drop['y'] - drop['length'] > self.lines:
                self.drops.remove(drop)
                self.drops.append(self._new_drop(init=False))

        for y in range(self.lines):
            row = self.grid[y]
            colrow = self.grid_colors[y]
            for x in range(self.cols):
                row[x] = ' '
                colrow[x] = RESET

        for drop in self.drops:
            y_start = int(drop['y'] - drop['length'])
            y_end = int(drop['y'])
            for y in range(max(0, y_start), min(self.lines, y_end + 1)):
                pos_in_drop = drop['y'] - y
                intensity = 1.0 - (pos_in_drop / drop['length'])
                intensity = max(0.0, min(1.0, intensity))
                if intensity > 0.7:
                    sat, val = 1.0, 1.0
                elif intensity > 0.3:
                    sat, val = 0.8, 0.6 + intensity * 0.4
                else:
                    sat, val = 0.4, 0.3 + intensity * 0.6
                color = rainbow(BLUE_HUE, sat, val)
                x = drop['x']
                if 0 <= x < self.cols:
                    self.grid[y][x] = drop['char']
                    self.grid_colors[y][x] = color

    def get_rows(self):
        rows = []
        for y in range(self.lines):
            row_chars = []
            for x in range(self.cols):
                if self.grid[y][x] != ' ':
                    row_chars.append(f"{self.grid_colors[y][x]}{self.grid[y][x]}{RESET}")
                else:
                    row_chars.append(' ')
            rows.append(''.join(row_chars))
        return rows

# ==============================================================================
# UI FUNCTIONS
# ==============================================================================
def get_banner_color(line_idx, frame_count):
    brightness = 0.85 + 0.15 * math.sin(frame_count*0.08 + line_idx*0.2)
    return rainbow(BLUE_HUE, sat=0.9, val=brightness)

def get_moving_line(length, anim_frame, reverse=False, speed=1.8):
    pulse = (math.sin(anim_frame * 0.2) + 1) / 2
    head_pos = (anim_frame * speed) % (length + 10) if not reverse else ((length + 10) - (anim_frame * speed)) % (length + 10)
    trail = 8
    line = ""
    base_hue = (anim_frame * 0.02) % 1.0
    for i in range(length):
        dist = (head_pos - i) if not reverse else (i - head_pos)
        if 0 <= dist < trail and pulse > 0.05:
            hue_offset = (dist / trail) * 0.4
            hue = (base_hue + hue_offset) % 1.0
            if dist == 0:
                sat, val = 1.0, 1.0
            elif dist < 3:
                sat, val = 0.9, 0.95
            else:
                sat, val = 0.8, 0.9
        else:
            hue = (base_hue + 0.5) % 1.0
            sat, val = 0.2, 0.2
        line += rainbow(hue, sat, val) + "─"
    return line

def render_shimmer_text(text, anim_frame):
    res = ""
    shimmer_pos = int(anim_frame * 1.2) % (len(text) + 6)
    base_hue = (anim_frame * 0.03) % 1.0
    for i, char in enumerate(text):
        dist = abs(i - shimmer_pos)
        if dist == 0:
            hue = (base_hue + 0.0) % 1.0
            sat, val = 1.0, 1.0
        elif dist == 1:
            hue = (base_hue + 0.15) % 1.0
            sat, val = 0.9, 0.95
        elif dist == 2:
            hue = (base_hue + 0.3) % 1.0
            sat, val = 0.8, 0.9
        else:
            hue = (base_hue + 0.5) % 1.0
            sat, val = 0.6, 0.7
        res += rainbow(hue, sat, val) + char
    return res

def get_key():
    if msvcrt.kbhit():
        ch = msvcrt.getch()
        if ch in (b'\xe0', b'\x00'):
            ch2 = msvcrt.getch()
            if ch2 in (b'H', b'7'):
                return "UP"
            elif ch2 in (b'P', b'8'):
                return "DOWN"
        elif ch in (b'w', b'W'):
            return "UP"
        elif ch in (b's', b'S'):
            return "DOWN"
        elif ch == b'\r':
            return "ENTER"
        elif ch == b'\x1b':
            return "ESC"
    return None

def build_option_cell(name, idx, is_selected, anim_frame, width):
    num_str = f"[{idx+1:02d}] "
    if is_selected:
        anim_name = render_shimmer_text(name, anim_frame)
        cell = f"{rainbow(anim_frame*0.05,1.0,1.0)}▶ {rainbow(anim_frame*0.03+0.3,1.0,1.0)}{num_str}{anim_name}"
    else:
        hue = (anim_frame * 0.01 + idx * 0.02) % 1.0
        cell = f"   {rainbow(hue, 0.5, 0.6)}{num_str}{rainbow(hue+0.2, 0.6, 0.7)}{name}"
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    visible = ansi_escape.sub('', cell)
    if len(visible) < width:
        cell += ' ' * (width - len(visible))
    return cell

# ==============================================================================
# RICERCA FILE CON GLOB
# ==============================================================================
def find_script_file(script_name):
    if '.' in os.path.basename(script_name):
        if os.path.isfile(os.path.join(BASE_DIR, script_name)):
            return os.path.join(BASE_DIR, script_name)
    
    for ext in ['.py', '.pyw', '.txt', '.bat', '.cmd']:
        path = os.path.join(BASE_DIR, script_name + ext)
        if os.path.isfile(path):
            return path
    
    pattern = os.path.join(BASE_DIR, script_name + "*")
    matches = glob.glob(pattern)
    for f in matches:
        if os.path.isfile(f):
            return f
    
    return None

# ==============================================================================
# ESEGUI SCRIPT — AGGIORNA IL MAPPING PER NUOVI TOOL
# ==============================================================================
def run_script(script_name):
    SCRIPT_MAP = {
        # SPYWARE PC
        "Spyware Builder V12": "spyware_01",
        # RAT Computer
        "Apocalypse RAT v3": "ratpc_01",
        "Rasomware Builder": "ratpc_02",
        "Key logger v5 PRO": "ratpc_03",
        "Crypto Miner Builder": "ratpc_04",
        # TOOLS
        "EXE To Image": "tools_05",
        "Brute force zip": "tools_06",
        "Grabber Builder v1": "tools_07",
        "CC Validator": "tools_08",
        "Discord Bot Pannel": "tools_09",
        "Web Scanner": "tools_10",
        # EXPLOITS
        "Exploit DB": "exploit_01",
        "Metasploit Helper": "exploit_02",
        "Payload Generator": "exploit_03",
        # OSINT
        "OSINT RS": "new_01",
        # MISC
        "Tool 1": "misc_01",
        "Tool 2": "misc_02"
        # SE AGGIUNGI NUOVI TOOL, AGGIUNGI QUI IL MAPPING, ES: "Nuovo Tool": "nuovo_file"
    }
    
    real_name = SCRIPT_MAP.get(script_name, script_name)
    script_path = find_script_file(real_name)
    
    sys.stdout.write("\033[?25h\033[?1049l")
    sys.stdout.flush()

    blue_bright = rainbow(0.9,1.0,1.0)
    print(f"{blue_bright}╭{'─'*58}╮{RESET}")
    print(f"{blue_bright}│ Esecuzione di: {script_name:<40} │{RESET}")
    print(f"{blue_bright}╰{'─'*58}╯{RESET}")

    if not script_path:
        err_color = rainbow(0.0, 1.0, 1.0)
        print(f"\n{err_color}[!] File non trovato: '{real_name}'{RESET}")
        print(f"{rainbow(0.5,1.0,1.0)}[~] Crea il file {real_name}.py per usarlo.{RESET}")
        input(f"\n{rainbow(0.6, 0.8, 0.9)}Premi INVIO per tornare al menu...{RESET}")
        return

    print(f"{rainbow(0.12,0.9,0.9)}[DEBUG] Trovato: {os.path.basename(script_path)}{RESET}")
    print(f"{rainbow(0.12,0.9,0.9)}[DEBUG] Avvio in modalita' interattiva...{RESET}")
    print()

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            encoding='utf-8',
            errors='replace'
        )
    except Exception as e:
        print(f"{rainbow(0.0,1.0,1.0)}[!] Errore durante l'esecuzione: {e}{RESET}")
        input(f"\n{rainbow(0.6, 0.8, 0.9)}Premi INVIO per tornare al menu...{RESET}")
        return

    if result.returncode != 0:
        print(f"\n{rainbow(0.0,1.0,1.0)}[!] Lo script è terminato con errore (codice {result.returncode}).{RESET}")
        print(f"{rainbow(0.12,0.9,0.9)}[~] Se hai visto errori di import, installa i moduli mancanti:{RESET}")
        print("    pip install requests python-whois dnspython")

    input(f"\n{rainbow(0.4, 0.7, 0.9)}Premi INVIO per tornare al menu...{RESET}")

# ==============================================================================
# MAIN LOOP — DINAMICO in base a LAYOUT e OPTIONS
# ==============================================================================
def main():
    selected_index = 0
    frame_count = 0

    BANNER_LINES = [
        r"██╗  ██╗███████╗██████╗ ███╗   ███╗███████╗███████╗    ███████╗████████╗ █████╗ ██████╗     ██╗   ██╗██████╗",
        r"██║  ██║██╔════╝██╔══██╗████╗ ████║██╔════╝██╔════╝    ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗    ██║   ██║╚════██╗",
        r"███████║█████╗  ██████╔╝██╔████╔██║█████╗  ███████╗    ███████╗   ██║   ███████║██████╔╝    ██║   ██║ █████╔╝",
        r"██╔══██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ╚════██║    ╚════██║   ██║   ██╔══██║██╔══██╗    ╚██╗ ██╔╝██╔═══╝",
        r"██║  ██║███████╗██║  ██║██║ ╚═╝ ██║███████╗███████║    ███████║   ██║   ██║  ██║██║  ██║     ╚████╔╝ ███████╗",
        r"╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝    ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝      ╚═══╝  ╚══════╝",
        "                                                          V2.0 - RAIN EDITION"
    ]

    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    max_len = 0
    for line in BANNER_LINES:
        clean = ansi_escape.sub('', line)
        max_len = max(max_len, len(clean))

    # Parametri di layout dinamici
    max_cols = max(len(row) for row in LAYOUT) if LAYOUT else 1
    INNER_WIDTH = 30
    SEP = "  "
    BOX_WIDTH = INNER_WIDTH + 2
    TOTAL_BOX_WIDTH = max_cols * BOX_WIDTH + (max_cols - 1) * len(SEP)
    FOOTER_WIDTH = 100

    try:
        sys.stdout.write("\033[?1049h\033[?25l")
        sys.stdout.flush()

        term_cols, term_lines = shutil.get_terminal_size((180, 50))
        rain = RainEngine(term_cols, term_lines, num_drops=120)
        last_cols, last_lines = term_cols, term_lines

        while True:
            key = get_key()
            if key == "UP":
                selected_index = (selected_index - 1) % len(TUTTE_LE_OPZIONI)
            elif key == "DOWN":
                selected_index = (selected_index + 1) % len(TUTTE_LE_OPZIONI)
            elif key == "ESC":
                break
            elif key == "ENTER":
                selected_name = TUTTE_LE_OPZIONI[selected_index]
                run_script(selected_name)

                sys.stdout.write("\033[?1049h\033[?25l")
                sys.stdout.flush()
                term_cols, term_lines = shutil.get_terminal_size((180, 50))
                last_cols, last_lines = term_cols, term_lines
                rain._resize(term_cols, term_lines)
                continue

            term_cols, term_lines = shutil.get_terminal_size((180, 50))
            if term_cols != last_cols or term_lines != last_lines:
                rain._resize(term_cols, term_lines)
                last_cols, last_lines = term_cols, term_lines

            rain.update()
            rain_rows = rain.get_rows()

            anim_frame = frame_count * 0.6

            banner_x = max(1, (term_cols - max_len) // 2 + 1)

            buf = ["\033[H"]

            # Pioggia
            for y, row in enumerate(rain_rows):
                if y < term_lines:
                    buf.append(f"\033[{y+1};1H{row}")

            # Banner
            for i, line in enumerate(BANNER_LINES):
                colore = get_banner_color(i, frame_count)
                line = line.rstrip()
                buf.append(f"\033[{1+i+1};{banner_x+1}H{colore}{line}{RESET}")

            current_y = len(BANNER_LINES) + 2

            for row_idx, row_cats in enumerate(LAYOUT):
                max_row_options = 0
                for cat in row_cats:
                    if cat in CATEGORY_OPTIONS:
                        max_row_options = max(max_row_options, len(CATEGORY_OPTIONS[cat]))
                if not row_cats:
                    continue

                num_cols = len(row_cats)
                row_width = num_cols * BOX_WIDTH + (num_cols - 1) * len(SEP)
                row_x = max(1, (term_cols - row_width) // 2 + 1)

                # Top border
                top_parts = []
                for col_idx, cat in enumerate(row_cats):
                    moving = get_moving_line(INNER_WIDTH, anim_frame + (row_idx*10 + col_idx)*4, speed=2.0)
                    top_parts.append(f"╭{moving}╮")
                top_row = SEP.join(top_parts)
                buf.append(f"\033[{current_y+1};{row_x+1}H{top_row}")
                current_y += 1

                # Titles
                title_cells = []
                for col_idx, cat in enumerate(row_cats):
                    titolo_color = rainbow(anim_frame*0.02 + (row_idx*10 + col_idx)*0.25, 1.0, 1.0)
                    text_len = len(cat)
                    left = (INNER_WIDTH - text_len) // 2
                    right = INNER_WIDTH - text_len - left
                    centered = ' ' * left + cat + ' ' * right
                    title_cells.append(f"│{centered}│")
                buf.append(f"\033[{current_y+1};{row_x+1}H{SEP.join(title_cells)}")
                current_y += 1

                # Options rows
                for row in range(max_row_options):
                    row_cells = []
                    for col_idx, cat in enumerate(row_cats):
                        if cat in CATEGORY_OPTIONS and row < len(CATEGORY_OPTIONS[cat]):
                            global_idx = OFFSETS[cat] + row
                            name = CATEGORY_OPTIONS[cat][row]
                            is_sel = (global_idx == selected_index)
                            cell_content = build_option_cell(name, global_idx, is_sel, anim_frame, INNER_WIDTH)
                            row_cells.append(f"│{cell_content}│")
                        else:
                            row_cells.append(f"│{' ' * INNER_WIDTH}│")
                    buf.append(f"\033[{current_y+row+1};{row_x+1}H{SEP.join(row_cells)}")
                current_y += max_row_options

                # Bottom border
                bottom_parts = []
                for col_idx, cat in enumerate(row_cats):
                    moving = get_moving_line(INNER_WIDTH, anim_frame + (row_idx*10 + col_idx)*4, reverse=True, speed=2.0)
                    bottom_parts.append(f"╰{moving}╯")
                bottom_row = SEP.join(bottom_parts)
                buf.append(f"\033[{current_y+1};{row_x+1}H{bottom_row}")
                current_y += 1
                current_y += 2

            # Footer
            footer_y = current_y
            footer_x = max(1, (term_cols - FOOTER_WIDTH) // 2 + 1)
            status_text = "  Status: Ready  "
            padding = (FOOTER_WIDTH - 4 - len(status_text)) // 2
            footer_color = rainbow(0.3, 1.0, 1.0)

            buf.append(f"\033[{footer_y+1};{footer_x+1}H{footer_color}╭{'─'*(FOOTER_WIDTH-2)}╮{RESET}")
            buf.append(f"\033[{footer_y+2};{footer_x+1}H{footer_color}│{' ' * padding}{rainbow(0.2,1.0,1.0)}{status_text}{' ' * padding}│{RESET}")
            buf.append(f"\033[{footer_y+3};{footer_x+1}H{footer_color}╰{'─'*(FOOTER_WIDTH-2)}╯{RESET}")

            # Copyright
            copy_y = footer_y + 5
            copy_text = "  © 2026 HERMES STAR V2 "
            copy_padding = (FOOTER_WIDTH - 4 - len(copy_text)) // 2
            copy_color = rainbow(0.7, 1.0, 1.0)

            buf.append(f"\033[{copy_y+1};{footer_x+1}H{copy_color}╭{'─'*(FOOTER_WIDTH-2)}╮{RESET}")
            buf.append(f"\033[{copy_y+2};{footer_x+1}H{copy_color}│{' ' * copy_padding}{rainbow(anim_frame*0.04,1.0,1.0)}{copy_text}{' ' * copy_padding}│{RESET}")
            buf.append(f"\033[{copy_y+3};{footer_x+1}H{copy_color}╰{'─'*(FOOTER_WIDTH-2)}╯{RESET}")

            sys.stdout.write("".join(buf))
            sys.stdout.flush()

            frame_count += 1
            time.sleep(0.05)

    finally:
        sys.stdout.write("\033[?25h\033[?1049l")
        sys.stdout.flush()

if __name__ == "__main__":
    main()