import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';

const screenshotDir = path.resolve('/Users/jiteshvishnoi/.gemini/antigravity-ide/brain/16afb82e-acaa-423e-9520-34e126c2a5e2/screenshots');
if (!fs.existsSync(screenshotDir)) {
  fs.mkdirSync(screenshotDir, { recursive: true });
}

async function run() {
  console.log('Launching browser for Loop 7 capture...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  // 1. Map View with Demo Control Panel
  console.log('1. Capturing GIS Map View with Demo Controls...');
  await page.goto('http://127.0.0.1:5173/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  
  // Click first marker
  const markers = await page.$$('.custom-issue-icon');
  if (markers.length > 0) {
    await markers[0].click();
    await page.waitForTimeout(800);
  }
  await page.screenshot({ path: path.join(screenshotDir, '1_gis_map_view.png'), fullPage: false });

  // 2. Click Bytes vs Video Analysis Modal
  console.log('2. Capturing Bytes vs Video Comparison Modal...');
  await page.click('#btn-bytes-modal');
  await page.waitForTimeout(1000);
  await page.screenshot({ path: path.join(screenshotDir, '6_bytes_comparison_modal.png'), fullPage: false });
  await page.click('#bytes-modal-close-btn');
  await page.waitForTimeout(600);

  // 3. Trigger Pass 2 Corroboration
  console.log('3. Triggering Pass 2 Corroboration...');
  await page.click('#btn-pass-2');
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path.join(screenshotDir, '7_pass2_corroboration.png'), fullPage: false });

  // 4. Trigger Offline Caching Simulation
  console.log('4. Triggering Offline Caching...');
  await page.click('#btn-toggle-offline');
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(screenshotDir, '8_offline_caching.png'), fullPage: false });
  await page.click('#btn-toggle-offline');
  await page.waitForTimeout(1000);

  // 5. Work Orders Queue
  console.log('5. Capturing Work Orders Queue...');
  await page.click('#tab-btn-work_orders');
  await page.waitForTimeout(1000);
  await page.screenshot({ path: path.join(screenshotDir, '2_work_orders_approved.png'), fullPage: false });

  console.log('All Loop 7 screenshots captured successfully in:', screenshotDir);
  await browser.close();
}

run().catch((err) => {
  console.error('Screenshot capture failed:', err);
  process.exit(1);
});
