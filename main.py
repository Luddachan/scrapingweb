from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# =========================
# CONFIG
# =========================
BASE_URL = "https://mydramalist.com"
START_URL = "https://mydramalist.com/search?adv=titles&ty=68,86&co=1,6&th=1045&so=rated"
MAX_RESULTS = 1000
RESULTS_PER_PAGE = 20
MAX_PAGES = MAX_RESULTS // RESULTS_PER_PAGE  # 250
OUTPUT_FILE = "mdl_bl_top_rated.csv"

# =========================
# SELENIUM SETUP
# =========================
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

# =========================
# COOKIE CONSENT
# =========================
def accept_cookies(driver):
    try:
        time.sleep(3)
        for b in driver.find_elements(By.TAG_NAME, "button"):
            if "accept" in b.text.lower():
                b.click()
                print("🍪 Cookie accettati")
                time.sleep(2)
                break
    except:
        pass

# =========================
# START
# =========================
results = []
seen_urls = set()
rank = 1

for page in range(1, MAX_PAGES + 1):
    if len(results) >= MAX_RESULTS:
        break

    page_url = f"{START_URL}&page={page}"
    print(f"\n📄 Pagina {page}/{MAX_PAGES} — Totale raccolti: {len(results)}")

    driver.get(page_url)
    accept_cookies(driver)

    # ⏳ attendi che almeno un titolo sia visibile
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h6.title a")))
    except:
        print("❌ Timeout: titoli non trovati")
        break

    soup = BeautifulSoup(driver.page_source, "html.parser")
    title_links = soup.select("h6.title a")

    if not title_links:
        print("⛔ Nessun titolo in questa pagina")
        break

    for a in title_links:
        if len(results) >= MAX_RESULTS:
            break

        href = a.get("href")
        if not href:
            continue

        url = BASE_URL + href
        if url in seen_urls:
            continue
        seen_urls.add(url)

        title = a.get_text(strip=True)

        # 🔍 risale al contenitore per meta info
        container = a.find_parent("div")
        meta = container.find("span", class_="text-muted") if container else None

        year, country = "", ""
        if meta:
            parts = meta.get_text(" ", strip=True).split("•")
            if len(parts) >= 1:
                year = parts[0].strip()
            if len(parts) >= 2:
                country = parts[1].strip()

        rating = ""
        score = container.find("span", class_="score") if container else None
        if score:
            rating = score.get_text(strip=True)

        print(f"➡️ {rank}. {title}")

        # =========================
        # OPEN DETAIL PAGE
        # =========================
        driver.execute_script("window.open(arguments[0]);", url)
        driver.switch_to.window(driver.window_handles[1])

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.box-body")))
        except:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue

        detail = BeautifulSoup(driver.page_source, "html.parser")

        def get_stat(label):
            tag = detail.find("span", string=label)
            if tag:
                val = tag.find_next_sibling("span")
                return val.get_text(strip=True) if val else ""
            return ""

        watchers = get_stat("Watchers")
        favorites = get_stat("Favorites")
        episodes = get_stat("Episodes")

        genres = ", ".join(
            g.get_text(strip=True)
            for g in detail.select("a[href*='/genres/']")
        )

        synopsis_tag = detail.select_one("span#show-more-text")
        synopsis = synopsis_tag.get_text(" ", strip=True) if synopsis_tag else ""

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        results.append({
            "rank": rank,
            "title": title,
            "year": year,
            "country": country,
            "rating": rating,
            "watchers": watchers,
            "favorites": favorites,
            "episodes": episodes,
            "genres": genres,
            "synopsis": synopsis,
            "url": url
        })

        rank += 1

    time.sleep(2)  # pausa gentile tra le pagine

driver.quit()

# =========================
# SAVE CSV
# =========================
df = pd.DataFrame(results)
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("\n✅ SCRAPING COMPLETATO")
print(f"📁 File: {OUTPUT_FILE}")
print(f"📊 Totale righe: {len(df)}")
