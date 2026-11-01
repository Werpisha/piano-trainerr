import random
import streamlit as st

# ==================== ДАННЫЕ ====================

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

INTERVALS = {
    'Прима': 0, 'Малая секунда': 1, 'Большая секунда': 2,
    'Малая терция': 3, 'Большая терция': 4, 'Чистая кварта': 5,
    'Увеличенная кварта (тритон)': 6, 'Чистая квинта': 7,
    'Малая секста': 8, 'Большая секста': 9, 'Малая септима': 10,
    'Большая септима': 11, 'Октава': 12,
}

TRIADS = {
    'Мажор': [0, 4, 7],
    'Минор': [0, 3, 7],
    'Уменьшённый': [0, 3, 6],
    'Увеличенный': [0, 4, 8],
}

SEVENTHS = {
    'Мажорный септаккорд (maj7)': [0, 4, 7, 11],
    'Доминантсептаккорд (7)':     [0, 4, 7, 10],
    'Минорный септаккорд (m7)':   [0, 3, 7, 10],
    'Полууменьшённый (m7b5)':     [0, 3, 6, 10],
    'Уменьшённый септаккорд (dim7)': [0, 3, 6, 9],
    'Большой минорный (mMaj7)':   [0, 3, 7, 11],
}

SCALES = {
    'Натуральный мажор':          [2, 2, 1, 2, 2, 2, 1],
    'Натуральный минор':          [2, 1, 2, 2, 1, 2, 2],
    'Гармонический минор':        [2, 1, 2, 2, 1, 3, 1],
    'Мелодический минор (вверх)': [2, 1, 2, 2, 2, 2, 1],
    'Лидийский':                  [2, 2, 2, 1, 2, 2, 1],
    'Целотоновая':                [2, 2, 2, 2, 2, 2],
    'Хроматическая':              [1] * 12,
}

MAJOR_KEYS = {
    'C': 0, 'G': 1, 'D': 2, 'A': 3, 'E': 4, 'B': 5,
    'F#': 6, 'C#': 7,
    'F': -1, 'Bb': -2, 'Eb': -3, 'Ab': -4, 'Db': -5, 'Gb': -6, 'Cb': -7,
}

MINOR_KEYS = {
    'A': 0, 'E': 1, 'B': 2, 'F#': 3, 'C#': 4, 'G#': 5,
    'D#': 6, 'A#': 7,
    'D': -1, 'G': -2, 'C': -3, 'F': -4, 'Bb': -5, 'Eb': -6, 'Ab': -7,
}

PARALLEL = {
    'C': 'A', 'G': 'E', 'D': 'B', 'A': 'F#', 'E': 'C#', 'B': 'G#',
    'F': 'D', 'Bb': 'G', 'Eb': 'C', 'Ab': 'F', 'Db': 'Bb', 'Gb': 'Eb',
    'Cb': 'Ab',
    'A': 'C', 'E': 'G', 'B': 'D', 'F#': 'A', 'C#': 'E', 'G#': 'B',
    'D': 'F', 'G': 'Bb', 'C': 'Eb', 'F': 'Ab', 'Bb': 'Db', 'Eb': 'Gb',
    'Ab': 'Cb',
}

# ==================== ВСПОМОГАТЕЛЬНЫЕ ====================

def note_to_semitone(note):
    return NOTES.index(note)

def semitone_to_note(semi):
    return NOTES[semi % 12]

def chord_notes(root, intervals):
    r = note_to_semitone(root)
    return [semitone_to_note(r + i) for i in intervals]

def interval_name_by_semitones(semi):
    mapping = {
        0: 'прима', 1: 'малая секунда', 2: 'большая секунда',
        3: 'малая терция', 4: 'большая терция', 5: 'чистая кварта',
        6: 'увеличенная кварта (тритон)', 7: 'чистая квинта',
        8: 'малая секста', 9: 'большая секста', 10: 'малая септима',
        11: 'большая септима', 12: 'октава',
    }
    return mapping.get(semi, f'{semi} пт')

