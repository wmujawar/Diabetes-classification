// Theme Management
class ThemeManager {
    constructor() {
        this.themeToggle = document.getElementById('themeToggle');
        this.themeIcon = document.getElementById('themeIcon');
        this.currentTheme = localStorage.getItem('theme') || 'light';
        
        this.init();
    }
    
    init() {
        this.setTheme(this.currentTheme);
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
        
        // Add smooth transition to theme toggle
        this.themeToggle.addEventListener('mouseenter', () => {
            this.themeToggle.style.transform = 'scale(1.1) rotate(10deg)';
        });
        
        this.themeToggle.addEventListener('mouseleave', () => {
            this.themeToggle.style.transform = 'scale(1) rotate(0deg)';
        });
    }
    
    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;
        localStorage.setItem('theme', theme);
        
        // Update icon with animation
        this.themeIcon.style.transform = 'rotate(360deg)';
        setTimeout(() => {
            this.themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            this.themeIcon.style.transform = 'rotate(0deg)';
        }, 150);
    }
    
    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
        
        // Add a glow effect when toggling in dark mode
        if (newTheme === 'dark') {
            this.addGlowEffect();
        }
    }
    
    addGlowEffect() {
        document.body.style.animation = 'none';
        document.body.offsetHeight; // Trigger reflow
        document.body.style.animation = 'darkModeGlow 0.5s ease-out';
        setTimeout(() => {
            document.body.style.animation = '';
        }, 500);
    }
}

// Form Management
class PredictionForm {
    constructor() {
        this.form = document.getElementById('predictionForm');
        this.predictBtn = document.getElementById('predictBtn');
        this.loader = document.getElementById('loader');
        this.resultContainer = document.getElementById('resultContainer');
        this.resultContent = document.getElementById('resultContent');
        
        this.init();
    }
    
