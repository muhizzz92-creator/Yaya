document.addEventListener('DOMContentLoaded', () => {
    console.log("Yaya English Logic Loaded");
});

function checkAnswer(btn) {
    // Находим контейнер с кнопками
    const container = btn.closest('.options-grid') || btn.parentElement;
    
    // Если уже ответили, ничего не делаем
    if (container.classList.contains('answered')) return;
    
    // Помечаем, что ответ дан
    container.classList.add('answered');

    // Проверяем правильность
    const isCorrect = btn.getAttribute('data-correct') === 'true';

    if (isCorrect) {
        btn.classList.add('correct');
        btn.style.backgroundColor = '#4CAF50'; // Зеленый
        btn.style.color = 'white';
        btn.innerText += " ✅";
    } else {
        btn.classList.add('wrong');
        btn.style.backgroundColor = '#F44336'; // Красный
        btn.style.color = 'white';
        btn.innerText += " ❌";
        
        // Подсвечиваем правильный ответ
        const allBtns = container.querySelectorAll('button');
        allBtns.forEach(b => {
            if (b.getAttribute('data-correct') === 'true') {
                b.classList.add('correct');
                b.style.border = '2px solid #4CAF50';
            }
        });
    }
}