import re

with open('update.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add coin elements and coin variable
js_init_search = """const gritBar = document.getElementById('gritBar');
const gritText = document.getElementById('gritText');
const petSummonBar = document.getElementById('petSummonBar');
const petSummonText = document.getElementById('petSummonText');

let score = 0;
let currentMajorStage = 1;"""

js_init_replace = """const gritBar = document.getElementById('gritBar');
const gritText = document.getElementById('gritText');
const petSummonBar = document.getElementById('petSummonBar');
const petSummonText = document.getElementById('petSummonText');
const coinsDisplay = document.getElementById('coinsDisplay');
const shopModal = document.getElementById('shopModal');
const shopCoinDisplay = document.getElementById('shopCoinDisplay');
const btnHeal = document.getElementById('btnHeal');
const btnDmg = document.getElementById('btnDmg');
const btnMaxHp = document.getElementById('btnMaxHp');
const closeShopBtn = document.getElementById('closeShopBtn');

let score = 0;
let coins = 0;
let currentMajorStage = 1;"""

content = content.replace(js_init_search, js_init_replace)

# Add player properties
player_search = """    worldX: 100, worldY: canvas.height - PLAYER_HEIGHT - 100,
    width: PLAYER_WIDTH, height: PLAYER_HEIGHT,
    dx: 0, dy: 0, grounded: false, facingRight: true,
    color: '#FFD700', bullets: [],
    weapons: ['peck_cannon'],
    currentWeaponIndex: 0,
    lastShotTime: 0,
    P_feather_spread_ammo: 0,
    P_egg_launcher_ammo: 0,
    invincible: false,
    invincibleTimer: 0,
    jumps: 2,
    maxJumps: 2,
    isDoubleJumping: false,
    grit: 0,
    maxGrit: 250,
    healAmount: 15,"""

player_replace = """    worldX: 100, worldY: canvas.height - PLAYER_HEIGHT - 100,
    width: PLAYER_WIDTH, height: PLAYER_HEIGHT,
    dx: 0, dy: 0, grounded: false, facingRight: true,
    color: '#FFD700', bullets: [],
    weapons: ['peck_cannon'],
    currentWeaponIndex: 0,
    lastShotTime: 0,
    P_feather_spread_ammo: 0,
    P_egg_launcher_ammo: 0,
    invincible: false,
    invincibleTimer: 0,
    jumps: 2,
    maxJumps: 2,
    isDoubleJumping: false,
    grit: 0,
    maxGrit: 250,
    healAmount: 15,
    maxHealth: 100,
    damageMultiplier: 1.0,"""

content = content.replace(player_search, player_replace)

with open('update.html', 'w', encoding='utf-8') as f:
    f.write(content)
