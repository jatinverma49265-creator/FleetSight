import { chromium } from 'playwright';
import { AxeBuilder } from '@axe-core/playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const reviewDir = path.resolve(__dirname, '../docs/ui-review');
if (!fs.existsSync(reviewDir)) {
  fs.mkdirSync(reviewDir, { recursive: true });
}

// Copy before screenshots if available
const brainScreenshotsDir = '/Users/jiteshvishnoi/.gemini/antigravity-ide/brain/16afb82e-acaa-423e-9520-34e126c2a5e2/screenshots';
const beforeMap = {
  '1_gis_map_view.png': 'risk-map-before-1280.png',
  '2_work_orders_approved.png': 'work-orders-before-1280.png',
  '4_traffic_heatmap.png': 'traffic-before-1280.png',
  '5_audit_trail.png': 'audit-before-1280.png',
  '9_public_portal.png': 'public-portal-before-1280.png',
  '6_bytes_comparison_modal.png': 'dashboard-before-1280.png'
};

for (const [src, dest] of Object.entries(beforeMap)) {
  const srcPath = path.join(brainScreenshotsDir, src);
  const destPath = path.join(reviewDir, dest);
  if (fs.existsSync(srcPath) && !fs.existsSync(destPath)) {
    fs.copyFileSync(srcPath, destPath);
  }
}

const viewports = [
  { name: '360', width: 360, height: 780 },
  { name: '768', width: 768, height: 1024 },
  { name: '1280', width: 1280, height: 850 },
  { name: '1920', width: 1920, height: 1080 }
];

