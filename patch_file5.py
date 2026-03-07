import re

with open('update.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Implement Shop show/hide and logic
shop_logic_search = """                        messageDisplay.textContent = `第 ${currentMajorStage} 關魔王已被擊敗!`;
                        setTimeout(()=> messageDisplay.textContent = "", 3000);
                        playerHealth = Math.min(player.maxHealth, playerHealth + 50);
                        currentMajorStage++;
                        if (currentMajorStage > MAX_STAGES) { gameWon = true; }
                        else {
                            nextBossSpawnX = player.worldX + BOSS_SPAWN_INTERVAL + Math.random() * 500;
                            if (currentMajorStage == 3 || currentMajorStage == 5) collectibles.push(new Collectible(target.worldX + target.width/2, target.worldY + target.height/2, 'weapon', 'egg_launcher'));
                            else collectibles.push(new Collectible(target.worldX + target.width/2, target.worldY + target.height/2, 'weapon', 'feather_spread'));
                        }"""

shop_logic_replace = """                        messageDisplay.textContent = `第 ${currentMajorStage} 關魔王已被擊敗!`;
                        setTimeout(()=> messageDisplay.textContent = "", 3000);
                        playerHealth = Math.min(player.maxHealth, playerHealth + 50);

                        if (currentMajorStage >= MAX_STAGES) {
                            gameWon = true;
                        } else {
                            setTimeout(() => { showShop(); }, 2000);
                        }"""

content = content.replace(shop_logic_search, shop_logic_replace)

shop_functions = """
/* ===================== 商店邏輯 ===================== */
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
});

/* ===================== 介面畫面 ===================== */
"""
content = content.replace("/* ===================== 介面畫面 ===================== */", shop_functions)

with open('update.html', 'w', encoding='utf-8') as f:
    f.write(content)
