// Animación para los elementos del equipo
const teamMembers = document.querySelectorAll('.team-member');

teamMembers.forEach((member, index) => {
    member.style.opacity = '0';
    member.style.transform = 'translateY(20px)';
    member.style.transition = `all 0.5s ease ${index * 0.1}s`;

    setTimeout(() => {
        member.style.opacity = '1';
        member.style.transform = 'translateY(0)';
    }, 500);
});

// Animación para la línea de tiempo
const timelineItems = document.querySelectorAll('.timeline-item');

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateX(0)';
        }
    });
}, { threshold: 0.1 });

timelineItems.forEach(item => {
    item.style.opacity = '0';
    item.style.transition = 'all 0.5s ease';

    if (item.classList.contains('left')) {
        item.style.transform = 'translateX(-50px)';
    } else {
        item.style.transform = 'translateX(50px)';
    }

    observer.observe(item);
});