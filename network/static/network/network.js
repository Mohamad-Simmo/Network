document.querySelectorAll('.post').forEach((post) => {
  post.addEventListener('click', (event) => {
    const id = event.currentTarget.dataset.id;
    window.location.href = `/post/${id}`;
  });
});

const likePost = (el, event) => {
  event.stopPropagation();
  const action = el.dataset.action;
  const postId = el.parentElement.dataset.id;
  const icon = el.children[0];
  const count = el.children[1];
  fetch(`/entity/${action}/${postId}`).then((res) => {
    if (res.status == 401) {
      window.location.replace('/login');
    } else if (res.status == 204) {
      if (action == 'like') {
        el.dataset.action = 'unlike';
        icon.classList.replace('bi-heart', 'bi-heart-fill');
        icon.classList.add('text-danger');
        count.innerText = parseInt(count.innerText) + 1;
      } else {
        el.dataset.action = 'like';
        icon.classList.replace('bi-heart-fill', 'bi-heart');
        icon.classList.remove('text-danger');
        count.innerText = parseInt(count.innerText) - 1;
      }
    }
  });
};

let editing = false;
const editPost = (el, event) => {
  event.stopPropagation();
  if (editing) {
    let dropdown = el.closest('.menu').children[0];
    dropdown = bootstrap.Dropdown.getInstance(dropdown);
    dropdown.hide();
    return;
  }
  editing = true;
  let dropdown = el.closest('.menu').children[0];
  dropdown = bootstrap.Dropdown.getInstance(dropdown);
  dropdown.hide();

  const body = el.closest('.post-header').nextElementSibling;
  const post = body.children[0];

  let postText = post.innerText;
  const textarea = document.createElement('textarea');
  textarea.classList.add('form-control', 'my-2');
  textarea.value = postText;
  post.replaceWith(textarea);
  textarea.style.height = `${textarea.scrollHeight}px`;

  const save = document.createElement('button');
  save.classList.add('btn', 'btn-primary', 'mb-2');
  save.innerText = 'save';
  textarea.insertAdjacentElement('afterend', save);
  textarea.onclick = (event) => {
    event.stopPropagation();
  };
  save.onclick = (event) => {
    event.stopPropagation();
    postText = textarea.value;

    let postId = el.closest('.entity').dataset.id;

    fetch(`/edit_post/${postId}`, {
      method: 'PUT',
      body: JSON.stringify({
        new_post: postText,
      }),
    }).then((res) => {
      if (res.status === 204) {
        post.innerText = postText;
        textarea.replaceWith(post);
        save.remove();
        editing = false;
      }
    });
  };
};

const deletePost = (el, event) => {
  event.stopPropagation();

  let postId = el.closest('.entity').dataset.id;
  const animation = el.closest('.entity').dataset.animation;
  fetch(`/delete_post/${postId}`).then((response) => {
    if (
      response.status === 200 &&
      el.closest('.entity').dataset.animation === undefined
    )
      window.location.replace('/');
    else {
      let post = el.closest('.entity');
      post.remove();
    }
  });
};

const navPosts = document.querySelector('#profile-posts-link');
const navAbout = document.querySelector('#profile-about-link');
const navEdit = document.querySelector('#profile-edit-link');
const containerPosts = document.querySelector('#profile-posts-cotainer');
const containerAbout = document.querySelector('#profile-about-container');
const containerEdit = document.querySelector('#profile-edit-container');
document.querySelector('#profile-tabs').addEventListener('click', (event) => {
  event.preventDefault();
  target = event.target;
  if (target.tagName != 'A') {
    return;
  } else {
    if (target === navPosts) {
      if (navPosts.classList.contains('active')) return;
      navPosts.classList.add('active');
      navAbout.classList.remove('active');
      if (navEdit) navEdit.classList.remove('active');
      containerPosts.hidden = false;
      containerAbout.hidden = true;
      if (containerEdit) containerEdit.hidden = true;
    } else if (target === navAbout) {
      if (navAbout.classList.contains('active')) return;
      navAbout.classList.add('active');
      navPosts.classList.remove('active');
      if (navEdit) navEdit.classList.remove('active');
      containerPosts.hidden = true;
      containerAbout.hidden = false;
      if (containerEdit) containerEdit.hidden = true;
    } else if (target === navEdit) {
      navAbout.classList.remove('active');
      navPosts.classList.remove('active');
      navEdit.classList.add('active');
      containerPosts.hidden = true;
      containerAbout.hidden = true;
      containerEdit.hidden = false;
    }
  }
});

const cover = document.querySelector('#cover');
const color = document.querySelector('input[type="color"]');
color.addEventListener('input', (event, c) => {
  cover.style.backgroundColor = event.srcElement.value;
});
