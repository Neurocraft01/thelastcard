/**
 * NFC Card Platform - Main JavaScript
 * =============================================================================
 */

(function() {
    'use strict';

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        initLucideIcons();
        initAlerts();
        initModals();
        initDropdowns();
        initTabs();
        initFormValidation();
        initCopyToClipboard();
        initTooltips();
        initScrollAnimations();
        initNavbarScroll();
        initParallax();
        initCounterAnimation();
        initImageLazyLoad();
        initSmoothScroll();
        initCardTilt();
    });

    /**
     * Initialize Lucide Icons
     */
    function initLucideIcons() {
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    /**
     * Initialize Alert Dismissal
     */
    function initAlerts() {
        document.querySelectorAll('.alert').forEach(function(alert) {
            const closeBtn = alert.querySelector('.alert-close');
            if (closeBtn) {
                closeBtn.addEventListener('click', function() {
                    alert.style.opacity = '0';
                    setTimeout(function() {
                        alert.remove();
                    }, 300);
                });
            }

            // Auto-dismiss after 5 seconds
            setTimeout(function() {
                if (alert.parentElement) {
                    alert.style.opacity = '0';
                    setTimeout(function() {
                        alert.remove();
                    }, 300);
                }
            }, 5000);
        });
    }

    /**
     * Modal System
     */
    function initModals() {
        // Open modal triggers
        document.querySelectorAll('[data-modal-target]').forEach(function(trigger) {
            trigger.addEventListener('click', function(e) {
                e.preventDefault();
                const modalId = this.getAttribute('data-modal-target');
                openModal(modalId);
            });
        });

        // Close modal triggers
        document.querySelectorAll('[data-modal-close]').forEach(function(trigger) {
            trigger.addEventListener('click', function() {
                closeAllModals();
            });
        });

        // Close on backdrop click
        document.querySelectorAll('.modal-backdrop').forEach(function(backdrop) {
            backdrop.addEventListener('click', function(e) {
                if (e.target === this) {
                    closeAllModals();
                }
            });
        });

        // Close on ESC key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeAllModals();
            }
        });
    }

    function openModal(modalId) {
        const modal = document.getElementById(modalId);
        const backdrop = document.querySelector('.modal-backdrop');
        
        if (modal && backdrop) {
            backdrop.classList.add('active');
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }

    function closeAllModals() {
        document.querySelectorAll('.modal.active').forEach(function(modal) {
            modal.classList.remove('active');
        });
        document.querySelectorAll('.modal-backdrop.active').forEach(function(backdrop) {
            backdrop.classList.remove('active');
        });
        document.body.style.overflow = '';
    }

    // Export for global use
    window.openModal = openModal;
    window.closeAllModals = closeAllModals;

    /**
     * Dropdown System
     */
    function initDropdowns() {
        document.querySelectorAll('[data-dropdown-toggle]').forEach(function(trigger) {
            trigger.addEventListener('click', function(e) {
                e.stopPropagation();
                const dropdownId = this.getAttribute('data-dropdown-toggle');
                const dropdown = document.getElementById(dropdownId);
                
                if (dropdown) {
                    // Close other dropdowns
                    document.querySelectorAll('.dropdown-menu.show').forEach(function(d) {
                        if (d !== dropdown) d.classList.remove('show');
                    });
                    
                    dropdown.classList.toggle('show');
                }
            });
        });

        // Close dropdowns when clicking outside
        document.addEventListener('click', function() {
            document.querySelectorAll('.dropdown-menu.show').forEach(function(dropdown) {
                dropdown.classList.remove('show');
            });
        });
    }

    /**
     * Tab System
     */
    function initTabs() {
        document.querySelectorAll('[data-tab-target]').forEach(function(tab) {
            tab.addEventListener('click', function(e) {
                e.preventDefault();
                
                const tabGroup = this.closest('.tabs');
                const targetId = this.getAttribute('data-tab-target');
                const target = document.getElementById(targetId);
                
                if (tabGroup && target) {
                    // Deactivate all tabs
                    tabGroup.querySelectorAll('[data-tab-target]').forEach(function(t) {
                        t.classList.remove('active');
                    });
                    
                    // Deactivate all panels
                    const panels = target.parentElement.querySelectorAll('.tab-panel');
                    panels.forEach(function(panel) {
                        panel.classList.remove('active');
                    });
                    
                    // Activate clicked tab and panel
                    this.classList.add('active');
                    target.classList.add('active');
                }
            });
        });
    }

    /**
     * Form Validation
     */
    function initFormValidation() {
        document.querySelectorAll('form[novalidate]').forEach(function(form) {
            form.addEventListener('submit', function(e) {
                if (!validateForm(form)) {
                    e.preventDefault();
                }
            });

            // Real-time validation
            form.querySelectorAll('input, select, textarea').forEach(function(field) {
                field.addEventListener('blur', function() {
                    validateField(this);
                });

                field.addEventListener('input', function() {
                    if (this.classList.contains('error')) {
                        validateField(this);
                    }
                });
            });
        });
    }

    function validateForm(form) {
        let isValid = true;
        
        form.querySelectorAll('input[required], select[required], textarea[required]').forEach(function(field) {
            if (!validateField(field)) {
                isValid = false;
            }
        });
        
        return isValid;
    }

    function validateField(field) {
        const value = field.value.trim();
        const type = field.type;
        let isValid = true;
        let message = '';

        // Required check
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            message = 'This field is required';
        }

        // Email validation
        if (type === 'email' && value && !isValidEmail(value)) {
            isValid = false;
            message = 'Please enter a valid email address';
        }

        // Min length
        if (field.hasAttribute('minlength')) {
            const minLength = parseInt(field.getAttribute('minlength'));
            if (value.length < minLength) {
                isValid = false;
                message = `Must be at least ${minLength} characters`;
            }
        }

        // Update field state
        if (isValid) {
            field.classList.remove('error');
            removeFieldError(field);
        } else {
            field.classList.add('error');
            showFieldError(field, message);
        }

        return isValid;
    }

    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function showFieldError(field, message) {
        removeFieldError(field);
        
        const errorEl = document.createElement('p');
        errorEl.className = 'form-error';
        errorEl.textContent = message;
        
        field.parentElement.appendChild(errorEl);
    }

    function removeFieldError(field) {
        const existingError = field.parentElement.querySelector('.form-error');
        if (existingError) {
            existingError.remove();
        }
    }

    /**
     * Copy to Clipboard
     */
    function initCopyToClipboard() {
        document.querySelectorAll('[data-copy]').forEach(function(button) {
            button.addEventListener('click', function() {
                const text = this.getAttribute('data-copy');
                
                navigator.clipboard.writeText(text).then(function() {
                    // Show success feedback
                    const originalText = button.innerHTML;
                    button.innerHTML = '<i data-lucide="check" width="16" height="16"></i> Copied!';
                    lucide.createIcons();
                    
                    setTimeout(function() {
                        button.innerHTML = originalText;
                        lucide.createIcons();
                    }, 2000);
                }).catch(function(err) {
                    console.error('Failed to copy:', err);
                });
            });
        });
    }

    /**
     * Tooltips
     */
    function initTooltips() {
        document.querySelectorAll('[data-tooltip]').forEach(function(element) {
            element.addEventListener('mouseenter', function() {
                const text = this.getAttribute('data-tooltip');
                
                const tooltip = document.createElement('div');
                tooltip.className = 'tooltip';
                tooltip.textContent = text;
                
                document.body.appendChild(tooltip);
                
                const rect = this.getBoundingClientRect();
                tooltip.style.top = (rect.top - tooltip.offsetHeight - 8) + 'px';
                tooltip.style.left = (rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)) + 'px';
                tooltip.classList.add('show');
                
                this._tooltip = tooltip;
            });
            
            element.addEventListener('mouseleave', function() {
                if (this._tooltip) {
                    this._tooltip.remove();
                    this._tooltip = null;
                }
            });
        });
    }

    /**
     * Utility: Debounce
     */
    window.debounce = function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = function() {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    };

    /**
     * Utility: Format Number
     */
    window.formatNumber = function(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    };

    /**
     * Utility: Format Date
     */
    window.formatDate = function(date) {
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        return new Date(date).toLocaleDateString('en-US', options);
    };

    /**
     * Analytics Tracking
     */
    window.trackEvent = function(cardId, eventType, metadata = {}) {
        fetch('/api/analytics/track/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                card_id: cardId,
                event: eventType,
                metadata: metadata
            })
        }).catch(function(err) {
            console.error('Failed to track event:', err);
        });
    };

    /**
     * Scroll Reveal Animations
     */
    function initScrollAnimations() {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('scroll-reveal');
                    // Optionally unobserve after animation
                    // observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Observe elements with data-animate attribute
        document.querySelectorAll('[data-animate]').forEach(function(el) {
            observer.observe(el);
        });

        // Observe cards, features, etc.
        document.querySelectorAll('.card, .feature-card, .pricing-card, .stat-card').forEach(function(el) {
            observer.observe(el);
        });
    }

    /**
     * Navbar Scroll Effect
     */
    function initNavbarScroll() {
        const navbar = document.querySelector('.navbar');
        if (!navbar) return;

        let lastScroll = 0;

        window.addEventListener('scroll', debounce(function() {
            const currentScroll = window.pageYOffset;

            // Add scrolled class when scrolled down
            if (currentScroll > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }

            // Hide navbar on scroll down, show on scroll up
            if (currentScroll > lastScroll && currentScroll > 200) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }

            lastScroll = currentScroll;
        }, 100));
    }

    /**
     * Parallax Effect
     */
    function initParallax() {
        const parallaxElements = document.querySelectorAll('.parallax');
        
        if (parallaxElements.length === 0) return;

        window.addEventListener('scroll', debounce(function() {
            const scrolled = window.pageYOffset;

            parallaxElements.forEach(function(el) {
                const speed = el.getAttribute('data-speed') || 0.5;
                const yPos = -(scrolled * speed);
                el.style.transform = `translateY(${yPos}px)`;
            });
        }, 10));
    }

    /**
     * Counter Animation (for stats)
     */
    function initCounterAnimation() {
        const counters = document.querySelectorAll('[data-count]');
        
        counters.forEach(function(counter) {
            const target = parseInt(counter.getAttribute('data-count'));
            const duration = 2000; // 2 seconds
            const increment = target / (duration / 16); // 60fps
            let current = 0;

            const observerOptions = {
                root: null,
                rootMargin: '0px',
                threshold: 0.5
            };

            const observer = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting && current === 0) {
                        const updateCounter = function() {
                            current += increment;
                            if (current < target) {
                                counter.textContent = Math.floor(current);
                                requestAnimationFrame(updateCounter);
                            } else {
                                counter.textContent = target;
                            }
                        };
                        updateCounter();
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);

            observer.observe(counter);
        });
    }

    /**
     * Lazy Load Images
     */
    function initImageLazyLoad() {
        const images = document.querySelectorAll('img[data-src]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.add('fade-in');
                        imageObserver.unobserve(img);
                    }
                });
            });

            images.forEach(function(img) {
                imageObserver.observe(img);
            });
        } else {
            // Fallback for older browsers
            images.forEach(function(img) {
                img.src = img.dataset.src;
            });
        }
    }

    /**
     * Smooth Scroll for Anchor Links
     */
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                
                // Ignore # only links
                if (href === '#') return;

                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    /**
     * 3D Card Tilt Effect
     */
    function initCardTilt() {
        const tiltCards = document.querySelectorAll('.card-tilt');
        
        tiltCards.forEach(function(card) {
            card.addEventListener('mousemove', function(e) {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
            });
            
            card.addEventListener('mouseleave', function() {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
            });
        });
    }

    /**
     * Button Ripple Effect (on click)
     */
    document.addEventListener('click', function(e) {
        const button = e.target.closest('.btn');
        if (!button) return;

        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');

        button.appendChild(ripple);

        setTimeout(function() {
            ripple.remove();
        }, 600);
    });

    /**
     * Form Input Animation
     */
    document.querySelectorAll('.form-input, .form-textarea').forEach(function(input) {
        // Floating label effect
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });

        // Check if already has value on page load
        if (input.value) {
            input.parentElement.classList.add('focused');
        }
    });

    /**
     * Page Transition Effect
     */
    window.addEventListener('beforeunload', function() {
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.3s ease';
    });

})();