def describe_chord(root, intervals):
    parts = []
    prev = 0
    for i, s in enumerate(intervals):
        if i == 0:
            parts.append(f'прима от {root}')
        else:
            step = s - prev
            parts.append(interval_name_by_semitones(step))
        prev = s
    notes = chord_notes(root, intervals)
    return f'**Состав:** {" + ".join(parts)}\n\n**Ноты:** {", ".join(notes)}'

def describe_scale(root, intervals):
    names = []
    for s in intervals:
        if s == 1:
            names.append('полутон')
        elif s == 2:
            names.append('тон')
        elif s == 3:
            names.append('полтора тона')
        else:
            names.append(f'{s} пт')
    notes = [root]
    cur = note_to_semitone(root)
    for s in intervals[:-1]:
        cur += s
        notes.append(semitone_to_note(cur))
    return f'**Интервалы:** {" – ".join(names)}\n\n**Ноты:** {", ".join(notes)} → {notes[0]} (октава)'

# ==================== ГЕНЕРАТОРЫ ЗАДАНИЙ ====================

def make_chord(level):
    root = random.choice(NOTES)
    if level >= 2 and random.random() < 0.5:
        name = random.choice(list(SEVENTHS.keys()))
        return {'kind': 'chord', 'root': root, 'name': name, 'ivs': SEVENTHS[name]}
    name = random.choice(list(TRIADS.keys()))
    return {'kind': 'chord', 'root': root, 'name': name, 'ivs': TRIADS[name]}

def make_interval():
    name = random.choice(list(INTERVALS.keys()))
    return {'kind': 'interval', 'name': name, 'semi': INTERVALS[name]}

def make_scale():
    root = random.choice(NOTES)
    name = random.choice(list(SCALES.keys()))
    return {'kind': 'scale', 'root': root, 'name': name, 'ivs': SCALES[name]}

def make_key_signature():
    if random.random() < 0.5:
        key = random.choice(list(MAJOR_KEYS.keys()))
        signs = MAJOR_KEYS[key]
        tonality = f'{key} мажор'
    else:
        key = random.choice(list(MINOR_KEYS.keys()))
        signs = MINOR_KEYS[key]
        tonality = f'{key} минор'
    if signs > 0:
        answer = f'{signs} диез(а/ов)'
        short = str(signs) + ' диез'
    elif signs < 0:
        answer = f'{abs(signs)} бемоль(я/ей)'
        short = str(abs(signs)) + ' бемоль'
    else:
        answer = 'нет знаков (0)'
        short = '0'
    return {'kind': 'key_signature', 'tonality': tonality,
            'answer': answer, 'short': short}

def make_parallel():
    key = random.choice(list(PARALLEL.keys()))
    return {'kind': 'parallel', 'key': key, 'par': PARALLEL[key]}

def make_arpeggio():
    root = random.choice(NOTES)
    name = random.choice(list(SEVENTHS.keys()))
    return {'kind': 'arpeggio', 'root': root, 'name': name, 'ivs': SEVENTHS[name]}

def generate_task(level):
    pool = []
    if level == 1:
        pool = ['chord', 'interval', 'scale', 'key']
    elif level == 2:
        pool = ['chord', 'interval', 'scale', 'key']
    elif level == 3:
        pool = ['chord', 'interval', 'scale', 'key', 'parallel']
    elif level == 4:
        pool = ['chord', 'interval', 'scale', 'key', 'parallel', 'arpeggio']
    kind = random.choice(pool)
    if kind == 'chord':
        return make_chord(level)
    if kind == 'interval':
        return make_interval()
    if kind == 'scale':
        return make_scale()
    if kind == 'key':
        return make_key_signature()
    if kind == 'parallel':
        return make_parallel()
    if kind == 'arpeggio':
        return make_arpeggio()

# ==================== ПРОВЕРКА ====================

def normalize(s):
    return s.strip().lower().replace('ё', 'е')

