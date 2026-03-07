import re

with open('update.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make coins persistent using localStorage
coins_init_search = """let score = 0;
let coins = 0;
let currentMajorStage = 1;"""

coins_init_replace = """let score = 0;
let coins = parseInt(localStorage.getItem('savedCoins')) || 0;
let currentMajorStage = 1;

function updatePersistentCoins(amount) {
    coins += amount;
    localStorage.setItem('savedCoins', coins);
    if(coinsDisplay) coinsDisplay.textContent = `金幣: ${coins}`;
    if(shopCoinDisplay) shopCoinDisplay.textContent = `擁有金幣: ${coins}`;
}"""
content = content.replace(coins_init_search, coins_init_replace)

pickup_coin_search = """            else if (item.type === 'coin') {
                coins += item.value;
                coinsDisplay.textContent = '金幣: ' + coins;
                playSound('pickup_health', {volume: 0.1}); // Reuse sound for now
            }"""

pickup_coin_replace = """            else if (item.type === 'coin') {
                updatePersistentCoins(item.value);
                playSound('pickup_health', {volume: 0.1}); // Reuse sound for now
            }"""
content = content.replace(pickup_coin_search, pickup_coin_replace)

# Main menu shop integration
btn_style_search = """    <button id="startButton" class="button">開始遊戲</button>
    <div id="messageDisplay" style="font-size: 22px; margin-top: 8px; color: #e67e22;"></div>"""

btn_style_replace = """    <div style="display: flex; gap: 20px;">
        <button id="startButton" class="button">開始遊戲</button>
        <button id="mainShopButton" class="button" style="background-color: #f39c12; box-shadow: 0 4px 0 #d35400;">進入商店</button>
    </div>
    <div id="messageDisplay" style="font-size: 22px; margin-top: 8px; color: #e67e22;"></div>"""
content = content.replace(btn_style_search, btn_style_replace)

shop_functions_search = """/* ===================== 商店邏輯 ===================== */
function showShop() {
    gameRunning = false;
    shopModal.style.display = 'block';
    updateShopUI();
}

function updateShopUI() {
    shopCoinDisplay.textContent = `擁有金幣: ${coins}`;
    btnHeal.disabled = coins < 50 || playerHealth >= player.maxHealth;
    btnDmg.disabled = coins < 100;
    btnMaxHp.disabled = coins < 150;
}

btnHeal.addEventListener('click', () => {
    if (coins >= 50 && playerHealth < player.maxHealth) {
        coins -= 50;
        playerHealth = player.maxHealth;
        playSound('pickup_health');
        updateShopUI();
        healthDisplay.textContent = `生命: ${Math.ceil(playerHealth)}`;
        coinsDisplay.textContent = `金幣: ${coins}`;
    }
});

btnDmg.addEventListener('click', () => {
    if (coins >= 100) {
        coins -= 100;
        player.damageMultiplier += 0.2;
        playSound('pickup_weapon');
        updateShopUI();
        coinsDisplay.textContent = `金幣: ${coins}`;
    }
});

btnMaxHp.addEventListener('click', () => {
    if (coins >= 150) {
        coins -= 150;
        player.maxHealth += 20;
        playerHealth += 20;
        playSound('pickup_health');
        updateShopUI();
        healthDisplay.textContent = `生命: ${Math.ceil(playerHealth)}`;
        coinsDisplay.textContent = `金幣: ${coins}`;
    }
});

closeShopBtn.addEventListener('click', () => {
    shopModal.style.display = 'none';
    currentMajorStage++;
    nextBossSpawnX = player.worldX + BOSS_SPAWN_INTERVAL + Math.random() * 500;
    if (currentMajorStage == 3 || currentMajorStage == 5) collectibles.push(new Collectible(player.worldX + 100, player.worldY, 'weapon', 'egg_launcher'));
    else collectibles.push(new Collectible(player.worldX + 100, player.worldY, 'weapon', 'feather_spread'));

    gameRunning = true;
    gameLoop(); // Restart the game loop
});"""

shop_functions_replace = """/* ===================== 商店邏輯 ===================== */
let isMainMenuShop = false;

function showShop(fromMainMenu = false) {
    gameRunning = false;
    isMainMenuShop = fromMainMenu;
    shopModal.style.display = 'block';
    if(isMainMenuShop) {
        document.getElementById('startButton').style.display = 'none';
        document.getElementById('mainShopButton').style.display = 'none';
        closeShopBtn.textContent = "關閉商店";
    } else {
        closeShopBtn.textContent = "繼續前進";
    }
    updateShopUI();
}

function updateShopUI() {
    shopCoinDisplay.textContent = `擁有金幣: ${coins}`;
    btnHeal.disabled = coins < 50 || playerHealth >= player.maxHealth || isMainMenuShop;
    btnDmg.disabled = coins < 100;
    btnMaxHp.disabled = coins < 150;
}

btnHeal.addEventListener('click', () => {
    if (coins >= 50 && playerHealth < player.maxHealth) {
        updatePersistentCoins(-50);
        playerHealth = player.maxHealth;
        playSound('pickup_health');
        updateShopUI();
        healthDisplay.textContent = `生命: ${Math.ceil(playerHealth)}`;
    }
});

btnDmg.addEventListener('click', () => {
    if (coins >= 100) {
        updatePersistentCoins(-100);
        player.damageMultiplier += 0.2;
        playSound('pickup_weapon');
        updateShopUI();
    }
});

btnMaxHp.addEventListener('click', () => {
    if (coins >= 150) {
        updatePersistentCoins(-150);
        player.maxHealth += 20;
        playerHealth += 20;
        playSound('pickup_health');
        updateShopUI();
        healthDisplay.textContent = `生命: ${Math.ceil(playerHealth)}`;
    }
});

closeShopBtn.addEventListener('click', () => {
    shopModal.style.display = 'none';
    if (isMainMenuShop) {
        document.getElementById('startButton').style.display = 'block';
        document.getElementById('mainShopButton').style.display = 'block';
        // Redraw main menu
        draw();
        return;
    }

    currentMajorStage++;
    nextBossSpawnX = player.worldX + BOSS_SPAWN_INTERVAL + Math.random() * 500;
    if (currentMajorStage == 3 || currentMajorStage == 5) collectibles.push(new Collectible(player.worldX + 100, player.worldY, 'weapon', 'egg_launcher'));
    else collectibles.push(new Collectible(player.worldX + 100, player.worldY, 'weapon', 'feather_spread'));

    gameRunning = true;
    gameLoop(); // Restart the game loop
});

document.getElementById('mainShopButton').addEventListener('click', () => {
    showShop(true);
});"""

content = content.replace(shop_functions_search, shop_functions_replace)

# Display Start Screen logic adjustments
start_screen_search = """function displayStartScreen() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.7)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'white'; ctx.font = '30px "Courier New"'; ctx.textAlign = 'center';
    ctx.fillText('戰鬥雞：無盡征途', canvas.width / 2, canvas.height / 2 - 60);
    ctx.font = '20px "Courier New"';
    ctx.fillText('準備好迎接真正的挑戰了嗎?', canvas.width / 2, canvas.height / 2 -10);
    ctx.fillText('擊敗五大蔬菜魔王，成為雞界傳奇!', canvas.width / 2, canvas.height / 2 + 20);
    ctx.fillText('按"開始遊戲"或 Enter/Space', canvas.width / 2, canvas.height / 2 + 60);
    startButton.style.display = 'block';
}"""

start_screen_replace = """function displayStartScreen() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.7)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'white'; ctx.font = '40px "Courier New"'; ctx.textAlign = 'center';
    ctx.fillText('戰鬥雞：無盡征途', canvas.width / 2, canvas.height / 2 - 60);
    ctx.font = '20px "Courier New"';
    ctx.fillText('準備好迎接真正的挑戰了嗎?', canvas.width / 2, canvas.height / 2 -10);
    ctx.fillText('擊敗蔬菜大軍，成為雞界傳奇!', canvas.width / 2, canvas.height / 2 + 20);

    if (shopModal.style.display !== 'block') {
        document.getElementById('startButton').style.display = 'block';
        document.getElementById('mainShopButton').style.display = 'block';
    }
}"""

content = content.replace(start_screen_search, start_screen_replace)

start_click_search = """startButton.addEventListener('click', async () => {
    if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
        animationFrameId = null;
    }
    if (audioCtx && audioCtx.state === 'suspended') {
        try { await audioCtx.resume(); } catch (e) {}
    }
    // 先載外部素材
    await preloadAll();

    initGame();
    playMusic(false);
    gameRunning = true; gameOver = false; gameWon = false;
    startButton.style.display = 'none'; startButton.textContent = "開始遊戲";
    gameLoop();
});"""

start_click_replace = """startButton.addEventListener('click', async () => {
    if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
        animationFrameId = null;
    }
    if (audioCtx && audioCtx.state === 'suspended') {
        try { await audioCtx.resume(); } catch (e) {}
    }
    // 先載外部素材
    await preloadAll();

    initGame();
    playMusic(false);
    gameRunning = true; gameOver = false; gameWon = false;
    document.getElementById('startButton').style.display = 'none';
    document.getElementById('mainShopButton').style.display = 'none';
    document.getElementById('startButton').textContent = "開始遊戲";
    gameLoop();
});"""

content = content.replace(start_click_search, start_click_replace)

game_over_search = """    ctx.fillText('點擊"重新開始"重新挑戰', canvas.width / 2, canvas.height / 2 + 90);
    startButton.style.display = 'block'; startButton.textContent = "重新開始"; gameRunning = false;
}"""

game_over_replace = """    ctx.fillText('點擊"重新開始"重新挑戰', canvas.width / 2, canvas.height / 2 + 90);
    if(shopModal.style.display !== 'block') {
        document.getElementById('startButton').style.display = 'block';
        document.getElementById('mainShopButton').style.display = 'block';
    }
    document.getElementById('startButton').textContent = "重新開始"; gameRunning = false;
}"""
content = content.replace(game_over_search, game_over_replace)

init_search = """function initGame() {
    score = 0; coins = 0; currentMajorStage = 1; gameOver = false; gameWon = false;"""

init_replace = """function initGame() {
    score = 0; currentMajorStage = 1; gameOver = false; gameWon = false;"""
content = content.replace(init_search, init_replace)


with open('update.html', 'w', encoding='utf-8') as f:
    f.write(content)
