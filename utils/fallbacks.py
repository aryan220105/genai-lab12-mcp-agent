"""
Fallback content for when Gemini LLM is unavailable.
Provides pre-written cultural paragraphs, itineraries, and market summaries
so the app remains fully functional for demo/submission.
"""

from typing import List, Dict

# =====================================================================
# CULTURAL / HISTORIC PARAGRAPHS
# =====================================================================
CULTURAL_INFO = {
    "tokyo": (
        "Tokyo, Japan's bustling capital, seamlessly blends ultramodern innovation with "
        "deep-rooted tradition. Originally a small fishing village called Edo, it rose to "
        "prominence in 1603 when Tokugawa Ieyasu established his shogunate here, transforming "
        "it into the political center of Japan. Today, Tokyo is a city of contrasts — ancient "
        "Senso-ji Temple in Asakusa stands minutes from the neon-lit streets of Akihabara, "
        "while the serene Meiji Shrine is nestled in a lush forest just steps from the trendy "
        "Harajuku district. The city is renowned for its culinary excellence, holding more "
        "Michelin stars than any other city in the world. From the orderly chaos of Shibuya "
        "Crossing to the tranquil gardens of the Imperial Palace, Tokyo offers an unparalleled "
        "travel experience. Its efficient rail network, legendary hospitality (omotenashi), "
        "cherry blossom seasons, and vibrant pop culture — from anime to cutting-edge fashion — "
        "make it one of the most fascinating destinations on Earth."
    ),
    "udaipur": (
        "Udaipur, known as the 'City of Lakes' and the 'Venice of the East,' is one of India's "
        "most romantic and picturesque destinations. Founded in 1559 by Maharana Udai Singh II "
        "as the capital of the Mewar Kingdom, the city is steeped in Rajput history, valor, and "
        "artistic heritage. The magnificent City Palace, rising along the banks of Lake Pichola, "
        "is a stunning fusion of Rajasthani and Mughal architecture spanning 400 years of "
        "construction. The serene lakes — Pichola, Fateh Sagar, and Udai Sagar — create a "
        "magical atmosphere, especially at sunset when the Aravalli hills glow amber. Udaipur's "
        "narrow winding streets are filled with vibrant bazaars selling miniature paintings, "
        "silver jewelry, and traditional textiles. The city's cultural scene thrives with folk "
        "music and dance performances, while its cuisine — dal baati churma, gatte ki sabzi — "
        "reflects the rich flavors of Rajasthan. Often chosen as a filming location for its "
        "breathtaking beauty, Udaipur remains a jewel of Indian heritage tourism."
    ),
    "new york": (
        "New York City, often called 'The Big Apple,' is a global icon of culture, finance, and "
        "ambition. Founded as New Amsterdam by Dutch settlers in 1626, it became New York under "
        "British rule and grew into America's largest city and the world's financial capital. "
        "The Statue of Liberty, a gift from France in 1886, stands as a universal symbol of "
        "freedom and opportunity. Manhattan's skyline — defined by the Empire State Building, "
        "One World Trade Center, and countless skyscrapers — is one of the most recognizable "
        "in the world. Central Park offers 843 acres of green respite, while neighborhoods like "
        "Greenwich Village, Harlem, and Brooklyn each pulse with distinct character. Broadway "
        "theaters, world-class museums (The Met, MoMA, Guggenheim), and an unrivaled food scene "
        "spanning every cuisine on Earth make NYC a cultural powerhouse. Its subway runs 24/7, "
        "its energy never stops, and its diversity — with over 200 languages spoken — makes it "
        "truly the crossroads of the world."
    ),
    "london": (
        "London, the capital of the United Kingdom, is a city where nearly two millennia of "
        "history coexist with cutting-edge modernity. Founded as Londinium by the Romans in "
        "43 AD, it has survived plagues, fires, and wars to emerge as one of the world's "
        "most influential cities. The Tower of London, built by William the Conqueror in 1066, "
        "houses the Crown Jewels, while the Houses of Parliament and Big Ben define the city's "
        "iconic skyline along the Thames. London's cultural offerings are extraordinary — the "
        "British Museum, Tate Modern, and National Gallery are all free to enter. The city's "
        "West End rivals Broadway for theatrical excellence, and its music scene has produced "
        "legends from The Beatles to Adele. From the royal pageantry of Buckingham Palace to "
        "the eclectic energy of Camden Market, London blends tradition with innovation. Its "
        "diverse population, world-class universities, and position as a global financial hub "
        "make it a destination of endless discovery."
    ),
    "paris": (
        "Paris, the 'City of Light,' has captivated the world for centuries with its art, "
        "architecture, cuisine, and romance. Founded over 2,000 years ago as Lutetia by Celtic "
        "tribes, it became the heart of French civilization and European culture. The Eiffel "
        "Tower, built for the 1889 World's Fair, has become the universal symbol of France, "
        "while Notre-Dame Cathedral (dating to 1163) represents Gothic architecture at its "
        "finest. The Louvre, housing the Mona Lisa and 380,000 other works, is the world's "
        "most visited museum. Paris shaped the Enlightenment, the French Revolution, and modern "
        "art movements from Impressionism to Surrealism. The Champs-Élysées, Montmartre's "
        "artistic quarter, and the Latin Quarter's intellectual cafés each tell different "
        "stories of the city's rich tapestry. Parisian cuisine — from croissants and crêpes to "
        "Michelin-starred gastronomy — is integral to the UNESCO-recognized French culinary "
        "tradition. With its grand boulevards, hidden gardens, and timeless elegance, Paris "
        "continues to define sophistication and beauty."
    ),
}


