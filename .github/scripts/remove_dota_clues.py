from pathlib import Path
import re

path = Path('dota-blind-spot/index.html')
text = path.read_text(encoding='utf-8')

text = text.replace('BETA 0.6', 'BETA 0.7')
text = text.replace(
    '每局随机抽取 5 名不同英雄。可以直接选择候选英雄，也可以输入全题库英雄名；每次答错都会扩大视野、转移侦察点，并逐步解锁英雄资料。',
    '每局随机抽取 5 名不同英雄。可以直接选择候选英雄，也可以输入全题库英雄名；每次答错只会扩大视野并转移侦察点，不提供属性或英雄特征提示。'
)
text = text.replace('<div class="type">英雄辨识</div>', '<div class="type">纯图挑战</div>')
text = text.replace('          <div class="clue-rail" id="clueRail"></div>\n', '')
text = text.replace(
    '<div class="hint" id="hint"><b>先知提示：</b>暂未使用真视。越早答对，分数越高。</div>',
    '<div class="hint" id="hint"><b>规则：</b>只根据画面判断英雄。真视仅扩大一次可视范围，不提供文字线索。</div>'
)
text = text.replace('使用真视 −120', '扩大视野 −120')

text = re.sub(
    r'\n    \.clue-rail \{.*?@keyframes clueOpen \{.*?\}\n',
    '\n',
    text,
    flags=re.S
)
text = text.replace('      .clue-rail { grid-template-columns: 1fr; }\n', '')
text = text.replace('      .clue-card { min-height: 48px; }\n', '')

text = re.sub(
    r'\n    function deriveClues\(question\) \{.*?\n    \}\n\n    function renderClues\(revealAll = false\) \{.*?\n    \}\n(?=\n    function renderGuessHistory)',
    '\n',
    text,
    flags=re.S
)

text = text.replace(
    '<div class="how-item"><div class="how-number">2</div><div><strong>错误会带来新信息</strong>每次猜错都会扣 150 分、扩大圆形视野、切换到较远点位，并解锁一条英雄资料。</div></div>',
    '<div class="how-item"><div class="how-number">2</div><div><strong>只增加视觉信息</strong>每次猜错都会扣 150 分、扩大圆形视野并切换到较远点位，不会提供主属性或英雄特征。</div></div>'
)
text = text.replace(
    '<div class="how-item"><div class="how-number">4</div><div><strong>少猜、少提示、快作答</strong>真视会直接解锁全部资料，但扣除 120 分；连胜还能获得额外奖励。</div></div>',
    '<div class="how-item"><div class="how-number">4</div><div><strong>少猜、少辅助、快作答</strong>真视只会额外扩大一级画面，并扣除 120 分；连胜还能获得额外奖励。</div></div>'
)

text = text.replace(
    "      $('hint').innerHTML = '<b>先知提示：</b>暂未使用真视。越早答对，分数越高。';",
    "      $('hint').innerHTML = '<b>规则：</b>只根据画面判断英雄。真视仅扩大一次可视范围，不提供文字线索。';"
)
text = text.replace('      renderClues();\n', '')
text = text.replace(
    "      toast(`回答错误：已解锁第 ${Math.min(attempt, 3)} 条资料，并转移侦察点。`);",
    "      toast('回答错误：视野扩大，并转移到新的侦察点。');"
)

old_hint = """    function useHint() {
      if (hintUsed || answered) return;
      hintUsed = true;
      currentScore = Math.max(100, currentScore - 120);
      updateScore();
      $('hint').innerHTML = `<b>真视生效：</b>${rounds[round].hint}`;
      renderClues(true);
      $('hintBtn').disabled = true;
      showFloat('−120');
      toast('已使用真视，本题扣除 120 分。');
    }"""
new_hint = """    function useHint() {
      if (hintUsed || answered) return;
      const currentLevel = Math.min(attempt, REVEAL.length - 2);
      const level = Math.min(currentLevel + 1, REVEAL.length - 2);
      if (level === currentLevel) {
        toast('当前辅助视野已经达到上限。');
        return;
      }
      hintUsed = true;
      currentScore = Math.max(100, currentScore - 120);
      root.style.setProperty('--reveal', REVEAL[level] + 'px');
      $('visible').textContent = VISIBLE[level];
      $('visionState').textContent = `真视等级 ${level + 1}`;
      moveFogPoint();
      updateScore();
      $('hint').innerHTML = '<b>真视已使用：</b>已额外扩大一级可视范围，不提供任何文字线索。';
      $('hintBtn').disabled = true;
      showFloat('−120');
      toast('真视仅扩大视野，本题扣除 120 分。');
    }"""
if old_hint not in text:
    raise SystemExit('useHint block not found')
text = text.replace(old_hint, new_hint)

text = text.replace(
    '<div><span>已解锁线索</span><strong>${hintUsed ? 3 : Math.min(attempt, 3)}/3</strong></div>',
    '<div><span>使用真视</span><strong>${hintUsed ? \'是\' : \'否\'}</strong></div>'
)

if 'clueRail' in text or 'deriveClues' in text or 'renderClues' in text:
    raise SystemExit('clue code still exists')
if '逐步解锁英雄资料' in text or '解锁一条英雄资料' in text:
    raise SystemExit('clue copy still exists')

path.write_text(text, encoding='utf-8')
