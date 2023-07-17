function getCookie(name){
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
}

function submit(id){
    const content_txt = document.getElementById(`textarea${id}`).value
    const content = document.getElementById(`content${id}`);
    const collapse = document.getElementById(`collapseExample${id}`);
    fetch(`/edit/${id}`, {
      method: "POST",
      headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
      body: JSON.stringify({
        content: content_txt
      })
    })
    .then(response => response.json())
    .then(result => {
      content.innerHTML = result.data;
    })
}

function count(id) {
    var likescounter = document.getElementById(`num_likes_${id}`).innerHTML;
    likescounter++;
    document.getElementById(`num_likes_${id}`).innerHTML= likescounter;
  }

  document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('button').onclick = count;
});