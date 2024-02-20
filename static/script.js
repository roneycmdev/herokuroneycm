function inicializarTabuleiro() {
    const tabuleiro = document.querySelector('#tabuleiro table');
    for (let i = 0; i < 3; i++) {
        const linha = tabuleiro.insertRow();
        for (let j = 0; j < 3; j++) {
            const celula = linha.insertCell();
            celula.classList.add('celula');
            celula.dataset.linha = i;
            celula.dataset.coluna = j;
            celula.addEventListener('click', () => jogar(i, j));
        }
    }
}

function jogar(linha, coluna) {
    fetch('/jogar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({linha, coluna})
    })
    .then(response => response.json())
    .then(data => {
        atualizarTabuleiro(data.tabuleiro);
        if (data.vencedor) {
            alert(data.vencedor === 'Empate' ? 'Empate!' : `Vencedor: ${data.vencedor}`);
            window.location.reload(); // Reinicia o jogo
        }
    })
    .catch(error => console.error('Erro:', error));
}

function atualizarTabuleiro(tabuleiro) {
    document.querySelectorAll('.celula').forEach((celula) => {
        const linha = celula.dataset.linha;
        const coluna = celula.dataset.coluna;
        celula.textContent = tabuleiro[linha][coluna];
    });
}
