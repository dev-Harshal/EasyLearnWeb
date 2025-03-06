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

// COURSE CONTENT CREATION

let sectionCount = 1;  // Initialize with one section by default

// Function to generate a section template
function createSection(sectionNumber) {
    return `
    <div class="col-12 section-item" data-section-number="${sectionNumber}">
        <div class="card">

            <!-- SECTION TITLE -->
            <div class="card-header bg-body-secondary">
                <div class="row align-items-center">
                    <div class="col-10">
                        <div class="row">
                            <label class="col-sm-2 col-form-label">Section (${sectionNumber}) :</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" placeholder="Title" name="section_title" required>
                                <input type="hidden" class="form-control" name="section_order" value="${sectionNumber}" required>
                            </div>
                        </div>
                    </div>
                    <div class="col-2 text-end">
                        <i class="bi bi-trash text-danger fs-5 remove-section"></i>
                    </div>
                </div>
            </div>

            <!-- SECTION CONTENT -->
            <div class="card-body">
                <div class="row g-3 p-2 item-container">
                    ${createVideoItem(sectionNumber, 1)}
                </div>
                <div class="col-12 text-end">
                    <div class="btn-group">
                        <button type="button" class="btn btn-primary btn-sm dropdown-toggle add-item-dropdown" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="bi bi-plus"></i> Add Item
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item addItem" href="#" data-type="video" data-section="${sectionNumber}">Video</a></li>
                            <li><a class="dropdown-item addItem" href="#" data-type="quiz" data-section="${sectionNumber}">Quiz</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `;
}

// Function to generate video template
function createVideoItem(sectionNumber, order) {
    return `
            <div class="col-12 item">
                <input type="hidden" class="form-control" name="item_order" value="${order}" required>
            <div class="row align-items-center video-item">
                <div class="col-11">
                    <div class="row g-3 justify-content-end">

                        <div class="col-12">
                            <div class="row">
                                <label class="col-sm-2 col-form-label video-label">(${order}) Video Title :</label>
                                <div class="col-sm-10">
                                    <input type="text" class="form-control" name="video_title" required>
                                </div>
                            </div>
                        </div>

                        <div class="col-10">
                            <div class="row">
                                <div class="col-6">
                                    <label class="form-label">Video File :</label>
                                    <input type="file" class="form-control" name="video_file" required>
                                </div>
                                <div class="col-6">
                                    <label class="form-label">Note File (Optional) :</label>
                                    <input type="file" class="form-control" name="note_file">
                                </div>    
                            </div>
                        </div>
                    <hr>
                    </div>
                </div>

                <div class="col-1 text-end">
                    <i class="bi bi-trash text-danger fs-5 remove-item"></i>
                </div>

            </div>
        </div>
    `;
} 

// Function to generate quiz template
function createQuizItem(sectionNumber, order) {
    return `
        <div class="col-12 item">
            <input type="hidden" class="form-control" name="item_order" value="${order}" required>

            <div class="row align-items-center quiz-item">
                <div class="col-11">
                    <div class="row g-3 justify-content-end">

                        <div class="col-12">
                            <div class="row">
                                <label class="col-sm-2 col-form-label quiz-label">(${order}) Quiz :</label>
                                <div class="col-sm-10">
                                    <input type="text" class="form-control" name="quiz_question" required>
                                </div>
                            </div>
                        </div>

                        <!-- Options -->
                        <div class="col-10">
                            <div class="row g-2">

                                <div class="col-6">
                                    <div class="row">
                                        <label class="col-sm-2 col-form-label">(1) :</label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" name="option" required>
                                        </div>
                                        <div class="col-sm-2">
                                            <input type="radio" name="isCorrect${sectionNumber}${order}" class="form-check-input" required>
                                        </div>
                                    </div>
                                </div>

                                <div class="col-6">
                                    <div class="row">
                                        <label class="col-sm-2 col-form-label">(2) :</label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" name="option" required>
                                        </div>
                                        <div class="col-sm-2">
                                            <input type="radio" name="isCorrect${sectionNumber}${order}" class="form-check-input" required>
                                        </div>
                                    </div>
                                </div>

                                <div class="col-6">
                                    <div class="row">
                                        <label class="col-sm-2 col-form-label">(3) :</label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" name="option" required>
                                        </div>
                                        <div class="col-sm-2">
                                            <input type="radio" name="isCorrect${sectionNumber}${order}" class="form-check-input" required>
                                        </div>
                                    </div>
                                </div>

                                <div class="col-6">
                                    <div class="row">
                                        <label class="col-sm-2 col-form-label">(4) :</label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" name="option" required>
                                        </div>
                                        <div class="col-sm-2">
                                            <input type="radio" name="isCorrect${sectionNumber}${order}" class="form-check-input" required>
                                        </div>
                                    </div>
                                </div>
                            
                            </div>
                        </div>
                    <hr>
                    </div>
                </div>

                <div class="col-1 text-end">
                    <i class="bi bi-trash text-danger fs-5 remove-item"></i>
                </div>

            </div>
        <div>
    `;
}

