(function() {
  'use strict';

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

  const toneStyles = {
    'Professional': {
      greeting: 'Dear',
      signoff: 'Best regards',
      bodyPrefix: 'We are pleased to inform you about our latest offerings tailored to your preferences.'
    },
    'Friendly': {
      greeting: 'Hey',
      signoff: 'Cheers',
      bodyPrefix: 'We hope you are doing great! We have something special just for you.'
    },
    'Luxury': {
      greeting: 'Dear',
      signoff: 'Yours sincerely',
      bodyPrefix: 'It is our privilege to present you with an exclusive selection curated to your exquisite taste.'
    },
    'Exciting': {
      greeting: 'Hello',
      signoff: 'See you soon',
      bodyPrefix: 'Get ready! We have some amazing news that will make your day.'
    }
  };

  const categoryAdjectives = {
    'Fashion': 'stylish',
    'Electronics': 'cutting-edge',
    'Books': 'bestselling',
    'Sports': 'high-performance',
    'Home Decor': 'elegant',
    'Beauty': 'premium'
  };

  const storeNames = [
    'ShopVault',
    'TrendHub',
    'PrimeCart',
    'StyleBazaar',
    'EliteMall'
  ];

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

  function getFormData() {
    return {
      name: customerName.value.trim(),
      age: age.value,
      gender: gender.value,
      location: location.value.trim(),
      purchases: purchaseHistory.value.trim(),
      category: favoriteCategory.value,
      spending: totalSpending.value,
      tone: emailTone.value
    };
  }

  function generateSubject(data) {
    const greetings = [
      `Exclusive Offer Just for You, ${data.name}!`,
      `${data.name}, Your Personalized Deal Awaits!`,
      `Special Invitation for ${data.name}!`,
      `${data.name}, Discover Your Perfect Match!`,
      `Don't Miss Out, ${data.name}!`
    ];
    return greetings[Math.floor(Math.random() * greetings.length)];
  }

  function generateEmail(data) {
    const tone = toneStyles[data.tone] || toneStyles['Professional'];
    const adjective = categoryAdjectives[data.category] || 'amazing';
    const store = storeNames[Math.floor(Math.random() * storeNames.length)];
    const purchaseList = data.purchases.split('\n').filter(p => p.trim()).map(p => p.trim());
    const purchaseStr = purchaseList.length > 1
      ? purchaseList.slice(0, -1).join(', ') + ' and ' + purchaseList[purchaseList.length - 1]
      : purchaseList[0] || 'our products';

    const subject = generateSubject(data);

    let body = `${tone.greeting} ${data.name},\n\n`;
    body += `${tone.bodyPrefix}\n\n`;
    body += `As a valued customer from ${data.location}, we truly appreciate your continued trust in ${store}. `;
    body += `Your recent purchases of ${purchaseStr} show your great taste in ${data.category.toLowerCase()}!\n\n`;
    body += `Based on your interest in ${data.category}, we are excited to introduce our latest ${adjective} collection that we think you will love. `;
    body += `With a total spending of \u20B9${parseFloat(data.spending).toLocaleString('en-IN')}, you are among our most valued customers. `;
    body += `As a special thank you, we have curated a selection of premium ${data.category.toLowerCase()} items just for you.\n\n`;
    body += `Here is what we recommend for you:\n`;
    body += `- Explore our new ${adjective} arrivals in ${data.category}\n`;
    body += `- Enjoy exclusive discounts available only for our ${data.location} customers\n`;
    body += `- Get personalized recommendations based on your purchase history\n\n`;
    body += `Hurry, these offers are available for a limited time only!\n\n`;
    body += `${tone.signoff},\n`;
    body += `${store} Team`;

    return { subject, body };
  }

  function showToast(message) {
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 2500);
  }

  function handleGenerate() {
    if (!validateForm()) return;

    const data = getFormData();

    spinnerOverlay.classList.add('active');
    generateBtn.disabled = true;
    copyBtn.disabled = true;

    setTimeout(() => {
      const result = generateEmail(data);
      subjectOutput.value = result.subject;
      emailOutput.value = result.body;

      spinnerOverlay.classList.remove('active');
      generateBtn.disabled = false;
      copyBtn.disabled = false;
    }, 2000);
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