def get_fallback_cultural_info(city: str) -> str:
    """Return a pre-written cultural paragraph for a city."""
    key = city.lower().strip()
    if key in CULTURAL_INFO:
        return CULTURAL_INFO[key]
    # Generic fallback
    return (
        f"{city} is a vibrant destination rich in culture, history, and unique experiences. "
        f"Visitors can explore its historic landmarks, taste authentic local cuisine, wander "
        f"through colorful markets, and immerse themselves in the traditions that define this "
        f"remarkable place. From ancient architecture to modern attractions, {city} offers "
        f"something for every traveler — whether you seek adventure, relaxation, spiritual "
        f"enrichment, or culinary discovery. The warmth of its people and the depth of its "
        f"heritage make {city} an unforgettable destination that rewards repeated visits."
    )


# =====================================================================
# DAY-BY-DAY ITINERARY
# =====================================================================
ITINERARIES = {
    "tokyo": """**Day 1: Arrival & Traditional Tokyo**
- Morning: Arrive at Narita/Haneda Airport. Transfer to hotel and freshen up.
- Afternoon: Visit **Senso-ji Temple** in Asakusa — Tokyo's oldest temple. Explore Nakamise Shopping Street for souvenirs and snacks.
- Evening: Walk to **Tokyo Skytree** for stunning sunset city views from 350m.
- Dining: Try ramen at a local Asakusa ramen shop.
- Tip: Get a Suica/Pasmo card at the airport for seamless train travel.

**Day 2: Modern Tokyo & Pop Culture**
- Morning: Explore **Meiji Shrine** and its forested grounds in Harajuku. Walk Takeshita Street for quirky fashion and crêpes.
- Afternoon: Head to **Shibuya Crossing** — the world's busiest intersection. Visit Shibuya Sky for panoramic views.
- Evening: Explore **Akihabara** — the electronics and anime capital. Browse multi-story arcades and manga shops.
- Dining: Conveyor belt sushi (kaiten-zushi) in Shibuya.

**Day 3: Culture & Gardens**
- Morning: Visit the **Imperial Palace East Gardens** (free entry, closed Mon/Fri). Beautiful traditional gardens.
- Afternoon: Explore **Ueno Park** — Tokyo National Museum, Ueno Zoo, and seasonal flowers.
- Evening: Shopping and dining in **Ginza** — Tokyo's upscale district.
- Dining: Try tempura or tonkatsu at a Ginza restaurant.

**Day 4: Day Trip & Markets**
- Morning: Take a day trip to **Tsukiji Outer Market** for the freshest sushi breakfast and street food.
- Afternoon: Visit **teamLab Borderless** (digital art museum) or explore **Odaiba** waterfront.
- Evening: Stroll through **Shinjuku** — visit the observation deck at Tokyo Metropolitan Government Building (free).
- Dining: Yakitori (grilled chicken skewers) in Shinjuku's Memory Lane (Omoide Yokocho).

**Day 5: Departure Day**
- Morning: Last-minute shopping at **Don Quijote** (24-hour store) or visit a local neighborhood.
- Afternoon: Head to the airport. Consider an ekiben (train bento) for the journey.
- Tip: Keep JPY coins for temple offerings and vending machines throughout your trip.""",

    "udaipur": """**Day 1: Arrival & Lake Pichola**
- Morning: Arrive in Udaipur. Check into hotel and freshen up.
- Afternoon: Take a boat ride on **Lake Pichola** — visit Jag Mandir island palace.
- Evening: Watch the sunset from **Ambrai Ghat** with stunning views of City Palace and Lake Palace.
- Dining: Rooftop dinner at Ambrai Restaurant overlooking the lake.
- Tip: Carry sunscreen and stay hydrated — Rajasthan can be very warm.

**Day 2: Palaces & Heritage**
- Morning: Explore **City Palace** — the majestic complex with museums, courtyards, and lake views (allow 3-4 hours).
- Afternoon: Visit **Jagdish Temple** — beautiful Indo-Aryan temple dedicated to Lord Vishnu, just outside City Palace.
- Evening: Attend a traditional **Rajasthani folk dance and music show** at Bagore Ki Haveli.
- Dining: Try dal baati churma and gatte ki sabzi at a local Rajasthani restaurant.

**Day 3: Gardens, Lakes & Departure**
- Morning: Visit **Saheliyon-ki-Bari** (Garden of the Maidens) — beautiful fountains and marble elephants.
- Afternoon: Drive to **Fateh Sagar Lake** and visit Nehru Garden island. Explore the surrounding hills.
- Evening: Last shopping at Hathi Pol bazaar for miniature paintings, silver jewelry, and textiles.
- Dining: Farewell dinner with a view of the illuminated City Palace.
- Tip: Bargain respectfully at bazaars — starting at 50% of asking price is normal.""",
}


