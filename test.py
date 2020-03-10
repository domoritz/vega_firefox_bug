import json

code = """
class Wrapper {
  constructor(generator) {
    Object.defineProperty(this, 'foo', {
      enumerable: true,
      get: generator
    });
  }
}

const f = new Wrapper(() => "Hello World")

const done = arguments[1];
done(f);
"""

for driver_name in ["chrome", "firefox"]:
    if driver_name == "firefox":
        from selenium.webdriver import Firefox as Driver
        from selenium.webdriver.firefox.options import Options
    else:
        from selenium.webdriver import Chrome as Driver
        from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--headless")
    driver = Driver(options=options)
    try:
        driver.get('about:blank')
        output = driver.execute_async_script(code, {})
    finally:
        driver.close()

    print("-------------------------------")
    print(f"Full output for {driver_name}")
    print(json.dumps(output, indent=2))
