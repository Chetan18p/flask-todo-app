from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
# tasks is a list of dicts: {'text': str, 'done': bool, 'created_at': str, 'completed_at': str}
tasks = []

# Helper functions (unit-testable)
def add_task(text: str) -> bool:
    text = (text or "").strip()
    if not text:
        return False
    # prevent exact duplicates
    if any(t['text'] == text for t in tasks):
        return False
    tasks.append({
        'text': text, 
        'done': False, 
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'completed_at': None
    })
    return True

def edit_task(task_id: int, new_text: str) -> bool:
    new_text = (new_text or "").strip()
    if not (0 <= task_id < len(tasks)) or not new_text:
        return False
    # prevent duplicate when changing
    if any(i != task_id and t['text'] == new_text for i, t in enumerate(tasks)):
        return False
    tasks[task_id]['text'] = new_text
    return True

def toggle_task(task_id: int) -> bool:
    if not (0 <= task_id < len(tasks)):
        return False
    tasks[task_id]['done'] = not tasks[task_id]['done']
    # Set completed_at timestamp when marking as done
    if tasks[task_id]['done']:
        tasks[task_id]['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        tasks[task_id]['completed_at'] = None
    return True

def delete_task(task_id: int) -> bool:
    if not (0 <= task_id < len(tasks)):
        return False
    tasks.pop(task_id)
    return True

def clear_tasks() -> None:
    """Clear only pending (not completed) tasks"""
    global tasks
    tasks[:] = [task for task in tasks if task['done']]

# Routes
@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    add_task(task)
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    new_text = request.form.get('task')
    edit_task(task_id, new_text)
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    toggle_task(task_id)
    return redirect(url_for('index'))

@app.route('/complete', methods=['POST'])
def complete():
    selected = request.form.getlist('selected')
    # Convert to integers and mark as done
    for task_id_str in selected:
        try:
            task_id = int(task_id_str)
            toggle_task(task_id)
        except (ValueError, IndexError):
            pass
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    delete_task(task_id)
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear():
    clear_tasks()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)