function popAlert(data) {
    let status
    let alertContainer = document.getElementById('alertContainer');
    let alert = document.createElement('div');
    alertContainer.innerHTML = ''
    alert.id = 'alert'
    
    if (data.status === 'error') {
        status = 'danger'
    }
    else{
        status = data.status
    }
    alert.className = `alert alert-${status}`
    alert.role = 'alert'
    alert.innerHTML = `${data.message}`
    setTimeout(() => {
        alertContainer.appendChild(alert)
        setTimeout(() => {
            alert.style.display = 'none'
        },5000)
    },200)
}

const createCourseForm = document.getElementById('createCourseForm')
if (createCourseForm) {
    createCourseForm.addEventListener('submit', function(event) {
        event.preventDefault();

        fetch('/teacher/create/course/', {
            method : 'POST',
            headers : {
                'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body : new FormData(createCourseForm)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = data.success_url
            }
            else {
                popAlert(data)
            }
        })
    })
}

const updateCourseForm = document.getElementById('updateCourseForm')
if (updateCourseForm) {
    updateCourseForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const id = document.getElementById('id').value

        url = `/teacher/update/course/${id}/`
        fetch(url, {
            method : 'POST',
            headers : {
                'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body : new FormData(updateCourseForm)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = data.success_url
            }
            else {
                window.scrollTo({ top: 0, behavior: 'smooth' });
                popAlert(data)
            }
        })
    })
}