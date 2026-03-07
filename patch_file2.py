import re

file_path = "update.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add logic for developer mode sequence tracking
dev_mode_code = """
/* ===================== 開發者模式 ===================== */
const devSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'KeyB', 'KeyA'];
let devSequenceIndex = 0;

function checkDevSequence(code) {
    if (code === devSequence[devSequenceIndex]) {
        devSequenceIndex++;
        if (devSequenceIndex === devSequence.length) {
            activateDevMode();
            devSequenceIndex = 0; // Reset after activation
        }
    } else {
        devSequenceIndex = 0; // Reset if sequence broken
        if (code === devSequence[0]) {
            devSequenceIndex = 1; // Restart sequence if it starts again
        }
    }
}

function activateDevMode() {
    updatePersistentCoins(9999);
    playerHealth = 9999;
    player.maxHealth = 9999;
    player.addWeapon('feather_spread');
    player.addWeapon('egg_launcher');
    player.P_feather_spread_ammo = Infinity;
    player.P_egg_launcher_ammo = Infinity;
    WEAPON_TYPES['feather_spread'].ammo = Infinity;
    WEAPON_TYPES['egg_launcher'].ammo = Infinity;
    player.grit = player.maxGrit;
    messageDisplay.textContent = "開發者模式已啟動！";
    playSound('pet_summon');
    createParticles(player.worldX + player.width/2, player.worldY + player.height/2, 100, '#FFD700', 10);
    setTimeout(() => messageDisplay.textContent = "", 3000);
}
"""

# Insert developer mode variables before the keydown listener
content = re.sub(r'const keys = \{\};\ndocument.addEventListener\(\'keydown\', \(e\) => \{', dev_mode_code + '\nconst keys = {};\ndocument.addEventListener(\'keydown\', (e) => {\n    checkDevSequence(e.code);', content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
