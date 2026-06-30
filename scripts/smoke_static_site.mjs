import { spawn } from "node:child_process";
import { request } from "node:http";
import { chromium } from "@playwright/test";

const pages = [
  { path: "/", text: /Michelin Star Per-Capita Dashboard/i },
  { path: "/nz", text: /Hiakai|The Grove|Amisfield/i },
  { path: "/global-map", text: /Global Star Density Map/i, visualSelector: "svg" },
  { path: "/network", text: /Chef & Cuisine Influence Network/i, visualSelector: "svg" },
  { path: "/gdp-stars", text: /GDP & Stars Analysis/i, visualSelector: "svg" },
  { path: "/sources", text: /Restaurant-Level Records/i }
];

const port = Number(process.env.SMOKE_PORT || 4173);
const baseUrl = `http://127.0.0.1:${port}`;

function waitForServer(url, timeoutMs = 30_000) {
  const started = Date.now();

  return new Promise((resolve, reject) => {
    const check = () => {
      const req = request(url, { method: "HEAD" }, (res) => {
        res.resume();
        if (res.statusCode && res.statusCode < 500) {
          resolve();
          return;
        }
        retry();
      });

      req.on("error", retry);
      req.end();
    };

    const retry = () => {
      if (Date.now() - started > timeoutMs) {
        reject(new Error(`Timed out waiting for ${url}`));
        return;
      }
      setTimeout(check, 500);
    };

    check();
  });
}

const server = spawn(
  "npx",
  ["observable", "preview", "--host", "127.0.0.1", "--port", String(port)],
  { stdio: ["ignore", "pipe", "pipe"] }
);

let serverOutput = "";
server.stdout.on("data", (chunk) => {
  serverOutput += chunk.toString();
});
server.stderr.on("data", (chunk) => {
  serverOutput += chunk.toString();
});

try {
  await waitForServer(`${baseUrl}/`);

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  for (const item of pages) {
    const response = await page.goto(`${baseUrl}${item.path}`, {
      waitUntil: "networkidle"
    });

    if (!response || !response.ok()) {
      throw new Error(`${item.path} returned ${response?.status() ?? "no response"}`);
    }

    const bodyText = await page.locator("body").innerText({ timeout: 10_000 });
    if (bodyText.trim().length < 200) {
      throw new Error(`${item.path} rendered too little visible text`);
    }
    if (!item.text.test(bodyText)) {
      throw new Error(`${item.path} did not render expected analysis text`);
    }
    if (item.visualSelector) {
      await page.locator(item.visualSelector).first().waitFor({ timeout: 15_000 });
    }
  }

  await browser.close();
  console.log(`Smoke checked ${pages.length} static pages at ${baseUrl}`);
} catch (error) {
  console.error(serverOutput);
  throw error;
} finally {
  server.kill("SIGTERM");
}