def get_fallback_itinerary(city: str, from_city: str, start_date: str, end_date: str,
                           travelers: int, budget: str, preferences: str,
                           attractions: List[str]) -> str:
    """Return a pre-written itinerary, or generate a generic one."""
    key = city.lower().strip()
    if key in ITINERARIES:
        return ITINERARIES[key]

    # Generic itinerary
    att_text = ""
    for i, att in enumerate(attractions[:6]):
        att_text += f"  - {att}\n"

    return f"""**Day 1: Arrival & Orientation**
- Morning: Arrive in {city} from {from_city}. Transfer to hotel and check in.
- Afternoon: Take a walking tour of the city center to get oriented. Visit a local café.
- Evening: Explore the main market area and try local street food.
- Dining: Traditional local restaurant near your hotel.

**Day 2: Major Attractions**
- Morning: Visit the top-rated attractions:
{att_text}- Afternoon: Continue exploring cultural and historic sites. Take photos and enjoy the atmosphere.
- Evening: Relax at a scenic viewpoint or waterfront area.
- Dining: Try the city's signature dish at a well-reviewed restaurant.

**Day 3: Culture & Shopping**
- Morning: Visit a local museum or art gallery. Learn about the region's history.
- Afternoon: Shopping for souvenirs and local crafts. Explore hidden neighborhoods.
- Evening: Farewell dinner at a rooftop or scenic restaurant.

**Day 4: Departure**
- Morning: Last-minute sightseeing or shopping.
- Afternoon: Transfer to airport/station for departure.
- Tip: Keep local currency for small purchases and tips throughout your trip.

*Budget: {budget} | Travelers: {travelers} | Dates: {start_date} to {end_date}*
*Preferences: {preferences if preferences else "General sightseeing"}*"""


