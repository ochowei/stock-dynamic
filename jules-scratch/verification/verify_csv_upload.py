from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Navigate to the app
        page.goto("http://localhost:3001")

        # 2. Verify initial state
        expect(page.get_by_text("No data available. Please upload a CSV file to begin.")).to_be_visible()

        # 3. Upload CSV
        page.get_by_label("Upload CSV").set_input_files("stock-performance-visualizer/e2e/fixtures/test-data.csv")

        # 4. Verify charts are visible after upload
        expect(page.get_by_role("heading", name="Investment Return")).to_be_visible()
        expect(page.get_by_role("heading", name="Performance Indicators")).to_be_visible()
        expect(page.get_by_role("heading", name="KD Indicator")).to_be_visible()

        # 5. Take screenshot
        page.screenshot(path="jules-scratch/verification/verification.png")

        browser.close()

if __name__ == "__main__":
    run_verification()