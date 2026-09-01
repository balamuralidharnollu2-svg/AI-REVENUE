// 1. The BAR_HEIGHTS constant
const BAR_HEIGHTS = [
  23, 40, 53, 40, 33, 14, 7, 17, 75, 65,
  88, 75, 65, 47, 33, 88, 4, 7, 9, 14,
  95, 65, 79, 37, 7, 40, 17, 20, 62, 47,
  92, 72,
];

// Config: resolve backend dynamically (target port 5000 if not served on same port)
const BACKEND_URL = window.location.port === '5000' ? '' : 'http://127.0.0.1:5000';

// Initial states for client-side simulator fallback
const INITIAL_WORKFLOWS = [
  {
    id: 'wf-1',
    customer: 'Rohit K. (Mock)',
    type: 'checkout',
    amount: 145,
    status: 'recovered',
    intervention: 'Hinglish Voice Recovery',
  },
  {
    id: 'wf-2',
    customer: 'Acme Enterprise (Mock)',
    type: 'receivables',
    amount: 2450,
    status: 'intervening',
    intervention: 'B2B Receivables Chaser',
  },
  {
    id: 'wf-3',
    customer: 'Aria S. (Mock)',
    type: 'subscription',
    amount: 49,
    status: 'detecting',
    intervention: 'Identifying Anomaly...',
  },
];

const INITIAL_LOGS = [
  { timestamp: '17:40:12', message: 'Agent initialized. Compliance engine active.', type: 'info' },
  { timestamp: '17:41:05', message: 'Risk detected: checkout drop-off by Rohit K. ($145)', type: 'warn' },
  { timestamp: '17:41:30', message: 'Intervention: Outbound voice call (Hinglish dialog model).', type: 'info' },
  { timestamp: '17:42:15', message: 'Outcome: Promised payment received. $145 recovered.', type: 'success' },
];

// Frontend State Machine
const state = {
  recoveredAmount: 14205890,
  workflows: [...INITIAL_WORKFLOWS],
  logs: [...INITIAL_LOGS],
  activeTab: 'workflows', // 'workflows' | 'audit' | 'rules'
  isMobileMenuOpen: false,
};

// DOM Cache
const dom = {
  amountVal: document.getElementById('amount-val'),
  workflowsView: document.getElementById('workflows-view'),
  auditView: document.getElementById('audit-view'),
  complianceView: document.getElementById('compliance-view'),
  tabWorkflows: document.getElementById('tab-workflows'),
  tabAudit: document.getElementById('tab-audit'),
  tabRules: document.getElementById('tab-rules'),
  chartBars: document.getElementById('chart-bars'),
  simulateBtn: document.getElementById('simulate-btn'),
  resetBtn: document.getElementById('reset-btn'),
  menuBtn: document.getElementById('menu-btn'),
  menuIcon: document.getElementById('menu-icon'),
  closeIcon: document.getElementById('close-icon'),
  mobileOverlay: document.getElementById('mobile-overlay'),
  mobileBackdrop: document.getElementById('mobile-backdrop'),
  mobilePanel: document.getElementById('mobile-panel'),
};

// Initialize Bottom Chart Bars
function initChart() {
  const maxVal = Math.max(...BAR_HEIGHTS);
  dom.chartBars.innerHTML = '';
  BAR_HEIGHTS.forEach((h, i) => {
    const isProjected = i >= 28;
    const heightPercent = (h / maxVal) * 100;
    const bar = document.createElement('div');
    bar.className = 'flex-1 rounded-[0.5px] animate-bar-grow origin-bottom';
    bar.style.height = `${heightPercent}%`;
    bar.style.backgroundColor = isProjected ? 'rgba(255,255,255,0.1)' : 'white';
    bar.style.animationDelay = `${1100 + i * 30}ms`;
    dom.chartBars.appendChild(bar);
  });
}

