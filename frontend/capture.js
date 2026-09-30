import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';

const screenshotDir = path.resolve('/Users/jiteshvishnoi/.gemini/antigravity-ide/brain/16afb82e-acaa-423e-9520-34e126c2a5e2/screenshots');
if (!fs.existsSync(screenshotDir)) {
  fs.mkdirSync(screenshotDir, { recursive: true });
}

async function run() {
  console.log('Launching browser for dashboard capture...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  // 1. Map View
  console.log('1. Capturing GIS Map View...');
  await page.goto('http://127.0.0.1:5173/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  
  // Click first marker if available
  const markers = await page.$$('.custom-issue-icon');
  if (markers.length > 0) {
    await markers[0].click();
    await page.waitForTimeout(1000);
  }
  await page.screenshot({ path: path.join(screenshotDir, '1_gis_map_view.png'), fullPage: false });

  // 2. Work Orders Tab - Engineer Action
  console.log('2. Capturing Work Orders Queue & Engineer Approval...');
  await page.click('#tab-btn-work_orders');
  await page.waitForTimeout(1000);
  await page.click('#btn-approve-wo');
  await page.waitForTimeout(1000);
  await page.screenshot({ path: path.join(screenshotDir, '2_work_orders_approved.png'), fullPage: false });

  // 3. RBAC Denial - Viewer role attempt
  console.log('3. Capturing RBAC Denial Modal...');
  await page.selectOption('#role-select', 'viewer');
  await page.waitForTimeout(500);
  await page.click('#btn-approve-wo');
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(screenshotDir, '3_rbac_denial_modal.png'), fullPage: false });
  await page.click('#rbac-modal-close-btn');
  await page.waitForTimeout(500);

  // 4. Traffic Heatmap Tab
  console.log('4. Capturing Traffic Corridor Heatmap...');
  await page.click('#tab-btn-traffic');
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(screenshotDir, '4_traffic_heatmap.png'), fullPage: false });

  // 5. Audit Trail Tab (Switch to Admin)
  console.log('5. Capturing Audit Trail...');
  await page.selectOption('#role-select', 'admin');
  await page.waitForTimeout(500);
  await page.click('#tab-btn-audit');
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path.join(screenshotDir, '5_audit_trail.png'), fullPage: false });

  console.log('All screenshots captured successfully in:', screenshotDir);
  await browser.close();
}

run().catch((err) => {
  console.error('Screenshot capture failed:', err);
  process.exit(1);
});
