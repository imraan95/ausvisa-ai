document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.nav-container') && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
            }
        });
    }

    // FAQ Accordion
    const faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach(question => {
        question.addEventListener('click', () => {
            const answer = question.nextElementSibling;
            const isOpen = answer.style.maxHeight;

            // Close all other answers
            document.querySelectorAll('.faq-answer').forEach(a => {
                if (a !== answer) {
                    a.style.maxHeight = null;
                    a.parentElement.classList.remove('active');
                }
            });

            // Toggle current answer
            if (isOpen) {
                answer.style.maxHeight = null;
                question.parentElement.classList.remove('active');
            } else {
                answer.style.maxHeight = answer.scrollHeight + 'px';
                question.parentElement.classList.add('active');
            }
        });
    });

    // Profile Form Submission
    const profileForm = document.getElementById('profile-form');
    const assessmentResult = document.getElementById('assessment-result');

    if (profileForm) {
        profileForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(profileForm);
            const data = Object.fromEntries(formData);
            
            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.error) {
                    throw new Error(result.error);
                }
                
                // Update success probability
                const probability = result.success_probability;
                const scoreFill = document.querySelector('.score-fill');
                const scorePercentage = document.querySelector('.score-percentage');
                
                scoreFill.style.width = `${probability * 100}%`;
                scorePercentage.textContent = `${Math.round(probability * 100)}%`;
                
                // Update recommendations
                const recommendationsList = document.querySelector('.recommendations-list');
                recommendationsList.innerHTML = result.recommendations.map(rec => `
                    <div class="recommendation-item">
                        <h4>${rec.visa_type}</h4>
                        <span class="confidence-badge ${rec.confidence.toLowerCase()}">${rec.confidence} Match</span>
                        <p>${rec.details}</p>
                    </div>
                `).join('');
                
                // Show results
                assessmentResult.style.display = 'block';
                assessmentResult.scrollIntoView({ behavior: 'smooth' });
                
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while processing your request. Please try again.');
            }
        });
    }

    // Form Handling
    const chatForm = document.getElementById('chatForm');
    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const userInput = document.getElementById('userInput');
            const message = userInput.value.trim();
            if (!message) return;

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message })
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                console.log('Response:', data);
                
                // Clear input
                userInput.value = '';
                
                // Add message to chat
                const chatMessages = document.getElementById('chatMessages');
                if (chatMessages) {
                    // Add user message
                    const userDiv = document.createElement('div');
                    userDiv.className = 'message user';
                    userDiv.innerHTML = `<p>${message}</p>`;
                    chatMessages.appendChild(userDiv);
                    
                    // Add AI response
                    const aiDiv = document.createElement('div');
                    aiDiv.className = 'message ai';
                    aiDiv.innerHTML = `<p>${data.response}</p>`;
                    chatMessages.appendChild(aiDiv);
                    
                    // Scroll to bottom
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Sorry, something went wrong. Please try again.');
            }
        });
    }
});