// Render dynamic UI parts
function render() {
  // 1. Render Amount
  dom.amountVal.innerText = `$${state.recoveredAmount.toLocaleString()}`;

  // 2. Render Workflows View
  dom.workflowsView.innerHTML = '';
  state.workflows.forEach((item) => {
    let typeLabel = 'Risk Anomaly';
    let typeColor = 'bg-white';
    switch (item.type) {
      case 'checkout':
        typeLabel = 'Checkout Drop-off';
        typeColor = 'bg-blue-400';
        break;
      case 'subscription':
        typeLabel = 'Failed Subscription';
        typeColor = 'bg-purple-400';
        break;
      case 'payment':
        typeLabel = 'Payment Failure';
        typeColor = 'bg-emerald-400';
        break;
      case 'receivables':
        typeLabel = 'B2B Overdue Invoice';
        typeColor = 'bg-amber-400';
        break;
    }

    let statusStyle = 'text-white bg-white/10';
    switch (item.status) {
      case 'detecting':
        statusStyle = 'text-amber-400 bg-amber-400/10';
        break;
      case 'intervening':
        statusStyle = 'text-blue-400 bg-blue-400/10 animate-pulse';
        break;
      case 'recovered':
        statusStyle = 'text-emerald-400 bg-emerald-400/10';
        break;
      case 'failed':
        statusStyle = 'text-rose-400 bg-rose-400/10';
        break;
    }

    const row = document.createElement('div');
    row.className = 'flex items-center justify-between p-3 bg-white/[0.03] hover:bg-white/[0.06] rounded-[12px] border border-white/[0.05] transition-all';
    row.innerHTML = `
      <div class="flex items-center gap-2.5">
        <span class="w-2 h-2 rounded-full ${typeColor}"></span>
        <div class="text-left">
          <p class="text-white text-[13px] font-[450] leading-none mb-1">${item.customer}</p>
          <p class="text-white/50 text-[10px] leading-none">${typeLabel} • ${item.intervention}</p>
        </div>
      </div>
      <div class="text-right">
        <p class="text-white text-[13px] font-[450] leading-none mb-1">$${item.amount}</p>
        <span class="inline-block text-[9px] font-[450] px-1.5 py-0.5 rounded uppercase tracking-wider ${statusStyle}">
          ${item.status}
        </span>
      </div>
    `;
    dom.workflowsView.appendChild(row);
  });

  // 3. Render Audit Log View
  dom.auditView.innerHTML = '';
  state.logs.forEach((log) => {
    let logColorClass = 'text-blue-400';
    switch (log.type) {
      case 'success':
        logColorClass = 'text-emerald-400';
        break;
      case 'warn':
        logColorClass = 'text-amber-400';
        break;
      case 'error':
        logColorClass = 'text-rose-400';
        break;
    }
    const logItem = document.createElement('div');
    logItem.className = 'text-left text-[11px] font-mono leading-relaxed border-b border-white/[0.02] pb-1.5';
    logItem.innerHTML = `
      <span class="text-white/40">[${log.timestamp}]</span>
      <span class="${logColorClass}">${log.message}</span>
    `;
    dom.auditView.appendChild(logItem);
  });

  // 4. Update Tab button states and View Visibilities
  const tabs = [
    { key: 'workflows', btn: dom.tabWorkflows, view: dom.workflowsView },
    { key: 'audit', btn: dom.tabAudit, view: dom.auditView },
    { key: 'rules', btn: dom.tabRules, view: dom.complianceView },
  ];

  tabs.forEach((t) => {
    if (state.activeTab === t.key) {
      t.btn.className = 'flex-1 py-1.5 rounded-[6px] transition-colors text-center text-white bg-white/10';
      t.view.classList.remove('hidden');
    } else {
      t.btn.className = 'flex-1 py-1.5 rounded-[6px] transition-colors text-center text-white/60 hover:text-white';
      t.view.classList.add('hidden');
    }
  });
}

