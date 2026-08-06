from pathlib import Path

path = Path('dota-blind-spot/index.html')
text = path.read_text(encoding='utf-8')


def replace_once(old: str, new: str, label: str) -> None:
    global text
    if old not in text:
        raise SystemExit(f'marker not found: {label}')
    text = text.replace(old, new, 1)


replace_once('BETA 0.5', 'BETA 0.6', 'version')
replace_once(
    '''        <button class="nav-item active">每日挑战</button>
        <button class="nav-item disabled" title="后续开放" disabled>无尽模式</button>
        <button class="nav-item disabled" title="后续开放" disabled>好友房</button>
        <span class="version">BETA 0.6</span>''',
    '''        <button class="nav-item active">每日挑战</button>
        <button class="nav-item disabled" title="后续开放" disabled>无尽模式</button>
        <button class="nav-item disabled" title="后续开放" disabled>好友房</button>
        <button class="nav-item utility" id="helpBtn">玩法</button>
        <button class="nav-item utility" id="statsBtn">战绩</button>
        <span class="version">BETA 0.6</span>''',
    'nav utilities'
)
replace_once(
    '        <p>每局随机抽取 5 名不同英雄。初始只开放极小视野；每次答错都会扣分、扩大视野，并将侦察点转移到另一个较远的离散位置。</p>',
    '        <p>每局随机抽取 5 名不同英雄。可以直接选择候选英雄，也可以输入全题库英雄名；每次答错都会扩大视野、转移侦察点，并逐步解锁英雄资料。</p>',
    'intro copy'
)

css = r'''
    .nav-item.utility { cursor: pointer; }
    .nav-item.utility:hover { color: #fff; border-color: rgba(216,181,106,.28); background: rgba(216,181,106,.05); }

    .clue-rail { display: grid; grid-template-columns: repeat(3, 1fr); gap: 7px; margin-bottom: 10px; }
    .clue-card { min-height: 56px; padding: 9px 10px; overflow: hidden; border: 1px solid rgba(255,255,255,.07); border-radius: 8px; background: rgba(255,255,255,.018); }
    .clue-card small { display: block; margin-bottom: 5px; color: #666e73; font-size: 9px; letter-spacing: .06em; }
    .clue-card strong { display: block; overflow: hidden; color: #5e666b; font-size: 11px; line-height: 1.35; text-overflow: ellipsis; white-space: nowrap; }
    .clue-card.open { border-color: rgba(216,181,106,.25); background: rgba(216,181,106,.055); animation: clueOpen .34s ease; }
    .clue-card.open small { color: #a68f61; }
    .clue-card.open strong { color: #e0cfaa; white-space: normal; }
    @keyframes clueOpen { from { opacity: .35; transform: translateY(4px); } }

    .guess-history { min-height: 32px; display: flex; align-items: center; gap: 6px; overflow-x: auto; margin-bottom: 9px; scrollbar-width: none; }
    .guess-history::-webkit-scrollbar { display: none; }
    .guess-empty { color: #60686d; font-size: 10px; }
    .guess-chip { flex: 0 0 auto; display: inline-flex; align-items: center; gap: 5px; padding: 6px 8px; color: #da8c80; border: 1px solid rgba(210,75,56,.24); border-radius: 999px; background: rgba(210,75,56,.075); font-size: 10px; }
    .guess-chip::before { content: '×'; font-weight: 900; }

    .guess-form { display: grid; grid-template-columns: minmax(0,1fr) 78px; gap: 7px; margin-bottom: 9px; }
    .hero-input { min-width: 0; height: 42px; padding: 0 12px; color: #e6e9ea; border: 1px solid rgba(255,255,255,.09); border-radius: 8px; outline: none; background: #111518; }
    .hero-input::placeholder { color: #646c71; }
    .hero-input:focus { border-color: rgba(216,181,106,.5); box-shadow: 0 0 0 3px rgba(216,181,106,.06); }
    .hero-input:disabled { opacity: .45; }

    .info-modal { position: fixed; z-index: 80; inset: 0; padding: 18px; display: grid; place-items: center; opacity: 0; pointer-events: none; background: rgba(2,3,4,.8); backdrop-filter: blur(9px); transition: .22s ease; }
    .info-modal.show { opacity: 1; pointer-events: auto; }
    .info-panel { width: min(580px,100%); max-height: min(760px,calc(100vh - 36px)); overflow: auto; border: 1px solid rgba(216,181,106,.24); border-radius: 15px; background: linear-gradient(180deg,#202428,#101315); box-shadow: 0 40px 120px rgba(0,0,0,.68); }
    .info-head { position: sticky; top: 0; z-index: 2; min-height: 58px; padding: 0 17px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--line); background: rgba(27,31,34,.98); }
    .info-head h3 { margin: 0; font: 700 20px Georgia,serif; }
    .close-info { width: 34px; height: 34px; color: #a5abaf; border: 1px solid var(--line); border-radius: 8px; background: #171b1e; cursor: pointer; }
    .info-body { padding: 18px; color: #a5acaF; font-size: 13px; line-height: 1.75; }
    .how-grid { display: grid; gap: 9px; }
    .how-item { display: grid; grid-template-columns: 38px 1fr; gap: 11px; padding: 12px; border: 1px solid var(--line); border-radius: 10px; background: rgba(255,255,255,.018); }
    .how-number { width: 38px; height: 38px; display: grid; place-items: center; color: var(--gold); border: 1px solid rgba(216,181,106,.25); border-radius: 50%; background: rgba(216,181,106,.055); font: 700 18px Georgia,serif; }
    .how-item strong { display: block; margin-bottom: 3px; color: #ece7dc; }
    .stat-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 9px; }
    .stat-box { padding: 14px; text-align: center; border: 1px solid var(--line); border-radius: 10px; background: rgba(255,255,255,.018); }
    .stat-box span { display: block; color: #747c81; font-size: 10px; }
    .stat-box strong { display: block; margin-top: 5px; color: var(--gold); font: 700 25px Georgia,serif; }
    .info-note { margin-top: 12px; padding: 11px 12px; color: #8f969a; border-left: 2px solid rgba(216,181,106,.45); background: rgba(216,181,106,.035); font-size: 11px; }
'''
replace_once('    .toast {', css + '\n    .toast {', 'extra css')

