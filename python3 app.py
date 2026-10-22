import os
from flask import Flask, render_template_string, request, send_from_directory
import sqlite3
import random
from datetime import datetime

app = Flask(__name__)
DB_NAME = "vbspu_library.db"

# ==========================================
# 1. DATABASE SETUP
# ==========================================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS passes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            course TEXT NOT NULL,
            shift TEXT NOT NULL,
            pass_code TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ==========================================
# 2. IMAGE HANDLER 
# ==========================================
@app.route('/<filename>')
def serve_images(filename):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
        return send_from_directory(os.getcwd(), filename)
    return "Not Found", 404

# ==========================================
# 3. SUPER ADVANCED HTML/CSS TEMPLATES
# ==========================================
BASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VBSPU | Cyber-Lib Gateway</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root { --blk: #050302; --grn: #00ff66; --pnk: #ff007f; --org: #ff6600; --brn: #5c3a21; }
        body { background-color: var(--blk); color: #ffffff; font-family: 'Rajdhani', sans-serif; overflow-x: hidden; background-image: radial-gradient(circle at center, #1a0f14 0%, var(--blk) 100%); }
        h1, h2, h3, .cyber-font { font-family: 'Orbitron', sans-serif; }
        .neon-text-grn { color: var(--grn); text-shadow: 0 0 10px var(--grn), 0 0 20px var(--grn); }
        .neon-text-pnk { color: var(--pnk); text-shadow: 0 0 8px var(--pnk); }
        .cyber-panel { background: rgba(92, 58, 33, 0.15); backdrop-filter: blur(12px); border: 1px solid var(--pnk); border-radius: 12px; position: relative; overflow: hidden; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
        .cyber-panel::before { content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,0,127,0.2), transparent); transform: skewX(-20deg); transition: 0.5s; }
        .cyber-panel:hover { transform: translateY(-8px) scale(1.02); box-shadow: 0 15px 30px rgba(0, 255, 102, 0.2); border-color: var(--grn); }
        .cyber-panel:hover::before { left: 150%; }
        .btn-orange { background: linear-gradient(45deg, var(--org), #ff3300); box-shadow: 0 0 15px var(--org); border: 1px solid #fff; transition: 0.3s; }
        .btn-orange:hover { box-shadow: 0 0 25px var(--org), 0 0 40px var(--org); transform: scale(1.05); }
        .animate-enter { animation: cyberSlideUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; opacity: 0; transform: translateY(40px); }
        @keyframes cyberSlideUp { to { opacity: 1; transform: translateY(0); } }
        .nav-link { position: relative; color: #fff; transition: 0.3s; text-transform: uppercase; letter-spacing: 1px; }
        .nav-link::after { content: ''; position: absolute; width: 0; height: 2px; bottom: -4px; left: 0; background-color: var(--grn); transition: width 0.3s; box-shadow: 0 0 10px var(--grn); }
        .nav-link:hover { color: var(--grn); }
        .nav-link:hover::after { width: 100%; }
        .cyber-input { background: rgba(0,0,0,0.6); border: 1px solid var(--brn); color: var(--grn); transition: 0.3s; }
        .cyber-input:focus { border-color: var(--grn); box-shadow: 0 0 10px var(--grn); outline: none; }
    </style>
</head>
<body class="min-h-screen flex flex-col">
    <nav class="p-5 border-b border-[#ff007f] shadow-[0_0_15px_rgba(255,0,127,0.3)] sticky top-0 z-50 bg-[#050302] bg-opacity-90 backdrop-blur-md">
        <div class="max-w-7xl mx-auto flex flex-wrap justify-between items-center">
            <div class="flex items-center gap-4 cursor-pointer hover:scale-105 transition">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6FDlSEadUhwed1AmV6vyCpuBV4G6R6MBM4rPznNDjUg&s" alt="Logo" class="h-12 rounded-full border-2 border-[#00ff66] shadow-[0_0_15px_#00ff66]">
                <div>
                    <h1 class="text-2xl font-black neon-text-grn uppercase tracking-widest">VBSPU Library</h1>
                    <span class="text-[10px] text-[#ff6600] tracking-[0.2em] font-bold">SYSTEM.ONLINE //</span>
                </div>
            </div>
            <div class="flex gap-6 font-bold mt-4 md:mt-0 text-sm">
                <a href="/" class="nav-link">Home</a>
                <a href="/about" class="nav-link">About</a>
                <a href="/booking" class="nav-link">Book Pass</a>
                <a href="/courses" class="nav-link">Courses</a>
                <a href="/developer" class="nav-link text-[#ff007f]">SYS_ADMIN</a>
            </div>
        </div>
    </nav>
    <main class="flex-grow p-4 md:p-8 flex items-center justify-center">
        <div class="w-full max-w-7xl animate-enter">
            {{ content | safe }}
        </div>
    </main>
    <footer class="p-6 border-t border-[#00ff66] text-center bg-black bg-opacity-80 mt-auto shadow-[0_-5px_15px_rgba(0,255,102,0.1)]">
        <p class="text-gray-400 font-bold uppercase tracking-wider text-sm"><span class="neon-text-pnk">VBSPU Cyber-Library Network</span> &copy; 2026</p>
        <p class="text-xs mt-2 text-[#5c3a21] uppercase font-black">Architected by <span class="text-[#ff6600] hover:text-[#00ff66] cursor-pointer transition">Raj Gautam</span></p>
    </footer>
</body>
</html>
"""

HOME_HTML = """
<div class="grid lg:grid-cols-2 gap-10 items-center">
    <div class="space-y-6 z-10">
        <div class="inline-block px-3 py-1 border border-[#ff007f] text-[#ff007f] rounded-full text-xs font-bold tracking-widest uppercase bg-[#ff007f] bg-opacity-10 mb-2">Access The Knowledge Grid</div>
        <h2 class="text-5xl md:text-7xl font-black leading-tight">VIVEKANANDA <br><span class="neon-text-grn">CENTRAL DATABANK</span></h2>
        <p class="text-gray-300 text-lg md:text-xl max-w-lg font-medium">Step into the future of learning at Veer Bahadur Singh Purvanchal University. Digital archives, silent pods, and infinite resources.</p>
        <div class="pt-4 flex gap-4">
            <a href="/booking" class="btn-orange text-white px-8 py-3 rounded text-lg font-bold uppercase tracking-wider inline-block">Initialize Pass //</a>
        </div>
    </div>
    <div class="grid grid-cols-2 gap-4 relative">
        <div class="absolute -inset-4 bg-[#00ff66] opacity-10 blur-2xl rounded-full"></div>
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRDyoa4TiqjDJIfK4uH6Jm9oZZt9sfYbPtaKvMYV7C-Q&s=10" class="rounded-xl border border-[#ff007f] shadow-lg w-full h-48 object-cover transform translate-y-8 cyber-panel">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROKnliWXEOBhaUOqXojnhFGB9KZIj8epyaLndIzbvFTg&s=10" class="rounded-xl border border-[#00ff66] shadow-lg w-full h-48 object-cover cyber-panel">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTan8HGgkwe7HI6GKSMv9adD4gtusJ4gAkxIJAchlZR5A&s=10" class="rounded-xl border border-[#ff6600] shadow-lg w-full h-48 object-cover col-span-2 cyber-panel">
    </div>
</div>
"""

ABOUT_HTML = """
<div class="max-w-5xl mx-auto cyber-panel p-8 md:p-12">
    <div class="text-center mb-10">
        <h2 class="text-4xl font-black neon-text-grn uppercase tracking-widest">About The Infrastructure</h2>
        <div class="h-1 w-24 bg-[#ff007f] mx-auto mt-4 shadow-[0_0_10px_#ff007f]"></div>
    </div>
    <div class="grid md:grid-cols-2 gap-10 items-center">
        <div><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQA3_TQ5uqXohLaqJG123pdT9QfB-O5kVRT-s7rOXseSg&s=10" class="w-full rounded-lg border-2 border-[#ff6600] shadow-[0_0_20px_rgba(255,102,0,0.3)] filter contrast-125"></div>
        <div class="space-y-6">
            <h3 class="text-2xl cyber-font text-[#ff007f]">VBSPU Core Node</h3>
            <p class="text-gray-300 text-lg leading-relaxed">The Vivekananda Central Library is upgraded for the modern scholar. Featuring ultra-fast terminals, biometric entry, and expansive study zones tailored for deep focus.</p>
            <div class="grid grid-cols-2 gap-4 mt-6">
                <div class="bg-black bg-opacity-50 p-4 border-l-4 border-[#00ff66] rounded"><h4 class="font-bold text-xl text-white">1.5M+</h4><p class="text-xs text-[#00ff66] uppercase tracking-wider">Physical Volumes</p></div>
                <div class="bg-black bg-opacity-50 p-4 border-l-4 border-[#ff007f] rounded"><h4 class="font-bold text-xl text-white">24/7</h4><p class="text-xs text-[#ff007f] uppercase tracking-wider">Digital Access</p></div>
                <div class="bg-black bg-opacity-50 p-4 border-l-4 border-[#ff6600] rounded"><h4 class="font-bold text-xl text-white">8AM - 8PM</h4><p class="text-xs text-[#ff6600] uppercase tracking-wider">Physical Shifts</p></div>
                <div class="bg-black bg-opacity-50 p-4 border-l-4 border-[#5c3a21] rounded"><h4 class="font-bold text-xl text-white">Zone 01</h4><p class="text-xs text-gray-400 uppercase tracking-wider">Silent Area</p></div>
            </div>
        </div>
    </div>
</div>
"""

BOOKING_HTML = """
<div class="max-w-2xl mx-auto">
    <div class="cyber-panel p-8">
        <div class="flex items-center gap-4 mb-8 border-b border-gray-700 pb-4">
            <div class="w-3 h-10 bg-[#00ff66] shadow-[0_0_10px_#00ff66]"></div>
            <div>
                <h2 class="text-3xl font-black uppercase text-white">Generate Access <span class="neon-text-pnk">Token</span></h2>
                <p class="text-gray-400 text-sm font-bold uppercase tracking-widest mt-1">Authorized Personnel Only</p>
            </div>
        </div>
        <form method="POST" action="/booking" class="space-y-5">
            <div class="grid grid-cols-2 gap-5">
                <div>
                    <label class="block text-[#00ff66] font-bold text-xs uppercase tracking-wider mb-2">Student Designation (Name)</label>
                    <input type="text" name="name" required class="w-full cyber-input rounded p-3 text-lg font-bold" placeholder="E.g. Raj Gautam">
                </div>
                <div>
                    <label class="block text-[#00ff66] font-bold text-xs uppercase tracking-wider mb-2">ID Matrix (Roll No)</label>
                    <input type="text" name="roll_no" required class="w-full cyber-input rounded p-3 text-lg font-bold" placeholder="XXXXXXXXX">
                </div>
            </div>
            <div class="grid grid-cols-2 gap-5">
                <div>
                    <label class="block text-[#ff007f] font-bold text-xs uppercase tracking-wider mb-2">Module (Course)</label>
                    <select name="course" class="w-full cyber-input rounded p-3 text-lg font-bold">
                        <option value="BCA">BCA (Bachelors in Comp App)</option>
                        <option value="B.Tech">B.Tech</option>
                        <option value="B.Sc Ag">B.Sc Agriculture</option>
                        <option value="MCA">MCA</option>
                    </select>
                </div>
                <div>
                    <label class="block text-[#ff007f] font-bold text-xs uppercase tracking-wider mb-2">Time Node (Shift)</label>
                    <select name="shift" class="w-full cyber-input rounded p-3 text-lg font-bold">
                        <option value="Morning (08:00 - 14:00)">Morning (08:00 - 14:00)</option>
                        <option value="Evening (14:00 - 20:00)">Evening (14:00 - 20:00)</option>
                    </select>
                </div>
            </div>
            <button type="submit" class="w-full btn-orange text-white font-black text-xl py-4 rounded uppercase tracking-widest mt-4">Execute Booking Protocol</button>
        </form>
        {% if pass_data %}
        <div class="mt-8 border-2 border-[#00ff66] bg-black rounded-lg p-6 relative overflow-hidden">
            <div class="absolute top-0 left-0 w-full h-1 bg-[#00ff66] opacity-50 shadow-[0_0_10px_#00ff66] animate-[scan_2s_ease-in-out_infinite]"></div>
            <style>@keyframes scan { 0% { top: 0; } 50% { top: 100%; } 100% { top: 0; } }</style>
            <div class="flex justify-between items-start">
                <div>
                    <h3 class="text-2xl font-black text-[#00ff66] uppercase mb-1">Access Granted</h3>
                    <p class="text-gray-400 text-xs font-bold uppercase tracking-widest">Vivekananda Library E-Pass</p>
                </div>
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6FDlSEadUhwed1AmV6vyCpuBV4G6R6MBM4rPznNDjUg&s" class="w-12 h-12 opacity-50 grayscale">
            </div>
            <div class="grid grid-cols-2 gap-4 mt-6">
                <div><p class="text-[#ff007f] text-[10px] uppercase font-bold">Holder Name</p><p class="text-white text-lg font-bold">{{ pass_data.name }}</p></div>
                <div><p class="text-[#ff007f] text-[10px] uppercase font-bold">Course / Module</p><p class="text-white text-lg font-bold">{{ pass_data.course }}</p></div>
                <div class="col-span-2 bg-[#5c3a21] bg-opacity-30 p-3 rounded border border-[#5c3a21]"><p class="text-[#ff6600] text-[10px] uppercase font-bold">Allocated Timeframe</p><p class="text-white text-md font-bold">{{ pass_data.shift }}</p></div>
            </div>
            <div class="mt-4 pt-4 border-t border-gray-800 text-center">
                <p class="cyber-font text-3xl tracking-widest text-white">{{ pass_data.code }}</p>
                <p class="text-[8px] text-[#00ff66] uppercase mt-1">Present this code at terminal gate</p>
            </div>
        </div>
        {% endif %}
    </div>
</div>
"""

COURSES_HTML = """
<div class="max-w-7xl mx-auto">
    <div class="text-center mb-12">
        <h2 class="text-4xl font-black neon-text-pnk uppercase tracking-widest">Academic Modules</h2>
        <p class="text-gray-400 font-bold mt-2 tracking-widest uppercase">Select your path</p>
    </div>
    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
        <div class="cyber-panel p-5 text-center group">
            <div class="overflow-hidden rounded-lg border-2 border-[#00ff66] mb-4">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPlg9bXm3kFPN0PVcGyAsO-L6o0LYImFL1qD-z5oAVPg&s=10" class="w-full h-40 object-cover group-hover:scale-110 transition duration-500 filter grayscale group-hover:grayscale-0">
            </div>
            <h3 class="text-2xl font-black text-white uppercase tracking-wider">BCA</h3>
            <div class="h-1 w-10 bg-[#00ff66] mx-auto my-2"></div><p class="text-sm text-gray-400 font-bold">Bachelor of Computer Applications</p>
        </div>
        <div class="cyber-panel p-5 text-center group">
            <div class="overflow-hidden rounded-lg border-2 border-[#ff007f] mb-4">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSH1xASn_izn8Xhw9UPj9GrpLiEw4O1b2EdWhANd37uHw&s=10" class="w-full h-40 object-cover group-hover:scale-110 transition duration-500 filter grayscale group-hover:grayscale-0">
            </div>
            <h3 class="text-2xl font-black text-white uppercase tracking-wider">B.Tech</h3>
            <div class="h-1 w-10 bg-[#ff007f] mx-auto my-2"></div><p class="text-sm text-gray-400 font-bold">Engineering & Tech</p>
        </div>
        <div class="cyber-panel p-5 text-center group">
            <div class="overflow-hidden rounded-lg border-2 border-[#ff6600] mb-4">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRDyoa4TiqjDJIfK4uH6Jm9oZZt9sfYbPtaKvMYV7C-Q&s=10" class="w-full h-40 object-cover group-hover:scale-110 transition duration-500 filter grayscale group-hover:grayscale-0">
            </div>
            <h3 class="text-2xl font-black text-white uppercase tracking-wider">B.Sc Ag</h3>
            <div class="h-1 w-10 bg-[#ff6600] mx-auto my-2"></div><p class="text-sm text-gray-400 font-bold">Agricultural Sciences</p>
        </div>
        <div class="cyber-panel p-5 text-center group">
            <div class="overflow-hidden rounded-lg border-2 border-[#5c3a21] mb-4">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQA3_TQ5uqXohLaqJG123pdT9QfB-O5kVRT-s7rOXseSg&s=10" class="w-full h-40 object-cover group-hover:scale-110 transition duration-500 filter grayscale group-hover:grayscale-0">
            </div>
            <h3 class="text-2xl font-black text-white uppercase tracking-wider">PUCAT</h3>
            <div class="h-1 w-10 bg-[#5c3a21] mx-auto my-2"></div><p class="text-sm text-gray-400 font-bold">University Entrance Exam</p>
        </div>
    </div>
</div>
"""

DEVELOPER_HTML = """
<div class="max-w-4xl mx-auto">
    <div class="cyber-panel p-1 border-t-4 border-[#ff6600]">
        <div class="bg-black bg-opacity-60 p-8 md:p-12 rounded-lg flex flex-col md:flex-row items-center gap-10 relative overflow-hidden">
            <div class="absolute inset-0 opacity-10 font-mono text-[8px] text-[#00ff66] select-none pointer-events-none overflow-hidden" style="line-height: 1;">
                01010010 01100001 01101010 00100000 01000111 01100001 01110101 01110100 01100001 01101101<br>def init_system(): pass<br>import os, sys, hacking_module<br>while True: build_future()<br>01010010 01100001 01101010 00100000 01000111 01100001 01110101 01110100 01100001 01101101<br>def init_system(): pass<br>import os, sys, hacking_module<br>while True: build_future()
            </div>
            <div class="relative z-10 shrink-0">
                <div class="absolute inset-0 bg-[#ff6600] rounded-full blur-md opacity-50 animate-pulse"></div>
                <img src="https://ui-avatars.com/api/?name=Raj+Gautam&background=ff6600&color=fff&size=256&font-size=0.33&bold=true" alt="Developer" class="relative w-48 h-48 rounded-full border-4 border-[#ff6600] object-cover">
                <div class="absolute -bottom-3 left-1/2 transform -translate-x-1/2 bg-black border border-[#00ff66] text-[#00ff66] text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-widest whitespace-nowrap">Sys Admin</div>
            </div>
            <div class="relative z-10 w-full text-center md:text-left">
                <div class="flex items-center justify-center md:justify-start gap-3 mb-2">
                    <h2 class="text-4xl md:text-5xl font-black text-white uppercase tracking-wider">Raj Gautam</h2>
                    <span class="w-3 h-3 bg-[#ff007f] rounded-full animate-ping"></span>
                </div>
                <p class="neon-text-grn text-lg font-bold tracking-widest uppercase mb-4 cyber-font">Full Stack Architect</p>
                <p class="text-gray-300 text-md leading-relaxed mb-6 font-medium">Navigating the intersection of design and code. Currently mastering core computing concepts in the 5th Semester of BCA at VBSPU. Built this library access portal to bridge academic infrastructure with next-gen futuristic UI.</p>
                <div class="flex flex-wrap justify-center md:justify-start gap-3">
                    <span class="bg-[#5c3a21] border border-[#ff6600] px-4 py-1.5 rounded text-xs font-bold text-white uppercase tracking-widest hover:bg-[#ff6600] transition cursor-default">Python Core</span>
                    <span class="bg-[#5c3a21] border border-[#ff007f] px-4 py-1.5 rounded text-xs font-bold text-white uppercase tracking-widest hover:bg-[#ff007f] transition cursor-default">Flask Backend</span>
                    <span class="bg-[#5c3a21] border border-[#00ff66] px-4 py-1.5 rounded text-xs font-bold text-white uppercase tracking-widest hover:bg-[#00ff66] transition cursor-default">UI/UX Design</span>
                </div>
            </div>
        </div>
    </div>
</div>
"""

# ==========================================
# 4. FLASK ROUTES
# ==========================================
def render_page(content_html, **kwargs):
    rendered_content = render_template_string(content_html, **kwargs)
    return render_template_string(BASE_HTML, content=rendered_content)

@app.route('/')
def home(): return render_page(HOME_HTML)

@app.route('/about')
def about(): return render_page(ABOUT_HTML)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    pass_data = None
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        course = request.form['course']
        shift = request.form['shift']
        
        pass_code = f"VBSPU-{random.randint(100,999)}-{random.randint(1000,9999)}"
        
        # 🟢 NEW FEATURE: Console Live Server Printing
        print("\n" + "="*50)
        print(f"🚨 ALERT: NEW PASS GENERATED AT {datetime.now().strftime('%H:%M:%S')} 🚨")
        print("="*50)
        print(f"👨‍🎓 STUDENT NAME : {name}")
        print(f"🆔 ROLL NUMBER  : {roll_no}")
        print(f"📚 COURSE       : {course}")
        print(f"⏱️ SHIFT        : {shift}")
        print(f"🔑 PASS CODE    : {pass_code}")
        print("="*50 + "\n")
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('INSERT INTO passes (student_name, roll_no, course, shift, pass_code) VALUES (?, ?, ?, ?, ?)', 
                  (name, roll_no, course, shift, pass_code))
        conn.commit()
        conn.close()
        
        pass_data = {"name": name, "course": course, "shift": shift, "code": pass_code}
        
    return render_page(BOOKING_HTML, pass_data=pass_data)

@app.route('/courses')
def courses(): return render_page(COURSES_HTML)

@app.route('/developer')
def developer(): return render_page(DEVELOPER_HTML)

if __name__ == '__main__':
    init_db()
    print("\n🚀 CYBER-LIB SYSTEM INITIALIZED: RUNNING ON http://127.0.0.1:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
