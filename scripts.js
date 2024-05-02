document.getElementById('analyzeButton').addEventListener('click', function() {
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('image', file);

    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        var resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `
            <p>Color: ${data.color}</p>
            <p>Shape: ${data.shape}</p>
            <p>Size (mm): ${data.size_mm}</p>
            <p>Purity: ${data.purity}</p>
            <p>Health: ${data.health}</p>
            <p>Germination Rate (%): ${data.germination_rate}</p>
            <p>Name: ${data.object_name}</p>
        `;
    })
    .catch(error => {
        console.error('Error:', error);
        var resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `<p>Error: Failed to analyze the image.</p>`;
    });
});
