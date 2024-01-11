document.getElementById('scoreForm').addEventListener('submit', function(e) {
    e.preventDefault();

    let formData = new FormData(this);
    let scores = {};
    let date = formData.get('date'); // 日付の取得

    formData.forEach((value, key) => {
        if (key.includes('player')) {
            scores[key] = parseFloat(value);
        }
    });

    let sortedScores = Object.keys(scores).sort((a, b) => scores[b] - scores[a]);
    let ranks = {};
    sortedScores.forEach((key, index) => {
        ranks[key] = index + 1;
    });

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ date, scores, ranks })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            this.reset(); // フォームのリセット
        } else {
            alert('エラーが発生しました。');
        }
    });
});
