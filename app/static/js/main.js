document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('uploadForm');
    const preview = document.getElementById('preview');
    const fileInput = document.querySelector('input[type="file"]');
    
    // Preview image
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            preview.innerHTML = `
                <img src="${URL.createObjectURL(file)}" 
                     style="max-width: 200px; margin-top: 10px;">
            `;
        }
    });

    // Form submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        
        try {
            const response = await fetch('/add-person', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                alert('Успешно добавлено!');
                location.reload();
            } else {
                alert('Ошибка при добавлении');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Load people list
    loadPeople();

    async function loadPeople() {
        const response = await fetch('/people');
        const people = await response.json();
        
        const list = document.getElementById('peopleList');
        list.innerHTML = people.map(person => `
            <div class="person-card">
                <h3>${person.full_name}</h3>
                <img src="/static/faces/${person.face_image_path.split('/').pop()}" 
                     alt="${person.full_name}">
            </div>
        `).join('');
    }
});