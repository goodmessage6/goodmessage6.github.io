import re

with open('update.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix shop resume logic to prevent game freeze
shop_resume_search = """closeShopBtn.addEventListener('click', () => {
    shopModal.style.display = 'none';
    currentMajorStage++;
    nextBossSpawnX = player.worldX + BOSS_SPAWN_INTERVAL + Math.random() * 500;
    if (currentMajorStage == 3 || currentMajorStage == 5) collectibles.push(new Collectible(player.worldX + 100, player.worldY, 'weapon', 'egg_launcher'));
    else collectibles.push(new Collectible(player.worldX + 100, player.worldY, 'weapon', 'feather_spread'));

    gameRunning = true;
});"""

shop_resume_replace = """closeShopBtn.addEventListener('click', () => {
    shopModal.style.display = 'none';
    currentMajorStage++;
    nextBossSpawnX = player.worldX + BOSS_SPAWN_INTERVAL + Math.random() * 500;
    if (currentMajorStage == 3 || currentMajorStage == 5) collectibles.push(new Collectible(player.worldX + 100, player.worldY, 'weapon', 'egg_launcher'));
    else collectibles.push(new Collectible(player.worldX + 100, player.worldY, 'weapon', 'feather_spread'));

    gameRunning = true;
    gameLoop(); // Restart the game loop
});"""
content = content.replace(shop_resume_search, shop_resume_replace)

# Prevent space/enter from restarting game when shop is open
input_search = """    if (!gameRunning && (e.code === 'Enter' || e.code === 'Space')) { startButton.click(); return; }
    if (!gameRunning || gameOver) return;"""
input_replace = """    if (!gameRunning && shopModal.style.display !== 'block' && (e.code === 'Enter' || e.code === 'Space')) { startButton.click(); return; }
    if (!gameRunning || gameOver) return;"""
content = content.replace(input_search, input_replace)

with open('update.html', 'w', encoding='utf-8') as f:
    f.write(content)