# =====================================================================
# MARKET SUMMARIES
# =====================================================================
MARKET_SUMMARIES = {
    "japan": (
        "Japan's financial market is one of the largest and most sophisticated in Asia. "
        "The official currency is the Japanese Yen (JPY), managed by the Bank of Japan. "
        "The Tokyo Stock Exchange (TSE), established in 1878, is the third-largest stock "
        "exchange globally by market capitalization. Its primary index, the **Nikkei 225**, "
        "tracks 225 major companies including Toyota, Sony, and SoftBank, while the **TOPIX** "
        "index covers all First Section companies. Japan is the world's third-largest economy "
        "by GDP and a major global exporter of automobiles, electronics, and machinery. "
        "The JPY is considered a safe-haven currency, often strengthening during global "
        "economic uncertainty. Japan's monetary policy, characterized by historically low "
        "interest rates, significantly influences Asian and global financial markets."
    ),
    "india": (
        "India's financial market has experienced remarkable growth, making it one of the "
        "most dynamic emerging markets globally. The official currency is the Indian Rupee (INR), "
        "regulated by the Reserve Bank of India. The **Bombay Stock Exchange (BSE)**, "
        "established in 1875, is Asia's oldest exchange, with its flagship **SENSEX** index "
        "tracking 30 major companies. The **National Stock Exchange (NSE)**, founded in 1992, "
        "operates the widely-followed **NIFTY 50** index. India ranks as the world's fifth-largest "
        "economy by GDP, driven by IT services, pharmaceuticals, and a massive consumer market "
        "of 1.4 billion people. Key listed companies include Reliance Industries, TCS, Infosys, "
        "and HDFC Bank. India's growing middle class and digital economy continue to attract "
        "significant foreign institutional investment."
    ),
    "united states": (
        "The United States hosts the world's largest and most influential financial markets. "
        "The US Dollar (USD) serves as the world's primary reserve currency. The **New York "
        "Stock Exchange (NYSE)**, founded in 1792, is the world's largest exchange by market "
        "capitalization. The **NASDAQ**, established in 1971, is the second-largest and heavily "
        "weighted toward technology companies. Key indices include the **S&P 500** (500 large-cap "
        "companies), **Dow Jones Industrial Average** (30 blue-chip stocks), and **NASDAQ "
        "Composite**. The US markets set the tone for global trading, with companies like "
        "Apple, Microsoft, Amazon, and Nvidia among the most valuable in the world. The Federal "
        "Reserve's monetary policy decisions have far-reaching global implications."
    ),
    "south korea": (
        "South Korea's financial market reflects its status as Asia's fourth-largest economy. "
        "The official currency is the South Korean Won (KRW), overseen by the Bank of Korea. "
        "The **Korea Exchange (KRX)**, headquartered in Busan, operates the **KOSPI** index "
        "(tracking all common stocks) and the **KOSDAQ** (focused on tech and small-cap firms). "
        "South Korea is a global leader in semiconductors, shipbuilding, automobiles, and "
        "electronics, with Samsung Electronics, SK Hynix, and Hyundai Motor among its largest "
        "listed companies. The country's export-driven economy and strong technology sector "
        "make it an important barometer for global trade and tech industry health."
    ),
    "china": (
        "China operates the world's second-largest stock market by total capitalization. "
        "The official currency is the Chinese Yuan/Renminbi (CNY), managed by the People's "
        "Bank of China. Major exchanges include the **Shanghai Stock Exchange (SSE)**, "
        "**Shenzhen Stock Exchange (SZSE)**, and the **Hong Kong Stock Exchange (HKEX)**. "
        "The SSE Composite Index and Hang Seng Index are closely watched global indicators. "
        "China's economy, the world's second-largest by GDP, is driven by manufacturing, "
        "technology, and an enormous domestic consumer market. Major listed companies include "
        "Alibaba, Tencent, ICBC, and PetroChina. The gradual internationalization of the "
        "Yuan and China's Belt and Road Initiative continue to reshape global financial flows."
    ),
    "united kingdom": (
        "The United Kingdom is one of the world's leading financial centers, anchored by "
        "London's City and Canary Wharf districts. The official currency is the British "
        "Pound Sterling (GBP), one of the oldest and most traded currencies globally, "
        "managed by the Bank of England (est. 1694). The **London Stock Exchange (LSE)**, "
        "founded in 1801, is Europe's largest exchange. Its primary index, the **FTSE 100**, "
        "tracks the 100 largest companies by market cap, including Shell, AstraZeneca, HSBC, "
        "and Unilever. The **FTSE 250** covers mid-cap firms. London's financial services "
        "sector contributes significantly to the UK's GDP, and the city serves as a global "
        "hub for foreign exchange trading, insurance (Lloyd's), and asset management."
    ),
}


def get_fallback_market_summary(country: str, currency_name: str = "",
                                 index_names: List[str] = None) -> str:
    """Return a pre-written market summary for a country."""
    key = country.lower().strip()
    if key in MARKET_SUMMARIES:
        return MARKET_SUMMARIES[key]
    return (
        f"{country}'s financial market features the {currency_name or 'local currency'} as its "
        f"official currency. The country's stock exchanges and major indices "
        f"({', '.join(index_names) if index_names else 'N/A'}) play an important role in the "
        f"regional and global financial landscape. Investors monitor these markets for insights "
        f"into the country's economic health, trade dynamics, and growth prospects."
    )
