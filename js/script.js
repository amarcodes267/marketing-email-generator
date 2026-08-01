(function() {
  'use strict';

  const REQUEST_TIMEOUT_MS = 300000;
  const NOTIFICATION_DURATION_MS = 4500;
  const SUBJECT_EMPTY_STATE = 'Waiting for generation...';
  const EMAIL_EMPTY_STATE = 'Your personalized email will appear here...';

  const API_BASE_URL = (function resolveApiBaseUrl() {
    const protocol = window.location.protocol;
    const host = window.location.hostname;
    if (host && host !== 'localhost' && host !== '127.0.0.1') {
      return `${protocol}//${host}:5000`;
    }
    return 'http://localhost:5000';
  })();

  const formFields = [
    document.getElementById('customerName'),
    document.getElementById('age'),
    document.getElementById('gender'),
    document.getElementById('location'),
    document.getElementById('purchaseHistory'),
    document.getElementById('favoriteCategory'),
    document.getElementById('totalSpending'),
    document.getElementById('emailTone')
  ];

  const generateBtn = document.getElementById('generateBtn');
  const copyBtn = document.getElementById('copyBtn');
  const clearBtn = document.getElementById('clearBtn');

  const subjectOutput = document.getElementById('subjectOutput');
  const emailOutput = document.getElementById('emailOutput');

  const spinnerOverlay = document.getElementById('spinnerOverlay');
  const outputCard = document.querySelector('.output-card');
  const notificationContainer = document.getElementById('notificationContainer');

  const fieldErrorMap = {
    customerName: document.getElementById('nameError'),
    age: document.getElementById('ageError'),
    gender: document.getElementById('genderError'),
    location: document.getElementById('locationError'),
    purchaseHistory: document.getElementById('purchaseError'),
    favoriteCategory: document.getElementById('categoryError'),
    totalSpending: document.getElementById('spendingError'),
    emailTone: document.getElementById('toneError')
  };

  let activeRequestController = null;
  let isSubmitting = false;

  function clearFieldErrors() {
    Object.keys(fieldErrorMap).forEach(function(fieldId) {
      const field = document.getElementById(fieldId);
      if (field) field.classList.remove('error');
      fieldErrorMap[fieldId].textContent = '';
    });
  }

  function markFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    if (field) field.classList.add('error');
    fieldErrorMap[fieldId].textContent = message;
  }

  function focusFirstInvalidField() {
    const firstInvalid = formFields.find(function(field) {
      return field.classList.contains('error');
    });
    if (firstInvalid) firstInvalid.focus();
  }

  function validateForm() {
    clearFieldErrors();
    let isValid = true;

    const nameValue = formFields[0].value.trim();
    if (!nameValue) {
      markFieldError('customerName', 'Customer name is required');
      isValid = false;
    }

    const ageValue = parseInt(formFields[1].value, 10);
    if (!formFields[1].value) {
      markFieldError('age', 'Age is required');
      isValid = false;
    } else if (isNaN(ageValue) || ageValue < 18 || ageValue > 100) {
      markFieldError('age', 'Age must be between 18 and 100');
      isValid = false;
    }

    if (!formFields[2].value) {
      markFieldError('gender', 'Please select a gender');
      isValid = false;
    }

    if (!formFields[3].value.trim()) {
      markFieldError('location', 'Location is required');
      isValid = false;
    }

    if (!formFields[4].value.trim()) {
      markFieldError('purchaseHistory', 'Purchase history is required');
      isValid = false;
    }

    if (!formFields[5].value) {
      markFieldError('favoriteCategory', 'Please select a category');
      isValid = false;
    }

    const spendingValue = parseFloat(formFields[6].value);
    if (!formFields[6].value) {
      markFieldError('totalSpending', 'Total spending is required');
      isValid = false;
    } else if (isNaN(spendingValue) || spendingValue <= 0) {
      markFieldError('totalSpending', 'Spending must be greater than 0');
      isValid = false;
    }

    if (!formFields[7].value) {
      markFieldError('emailTone', 'Please select an email tone');
      isValid = false;
    }

    if (!isValid) {
      focusFirstInvalidField();
      createNotification('warning', 'Please fix the highlighted fields before generating.', '⚠️');
    }

    return isValid;
  }

  function buildRequestPayload() {
    return {
      customer_name: formFields[0].value.trim(),
      age: parseInt(formFields[1].value, 10),
      gender: formFields[2].value,
      location: formFields[3].value.trim(),
      purchase_history: formFields[4].value.trim(),
      favorite_category: formFields[5].value,
      total_spending: parseFloat(formFields[6].value),
      tone: formFields[7].value
    };
  }

  function createNotification(type, message, icon) {
    const existing = notificationContainer.querySelectorAll('.notification');
    if (existing.length >= 4) {
      notificationContainer.removeChild(existing[0]);
    }

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.setAttribute('role', type === 'error' ? 'alert' : 'status');

    const iconElement = document.createElement('span');
    iconElement.className = 'notification-icon';
    iconElement.textContent = icon || (type === 'success' ? '✅' : type === 'error' ? '❌' : '⚠️');
    iconElement.setAttribute('aria-hidden', 'true');

    const contentElement = document.createElement('div');
    contentElement.className = 'notification-content';
    contentElement.textContent = message;

    const closeElement = document.createElement('button');
    closeElement.className = 'notification-close';
    closeElement.type = 'button';
    closeElement.setAttribute('aria-label', 'Dismiss notification');
    closeElement.textContent = '✕';

    notification.appendChild(iconElement);
    notification.appendChild(contentElement);
    notification.appendChild(closeElement);

    notificationContainer.appendChild(notification);

    let dismissTimer = null;

    function dismissNotification() {
      if (dismissTimer) {
        clearTimeout(dismissTimer);
        dismissTimer = null;
      }
      notification.classList.add('leaving');
      notification.addEventListener('animationend', function onAnimationEnd() {
        notification.removeEventListener('animationend', onAnimationEnd);
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      });
    }

    closeElement.addEventListener('click', dismissNotification);

    dismissTimer = setTimeout(dismissNotification, NOTIFICATION_DURATION_MS);

    return notification;
  }

  function setLoadingState(loading) {
    if (loading) {
      isSubmitting = true;
      spinnerOverlay.classList.add('active');
      outputCard.setAttribute('aria-busy', 'true');
      generateBtn.disabled = true;
      generateBtn.classList.add('btn-loading');
      copyBtn.disabled = true;
      formFields.forEach(function(field) {
        field.disabled = true;
      });
    } else {
      isSubmitting = false;
      spinnerOverlay.classList.remove('active');
      outputCard.removeAttribute('aria-busy');
      generateBtn.disabled = false;
      generateBtn.classList.remove('btn-loading');
      formFields.forEach(function(field) {
        field.disabled = false;
      });
    }
  }

  function setGeneratedOutput(subject, email) {
    subjectOutput.value = subject;
    emailOutput.value = email;
    subjectOutput.classList.add('filled');
    emailOutput.classList.add('filled');
    copyBtn.disabled = false;
  }

  function resetOutputState() {
    subjectOutput.value = '';
    emailOutput.value = '';
    subjectOutput.placeholder = SUBJECT_EMPTY_STATE;
    emailOutput.placeholder = EMAIL_EMPTY_STATE;
    subjectOutput.classList.remove('filled');
    emailOutput.classList.remove('filled');
    copyBtn.disabled = true;
  }

  function readResponsePayload(response, fallbackMessage) {
    return response.json().then(function(data) {
      if (data && typeof data === 'object') {
        return data;
      }
      return { success: false, message: fallbackMessage };
    }).catch(function() {
      return { success: false, message: fallbackMessage };
    });
  }

  async function submitGenerationRequest(payload) {
    const controller = new AbortController();
    activeRequestController = controller;

    const timeoutId = setTimeout(function() {
      controller.abort();
    }, REQUEST_TIMEOUT_MS);

    try {
      const response = await fetch(`${API_BASE_URL}/generate-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload),
        signal: controller.signal
      });

      const result = await readResponsePayload(response, 'The server returned an unreadable response. Please try again.');

      if (response.ok && result.success) {
        return { ok: true, data: result };
      }
      return { ok: false, data: result };
    } finally {
      clearTimeout(timeoutId);
      activeRequestController = null;
    }
  }

  async function handleGenerate() {
    if (isSubmitting) return;

    if (!validateForm()) return;

    const payload = buildRequestPayload();

    setLoadingState(true);
    resetOutputState();

    let outcome;

    try {
      outcome = await submitGenerationRequest(payload);
    } catch (error) {
      if (error && error.name === 'AbortError') {
        outcome = { ok: false, data: { success: false, message: 'The request timed out. The AI model may still be loading. Please try again.' } };
      } else {
        outcome = { ok: false, data: { success: false, message: 'Unable to reach the server. Please check your connection and try again.' } };
      }
    } finally {
      setLoadingState(false);
    }

    if (outcome.ok && outcome.data.subject && outcome.data.email) {
      setGeneratedOutput(outcome.data.subject, outcome.data.email);
      createNotification('success', 'Email generated successfully!', '✅');
    } else {
      resetOutputState();
      const errorMessage = (outcome.data && outcome.data.message) || 'Something went wrong. Please try again.';
      createNotification('error', errorMessage, '❌');
    }
  }

  async function handleCopy() {
    const emailContent = emailOutput.value;
    if (!emailContent || copyBtn.disabled) return;

    if (navigator.clipboard && navigator.clipboard.writeText) {
      try {
        await navigator.clipboard.writeText(emailContent);
        createNotification('success', 'Email copied successfully', '✅');
      } catch (error) {
        fallbackCopy(emailContent);
      }
    } else {
      fallbackCopy(emailContent);
    }
  }

  function fallbackCopy(text) {
    const tempTextarea = document.createElement('textarea');
    tempTextarea.value = text;
    tempTextarea.setAttribute('readonly', '');
    tempTextarea.style.position = 'fixed';
    tempTextarea.style.opacity = '0';
    tempTextarea.style.pointerEvents = 'none';
    document.body.appendChild(tempTextarea);
    tempTextarea.select();
    tempTextarea.setSelectionRange(0, text.length);
    try {
      document.execCommand('copy');
      createNotification('success', 'Email copied successfully', '✅');
    } catch (error) {
      createNotification('error', 'Failed to copy the email. Please try again.', '❌');
    }
    document.body.removeChild(tempTextarea);
  }

  function handleClear() {
    if (isSubmitting) return;

    formFields.forEach(function(field) {
      field.value = '';
    });

    clearFieldErrors();
    resetOutputState();
    setLoadingState(false);

    const notifications = notificationContainer.querySelectorAll('.notification');
    notifications.forEach(function(notification) {
      notification.classList.add('leaving');
      notification.addEventListener('animationend', function onAnimationEnd() {
        notification.removeEventListener('animationend', onAnimationEnd);
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      });
    });
  }

  generateBtn.addEventListener('click', handleGenerate);
  copyBtn.addEventListener('click', handleCopy);
  clearBtn.addEventListener('click', handleClear);

  resetOutputState();

})();

