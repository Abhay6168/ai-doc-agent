// AI Document Agent - Enhanced JavaScript with Dark Theme Support

// Global variables
let currentResults = null;
let uploadedFile = null;

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize application
function initializeApp() {
    setupFileUpload();
    setupFormSubmission();
    setupAnimations();
    setupScrollEffects();
}

// File Upload Setup
function setupFileUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const removeBtn = document.getElementById('removeFile');

    if (!uploadArea || !fileInput) return;

    // Click to upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Remove file button
    if (removeBtn) {
        removeBtn.addEventListener('click', removeFile);
    }
}

// Drag and drop handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        processFile(file);
    }
}

// Process selected file
function processFile(file) {
    if (!validateFile(file)) return;
    
    uploadedFile = file;
    showFileInfo(file);
    animateUploadSuccess();
}

// Show file information
function showFileInfo(file) {
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const fileIcon = document.getElementById('fileIcon');

    if (fileName) fileName.textContent = file.name;
    if (fileSize) fileSize.textContent = formatFileSize(file.size);
    
    // Set appropriate icon based on file type
    if (fileIcon) {
        const extension = file.name.split('.').pop().toLowerCase();
        const iconClass = getFileIcon(extension);
        fileIcon.className = `fas ${iconClass}`;
    }

    if (fileInfo) {
        fileInfo.classList.remove('d-none');
        fileInfo.style.animation = 'fadeInUp 0.5s ease-out';
    }
}

// Remove file
function removeFile() {
    uploadedFile = null;
    const fileInfo = document.getElementById('fileInfo');
    const fileInput = document.getElementById('fileInput');
    
    if (fileInfo) {
        fileInfo.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => {
            fileInfo.classList.add('d-none');
        }, 300);
    }
    
    if (fileInput) fileInput.value = '';
}

// Get file icon based on extension
function getFileIcon(extension) {
    const iconMap = {
        'pdf': 'fa-file-pdf',
        'docx': 'fa-file-word',
        'doc': 'fa-file-word',
        'txt': 'fa-file-alt',
        'md': 'fa-file-code'
    };
    return iconMap[extension] || 'fa-file';
}

// Validate file
function validateFile(file) {
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['pdf', 'docx', 'doc', 'txt', 'md'];
    const extension = file.name.split('.').pop().toLowerCase();
    
    if (file.size > maxSize) {
        showNotification('File is too large. Maximum size is 16MB.', 'error');
        return false;
    }
    
    if (!allowedTypes.includes(extension)) {
        showNotification(`File type not supported. Allowed: ${allowedTypes.join(', ')}`, 'error');
        return false;
    }
    
    return true;
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Form submission setup
function setupFormSubmission() {
    const form = document.getElementById('uploadForm');
    if (!form) return;

    form.addEventListener('submit', handleFormSubmit);
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    if (!uploadedFile) {
        showNotification('Please select a file first.', 'warning');
        return;
    }

    const formData = new FormData();
    formData.append('file', uploadedFile);
    
    // Get form options
    const generateSummary = document.getElementById('generateSummary')?.checked || false;
    const generateQuiz = document.getElementById('generateQuiz')?.checked || false;
    const summaryType = document.getElementById('summaryType')?.value || 'comprehensive';
    const numQuestions = document.getElementById('numQuestions')?.value || '10';
    const difficulty = document.getElementById('difficulty')?.value || 'medium';

    formData.append('generate_summary', generateSummary);
    formData.append('generate_quiz', generateQuiz);
    formData.append('summary_type', summaryType);
    formData.append('num_questions', numQuestions);
    formData.append('difficulty', difficulty);

    try {
        await submitForm(formData);
    } catch (error) {
        console.error('Form submission error:', error);
        showNotification('An error occurred while processing your request.', 'error');
        hideProgress();
    }
}

// Submit form with progress tracking
async function submitForm(formData) {
    showProgress();
    updateProgress(0, 'Uploading file...');

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Simulate progress updates
        updateProgress(25, 'Extracting text from document...');
        await sleep(1000);
        
        updateProgress(50, 'Analyzing content with AI...');
        await sleep(1500);
        
        updateProgress(75, 'Generating results...');
        await sleep(1000);

        const result = await response.json();
        
        updateProgress(100, 'Complete!');
        await sleep(500);

        hideProgress();
        displayResults(result);
        
    } catch (error) {
        hideProgress();
        throw error;
    }
}

