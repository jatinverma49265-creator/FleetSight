import { chromium } from 'playwright';

async function runTests() {
  console.log('=== Running Playwright Browser E2E Test Suite ===');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  let passed = 0;
  let failed = 0;

  async function test(name, fn) {
    try {
      process.stdout.write(`• ${name}... `);
      await fn();
      console.log('PASSED ✓');
      passed++;
    } catch (err) {
      console.log(`FAILED ✗\n  Error: ${err.message}`);
      failed++;
    }
  }

  // 1. Initial Page Load (Public Portal & DPDP Charter)
  await test('Public Portal loads with brand title, MoRTH statistics, and DPDP charter', async () => {
    await page.goto('http://127.0.0.1:5173/', { waitUntil: 'networkidle' });
    const title = await page.textContent('header');
    if (!title.includes('FleetSight')) throw new Error('Brand title not found in header');
    const bodyText = await page.textContent('body');
    if (!bodyText.includes('4,61,312') || !bodyText.includes('DPDP')) {
      throw new Error('MoRTH statistics or DPDP charter not rendered on portal');
    }
  });

  // 2. Leaflet Map Markers & Detail Drawer
  await test('GIS Map renders markers and opens Detail Drawer on click', async () => {
    await page.click('#tab-btn-map');
    await page.waitForTimeout(600);
    const markers = await page.$$('.custom-issue-icon');
    if (markers.length === 0) throw new Error('No issue markers rendered on Leaflet map');
    await markers[0].click();
    await page.waitForTimeout(500);
    const drawer = await page.$('#issue-detail-drawer');
    if (!drawer) throw new Error('Detail drawer not visible after marker click');
    const scoreText = await drawer.textContent();
    if (!scoreText.includes('Explainable Priority Score')) throw new Error('Priority score not in drawer');
  });

  // 3. Work Orders Queue & Engineer Workflow
  await test('Work Orders Queue allows PWD Engineer to approve and assign', async () => {
    await page.click('#tab-btn-work_orders');
    await page.waitForTimeout(600);
    await page.selectOption('#role-select', 'engineer');
    await page.waitForTimeout(300);
    await page.click('#btn-approve-wo');
    await page.waitForTimeout(800);
    const text = await page.textContent('body');
    if (!text.includes('Successfully transitioned') && !text.includes('ASSIGNED')) {
      throw new Error('Approval confirmation banner did not appear');
    }
  });

  // 4. RBAC 403 Access Denial Enforcement
  await test('Public Viewer role is denied Work Order modification (403 Modal)', async () => {
    await page.selectOption('#role-select', 'viewer');
    await page.waitForTimeout(300);
    await page.click('#btn-approve-wo');
    await page.waitForTimeout(500);
    const modal = await page.$('#rbac-denial-modal');
    if (!modal) throw new Error('RBAC Denial Modal did not appear for viewer role');
    const modalText = await modal.textContent();
    if (!modalText.includes('RBAC Access Denied')) throw new Error('Modal text missing denial header');
    await page.click('#rbac-modal-close-btn');
    await page.waitForTimeout(300);
  });

  // 5. Traffic Heatmap Tab & Chart
  await test('Traffic Heatmap renders corridor time-series chart and segment metrics', async () => {
    await page.click('#tab-btn-traffic');
    await page.waitForTimeout(800);
    const pageContent = await page.textContent('body');
    if (!pageContent.includes('Corridor Traffic Congestion')) throw new Error('Traffic header missing');
    if (!pageContent.includes('MI Road') || !pageContent.includes('Tonk Road')) {
      throw new Error('Corridor segments missing in traffic view');
    }
  });

  // 6. Audit Trail RBAC Protection
  await test('Audit Trail is restricted to Admin & Police roles', async () => {
    // With role = viewer: Access Denied banner
    await page.selectOption('#role-select', 'viewer');
    await page.click('#tab-btn-audit');
    await page.waitForTimeout(500);
    let content = await page.textContent('body');
    if (!content.includes('RBAC Access Denied: 403 Forbidden')) {
      throw new Error('Viewer was not blocked from Audit Trail');
    }

    // With role = admin: Full Audit Table
    await page.selectOption('#role-select', 'admin');
    await page.waitForTimeout(600);
    content = await page.textContent('body');
    if (!content.includes('Immutable Compliance & Operational Audit Trail')) {
      throw new Error('Admin could not view Audit Table');
    }
  });

  console.log(`\n========================================`);
  console.log(`E2E Summary: ${passed} Passed, ${failed} Failed`);
  console.log(`========================================\n`);

  await browser.close();

  if (failed > 0) {
    process.exit(1);
  }
}

runTests().catch((err) => {
  console.error('Fatal Playwright runner error:', err);
  process.exit(1);
});
