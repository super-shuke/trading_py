import asyncio  # 必须导入 asyncio
from fake_useragent import UserAgent
from playwright.async_api import async_playwright


class TrainingPy:
    def __init__(self):
        self.ua = UserAgent()

    async def get_scrape_movie(self, url: str):

        async with async_playwright() as p:
            # 1. 启动浏览器，但要隐藏自动化特征
            browser = await p.chromium.launch(
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",  # 【关键】移除自动化特征
                    "--no-sandbox",
                    "--disable-infobars",
                ],
            )
            context = await browser.new_context(
                user_agent=self.ua.random,  # 使用随机用户代理
                viewport={"width": 1280, "height": 800},
                locale="zh-CN",
                timezone_id="America/New_York",
            )
            page = await context.new_page()

            try:
                #  访问页面
                await page.goto(
                    url,
                    wait_until="networkidle",
                    timeout=60000,
                )
                await page.locator("body").first.is_visible()

                print(f"Successfully loaded page: {url}")
                await page.get_by_role("link").nth(1).click()

                print(f"Captured XHR response123123")
            except Exception as e:
                print(f"Failed to load page: {e}")


# === 这才是运行程序的入口 ===
async def main():
    spider = TrainingPy()
    # 调用你的方法
    await spider.get_scrape_movie("https://ssr1.scrape.center/")


if __name__ == "__main__":
    # 运行异步事件循环
    asyncio.run(main())
