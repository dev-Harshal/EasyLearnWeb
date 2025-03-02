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

function startTimer() {
    let countdown;
    let countdownTime = 30;
    let timerElement = document.getElementById('resendTimer');
    timerElement.textContent = countdownTime;
    resendButton.disabled = true;
    countdown = setInterval(() => {
        countdownTime--;
        timerElement.textContent = countdownTime;
        if (countdownTime <= 0) {
            clearInterval(countdown);
            resendButton.disabled = false;
        }
    }, 1000);  
}

function showOtpSection() {
    otpSection = document.getElementById('otpSection')
    verifyBtn = document.getElementById('verifyBtn')
    loginBtn = document.querySelector('.login-btn')
    otpCode = document.getElementById('otpCode')
    emailId = document.getElementById('email')
    password = document.getElementById('password')

    otpSection.classList.remove('d-none')
    emailId.disabled = true
    password.disabled = true
    otpCode.disabled = false
    verifyBtn.classList.remove('d-none')
    verifyBtn.disabled = false
    loginBtn.disabled = true
    loginBtn.classList.add('d-none')
    startTimer()
}

function login() {
    let formData = new FormData()
    const email = document.querySelector('input[name="email"]').value
    const password = document.querySelector('input[name="password"]').value
    formData.append('email', email)
    formData.append('password', password)
    
    fetch('/login/', {
        method : 'POST',
        headers : {
            'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body : formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showOtpSection();
            popAlert(data);
        }
        else {
            popAlert(data);
        }
    })
}

function staffLogin() {
    let formData = new FormData()
    const email = document.querySelector('input[name="email"]').value
    const password = document.querySelector('input[name="password"]').value
    const role = document.querySelector('input[name="role"]').value
    formData.append('email', email)
    formData.append('password', password)

    url = `/${role}/login/`
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
            showOtpSection();
            popAlert(data);
        }
        else {
            popAlert(data);
        }
    })
}

function verifyOtp() {
    const formData = new FormData()
    email = document.querySelector('input[name="email"]').value
    password = document.querySelector('input[name="password"]').value,
    otp_code = document.querySelector('input[name="otp_code"]').value,
    formData.append('email', email)
    formData.append('password', password)
    formData.append('otp_code', otp_code)

    fetch('/verify-otp/',{
        method:'POST',
        headers:{
            'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: formData 
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === 'success'){
            window.location.href = data.success_url
        }
        else{
            popAlert(data)
        }
    })
}

alertBox = document.getElementById('alert')
if (alertBox) {
    setTimeout(function() {
        alertBox.style.display = 'none';
    }, 5000);
}

const registerForm = document.getElementById('registerForm')
if (registerForm) {
    registerForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(registerForm)
        url = '/register/'
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
                window.location.href = data.success_url
            }
            else {
                popAlert(data);
            }
        })
    })
}

const resendButton = document.getElementById('resendBtn');
if (resendButton){
    resendButton.addEventListener('click', function(event) {
        event.preventDefault();
        if (event.target.value === 'staff-login') {
            if (!resendButton.disabled) {
                staffLogin();
            }
        }
        else {
            if (!resendButton.disabled) {
                login();
            }
        }

    });
}

const loginForm = document.getElementById('loginForm')
if (loginForm) {
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
    
        if (event.submitter.id === 'studentLoginBtn') {
            login();
        }
        else if (event.submitter.id === 'staffLoginBtn') {
            staffLogin();
        }
        else {
            verifyOtp();
        }
    })
}


const createTeacherForm = document.getElementById('createTeacherForm')
if (createTeacherForm) {
    createTeacherForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(createTeacherForm)
        fetch('/admin/create/teacher/',{
            method : 'POST',
            headers : {
                'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body : formData
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success'){
                window.location.href = data.success_url
            }
            else{
                window.scrollTo({ top: 0, behavior: 'smooth' });
                popAlert(data)
            }
        })
        
    })
}

const updateTeacherForm = document.getElementById('updateTeacherForm')
if (updateTeacherForm) {
    updateTeacherForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const formData = new FormData(updateTeacherForm)
        const id = document.getElementById('id').value
        url = `/admin/update/teacher/${id}/`
        fetch(url,{
            method : 'POST',
            headers : {
                'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body : formData
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success'){
                window.location.href = data.success_url
            }
            else{
                window.scrollTo({ top: 0, behavior: 'smooth' });
                popAlert(data)
            }
        })
        
    })
}

const staffProfileForm = document.getElementById('staffProfileForm')
if (staffProfileForm) {
    staffProfileForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(staffProfileForm)
        const role = document.getElementById('role').value
        url = `/${role}/profile/`
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
                window.location.href = data.success_url
            }
            else {
                popAlert(data)
            }
        })
    })
}

const changePasswordForm = document.getElementById('changePasswordForm')
if (changePasswordForm) {
    changePasswordForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(changePasswordForm)
        fetch('/change-password/', {
            method : 'POST',
            headers : {
                'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body : formData
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