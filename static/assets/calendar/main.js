document.addEventListener('DOMContentLoaded', (event) => {
    // Since the lessons variable is defined in the HTML template,
    // you need to ensure that this file is included after the variable declaration.
    const date = new Date();
    const firstDayOfMonth = new Date(date.getFullYear(), date.getMonth(), 1).getDay();
    const lastDateOfMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
    const daysList = document.getElementById('daysList');
    const monthHeader = document.getElementById('monthHeader');

    monthHeader.textContent = date.toLocaleDateString('en-us', {
        month: 'long',
        year: 'numeric'
    });

    for (let i = 0; i < firstDayOfMonth; i++) {
        const emptyLi = document.createElement('li');
        emptyLi.classList.add('outside');
        daysList.appendChild(emptyLi);
    }

    for (let i = 1; i <= lastDateOfMonth; i++) {
        const li = document.createElement('li');
        const divDate = document.createElement('div');
        divDate.classList.add('date');
        const span = document.createElement('span');
        span.textContent = i;
        divDate.appendChild(span);
        li.appendChild(divDate);
        daysList.appendChild(li);
    }

    function addLessonToDay(lesson) {
        const lessonDate = new Date(lesson.fields.date);
        const dayOfMonth = lessonDate.getDate();
        const li = daysList.children[dayOfMonth + firstDayOfMonth - 1]; // -1 because arrays are zero-indexed

        if (li) {
            const divEvent = document.createElement('div');
            divEvent.classList.add('event', 'bg-success');
            const spanEvent = document.createElement('span');
            spanEvent.textContent = lesson.fields.title;
            divEvent.appendChild(spanEvent);
            li.appendChild(divEvent);
        }
    }

    if (window.lessons) {
        window.lessons.forEach((lesson) => {
            addLessonToDay(lesson);
        });
    }
});
