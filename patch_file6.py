import re

with open('update.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Adjust physics constants
phys_search = """const GRAVITY = 0.6;
const JUMP_FORCE = -12;"""
phys_replace = """const GRAVITY = 0.7;
const JUMP_FORCE = -13;"""
content = content.replace(phys_search, phys_replace)

# Add dash variables
dash_search = """    damageMultiplier: 1.0,
    animationFrame: 0,
    animationTimer: 0,"""
dash_replace = """    damageMultiplier: 1.0,
    animationFrame: 0,
    animationTimer: 0,
    dashCooldown: 0,
    dashTimer: 0,
    isDashing: false,"""
content = content.replace(dash_search, dash_replace)

# Keybind for dash
keys_search = """    if (e.code === 'KeyQ' || e.code === 'KeyE') player.switchWeapon();
    if (e.code === 'KeyF') player.healWithGrit();
    if (e.code === 'KeyP') player.summonPet();"""
keys_replace = """    if (e.code === 'KeyQ' || e.code === 'KeyE') player.switchWeapon();
    if (e.code === 'KeyF') player.healWithGrit();
    if (e.code === 'KeyP') player.summonPet();
    if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') {
        if (!player.isDashing && player.dashCooldown <= 0 && gameRunning && !gameOver) {
            player.isDashing = true;
            player.dashCooldown = 60;
            player.dashTimer = 10;
            player.invincible = true;
            player.invincibleTimer = 300;
            playSound('skill_use', {volume: 0.2});
        }
    }"""
content = content.replace(keys_search, keys_replace)

# Update physics logic for dash
update_search = """        this.worldX += this.dx;
        if (this.dx > 0) this.facingRight = true; if (this.dx < 0) this.facingRight = false;

        this.dy += GRAVITY;
        this.worldY += this.dy;"""
update_replace = """        if (this.dashCooldown > 0) this.dashCooldown--;

        if (this.isDashing) {
            this.dashTimer--;
            this.dx = this.facingRight ? PLAYER_SPEED * 3 : -PLAYER_SPEED * 3;
            this.dy = 0; // No gravity while dashing

            // Ghost trail effect
            if (this.dashTimer % 2 === 0) {
                createParticles(this.worldX + this.width/2, this.worldY + this.height/2, 2, '#FFD700', 0);
            }

            if (this.dashTimer <= 0) {
                this.isDashing = false;
            }
        }

        this.worldX += this.dx;
        if (!this.isDashing) {
            if (this.dx > 0) this.facingRight = true;
            if (this.dx < 0) this.facingRight = false;
            this.dy += GRAVITY;
        }
        this.worldY += this.dy;"""
content = content.replace(update_search, update_replace)

# Init variables
init_search = """    player.dx = 0; player.dy = 0; player.grounded = false; player.bullets = []; player.facingRight = true;
    player.invincible = false; player.invincibleTimer = 0;
    player.jumps = player.maxJumps;"""
init_replace = """    player.dx = 0; player.dy = 0; player.grounded = false; player.bullets = []; player.facingRight = true;
    player.invincible = false; player.invincibleTimer = 0;
    player.isDashing = false; player.dashCooldown = 0; player.dashTimer = 0;
    player.jumps = player.maxJumps;"""
content = content.replace(init_search, init_replace)

with open('update.html', 'w', encoding='utf-8') as f:
    f.write(content)
