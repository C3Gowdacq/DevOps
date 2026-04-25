document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const textInput = document.getElementById('textInput');
    const text = textInput.value;
    const loading = document.getElementById('loading');
    const resultSection = document.getElementById('resultSection');

    if (!text.trim()) {
        alert("Enter some intelligence text first.");
        return;
    }

    // UI Feedback
    loading.classList.remove('hidden');
    resultSection.classList.add('hidden');
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text }),
        });

        if (!response.ok) throw new Error('Neural analysis failed');

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error(error);
        alert("Connection to Neural Engine lost.");
    } finally {
        loading.classList.add('hidden');
    }
});

function displayResults(data) {
    const resultSection = document.getElementById('resultSection');
    const sentimentResult = document.getElementById('sentimentResult');
    const spamResult = document.getElementById('spamResult');
    const keywordsResult = document.getElementById('keywordsResult');
    const versionInfo = document.getElementById('versionInfo');

    const sentimentCard = document.getElementById('sentimentCard');
    const spamCard = document.getElementById('spamCard');

    // Update Text
    sentimentResult.textContent = data.sentiment;
    spamResult.textContent = data.spam;
    versionInfo.textContent = data.version || "V2.0-HYBRID";

    // Update Visual States (Coloring)
    sentimentCard.setAttribute('data-sentiment', data.sentiment.toLowerCase());
    spamCard.setAttribute('data-spam', data.spam.toLowerCase());

    // Populate Keywords
    keywordsResult.innerHTML = '';
    if (data.keywords && data.keywords.length > 0) {
        data.keywords.forEach(kw => {
            const span = document.createElement('span');
            span.className = 'keyword-tag';
            span.textContent = kw;
            keywordsResult.appendChild(span);
        });
    } else {
        keywordsResult.innerHTML = '<span class="label">Minimal entity density detected</span>';
    }

    // Reveal with animation
    resultSection.classList.remove('hidden');
}
