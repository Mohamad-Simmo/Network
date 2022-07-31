document.querySelectorAll('.like-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    fetch(`/entity/${btn.dataset.like}/${btn.parentElement.dataset.id}`).then(
      (response) => {
        if (response.status == 401) {
          window.location.replace('/login');
        } else {
          if (btn.dataset.like == 'like') {
            btn.dataset.like = 'unlike';
            btn.children[0].classList.replace('bi-heart', 'bi-heart-fill');
            btn.children[0].classList.add('text-danger');
            btn.children[1].innerText = parseInt(btn.children[1].innerText) + 1;
          } else if (btn.dataset.like == 'unlike') {
            btn.dataset.like = 'like';
            btn.children[0].classList.replace('bi-heart-fill', 'bi-heart');
            btn.children[0].classList.remove('text-danger');
            btn.children[1].innerText = parseInt(btn.children[1].innerText) - 1;
          } else console.log('invalid');
        }
      }
    );
  });
});

document.querySelectorAll('.edit-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    btn.style.display = 'none';
    postId = btn.parentElement.dataset.id;
    postText = btn.nextElementSibling.innerText;
    editField = document.createElement('div');
    editField.innerHTML = `
      <form id="saveEdit">
        <textarea class="form-control" name="editText">${postText}</textarea>
        <input type="submit" class="btn btn-primary mt-2" value="save">
      </form>
    `;
    textFieldElement = btn.nextElementSibling;
    btn.nextElementSibling.replaceWith(editField);
    editForm = document.getElementById('saveEdit');
    editForm.addEventListener('submit', (event) => {
      event.preventDefault();
      newPost = editForm.elements.editText.value;
      fetch(`/edit_post/${postId}`, {
        method: 'PUT',
        body: JSON.stringify({
          new_post: newPost,
        }),
      }).then(() => {
        textFieldElement.innerText = newPost;
        editField.replaceWith(textFieldElement);
        btn.style.display = 'block';
      });
    });
  });
});
