"""
seed.py
───────
Migrates the hardcoded `experiences`, `festivals`, and `circles` arrays
(and their embedded reviews) from AtithiSetu.html's <script> block into
PostgreSQL. After this runs, the database — not the HTML file — is the
source of truth for catalog data.

The data below was copied by hand from the frontend's JS `experiences`,
`festivals`, and `circles` consts, field for field. Image values are
the raw Wikimedia Commons filenames used by the frontend's own pic()
helper, so they'll work unchanged once the frontend switches to reading
from the API.

Run with:
    python seed.py
"""

import sys

from database import SessionLocal, engine, Base
import models

# Make sure the tables exist before we try to insert into them.
Base.metadata.create_all(bind=engine)


# ─────────────────────────── Source data ───────────────────────────

EXPERIENCES = [
    {
        "id": "exp7", "title": "Tea-slope mornings above Munnar", "city": "Munnar",
        "location": "Chinnakanal, Idukki, Kerala", "interests": ["community", "food"],
        "price_label": "₹1,900 / person", "rating": 4.8, "review_count": 26,
        "image": "Hill View (Munnar - Kerala).jpg",
        "gallery": ["Munnar Overview.jpg", "Western Ghats Kerala.jpg", "Western-Ghats-Matheran.jpg"],
        "date_label": "September – March · 6:00 AM", "people_label": "2–6 guests", "duration_label": "Half day",
        "tags": ["Tea picking", "Shola forest walk", "Estate kitchen", "Cardamom hills"],
        "host_name": "Sheeba Thomas", "host_since": "2022", "host_langs": "Malayalam, Tamil, English",
        "host_bio": "Sheeba's family has worked these slopes for three generations. She picks with the morning "
                    "shift, then cooks lunch for guests in the estate quarters where she grew up.",
        "description": "Above Munnar the hills are cut into terraces so old the bushes have gone woody, and the "
                        "mist sits in the valleys until nine. You pick with the morning shift — two leaves and a "
                        "bud, and Sheeba will tell you kindly that you are doing it wrong — then walk into a patch "
                        "of shola forest that has never been cleared. Lunch is kappa, meen curry and black tea "
                        "from the leaf you helped bring in.",
        "plan": [
            "6:00 AM · walk up to the terraces while the mist is still in the valley",
            "6:45 AM · picking with the morning shift, two leaves and a bud",
            "8:30 AM · breakfast of puttu and kadala in the estate quarters",
            "10:00 AM · shola forest walk — endemic birds, cardamom, wild pepper",
            "12:30 PM · kappa and meen curry cooked by Sheeba",
            "2:00 PM · tasting the estate's tea grades, from dust to orthodox leaf",
        ],
        "included": ["Picking basket and apron", "Breakfast and lunch", "Forest walk with a local guide",
                      "100g of estate tea to take home"],
        "bring": ["Shoes for wet grass", "A jacket — it is cold until the sun clears the ridge"],
        "reviews": [
            {"reviewer_name": "Deepa R.", "reviewer_city": "Chennai", "stars": 5,
             "text": "I have driven past those slopes a hundred times. Walking them with someone who works them "
                     "is a completely different thing."},
            {"reviewer_name": "Nils P.", "reviewer_city": "Oslo", "stars": 5,
             "text": "The forest walk was the surprise. Sheeba named every bird before I could raise the "
                     "binoculars."},
        ],
    },
    {
        "id": "exp6", "title": "Umngot river mornings in Shnongpdeng", "city": "Shnongpdeng",
        "location": "Shnongpdeng, West Jaintia Hills, Meghalaya", "interests": ["community", "heritage"],
        "price_label": "₹2,100 / person", "rating": 4.9, "review_count": 18,
        "image": "Umngot river, Dawki.jpg",
        "gallery": ["Umngot river, Dawki.jpg", "Dawki Bridge and Umngot River.jpg",
                     "Living root bridges, Nongriat village, Meghalaya.jpg"],
        "date_label": "October – April · 5:30 AM", "people_label": "2–6 guests",
        "duration_label": "Full day + optional camp",
        "tags": ["Clear-water boating", "Khasi home cooking", "River camp", "Village walk"],
        "host_name": "Banri Nongrum", "host_since": "2021", "host_langs": "Khasi, English, Hindi",
        "host_bio": "Banri grew up fifty metres from the Umngot. Her father still fishes it and her brothers run "
                    "the boats. She hosts guests in the family home above the river and cooks the meals herself.",
        "description": "Shnongpdeng sits on the Umngot, one of India's clearest rivers — in winter the water goes "
                        "so glassy that the boats look like they are floating on air, and you can count the "
                        "stones four metres down. You'll push off before the sun clears the ridge, when the "
                        "surface is still and the light comes in sideways, then come back to Banri's kitchen for "
                        "jadoh and tungrymbai. The afternoon is yours for the rope bridge, the cliff jump or "
                        "nothing at all, and you can stay the night in a riverside tent if you want the stars.",
        "plan": [
            "5:30 AM · walk down to the jetty with the family for first light",
            "6:00 AM · dugout boat over the clear stretch below the rapids",
            "8:30 AM · breakfast of red rice and river fish at the family home",
            "11:00 AM · village walk — betel groves, the church, the old suspension bridge",
            "1:30 PM · jadoh, tungrymbai and doh-khleh cooked with Banri",
            "4:00 PM · free water time: snorkelling, cliff jump or kayak",
            "Optional · riverside tent, bonfire and Khasi songs after dark",
        ],
        "included": ["Boat and life jackets", "All meals with the family", "Village guide",
                      "Tent and bedding if you stay over"],
        "bring": ["A change of clothes", "Shoes with grip for the rocks", "Warm layer for the pre-dawn boat"],
        "reviews": [
            {"reviewer_name": "Meera J.", "reviewer_city": "Bengaluru", "stars": 5,
             "text": "The water really is that clear — but the part I remember is Banri's mother teaching me to "
                     "fold the banana leaf."},
            {"reviewer_name": "Owen T.", "reviewer_city": "Bristol", "stars": 5,
             "text": "Camped by the river. The boats at dawn, the bonfire, the songs. Cheapest and best two days "
                     "of the whole trip."},
        ],
    },
    {
        "id": "exp1", "title": "Ganesh Chaturthi with the Kumar family", "city": "Mumbai",
        "location": "Dadar, Mumbai", "interests": ["festivals", "food"],
        "price_label": "₹2,400 / person", "rating": 4.9, "review_count": 34,
        "image": "Anant Chaturdashi.jpg",
        "gallery": ["Mumbai 03-2016 30 Gateway of India.jpg", "Anant Chaturdashi.jpg",
                     "Chandni Chowk Road, Delhi (43802533965).jpg"],
        "date_label": "7 September · 7:30 AM", "people_label": "2–8 guests", "duration_label": "Full day",
        "tags": ["Festival ritual", "Home cooking", "Street procession", "Visarjan"],
        "host_name": "Rajesh Kumar", "host_since": "2018", "host_langs": "Marathi, Hindi, English",
        "host_bio": "A third-generation Ganesh Chaturthi organiser for his Dadar chawl. Rajesh has been opening "
                    "his home to travellers since 2018 — the puja, the kitchen, the procession, all of it.",
        "description": "Wake at dawn to dhols and join the Kumar family as they prepare for one of Mumbai's most "
                        "electric festivals. Help with the flower rangoli, walk with the street procession, offer "
                        "prayers at the aarti and feast on modaks and a Maharashtrian thali cooked by Rajesh's "
                        "mother. Not a performance — real, chaotic, joyful family life.",
        "plan": [
            "7:30 AM · flower rangoli and decorating the idol with the family",
            "9:00 AM · morning aarti in the chawl courtyard",
            "11:00 AM · rolling modaks in the kitchen with Rajesh's mother",
            "1:00 PM · Maharashtrian thali — puran poli, ukadiche modak, sol kadhi",
            "4:00 PM · dhol-tasha procession through the lanes of Dadar",
            "7:00 PM · visarjan at Girgaum Chowpatty",
        ],
        "included": ["All meals and prasad", "Festival clothing if you want it", "Procession entry with the "
                      "mandal"],
        "bring": ["Clothes you can dance in", "Sandals you can lose"],
        "reviews": [
            {"reviewer_name": "Sophia L.", "reviewer_city": "Berlin", "stars": 5,
             "text": "I was in tears by the end. Rajesh's family treated me like a daughter — the procession, "
                     "the music, the food."},
            {"reviewer_name": "James R.", "reviewer_city": "London", "stars": 5,
             "text": "My kids still talk about it every week. The drumming was electric and Rajesh answered "
                     "questions before I asked them."},
        ],
    },
    {
        "id": "exp2", "title": "Rajasthani block printing masterclass", "city": "Jaipur",
        "location": "Old City, Jaipur", "interests": ["arts", "heritage"],
        "price_label": "₹3,200 / person", "rating": 4.8, "review_count": 29,
        "image": "Hawa Mahal 2011.jpg",
        "gallery": ["Hawa Mahal Jaipur.jpg", "Hawa Mahal 2011.jpg", "Taj Mahal, Agra, India edit3.jpg"],
        "date_label": "Rolling availability", "people_label": "2–6 guests", "duration_label": "5 hours",
        "tags": ["Hands-on craft", "Heritage haveli", "Natural dyes", "Take your work home"],
        "host_name": "Priya Meenakshi", "host_since": "2020", "host_langs": "Hindi, English, Marwari",
        "host_bio": "A sixth-generation printer working out of the family haveli. Priya still cuts her own "
                    "blocks and sells the household's cloth in the Old City bazaar.",
        "description": "Step into Priya's six-generation haveli in the Pink City's old quarter and lose an "
                        "afternoon to the meditative rhythm of block printing. Mix natural dyes from indigo and "
                        "madder, hand-print a metre of fabric and carry it home. Her family still sells these "
                        "textiles in the bazaar, so your piece is the real thing.",
        "plan": [
            "Tour of the 200-year-old haveli and the drying terrace",
            "How a block is carved — and why the register has to be perfect",
            "Mixing dye from indigo, madder and pomegranate rind",
            "Printing your own metre of cotton, mistakes and all",
            "Chai and kachori on the terrace while it dries",
            "Walk to the family stall in the bazaar",
        ],
        "included": ["All materials", "Your printed fabric to take home", "Chai and snacks"],
        "bring": ["Clothes that can take a dye splash"],
        "reviews": [
            {"reviewer_name": "Clara M.", "reviewer_city": "Paris", "stars": 5,
             "text": "The most beautiful afternoon in Jaipur. I came for a workshop and left with a friendship."},
            {"reviewer_name": "Emily T.", "reviewer_city": "New York", "stars": 5,
             "text": "Brought my sceptical teenager. She was hooked in ten minutes and printed three pieces."},
        ],
    },
    {
        "id": "exp3", "title": "Dawn on the Ganges: raag at sunrise", "city": "Varanasi",
        "location": "Assi Ghat, Varanasi", "interests": ["heritage", "community"],
        "price_label": "₹1,800 / person", "rating": 5.0, "review_count": 41,
        "image": "Ganga Aarti at Dawn.jpg",
        "gallery": ["Assi Ghat Varanasi After Ganga Aarti.jpg",
                     "Pandits, Ganga Aarti at Dashashwamedh Ghat, Varanasi.jpg",
                     "Evening Ganga Aarti at Dashashwamedh Ghat.JPG"],
        "date_label": "Daily · 4:30 AM", "people_label": "2–5 guests", "duration_label": "4 hours",
        "tags": ["Sunrise ritual", "Live sarangi", "Ganga aarti", "Ancient ghats"],
        "host_name": "Anand Tiwari", "host_since": "2019", "host_langs": "Hindi, English, Bhojpuri",
        "host_bio": "A classical sarangi player with a doctorate in Hindustani music, born four lanes from Assi "
                    "Ghat. He plays on the boat himself rather than narrating over a recording.",
        "description": "Board a wooden boat before first light and drift past three-thousand-year-old ghats "
                        "while Anand plays a sunrise raag on the sarangi. Watch the dawn aarti, float diyas on "
                        "the river and share chai with a boatman's family. His commentary turns a boat ride "
                        "into a real encounter with one of the world's oldest living cities.",
        "plan": [
            "4:30 AM · meet at Assi Ghat while the lanes are still dark",
            "5:00 AM · wooden boat past the ghats as the sky turns",
            "5:45 AM · live sarangi raag on the water at sunrise",
            "6:30 AM · the dawn Ganga aarti from the river",
            "7:15 AM · float diyas, then chai with a boatman family",
            "8:00 AM · walk back through the lanes of Kashi",
        ],
        "included": ["Private boat", "Chai and breakfast", "Diyas"],
        "bring": ["A shawl — the river is cold before sunrise"],
        "reviews": [
            {"reviewer_name": "Lars N.", "reviewer_city": "Stockholm", "stars": 5,
             "text": "I've been to sixty countries. This single morning is the one I describe first, every "
                     "time."},
            {"reviewer_name": "Tom B.", "reviewer_city": "Melbourne", "stars": 5,
             "text": "Arrived sceptical, not a spiritual person at all. Left moved. It's about people, not "
                     "religion."},
        ],
    },
    {
        "id": "exp4", "title": "Kerala sadya: 28 dishes, one banana leaf", "city": "Kochi",
        "location": "Thrissur, Kerala", "interests": ["food", "community"],
        "price_label": "₹2,800 / person", "rating": 4.9, "review_count": 22,
        "image": "Onam Sadya (15164960372).jpg",
        "gallery": ["2006 Sadhya Onam traditional vegetarian meal, Kerala India.jpg", "Onam Sadya.png",
                     "Onam Sadya (15164960372).jpg"],
        "date_label": "Every Sunday", "people_label": "4–10 guests", "duration_label": "7 hours",
        "tags": ["Vegetarian feast", "Cooking together", "Onam tradition", "Floor dining"],
        "host_name": "The Nair family", "host_since": "2019", "host_langs": "Malayalam, English, Tamil",
        "host_bio": "Three generations in one tharavad. Ammamma runs the kitchen, her daughters run the market "
                    "trip, and everyone eats on the floor together at the end.",
        "description": "The sadya — twenty-eight dishes on a banana leaf — is one of India's great meals. Join "
                        "the Nair family as they build it from scratch: grind the coconut chutney, cook the "
                        "avial, stir the payasam. You'll cook, serve and eat cross-legged on the floor exactly as "
                        "tradition asks. Joyful, chaotic, delicious.",
        "plan": [
            "7:00 AM · market run with the family matriarch",
            "9:00 AM · grinding coconut, cutting for avial and thoran",
            "11:30 AM · cooking six of the twenty-eight dishes yourself",
            "12:30 PM · cutting and laying the banana leaves",
            "1:00 PM · the full sadya, eaten cross-legged and south-facing",
            "3:00 PM · payasam, and a walk through the old tharavad",
        ],
        "included": ["Market trip", "All ingredients", "The full sadya", "Recipe cards to take home"],
        "bring": ["An appetite, and clothes you can sit on the floor in"],
        "reviews": [
            {"reviewer_name": "Francesca B.", "reviewer_city": "Rome", "stars": 5,
             "text": "I write about food for a living. This was one of the five best meals of my life."},
            {"reviewer_name": "Anna K.", "reviewer_city": "Helsinki", "stars": 5,
             "text": "The grandmother spoke no English. We talked through food and smiles anyway."},
        ],
    },
    {
        "id": "exp5", "title": "Chandni Chowk street food crawl", "city": "Delhi",
        "location": "Chandni Chowk, Delhi", "interests": ["food", "heritage"],
        "price_label": "₹1,200 / person", "rating": 4.7, "review_count": 56,
        "image": "View of Chandni Chowk, Old Delhi, India - September 2014.jpg",
        "gallery": ["Chandni Chowk Road, Delhi (43802533965).jpg", "The Gurudwara Sis Ganj Sahib, Chandni Chowk, "
                     "Delhi.JPG", "View of Chandni Chowk, Old Delhi, India - September 2014.jpg"],
        "date_label": "Daily · 6:00 PM", "people_label": "2–8 guests", "duration_label": "3 hours",
        "tags": ["Street food", "Evening walk", "Mughal history", "Century-old stalls"],
        "host_name": "Vikram Malhotra", "host_since": "2020", "host_langs": "Hindi, Urdu, English",
        "host_bio": "Fourth generation behind the counter of a Khari Baoli spice shop. Vikram knows the halwais "
                    "by name and orders in the order they should be eaten.",
        "description": "Navigate the maze of Chandni Chowk with Vikram, whose family has run a spice shop here "
                        "for four generations. He knows which alley hides the best jalebi, which halwai still "
                        "uses a clay-pot oven, and why every dish carries a story of Partition, Mughal kitchens "
                        "and street ingenuity. Come hungry.",
        "plan": [
            "6:00 PM · Paranthe Wali Gali, starting where his grandfather started",
            "6:45 PM · Khari Baoli, Asia's largest spice market, at closing hour",
            "7:15 PM · kulfi on the steps of Fatehpuri Masjid",
            "8:00 PM · jalebi from a two-hundred-year-old kadhai",
            "8:30 PM · chai, and the story of how Partition rewrote this menu",
        ],
        "included": ["Every tasting on the route", "Bottled water", "Rickshaw between stops"],
        "bring": ["Comfortable shoes and an empty stomach"],
        "reviews": [
            {"reviewer_name": "Michael O.", "reviewer_city": "Chicago", "stars": 5,
             "text": "Vikram made Chandni Chowk make sense. Three hours felt like ten minutes."},
            {"reviewer_name": "Hana M.", "reviewer_city": "Tokyo", "stars": 5,
             "text": "The food alone is worth it. I'm still thinking about the kachori three months later."},
        ],
    },
]

