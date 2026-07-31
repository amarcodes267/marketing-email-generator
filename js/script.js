(function() {
  'use strict';

  const API_BASE_URL = 'http://localhost:5000';

  const customerName = document.getElementById('customerName');
  const age = document.getElementById('age');
  const gender = document.getElementById('gender');
  const location = document.getElementById('location');
  const purchaseHistory = document.getElementById('purchaseHistory');
  const favoriteCategory = document.getElementById('favoriteCategory');
  const totalSpending = document.getElementById('totalSpending');
  const emailTone = document.getElementById('emailTone');

  const generateBtn = document.getElementById('generateBtn');
  const copyBtn = document.getElementById('copyBtn');
  const clearBtn = document.getElementById('clearBtn');

  const subjectOutput = document.getElementById('subjectOutput');
  const emailOutput = document.getElementById('emailOutput');

  const spinnerOverlay = document.getElementById('spinnerOverlay');
  const toast = document.getElementById('toast');

  const errorElements = {
    customerName: document.getElementById('nameError'),
    age: document.getElementById('ageError'),
    gender: document.getElementById('genderError'),
    location: document.getElementById('locationError'),
    purchaseHistory: document.getElementById('purchaseError'),
    favoriteCategory: document.getElementById('categoryError'),
    totalSpending: document.getElementById('spendingError'),
    emailTone: document.getElementById('toneError')
  };

  function clearErrors() {
    Object.values(errorElements).forEach(el => el.textContent = '');
    document.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
  }

  function showError(inputId, message) {
    const input = document.getElementById(inputId);
    if (input) input.classList.add('error');
    if (errorElements[inputId]) errorElements[inputId].textContent = message;
  }

  function validateForm() {
    clearErrors();
    let isValid = true;

    if (!customerName.value.trim()) {
      showError('customerName', 'Customer name is required');
      isValid = false;
    }

    const ageValue = parseInt(age.value, 10);
    if (!age.value) {
      showError('age', 'Age is required');
      isValid = false;
    } else if (isNaN(ageValue) || ageValue < 18 || ageValue > 100) {
      showError('age', 'Age must be between 18 and 100');
      isValid = false;
    }

    if (!gender.value) {
      showError('gender', 'Please select a gender');
      isValid = false;
    }

    if (!location.value.trim()) {
      showError('location', 'Location is required');
      isValid = false;
    }

    if (!purchaseHistory.value.trim()) {
      showError('purchaseHistory', 'Purchase history is required');
      isValid = false;
    }

    if (!favoriteCategory.value) {
      showError('favoriteCategory', 'Please select a category');
      isValid = false;
    }

    const spendingValue = parseFloat(totalSpending.value);
    if (!totalSpending.value) {
      showError('totalSpending', 'Total spending is required');
      isValid = false;
    } else if (isNaN(spendingValue) || spendingValue <= 0) {
      showError('totalSpending', 'Spending must be greater than 0');
      isValid = false;
    }

    if (!emailTone.value) {
      showError('emailTone', 'Please select an email tone');
      isValid = false;
    }

    return isValid;
  }

  function buildPayload() {
    return {
      customer_name: customerName.value.trim(),
      age: parseInt(age.value, 10),
      gender: gender.value,
      location: location.value.trim(),
      purchase_history: purchaseHistory.value.trim(),
      favorite_category: favoriteCategory.value,
      total_spending: parseFloat(totalSpending.value),
      tone: emailTone.value
    };
  }

  function showToast(message) {
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 2500);
  }

  function setLoading(loading) {
    if (loading) {
      spinnerOverlay.classList.add('active');
      generateBtn.disabled = true;
      copyBtn.disabled = true;
    } else {
      spinnerOverlay.classList.remove('active');
      generateBtn.disabled = false;
    }
  }

  async function handleGenerate() {
    if (!validateForm()) return;

    const payload = buildPayload();

    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/generate-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      const result = await response.json();

      if (response.ok && result.success) {
        subjectOutput.value = result.subject;
        emailOutput.value = result.email;
        copyBtn.disabled = false;
      } else {
        subjectOutput.value = 'Subject will appear here...';
        emailOutput.value = 'Your AI generated email will appear here...';
        copyBtn.disabled = true;
        showToast(result.message || 'An error occurred');
      }
    } catch (error) {
      subjectOutput.value = 'Subject will appear here...';
      emailOutput.value = 'Your AI generated email will appear here...';
      copyBtn.disabled = true;
      showToast('Unable to connect to the server. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  }

  function handleCopy() {
    const emailContent = emailOutput.value;
    if (!emailContent || emailContent === 'Your AI generated email will appear here...') return;

    const fullText = `Subject: ${subjectOutput.value}\n\n${emailContent}`;

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(fullText).then(() => {
        showToast('Email copied successfully!');
      }).catch(() => {
        fallbackCopy(fullText);
      });
    } else {
      fallbackCopy(fullText);
    }
  }

  function fallbackCopy(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand('copy');
      showToast('Email copied successfully!');
    } catch (e) {
      showToast('Failed to copy email');
    }
    document.body.removeChild(textarea);
  }

  function handleClear() {
    customerName.value = '';
    age.value = '';
    gender.value = '';
    location.value = '';
    purchaseHistory.value = '';
    favoriteCategory.value = '';
    totalSpending.value = '';
    emailTone.value = '';

    subjectOutput.value = 'Subject will appear here...';
    emailOutput.value = 'Your AI generated email will appear here...';

    clearErrors();
    copyBtn.disabled = true;
    spinnerOverlay.classList.remove('active');
    generateBtn.disabled = false;
  }

  generateBtn.addEventListener('click', handleGenerate);
  copyBtn.addEventListener('click', handleCopy);
  clearBtn.addEventListener('click', handleClear);

})();