// Progress bar functions
function showProgress() {
    const progressContainer = document.getElementById('progressContainer');
    const submitBtn = document.getElementById('submitBtn');
    
    if (progressContainer) {
        progressContainer.classList.remove('d-none');
        progressContainer.style.animation = 'fadeInUp 0.5s ease-out';
    }
    
    if (submitBtn) {
        submitBtn.disabled = true;
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoader = submitBtn.querySelector('.btn-loader');
        
        if (btnText) btnText.classList.add('d-none');
        if (btnLoader) btnLoader.classList.remove('d-none');
    }
}

function updateProgress(percent, text) {
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const progressPercent = document.getElementById('progressPercent');
    
    if (progressBar) {
        progressBar.style.width = `${percent}%`;
    }
    
    if (progressText) {
        progressText.textContent = text;
    }
    
    if (progressPercent) {
        progressPercent.textContent = `${percent}%`;
    }
}

function hideProgress() {
    const progressContainer = document.getElementById('progressContainer');
    const submitBtn = document.getElementById('submitBtn');
    
    if (progressContainer) {
        progressContainer.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => {
            progressContainer.classList.add('d-none');
        }, 300);
    }
    
    if (submitBtn) {
        submitBtn.disabled = false;
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoader = submitBtn.querySelector('.btn-loader');
        
        if (btnLoader) btnLoader.classList.add('d-none');
        if (btnText) btnText.classList.remove('d-none');
    }
}

