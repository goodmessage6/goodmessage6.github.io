import re

with open('update.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add UI and logic for vehicle button in shop
shop_btn_search = """        <button id="btnMaxHp" class="shop-btn">最大生命 +20 (150 金幣)</button>
        <button id="closeShopBtn" class="shop-btn">繼續前進</button>"""
shop_btn_replace = """        <button id="btnMaxHp" class="shop-btn">最大生命 +20 (150 金幣)</button>
        <button id="btnVehicle" class="shop-btn">解鎖/呼叫 機甲載具 (500 金幣)</button>
        <button id="closeShopBtn" class="shop-btn">繼續前進</button>"""
content = content.replace(shop_btn_search, shop_btn_replace)

shop_js_search = """const btnMaxHp = document.getElementById('btnMaxHp');
const closeShopBtn = document.getElementById('closeShopBtn');"""
shop_js_replace = """const btnMaxHp = document.getElementById('btnMaxHp');
const btnVehicle = document.getElementById('btnVehicle');
const closeShopBtn = document.getElementById('closeShopBtn');"""
content = content.replace(shop_js_search, shop_js_replace)

shop_logic_search = """function updateShopUI() {
    shopCoinDisplay.textContent = `擁有金幣: ${coins}`;
    btnHeal.disabled = coins < 50 || playerHealth >= player.maxHealth || isMainMenuShop;
    btnDmg.disabled = coins < 100;
    btnMaxHp.disabled = coins < 150;
}"""
shop_logic_replace = """function updateShopUI() {
    shopCoinDisplay.textContent = `擁有金幣: ${coins}`;
    btnHeal.disabled = coins < 50 || playerHealth >= player.maxHealth || isMainMenuShop;
    btnDmg.disabled = coins < 100;
    btnMaxHp.disabled = coins < 150;
    btnVehicle.disabled = coins < 500 || player.hasVehicle;
    if (player.hasVehicle) btnVehicle.textContent = "機甲載具 (已解鎖 - 按 V 呼叫)";
}"""
content = content.replace(shop_logic_search, shop_logic_replace)

shop_events_search = """btnMaxHp.addEventListener('click', () => {
    if (coins >= 150) {
        updatePersistentCoins(-150);
        player.maxHealth += 20;
        playerHealth += 20;
        playSound('pickup_health');
        updateShopUI();
        healthDisplay.textContent = `生命: ${Math.ceil(playerHealth)}`;
    }
});"""
shop_events_replace = """btnMaxHp.addEventListener('click', () => {
    if (coins >= 150) {
        updatePersistentCoins(-150);
        player.maxHealth += 20;
        playerHealth += 20;
        playSound('pickup_health');
        updateShopUI();
        healthDisplay.textContent = `生命: ${Math.ceil(playerHealth)}`;
    }
});

btnVehicle.addEventListener('click', () => {
    if (coins >= 500 && !player.hasVehicle) {
        updatePersistentCoins(-500);
        player.hasVehicle = true;
        playSound('pickup_weapon');
        updateShopUI();
    }
});"""
content = content.replace(shop_events_search, shop_events_replace)

player_props_search = """    isDashing: false,

    healWithGrit: function() {"""
player_props_replace = """    isDashing: false,
    hasVehicle: false,
    inVehicle: false,
    vehicleHp: 200,
    vehicleMaxHp: 200,
    vehicleSummoning: false,
    vehicleSummonTimer: 0,
    vehicleSummonY: 0,

    healWithGrit: function() {"""
content = content.replace(player_props_search, player_props_replace)

# Modify player update to handle summoning animation and vehicle state
player_update_search = """    update: function() {
        if (this.invincibleTimer > 0) {
            this.invincibleTimer -= 1000/60;
            if (this.invincibleTimer <= 0) { this.invincible = false; }
        }

        if (this.dashCooldown > 0) this.dashCooldown--;"""

player_update_replace = """    update: function() {
        if (this.vehicleSummoning) {
            this.vehicleSummonTimer++;
            this.vehicleSummonY += 15;
            if (this.vehicleSummonY >= this.worldY) {
                this.vehicleSummoning = false;
                this.inVehicle = true;
                this.vehicleHp = this.vehicleMaxHp;
                triggerScreenShake(15, 500);
                playSound('particle_burst', {volume: 0.5});
                createParticles(this.worldX + this.width/2, this.worldY + this.height, 50, '#7f8c8d', 8);
                messageDisplay.textContent = "機甲已部署！";
                setTimeout(() => messageDisplay.textContent = "", 2000);
                healthDisplay.textContent = `機甲: ${this.vehicleHp}`;
            }
            return; // Freeze player while summoning
        }

        if (this.invincibleTimer > 0) {
            this.invincibleTimer -= 1000/60;
            if (this.invincibleTimer <= 0) { this.invincible = false; }
        }

        if (this.dashCooldown > 0) this.dashCooldown--;"""
content = content.replace(player_update_search, player_update_replace)

# Modify player drawing to render vehicle
player_draw_search = """    draw: function() {
        const screenX = this.worldX - cameraX;

        // 先用貼圖（小雞 4 幀）"""

player_draw_replace = """    draw: function() {
        const screenX = this.worldX - cameraX;

        if (this.vehicleSummoning) {
            ctx.fillStyle = '#7f8c8d';
            ctx.fillRect(screenX - 10, this.vehicleSummonY - cameraX * 0, 60, 60);
            ctx.fillStyle = '#c0392b';
            ctx.fillRect(screenX, this.vehicleSummonY + 20, 40, 20);
        }

        if (this.inVehicle) {
            ctx.save();
            ctx.translate(screenX + this.width/2, this.worldY + this.height/2);
            ctx.scale(this.facingRight ? 1 : -1, 1);

            // Draw Mech
            ctx.fillStyle = '#7f8c8d'; // Body
            ctx.fillRect(-25, -25, 50, 50);
            ctx.fillStyle = '#2c3e50'; // Cockpit
            ctx.fillRect(-15, -15, 30, 20);
            ctx.fillStyle = '#f1c40f'; // Player eye inside
            ctx.fillRect(-5, -10, 5, 5);
            ctx.fillStyle = '#bdc3c7'; // Legs
            ctx.fillRect(-20, 25, 10, 15);
            ctx.fillRect(10, 25, 10, 15);

            // Giant Cannon
            ctx.fillStyle = '#34495e';
            ctx.fillRect(10, 0, 40, 15);
            ctx.fillStyle = '#e74c3c';
            ctx.fillRect(45, 2, 8, 11);

            ctx.restore();

            // Draw vehicle HP bar overhead
            ctx.fillStyle = 'red'; ctx.fillRect(screenX - 5, this.worldY - 15, 50, 5);
            ctx.fillStyle = '#f1c40f'; ctx.fillRect(screenX - 5, this.worldY - 15, 50 * (this.vehicleHp / this.vehicleMaxHp), 5);

        } else {
        // 先用貼圖（小雞 4 幀）"""

content = content.replace(player_draw_search, player_draw_replace)
player_draw_close_search = """                const legY = this.worldY + this.height - 5;
                ctx.fillRect(screenX + this.width * 0.3 - 2, legY, 4, 10);
                ctx.fillRect(screenX + this.width * 0.7 - 2, legY, 4, 10);
            }
        }

        // 玩家子彈（貼圖優先）"""
player_draw_close_replace = """                const legY = this.worldY + this.height - 5;
                ctx.fillRect(screenX + this.width * 0.3 - 2, legY, 4, 10);
                ctx.fillRect(screenX + this.width * 0.7 - 2, legY, 4, 10);
            }
        }
        } // End else if not in vehicle

        // 玩家子彈（貼圖優先）"""
content = content.replace(player_draw_close_search, player_draw_close_replace)

# Modify shooting logic for vehicle
player_shoot_search = """        this.lastShotTime = now;
        playSound('player_shoot');
        const bulletY = this.worldY + this.height / 2 - weaponStats.bulletRadius;

        const weaponX = this.worldX + this.width / 2;
        const weaponY = this.worldY + this.height * 0.5;"""
player_shoot_replace = """        this.lastShotTime = now;

        if (this.inVehicle) {
            playSound('player_shoot'); // Could use heavier sound
            const targetWorldX = mouseX + cameraX;
            const targetWorldY = mouseY;
            const weaponX = this.worldX + this.width / 2;
            const weaponY = this.worldY + this.height / 2;
            const angle = Math.atan2(targetWorldY - weaponY, targetWorldX - weaponX);

            if (targetWorldX > weaponX) this.facingRight = true;
            else this.facingRight = false;

            const muzzleX = weaponX + Math.cos(angle) * 45;
            const muzzleY = weaponY + Math.sin(angle) * 45;

            muzzleFlashes.push({ x: muzzleX, y: muzzleY, alpha: 1 });

            // Mech shoots powerful explosive rounds
            this.bullets.push({
                worldX: muzzleX, worldY: muzzleY,
                radius: 12, color: '#f1c40f',
                speedX: Math.cos(angle) * 12,
                speedY: Math.sin(angle) * 12,
                damage: 40 * this.damageMultiplier,
                isExplosive: true
            });
            return; // Skip normal weapon logic
        }

        playSound('player_shoot');
        const bulletY = this.worldY + this.height / 2 - weaponStats.bulletRadius;

        const weaponX = this.worldX + this.width / 2;
        const weaponY = this.worldY + this.height * 0.5;"""
content = content.replace(player_shoot_search, player_shoot_replace)

# Key bindings to summon vehicle
keys_search = """    if (e.code === 'KeyP') player.summonPet();
    if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') {"""
keys_replace = """    if (e.code === 'KeyP') player.summonPet();
    if (e.code === 'KeyV' && player.hasVehicle && !player.inVehicle && !player.vehicleSummoning) {
        player.vehicleSummoning = true;
        player.vehicleSummonTimer = 0;
        player.vehicleSummonY = -100;
        player.dx = 0; player.dy = 0;
        playSound('skill_use'); // Use skill sound for incoming
    }
    if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') {"""
content = content.replace(keys_search, keys_replace)

# Modify collision damage to hit vehicle first
collision_search = """                if (!player.invincible) {
                    playerHealth -= bullet.damage; playSound('player_hit'); triggerScreenShake(5, 150);
                    damageOverlay.style.opacity = 1; setTimeout(() => damageOverlay.style.opacity = 0, 100);
                    player.invincible = true; player.invincibleTimer = 1000;
                    if (playerHealth <= 0) { playerHealth = 0; gameOver = true; }
                }"""
collision_replace = """                if (!player.invincible) {
                    playSound('player_hit'); triggerScreenShake(5, 150);
                    damageOverlay.style.opacity = 1; setTimeout(() => damageOverlay.style.opacity = 0, 100);
                    player.invincible = true; player.invincibleTimer = 1000;
                    if (player.inVehicle) {
                        player.vehicleHp -= bullet.damage;
                        if (player.vehicleHp <= 0) {
                            player.inVehicle = false; player.hasVehicle = false; // Destroyed
                            createParticles(player.worldX + player.width/2, player.worldY + player.height/2, 50, '#e74c3c', 10, true);
                            player.dy = -10; // Eject player
                        }
                    } else {
                        playerHealth -= bullet.damage;
                        if (playerHealth <= 0) { playerHealth = 0; gameOver = true; }
                    }
                }"""
content = content.replace(collision_search, collision_replace)

collision_search2 = """            if (!player.invincible) {
                playerHealth -= source.contactDamage; playSound('player_hit', {volume: 0.15}); triggerScreenShake(8, 200);
                damageOverlay.style.opacity = 1; setTimeout(() => damageOverlay.style.opacity = 0, 100);
                player.invincible = true; player.invincibleTimer = 800;
                if (playerHealth <= 0) { playerHealth = 0; gameOver = true; }
            }"""
collision_replace2 = """            if (!player.invincible) {
                playSound('player_hit', {volume: 0.15}); triggerScreenShake(8, 200);
                damageOverlay.style.opacity = 1; setTimeout(() => damageOverlay.style.opacity = 0, 100);
                player.invincible = true; player.invincibleTimer = 800;
                if (player.inVehicle) {
                    player.vehicleHp -= source.contactDamage;
                    if (player.vehicleHp <= 0) {
                        player.inVehicle = false; player.hasVehicle = false;
                        createParticles(player.worldX + player.width/2, player.worldY + player.height/2, 50, '#e74c3c', 10, true);
                        player.dy = -10;
                    }
                } else {
                    playerHealth -= source.contactDamage;
                    if (playerHealth <= 0) { playerHealth = 0; gameOver = true; }
                }
            }"""
content = content.replace(collision_search2, collision_replace2)

collision_search3 = """            if (!player.invincible) {
                playerHealth -= hazard.damage; playSound('player_hit', {volume: 0.1}); triggerScreenShake(3, 100);
                damageOverlay.style.opacity = 1; setTimeout(() => damageOverlay.style.opacity = 0, 100);
                player.invincible = true; player.invincibleTimer = 500;
                if (playerHealth <= 0) { playerHealth = 0; gameOver = true; }
            }"""
collision_replace3 = """            if (!player.invincible) {
                playSound('player_hit', {volume: 0.1}); triggerScreenShake(3, 100);
                damageOverlay.style.opacity = 1; setTimeout(() => damageOverlay.style.opacity = 0, 100);
                player.invincible = true; player.invincibleTimer = 500;
                if (player.inVehicle) {
                    player.vehicleHp -= hazard.damage;
                    if (player.vehicleHp <= 0) {
                        player.inVehicle = false; player.hasVehicle = false;
                        createParticles(player.worldX + player.width/2, player.worldY + player.height/2, 50, '#e74c3c', 10, true);
                        player.dy = -10;
                    }
                } else {
                    playerHealth -= hazard.damage;
                    if (playerHealth <= 0) { playerHealth = 0; gameOver = true; }
                }
            }"""
content = content.replace(collision_search3, collision_replace3)

with open('update.html', 'w', encoding='utf-8') as f:
    f.write(content)
