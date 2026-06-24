/**
 * Dukick Hub Server — 1 port, 5 agents
 * Port 9000: hub page + proxy to all 5 agents
 */
const http = require('http');
const net = require('net');
const url = require('url');

const AGENTS = [
  { id: 'tong',     port: 9001, label: 'Tổng Coordinator', icon: '🎯', color: '#1e3a5f' },
  { id: 'sales',    port: 9002, label: 'Sales Agent',       icon: '📣', color: '#1e3a2f' },
  { id: 'account',  port: 9003, label: 'Account Agent',     icon: '📋', color: '#3a1e1e' },
  { id: 'creative', port: 9004, label: 'Creative Agent',    icon: '🎨', color: '#2a1e3a' },
  { id: 'finance',  port: 9005, label: 'Finance Agent',     icon: '💰', color: '#1e2e3a' },
];

function buildHubHtml() {
  const tabs = AGENTS.map((a,i) =>
    '  <div class="agent-tab' + (i===0?' active':'') + '" onclick="switchAgent(\'' + a.id + '\',this)">' +
    '<span class="status"></span>' + a.icon + ' ' + a.label + '</div>'
  ).join('\n');
  return `<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dukick Agent Hub</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,sans-serif;background:#0f0f0f;color:#fff;height:100vh;display:flex;flex-direction:column}
header{padding:16px 24px;border-bottom:1px solid #222;display:flex;align-items:center;gap:12px;background:#111}
header h1{font-size:18px;font-weight:600}
header span{color:#555;font-size:13px}
.agents{display:flex;gap:8px;padding:12px 24px;border-bottom:1px solid #222;background:#111;overflow-x:auto}
.agent-tab{padding:8px 16px;border-radius:8px;cursor:pointer;font-size:13px;border:1px solid #2a2a2a;background:#1a1a1a;white-space:nowrap;transition:all 0.2s}
.agent-tab:hover{border-color:#444}
.agent-tab.active{background:#1d4ed8;border-color:#1d4ed8;color:#fff}
.frame-wrap{flex:1;position:relative}
iframe{width:100%;height:100%;border:none;position:absolute;top:0;left:0}
.status{width:8px;height:8px;border-radius:50%;background:#4ade80;display:inline-block;margin-right:6px}
</style>
</head>
<body>
<header>
  <span style="font-size:22px">&#128293;</span>
  <div><h1>Dukick Agent Hub</h1><span>5 AI Agents &#8212; Hermes Studio</span></div>
</header>
<div class="agents" id="tabs">
` + tabs + `
</div>
<div class="frame-wrap">
  <iframe id="frame" src="/proxy/tong/" allow="*"></iframe>
</div>
<script>
function switchAgent(id,el){
  document.querySelectorAll('.agent-tab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('frame').src='/proxy/'+id+'/';
}
</script>
</body>
</html>`;
}

// Proxy HTTP request
function proxyRequest(req, res, targetPort, pathPrefix) {
  const targetPath = req.url.replace(new RegExp('^/proxy/' + pathPrefix), '') || '/';
  const options = {
    hostname: 'localhost',
    port: targetPort,
    path: targetPath,
    method: req.method,
    headers: { ...req.headers, host: 'localhost:' + targetPort },
  };
  const proxy = http.request(options, (proxyRes) => {
    // Fix asset paths in HTML responses
    let contentType = proxyRes.headers['content-type'] || '';
    res.writeHead(proxyRes.statusCode, proxyRes.headers);
    if (contentType.includes('text/html')) {
      let body = '';
      proxyRes.setEncoding('utf8');
      proxyRes.on('data', chunk => body += chunk);
      proxyRes.on('end', () => {
        // Rewrite absolute paths to proxy paths
        body = body.replace(/(href|src|action)="\//g, `$1="/proxy/${pathPrefix}/`);
        body = body.replace(/url\('\//g, `url('/proxy/${pathPrefix}/`);
        res.end(body);
      });
    } else {
      proxyRes.pipe(res);
    }
  });
  proxy.on('error', () => res.end('Agent not available'));
  req.pipe(proxy);
}

const server = http.createServer((req, res) => {
  const parsed = url.parse(req.url);
  const pathname = parsed.pathname;

  // Hub root
  if (pathname === '/' || pathname === '/hub') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    return res.end(buildHubHtml());
  }

  // Proxy to agents
  for (const agent of AGENTS) {
    if (pathname.startsWith('/proxy/' + agent.id)) {
      return proxyRequest(req, res, agent.port, agent.id);
    }
  }

  res.writeHead(404);
  res.end('Not found');
});

// WebSocket proxy
server.on('upgrade', (req, socket, head) => {
  const pathname = url.parse(req.url).pathname;
  for (const agent of AGENTS) {
    if (pathname.startsWith('/proxy/' + agent.id) || pathname.startsWith('/socket.io')) {
      const targetSocket = net.connect(agent.port, 'localhost', () => {
        const newPath = req.url.replace(new RegExp('^/proxy/' + agent.id), '') || '/';
        const reqStr = `${req.method} ${newPath} HTTP/${req.httpVersion}\r\n` +
          Object.entries(req.headers).map(([k,v]) => `${k}: ${v}`).join('\r\n') +
          '\r\n\r\n';
        targetSocket.write(reqStr);
        targetSocket.write(head);
        socket.pipe(targetSocket);
        targetSocket.pipe(socket);
      });
      targetSocket.on('error', () => socket.destroy());
      return;
    }
  }
  socket.destroy();
});

server.listen(9000, '0.0.0.0', () => {
  console.log('Dukick Hub running on http://localhost:9000');
  console.log('Tailscale: https://admin-pc-1.tailc0eb7b.ts.net:9000');
});
