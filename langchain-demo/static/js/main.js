let emotion = '';
let answers = [];

function showLoader(msg) {
    document.getElementById('status').innerHTML = `<span>${msg}</span><div class="loader"></div>`;
}

const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const snapBtn = document.getElementById('snapBtn');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => { video.srcObject = stream; })
    .catch(err => { document.getElementById('status').innerText = '无法访问摄像头: ' + err; });

snapBtn.onclick = async function () {
    canvas.getContext('2d').drawImage(video, 0, 0, 320, 240);
    let imageData = canvas.toDataURL('image/jpeg');

    snapBtn.disabled = true;
    showLoader('正在识别情绪...');
    document.getElementById('questions').innerHTML = '';
    document.getElementById('inputArea').innerHTML = '';
    document.getElementById('summary').innerHTML = '';
    answers = [];
    document.getElementById('cameraArea').style.display = 'none';

    const res = await fetch('/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: imageData })
    });
    const data = await res.json();
    snapBtn.disabled = false;
    if (data.status === 'ok') {
        emotion = data.emotion;
        document.getElementById('status').innerHTML = `识别到情绪：<b>${emotion}</b>（置信度 ${data.score.toFixed(2)}）`;
        showQuestion(data.question);
    } else {
        document.getElementById('status').innerText = data.msg;
    }
};

function showQuestion(questionText) {
    const chatArea = document.getElementById('questions');
    const inputArea = document.getElementById('inputArea');

    const aiBubble = document.createElement('div');
    aiBubble.className = 'bubble ai';
    printText(aiBubble, questionText);
    chatArea.appendChild(aiBubble);
    chatArea.scrollTop = chatArea.scrollHeight;

    inputArea.innerHTML = `
        <form onsubmit="return false;" class="input-row">
            <input type="text" id="ansInput" placeholder="请输入你的回答" autocomplete="off" autofocus>
            <button id="sendBtn">发送</button>
            <button id="stopBtn" type="button">结束</button>
        </form>
    `;

    document.getElementById('sendBtn').onclick = async function () {
        const val = document.getElementById('ansInput').value.trim();
        if (!val) return;

        const userBubble = document.createElement('div');
        userBubble.className = 'bubble user';
        userBubble.innerText = val;
        chatArea.appendChild(userBubble);
        chatArea.scrollTop = chatArea.scrollHeight;

        answers.push(val);
        inputArea.innerHTML = '';
        showLoader('AI 正在思考下一个问题...');

        const res = await fetch('/next', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answer: val })
        });
        const data = await res.json();
        if (data.status === 'ok') {
            document.getElementById('status').innerText = '';
            showQuestion(data.question);
        } else {
            document.getElementById('status').innerText = data.msg;
        }
    };

    document.getElementById('stopBtn').onclick = function () {
        submitAnswers();
    };
}

async function submitAnswers() {
    showLoader('AI正在分析你的回答...');
    document.getElementById('inputArea').innerHTML = '';
    const res = await fetch('/summary', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ feedbacks: answers, emotion: emotion })
    });
    const data = await res.json();
    const summaryDom = document.getElementById('summary');
    summaryDom.innerHTML = `<b>情绪总结与建议：</b><br><span id="typedText" class="typing"></span>`;
    const typedTarget = document.getElementById('typedText');
        printText(typedTarget, data.result);  // 逐字打印
    // document.getElementById('summary').innerHTML = `<b>情绪总结与建议：</b><br>${data.result}`;
    document.getElementById('status').innerText = '对话结束，可以重新开始。';
    document.getElementById('restartArea').innerHTML = `
        <button id="restartBtn" class="start-btn">🔄 重新开始</button>
    `;
    document.getElementById('restartBtn').onclick = () => window.location.reload();
}


function printText(dom, content, speed = 50) {
    let index = 0;
    setCursorStatus(dom, 'typing');
    let printInterval = setInterval(() => {
        dom.textContent += content[index];
        index++;
        if (index >= content.length) {
            setCursorStatus(dom, 'end');
            clearInterval(printInterval);
        }
    }, speed);
}

function setCursorStatus(dom, status) {
    const classList = {
        loading: 'typing blinker',
        typing: 'typing',
        end: '',
    };
    dom.classList.remove('blinker', 'typing');
    if (classList[status]) {
        dom.classList.add(...classList[status].split(' '));
    }
}