mobile = r'''
    @media (max-width: 900px) {
      .nav-item.utility { display: inline-flex !important; padding: 8px 9px; }
      .nav-item.disabled { display: none !important; }
      .clue-rail { grid-template-columns: 1fr; }
      .clue-card { min-height: 48px; }
    }
    @media (max-width: 560px) {
      .nav-item.utility { font-size: 11px; }
      .version { display: none; }
      .guess-form { grid-template-columns: minmax(0,1fr) 68px; }
    }

'''
replace_once('    @media (prefers-reduced-motion: reduce) {', mobile + '    @media (prefers-reduced-motion: reduce) {', 'mobile overrides')

answer_old = '''          <div class="prompt">迷雾中是哪一位英雄？</div>
          <div class="options" id="options"></div>'''
answer_new = '''          <div class="prompt">迷雾中是哪一位英雄？</div>
          <div class="clue-rail" id="clueRail"></div>
          <div class="guess-history" id="guessHistory"><span class="guess-empty">错误猜测会记录在这里</span></div>
          <div class="guess-form">
            <input class="hero-input" id="heroInput" list="heroNames" placeholder="输入任意英雄名，回车提交" autocomplete="off" />
            <datalist id="heroNames"></datalist>
            <button class="btn" id="submitGuessBtn">提交</button>
          </div>
          <div class="options" id="options"></div>'''
replace_once(answer_old, answer_new, 'answer enhancements')

info_html = '''
  <div class="info-modal" id="infoModal" aria-hidden="true">
    <div class="info-panel">
      <div class="info-head"><h3 id="infoTitle">玩法说明</h3><button class="close-info" id="closeInfoBtn" aria-label="关闭">×</button></div>
      <div class="info-body" id="infoBody"></div>
    </div>
  </div>
'''
replace_once('''  <script>
    const GAME_SIZE = 5;''', info_html + '''
  <script>
    const GAME_SIZE = 5;''', 'info modal')

replace_once(
    '''    let results = [];
    let currentFogPoint = null;''',
    '''    let results = [];
    let currentFogPoint = null;
    let wrongGuesses = [];
    let skipArmed = false;
    let skipTimer = null;
    let statsSaved = false;''',
    'state vars'
)

