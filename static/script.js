let idJogo = null;

document.getElementById('novoJogoBtn').addEventListener('click', novoJogo);

function novoJogo() {
    fetch('/novo_jogo')
        .then(response => response.json())
        .then(data => {
            idJogo = data.id_jogo;
            console.log("ID do Jogo:", idJogo); // Para depuração
            inicializarTabuleiro();
        });
}

function inicializarTabuleiro() {
    const tabuleiroElemento = document.getElementById('tabuleiro');
    tabuleiroElemento.innerHTML = '';  // Limpa o tabuleiro anterior
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            const celula = document.createElement('div');
            celula.dataset.linha = i;
            celula.dataset.coluna = j;
            celula.addEventListener('click', () => fazerJogada(i, j));
            tabuleiroElemento.appendChild(celula);
        }
    }
}

function fazerJogada(linha, coluna) {
    if (!idJogo) return;
    fetch('/jogar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({id_jogo: idJogo, linha, coluna})
    })
    .then(response => response.json())
    .then(jogo => {
        console.log(jogo); // Para depuração
        atualizarTabuleiro(jogo.tabuleiro);
        if (jogo.vencedor) {
            alert(jogo.vencedor === 'Empate' ? 'Empate!' : `Vencedor: ${jogo.vencedor}`);
        }
    });
}

function atualizarTabuleiro(tabuleiro) {
    tabuleiro.forEach((linha, i) => {
        linha.forEach((valor, j) => {
            const celula = document.querySelector(`[data-linha="${i}"][data-coluna="${j}"]`);
            celula.textContent = valor;
        });
    });
}
document.getElementById('novoJogoBtn').addEventListener('click', novoJogo);
document.getElementById('entrarJogoBtn').addEventListener('click', entrarJogo);

function novoJogo() {
    fetch('/novo_jogo')
        .then(response => response.json())
        .then(data => {
            idJogo = data.id_jogo;
            alert("ID do Jogo: " + idJogo); // Exibe o ID do jogo para compartilhamento
            inicializarTabuleiro();
            atualizarEstadoJogo();
        });
}

function entrarJogo() {
    const idJogoEntrada = document.getElementById('idJogoEntrada').value;
    if (idJogoEntrada) {
        idJogo = idJogoEntrada;
        inicializarTabuleiro();
        atualizarEstadoJogo();
    }
}

function atualizarEstadoJogo() {
    if (!idJogo) return;
    fetch(`/estado/${idJogo}`)
        .then(response => response.json())
        .then(data => {
            if (data.tabuleiro) {
                atualizarTabuleiro(data.tabuleiro);
            }
            if (!data.vencedor) {
                setTimeout(atualizarEstadoJogo, 2000); // Atualiza o estado do jogo a cada 2 segundos
            } else if (data.vencedor !== 'Empate') {
                alert(`Vencedor: ${data.vencedor}`);
            } else {
                alert("Empate!");
            }
        });
}
