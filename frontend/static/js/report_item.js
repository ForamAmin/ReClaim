 // ── PROGRESS TRACKING ──────────────────────────
  const fill  = document.getElementById('progress-fill');
  const prog1 = document.getElementById('prog-1');
  const prog2 = document.getElementById('prog-2');
  const prog3 = document.getElementById('prog-3');

  function updateProgress() {
    const title    = document.getElementById('title').value.trim();
    const desc     = document.getElementById('description').value.trim();
    const category = document.querySelector('input[name="category"]:checked');
    const location = document.getElementById('location_found').value.trim();
    const image    = document.getElementById('image-input').files.length > 0;

    const step1Done = title && desc && category && location;
    const step2Done = image;

    if (step2Done && step1Done) {
      fill.style.width = '100%';
      prog1.className = 'progress-label done';
      prog2.className = 'progress-label done';
      prog3.className = 'progress-label active';
    } else if (step1Done) {
      fill.style.width = '66%';
      prog1.className = 'progress-label done';
      prog2.className = 'progress-label active';
      prog3.className = 'progress-label';
    } else {
      fill.style.width = '33%';
      prog1.className = 'progress-label active';
      prog2.className = 'progress-label';
      prog3.className = 'progress-label';
    }
  }

  document.querySelectorAll('.form-input, .form-textarea, input[name="category"]')
    .forEach(el => el.addEventListener('input', updateProgress));
  document.querySelectorAll('input[name="category"]')
    .forEach(el => el.addEventListener('change', updateProgress));

  // ── IMAGE UPLOAD PREVIEW ───────────────────────
  const imageInput  = document.getElementById('image-input');
  const uploadZone  = document.getElementById('upload-zone');
  const uploadPreview = document.getElementById('upload-preview');
  const previewImg  = document.getElementById('preview-img');
  const removeBtn   = document.getElementById('remove-img');

  imageInput.addEventListener('change', function () {
    if (this.files && this.files[0]) {
      const reader = new FileReader();
      reader.onload = e => {
        previewImg.src = e.target.result;
        uploadZone.style.display = 'none';
        uploadPreview.style.display = 'block';
        updateProgress();
      };
      reader.readAsDataURL(this.files[0]);
    }
  });

  removeBtn.addEventListener('click', () => {
    imageInput.value = '';
    previewImg.src = '';
    uploadZone.style.display = 'block';
    uploadPreview.style.display = 'none';
    updateProgress();
  });

  // Drag and drop
  uploadZone.addEventListener('dragover', e => {
    e.preventDefault();
    uploadZone.classList.add('drag-over');
  });

  uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('drag-over'));

  uploadZone.addEventListener('drop', e => {
    e.preventDefault();
    uploadZone.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      imageInput.files = e.dataTransfer.files;
      const reader = new FileReader();
      reader.onload = ev => {
        previewImg.src = ev.target.result;
        uploadZone.style.display = 'none';
        uploadPreview.style.display = 'block';
        updateProgress();
      };
      reader.readAsDataURL(file);
    }
  });

  // ── SET TODAY AS DEFAULT DATE ──────────────────
  const dateInput = document.getElementById('date_found');
  dateInput.value = new Date().toISOString().split('T')[0];
