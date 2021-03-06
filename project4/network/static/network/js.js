document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.postuser').forEach(button => button.addEventListener('click', event => postuser(event)))
    document.querySelectorAll('.btn.btn-outline-primary.btn-sm').forEach(button => button.addEventListener('click', event => edit(event)))
    document.querySelectorAll('.material-icons').forEach(button => button.addEventListener('click', button => clickicon(button)))
})


function postuser(event) {
    document.location.href = `profile/${event.target.innerText}`
}


function edit(event) {
    const editbutton = event.composedPath()[1].childNodes[3]
    editbutton.disabled = true
    const id = event.composedPath()[1].childNodes[11].innerText
    const element = event.composedPath()[1].childNodes[5]
    const textarea = document.createElement('textarea')
    textarea.value = element.innerText
    textarea.rows = 3
    element.innerText = ''
    element.appendChild(textarea)
    const button = document.createElement('button')
    button.className = 'btn btn-outline-primary btn-sm'
    button.innerText = 'Save'
    button.onclick = function() {
        fetch('/edit/edit', {
            method: 'POST',
            body: JSON.stringify({
                id: id,
                text: element.firstChild.value
            })
        })
        .then(response => response.json())
        .then(text => {
            element.innerHTML = text.text
            button.remove()
            editbutton.disabled = false
        })
    }
    element.after(button)
}


function clickicon(button) {
    if (button.composedPath()[0].innerText === 'favorite_border'){
        button.composedPath()[0].innerText = 'favorite'
    } else{
        button.composedPath()[0].innerText = 'favorite_border'
    }
    const id = button.composedPath()[2].querySelector('.hidden').innerText
    const nlikes = button.composedPath()[2].querySelector('.likes div')
    fetch('/edit/likes', {
        method: 'POST',
        body: JSON.stringify({
            id: id
        })
    })
    .then(response => response.json())
    .then(likes =>{
        nlikes.innerText = likes.likes
    })
}