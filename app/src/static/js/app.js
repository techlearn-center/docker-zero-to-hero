const form = document.getElementById('todo-form');
const input = document.getElementById('todo-input');
const todoList = document.getElementById('todo-list');
const emptyState = document.getElementById('empty-state');

// Fetch and render all todos
async function loadTodos() {
    const res = await fetch('/api/todos');
    const todos = await res.json();
    renderTodos(todos);
}

// Render todo list
function renderTodos(todos) {
    todoList.innerHTML = '';
    if (todos.length === 0) {
        emptyState.classList.remove('hidden');
    } else {
        emptyState.classList.add('hidden');
        todos.forEach(todo => {
            const item = document.createElement('div');
            item.className = 'todo-item';
            item.innerHTML = `
                <input type="checkbox" ${todo.completed ? 'checked' : ''}
                    onchange="toggleTodo('${todo.id}', '${todo.title.replace(/'/g, "\\'")}', this.checked)" />
                <span class="title ${todo.completed ? 'completed' : ''}">${escapeHtml(todo.title)}</span>
                <button class="delete-btn" onclick="deleteTodo('${todo.id}')">&#10005;</button>
            `;
            todoList.appendChild(item);
        });
    }
}

// Add a new todo
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = input.value.trim();
    if (!title) return;

    await fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
    });

    input.value = '';
    loadTodos();
});

// Toggle todo completion
async function toggleTodo(id, title, completed) {
    await fetch(`/api/todos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, completed })
    });
    loadTodos();
}

// Delete a todo
async function deleteTodo(id) {
    await fetch(`/api/todos/${id}`, { method: 'DELETE' });
    loadTodos();
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initial load
loadTodos();
