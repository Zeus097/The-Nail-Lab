/*!
 * Flatpickr v4.6.9
 * Copyright (c) 2025 Samuel Sharp
 * Licensed under the MIT License (https://opensource.org/licenses/MIT)
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */



flatpickr("#date", {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
    minDate: "today",
    minuteIncrement: 30,
    disable: [
        function(date) {
            return date.getDay() === 0 || date.getDay() === 6; // Disable weekends
        }
    ],
    time_24hr: true,
    onReady: function(selectedDates, dateStr, instance) {
        instance.config.onChange.push(function(selectedDates, dateStr, instance) {
            const time = selectedDates[0].getHours();
            if (time < 10 || time >= 18) {
                alert("Изберете час между 10:00 и 18:00!");
                instance.clear();
            }
        });
    }
});

const form = document.getElementById("appointment-form");
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    try {
        const response = await fetch("http://127.0.0.1:5000/", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            alert("Часът е записан успешно!");
            form.reset();
        } else {
            const errorMessage = await response.text();
            alert(`Възникна грешка: ${errorMessage}`);
        }
    } catch (error) {
        alert(`Възникна грешка: ${error.message}`);
    }
});
