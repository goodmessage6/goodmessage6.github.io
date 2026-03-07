import re

with open('update.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace CSS
css_search = """        #gameUI {
            margin-top: 10px; font-size: 18px; display: flex; justify-content: space-around; width: 800px; flex-wrap: wrap; position: relative;
        }
        #gameUI span { margin: 2px 10px; }
        #controlsInfo { margin-top: 5px; font-size: 14px; text-align: center; }
        .button { padding: 10px 20px; font-size: 18px; color: white; background-color: #27ae60; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px; }
        .button:hover { background-color: #229954; }

        #resourceBarsContainer { display: flex; gap: 20px; justify-content: center; align-items: center; width: 100%; margin: 12px 0; }
        .resource-container { position: relative; width: 200px; height: 15px; background-color: #555; border: 1px solid #fff; border-radius: 3px; }"""

css_replace = """        #gameUI {
            margin-top: 10px; font-size: 18px; display: flex; justify-content: space-around; width: 800px; flex-wrap: wrap; position: relative;
            background: rgba(0, 0, 0, 0.6); padding: 10px; border-radius: 8px; border: 1px solid #444; box-shadow: 0 4px 8px rgba(0,0,0,0.5);
        }
        #gameUI span { margin: 2px 10px; text-shadow: 1px 1px 2px black; font-weight: bold; }
        #controlsInfo { margin-top: 5px; font-size: 14px; text-align: center; color: #ddd; }
        .button { padding: 10px 20px; font-size: 18px; color: white; background-color: #27ae60; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px; box-shadow: 0 4px 0 #1e8449; transition: all 0.1s; }
        .button:hover { background-color: #2ecc71; transform: translateY(2px); box-shadow: 0 2px 0 #1e8449; }

        #shopModal {
            display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #2c3e50, #34495e); border: 4px solid #f1c40f; border-radius: 15px;
            padding: 30px; text-align: center; z-index: 100; box-shadow: 0 0 20px rgba(0,0,0,0.8);
            width: 400px;
        }
        #shopModal h2 { margin-top: 0; color: #f1c40f; text-shadow: 2px 2px 4px #000; font-size: 28px; }
        .shop-btn {
            display: block; width: 100%; margin: 15px 0; padding: 15px; font-size: 18px; font-weight: bold;
            background-color: #e67e22; border: 2px solid #d35400; border-radius: 8px; color: white; cursor: pointer;
            box-shadow: 0 4px 0 #d35400; transition: all 0.1s;
        }
        .shop-btn:hover:not(:disabled) { background-color: #f39c12; transform: translateY(2px); box-shadow: 0 2px 0 #d35400; }
        .shop-btn:disabled { background-color: #7f8c8d; border-color: #95a5a6; box-shadow: 0 4px 0 #95a5a6; cursor: not-allowed; color: #bdc3c7; }
        #closeShopBtn { background-color: #3498db; border-color: #2980b9; box-shadow: 0 4px 0 #2980b9; margin-top: 25px; }
        #closeShopBtn:hover { background-color: #2980b9; transform: translateY(2px); box-shadow: 0 2px 0 #2980b9; }
        #shopCoinDisplay { font-size: 22px; color: #f1c40f; margin-bottom: 20px; font-weight: bold; text-shadow: 1px 1px 2px #000; }

        #resourceBarsContainer { display: flex; gap: 20px; justify-content: center; align-items: center; width: 100%; margin: 12px 0; }
        .resource-container { position: relative; width: 200px; height: 15px; background-color: #555; border: 1px solid #fff; border-radius: 3px; }"""

content = content.replace(css_search, css_replace)

# Replace HTML
html_search = """    <div id="gameUI">
        <span id="score">分數: 0</span>
        <span id="stage">大關卡: 1</span>
        <span id="progress">進度: 0m</span>
        <span id="health">生命: 100</span>
        <span id="weapon">武器: 小雞啄米槍</span>
        <span id="skillStatus">技能: 就緒! (S)</span>
        <span id="petStatus">寵物: 未召喚</span>
    </div>

    <div id="resourceBarsContainer">
        <div id="gritContainer" class="resource-container">"""

html_replace = """    <div id="gameUI">
        <span id="score">分數: 0</span>
        <span id="coinsDisplay">金幣: 0</span>
        <span id="stage">大關卡: 1</span>
        <span id="progress">進度: 0m</span>
        <span id="health">生命: 100</span>
        <span id="weapon">武器: 小雞啄米槍</span>
        <span id="skillStatus">技能: 就緒! (S)</span>
        <span id="petStatus">寵物: 未召喚</span>
    </div>

    <div id="shopModal">
        <h2>★ 神秘商店 ★</h2>
        <div id="shopCoinDisplay">擁有金幣: 0</div>
        <button id="btnHeal" class="shop-btn">恢復生命 (50 金幣)</button>
        <button id="btnDmg" class="shop-btn">攻擊力 +20% (100 金幣)</button>
        <button id="btnMaxHp" class="shop-btn">最大生命 +20 (150 金幣)</button>
        <button id="closeShopBtn" class="shop-btn">繼續前進</button>
    </div>

    <div id="resourceBarsContainer">
        <div id="gritContainer" class="resource-container">"""

content = content.replace(html_search, html_replace)

with open('update.html', 'w', encoding='utf-8') as f:
    f.write(content)
