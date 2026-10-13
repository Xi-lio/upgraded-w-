// 双摆 RK4 数值稳定性验证：长时间积分后检查能量漂移与角度是否发散
const P = { L1: 150, L2: 130, m1: 1.0, m2: 1.0, g: 9.8 };
const TH1 = 0, W1 = 1, TH2 = 2, W2 = 3;

function derivatives(s) {
  const t1 = s[TH1], w1 = s[W1], t2 = s[TH2], w2 = s[W2];
  const { L1, L2, m1, m2, g } = P;
  const delta = t1 - t2;
  const denom = 2 * m1 + m2 - m2 * Math.cos(2 * delta);
  const a1 =
    (-g * (2 * m1 + m2) * Math.sin(t1) -
      m2 * g * Math.sin(t1 - 2 * t2) -
      2 * Math.sin(delta) * m2 * (w2 * w2 * L2 + w1 * w1 * L1 * Math.cos(delta))) /
    (L1 * denom);
  const a2 =
    (2 * Math.sin(delta) *
      (w1 * w1 * L1 * (m1 + m2) + g * (m1 + m2) * Math.cos(t1) +
        w2 * w2 * L2 * m2 * Math.cos(delta))) /
    (L2 * denom);
  return [w1, a1, w2, a2];
}

function rk4Step(s, dt) {
  const add = (a, b, k) => a.map((v, i) => v + b[i] * k);
  const k1 = derivatives(s);
  const k2 = derivatives(add(s, k1, dt / 2));
  const k3 = derivatives(add(s, k2, dt / 2));
  const k4 = derivatives(add(s, k3, dt));
  return s.map((v, i) => v + (dt / 6) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]));
}

// 总能量（动能 + 势能），无量纲化后用于检验守恒性
function energy(s) {
  const { L1, L2, m1, m2, g } = P;
  const t1 = s[TH1], w1 = s[W1], t2 = s[TH2], w2 = s[W2];
  const KE =
    0.5 * m1 * L1 * L1 * w1 * w1 +
    0.5 * m2 * (L1 * L1 * w1 * w1 + L2 * L2 * w2 * w2 +
      2 * L1 * L2 * w1 * w2 * Math.cos(t1 - t2));
  const PE = -(m1 + m2) * g * L1 * Math.cos(t1) - m2 * g * L2 * Math.cos(t2);
  return KE + PE;
}

let s = [Math.PI / 2 + 0.6, 0, Math.PI / 2 + 0.9, 0];
const E0 = energy(s);
const SUB = 1 / 600;

// 模拟 60 秒
let maxAbsAngle = 0, maxDrift = 0;
for (let t = 0; t < 60; t += SUB) {
  s = rk4Step(s, SUB);
  const drift = Math.abs((energy(s) - E0) / E0);
  if (drift > maxDrift) maxDrift = drift;
  maxAbsAngle = Math.max(maxAbsAngle, Math.abs(s[TH1]), Math.abs(s[TH2]));
}

const finite = s.every(Number.isFinite);
console.log('积分时长            : 60 s，步长 1/600 s（共 ' + (60 / SUB).toFixed(0) + ' 步）');
console.log('末态                 : θ1=' + s[TH1].toFixed(4) +
            '  θ2=' + s[TH2].toFixed(4) +
            '  ω1=' + s[W1].toFixed(4) + '  ω2=' + s[W2].toFixed(4));
console.log('所有数值是否有限     : ' + (finite ? '是（无 NaN / Infinity）' : '否 —— 数值发散！'));
console.log('最大能量相对漂移     : ' + (maxDrift * 100).toFixed(3) + ' %');
console.log('判定                 : ' + (finite && maxDrift < 0.02
  ? 'PASS —— RK4 步长下能量守恒良好，无数值发散'
  : 'FAIL —— 需要减小步长或改用辛积分器'));
