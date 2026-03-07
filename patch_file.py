import re

file_path = "update.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add mouse state variables and event listeners
mouse_state_code = """let mouseX = 0;
let mouseY = 0;
let isMouseDown = false;

canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouseX = e.clientX - rect.left;
    mouseY = e.clientY - rect.top;
});

canvas.addEventListener('mousedown', (e) => {
    if (e.button === 0) { // Left click
        isMouseDown = true;
    }
});

canvas.addEventListener('mouseup', (e) => {
    if (e.button === 0) { // Left click
        isMouseDown = false;
    }
});
"""

content = re.sub(r'let mouseX = 0;\s*let mouseY = 0;\s*canvas\.addEventListener\(\'mousemove\', \(e\) => \{\s*const rect = canvas\.getBoundingClientRect\(\);\s*mouseX = e\.clientX - rect\.left;\s*mouseY = e\.clientY - rect\.top;\s*\}\);', mouse_state_code, content)

# Modify update or input loop to handle continuous shooting
handle_input_code = """function handleInput() {
    if (!gameRunning || gameOver) return; player.dx = 0;
    if (keys['ArrowLeft'] || keys['KeyA']) player.dx = -PLAYER_SPEED;
    if (keys['ArrowRight'] || keys['KeyD']) player.dx = PLAYER_SPEED;
    if (isMouseDown || keys['Space']) player.shoot(); // Allow both space and left mouse hold
}"""

content = re.sub(r'function handleInput\(\) \{\s*if \(\!gameRunning \|\| gameOver\) return; player\.dx = 0;\s*if \(keys\[\'ArrowLeft\'\] \|\| keys\[\'KeyA\'\]\) player\.dx = -PLAYER_SPEED;\s*if \(keys\[\'ArrowRight\'\] \|\| keys\[\'KeyD\'\]\) player\.dx = PLAYER_SPEED;\s*\}', handle_input_code, content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