def check_key_signature(user, short):
    u = normalize(user)
    num = short.split()[0]
    words = {
        '0': ['0', 'ноль', 'нет'],
        '1': ['1', 'один', 'одна'],
        '2': ['2', 'два', 'две'],
        '3': ['3', 'три'],
        '4': ['4', 'четыре'],
        '5': ['5', 'пять'],
        '6': ['6', 'шесть'],
        '7': ['7', 'семь'],
    }
    matched_num = any(w in u for w in words.get(num, [num]))
    if not matched_num:
        return False
    if 'диез' in short:
        return 'бемоль' not in u
    if 'бемоль' in short:
        return 'диез' not in u
    return True

def check_parallel(user, expected):
    u = normalize(user).replace(' ', '')
    e = normalize(expected).replace(' ', '')
    return e in u

# ==================== UI ====================

st.set_page_config(page_title='Piano Trainer', page_icon='🎹', layout='centered')

st.markdown("""
<style>
.big-task {
    background: #1e3a5f;
    color: white;
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    font-size: 32px;
    margin: 20px 0;
}
.subtask {
    font-size: 18px;
    opacity: 0.8;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title('🎹 Piano Trainer')

# ---- Инициализация состояния ----
if 'level' not in st.session_state:
    st.session_state.level = None
if 'task' not in st.session_state:
    st.session_state.task = None
if 'revealed' not in st.session_state:
    st.session_state.revealed = False
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'feedback' not in st.session_state:
    st.session_state.feedback = None
if 'stats' not in st.session_state:
    st.session_state.stats = {'total': 0, 'correct': 0}

# ---- Экран выбора уровня ----
if st.session_state.level is None:
    st.markdown('### Выберите уровень:')
    st.markdown("""
    - **1 — Новичок**: трезвучия (1–2 октава), интервалы, гаммы, знаки в тональностях
    - **2 — Средний**: все аккорды (включая септаккорды), вся клавиатура
    - **3 — Умеющий**: + параллельные тональности
    - **4 — Продвинутый**: + арпеджио
    """)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button('1. Новичок', use_container_width=True):
        st.session_state.level = 1
        st.session_state.task = generate_task(1)
        st.rerun()
    if c2.button('2. Средний', use_container_width=True):
        st.session_state.level = 2
        st.session_state.task = generate_task(2)
        st.rerun()
    if c3.button('3. Умеющий', use_container_width=True):
        st.session_state.level = 3
        st.session_state.task = generate_task(3)
        st.rerun()
    if c4.button('4. Продвинутый', use_container_width=True):
        st.session_state.level = 4
        st.session_state.task = generate_task(4)
        st.rerun()
    st.stop()

# ---- Основной экран ----
col_l, col_r = st.columns([3, 1])
with col_l:
    lvl_names = {1: 'Новичок', 2: 'Средний', 3: 'Умеющий', 4: 'Продвинутый'}
    st.markdown(f"**Уровень {st.session_state.level} — {lvl_names[st.session_state.level]}**")
with col_r:
    if st.button('🔄 Сменить уровень'):
        st.session_state.level = None
        st.session_state.task = None
        st.session_state.revealed = False
        st.session_state.attempts = 0
        st.session_state.feedback = None
        st.rerun()

st.caption(f"Решено: {st.session_state.stats['correct']} / {st.session_state.stats['total']}")

task = st.session_state.task
kind = task['kind']

# ---- Отображение задания ----
if kind == 'chord':
    st.markdown(
        f'<div class="big-task">🎵 {task["root"]} {task["name"]}'
        f'<div class="subtask">Сыграйте аккорд и нажмите «Показать разбор»</div></div>',
        unsafe_allow_html=True)
elif kind == 'interval':
    st.markdown(
        f'<div class="big-task">🎵 Интервал: {task["name"]}'
        f'<div class="subtask">Постройте от любой ноты, сыграйте и нажмите «Показать разбор»</div></div>',
        unsafe_allow_html=True)
elif kind == 'scale':
    st.markdown(
        f'<div class="big-task">🎵 Гамма: {task["name"]} от {task["root"]}'
        f'<div class="subtask">Сыграйте и нажмите «Показать разбор»</div></div>',
        unsafe_allow_html=True)
elif kind == 'arpeggio':
    st.markdown(
        f'<div class="big-task">🎵 Арпеджио: {task["name"]} от {task["root"]}'
        f'<div class="subtask">Сыграйте вверх и нажмите «Показать разбор»</div></div>',
        unsafe_allow_html=True)
elif kind == 'key_signature':
    st.markdown(
        f'<div class="big-task">❓ Сколько знаков в тональности {task["tonality"]}?'
        f'<div class="subtask">Ответьте числом (например: 2) или словами (2 диез)</div></div>',
        unsafe_allow_html=True)
elif kind == 'parallel':
    st.markdown(
        f'<div class="big-task">❓ Параллельная тональность к {task["key"]}?'
        f'<div class="subtask">Ответьте как тональность (например: A или A минор)</div></div>',
        unsafe_allow_html=True)

# ---- Логика: игровые задания (chord/interval/scale/arpeggio) ----
if kind in ('chord', 'interval', 'scale', 'arpeggio'):
    if not st.session_state.revealed:
        if st.button('✅ Показать разбор', type='primary'):
            st.session_state.revealed = True
            st.rerun()
    else:
        st.success('Разбор:')
        if kind == 'chord':
            st.markdown(describe_chord(task['root'], task['ivs']))
        elif kind == 'interval':
            semi = task['semi']
            tones = semi / 2
            st.markdown(f'**Полутонов:** {semi}  \n**Тонов:** {tones:g}')
        elif kind == 'scale':
            st.markdown(describe_scale(task['root'], task['ivs']))
        elif kind == 'arpeggio':
            st.markdown(describe_chord(task['root'], task['ivs']))
            st.caption('Сыграйте эти ноты поочерёдно вверх и вниз.')
        if st.button('➡️ Следующее задание', type='primary'):
            st.session_state.stats['total'] += 1
            st.session_state.task = generate_task(st.session_state.level)
            st.session_state.revealed = False
            st.rerun()

# ---- Логика: текстовые вопросы (key_signature/parallel) ----
else:
    if not st.session_state.revealed:
        with st.form(key='answer_form', clear_on_submit=True):
            user_answer = st.text_input('Ваш ответ:', key='input_answer')
            submitted = st.form_submit_button('Ответить', type='primary')

        if submitted and user_answer.strip():
            if kind == 'key_signature':
                ok = check_key_signature(user_answer, task['short'])
                expected = task['answer']
            else:
                ok = check_parallel(user_answer, task['par'])
                expected = task['par']

            if ok:
                st.session_state.feedback = ('success', '✅ Верно!')
                st.session_state.revealed = True
                st.session_state.stats['correct'] += 1
                st.session_state.stats['total'] += 1
                st.rerun()
            else:
                st.session_state.attempts += 1
                remaining = 4 - st.session_state.attempts
                if remaining <= 0:
                    st.session_state.feedback = ('error',
                        f'❌ Попытки закончились. Правильный ответ: **{expected}**')
                    st.session_state.revealed = True
                    st.session_state.stats['total'] += 1
                    st.rerun()
                else:
                    st.session_state.feedback = ('warning',
                        f'❌ Неверно. Осталось попыток: {remaining}')
                    st.rerun()

        # показываем фидбек
        if st.session_state.feedback:
            level_, msg = st.session_state.feedback
            if level_ == 'success':
                st.success(msg)
            elif level_ == 'warning':
                st.warning(msg)
            else:
                st.error(msg)
    else:
        if st.session_state.feedback:
            level_, msg = st.session_state.feedback
            if level_ == 'success':
                st.success(msg)
            else:
                st.error(msg)
        if st.button('➡️ Следующее задание', type='primary'):
            st.session_state.task = generate_task(st.session_state.level)
            st.session_state.revealed = False
            st.session_state.attempts = 0
            st.session_state.feedback = None
            st.rerun()