// Tab click handlers
dom.tabWorkflows.addEventListener('click', () => { state.activeTab = 'workflows'; render(); });
dom.tabAudit.addEventListener('click', () => { state.activeTab = 'audit'; render(); });
dom.tabRules.addEventListener('click', () => { state.activeTab = 'rules'; render(); });

// Client-Side Simulated Events (Fallback)
function triggerLocalSimulation() {
  const customers = ['John D. (Mock)', 'Priya M. (Mock)', 'Saasify Inc (Mock)', 'Elena R. (Mock)', 'Karan S. (Mock)'];
  const types = ['checkout', 'subscription', 'payment', 'receivables'];
  const interventions = {
    checkout: 'Hinglish Voice Recovery',
    subscription: 'Failed Subscription Recovery',
    payment: 'Mandate Retry Sequencer',
    receivables: 'B2B Receivables Chaser',
  };
  const amounts = [89, 145, 450, 2450, 75];

  const randomCustomer = customers[Math.floor(Math.random() * customers.length)];
  const randomType = types[Math.floor(Math.random() * types.length)];
  const randomAmount = amounts[Math.floor(Math.random() * amounts.length)];
  const randomIntervention = interventions[randomType];
  const id = `wf-${Date.now()}`;

  state.activeTab = 'workflows';

  const newItem = {
    id,
    customer: randomCustomer,
    type: randomType,
    amount: randomAmount,
    status: 'detecting',
    intervention: 'Identifying Root Cause...',
  };

  state.workflows = [newItem, ...state.workflows.slice(0, 4)];

  const timestamp = new Date().toTimeString().split(' ')[0];
  state.logs.unshift({
    timestamp,
    message: `Risk Anomaly detected: ${randomType} deviation on customer ${randomCustomer} ($${randomAmount})`,
    type: 'warn',
  });
  render();

  setTimeout(() => {
    state.workflows = state.workflows.map((item) =>
      item.id === id
        ? { ...item, status: 'intervening', intervention: randomIntervention }
        : item
    );
    state.logs.unshift({
      timestamp: new Date().toTimeString().split(' ')[0],
      message: `Decision determined: Routing outreach using ${randomIntervention}`,
      type: 'info',
    });
    render();
  }, 1500);

  setTimeout(() => {
    const isSuccess = Math.random() > 0.15;
    const timeStr = new Date().toTimeString().split(' ')[0];

    state.workflows = state.workflows.map((item) =>
      item.id === id ? { ...item, status: isSuccess ? 'recovered' : 'failed' } : item
    );

    if (isSuccess) {
      state.recoveredAmount += randomAmount;
      state.logs.unshift({
        timestamp: timeStr,
        message: `Execution Success: Recovered $${randomAmount} from ${randomCustomer}`,
        type: 'success',
      });
    } else {
      state.logs.unshift({
        timestamp: timeStr,
        message: `Stopping Rule Met: DND constraint or limit reached for ${randomCustomer}`,
        type: 'error',
      });
    }
    render();
  }, 3500);
}

// Reset stats handler (Fallback)
function resetLocalStats() {
  state.recoveredAmount = 14205890;
  state.workflows = [...INITIAL_WORKFLOWS];
  state.logs = [...INITIAL_LOGS];
  state.activeTab = 'workflows';
  render();
}

// Syncing state with FastAPI backend
async function syncWithBackend() {
  try {
    const [statsRes, workflowsRes, logsRes] = await Promise.all([
      fetch(`${BACKEND_URL}/api/stats`),
      fetch(`${BACKEND_URL}/api/workflows`),
      fetch(`${BACKEND_URL}/api/logs`),
    ]);

    if (statsRes.ok && workflowsRes.ok && logsRes.ok) {
      const stats = await statsRes.json();
      const flows = await workflowsRes.json();
      const audit = await logsRes.json();

      state.recoveredAmount = stats.recoveredAmount;
      state.workflows = flows;
      state.logs = audit;
      render();
    }
  } catch (err) {
    console.warn('Backend offline or not reachable. Error:', err);
  }
}