helpers = r'''

    function deriveClues(question) {
      const hint = question.hint || '';
      const attributeMatch = hint.match(/(力量|敏捷|智力|全才)型/);
      const attackMatch = hint.match(/(近战|远程)英雄/);
      const attribute = attributeMatch ? attributeMatch[1] : '未知';
      const attack = attackMatch ? attackMatch[1] : '未知';
      let feature = hint.replace(/^(力量|敏捷|智力|全才)型(近战|远程)英雄[，,]?\s*/, '');
      if (!feature || feature === hint) feature = hint || '暂无额外英雄档案';
      return [
        { label: '主属性', value: attribute },
        { label: '攻击方式', value: attack },
        { label: '英雄特征', value: feature }
      ];
    }

    function renderClues(revealAll = false) {
      const question = rounds[round];
      if (!question) return;
      const clues = deriveClues(question);
      const unlocked = revealAll ? clues.length : Math.min(attempt, clues.length);
      $('clueRail').innerHTML = clues.map((clue, index) => {
        const open = index < unlocked;
        return `<div class="clue-card ${open ? 'open' : ''}"><small>线索 ${index + 1} · ${clue.label}</small><strong>${open ? clue.value : '等待错误后解锁'}</strong></div>`;
      }).join('');
    }

    function renderGuessHistory() {
      $('guessHistory').innerHTML = wrongGuesses.length
        ? wrongGuesses.map((name) => `<span class="guess-chip">${name}</span>`).join('')
        : '<span class="guess-empty">错误猜测会记录在这里</span>';
      $('guessHistory').scrollLeft = $('guessHistory').scrollWidth;
    }

    function populateHeroNames() {
      const names = [...new Set(pool.map((item) => item.name))].sort((a, b) => a.localeCompare(b, 'zh-CN'));
      $('heroNames').innerHTML = names.map((name) => `<option value="${name}"></option>`).join('');
    }

    function loadLongStats() {
      try {
        return { plays: 0, totalCorrect: 0, totalScore: 0, perfect: 0, ...JSON.parse(localStorage.getItem('dotaFogStats') || '{}') };
      } catch (error) {
        return { plays: 0, totalCorrect: 0, totalScore: 0, perfect: 0 };
      }
    }

    function saveLongStats(correctCount) {
      if (statsSaved) return loadLongStats();
      const stats = loadLongStats();
      stats.plays += 1;
      stats.totalCorrect += correctCount;
      stats.totalScore += totalScore;
      if (correctCount === GAME_SIZE) stats.perfect += 1;
      localStorage.setItem('dotaFogStats', JSON.stringify(stats));
      statsSaved = true;
      return stats;
    }

    function openInfo(title, body) {
      $('infoTitle').textContent = title;
      $('infoBody').innerHTML = body;
      $('infoModal').classList.add('show');
      $('infoModal').setAttribute('aria-hidden', 'false');
    }

    function closeInfo() {
      $('infoModal').classList.remove('show');
      $('infoModal').setAttribute('aria-hidden', 'true');
    }

    function showHelp() {
      openInfo('玩法说明', `
        <div class="how-grid">
          <div class="how-item"><div class="how-number">1</div><div><strong>观察极小视野</strong>首轮只会显示英雄原画的一小块，侦察点不能手动移动。</div></div>
          <div class="how-item"><div class="how-number">2</div><div><strong>错误会带来新信息</strong>每次猜错都会扣 150 分、扩大圆形视野、切换到较远点位，并解锁一条英雄资料。</div></div>
          <div class="how-item"><div class="how-number">3</div><div><strong>两种答题方式</strong>可以点击六个快捷候选，也可以输入题库中的任意英雄名，适合更熟悉 DOTA 的玩家。</div></div>
          <div class="how-item"><div class="how-number">4</div><div><strong>少猜、少提示、快作答</strong>真视会直接解锁全部资料，但扣除 120 分；连胜还能获得额外奖励。</div></div>
        </div>
        <div class="info-note">键盘快捷键：数字 1—6 选择候选；输入框中按 Enter 提交；按 / 可快速聚焦输入框。</div>
      `);
    }

    function showStats() {
      const stats = loadLongStats();
      const averageCorrect = stats.plays ? (stats.totalCorrect / stats.plays).toFixed(1) : '0.0';
      const averageScore = stats.plays ? Math.round(stats.totalScore / stats.plays).toLocaleString() : '0';
      const best = Number(localStorage.getItem('dotaFogBest') || 0).toLocaleString();
      openInfo('本机战绩', `
        <div class="stat-grid">
          <div class="stat-box"><span>完成挑战</span><strong>${stats.plays}</strong></div>
          <div class="stat-box"><span>平均答对</span><strong>${averageCorrect}/5</strong></div>
          <div class="stat-box"><span>平均得分</span><strong>${averageScore}</strong></div>
          <div class="stat-box"><span>历史最高</span><strong>${best}</strong></div>
          <div class="stat-box"><span>全对次数</span><strong>${stats.perfect}</strong></div>
          <div class="stat-box"><span>累计识破</span><strong>${stats.totalCorrect}</strong></div>
        </div>
        <div class="info-note">统计仅保存在当前浏览器，不会上传账号或服务器。</div>
      `);
    }

    function submitTextGuess() {
      if (answered) return;
      const name = $('heroInput').value.trim();
      if (!name) {
        toast('请输入英雄名称。');
        return;
      }
      const selected = pool.find((item) => item.name === name);
      if (!selected) {
        toast('题库中没有这个英雄，请从联想列表选择。');
        return;
      }
      if (wrongGuesses.includes(name)) {
        toast('这个英雄已经猜过了。');
        return;
      }
      const optionButton = [...$('options').querySelectorAll('.option')].find((button) => button.dataset.id === selected.id) || null;
      guess(optionButton, selected.id, selected.name);
      $('heroInput').value = '';
    }

    function armSkip() {
      if (answered) return;
      if (!skipArmed) {
        skipArmed = true;
        $('skipBtn').textContent = '再次点击确认放弃';
        toast('再次点击才会揭晓答案。');
        clearTimeout(skipTimer);
        skipTimer = setTimeout(() => {
          skipArmed = false;
          if (!answered) $('skipBtn').textContent = '放弃并揭晓';
        }, 2200);
        return;
      }
      clearTimeout(skipTimer);
      finish(false, false);
    }
'''
replace_once('\n    function pickFogPoint(previous = null) {', helpers + '\n    function pickFogPoint(previous = null) {', 'helpers')