FESTIVALS = [
    {
        "title": "Clear-water mornings, Shnongpdeng", "date_label": "October – April · daily",
        "region": "West Jaintia Hills, Meghalaya", "seats": 4, "image": "Umngot river, Dawki.jpg",
        "is_big_tile": True, "who": None,
        "description": "The Umngot runs glass-clear through the winter months. Dawn boats with a Khasi family, "
                        "breakfast in their kitchen, and a tent by the river if you stay the night.",
        "about": [], "linked_experience_id": "exp6",
    },
    {
        "title": "Ka Pomblang Nongkrem", "date_label": "Early November · 5 days",
        "region": "Smit, Khasi Hills, Meghalaya", "seats": 6, "image": "Nongkrem Dance.jpg",
        "is_big_tile": False, "who": "Hosted by the Syiem household of Hima Khyrim",
        "description": "A thanksgiving dance at the Syiem's courtyard, held for the harvest and for the "
                        "wellbeing of the state.",
        "about": [
            "Unmarried women dance in the inner circle in gold and coral; men circle them with swords and whisks",
            "The Pomblang goat offering opens the ceremony at the Iing Sad, the sacred house",
            "You are a guest of the household, not an audience — expect to be fed between dances",
            "Cameras are welcome in the courtyard but not inside the Iing Sad",
        ],
        "linked_experience_id": None,
    },
    {
        "title": "Behdienkhlam", "date_label": "July · 4 days", "region": "Jowai, Jaintia Hills, Meghalaya",
        "seats": 4, "image": "Living root bridges, Nongriat village, Meghalaya2.jpg", "is_big_tile": False,
        "who": "Hosted by a Pnar family in Jowai",
        "description": "\"Chasing away the plague.\" Carved wooden khnongs are wrestled through a mud pool "
                        "while the whole town watches.",
        "about": [
            "Men carry decorated rots — towering bamboo-and-paper structures — through the streets",
            "The dance in the Aitnar mud pool is the moment everyone comes for",
            "Datlawakor, a rough football game, decides the year's harvest omen",
            "Bring clothes you are happy to ruin. You will be muddy.",
        ],
        "linked_experience_id": None,
    },
    {
        "title": "100 Drums Wangala", "date_label": "Second week of November",
        "region": "Asanang, Garo Hills, Meghalaya", "seats": 5, "image": "Wangala Dance.jpg",
        "is_big_tile": False, "who": "Hosted by a Garo family near Tura",
        "description": "The Garo harvest thanksgiving to Misi Saljong, danced by a hundred drums at once.",
        "about": [
            "Rows of dama drummers in feathered headdresses move as one line",
            "Village troupes compete; the winning dance is argued about for the rest of the year",
            "Rice beer is poured for guests before the dancing starts",
            "Your host walks you through which drum pattern belongs to which village",
        ],
        "linked_experience_id": None,
    },
    {
        "title": "Hornbill Festival", "date_label": "1 – 10 December", "region": "Kisama, Kohima, Nagaland",
        "seats": 3, "image": "Hornbill Festival,Nagaland.jpg", "is_big_tile": False,
        "who": "Hosted by an Angami family in Kohima",
        "description": "The festival of festivals — every Naga tribe in one heritage village for ten days.",
        "about": [
            "Each tribe keeps its own morung, and yours is the one your host belongs to",
            "Log-drum pulling, Naga wrestling, chilli-eating and the night music concerts",
            "Smoked pork with axone eaten at the family table, not the food stalls",
            "December in Kohima is genuinely cold — pack for it",
        ],
        "linked_experience_id": None,
    },
    {
        "title": "Theyyam season", "date_label": "December – April · night", "region": "Kannur, north Kerala",
        "seats": 4, "image": "Theyyam of Kerala 3.jpg", "is_big_tile": False,
        "who": "Hosted by a family attached to a kaavu shrine",
        "description": "An all-night ritual where a performer becomes the deity and the village comes to speak "
                        "with him.",
        "about": [
            "Watch the four-hour makeup, applied lying down, before the transformation",
            "The mudi headdress can stand twenty feet tall and is lit only by fire",
            "Villagers approach the theyyam to ask for blessings and to be answered directly",
            "It runs from dusk until dawn. You are welcome to sleep and be woken for the important hours",
        ],
        "linked_experience_id": None,
    },
    {
        "title": "Ganesh Chaturthi", "date_label": "7 September", "region": "Dadar, Mumbai", "seats": 3,
        "image": "Anant Chaturdashi.jpg", "is_big_tile": False, "who": None, "description": None, "about": [],
        "linked_experience_id": "exp1",
    },
    {
        "title": "Ganga aarti at dawn", "date_label": "October · daily", "region": "Assi Ghat, Varanasi",
        "seats": 2, "image": "Evening Ganga Aarti at Dashashwamedh Ghat.JPG", "is_big_tile": False, "who": None,
        "description": None, "about": [], "linked_experience_id": "exp3",
    },
]

