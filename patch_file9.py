import re

with open('update.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update window size from 800 to 1024, height 400 to 576.
viewport_search = '<meta name="viewport" content="width=800, initial-scale=1.0">'
viewport_replace = '<meta name="viewport" content="width=1024, initial-scale=1.0">'
content = content.replace(viewport_search, viewport_replace)

ui_width_search = 'width: 800px;'
ui_width_replace = 'width: 1024px;'
content = content.replace(ui_width_search, ui_width_replace)

canvas_search = '<canvas id="gameCanvas" width="800" height="400"></canvas>'
canvas_replace = '<canvas id="gameCanvas" width="1024" height="576"></canvas>'
content = content.replace(canvas_search, canvas_replace)

# 2. Add mouse aiming logic
js_init_search = """const closeShopBtn = document.getElementById('closeShopBtn');

let score = 0;"""
js_init_replace = """const closeShopBtn = document.getElementById('closeShopBtn');

let mouseX = 0;
let mouseY = 0;

canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouseX = e.clientX - rect.left;
    mouseY = e.clientY - rect.top;
});

let score = 0;"""
content = content.replace(js_init_search, js_init_replace)

shoot_search = """        const muzzleXOffset = this.facingRight ? this.width + 10 : -10;
        const muzzleYOffset = this.height * 0.55;
        muzzleFlashes.push({ x: this.worldX + muzzleXOffset, y: this.worldY + muzzleYOffset, alpha: 1 });

        const bulletXOffset = this.facingRight ? this.width : 0;

        if (weaponStats.pattern === 'single' || weaponStats.pattern === 'single_big') {
            this.bullets.push({
                worldX: this.worldX + bulletXOffset, worldY: bulletY,
                radius: weaponStats.bulletRadius, color: weaponStats.bulletColor,
                speedX: (this.facingRight ? 1 : -1) * weaponStats.bulletSpeed, speedY: 0,
                damage: weaponStats.damage * this.damageMultiplier
            });
        } else if (weaponStats.pattern === 'triple_spread') {
            const angles = [-0.2, 0, 0.2];
            angles.forEach(angle => {
                this.bullets.push({
                    worldX: this.worldX + bulletXOffset, worldY: bulletY,
                    radius: weaponStats.bulletRadius, color: weaponStats.bulletColor,
                    speedX: Math.cos(angle) * (this.facingRight ? 1 : -1) * weaponStats.bulletSpeed,
                    speedY: Math.sin(angle) * weaponStats.bulletSpeed,
                    damage: weaponStats.damage * this.damageMultiplier
                });
            });
        }"""
shoot_replace = """        const weaponX = this.worldX + this.width / 2;
        const weaponY = this.worldY + this.height * 0.5;

        // Target is relative to screen. We need world coordinates for the mouse.
        const targetWorldX = mouseX + cameraX;
        const targetWorldY = mouseY;

        const angle = Math.atan2(targetWorldY - weaponY, targetWorldX - weaponX);

        // Update facing direction based on mouse
        if (targetWorldX > weaponX) this.facingRight = true;
        else this.facingRight = false;

        const muzzleX = weaponX + Math.cos(angle) * (this.width/2 + 10);
        const muzzleY = weaponY + Math.sin(angle) * (this.width/2 + 10);

        muzzleFlashes.push({ x: muzzleX, y: muzzleY, alpha: 1 });

        if (weaponStats.pattern === 'single' || weaponStats.pattern === 'single_big') {
            this.bullets.push({
                worldX: muzzleX, worldY: muzzleY,
                radius: weaponStats.bulletRadius, color: weaponStats.bulletColor,
                speedX: Math.cos(angle) * weaponStats.bulletSpeed,
                speedY: Math.sin(angle) * weaponStats.bulletSpeed,
                damage: weaponStats.damage * this.damageMultiplier
            });
        } else if (weaponStats.pattern === 'triple_spread') {
            const spreadAngles = [-0.2, 0, 0.2];
            spreadAngles.forEach(spread => {
                const finalAngle = angle + spread;
                this.bullets.push({
                    worldX: muzzleX, worldY: muzzleY,
                    radius: weaponStats.bulletRadius, color: weaponStats.bulletColor,
                    speedX: Math.cos(finalAngle) * weaponStats.bulletSpeed,
                    speedY: Math.sin(finalAngle) * weaponStats.bulletSpeed,
                    damage: weaponStats.damage * this.damageMultiplier
                });
            });
        }"""
content = content.replace(shoot_search, shoot_replace)

# Modify player weapon drawing to point to mouse
draw_weapon_search = """                const currentWeaponKey = this.weapons[this.currentWeaponIndex];
                const weaponY = this.worldY + this.height * 0.5;
                ctx.fillStyle = '#666';
                if (this.facingRight) {
                    const weaponX = screenX + this.width - 10;
                    switch(currentWeaponKey) {
                        case 'peck_cannon': ctx.fillRect(weaponX, weaponY, 20, 8); break;
                        case 'feather_spread':
                            ctx.fillRect(weaponX, weaponY - 4, 25, 16);
                            ctx.fillRect(weaponX + 25, weaponY - 2, 5, 12);
                            break;
                        case 'egg_launcher':
                            ctx.fillStyle = '#4a4a4a'; ctx.fillRect(weaponX - 5, weaponY - 8, 30, 16);
                            ctx.beginPath(); ctx.arc(weaponX + 25, weaponY, 10, 0, Math.PI * 2); ctx.fill();
                            break;
                    }
                } else {
                    const weaponX = screenX - 10;
                    switch(currentWeaponKey) {
                        case 'peck_cannon': ctx.fillRect(weaponX, weaponY, 20, 8); break;
                        case 'feather_spread':
                            ctx.fillRect(weaponX - 15, weaponY - 4, 25, 16);
                            ctx.fillRect(weaponX - 20, weaponY - 2, 5, 12);
                            break;
                        case 'egg_launcher':
                            ctx.fillStyle = '#4a4a4a'; ctx.fillRect(weaponX - 15, weaponY - 8, 30, 16);
                            ctx.beginPath(); ctx.arc(weaponX - 15, weaponY, 10, 0, Math.PI * 2); ctx.fill();
                            break;
                    }
                }"""
draw_weapon_replace = """                const currentWeaponKey = this.weapons[this.currentWeaponIndex];
                const weaponCenterX = screenX + this.width / 2;
                const weaponCenterY = this.worldY + this.height * 0.5;

                const targetWorldX = mouseX + cameraX;
                const targetWorldY = mouseY;
                const angle = Math.atan2(targetWorldY - (this.worldY + this.height/2), targetWorldX - (this.worldX + this.width/2));

                ctx.save();
                ctx.translate(weaponCenterX, weaponCenterY);
                ctx.rotate(angle);

                ctx.fillStyle = '#666';
                const weaponX = 10;
                switch(currentWeaponKey) {
                    case 'peck_cannon': ctx.fillRect(weaponX, -4, 20, 8); break;
                    case 'feather_spread':
                        ctx.fillRect(weaponX, -8, 25, 16);
                        ctx.fillRect(weaponX + 25, -6, 5, 12);
                        break;
                    case 'egg_launcher':
                        ctx.fillStyle = '#4a4a4a'; ctx.fillRect(weaponX, -8, 30, 16);
                        ctx.beginPath(); ctx.arc(weaponX + 30, 0, 10, 0, Math.PI * 2); ctx.fill();
                        break;
                }
                ctx.restore();"""
content = content.replace(draw_weapon_search, draw_weapon_replace)

# 3. Add Parallax Background Layers
bg_search = """    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
    gradient.addColorStop(0, skyColor1); gradient.addColorStop(1, skyColor2);
    ctx.fillStyle = gradient; ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 疊加：白天藍天 / 夜晚星空（貼圖存在才畫）
    if (IMAGES.sky && (timeOfDay >= dawnTime && timeOfDay <= duskTime)) {
        ctx.drawImage(IMAGES.sky, 0, 0, canvas.width, canvas.height);
    }
    if (IMAGES.stars && (timeOfDay < dawnTime * 0.9 || timeOfDay > duskTime * 1.05)) {
        const tile = IMAGES.stars, TW = tile.width, TH = tile.height;
        for (let y=0;y<canvas.height;y+=TH){
            for (let x=0;x<canvas.width;x+=TW){
                ctx.drawImage(tile,x,y);
            }
        }
    }"""
bg_replace = """    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
    gradient.addColorStop(0, skyColor1); gradient.addColorStop(1, skyColor2);
    ctx.fillStyle = gradient; ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (IMAGES.sky && (timeOfDay >= dawnTime && timeOfDay <= duskTime)) {
        ctx.drawImage(IMAGES.sky, 0, 0, canvas.width, canvas.height);
    }
    if (IMAGES.stars && (timeOfDay < dawnTime * 0.9 || timeOfDay > duskTime * 1.05)) {
        const tile = IMAGES.stars, TW = tile.width, TH = tile.height;
        for (let y=0;y<canvas.height;y+=TH){
            for (let x=0;x<canvas.width;x+=TW){
                ctx.drawImage(tile,x,y);
            }
        }
    }

    // Draw Parallax Mountains Layer 1 (Back)
    ctx.fillStyle = timeOfDay > duskTime || timeOfDay < dawnTime ? '#111820' : '#2c3e50';
    const parallax1 = cameraX * 0.2;
    ctx.beginPath();
    for (let i = 0; i < 5; i++) {
        const xStart = (i * 600) - (parallax1 % 600);
        ctx.moveTo(xStart - 100, canvas.height);
        ctx.lineTo(xStart + 300, canvas.height - 250);
        ctx.lineTo(xStart + 700, canvas.height);
    }
    ctx.fill();

    // Draw Parallax Hills Layer 2 (Mid)
    ctx.fillStyle = timeOfDay > duskTime || timeOfDay < dawnTime ? '#1a252f' : '#34495e';
    const parallax2 = cameraX * 0.4;
    ctx.beginPath();
    for (let i = 0; i < 6; i++) {
        const xStart = (i * 400) - (parallax2 % 400);
        ctx.moveTo(xStart - 50, canvas.height);
        ctx.quadraticCurveTo(xStart + 200, canvas.height - 180, xStart + 450, canvas.height);
    }
    ctx.fill();"""
content = content.replace(bg_search, bg_replace)

# Fix collision boundaries to account for new canvas height
bounds_search = """        if (this.worldY + this.height > canvas.height + PLAYER_HEIGHT * 2) { playerHealth = 0; gameOver = true; }"""
bounds_replace = """        if (this.worldY + this.height > canvas.height + PLAYER_HEIGHT * 2) { playerHealth = 0; gameOver = true; }"""

with open('update.html', 'w', encoding='utf-8') as f:
    f.write(content)