// Bind Button actions
dom.simulateBtn.addEventListener('click', async () => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/simulate`, { method: 'POST' });
    if (response.ok) {
      await syncWithBackend();
    } else {
      triggerLocalSimulation();
    }
  } catch (err) {
    triggerLocalSimulation();
  }
});

dom.resetBtn.addEventListener('click', async () => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/reset`, { method: 'POST' });
    if (response.ok) {
      await syncWithBackend();
    } else {
      resetLocalStats();
    }
  } catch (err) {
    resetLocalStats();
  }
});

// Mobile Overlay Toggle
function toggleMobileMenu() {
  state.isMobileMenuOpen = !state.isMobileMenuOpen;
  document.body.style.overflow = state.isMobileMenuOpen ? 'hidden' : '';

  if (state.isMobileMenuOpen) {
    dom.menuIcon.className.baseVal = 'w-5 h-5 text-white absolute inset-0 transition-all duration-300 ease-out opacity-0 rotate-90 scale-75';
    dom.closeIcon.className.baseVal = 'w-5 h-5 text-white absolute inset-0 transition-all duration-300 ease-out opacity-100 rotate-0 scale-100';

    dom.mobileOverlay.classList.remove('invisible');
    dom.mobileBackdrop.classList.remove('opacity-0');
    dom.mobileBackdrop.classList.add('opacity-100');

    dom.mobilePanel.classList.remove('opacity-0', '-translate-y-4', 'scale-[0.97]');
    dom.mobilePanel.classList.add('opacity-100', 'translate-y-0', 'scale-100');

    const links = document.querySelectorAll('.mobile-link');
    links.forEach((link, idx) => {
      link.style.transitionDelay = `${100 + idx * 50}ms`;
      link.classList.remove('opacity-0', '-translate-x-3');
      link.classList.add('opacity-100', 'translate-x-0');
    });

    const ctas = document.getElementById('mobile-cta-container');
    ctas.style.transitionDelay = '350ms';
    ctas.classList.remove('opacity-0', 'translate-y-2');
    ctas.classList.add('opacity-100', 'translate-y-0');
  } else {
    dom.menuIcon.className.baseVal = 'w-5 h-5 text-white absolute inset-0 transition-all duration-300 ease-out opacity-100 rotate-0 scale-100';
    dom.closeIcon.className.baseVal = 'w-5 h-5 text-white absolute inset-0 transition-all duration-300 ease-out opacity-0 -rotate-90 scale-75';

    dom.mobileBackdrop.classList.remove('opacity-100');
    dom.mobileBackdrop.classList.add('opacity-0');

    dom.mobilePanel.classList.remove('opacity-100', 'translate-y-0', 'scale-100');
    dom.mobilePanel.classList.add('opacity-0', '-translate-y-4', 'scale-[0.97]');

    setTimeout(() => {
      if (!state.isMobileMenuOpen) {
        dom.mobileOverlay.classList.add('invisible');
      }
    }, 500);

    const links = document.querySelectorAll('.mobile-link');
    links.forEach((link) => {
      link.style.transitionDelay = '0ms';
      link.classList.remove('opacity-100', 'translate-x-0');
      link.classList.add('opacity-0', '-translate-x-3');
    });

    const ctas = document.getElementById('mobile-cta-container');
    ctas.style.transitionDelay = '0ms';
    ctas.classList.remove('opacity-100', 'translate-y-0');
    ctas.classList.add('opacity-0', 'translate-y-2');
  }
}

dom.menuBtn.addEventListener('click', toggleMobileMenu);
dom.mobileBackdrop.addEventListener('click', toggleMobileMenu);

// Page Load
initChart();
render();

// Polling for Python API updates (tries every 3s)
setInterval(syncWithBackend, 3000);
syncWithBackend();
