import json
import os
import uuid
from datetime import date as date_obj
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

HOF_PATH      = os.path.join('data', 'hof.json')
ROADMAP_PATH  = os.path.join('data', 'roadmap.json')
ARCHIVE_PATH = os.path.join('data', 'archive.json')
ARCHIVE_FOLDER = os.path.join('static', 'uploads', 'archive')
ARCHIVE_EXTENSIONS = {'pdf', 'docx', 'hwp', 'md', 'ppt', 'pptx', 'txt'}

FILE_ICONS = {
    'pdf': '📄', 'docx': '📄', 'hwp': '📄',
    'md': '📄', 'ppt': '📄', 'pptx': '📄',
}

HOF_ICONS = {
  'defcon_finalist': '<svg viewBox="0 0 16 16" fill="currentColor" width="46" height="46"><rect x="3" y="1" width="10" height="8" rx="4"/><rect x="4" y="9" width="8" height="5"/><rect x="3" y="3" width="3" height="3" fill="black" opacity=".45"/><rect x="10" y="3" width="3" height="3" fill="black" opacity=".45"/><rect x="4" y="12" width="3" height="2" fill="black" opacity=".45"/><rect x="9" y="12" width="3" height="2" fill="black" opacity=".45"/><rect x="7" y="6" width="2" height="2" fill="black" opacity=".35"/></svg>',
  'elite_operative': '<svg viewBox="0 0 16 16" fill="currentColor" width="46" height="46"><path d="M8 1L2 3.5V9c0 3.5 2.5 6 6 7 3.5-1 6-3.5 6-7V3.5L8 1z"/><polygon points="8,5.5 9,8 11.5,8 9.5,9.5 10.5,12 8,10.5 5.5,12 6.5,9.5 4.5,8 7,8" fill="black" opacity=".45"/></svg>',
  'the_president':   '<svg viewBox="0 0 16 16" fill="currentColor" width="46" height="46"><rect x="1" y="12" width="14" height="2.5" rx="1"/><path d="M2.5 12L4 6l2.5 2.5L8 3l1.5 5.5L12 6l1.5 6H2.5z"/><circle cx="3.5" cy="5" r="1.5"/><circle cx="8" cy="2.5" r="1.5"/><circle cx="12.5" cy="5" r="1.5"/></svg>',
  'bob_whs':         '<svg viewBox="0 0 16 16" fill="currentColor" width="46" height="46"><polygon points="8,1 14.5,4 8,5 1.5,4"/><rect x="1.5" y="4" width="13" height="1.5"/><rect x="2" y="13.5" width="12" height="2" rx="1"/><rect x="4" y="5.5" width="8" height="8"/><rect x="5.5" y="7.5" width="5" height="1" fill="black" opacity=".4"/><rect x="5.5" y="9.5" width="5" height="1" fill="black" opacity=".4"/><rect x="5.5" y="11.5" width="3.5" height="1" fill="black" opacity=".4"/></svg>',
  'english_master':  '<svg viewBox="0 0 16 16" fill="currentColor" width="46" height="46"><circle cx="8" cy="8" r="7" opacity=".2"/><path d="M8 1.5a6.5 6.5 0 1 0 0 13A6.5 6.5 0 0 0 8 1.5zm0 1c.6 0 1.6 1.6 2.2 4.1H5.8C6.4 4.1 7.4 2.5 8 2.5zM5.5 8c0-.5.1-1 .2-1.4h4.6c.1.4.2.9.2 1.4s-.1 1-.2 1.4H5.7A6 6 0 0 1 5.5 8zm-2.7 0c0-.5.1-1 .2-1.4h1.5A7.7 7.7 0 0 0 4.4 8c0 .5 0 1 .1 1.4H2.8A5.5 5.5 0 0 1 2.8 8zm5.2 5c-.6 0-1.6-1.6-2.2-4.1h4.4C9.6 11.4 8.6 13 8 13zm2.8-1c.7-.9 1.2-2.2 1.2-3.6v-.5l.2-.9h1.5A5.5 5.5 0 0 1 10.8 12z"/></svg>',
  'jlpt':            '<svg viewBox="0 0 16 16" fill="currentColor" width="46" height="46"><rect x="1" y="13" width="14" height="2" rx="1"/><rect x="7" y="2" width="2" height="11"/><rect x="2" y="4.5" width="12" height="2"/><rect x="2" y="4.5" width="2" height="8.5"/><rect x="12" y="4.5" width="2" height="8.5"/></svg>',
  'hsk':             '<svg viewBox="0 0 16 16" fill="currentColor" width="46" height="46"><rect x="1" y="1" width="14" height="14" rx="1" opacity=".15"/><rect x="1" y="7.5" width="14" height="1.5"/><rect x="7.5" y="1" width="1.5" height="14"/><rect x="2" y="3" width="4" height="1.5"/><rect x="10" y="3" width="4" height="1.5"/><rect x="2" y="11.5" width="4" height="1.5"/><rect x="10" y="11.5" width="4" height="1.5"/></svg>',
  'multi_linguist':  '<svg viewBox="0 0 16 16" fill="currentColor" width="46" height="46"><rect x="1" y="2" width="9" height="6" rx="1.5"/><rect x="3.5" y="8" width="2" height="1.5"/><rect x="1" y="8" width="3" height="1" opacity=".4"/><rect x="6" y="7.5" width="9" height="5.5" rx="1.5"/><rect x="12" y="13" width="2" height="1.5"/><rect x="11" y="13" width="3.5" height="1" opacity=".4"/></svg>',
  'niat':            '<svg viewBox="0 0 16 16" fill="currentColor" width="46" height="46"><circle cx="8" cy="8" r="7" opacity=".15"/><circle cx="8" cy="8" r="4.5" opacity=".2"/><circle cx="8" cy="8" r="2"/><rect x="7.2" y="1" width="1.6" height="3.5"/><rect x="7.2" y="11.5" width="1.6" height="3.5"/><rect x="1" y="7.2" width="3.5" height="1.6"/><rect x="11.5" y="7.2" width="3.5" height="1.6"/></svg>',
  'certified':       '<svg viewBox="0 0 16 16" fill="currentColor" width="46" height="46"><rect x="1" y="2" width="14" height="9" rx="1"/><rect x="3" y="4" width="5" height="1" fill="black" opacity=".4"/><rect x="3" y="6" width="7" height="1" fill="black" opacity=".4"/><rect x="3" y="8" width="4" height="1" fill="black" opacity=".4"/><circle cx="11.5" cy="13" r="3"/><circle cx="11.5" cy="13" r="1.5" fill="black" opacity=".3"/><rect x="10.5" y="15" width="2" height="1"/></svg>',
  'black_belt':      '<svg viewBox="0 0 16 16" fill="currentColor" width="46" height="46"><rect x="1" y="6.5" width="14" height="3" rx="1"/><rect x="6" y="5.5" width="4" height="5" rx="0.5"/><rect x="7" y="4" width="2" height="1.5"/><rect x="7" y="10.5" width="2" height="1.5"/><rect x="2.5" y="8" width="11" height="0.5" fill="black" opacity=".3"/></svg>',
  'security_researcher': '<svg viewBox="0 0 16 16" fill="currentColor" width="46" height="46"><path d="M6.5 1a5.5 5.5 0 1 0 0 11 5.5 5.5 0 0 0 0-11zm0 1.5a4 4 0 1 1 0 8 4 4 0 0 1 0-8z"/><rect x="9.8" y="10.2" width="5.5" height="1.8" rx="0.9" transform="rotate(45 9.8 10.2)"/></svg>',
  'ctf_veteran':     '<svg viewBox="0 0 16 16" fill="currentColor" width="46" height="46"><rect x="2" y="1" width="2" height="14" rx="1"/><rect x="4" y="2" width="10" height="6.5" rx="1"/><rect x="4" y="2" width="10" height="1.5" opacity=".3" fill="black"/><rect x="4" y="7" width="10" height="1.5" opacity=".2" fill="black"/></svg>',
  'bug_hunter':      '<svg viewBox="0 0 16 16" fill="currentColor" width="46" height="46"><ellipse cx="8" cy="9.5" rx="3.5" ry="4.5"/><circle cx="8" cy="5" r="2.5"/><rect x="11" y="6" width="3.5" height="1.2" rx=".6" transform="rotate(-25 11 6)"/><rect x="1.5" y="6" width="3.5" height="1.2" rx=".6" transform="rotate(25 1.5 6)"/><rect x="11.5" y="9" width="3" height="1.2" rx=".6" transform="rotate(-10 11.5 9)"/><rect x="1.5" y="9" width="3" height="1.2" rx=".6" transform="rotate(10 1.5 9)"/><rect x="10.5" y="11.5" width="3" height="1.2" rx=".6" transform="rotate(20 10.5 11.5)"/><rect x="2.5" y="11.5" width="3" height="1.2" rx=".6" transform="rotate(-20 2.5 11.5)"/></svg>',
  'active_project':  '<svg viewBox="0 0 16 16" fill="currentColor" width="46" height="46"><circle cx="8" cy="8" r="2.5"/><rect x="7.2" y="1" width="1.6" height="2.5"/><rect x="7.2" y="12.5" width="1.6" height="2.5"/><rect x="1" y="7.2" width="2.5" height="1.6"/><rect x="12.5" y="7.2" width="2.5" height="1.6"/><rect x="3" y="3" width="1.8" height="1.8" transform="rotate(45 3 3)"/><rect x="11.2" y="3" width="1.8" height="1.8" transform="rotate(45 11.2 3)"/><rect x="3" y="11.2" width="1.8" height="1.8" transform="rotate(45 3 11.2)"/><rect x="11.2" y="11.2" width="1.8" height="1.8" transform="rotate(45 11.2 11.2)"/></svg>',
}

