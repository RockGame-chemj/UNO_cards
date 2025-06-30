const socket = io("https://your-render-app.onrender.com"); // 替换为你的Render后端地址
let myHand = [];
let currentPlayer = null;
let myPlayerId = null;

// 初始化连接
socket.on("connect", () => {
    myPlayerId = socket.id;
    console.log("Connected as player:", myPlayerId);
});

// 更新游戏状态
socket.on("update-game", (data) => {
    myHand = data.hand;
    currentPlayer = data.currentPlayer;
    document.getElementById("player-count").textContent = data.playerCount;
    renderGame();
});

// 渲染游戏界面
function renderGame() {
    const handDiv = document.getElementById("hand");
    handDiv.innerHTML = "";
    myHand.forEach(card => {
        const cardDiv = document.createElement("div");
        cardDiv.className = `card ${card.color}`;
        cardDiv.textContent = card.value;
        cardDiv.onclick = () => playCard(card);
        handDiv.appendChild(cardDiv);
    });

    // 更新弃牌堆
    if (data.discardPile.length > 0) {
        const topCard = data.discardPile[data.discardPile.length - 1];
        const pileDiv = document.getElementById("discard-pile");
        pileDiv.className = `card ${topCard.color}`;
        pileDiv.textContent = topCard.value;
    }

    // 启用/禁用UNO按钮
    document.getElementById("uno-button").disabled = (currentPlayer !== myPlayerId);
}

// 出牌
function playCard(card) {
    if (currentPlayer === myPlayerId) {
        socket.emit("play-card", { card });
    }
}

// 喊UNO
document.getElementById("uno-button").addEventListener("click", () => {
    socket.emit("call-uno");
});
