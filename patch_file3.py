import re

with open('update.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix player health references and damage output
h_search = "playerHealth = Math.min(100, playerHealth + this.healAmount);"
h_replace = "playerHealth = Math.min(this.maxHealth, playerHealth + this.healAmount);"
content = content.replace(h_search, h_replace)

h2_search = "playerHealth = Math.min(100, playerHealth + 50);"
h2_replace = "playerHealth = Math.min(player.maxHealth, playerHealth + 50);"
content = content.replace(h2_search, h2_replace)

h3_search = "playerHealth < 100"
h3_replace = "playerHealth < this.maxHealth"
content = content.replace(h3_search, h3_replace)

dmg1_search = "damage: weaponStats.damage"
dmg1_replace = "damage: weaponStats.damage * this.damageMultiplier"
content = content.replace(dmg1_search, dmg1_replace)

# Ensure init resets properly
init_search = """function initGame() {
    score = 0; currentMajorStage = 1; playerHealth = 100; gameOver = false; gameWon = false;
    bossActive = false; activeBoss = null; cameraX = 0; worldGeneratedUpToX = 0;
    player.worldX = 100; player.worldY = canvas.height - PLAYER_HEIGHT - 100;"""

init_replace = """function initGame() {
    score = 0; coins = 0; currentMajorStage = 1; gameOver = false; gameWon = false;
    player.maxHealth = 100; playerHealth = player.maxHealth; player.damageMultiplier = 1;
    coinsDisplay.textContent = '金幣: 0'; shopModal.style.display = 'none';
    bossActive = false; activeBoss = null; cameraX = 0; worldGeneratedUpToX = 0;
    player.worldX = 100; player.worldY = canvas.height - PLAYER_HEIGHT - 100;"""
content = content.replace(init_search, init_replace)

with open('update.html', 'w', encoding='utf-8') as f:
    f.write(content)
