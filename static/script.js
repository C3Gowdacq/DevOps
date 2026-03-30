document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const text = document.getElementById('textInput').value;
    const loading = document.getElementById('loading');
    const resultSection = document.getElementById('resultSection');

    if (!text.trim()) {
        alert("Please enter some text.");
        return;
    }

    loading.classList.remove('hidden');
    resultSection.classList.add('hidden');

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }),
        });

        if (!response.ok) {
            throw new Error('Analysis failed');
        }

        const data = await response.ok ? await response.json() : null;
        
        displayResults(data);
    } catch (error) {
        console.error(error);
        alert("An error occurred during analysis.");
    } finally {
        loading.classList.add('hidden');
    }
});

function displayResults(data) {
    const resultSection = document.getElementById('resultSection');
    const sentimentResult = document.getElementById('sentimentResult');
    const spamResult = document.getElementById('spamResult');
    const keywordsResult = document.getElementById('keywordsResult');

    sentimentResult.textContent = data.sentiment;
    spamResult.textContent = data.spam;

    // Clear previous keywords
    keywordsResult.innerHTML = '';
    if (data.keywords && data.keywords.length > 0) {
        data.keywords.forEach(kw => {
            const span = document.createElement('span');
            span.className = 'keyword-tag';
            span.textContent = kw;
            keywordsResult.appendChild(span);
        });
    } else {
        keywordsResult.textContent = 'None detected';
    }

    resultSection.classList.remove('hidden');
}
