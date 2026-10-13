const fs = require('fs');
const vm = require('vm');

function analyze(file) {
  const html = fs.readFileSync(file, 'utf8');
  const scriptBlock = html.match(/<script>([\s\S]*?)<\/script>/)[1];

  // 1) 从 HTML 的 onclick 属性里取出被调用的函数名
  const onclickMatch = html.match(/onclick="([A-Za-z_$][\w$]*)\(\)"/);
  const calledName = onclickMatch ? onclickMatch[1] : null;

  // 2) 把 script 放进沙箱执行，检查该标识符是否存在于全局作用域
  const sandbox = {
    document: { getElementById: () => ({ getContext: () => ({}), addEventListener() {} }) },
    window: {},
    performance: { now: () => 0 },
    requestAnimationFrame() {}
  };
  const ctxObj = vm.createContext(sandbox);
  let defined = null;
  try {
    vm.runInContext(scriptBlock, ctxObj);
    defined = typeof ctxObj[calledName];
  } catch (e) {
    defined = 'SCRIPT_THREW: ' + e.message;
  }

  return { file, calledName, defined };
}

for (const f of [
  'starter_code/03_buggy_practice/index.html',
  'starter_code/04_fixed_solution/index.html'
]) {
  const r = analyze(f);
  const status =
    r.defined === 'function' ? 'OK   -> 全局可调用，控制台无报错' : 'FAIL -> ReferenceError';
  console.log(r.file);
  console.log('   onclick 调用    : ' + r.calledName + '()');
  console.log('   全局查找结果    : ' + r.defined);
  console.log('   判定            : ' + status);
  console.log('');
}
