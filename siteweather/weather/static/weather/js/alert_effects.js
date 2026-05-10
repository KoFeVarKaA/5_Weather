document.addEventListener('DOMContentLoaded', function() {
        const alerts = document.querySelectorAll('.alert-effect');
        
        alerts.forEach(function(alert) {
            // Устанавливаем таймер на 5 секунд
            setTimeout(function() {
                // Плавное исчезновение через прозрачность
                alert.style.transition = "opacity 0.5s ease";
                alert.style.opacity = "0";
                
                // Полное удаление из документа после завершения анимации
                setTimeout(() => alert.remove(), 500);
            }, 1000); 
        });
    });