def load_archive():
    with open(ARCHIVE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_archive(data):
    with open(ARCHIVE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def allowed_archive(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ARCHIVE_EXTENSIONS

def load_roadmap():
    with open(ROADMAP_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_roadmap(data):
    with open(ROADMAP_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_hof():
    with open(HOF_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_hof(data):
    with open(HOF_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

@app.template_filter('file_icon')
def file_icon_filter(filename):
    return '📁'

DATA_PATH = os.path.join('data', 'profile.json')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def normalize_images(images):
    result = []
    for img in images:
        if isinstance(img, str):
            result.append({'filename': img, 'caption': '', 'date': ''})
        elif isinstance(img, dict):
            img.setdefault('caption', '')
            img.setdefault('date', '')
            result.append(img)
    return result

def load_profile():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        p = json.load(f)
    p.setdefault('profile_image', '')
    p.setdefault('mood', '')
    p.setdefault('location', '')
    p.setdefault('now_working', '')
    p.setdefault('status_extra', [])
    p.setdefault('skills', [])
    p.setdefault('stack_languages', [])
    p.setdefault('stack_security', [])
    p.setdefault('stack_tools', [])
    p['images'] = normalize_images(p.get('images', []))
    return p

def save_profile(data):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', p=load_profile())

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    p = load_profile()
    if request.method == 'POST':
        p['name']        = request.form.get('name', '')
        p['age']         = request.form.get('age', '')
        p['grade']       = request.form.get('grade', '')
        p['org']         = request.form.get('org', '')
        p['specialty']   = request.form.get('specialty', '')
        p['mbti']        = request.form.get('mbti', '')
        p['goal']        = request.form.get('goal', '')
        p['current']     = request.form.get('current', '')
        p['mood']        = request.form.get('mood', '')
        p['location']    = request.form.get('location', '')
        p['now_working'] = request.form.get('now_working', '')
        p['about']       = request.form.get('about', '')
        p['stack_languages'] = [s.strip() for s in request.form.get('stack_languages', '').split(',') if s.strip()]
        p['stack_security']  = [s.strip() for s in request.form.get('stack_security', '').split(',') if s.strip()]
        p['stack_tools']     = [s.strip() for s in request.form.get('stack_tools', '').split(',') if s.strip()]
        p['affiliation'] = [s.strip() for s in request.form.get('affiliation', '').split('\n') if s.strip()]

        extra_texts = request.form.getlist('extra_text')
        extra_dots  = request.form.getlist('extra_dot')
        p['status_extra'] = [
            {'dot': dot, 'text': text.strip()}
            for dot, text in zip(extra_dots, extra_texts) if text.strip()
        ]

        skill_names = request.form.getlist('skill_name')
        skill_pcts  = request.form.getlist('skill_pct')
        p['skills'] = [
            {'name': name.strip(), 'pct': max(0, min(100, int(pct) if pct.isdigit() else 0))}
            for name, pct in zip(skill_names, skill_pcts) if name.strip()
        ]

        contact = []
        for icon, label, url, sub in zip(
            request.form.getlist('contact_icon'),
            request.form.getlist('contact_label'),
            request.form.getlist('contact_url'),
            request.form.getlist('contact_sub'),
        ):
            if label.strip():
                contact.append({'icon': icon, 'label': label.strip(), 'url': url.strip(), 'sub': sub.strip()})
        p['contact'] = contact

        save_profile(p)
        return redirect(url_for('index'))

    return render_template('edit.html', p=p)

@app.route('/upload_profile', methods=['POST'])
def upload_profile():
    p = load_profile()
    file = request.files.get('profile_image')
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f'profile_pic.{ext}'
        for old_ext in ALLOWED_EXTENSIONS:
            old_path = os.path.join(app.config['UPLOAD_FOLDER'], f'profile_pic.{old_ext}')
            if os.path.exists(old_path):
                os.remove(old_path)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        p['profile_image'] = filename
        save_profile(p)
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
    p = load_profile()
    file = request.files.get('image')
    caption = request.form.get('caption', '').strip()
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        base, ext = os.path.splitext(filename)
        i = 1
        while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            filename = f'{base}_{i}{ext}'
            i += 1
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        p['images'].append({
            'filename': filename,
            'caption': caption,
            'date': date_obj.today().isoformat()
        })
        save_profile(p)
    return redirect(url_for('index'))

@app.route('/delete_image/<filename>', methods=['POST'])
def delete_image(filename):
    p = load_profile()
    safe = secure_filename(filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], safe)
    if os.path.exists(path):
        os.remove(path)
    p['images'] = [img for img in p['images'] if img['filename'] != safe]
    save_profile(p)
    return redirect(url_for('index'))

@app.route('/archive')
def archive():
    data = load_archive()
    return render_template('archive.html', files=data['files'])

@app.route('/archive/upload', methods=['POST'])
def archive_upload():
    data = load_archive()
    file = request.files.get('file')
    title    = request.form.get('title', '').strip()
    category = request.form.get('category', '기타')
    desc     = request.form.get('desc', '').strip()
    if file and title and allowed_archive(file.filename):
        filename = secure_filename(file.filename)
        base, ext = os.path.splitext(filename)
        i = 1
        while os.path.exists(os.path.join(ARCHIVE_FOLDER, filename)):
            filename = f'{base}_{i}{ext}'
            i += 1
        file.save(os.path.join(ARCHIVE_FOLDER, filename))
        data['files'].append({
            'filename': filename,
            'title':    title,
            'category': category,
            'desc':     desc,
            'date':     date_obj.today().isoformat(),
        })
        save_archive(data)
    return redirect(url_for('archive'))

@app.route('/archive/download/<filename>')
def archive_download(filename):
    safe = secure_filename(filename)
    return send_from_directory(os.path.abspath(ARCHIVE_FOLDER), safe, as_attachment=True)

@app.route('/archive/delete/<filename>', methods=['POST'])
def archive_delete(filename):
    data = load_archive()
    safe = secure_filename(filename)
    path = os.path.join(ARCHIVE_FOLDER, safe)
    if os.path.exists(path):
        os.remove(path)
    data['files'] = [f for f in data['files'] if f['filename'] != safe]
    save_archive(data)
    return redirect(url_for('archive'))

@app.route('/roadmap')
def roadmap():
    return render_template('roadmap.html', steps=load_roadmap())

@app.route('/roadmap/toggle/<step_id>/<node_id>', methods=['POST'])
def roadmap_toggle(step_id, node_id):
    data = load_roadmap()
    result = {'unlocked': False}
    for step in data:
        if step['id'] == step_id:
            for node in step['nodes']:
                if node['id'] == node_id:
                    node['unlocked'] = not node['unlocked']
                    result['unlocked'] = node['unlocked']
                    break
    save_roadmap(data)
    return jsonify(result)

@app.route('/roadmap/update/<step_id>/<node_id>', methods=['POST'])
def roadmap_update(step_id, node_id):
    data = load_roadmap()
    body = request.get_json()
    for step in data:
        if step['id'] == step_id:
            for node in step['nodes']:
                if node['id'] == node_id:
                    node['title'] = body.get('title', node['title'])
                    node['desc']  = body.get('desc',  node['desc'])
                    break
    save_roadmap(data)
    return jsonify({'ok': True})

@app.route('/roadmap/add/<step_id>', methods=['POST'])
def roadmap_add(step_id):
    data = load_roadmap()
    body = request.get_json()
    title = body.get('title', '').strip()
    desc  = body.get('desc',  '').strip()
    if not title:
        return jsonify({'ok': False}), 400
    node_id = 'node_' + uuid.uuid4().hex[:8]
    for step in data:
        if step['id'] == step_id:
            step['nodes'].append({'id': node_id, 'title': title, 'desc': desc, 'unlocked': False})
            break
    save_roadmap(data)
    return jsonify({'ok': True, 'id': node_id})

@app.route('/hof')
def hof():
    data = load_hof()
    return render_template('hof.html', badges=data['badges'], icons=HOF_ICONS)

@app.route('/hof/edit', methods=['GET', 'POST'])
def hof_edit():
    data = load_hof()
    if request.method == 'POST':
        badge_ids = request.form.getlist('badge_id')
        for badge in data['badges']:
            bid = badge['id']
            badge['locked']            = f'locked_{bid}' in request.form
            badge['date']              = request.form.get(f'date_{bid}', '').strip()
            badge['link']              = request.form.get(f'link_{bid}', '').strip()
            badge['unlock_condition']  = request.form.get(f'condition_{bid}', '').strip()
            badge['detail']            = request.form.get(f'detail_{bid}', '').strip()
        save_hof(data)
        return redirect(url_for('hof'))
    return render_template('hof_edit.html', badges=data['badges'])

if __name__ == '__main__':
    app.run(debug=True, port=5001)