// Add default section on load
const sectionContainer = document.getElementById("sectionContainer")
if (sectionContainer) {
    sectionContainer.innerHTML += createSection(sectionCount);    
}

const addSection = document.getElementById("addSection")
if (addSection) {
    addSection.addEventListener("click", function(event) {
        event.preventDefault();  // Prevent page reload
        sectionCount++;
        const newSection = createSection(sectionCount);
        document.getElementById("sectionContainer").insertAdjacentHTML('beforeend', newSection);
        scrollToElement(document.querySelector(`[data-section-number="${sectionCount}"]`));
    });
}

// Handle adding video/quiz items dynamically via the dropdown
if (sectionContainer) {
    sectionContainer.addEventListener("click", function(e) {
        if (e.target && e.target.classList.contains("addItem")) {
            e.preventDefault();
            const sectionNumber = e.target.getAttribute('data-section');
            const section = e.target.closest('.section-item');
            const itemContainer = section.querySelector('.item-container');
            let itemType = e.target.getAttribute('data-type');
    
            let newItem;
            if (itemType === 'video') {
                
                newItem = createVideoItem(sectionNumber, itemContainer.childElementCount+1);
            } else if (itemType === 'quiz') {
                newItem = createQuizItem(sectionNumber, itemContainer.childElementCount+1);
            }
            itemContainer.insertAdjacentHTML('beforeend', newItem);
            scrollToElement(itemContainer.lastElementChild);  // Scroll to the newly added item
        }
        // Handle remove video/quiz
        if (e.target && e.target.classList.contains("remove-item")) {
            const section = e.target.closest('.section-item');
            e.target.closest('.item').remove();
            updateItemNumber(section);
        }
        // Handle remove section
        if (e.target && e.target.classList.contains("remove-section")) {
            e.target.closest('.section-item').remove();
            updateSectionNumbers();
        }
    });
}

function updateItemNumber(section) {
    const itemContainer = section.querySelector('.item-container');
    Array.from(itemContainer.children).forEach((item, index) => {
        const input = item.querySelector("input[name='item_order']");
        const videoLabel = item.querySelector(".video-label");
        const quizLabel = item.querySelector(".quiz-label");
        if (videoLabel) {
            videoLabel.textContent = `(${index + 1}) Video Title`;
        }
        if (quizLabel) {
            quizLabel.textContent = `(${index + 1}) Quiz :`;
        }
        input.value = index + 1;  // Update the order value
    });
}

    



// Update section numbers after removing
function updateSectionNumbers() {
    const sections = document.querySelectorAll(".section-item");
    sections.forEach((section, index) => {
        const label = section.querySelector(".card-header label");
        label.textContent = `Section (${index + 1}) :`;
    });
}

// Scroll to the newly added element smoothly
function scrollToElement(element) {
    element.scrollIntoView({ behavior: "smooth", block: "center" });
}

// Save curriculum using FormData
const saveCurriculumForm = document.getElementById("saveCurriculumForm");
if (saveCurriculumForm) {
    saveCurriculumForm.addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(saveCurriculumForm)

    const courseId = document.getElementById('courseId').value

    url =  `/teacher/save/curriculum/${courseId}/`

    fetch(url, {
        method : 'POST',
        headers : {
            'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body : formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Success')
        }
        else {
            alert('Failed')
        }
    })

   })
}