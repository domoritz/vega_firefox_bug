import os
import json

html = """
<!DOCTYPE html>
<html><head>
</head>
<body></body>
</html>
"""

code = """
class Wrapper {
  constructor(exprGenerator) {
    Object.defineProperty(this, 'foo', {
      enumerable: true,
      get: exprGenerator
    });
  }
}

const f = new Wrapper(() => "Hello World")

const done = arguments[1];
done(f);
"""

html_file = os.path.abspath("index.html")
with open(html_file, "w") as f:
    f.write(html)
url = f"file://{html_file}"

results = {}

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
        driver.get(url)
        output = driver.execute_async_script(code, {})
    finally:
        driver.close()

    print("-------------------------------")
    print(f"Full output for {driver_name}")
    print(json.dumps(output, indent=2))
    results[driver_name] = output
