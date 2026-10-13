// 批量语法体检：抽取每个 HTML 的内嵌 <script> 并用 node --check 校验
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const NODE = process.execPath;
const files = [
  'index.html',
  'starter_code/03_buggy_practice/index.html',
  'starter_code/04_fixed_solution/index.html',
  'bonus_a_double_pendulum/index.html',
  'bonus_b_celestial_persistence/index.html'
];

let allPass = true;
for (const f of files) {
  if (!fs.existsSync(f)) {
    console.log('MISSING  ' + f);
    allPass = false;
    continue;
  }
  const html = fs.readFileSync(f, 'utf8');
  const blocks = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]);
  const tmp = '_syntax_tmp_' + path.basename(path.dirname(f) || 'root') + '.js';
  let status = 'OK';

  for (const js of blocks) {
    fs.writeFileSync(tmp, js, 'utf8');
    try {
      execFileSync(NODE, ['--check', tmp], { stdio: 'pipe' });
    } catch (e) {
      status = 'SYNTAX ERROR -> ' + String(e.stderr || e.message).split('\n').slice(0, 3).join(' ');
      allPass = false;
    }
  }
  if (fs.existsSync(tmp)) fs.unlinkSync(tmp);

  console.log(status.padEnd(8) + '  ' + f + '   (script 块: ' + blocks.length + ')');
}

console.log('');
console.log(allPass ? '全部文件语法校验通过 ✅' : '存在语法错误 ❌');