CIRCLES = [
    {"display_code": "01", "name": "Spice & Story Circle", "member_count": 214, "host_name": "Vikram",
     "description": "Food pilgrims and street-food explorers"},
    {"display_code": "02", "name": "Festival Seekers", "member_count": 381, "host_name": "Rajesh",
     "description": "For people who plan trips around festival dates"},
    {"display_code": "03", "name": "Highlands & Root Bridges", "member_count": 126, "host_name": "Banri",
     "description": "Meghalaya, the Northeast, and slow river days"},
    {"display_code": "04", "name": "Craft & Colour", "member_count": 97, "host_name": "Priya",
     "description": "Artists, makers and heritage craft lovers"},
]


# ─────────────────────────── Seeding logic ───────────────────────────

def seed(reset: bool = False):
    db = SessionLocal()
    try:
        existing_count = db.query(models.Experience).count()
        if existing_count > 0 and not reset:
            print(
                f"Found {existing_count} experience(s) already in the database. "
                f"Skipping seed to avoid duplicates.\n"
                f"Run 'python seed.py --reset' if you want to wipe and reseed."
            )
            return

        if reset:
            print("Resetting: deleting existing catalog rows…")
            db.query(models.Review).delete()
            db.query(models.Festival).delete()
            db.query(models.Circle).delete()
            db.query(models.Experience).delete()
            db.commit()

        print("Inserting experiences and reviews…")
        total_reviews = 0
        for exp_data in EXPERIENCES:
            exp_data = dict(exp_data)  # copy, so popping "reviews" doesn't mutate the module-level list
            reviews_data = exp_data.pop("reviews")
            experience = models.Experience(**exp_data)
            db.add(experience)
            for review_data in reviews_data:
                db.add(models.Review(experience_id=experience.id, **review_data))
            total_reviews += len(reviews_data)

        print("Inserting festivals…")
        for fest_data in FESTIVALS:
            db.add(models.Festival(**fest_data))

        print("Inserting circles…")
        for circle_data in CIRCLES:
            db.add(models.Circle(**circle_data))

        db.commit()
        print(
            f"Done. Seeded {len(EXPERIENCES)} experiences, {total_reviews} reviews, "
            f"{len(FESTIVALS)} festivals, {len(CIRCLES)} circles."
        )
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed(reset="--reset" in sys.argv)
