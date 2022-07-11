document.querySelectorAll('.like-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    fetch(`/entity/${btn.dataset.like}/${btn.dataset.id}`).then((response) => {
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
    });
  });
});
