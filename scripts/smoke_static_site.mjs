import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import { createServer } from "node:http";
import path from "node:path";
import { chromium } from "@playwright/test";

const pages = [
  { path: "/", text: "Michelin Star Per-Capita Dashboard" },
  { path: "/nz", text: "New Zealand Records", visualSelector: "svg" },
  { path: "/global-map", text: "Restaurant Location Map", visualSelector: "svg" },
  { path: "/network", text: "Cuisine And Country Network", visualSelector: "svg" },
  { path: "/gdp-stars", text: "GDP & Stars Analysis", visualSelector: "svg" },
  { path: "/pivot", text: "Pivot Results", visualSelector: "svg" },
  { path: "/sources", text: "Restaurant-Level Records" }
];

const mimeTypes = new Map([
  [".css", "text/css; charset=utf-8"],
  [".html", "text/html; charset=utf-8"],
  [".js", "text/javascript; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".parquet", "application/octet-stream"],
  [".svg", "image/svg+xml"]
]);

const port = Number(process.env.SMOKE_PORT || 4173);
const baseUrl = `http://127.0.0.1:${port}`;
const distRoot = path.resolve("dist");
const launchOptions = { headless: true };
if (process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH) {
  launchOptions.executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
}
if (process.env.PLAYWRIGHT_BROWSER_CHANNEL) {
  launchOptions.channel = process.env.PLAYWRIGHT_BROWSER_CHANNEL;
}

function distPathForRequest(requestUrl) {
  const url = new URL(requestUrl, baseUrl);
  const decodedPath = decodeURIComponent(url.pathname);
  const cleanPath = decodedPath === "/" ? "/index.html" : decodedPath;
  const candidate = path.resolve(distRoot, `.${cleanPath}`);
  if (!candidate.startsWith(distRoot)) {
    return null;
  }
  if (path.extname(candidate)) {
    return candidate;
  }
  return `${candidate}.html`;
}

const server = createServer(async (req, res) => {
  const filePath = distPathForRequest(req.url ?? "/");
  if (!filePath) {
    res.writeHead(400);
    res.end("Bad request");
    return;
  }

  try {
    const fileStat = await stat(filePath);
    if (!fileStat.isFile()) {
      throw new Error("Not a file");
    }
    res.writeHead(200, {
      "content-length": fileStat.size,
      "content-type": mimeTypes.get(path.extname(filePath)) ?? "application/octet-stream"
    });
    if (req.method === "HEAD") {
      res.end();
      return;
    }
    createReadStream(filePath).pipe(res);
  } catch {
    res.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
    res.end("Not found");
  }
});

let browser;
try {
  await new Promise((resolve) => server.listen(port, "127.0.0.1", resolve));

  browser = await chromium.launch(launchOptions);
  const page = await browser.newPage();
  page.setDefaultTimeout(15_000);

  for (const item of pages) {
    const response = await page.goto(`${baseUrl}${item.path}`, {
      timeout: 30_000,
      waitUntil: "domcontentloaded"
    });

    if (!response || !response.ok()) {
      throw new Error(`${item.path} returned ${response?.status() ?? "no response"}`);
    }

    await page.getByText(item.text).first().waitFor();
    const bodyText = await page.locator("body").innerText({ timeout: 10_000 });
    if (bodyText.trim().length < 200) {
      throw new Error(`${item.path} rendered too little visible text`);
    }
    if (item.visualSelector) {
      await page.waitForFunction(
        (selector) =>
          Array.from(document.querySelectorAll(selector)).some((element) => {
            const bounds = element.getBoundingClientRect();
            return bounds.width >= 100 && bounds.height >= 100;
          }),
        item.visualSelector,
        { timeout: 15_000 }
      );
    }
  }

  console.log(`Smoke checked ${pages.length} static pages at ${baseUrl}`);
} finally {
  await browser?.close();
  await new Promise((resolve, reject) => {
    server.close((error) => (error ? reject(error) : resolve()));
  });
}