// Display results
function displayResults(data) {
    currentResults = data;
    
    const resultsSection = document.getElementById('resultsSection');
    
    // Show results section
    if (resultsSection) {
        resultsSection.classList.remove('d-none');
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Handle errors
    if (data.errors && data.errors.length > 0) {
        showNotification(data.errors.join('<br>'), 'error');
    }
    
    // Display summary results
    if (data.summary_data) {
        displaySummaryResults(data.summary_data);
        document.getElementById('summaryResults').style.display = 'block';
    } else {
        document.getElementById('summaryResults').style.display = 'none';
    }
    
    // Display quiz results  
    if (data.quiz_data) {
        displayQuizResults(data.quiz_data);
        document.getElementById('quizResults').style.display = 'block';
    } else {
        document.getElementById('quizResults').style.display = 'none';
    }
    
    if (data.success) {
        showNotification('Document processed successfully!', 'success');
    } else {
        showNotification(data.error || 'Processing failed', 'error');
    }
}

// Display summary results
function displaySummaryResults(summaryData) {
    const summaryContent = document.getElementById('summaryContent');
    const summaryWords = document.getElementById('summaryWords');
    const compressionRatio = document.getElementById('compressionRatio');
    const keyPointsCount = document.getElementById('keyPointsCount');
    
    if (summaryContent && summaryData.summary) {
        summaryContent.innerHTML = summaryData.summary.replace(/\n/g, '<br>');
    }
    
    if (summaryWords) summaryWords.textContent = summaryData.word_count || '0';
    if (compressionRatio) compressionRatio.textContent = `${(summaryData.compression_ratio * 100).toFixed(1)}%`;
    if (keyPointsCount) keyPointsCount.textContent = summaryData.key_points ? summaryData.key_points.length : '0';
}

// Display quiz results
function displayQuizResults(quizData) {
    const quizPreview = document.getElementById('quizPreview');
    const quizQuestionsCount = document.getElementById('quizQuestionsCount');
    const quizDifficulty = document.getElementById('quizDifficulty');
    const estimatedTime = document.getElementById('estimatedTime');
    
    if (quizPreview && quizData.questions) {
        quizPreview.innerHTML = '';
        quizData.questions.slice(0, 3).forEach((q, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'quiz-question mb-3';
            questionDiv.innerHTML = `
                <h6>Q${index + 1}: ${q.question}</h6>
                ${q.type === 'multiple_choice' && q.options ? 
                    Object.entries(q.options).map(([key, value]) => 
                        `<div class="ms-3">○ ${key}: ${value}</div>`
                    ).join('') : 
                    q.type === 'true_false' ? 
                        '<div class="ms-3">○ True / False</div>' : 
                        '<div class="ms-3"><em>Short answer question</em></div>'
                }
            `;
            quizPreview.appendChild(questionDiv);
        });
        
        if (quizData.questions.length > 3) {
            const moreDiv = document.createElement('div');
            moreDiv.className = 'text-muted text-center mt-3';
            moreDiv.innerHTML = `<em>... and ${quizData.questions.length - 3} more questions</em>`;
            quizPreview.appendChild(moreDiv);
        }
    }
    
    if (quizData.quiz_metadata) {
        const metadata = quizData.quiz_metadata;
        if (quizQuestionsCount) quizQuestionsCount.textContent = metadata.num_questions || '0';
        if (quizDifficulty) quizDifficulty.textContent = metadata.difficulty || 'medium';
        if (estimatedTime) estimatedTime.textContent = metadata.estimated_time || '0 min';
    }
}

// Format summary text
function formatSummaryText(summary) {
    if (typeof summary === 'string') {
        return `<p>${summary.replace(/\n/g, '</p><p>')}</p>`;
    }
    return '<p>Summary not available</p>';
}

// Format quiz questions
function formatQuizQuestions(questions) {
    if (!Array.isArray(questions)) return '<p>No questions available</p>';
    
    return questions.slice(0, 3).map((q, index) => `
        <div class="quiz-question">
            <h6>Question ${index + 1}</h6>
            <p>${q.question}</p>
            ${q.options ? `
                <ul class="quiz-options">
                    ${q.options.map(opt => `<li>${opt}</li>`).join('')}
                </ul>
            ` : ''}
        </div>
    `).join('');
}

// Download functions
function downloadSummary() {
    if (!currentResults?.summary) {
        showNotification('No summary available to download.', 'warning');
        return;
    }
    
    const data = {
        summary: currentResults.summary,
        stats: currentResults.summary_stats,
        generated_at: new Date().toISOString()
    };
    
    downloadJSON(data, `summary_${Date.now()}.json`);
    showNotification('Summary downloaded successfully!', 'success');
}

function downloadQuiz() {
    if (!currentResults?.quiz) {
        showNotification('No quiz available to download.', 'warning');
        return;
    }
    
    const data = {
        quiz: currentResults.quiz,
        info: currentResults.quiz_info,
        generated_at: new Date().toISOString()
    };
    
    downloadJSON(data, `quiz_${Date.now()}.json`);
    showNotification('Quiz downloaded successfully!', 'success');
}

// Download JSON helper
function downloadJSON(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Animations and effects
function setupAnimations() {
    // Animate upload success
    window.animateUploadSuccess = function() {
        const uploadIcon = document.querySelector('.upload-icon');
        if (uploadIcon) {
            uploadIcon.style.animation = 'pulse 0.6s ease-out';
            setTimeout(() => {
                uploadIcon.style.animation = '';
            }, 600);
        }
    };
}

// Scroll effects
function setupScrollEffects() {
    const nav = document.querySelector('.glass-nav');
    if (!nav) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };
    
    notification.innerHTML = `
        <div class="notification-content">
            <i class="${icons[type] || icons.info}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add notification styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 350px;
        background: var(--bg-card);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: var(--radius-lg);
        padding: 1rem;
        backdrop-filter: blur(20px);
        animation: slideInRight 0.3s ease-out;
        box-shadow: var(--shadow-md);
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// Utility functions
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Functions for template compatibility
function downloadSummary() {
    if (currentResults && currentResults.summary_data) {
        const dataStr = JSON.stringify(currentResults.summary_data, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `summary_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
        link.click();
        URL.revokeObjectURL(url);
    }
}

function downloadQuiz() {
    if (currentResults && currentResults.quiz_data) {
        const dataStr = JSON.stringify(currentResults.quiz_data, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `quiz_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
        link.click();
        URL.revokeObjectURL(url);
    }
}

function clearResults() {
    currentResults = null;
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection) {
        resultsSection.classList.add('d-none');
    }
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Text copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy to clipboard.', 'error');
    });
}

// Export functions for global access
window.downloadSummary = downloadSummary;
window.downloadQuiz = downloadQuiz;
window.copySummary = function() {
    if (currentResults?.summary) {
        copyToClipboard(currentResults.summary);
    }
};

window.startQuiz = function() {
    showNotification('Interactive quiz mode coming soon!', 'info');
};