async function run() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  console.log('🚀 Starting Review Screenshot & Accessibility Capture Suite...');

  // 1. Capture across viewports
  for (const vp of viewports) {
    await page.setViewportSize({ width: vp.width, height: vp.height });
    console.log(`\n📸 Capturing at ${vp.width}x${vp.height} (${vp.name}px)...`);

    // Public Portal
    await page.goto('http://127.0.0.1:5173/');
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(reviewDir, `public-portal-after-${vp.name}.png`), fullPage: false });

    // Open Dashboard / Internal View
    const launchBtn = page.locator('#btn-launch-command-center');
    if (await launchBtn.isVisible()) {
      await launchBtn.click();
      await page.waitForTimeout(1000);
    }

    // Dashboard Overview
    const dashTab = page.locator('#tab-btn-dashboard');
    if (await dashTab.isVisible()) {
      await dashTab.click();
      await page.waitForTimeout(1000);
    }
    await page.screenshot({ path: path.join(reviewDir, `dashboard-after-${vp.name}.png`), fullPage: false });

    // GIS Map
    const mapTab = page.locator('#tab-btn-map');
    if (await mapTab.isVisible()) {
      await mapTab.click();
      await page.waitForTimeout(1500);
      await page.screenshot({ path: path.join(reviewDir, `risk-map-after-${vp.name}.png`), fullPage: false });
    }

    // Work Orders
    const woTab = page.locator('#tab-btn-work_orders');
    if (await woTab.isVisible()) {
      await woTab.click();
      await page.waitForTimeout(1000);
      await page.screenshot({ path: path.join(reviewDir, `work-orders-after-${vp.name}.png`), fullPage: false });
    }

    // Traffic Heatmap
    const trafficTab = page.locator('#tab-btn-traffic');
    if (await trafficTab.isVisible()) {
      await trafficTab.click();
      await page.waitForTimeout(1000);
      await page.screenshot({ path: path.join(reviewDir, `traffic-after-${vp.name}.png`), fullPage: false });
    }

    // Audit Log (switch to admin)
    const roleSelect = page.locator('#role-select');
    if (await roleSelect.isVisible()) {
      await roleSelect.selectOption('admin');
      await page.waitForTimeout(500);
    }
    const auditTab = page.locator('#tab-btn-audit');
    if (await auditTab.isVisible()) {
      await auditTab.click();
      await page.waitForTimeout(1000);
      await page.screenshot({ path: path.join(reviewDir, `audit-after-${vp.name}.png`), fullPage: false });
    }
  }

  // 2. Run Accessibility Audit on 1280px Desktop
  await page.setViewportSize({ width: 1280, height: 850 });
  console.log('\n♿ Running Axe-Core WCAG 2.1 AA Accessibility Audit...');

  const viewsToAudit = [
    { name: 'Public Portal', url: 'http://127.0.0.1:5173/', setup: async () => {} },
    {
      name: 'Dashboard Overview',
      url: 'http://127.0.0.1:5173/',
      setup: async () => {
        const btn = page.locator('#btn-launch-command-center');
        if (await btn.isVisible()) await btn.click();
        const tab = page.locator('#tab-btn-dashboard');
        if (await tab.isVisible()) await tab.click();
      }
    },
    {
      name: 'GIS Risk Map',
      url: 'http://127.0.0.1:5173/',
      setup: async () => {
        const btn = page.locator('#btn-launch-command-center');
        if (await btn.isVisible()) await btn.click();
        const tab = page.locator('#tab-btn-map');
        if (await tab.isVisible()) await tab.click();
      }
    },
    {
      name: 'Work Orders Queue',
      url: 'http://127.0.0.1:5173/',
      setup: async () => {
        const btn = page.locator('#btn-launch-command-center');
        if (await btn.isVisible()) await btn.click();
        const tab = page.locator('#tab-btn-work_orders');
        if (await tab.isVisible()) await tab.click();
      }
    },
    {
      name: 'Traffic Analysis',
      url: 'http://127.0.0.1:5173/',
      setup: async () => {
        const btn = page.locator('#btn-launch-command-center');
        if (await btn.isVisible()) await btn.click();
        const tab = page.locator('#tab-btn-traffic');
        if (await tab.isVisible()) await tab.click();
      }
    },
    {
      name: 'Audit Trail',
      url: 'http://127.0.0.1:5173/',
      setup: async () => {
        const btn = page.locator('#btn-launch-command-center');
        if (await btn.isVisible()) await btn.click();
        const role = page.locator('#role-select');
        if (await role.isVisible()) await role.selectOption('admin');
        const tab = page.locator('#tab-btn-audit');
        if (await tab.isVisible()) await tab.click();
      }
    }
  ];

  const auditReport = [];

  for (const view of viewsToAudit) {
    await page.goto(view.url);
    await page.waitForTimeout(800);
    await view.setup();
    await page.waitForTimeout(1000);

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    const critical = results.violations.filter(v => v.impact === 'critical').length;
    const serious = results.violations.filter(v => v.impact === 'serious').length;
    const moderate = results.violations.filter(v => v.impact === 'moderate').length;
    const minor = results.violations.filter(v => v.impact === 'minor').length;
    const totalViolations = results.violations.length;
    const passedChecks = results.passes.length;

    // Score calculation based on ratio of passed rules to total rules evaluated
    const totalRules = passedChecks + totalViolations;
    const score = totalRules > 0 ? Math.round((passedChecks / totalRules) * 100) : 100;

    console.log(`  • ${view.name.padEnd(20)}: Score ${score}/100 | Passes: ${passedChecks}, Violations: ${totalViolations} (Crit: ${critical}, Ser: ${serious}, Mod: ${moderate}, Min: ${minor})`);

    auditReport.push({
      view: view.name,
      score,
      passedChecks,
      violations: totalViolations,
      critical,
      serious,
      moderate,
      minor,
      violationDetails: results.violations.map(v => ({ id: v.id, impact: v.impact, description: v.description }))
    });
  }

  const avgScore = Math.round(auditReport.reduce((acc, r) => acc + r.score, 0) / auditReport.length);
  console.log(`\n🏆 Overall Frontend Accessibility Score: ${avgScore}/100`);

  fs.writeFileSync(
    path.join(reviewDir, 'accessibility_audit.json'),
    JSON.stringify({ timestamp: new Date().toISOString(), avgScore, reports: auditReport }, null, 2)
  );

  await browser.close();
  console.log('✅ Capture & Audit Suite Completed successfully.');
}

run().catch(err => {
  console.error('Error running review capture suite:', err);
  process.exit(1);
});