replace_once(
    '''        pool = data.filter((item) => item && item.id && item.name && item.image);
        const uniqueNames = new Set(pool.map((item) => item.name));''',
    '''        pool = data.filter((item) => item && item.id && item.name && item.image);
        populateHeroNames();
        const uniqueNames = new Set(pool.map((item) => item.name));''',
    'populate names'
)

replace_once(
    '''      round = 0;
      totalScore = 0;
      streak = 0;
      results = [];''',
    '''      round = 0;
      totalScore = 0;
      streak = 0;
      results = [];
      statsSaved = false;''',
    'reset session stats'
)

replace_once(
    '''      hintUsed = false;
      answered = false;

      $('stage').classList.remove('success');''',
    '''      hintUsed = false;
      answered = false;
      wrongGuesses = [];
      skipArmed = false;
      clearTimeout(skipTimer);

      $('stage').classList.remove('success');''',
    'round reset'
)

replace_once(
    '''      $('hintBtn').disabled = false;
      $('skipBtn').disabled = false;

      renderDots();
      renderOptions(question);
      renderRoundStrip();''',
    '''      $('hintBtn').disabled = false;
      $('skipBtn').disabled = false;
      $('skipBtn').textContent = '放弃并揭晓';
      $('heroInput').disabled = false;
      $('submitGuessBtn').disabled = false;
      $('heroInput').value = '';

      renderDots();
      renderClues();
      renderGuessHistory();
      renderOptions(question);
      renderRoundStrip();''',
    'round render extras'
)

replace_once(
    '''    function disableOptions(correctId = '') {
      $('options').querySelectorAll('.option').forEach((button) => {
        button.disabled = true;
        if (correctId && button.dataset.id !== correctId && !button.classList.contains('wrong')) button.classList.add('dimmed');
      });
    }''',
    '''    function disableOptions(correctId = '') {
      $('options').querySelectorAll('.option').forEach((button) => {
        button.disabled = true;
        if (correctId && button.dataset.id !== correctId && !button.classList.contains('wrong')) button.classList.add('dimmed');
      });
      $('heroInput').disabled = true;
      $('submitGuessBtn').disabled = true;
    }''',
    'disable input'
)