    init() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.addInputAnimations();
        this.addFormValidation();
    }
    
    addInputAnimations() {
        const inputs = this.form.querySelectorAll('input');
        
        inputs.forEach(input => {
            // Add input validation styling
            input.addEventListener('input', () => {
                this.validateInput(input);
            });
        });
    }
    
    validateInput(input) {
        const value = parseFloat(input.value);
        const min = parseFloat(input.min);
        const max = parseFloat(input.max);
        
        if (value < min || value > max) {
            input.style.borderColor = 'var(--error-color)';
            input.style.boxShadow = '0 0 10px rgba(239, 68, 68, 0.3)';
        } else {
            input.style.borderColor = 'var(--success-color)';
            input.style.boxShadow = '0 0 10px rgba(16, 185, 129, 0.3)';
        }
    }
    
    addFormValidation() {
        const inputs = this.form.querySelectorAll('input');
        
        inputs.forEach(input => {
            input.addEventListener('invalid', (e) => {
                e.preventDefault();
                this.showValidationError(input);
            });
        });
    }
    
    showValidationError(input) {
        const formGroup = input.closest('.form-group');
        
        // Remove existing error message
        const existingError = formGroup.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Add error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = `Please enter a value between ${input.min} and ${input.max}`;
        errorDiv.style.color = 'var(--error-color)';
        errorDiv.style.fontSize = '0.875rem';
        errorDiv.style.marginTop = '5px';
        errorDiv.style.animation = 'slideInUp 0.3s ease';
        
        formGroup.appendChild(errorDiv);
        
        // Remove error after 3 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 3000);
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        if (!this.validateForm()) {
            return;
        }
        
        const formData = this.getFormData();
        
        try {
            this.showLoader();
            const result = await this.submitPrediction(formData);
            this.showResult(result);
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoader();
        }
    }
    
    validateForm() {
        const inputs = this.form.querySelectorAll('input');
        let isValid = true;
        
        inputs.forEach(input => {
            const value = parseFloat(input.value);
            const min = parseFloat(input.min);
            const max = parseFloat(input.max);
            
            if (isNaN(value) || value < min || value > max) {
                this.showValidationError(input);
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    getFormData() {
        const formData = new FormData(this.form);
        const data = {};
        
        // Convert form field names to match expected API format
        const fieldMapping = {
            'pregnancies': 'Pregnancies',
            'glucose': 'Glucose',
            'bloodPressure': 'BloodPressure',
            'skinThickness': 'SkinThickness',
            'insulin': 'Insulin',
            'bmi': 'BMI',
            'diabetesPedigree': 'DiabetesPedigreeFunction',
            'age': 'Age'
        };
        
        for (const [key, value] of formData.entries()) {
            const apiKey = fieldMapping[key] || key;
            data[apiKey] = parseFloat(value);
        }
        
        return data;
    }
    
    async submitPrediction(data) {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.text();
        return result;
    }
    
    showLoader() {
        this.predictBtn.disabled = true;
        this.predictBtn.innerHTML = `
            <i class="fas fa-spinner fa-spin"></i>
            <span>Processing...</span>
        `;
        this.loader.style.display = 'flex';
        this.resultContainer.style.display = 'none';
    }
    
    hideLoader() {
        this.predictBtn.disabled = false;
        this.predictBtn.innerHTML = `
            <i class="fas fa-brain"></i>
            <span>Predict Risk</span>
            <div class="button-glow"></div>
        `;
        this.loader.style.display = 'none';
    }
    
    showResult(result) {
        const prediction = parseInt(result);
        const isHighRisk = prediction === 1;
        
        this.resultContent.innerHTML = `
            <div class="prediction-result ${isHighRisk ? 'high-risk' : 'low-risk'}">
                <div class="result-icon">
                    <i class="fas ${isHighRisk ? 'fa-exclamation-triangle' : 'fa-check-circle'}"></i>
                </div>
                <div class="result-text">
                    <h4>${isHighRisk ? 'High Diabetes Risk' : 'Low Diabetes Risk'}</h4>
                    <p>
                        ${isHighRisk 
                            ? 'The model indicates a higher likelihood of diabetes. Please consult with a healthcare professional for proper evaluation.' 
                            : 'The model indicates a lower likelihood of diabetes. Continue maintaining a healthy lifestyle.'}
                    </p>
                </div>
            </div>
        `;
        
        this.resultContainer.style.display = 'block';
        
        // Add result-specific styling
        this.addResultStyling(isHighRisk);
        
        // Scroll to result
        this.resultContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    addResultStyling(isHighRisk) {
        const resultCard = this.resultContainer.querySelector('.result-card');
        const color = isHighRisk ? 'var(--error-color)' : 'var(--success-color)';
        
        resultCard.style.borderColor = color;
        
        if (document.documentElement.getAttribute('data-theme') === 'dark') {
            resultCard.style.boxShadow = `0 0 30px ${color}33, 0 0 60px ${color}22`;
        }
        
        // Add pulsing animation
        const resultElement = this.resultContainer.querySelector('.prediction-result');
        resultElement.style.animation = 'resultPulse 0.5s ease-out';
    }
    
    showError(message) {
        this.resultContent.innerHTML = `
            <div class="prediction-result error">
                <div class="result-icon">
                    <i class="fas fa-times-circle"></i>
                </div>
                <div class="result-text">
                    <h4>Prediction Error</h4>
                    <p>Unable to process your request: ${message}</p>
                </div>
            </div>
        `;
        
        this.resultContainer.style.display = 'block';
        this.resultContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Enhanced UI Effects
class UIEffects {
    constructor() {
        this.init();
    }
    
    init() {
        this.addParallaxEffect();
        this.addSmoothScrolling();
        this.addCustomAnimations();
        this.addInteractiveElements();
    }
    
    addParallaxEffect() {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const parallax = document.querySelector('.form-container');
            if (parallax) {
                const speed = scrolled * 0.1;
                parallax.style.transform = `translateY(${speed}px)`;
            }
        });
    }
    
    addSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    }
    
    addCustomAnimations() {
        // Add CSS animations dynamically
        const style = document.createElement('style');
        style.textContent = `
            @keyframes darkModeGlow {
                0% { box-shadow: inset 0 0 0 0 rgba(96, 165, 250, 0); }
                50% { box-shadow: inset 0 0 50px 10px rgba(96, 165, 250, 0.1); }
                100% { box-shadow: inset 0 0 0 0 rgba(96, 165, 250, 0); }
            }
            
            @keyframes resultPulse {
                0% { transform: scale(0.95); opacity: 0; }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); opacity: 1; }
            }
            
            .prediction-result {
                display: flex;
                align-items: center;
                gap: 20px;
                padding: 20px;
                border-radius: 12px;
                background: var(--bg-secondary);
            }
            
            .result-icon {
                font-size: 2rem;
                width: 60px;
                height: 60px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                background: var(--bg-primary);
            }
            
            .high-risk .result-icon {
                color: var(--error-color);
                background: rgba(239, 68, 68, 0.1);
            }
            
            .low-risk .result-icon {
                color: var(--success-color);
                background: rgba(16, 185, 129, 0.1);
            }
            
            .error .result-icon {
                color: var(--error-color);
                background: rgba(239, 68, 68, 0.1);
            }
            
            .result-text h4 {
                margin-bottom: 8px;
                font-size: 1.2rem;
            }
            
            .result-text p {
                color: var(--text-secondary);
                line-height: 1.6;
            }
        `;
        document.head.appendChild(style);
    }
    
    addInteractiveElements() {
        // Add hover effects to form groups
        const formGroups = document.querySelectorAll('.form-group');
        
        formGroups.forEach(group => {
            group.addEventListener('mouseenter', () => {
                if (document.documentElement.getAttribute('data-theme') === 'dark') {
                    group.style.filter = 'brightness(1.1)';
                }
            });
            
            group.addEventListener('mouseleave', () => {
                group.style.filter = 'brightness(1)';
            });
        });
        
        // Add click ripple effect to button
        const button = document.querySelector('.predict-btn');
        button.addEventListener('click', this.addRippleEffect);
    }
    
    addRippleEffect(e) {
        const button = e.currentTarget;
        const rect = button.getBoundingClientRect();
        const ripple = document.createElement('span');
        
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
        `;
        
        button.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ThemeManager();
    new PredictionForm();
    new UIEffects();
    
    // Add loading animation for form elements
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach((group, index) => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        setTimeout(() => {
            group.style.transition = 'all 0.5s ease';
            group.style.opacity = '1';
            group.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Add ripple animation to CSS
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);
});

// Add service worker for PWA capabilities (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then((registration) => {
                console.log('SW registered: ', registration);
            })
            .catch((registrationError) => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}
