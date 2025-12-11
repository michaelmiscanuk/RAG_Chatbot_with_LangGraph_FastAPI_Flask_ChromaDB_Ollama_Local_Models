/**
 * Frontend JavaScript for Text Analysis App
 * Handles form submission, API calls, and dynamic UI updates
 */

// DOM Elements
const analyzeForm = document.getElementById('analyzeForm');
const textInput = document.getElementById('textInput');
const modelSelect = document.getElementById('modelSelect');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('results');
const loadingSection = document.getElementById('loading');
const errorAlert = document.getElementById('errorAlert');
const charCount = document.getElementById('charCount');
const wordCountDisplay = document.getElementById('wordCount');

// Character counter
if (textInput && charCount) {
    textInput.addEventListener('input', () => {
        const count = textInput.value.length;
        charCount.textContent = count;

        // Update color based on length
        if (count > 9000) {
            charCount.style.color = 'var(--error-color)';
        } else if (count > 7000) {
            charCount.style.color = 'var(--warning-color)';
        } else {
            charCount.style.color = 'var(--text-muted)';
        }
    });
}

// Load available models on page load
async function loadModels() {
    try {
        const response = await fetch('/api/models');
        if (response.ok) {
            const data = await response.json();
            if (data.models && modelSelect) {
                modelSelect.innerHTML = '';
                data.models.forEach(model => {
                    const option = document.createElement('option');
                    option.value = model;
                    option.textContent = model;
                    if (model === data.default) {
                        option.selected = true;
                    }
                    modelSelect.appendChild(option);
                });
            }
        }
    } catch (error) {
        console.warn('Could not load models:', error);
    }
}

// Show error message
function showError(message) {
    if (errorAlert) {
        const errorText = errorAlert.querySelector('.alert-text') || errorAlert;
        errorText.textContent = message;
        errorAlert.classList.remove('hidden');

        // Scroll to error
        errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });

        // Auto-hide after 10 seconds
        setTimeout(() => {
            errorAlert.classList.add('hidden');
        }, 10000);
    }
}

// Hide error message
function hideError() {
    if (errorAlert) {
        errorAlert.classList.add('hidden');
    }
}

// Show loading state
function showLoading() {
    if (loadingSection) loadingSection.classList.remove('hidden');
    if (resultsSection) resultsSection.classList.add('hidden');
    hideError();
    if (analyzeBtn) {
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<span class="spinner"></span> Analyzing...';
    }
}

// Hide loading state
function hideLoading() {
    if (loadingSection) loadingSection.classList.add('hidden');
    if (analyzeBtn) {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '✨ Analyze Text';
    }
}

// Display results
function displayResults(data) {
    if (!resultsSection) return;

    // Update statistics
    const wordCount = document.getElementById('resultWordCount');
    const charCountResult = document.getElementById('resultCharCount');
    const modelUsed = document.getElementById('resultModel');

    if (wordCount) wordCount.textContent = data.word_count || 0;
    if (charCountResult) charCountResult.textContent = data.character_count || 0;
    if (modelUsed) modelUsed.textContent = data.model_used || 'N/A';

    // Update summary
    const summaryText = document.getElementById('summaryText');
    if (summaryText) summaryText.textContent = data.summary || 'No summary generated';

    // Update sentiment
    const sentimentBadge = document.getElementById('sentimentBadge');
    if (sentimentBadge && data.sentiment) {
        const sentiment = data.sentiment.toLowerCase();
        sentimentBadge.textContent = sentiment.charAt(0).toUpperCase() + sentiment.slice(1);

        // Remove all sentiment classes
        sentimentBadge.className = 'sentiment-badge';

        // Add appropriate class
        sentimentBadge.classList.add(`sentiment-${sentiment}`);

        // Add emoji based on sentiment
        const emojis = {
            'positive': '😊',
            'negative': '😔',
            'neutral': '😐',
            'mixed': '🤔'
        };
        sentimentBadge.textContent = `${emojis[sentiment] || ''} ${sentimentBadge.textContent}`;
    }

    // Show results section with animation
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Handle form submission
if (analyzeForm) {
    analyzeForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const text = textInput.value.trim();
        const model = modelSelect ? modelSelect.value : 'qwen2.5-coder:0.5b';

        // Validation
        if (!text) {
            showError('Please enter some text to analyze');
            return;
        }

        if (text.length > 10000) {
            showError('Text is too long. Maximum 10,000 characters allowed.');
            return;
        }

        // Show loading
        showLoading();

        try {
            // Make API request
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    model_name: model
                })
            });

            const data = await response.json();

            if (response.ok && data.success !== false) {
                // Display results
                displayResults(data);
            } else {
                // Show error
                const errorMsg = data.error || data.detail || 'An error occurred during analysis';
                showError(errorMsg);
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Failed to connect to the server. Please check if the backend is running and try again.');
        } finally {
            hideLoading();
        }
    });
}

// Load models when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadModels);
} else {
    loadModels();
}

// Add sample texts functionality (if sample buttons exist)
document.querySelectorAll('.sample-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const sampleText = btn.getAttribute('data-sample');
        if (textInput && sampleText) {
            textInput.value = sampleText;
            // Trigger input event to update character count
            textInput.dispatchEvent(new Event('input'));
        }
    });
});
