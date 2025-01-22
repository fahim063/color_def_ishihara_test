function submitTest() {
    const form = document.getElementById('testForm');
    const formData = new FormData(form);
    const answers = {};

    // Collect all answers based on the radio groups
    formData.forEach((value, key) => {
        answers[key.replace('plate', '')] = value; // Map plate ID to the selected answer
    });

    console.log("Submitting answers:", answers); // Debugging log

    // Send answers to the backend
    fetch('/test', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ answers }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response from server:", data); // Debugging log

        // Replace the page content with the results
        document.body.innerHTML = `
            <div class="container">
                <h1>Test Results</h1>
                <p>Diagnosis: ${data.diagnosis}</p>
                <p>Test Result: ${data.test_result}</p>
                <table>
                    <thead>
                        <tr>
                            <th>Plate No.</th>
                            <th>User Answer</th>
                            <th>Correct Answer</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.results.map(result => `
                            <tr>
                                <td>${result.plate_id}</td>
                                <td>${result.user_answer}</td>
                                <td>${result.correct_answer}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
                <button onclick="window.location.href='/'">Restart</button>
            </div>
        `;
    })
    .catch(error => console.error('Error:", error'));
}

