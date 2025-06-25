# import asyncio
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

# async def main():
#     async with AsyncWebCrawler() as crawler:
#         result = await crawler.arun(
#             url="https://www.example.com",
#         )
#         print(result.markdown)  # Show the first 300 characters of extracted text

# if __name__ == "__main__":
#     asyncio.run(main())




# import asyncio
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

# async def main():
#     browser_conf = BrowserConfig(headless=False)  # or False to see the browser
#     run_conf = CrawlerRunConfig(
#         cache_mode=CacheMode.BYPASS
#     )

#     async with AsyncWebCrawler(config=browser_conf) as crawler:
#         result = await crawler.arun(
#             url="https://example.com",
#             config=run_conf
#         )
#         print(result.markdown)

# if __name__ == "__main__":
#     asyncio.run(main())


from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai import LLMConfig

# Generate a schema (one-time cost)
html = "<div class='product'><h2>Gaming Laptop</h2><span class='price'>$999.99</span></div>"

# Using OpenAI (requires API token)
# schema = JsonCssExtractionStrategy.generate_schema(
#     html,
#     llm_config = LLMConfig(provider="gemini/gemini-2.0-flash",api_token="AIzaSyC96ELnaWIN_3kHSzykc--ZISfgm04lVxI")  # Required for OpenAI
# )

# # Or using Ollama (open source, no token needed)
schema = JsonCssExtractionStrategy.generate_schema(
    html,
    llm_config = LLMConfig(provider="ollama/llama3.2:latest", api_token=None)  # Not needed for Ollama
)

# Use the schema for fast, repeated extractions
strategy = JsonCssExtractionStrategy(schema)

print("Generated Schema:")
print(schema)