start = text.index('    function guess(button, id) {')
end = text.index('\n    function useHint()', start)
new_guess = r'''    function guess(button, id, selectedName = '') {
      if (answered || (button && button.classList.contains('wrong'))) return;
      const question = rounds[round];
      const selected = pool.find((item) => item.id === id);
      const name = selectedName || (selected ? selected.name : '未知英雄');
      if (wrongGuesses.includes(name)) {
        toast('这个英雄已经猜过了。');
        return;
      }
      const isCorrect = id === question.id || name === question.name;
      if (isCorrect) {
        const streakBonus = Math.min(streak * 25, 100);
        if (streakBonus > 0) {
          currentScore += streakBonus;
          showFloat('连胜 +' + streakBonus, true);
          updateScore();
        }
        const correctButton = button || [...$('options').querySelectorAll('.option')].find((item) => item.dataset.id === question.id);
        if (correctButton) correctButton.classList.add('correct');
        disableOptions(question.id);
        $('stage').classList.add('success');
        finish(true, false);
        return;
      }

      attempt++;
      wrongGuesses.push(name);
      currentScore = Math.max(100, currentScore - 150);
      if (button) {
        button.classList.add('wrong');
        button.disabled = true;
      }
      const level = Math.min(attempt, REVEAL.length - 1);
      root.style.setProperty('--reveal', REVEAL[level] + 'px');
      moveFogPoint();
      $('visible').textContent = VISIBLE[level];
      $('attemptLabel').textContent = `第 ${Math.min(attempt + 1, 5)} 次猜测`;
      $('visionState').textContent = `视野等级 ${level + 1}`;
      updateScore();
      renderDots();
      renderClues();
      renderGuessHistory();
      showFloat('−150');
      toast(`回答错误：已解锁第 ${Math.min(attempt, 3)} 条资料，并转移侦察点。`);
      if (attempt >= 5) setTimeout(() => finish(false, false), 430);
    }
'''
text = text[:start] + new_guess + text[end:]

replace_once(
    '''      $('hint').innerHTML = `<b>真视生效：</b>${rounds[round].hint}`;
      $('hintBtn').disabled = true;''',
    '''      $('hint').innerHTML = `<b>真视生效：</b>${rounds[round].hint}`;
      renderClues(true);
      $('hintBtn').disabled = true;''',
    'hint clues'
)

replace_once(
    '''      results.push({ correct, score: currentScore, attempts: correct ? attempt + 1 : 0, name: question.name });''',
    '''      results.push({ correct, score: currentScore, attempts: correct ? attempt + 1 : 0, name: question.name, hintUsed, timeLeft: seconds });''',
    'result metadata'
)

replace_once(
    '''          <div><span>剩余关卡</span><strong>${GAME_SIZE - round - 1}</strong></div>''',
    '''          <div><span>已解锁线索</span><strong>${hintUsed ? 3 : Math.min(attempt, 3)}/3</strong></div>''',
    'result stat clue'
)

old_share = '''    function buildShareText() {
      const no = String(dailyNumber()).padStart(3, '0');
      const blocks = results.map((item) => item.correct ? `🟩${item.attempts}` : '🟥').join(' ');
      return `战争迷雾 #${no}\\n${blocks}\\n答对 ${results.filter((item) => item.correct).length}/${GAME_SIZE} · ${totalScore} 分\\n英雄池 ${new Set(pool.map((item) => item.name)).size}`;
    }'''
new_share = '''    function buildShareText() {
      const no = String(dailyNumber()).padStart(3, '0');
      const blocks = results.map((item) => item.correct ? (item.hintUsed ? '🟨' : '🟩') : '🟥').join('');
      const attempts = results.map((item) => item.correct ? item.attempts : '×').join(' · ');
      return `战争迷雾 #${no}\\n${blocks}\\n猜测 ${attempts}\\n答对 ${results.filter((item) => item.correct).length}/${GAME_SIZE} · ${totalScore} 分`;
    }'''
