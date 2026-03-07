import re

with open('update.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Expand MAX_STAGES and BOSS_TYPES
boss_search = """let score = 0;
let coins = 0;
let currentMajorStage = 1;
const MAX_STAGES = 5;
let playerHealth = 100;"""

boss_replace = """let score = 0;
let coins = 0;
let currentMajorStage = 1;
const MAX_STAGES = 10;
let playerHealth = 100;"""
content = content.replace(boss_search, boss_replace)

boss_types_search = """const BOSS_TYPES = [
    { name: '高麗菜國王', type: 'boss_cabbage_king', health: 400, width: 70, height: 70, color: '#5DBB63', damage: 15, specialCooldown: 8000 },
    { name: '番茄領主', type: 'boss_tomato_lord', health: 600, width: 80, height: 80, color: '#D44A4A', damage: 20, specialCooldown: 9000 },
    { name: '玉米將軍', type: 'boss_corn_general', health: 850, width: 60, height: 100, color: '#F8D568', damage: 25, specialCooldown: 7000 },
    { name: '洋蔥霸主', type: 'boss_onion_overlord', health: 1200, width: 90, height: 90, color: '#B264C3', damage: 30, specialCooldown: 10000 },
    { name: '南瓜大帝', type: 'boss_pumpkin_emperor', health: 1800, width: 100, height: 100, color: '#F37021', damage: 35, specialCooldown: 8000 }
];"""

boss_types_replace = """const BOSS_TYPES = [
    { name: '高麗菜國王', type: 'boss_cabbage_king', health: 400, width: 70, height: 70, color: '#5DBB63', damage: 15, specialCooldown: 8000 },
    { name: '番茄領主', type: 'boss_tomato_lord', health: 600, width: 80, height: 80, color: '#D44A4A', damage: 20, specialCooldown: 9000 },
    { name: '玉米將軍', type: 'boss_corn_general', health: 850, width: 60, height: 100, color: '#F8D568', damage: 25, specialCooldown: 7000 },
    { name: '洋蔥霸主', type: 'boss_onion_overlord', health: 1200, width: 90, height: 90, color: '#B264C3', damage: 30, specialCooldown: 10000 },
    { name: '南瓜大帝', type: 'boss_pumpkin_emperor', health: 1800, width: 100, height: 100, color: '#F37021', damage: 35, specialCooldown: 8000 },
    { name: '蘑菇大師', type: 'boss_mushroom_master', health: 2500, width: 80, height: 90, color: '#8e44ad', damage: 40, specialCooldown: 9000 },
    { name: '蘿蔔忍者', type: 'boss_carrot_ninja', health: 3200, width: 60, height: 80, color: '#e67e22', damage: 45, specialCooldown: 6000 },
    { name: '辣椒爆彈', type: 'boss_chili_bomber', health: 4000, width: 70, height: 110, color: '#c0392b', damage: 50, specialCooldown: 8500 },
    { name: '花椰菜坦克', type: 'boss_broccoli_tank', health: 5500, width: 120, height: 100, color: '#27ae60', damage: 60, specialCooldown: 11000 },
    { name: '究極果王', type: 'boss_ultimate_fruit_king', health: 8000, width: 150, height: 150, color: '#f1c40f', damage: 75, specialCooldown: 10000 }
];"""
content = content.replace(boss_types_search, boss_types_replace)

# Draw Bosses
draw_boss_search = """            case 'boss_cabbage_king': case 'boss_tomato_lord': case 'boss_corn_general':
            case 'boss_onion_overlord': case 'boss_pumpkin_emperor':"""
draw_boss_replace = """            case 'boss_cabbage_king': case 'boss_tomato_lord': case 'boss_corn_general':
            case 'boss_onion_overlord': case 'boss_pumpkin_emperor':
            case 'boss_mushroom_master': case 'boss_carrot_ninja': case 'boss_chili_bomber':
            case 'boss_broccoli_tank': case 'boss_ultimate_fruit_king':"""
content = content.replace(draw_boss_search, draw_boss_replace)

# Boss logic block update
boss_logic_search = """                }
                break;
        }

    } else {
        if (this.type === 'wasp') {"""
boss_logic_replace = """                }
                break;
            case 'boss_mushroom_master':
                if (this.attackPhase === 1) {
                    this.worldX = activeBoss.initialArenaX + Math.random() * (canvas.width - this.width);
                    this.worldY = canvas.height - 60 - this.height - Math.random() * 100;
                    for (let i = 0; i < (this.isRaged ? 3 : 1); i++) {
                        environmentalHazards.push({
                            type: 'gas', x: this.worldX + this.width / 2 + (Math.random()-0.5)*100, y: this.worldY + this.height,
                            radius: 0, maxRadius: 150, duration: 250, damage: 0.8
                        });
                    }
                    this.attackPhase = 0;
                } else {
                    if (now - this.lastShotTime > this.shootInterval) {
                        this.lastShotTime = now;
                        for(let i=0; i< (this.isRaged ? 6 : 4); i++){
                            this.bullets.push({
                                worldX: this.worldX + this.width/2, worldY: this.worldY + this.height/2, radius: 8,
                                speedX: (Math.random() - 0.5) * 6, speedY: -5 - Math.random() * 3,
                                color: '#9b59b6', damage: this.damage, creationX: this.worldX, maxRange: ENEMY_BULLET_MAX_RANGE
                            });
                        }
                    }
                }
                break;
            case 'boss_carrot_ninja':
                if (this.attackPhase === 1) {
                    this.attackPhase = 2; this.attackTimer = 20;
                    this.targetX = player.worldX; this.targetY = player.worldY;
                } else if (this.attackPhase === 2) {
                    this.attackTimer--;
                    this.worldX += (this.targetX - this.worldX) * 0.2;
                    this.worldY += (this.targetY - this.worldY) * 0.2;
                    if (this.attackTimer <= 0) {
                        for(let i=0; i<8; i++){
                            const angle = i * (Math.PI / 4);
                            this.bullets.push({
                                worldX: this.worldX + this.width/2, worldY: this.worldY + this.height/2, radius: 5,
                                speedX: Math.cos(angle) * 8, speedY: Math.sin(angle) * 8,
                                color: '#e67e22', damage: this.damage, creationX: this.worldX, maxRange: ENEMY_BULLET_MAX_RANGE
                            });
                        }
                        this.attackPhase = 0;
                        this.worldY = canvas.height - 60 - this.height;
                    }
                } else {
                    if (now - this.lastShotTime > this.shootInterval) {
                        this.lastShotTime = now;
                        this.bullets.push({
                            worldX: this.worldX + this.width/2, worldY: this.worldY + this.height/2, radius: 6,
                            speedX: player.worldX < this.worldX ? -10 : 10, speedY: 0,
                            color: '#d35400', damage: this.damage, creationX: this.worldX, maxRange: ENEMY_BULLET_MAX_RANGE
                        });
                    }
                }
                break;
            case 'boss_chili_bomber':
                if (this.attackPhase === 1) {
                    environmentalHazards.push({type: 'meteor_warning', x: player.worldX + player.width/2, y: canvas.height - 20, radius: 50, duration: 60, damage: 30});
                    if(this.isRaged) {
                        environmentalHazards.push({type: 'meteor_warning', x: player.worldX + player.width/2 - 100, y: canvas.height - 20, radius: 40, duration: 70, damage: 30});
                        environmentalHazards.push({type: 'meteor_warning', x: player.worldX + player.width/2 + 100, y: canvas.height - 20, radius: 40, duration: 70, damage: 30});
                    }
                    this.attackPhase = 0;
                } else {
                    if (now - this.lastShotTime > this.shootInterval) {
                        this.lastShotTime = now;
                        this.bullets.push({
                            worldX: this.worldX + this.width/2, worldY: this.worldY, radius: 12,
                            speedX: (player.worldX - this.worldX) * 0.02, speedY: -8,
                            color: '#e74c3c', damage: this.damage, creationX: this.worldX, maxRange: canvas.height, homing: false, lifetime: 0
                        });
                    }
                }
                break;
            case 'boss_broccoli_tank':
                if (this.attackPhase === 1) {
                    this.attackPhase = 2; this.attackTimer = 60;
                } else if (this.attackPhase === 2) {
                    this.attackTimer--;
                    if (this.attackTimer % 5 === 0) {
                        this.bullets.push({
                            worldX: this.worldX, worldY: this.worldY + this.height/2 + (Math.random()-0.5)*30, radius: 15,
                            speedX: -12, speedY: 0,
                            color: '#2ecc71', damage: this.damage, creationX: this.worldX, maxRange: canvas.width
                        });
                    }
                    if (this.attackTimer <= 0) this.attackPhase = 0;
                } else {
                    if (now - this.lastShotTime > this.shootInterval) {
                        this.lastShotTime = now;
                        for (let i=-1; i<=1; i++) {
                            this.bullets.push({
                                worldX: this.worldX, worldY: this.worldY + 20, radius: 8,
                                speedX: -6, speedY: i * 2,
                                color: '#27ae60', damage: this.damage, creationX: this.worldX, maxRange: ENEMY_BULLET_MAX_RANGE
                            });
                        }
                    }
                }
                break;
            case 'boss_ultimate_fruit_king':
                if (this.attackPhase === 1) {
                    const attacks = [
                        () => { this.attackPhase = 2; this.targetY = 50; },
                        () => { environmentalHazards.push({type: 'gas', x: this.worldX + this.width/2, y: this.worldY + this.height/2, radius: 0, maxRadius: 400, duration: 300, damage: 1.5}); this.attackPhase = 0; },
                        () => {
                            for (let i=-2; i<=2; i++) {
                                environmentalHazards.push({type: 'shockwave', x: this.worldX + this.width/2, y: canvas.height - 60, speedX: i * 5, radius: 20, duration: 100, damage: 25});
                            }
                            this.attackPhase = 0;
                        }
                    ];
                    attacks[Math.floor(Math.random() * attacks.length)]();
                } else if (this.attackPhase === 2) {
                    this.worldY -= 8;
                    if(this.worldY <= this.targetY) this.attackPhase = 3;
                } else if (this.attackPhase === 3) {
                    for(let i=0; i< 8 ; i++){
                        environmentalHazards.push({
                            type: 'meteor_warning', x: activeBoss.initialArenaX + Math.random() * canvas.width, y: canvas.height - 20,
                            radius: 30 + Math.random() * 20, duration: 80, damage: 20
                        });
                    }
                    this.attackPhase = 4;
                } else if (this.attackPhase === 4) {
                    this.worldY += 10;
                    if(this.worldY >= canvas.height - 60 - this.height) {
                        this.worldY = canvas.height - 60 - this.height;
                        triggerScreenShake(20, 800);
                        this.attackPhase = 0;
                    }
                } else {
                    if (now - this.lastShotTime > this.shootInterval) {
                        this.lastShotTime = now;
                        const bulletsToShoot = this.isRaged ? 16 : 10;
                        for (let i = 0; i < bulletsToShoot; i++) {
                            const angle = (Date.now() / 200) + (i * (Math.PI * 2 / bulletsToShoot));
                            this.bullets.push({
                                worldX: this.worldX + this.width / 2, worldY: this.worldY + this.height / 2, radius: 10,
                                speedX: Math.cos(angle) * 5, speedY: Math.sin(angle) * 5,
                                color: '#f1c40f', damage: this.damage, creationX: this.worldX, maxRange: ENEMY_BULLET_MAX_RANGE
                            });
                        }
                    }
                }
                break;
        }

    } else {
        if (this.type === 'wasp') {"""
content = content.replace(boss_logic_search, boss_logic_replace)

with open('update.html', 'w', encoding='utf-8') as f:
    f.write(content)
