import re

with open('update.html', 'r', encoding='utf-8') as f:
    content = f.read()

col_draw_search = """        if (this.type === 'weapon' && IMAGES.pickupCoin) {
            ctx.drawImage(IMAGES.pickupCoin, screenX, this.worldY, 20, 20);
        } else if (this.type === 'health' && IMAGES.pickupHeal) {
            ctx.drawImage(IMAGES.pickupHeal, screenX, this.worldY, 20, 20);
        } else {
            ctx.fillStyle = this.type === 'weapon' ? '#00FFFF' : (this.type === 'health' ? '#FF69B4' : '#FFFF00');
            ctx.fillRect(screenX, this.worldY, this.width, this.height);
        }"""

col_draw_replace = """        if (this.type === 'coin') {
            ctx.fillStyle = '#FFD700'; ctx.beginPath(); ctx.arc(screenX + this.width/2, this.worldY + this.height/2, this.width/2, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#F5B041'; ctx.beginPath(); ctx.arc(screenX + this.width/2, this.worldY + this.height/2, this.width/3, 0, Math.PI*2); ctx.fill();
        } else if (this.type === 'weapon' && IMAGES.pickupCoin) {
            ctx.drawImage(IMAGES.pickupCoin, screenX, this.worldY, 20, 20);
        } else if (this.type === 'health' && IMAGES.pickupHeal) {
            ctx.drawImage(IMAGES.pickupHeal, screenX, this.worldY, 20, 20);
        } else {
            ctx.fillStyle = this.type === 'weapon' ? '#00FFFF' : (this.type === 'health' ? '#FF69B4' : '#FFFF00');
            ctx.fillRect(screenX, this.worldY, this.width, this.height);
        }"""

content = content.replace(col_draw_search, col_draw_replace)

drop_coin_search = """                if (target.health <= 0) {
                    score += target.isBoss ? 500 * currentMajorStage : (target.isElite ? 50 : 10 + currentMajorStage * 2);
                    createParticles(target.worldX + target.width/2, target.worldY + target.height/2, 30, target.color || '#FFFFFF', 5, true);"""

drop_coin_replace = """                if (target.health <= 0) {
                    score += target.isBoss ? 500 * currentMajorStage : (target.isElite ? 50 : 10 + currentMajorStage * 2);
                    let dropCoins = target.isBoss ? 50 * currentMajorStage : (target.isElite ? 10 : 3);
                    collectibles.push(new Collectible(target.worldX + target.width/2 - 10, target.worldY + target.height/2 - 10, 'coin', dropCoins));
                    createParticles(target.worldX + target.width/2, target.worldY + target.height/2, 30, target.color || '#FFFFFF', 5, true);"""

content = content.replace(drop_coin_search, drop_coin_replace)

pickup_search = """    // Player vs collectibles
    collectibles.forEach((item, index) => {
        if (!item.collected && player.worldX < item.worldX + item.width && player.worldX + player.width > item.worldX &&
            player.worldY < item.worldY + item.height && player.worldY + player.height > item.worldY) {
            item.collected = true;
            collectibles.splice(index, 1);
            if (item.type === 'weapon') { player.addWeapon(item.value); }
        }
    });"""

pickup_replace = """    // Player vs collectibles
    collectibles.forEach((item, index) => {
        if (!item.collected && player.worldX < item.worldX + item.width && player.worldX + player.width > item.worldX &&
            player.worldY < item.worldY + item.height && player.worldY + player.height > item.worldY) {
            item.collected = true;
            collectibles.splice(index, 1);
            if (item.type === 'weapon') { player.addWeapon(item.value); }
            else if (item.type === 'coin') {
                coins += item.value;
                coinsDisplay.textContent = '金幣: ' + coins;
                playSound('pickup_health', {volume: 0.1}); // Reuse sound for now
            }
        }
    });"""

content = content.replace(pickup_search, pickup_replace)

with open('update.html', 'w', encoding='utf-8') as f:
    f.write(content)