replace_once(old_share, new_share, 'share format')

start = text.index('    function showFinal() {')
end = text.index('\n    function toast(text)', start)
new_final = r'''    function showFinal() {
      const correctCount = results.filter((item) => item.correct).length;
      const oldBest = Number(localStorage.getItem('dotaFogBest') || 0);
      const newBest = Math.max(oldBest, totalScore);
      localStorage.setItem('dotaFogBest', String(newBest));
      saveLongStats(correctCount);
      $('bestScore').textContent = newBest.toLocaleString();
      const solved = results.filter((item) => item.correct);
      const averageAttempts = solved.length ? (solved.reduce((sum, item) => sum + item.attempts, 0) / solved.length).toFixed(1) : '—';
      const hintCount = results.filter((item) => item.hintUsed).length;
      $('resultImg').style.backgroundImage = 'radial-gradient(circle at 50% 25%, rgba(216,181,106,.22), transparent 28%), linear-gradient(135deg, #3c1511, #0d1012 62%)';
      $('resultImg').style.backgroundSize = 'cover';
      $('resultBody').innerHTML = `
        <div class="kicker">DAILY CHALLENGE COMPLETE</div>
        <h3>${correctCount >= 4 ? '真视先知' : correctCount >= 2 ? '高地观察员' : '战争迷雾受害者'}</h3>
        <div class="end">
          ${results.map((item) => `<span class="${item.correct ? '' : 'fail'}">${item.correct ? (item.hintUsed ? '◐ ' : '✓ ') + item.attempts + '猜' : '×'}</span>`).join('')}
        </div>
        <p>答对 <b style="color:#d8b56a">${correctCount}/${GAME_SIZE}</b>，平均 <b style="color:#d8b56a">${averageAttempts}</b> 猜，使用真视 <b style="color:#d8b56a">${hintCount}</b> 次，总得分 <b style="color:#d8b56a">${totalScore.toLocaleString()}</b>${totalScore >= oldBest && totalScore > 0 ? '，刷新了本机最高纪录。' : '。'}</p>
        <div class="result-actions">
          <button class="btn gold-btn" id="shareBtn">分享战绩</button>
          <button class="btn primary" id="restartBtn">重新随机 5 名英雄</button>
        </div>
      `;
      $('modal').classList.add('show');
      $('modal').setAttribute('aria-hidden', 'false');
      $('shareBtn').onclick = shareResult;
      $('restartBtn').onclick = async () => {
        $('modal').classList.remove('show');
        $('modal').setAttribute('aria-hidden', 'true');
        $('loading').classList.remove('hidden');
        updateLoading(30, '正在重新随机英雄...');
        await startSession(true);
        updateLoading(100, '新一局准备完成');
        setTimeout(() => $('loading').classList.add('hidden'), 220);
      };
    }
'''
text = text[:start] + new_final + text[end:]

old_events = '''    $('hintBtn').onclick = useHint;
    $('skipBtn').onclick = () => finish(false, false);
    document.addEventListener('keydown', (event) => {
      const index = Number(event.key);
      if (index >= 1 && index <= 6 && !answered) {
        const button = $('options').querySelectorAll('.option')[index - 1];
        if (button) button.click();
      }
    });'''
new_events = '''    $('hintBtn').onclick = useHint;
    $('skipBtn').onclick = armSkip;
    $('submitGuessBtn').onclick = submitTextGuess;
    $('heroInput').addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        submitTextGuess();
      }
    });
    $('helpBtn').onclick = showHelp;
    $('statsBtn').onclick = showStats;
    $('closeInfoBtn').onclick = closeInfo;
    $('infoModal').addEventListener('click', (event) => {
      if (event.target === $('infoModal')) closeInfo();
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') closeInfo();
      if (event.key === '/' && !answered) {
        event.preventDefault();
        $('heroInput').focus();
        return;
      }
      if (document.activeElement === $('heroInput')) return;
      const index = Number(event.key);
      if (index >= 1 && index <= 6 && !answered) {
        const button = $('options').querySelectorAll('.option')[index - 1];
        if (button) button.click();
      }
    });'''
replace_once(old_events, new_events, 'events')

path.write_text(text, encoding='utf-8')
print('patched', path, 'chars=', len(text))
