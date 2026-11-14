"""Topic banks for the Deeni & Friends 1,000-day plan.

Each item: (english, hinglish, thumb_en, thumb_hi, lesson_en, source)
Sources are REFERENCES TO VERIFY: every religious line must be checked by the reviewer before use.
"""
NO_SRC = "No religious text quoted (general learning) - reviewer checks lyrics"
CREATOR = "Allah is the Creator of all things (Quran 39:62)"

DUAS = [
    ("Bismillah Before Eating", "Khaane Se Pehle Bismillah", "Bismillah!", "Bismillah!", "Say Bismillah before we eat", "Sahih al-Bukhari 5376; Sahih Muslim 2022"),
    ("Alhamdulillah After Eating", "Khaane Ke Baad Alhamdulillah", "Alhamdulillah!", "Alhamdulillah!", "Thank Allah after eating", "Sahih Muslim 2734"),
    ("Dua Before Sleeping", "Sone Ki Dua", "Sleepy Dua", "Sone Ki Dua", "Say the dua before we sleep", "Sahih al-Bukhari 6324"),
    ("Dua When Waking Up", "Jaagne Ki Dua", "Good Morning!", "Subah Ki Dua", "Thank Allah when we wake up", "Sahih al-Bukhari 6324"),
    ("Saying Assalamu Alaikum", "Assalamu Alaikum Kehna", "Salaam!", "Salaam!", "Greet everyone with salaam", "Sahih Muslim 54"),
    ("Dua for Leaving the House", "Ghar Se Nikalne Ki Dua", "Bye Bye Home", "Ghar Se Bahar", "Say the dua when we go out", "Sunan Abi Dawud 5095; Jami at-Tirmidhi 3426"),
    ("Mentioning Allah When Entering the House", "Ghar Mein Aate Waqt Allah Ka Naam", "Back Home!", "Ghar Aa Gaye!", "Say Bismillah when we come home", "Sahih Muslim 2018"),
    ("Dua Before Entering the Toilet", "Bathroom Jaane Ki Dua", "Toilet Dua", "Bathroom Dua", "Say the dua before the toilet", "Sahih al-Bukhari 142; Sahih Muslim 375"),
    ("Dua After Leaving the Toilet", "Bathroom Se Nikalne Ki Dua", "Ghufranak!", "Ghufranak!", "Say Ghufranak after the toilet", "Sunan Abi Dawud 30; Jami at-Tirmidhi 7"),
    ("Dua for Wearing Clothes", "Kapde Pehenne Ki Dua", "New Clothes!", "Naye Kapde!", "Thank Allah for our clothes", "Sunan Abi Dawud 4023"),
    ("Dua for Entering the Masjid", "Masjid Mein Jaane Ki Dua", "Masjid Time!", "Masjid Chalo!", "Say the dua entering the masjid", "Sahih Muslim 713"),
    ("Dua for Leaving the Masjid", "Masjid Se Nikalne Ki Dua", "Bye Masjid", "Masjid Se Bahar", "Say the dua leaving the masjid", "Sahih Muslim 713"),
    ("When We Sneeze: Alhamdulillah", "Chheenk Aaye To Alhamdulillah", "Achoo!", "Aachhoo!", "Say Alhamdulillah when we sneeze", "Sahih al-Bukhari 6224"),
    ("Drinking Water in Three Sips", "Teen Saans Mein Paani", "Glug Glug!", "Glug Glug!", "Drink slowly in three sips", "Sahih Muslim 2028"),
    ("Dua for Riding in a Car", "Gaadi Mein Baithne Ki Dua", "Car Dua!", "Safar Ki Dua", "Say the travel dua in the car", "Quran 43:13-14; Sahih Muslim 1342"),
    ("Dua When It Rains", "Baarish Ki Dua", "Rain Rain!", "Baarish!", "Ask Allah for good rain", "Sahih al-Bukhari 1032"),
    ("Saying InshaAllah", "InshaAllah Kehna", "InshaAllah!", "InshaAllah!", "Say InshaAllah for things we plan", "Quran 18:23-24"),
    ("Saying MashaAllah", "MashaAllah Kehna", "MashaAllah!", "MashaAllah!", "Say MashaAllah when we like something", "Quran 18:39"),
    ("Saying SubhanAllah", "SubhanAllah Kehna", "SubhanAllah!", "SubhanAllah!", "Say SubhanAllah when we see Allah's creation", "Quran 3:190-191; Sahih al-Bukhari 6406"),
    ("Saying Astaghfirullah", "Astaghfirullah Kehna", "Sorry Allah", "Astaghfirullah", "Say Astaghfirullah when we make a mistake", "Sahih al-Bukhari 6307"),
    ("Saying JazakAllahu Khayran", "JazakAllah Khair Kehna", "Thank You!", "JazakAllah!", "Thank people with JazakAllahu khayran", "Jami at-Tirmidhi 2035"),
    ("When I Feel Angry: A'udhu Billah", "Gussa Aaye To A'udhu Billah", "Calm Down!", "Gussa Nahi!", "Seek refuge in Allah when angry", "Sahih al-Bukhari 3282"),
    ("Eating With the Right Hand", "Seedhe Haath Se Khana", "Right Hand!", "Seedha Haath!", "Eat with the right hand", "Sahih al-Bukhari 5376"),
    ("Dua for Parents (Rabbir-hamhuma)", "Ammi Abbu Ke Liye Dua", "Love Mama Baba", "Ammi Abbu!", "Make dua for our parents", "Quran 17:24"),
    ("Dua for Knowledge (Rabbi Zidni Ilma)", "Ilm Ki Dua", "Smart Dua!", "Ilm Ki Dua", "Ask Allah to increase our knowledge", "Quran 20:114"),
    ("Rabbana Atina Dua", "Rabbana Atina Dua", "Best Dua!", "Pyaari Dua", "Ask Allah for good in both worlds", "Quran 2:201"),
    ("Brushing Teeth: the Miswak Sunnah", "Miswak Ki Sunnat", "Brush Brush!", "Brush Karo!", "Keep our teeth clean like the Sunnah", "Sahih al-Bukhari 887"),
    ("Sitting Down to Drink", "Baith Kar Paani Peena", "Sit & Sip!", "Baith Ke Piyo!", "Sit down when we drink", "Sahih Muslim 2024"),
]
DUA_FORMATS = [("Song", "Song"), ("Story at Home", "Ghar Ki Kahani"), ("Story at the Park", "Park Ki Kahani"),
               ("Sing & Practice with Deeni", "Deeni Ke Saath Practice"), ("Dance Remix", "Dance Remix"),
               ("Quiz with Bubbly", "Bubbly Ka Quiz"), ("Slow Lullaby Version", "Lori Version"),
               ("Call & Response", "Tum Bhi Bolo!"), ("Ayaan Forgets!", "Ayaan Bhool Gaya!"), ("Amira Teaches", "Amira Sikhaati Hai")]

LETTERS = ["Alif", "Ba", "Ta", "Tha", "Jeem", "Haa", "Khaa", "Dal", "Dhal", "Ra", "Zay", "Seen", "Sheen", "Saad", "Daad",
           "Taa", "Dhaa", "Ain", "Ghain", "Fa", "Qaf", "Kaf", "Lam", "Meem", "Noon", "Ha", "Waw", "Ya"]
ARABIC = ([(f"Arabic Letter {l}", f"Arabic Harf {l}", f"{l}!", f"{l}!", f"Learn the Arabic letter {l}", "Arabic pronunciation check by teacher") for l in LETTERS] +
          [(f"Arabic Number {n}", f"Arabic Ginti {n}", str(n), str(n), f"Count {n} in Arabic", "Arabic pronunciation check by teacher") for n in range(1, 11)] +
          [(e, h, t, t, f"Learn {e.lower()}", "Arabic pronunciation check by teacher") for e, h, t in [
              ("Fatha, Kasra and Damma", "Zabar, Zer aur Pesh", "A I U!"), ("Arabic Colour Words", "Arabic Mein Rang", "Colours!"),
              ("Arabic Family Words", "Arabic Mein Ghar Wale", "Family!"), ("Arabic Body Words", "Arabic Mein Jism Ke Hisse", "My Body!"),
              ("Arabic Animal Words", "Arabic Mein Jaanwar", "Animals!"), ("Arabic Fruit Words", "Arabic Mein Phal", "Fruits!"),
              ("Arabic Greetings", "Arabic Mein Salaam", "Salaam!"), ("Arabic Days of the Week", "Arabic Mein Hafte Ke Din", "7 Days!"),
              ("Arabic Numbers 1 to 10", "Arabic Ginti 1 Se 10", "1 to 10!"), ("The Arabic Alphabet Song", "Alif Ba Ta Song", "Alif Ba Ta!"),
              ("Arabic Words at Home", "Ghar Ke Arabic Lafz", "My Home!"), ("Arabic Words at the Masjid", "Masjid Ke Arabic Lafz", "Masjid Words!"),
              ("Tanween: An, In, Un", "Do Zabar, Do Zer, Do Pesh", "An In Un!"), ("Sukoon and Shaddah", "Jazm aur Tashdeed", "Shaddah!"),
              ("Long Vowels: Madd", "Lambi Aawaaz: Madd", "Madd!")]])
ARABIC_FORMATS = [("Song", "Gaana"), ("Words That Start With It", "Is Se Shuru Hone Wale Lafz"), ("Trace & Write", "Likhna Seekho"),
                  ("Quiz with Bubbly", "Bubbly Ka Quiz"), ("Treasure Hunt", "Khazana Dhoondo"), ("Dance Song", "Dance Song")]

VALUES = [
    ("Honesty", "Sach Bolna", "Tell the Truth!", "Sach Bolo!", "Always tell the truth", "Sahih al-Bukhari 6094"),
    ("Sharing", "Share Karna", "Let's Share!", "Share Karo!", "Sharing makes everyone happy", "Sahih al-Bukhari 12"),
    ("Kindness to Animals", "Jaanwaron Par Reham", "Be Kind!", "Reham Karo!", "Be kind to animals", "Sahih al-Bukhari 2363"),
    ("Respecting Parents", "Ammi Abbu Ki Izzat", "Love Mama!", "Ammi Abbu!", "Respect and love our parents", "Quran 17:23"),
    ("Helping at Home", "Ghar Mein Madad", "I Can Help!", "Madad Karo!", "Help our family at home", "Sahih al-Bukhari 676"),
    ("Patience", "Sabr", "Wait Wait!", "Sabr Karo!", "Be patient", "Quran 2:153"),
    ("Saying Sorry", "Sorry Bolna", "Sorry!", "Sorry!", "Say sorry when we hurt someone", NO_SRC),
    ("Forgiving Others", "Maaf Karna", "It's OK!", "Maaf Kiya!", "Forgive others", "Quran 24:22"),
    ("Saying Thank You", "Shukriya Kehna", "Thank You!", "Shukriya!", "Thank people who help us", "Sunan Abi Dawud 4811"),
    ("Being Gentle", "Naram Dil Rehna", "Gentle!", "Pyaar Se!", "Be gentle with everyone", "Sahih Muslim 2594"),
    ("Not Wasting Food", "Khana Zaya Na Karo", "No Waste!", "Zaya Nahi!", "Don't waste food", "Quran 7:31"),
    ("Saving Water", "Paani Bachao", "Save Water!", "Paani Bachao!", "Use only the water we need", "Quran 7:31"),
    ("Keeping Promises", "Waada Nibhana", "Promise!", "Waada!", "Keep our promises", "Quran 17:34"),
    ("Tidying Up", "Safai Karna", "Clean Up!", "Safai!", "Put our toys away", "Sahih Muslim 223"),
    ("Being a Good Neighbour", "Achha Padosi", "Hello Neighbour!", "Padosi!", "Be kind to neighbours", "Sahih al-Bukhari 6014"),
    ("Big Feelings: Angry", "Jab Gussa Aaye", "So Angry!", "Gussa!", "What to do when we feel angry", "Sahih al-Bukhari 3282"),
    ("Big Feelings: Sad", "Jab Udaas Ho", "Feeling Sad", "Udaas?", "Allah is with us when we are sad", "Quran 9:40; Quran 94:5-6"),
    ("Big Feelings: Scared", "Jab Darr Lage", "Scared?", "Darr Lage?", "Say A'udhu billah and feel safe", "Quran 113-114"),
    ("Big Feelings: Jealous", "Jab Jalan Ho", "Not Fair!", "Jalan?", "Be happy for others", "Sahih al-Bukhari 13"),
    ("Trying New Things", "Kuch Naya Try Karo", "I Can Try!", "Try Karo!", "Try new things with Bismillah", NO_SRC),
    ("Taking Turns", "Baari Baari", "My Turn!", "Meri Baari!", "Wait for our turn", NO_SRC),
    ("Smiling is Sadaqah", "Muskurana Sadqa Hai", "Smile!", "Muskurao!", "A smile is charity", "Jami at-Tirmidhi 1956"),
    ("Being Grateful", "Shukr Karna", "Thank Allah!", "Shukr!", "Thank Allah for everything", "Quran 14:7"),
    ("Staying Clean", "Saaf Suthra Rehna", "So Clean!", "Saaf Suthra!", "Cleanliness is part of faith", "Sahih Muslim 223"),
    ("Kind Words", "Meethe Bol", "Kind Words!", "Meethe Bol!", "A good word is charity", "Sahih al-Bukhari 2989"),
    ("Giving Charity", "Sadqa Dena", "Give!", "Sadqa!", "Give to people in need", "Quran 2:261"),
    ("Visiting Grandparents", "Nana Nani Se Milna", "Nani & Nana!", "Nana Nani!", "Love and visit our family", "Quran 17:23"),
    ("Respecting Teachers", "Ustaad Ki Izzat", "My Teacher!", "Ustaad Ji!", "Respect people who teach us", "Sunan Abi Dawud 4843; Jami at-Tirmidhi 1920"),
    ("Caring for Plants", "Paudhon Ka Khayal", "Grow Grow!", "Paudha!", "Planting is a good deed", "Sahih al-Bukhari 2320"),
    ("Including Everyone", "Sab Ko Saath Khilao", "Play Together!", "Saath Khelo!", "Let everyone play", NO_SRC),
]
SETTINGS = [("at Home", "Ghar Par"), ("at the Park", "Park Mein"), ("at the Masjid", "Masjid Mein"), ("at School", "School Mein"),
            ("at the Market", "Bazaar Mein")]
VALUE_FORMATS = [("Story + Song", "Kahani + Gaana"), ("Role-play with Bubbly", "Bubbly Ke Saath Natak")]

COLOURS = [("Red", "Laal"), ("Blue", "Neela"), ("Yellow", "Peela"), ("Green", "Hara"), ("Orange", "Naarangi"), ("Purple", "Jamni"),
           ("Pink", "Gulabi"), ("Brown", "Bhoora"), ("Black and White", "Kaala aur Safed"), ("Rainbow Colours", "Indradhanush Ke Rang")]
ANIMALS = [("Camel", "Oont"), ("Cat", "Billi"), ("Cow", "Gaay"), ("Sheep", "Bhed"), ("Horse", "Ghoda"), ("Chicken", "Murgi"),
           ("Elephant", "Haathi"), ("Lion", "Sher"), ("Giraffe", "Giraffe"), ("Monkey", "Bandar"), ("Bee", "Madhumakkhi"), ("Ant", "Cheenti"),
           ("Butterfly", "Titli"), ("Bird", "Chidiya"), ("Owl", "Ullu"), ("Duck", "Batakh"), ("Rabbit", "Khargosh"), ("Goat", "Bakri"),
           ("Penguin", "Penguin"), ("Zebra", "Zebra"), ("Bear", "Bhaalu"), ("Frog", "Mendhak"), ("Parrot", "Tota"), ("Squirrel", "Gilehri")]
FRUITS = [("Dates", "Khajoor"), ("Apples", "Seb"), ("Bananas", "Kele"), ("Grapes", "Angoor"), ("Mangoes", "Aam"), ("Watermelon", "Tarbooz"),
          ("Oranges", "Santre"), ("Pomegranate", "Anaar"), ("Figs", "Anjeer"), ("Olives", "Zaitoon"), ("Strawberries", "Strawberry"), ("Guava", "Amrood")]
VEG = [("Carrots", "Gaajar"), ("Tomatoes", "Tamatar"), ("Potatoes", "Aloo"), ("Cucumbers", "Kheera"), ("Peas", "Matar"), ("Pumpkins", "Kaddu"),
       ("Onions", "Pyaaz"), ("Spinach", "Palak")]
SHAPES = [("Circle", "Gol"), ("Square", "Chaukor"), ("Triangle", "Tikona"), ("Star", "Sitara"), ("Heart", "Dil"), ("Rectangle", "Lamba Chaukor"),
          ("Oval", "Anda Shape"), ("Crescent", "Hilaal")]
BODY = [("Eyes", "Aankhein"), ("Ears", "Kaan"), ("Hands", "Haath"), ("Feet", "Pair"), ("Teeth", "Daant"), ("Nose", "Naak"), ("Hair", "Baal")]
WEATHER = [("Sunny Day", "Dhoop Wala Din"), ("Rainy Day", "Baarish Ka Din"), ("Windy Day", "Hawa Wala Din"), ("Cloudy Day", "Baadal Wala Din"),
           ("Snowy Day", "Barf Wala Din"), ("Rainbow", "Indradhanush")]
NATURE = [("The Sun", "Suraj"), ("The Moon", "Chaand"), ("The Stars", "Taare"), ("Day and Night", "Din aur Raat"), ("Big and Small", "Bada aur Chhota"),
          ("Up and Down", "Upar aur Neeche"), ("Hot and Cold", "Garam aur Thanda"), ("Fast and Slow", "Tez aur Dheere"),
          ("Loud and Quiet", "Zor Se aur Dheere Se"), ("Wet and Dry", "Geela aur Sookha"), ("Mountains", "Pahaad"), ("Trees", "Ped"), ("Flowers", "Phool")]
VEHICLES = [("Car", "Gaadi"), ("Bus", "Bus"), ("Train", "Rail Gaadi"), ("Aeroplane", "Hawai Jahaz"), ("Boat", "Naav"), ("Bicycle", "Cycle"),
            ("Fire Engine", "Fire Engine"), ("Tractor", "Tractor")]

PRESCHOOL = (
    [(f"Colour {e}: Things Allah Made", f"{h} Rang: Allah Ki Banai Cheezein", f"{e}!", f"{h}!", f"Learn the colour {e.lower()}", CREATOR) for e, h in COLOURS] +
    [(f"Number {n} Song", f"Ginti {n} Ka Gaana", str(n), str(n), f"Learn the number {n}", NO_SRC) for n in range(1, 21)] +
    [(f"Shape: {e}", f"Shape: {h}", f"{e}!", f"{h}!", f"Learn the {e.lower()} shape", NO_SRC) for e, h in SHAPES] +
    [(f"Allah Made the {e}", f"Allah Ne Banaya {h}", f"{e}!", f"{h}!", f"Learn about the {e.lower()}", CREATOR) for e, h in ANIMALS] +
    [(f"Yummy Fruits: {e}", f"Mazedaar Phal: {h}", f"{e}!", f"{h}!", f"Learn about {e.lower()}", CREATOR) for e, h in FRUITS] +
    [(f"Healthy Vegetables: {e}", f"Sehatmand Sabzi: {h}", f"{e}!", f"{h}!", f"Learn about {e.lower()}", CREATOR) for e, h in VEG] +
    [(f"My Body: {e}", f"Mera Jism: {h}", f"{e}!", f"{h}!", f"Allah gave us {e.lower()}", "Quran 16:78; Quran 95:4") for e, h in BODY] +
    [(f"Weather: {e}", f"Mausam: {h}", f"{e}!", f"{h}!", f"Learn about a {e.lower()}", CREATOR) for e, h in WEATHER] +
    [(e, h, f"{e}!", f"{h}!", f"Learn about {e.lower()}", CREATOR) for e, h in NATURE] +
    [(f"Vehicles: {e}", f"Gaadiyan: {h}", f"{e}!", f"{h}!", f"Learn about the {e.lower()}", NO_SRC) for e, h in VEHICLES] +
    [(e, h, t, t, l, NO_SRC) for e, h, t, l in [
        ("Days of the Week Song", "Hafte Ke Din Ka Gaana", "7 Days!", "Learn the days of the week"),
        ("Months of the Year Song", "Saal Ke Mahine", "12 Months!", "Learn the months"),
        ("ABC Song with Deeni", "Deeni Ke Saath ABC", "ABC!", "Learn the English alphabet"),
        ("Phonics A to M", "Phonics A Se M", "A to M!", "Learn letter sounds A to M"),
        ("Phonics N to Z", "Phonics N Se Z", "N to Z!", "Learn letter sounds N to Z")]])
PRESCHOOL_FORMATS = [("Song", "Gaana"), ("Learn & Play with Deeni", "Deeni Ke Saath Seekho Aur Khelo"), ("Hide & Seek Game", "Chhupan Chhupai")]

MONTHS = ["Muharram", "Safar", "Rabi al-Awwal", "Rabi al-Thani", "Jumada al-Ula", "Jumada al-Akhirah", "Rajab", "Sha'ban",
          "Ramadan", "Shawwal", "Dhul Qa'dah", "Dhul Hijjah"]
NAMES = ["Ar-Rahman", "Ar-Rahim", "Al-Khaliq", "Ar-Razzaq", "As-Salam", "Al-Wadud", "As-Sami'", "Al-Basir", "Al-Ghafur", "Al-Malik"]
SURAHS = [("Al-Fatiha", 1), ("An-Nas", 114), ("Al-Falaq", 113), ("Al-Ikhlas", 112), ("Al-Masad", 111), ("An-Nasr", 110),
          ("Al-Kafirun", 109), ("Al-Kawthar", 108), ("Al-Ma'un", 107), ("Quraysh", 106), ("Al-Fil", 105), ("Al-Humazah", 104),
          ("Al-Asr", 103), ("At-Takathur", 102), ("Al-Qari'ah", 101)]
BASICS = (
    [(e, h, t, th, l, s) for e, h, t, th, l, s in [
        ("The Five Pillars of Islam", "Islam Ke 5 Sutoon", "5 Pillars!", "5 Sutoon!", "Learn the five pillars", "Sahih al-Bukhari 8"),
        ("The Shahada", "Kalima Shahadat", "Shahada!", "Kalima!", "Learn the Shahada", "Sahih al-Bukhari 8"),
        ("Fajr: The Morning Prayer", "Fajr Ki Namaz", "Fajr!", "Fajr!", "Learn about Fajr", "Quran 4:103"),
        ("Dhuhr: The Noon Prayer", "Zuhr Ki Namaz", "Dhuhr!", "Zuhr!", "Learn about Dhuhr", "Quran 4:103"),
        ("Asr: The Afternoon Prayer", "Asr Ki Namaz", "Asr!", "Asr!", "Learn about Asr", "Quran 4:103"),
        ("Maghrib: The Sunset Prayer", "Maghrib Ki Namaz", "Maghrib!", "Maghrib!", "Learn about Maghrib", "Quran 4:103"),
        ("Isha: The Night Prayer", "Isha Ki Namaz", "Isha!", "Isha!", "Learn about Isha", "Quran 4:103"),
        ("Five Daily Prayers Song", "5 Waqt Ki Namaz", "5 Prayers!", "5 Namazein!", "We pray five times a day", "Sahih al-Bukhari 528"),
        ("Wudu Step by Step", "Wuzu Ka Tareeqa", "Wudu!", "Wuzu!", "Learn how to make wudu", "Quran 5:6"),
        ("Our Masjid", "Hamari Masjid", "Masjid!", "Masjid!", "The masjid is Allah's house", "Sahih Muslim 671"),
        ("The Quran is Our Book", "Quran Hamari Kitaab", "My Quran!", "Mera Quran!", "The Quran is Allah's words", "Quran 2:2"),
        ("The Kaaba", "Khana Kaaba", "Kaaba!", "Kaaba!", "The Kaaba is in Makkah", "Quran 3:96"),
        ("Zakat and Charity", "Zakat Aur Sadqa", "Zakat!", "Zakat!", "Sharing our wealth", "Quran 2:43"),
        ("Fasting for Little Ones", "Bachon Ka Roza", "Fasting!", "Roza!", "Learn what fasting is", "Quran 2:183"),
        ("Hajj for Kids", "Bachon Ke Liye Hajj", "Hajj!", "Hajj!", "Learn what Hajj is", "Quran 3:97"),
        ("Friday is Special: Jumu'ah", "Jumma Ka Mubarak Din", "Jumu'ah!", "Jumma!", "Friday is a special day", "Quran 62:9"),
        ("Friday Sunnah: Ghusl and Best Clothes", "Jumma Ki Sunnatein", "Friday Fresh!", "Jumma Taiyaari!", "Get clean and dressed for Jumu'ah", "Sahih al-Bukhari 877"),
        ("The Six Pillars of Imaan", "Imaan Ki 6 Baatein", "6 Pillars!", "Imaan!", "Learn the six pillars of imaan", "Sahih Muslim 8"),
        ("Allah is One", "Allah Ek Hai", "Allah is One!", "Allah Ek Hai!", "There is only one Allah", "Quran 112")]] +
    [(f"Islamic Month: {m}", f"Islami Mahina: {m}", f"{m}!", f"{m}!", f"Learn the Islamic month {m}", "Quran 9:36") for m in MONTHS] +
    [(f"Allah's Beautiful Name: {n}", f"Allah Ka Pyaara Naam: {n}", n, n, f"Learn Allah's name {n}", "Quran 7:180") for n in NAMES] +
    [(e, h, t, th, l, s) for e, h, t, th, l, s in [
        ("Facing the Qibla", "Qibla Ki Taraf", "Qibla!", "Qibla!", "We face the Kaaba when we pray", "Quran 2:144"),
        ("My Prayer Mat", "Meri Jaa-Namaz", "Prayer Mat!", "Jaa-Namaz!", "Keep our prayer place clean", "Quran 2:125; Sahih Muslim 223"),
        ("Standing in Prayer", "Namaz Mein Khade Hona", "Stand Tall!", "Qiyaam!", "Learn how we stand in salah", "Sahih al-Bukhari 757"),
        ("Bowing in Prayer: Ruku", "Ruku Karna", "Ruku!", "Ruku!", "Learn how we bow in salah", "Sahih al-Bukhari 757"),
        ("Prostrating in Prayer: Sujood", "Sajda Karna", "Sujood!", "Sajda!", "Learn how we prostrate in salah", "Sahih al-Bukhari 757"),
        ("Ending Prayer with Salaam", "Salaam Se Namaz Khatam", "Salaam!", "Salaam!", "We end salah with salaam", "Sahih Muslim 498"),
        ("Masjid Manners: Quiet Voices", "Masjid Mein Dheere Bolo", "Shhh!", "Dheere!", "Speak softly in the masjid", NO_SRC),
        ("Masjid Manners: Shoes on the Rack", "Joote Rack Mein", "Shoes Away!", "Joote Rakho!", "Keep the masjid tidy", NO_SRC),
        ("Raising Hands for Dua", "Haath Utha Kar Dua", "Dua Time!", "Dua!", "We raise our hands to make dua", "Sunan Abi Dawud 1488"),
        ("Allah Hears Our Dua", "Allah Hamari Dua Sunta Hai", "Allah Hears!", "Allah Sunta Hai!", "Allah is near and hears our dua", "Quran 2:186"),
        ("Taking Care of Our Quran", "Quran Ki Hifazat", "My Quran!", "Mera Quran!", "Keep our Quran clean and safe", NO_SRC),
        ("The Masjid Charity Box", "Masjid Ka Sadqa Dabba", "Give!", "Sadqa!", "Give a little charity", "Quran 2:261"),
        ("Saying Bismillah Before Reading", "Padhne Se Pehle Bismillah", "Bismillah!", "Bismillah!", "Start reading with Allah's name", "Quran 96:1"),
        ("Angels Are Allah's Creation", "Farishte Allah Ki Makhlooq", "Angels!", "Farishte!", "Angels are created by Allah", "Sahih Muslim 8"),
        ("The Day of Jumu'ah Song", "Jumma Ka Gaana", "Jumu'ah!", "Jumma!", "Friday is a special day", "Quran 62:9"),
        ("Helping at the Masjid", "Masjid Mein Madad", "Helpers!", "Madadgaar!", "Help keep the masjid clean", NO_SRC)]])
BASICS_FORMATS = [("Song", "Gaana"), ("Story", "Kahani"), ("Quiz with Bubbly", "Bubbly Ka Quiz"), ("Activity", "Activity"), ("Remix", "Remix")]
SURAH_FORMATS = [("Line by Line", "Aayat Ba Aayat"), ("Revision Sing-along", "Dohraao"), ("Memory Challenge", "Yaad Karo Challenge"),
                 ("Meaning for Kids", "Bachon Ke Liye Matlab"), ("Listen and Repeat", "Suno Aur Dohraao")]

PLACES = [("Coral Reef", "Moonge Ki Chattan"), ("Beach", "Samundar Kinare"), ("Park", "Park"), ("Rainy Day", "Baarish Ka Din"),
          ("Garden", "Bageecha"), ("Farm", "Khet"), ("Zoo", "Chidiyaghar"), ("Market", "Bazaar"), ("Masjid Garden", "Masjid Ka Bageecha"),
          ("Kitchen", "Rasoi"), ("Picnic", "Picnic"), ("Snow Day", "Barf Wala Din"), ("Desert", "Registaan"), ("Mountain", "Pahaad"),
          ("River", "Nadi"), ("Night Sky", "Raat Ka Aasmaan"), ("Bakery", "Bakery"), ("Library", "Library"), ("Fruit Orchard", "Phalon Ka Baagh"),
          ("Bus Ride", "Bus Ki Sair")]

SEA = [("Whale", "Whale"), ("Dolphin", "Dolphin"), ("Sea Turtle", "Samundari Kachhua"), ("Octopus", "Octopus"), ("Starfish", "Starfish"),
       ("Seahorse", "Samundari Ghoda"), ("Jellyfish", "Jellyfish"), ("Crab", "Kekda"), ("Lobster", "Lobster"), ("Clownfish", "Clownfish"),
       ("Stingray", "Stingray"), ("Pufferfish", "Pufferfish"), ("Seal", "Seal"), ("Penguin", "Penguin"), ("Walrus", "Walrus"),
       ("Coral", "Moonga"), ("Sea Snail", "Samundari Ghonga"), ("Shrimp", "Jhinga"), ("Squid", "Squid"), ("Eel", "Eel"),
       ("Sea Otter", "Sea Otter"), ("Pelican", "Pelican"), ("Seagull", "Samundari Bagla"), ("Manatee", "Manatee"), ("Narwhal", "Narwhal"),
       ("Swordfish", "Swordfish"), ("Angelfish", "Angelfish"), ("Oyster and Pearl", "Seep aur Moti"), ("Sea Urchin", "Sea Urchin"), ("Seaweed", "Samundari Ghaas")]
SEA_FORMATS = [("Song", "Gaana"), ("Count with Deeni", "Deeni Ke Saath Ginti"), ("Colour Hunt", "Rang Dhoondo"),
               ("Big and Small", "Bada Chhota"), ("Sounds and Moves", "Aawaaz Aur Harkat")]

LULLABIES = [
    ("Sleepy Time Dua Lullaby", "Sone Ki Dua Ki Lori", "Sahih al-Bukhari 6324"), ("Count the Stars Lullaby", "Taare Gino Lori", CREATOR),
    ("Moon Lullaby", "Chanda Ki Lori", CREATOR), ("SubhanAllah Lullaby", "SubhanAllah Lori", "Sahih al-Bukhari 6406"),
    ("Ocean Waves Lullaby", "Leheron Ki Lori", CREATOR), ("Goodnight Deeni", "Shab Bakhair Deeni", NO_SRC),
    ("Goodnight Mama and Baba", "Shab Bakhair Ammi Abbu", NO_SRC), ("Calm Breathing Lullaby", "Aaram Se Saans Lo", NO_SRC),
    ("Thank You Allah for Today", "Shukriya Allah Aaj Ke Liye", "Quran 14:7"), ("Rain Lullaby", "Baarish Ki Lori", CREATOR),
    ("Alhamdulillah Lullaby", "Alhamdulillah Lori", "Sahih Muslim 223"), ("Little Hearts Lullaby", "Chhote Dil Ki Lori", NO_SRC),
    ("Sleepy Bubbly", "Neend Wala Bubbly", NO_SRC), ("Soft Clouds Lullaby", "Naram Baadal Lori", CREATOR),
    ("Crescent Moon Lullaby", "Hilaal Lori", CREATOR), ("Allah Is Always With Me", "Allah Hamesha Saath Hai", "Quran 57:4"),
    ("Sweet Dreams Little One", "Meethe Sapne", NO_SRC), ("Sleepy Animals Lullaby", "Soye Jaanwar Lori", CREATOR),
    ("Quiet Night Lullaby", "Khamosh Raat Lori", NO_SRC), ("Hug Time Lullaby", "Jhappi Lori", NO_SRC)]
NIGHT_SCENES = [("Bedroom", "Kamre Mein"), ("Garden at Night", "Raat Ka Bageecha"), ("Ocean Night", "Samundar Ki Raat"),
                ("Rainy Night", "Baarish Ki Raat"), ("Desert Stars", "Registaan Ke Taare"), ("Snowy Night", "Barf Ki Raat"),
                ("Masjid at Night", "Raat Mein Masjid")]

PRE_RAMADAN = [("Ramadan is Coming!", "Ramzan Aa Raha Hai!"), ("Getting Ready for Ramadan", "Ramzan Ki Taiyaari"),
               ("Ramadan Calendar Craft", "Ramzan Calendar Banao"), ("Sha'ban: The Month Before Ramadan", "Shaban: Ramzan Se Pehle"),
               ("What is Fasting?", "Roza Kya Hai?"), ("Our Ramadan Moon Lamp", "Hamara Ramzan Lamp"), ("Suhoor and Iftar Words", "Sehri Aur Iftar"),
               ("Ramadan Kindness Jar", "Nekiyon Ka Dabba"), ("Ramadan Countdown Song", "Ramzan Countdown"), ("Why We Fast", "Hum Roza Kyun Rakhte Hain"),
               ("Ramadan at Nani's House", "Nani Ke Ghar Ramzan"), ("Decorating for Ramadan", "Ramzan Ki Sajawat"),
               ("My Ramadan Good Habits Chart", "Meri Achhi Aadatein Chart"), ("Dates: The Ramadan Fruit", "Khajoor: Ramzan Ka Phal")]
RAMADAN = [("Welcome Ramadan!", "Ramzan Mubarak!", "Quran 2:185"), ("Spotting the Crescent Moon", "Chaand Dekho!", "Sahih al-Bukhari 1909"),
           ("Suhoor Time", "Sehri Ka Waqt", "Sahih al-Bukhari 1923"), ("Iftar with Dates", "Khajoor Se Iftar", "Sunan Abi Dawud 2356"),
           ("My First Little Fast", "Mera Pehla Chhota Roza", "Quran 2:183"), ("Sharing Iftar with Neighbours", "Padosi Ke Saath Iftar", "Jami at-Tirmidhi 807"),
           ("Taraweeh at the Masjid", "Masjid Mein Taraweeh", "Sahih al-Bukhari 2009"), ("Reading Quran in Ramadan", "Ramzan Mein Quran", "Quran 2:185"),
           ("My Sadaqah Box", "Mera Sadqa Dabba", "Quran 2:261"), ("Kind Deeds Calendar", "Nekiyon Ka Calendar", NO_SRC),
           ("Laylat al-Qadr: The Special Night", "Shab-e-Qadr", "Quran 97"), ("Zakat al-Fitr", "Fitrana", "Sahih al-Bukhari 1503"),
           ("Countdown to Eid", "Eid Ka Countdown", NO_SRC), ("Ramadan Lanterns", "Ramzan Ki Lalten", NO_SRC),
           ("Being Patient When Fasting", "Roze Mein Sabr", "Quran 2:153"), ("Helping Mama with Iftar", "Ammi Ki Iftar Mein Madad", "Sahih al-Bukhari 676"),
           ("Dua for Breaking the Fast", "Iftar Ki Dua", "Sunan Abi Dawud 2357"), ("Quran Story Time", "Quran Ki Kahani", "Quran 2:185"),
           ("Ramadan Words in Arabic", "Ramzan Ke Arabic Lafz", "Arabic pronunciation check by teacher"),
           ("Thank You Allah for Food", "Khaane Ka Shukriya Allah", "Sahih Muslim 2734"), ("Visiting the Masjid at Night", "Raat Ko Masjid", NO_SRC),
           ("Giving Food to People in Need", "Zaroorat Mandon Ko Khana", "Sahih al-Bukhari 12"), ("The Last 10 Nights", "Aakhri 10 Raatein", "Sahih al-Bukhari 2024"),
           ("Kind Words While Fasting", "Roze Mein Meethe Bol", "Sahih al-Bukhari 1904"), ("No Fighting in Ramadan", "Ramzan Mein Ladai Nahi", "Sahih al-Bukhari 1904"),
           ("Moon Sighting for Eid", "Eid Ka Chaand", "Sahih al-Bukhari 1909"), ("Making Eid Cards", "Eid Card Banao", NO_SRC),
           ("Sharing Sweets", "Mithai Baanto", NO_SRC), ("Goodbye Ramadan", "Alvida Ramzan", NO_SRC), ("My Ramadan Diary", "Meri Ramzan Diary", NO_SRC)]
HAJJ = [("Dhul Hijjah: The 10 Best Days", "Zul Hijjah Ke 10 Din", "Sahih al-Bukhari 969"), ("The Hajj Song", "Hajj Ka Gaana", "Quran 3:97"),
        ("Ihram: The White Clothes", "Ehram Ke Safed Kapde", "Sahih al-Bukhari 1838; Jami at-Tirmidhi 994"), ("Going Around the Kaaba", "Kaaba Ka Tawaf", "Quran 22:29"),
        ("Safa and Marwa", "Safa Aur Marwa", "Quran 2:158"), ("Zamzam Water", "Aab-e-Zamzam", "Sahih Muslim 2473"),
        ("The Day of Arafah", "Arafah Ka Din", "Sahih Muslim 1162"), ("The Takbeer Song", "Takbeer Ka Gaana", "Quran 22:28"),
        ("Qurbani Explained Gently", "Qurbani Ki Kahani", "Quran 22:36")]
EID_FITR = [("Eid Mubarak Song", "Eid Mubarak Gaana"), ("Eid Prayer and New Clothes", "Eid Ki Namaz Aur Naye Kapde"),
            ("Eid Gifts and Visiting Family", "Eidi Aur Rishtedaar"), ("Eid Breakfast: Odd Number of Dates", "Eid Ka Nashta: Taak Khajoor"),
            ("Eid Takbeer on the Way", "Eid Ki Takbeer"), ("Eid Fun with Friends", "Doston Ke Saath Eid")]
EID_ADHA = [("Eid al-Adha Mubarak Song", "Bakra Eid Mubarak Gaana"), ("Takbeer and Eid Prayer", "Takbeer Aur Eid Ki Namaz"),
            ("Sharing Qurbani Meat", "Qurbani Ka Gosht Baanto"), ("Eid al-Adha Family Day", "Bakra Eid Family Din"),
            ("Kindness to the Animals of Qurbani", "Qurbani Ke Jaanwar Par Reham"), ("Eid al-Adha Games", "Bakra Eid Ke Khel")]
EID_SRC = "Sahih al-Bukhari 952; Sahih al-Bukhari 953"

# ---------------------------------------------------------------- Short-3 originals
SUNNAHS = [("Smile at Others", "Muskurao", "Jami at-Tirmidhi 1956"), ("Say Salaam First", "Pehle Salaam Karo", "Sahih Muslim 54"),
           ("Use Your Right Hand", "Seedha Haath", "Sahih al-Bukhari 5376"), ("Use the Miswak", "Miswak Karo", "Sahih al-Bukhari 887"),
           ("Sit to Drink", "Baith Ke Piyo", "Sahih Muslim 2024"), ("Sleep on Your Right Side", "Daayin Karwat Soyo", "Sahih al-Bukhari 247"),
           ("Say Bismillah First", "Pehle Bismillah", "Sahih al-Bukhari 5376"), ("Help at Home", "Ghar Mein Madad", "Sahih al-Bukhari 676"),
           ("Give Gifts", "Tohfa Do", "Al-Adab Al-Mufrad 594"), ("Be Kind to Animals", "Jaanwaron Par Reham", "Sahih al-Bukhari 2363"),
           ("Plant a Tree", "Ped Lagao", "Sahih al-Bukhari 2320"), ("Say a Good Word", "Achhi Baat Kaho", "Sahih al-Bukhari 2989")]
COUNT_OBJECTS = [("Dates", "Khajoor"), ("Stars", "Taare"), ("Bubbles", "Bulbule"), ("Fish", "Machhliyan"), ("Apples", "Seb"),
                 ("Balloons", "Gubbare"), ("Ducks", "Batakh"), ("Shells", "Seepiyan"), ("Cars", "Gaadiyan"), ("Flowers", "Phool"),
                 ("Lanterns", "Laltein"), ("Books", "Kitaabein"), ("Cats", "Billiyan"), ("Clouds", "Baadal"), ("Butterflies", "Titliyan")]
HUNT_PLACES = [("in the Kitchen", "Rasoi Mein"), ("in the Garden", "Bageeche Mein"), ("at the Beach", "Samundar Kinare"),
               ("in the Bedroom", "Kamre Mein"), ("at the Market", "Bazaar Mein"), ("at the Park", "Park Mein"), ("Under the Sea", "Samundar Ke Neeche"),
               ("at the Farm", "Khet Mein"), ("at the Zoo", "Chidiyaghar Mein"), ("in the Classroom", "Class Mein"),
               ("at Nani's House", "Nani Ke Ghar"), ("in the Car", "Gaadi Mein"), ("at the Masjid", "Masjid Mein"), ("in the Rain", "Baarish Mein"),
               ("at the Bakery", "Bakery Mein")]
SITUATIONS = [("at Home", "Ghar Par"), ("at the Park", "Park Mein"), ("at the Masjid", "Masjid Mein"), ("at School", "School Mein"),
              ("at the Market", "Bazaar Mein"), ("in the Car", "Gaadi Mein")]
LETTER_ANGLES = [("Sound", "Aawaaz"), ("Shape", "Shakal"), ("with Deeni", "Deeni Ke Saath"), ("with Bubbly", "Bubbly Ke Saath"),
                 ("Find It!", "Dhoondo!"), ("Write It!", "Likho!")]


# ---------------------------------------------------------------- visuals for the automatic renderer
AR_LETTERS = "ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي".split()
AR_DIGITS = ["١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩", "١٠"]
AR_NAMES = {"Ar-Rahman": "الرحمن", "Ar-Rahim": "الرحيم", "Al-Khaliq": "الخالق", "Ar-Razzaq": "الرزاق", "As-Salam": "السلام",
            "Al-Wadud": "الودود", "As-Sami'": "السميع", "Al-Basir": "البصير", "Al-Ghafur": "الغفور", "Al-Malik": "الملك"}
EMOJI = {
    # duas
    "Bismillah Before Eating": "🍽", "Alhamdulillah After Eating": "😋", "Dua Before Sleeping": "😴", "Dua When Waking Up": "🌅",
    "Saying Assalamu Alaikum": "👋", "Dua for Leaving the House": "🚪", "Mentioning Allah When Entering the House": "🏠",
    "Dua Before Entering the Toilet": "🚽", "Dua After Leaving the Toilet": "🧼", "Dua for Wearing Clothes": "👕",
    "Dua for Entering the Masjid": "🕌", "Dua for Leaving the Masjid": "🕌", "When We Sneeze: Alhamdulillah": "🤧",
    "Drinking Water in Three Sips": "💧", "Dua for Riding in a Car": "🚗", "Dua When It Rains": "🌧", "Saying InshaAllah": "🤲",
    "Saying MashaAllah": "🌟", "Saying SubhanAllah": "✨", "Saying Astaghfirullah": "🙏", "Saying JazakAllahu Khayran": "💝",
    "When I Feel Angry: A'udhu Billah": "😌", "Eating With the Right Hand": "✋", "Dua for Parents (Rabbir-hamhuma)": "👪",
    "Dua for Knowledge (Rabbi Zidni Ilma)": "📚", "Rabbana Atina Dua": "🤲", "Brushing Teeth: the Miswak Sunnah": "🪥", "Sitting Down to Drink": "🥛",
    # values
    "Honesty": "🤝", "Sharing": "🍪", "Kindness to Animals": "🐈", "Respecting Parents": "👪", "Helping at Home": "🧹", "Patience": "⏳",
    "Saying Sorry": "🙇", "Forgiving Others": "🤗", "Saying Thank You": "💐", "Being Gentle": "🕊", "Not Wasting Food": "🍚",
    "Saving Water": "🚰", "Keeping Promises": "🤝", "Tidying Up": "🧸", "Being a Good Neighbour": "🏘", "Big Feelings: Angry": "😠",
    "Big Feelings: Sad": "😢", "Big Feelings: Scared": "😨", "Big Feelings: Jealous": "😒", "Trying New Things": "🚲",
    "Taking Turns": "🎠", "Smiling is Sadaqah": "😁", "Being Grateful": "🤲", "Staying Clean": "🛁", "Kind Words": "💬",
    "Giving Charity": "💰", "Visiting Grandparents": "👵", "Respecting Teachers": "📚", "Caring for Plants": "🌱", "Including Everyone": "⚽",
    # preschool words
    "Red": "🔴", "Blue": "🔵", "Yellow": "🟡", "Green": "🟢", "Orange": "🟠", "Purple": "🟣", "Pink": "🌸", "Brown": "🟤",
    "Black and White": "⚫", "Rainbow Colours": "🌈", "Circle": "⚪", "Square": "🟥", "Triangle": "🔺", "Star": "⭐", "Heart": "❤",
    "Rectangle": "🟦", "Oval": "🥚", "Crescent": "🌙", "Camel": "🐪", "Cat": "🐈", "Cow": "🐄", "Sheep": "🐑", "Horse": "🐎",
    "Chicken": "🐔", "Elephant": "🐘", "Lion": "🦁", "Giraffe": "🦒", "Monkey": "🐒", "Bee": "🐝", "Ant": "🐜", "Butterfly": "🦋",
    "Bird": "🐦", "Owl": "🦉", "Duck": "🦆", "Rabbit": "🐇", "Goat": "🐐", "Penguin": "🐧", "Zebra": "🦓", "Bear": "🐻", "Frog": "🐸",
    "Parrot": "🦜", "Squirrel": "🐿", "Dates": "🌴", "Apples": "🍎", "Bananas": "🍌", "Grapes": "🍇", "Mangoes": "🥭",
    "Watermelon": "🍉", "Oranges": "🍊", "Olives": "🫒", "Strawberries": "🍓", "Carrots": "🥕", "Tomatoes": "🍅", "Potatoes": "🥔",
    "Cucumbers": "🥒", "Peas": "🫛", "Onions": "🧅", "Spinach": "🥬", "Eyes": "👀", "Ears": "👂", "Hands": "✋", "Feet": "🦶",
    "Teeth": "🦷", "Nose": "👃", "Sunny Day": "☀", "Rainy Day": "🌧", "Windy Day": "💨", "Cloudy Day": "☁", "Snowy Day": "❄",
    "Rainbow": "🌈", "The Sun": "☀", "The Moon": "🌙", "The Stars": "⭐", "Day and Night": "🌗", "Big and Small": "🐘",
    "Up and Down": "🎈", "Hot and Cold": "🔥", "Fast and Slow": "🐢", "Loud and Quiet": "📢", "Wet and Dry": "💧",
    "Mountains": "⛰", "Trees": "🌳", "Flowers": "🌷", "Car": "🚗", "Bus": "🚌", "Train": "🚆", "Aeroplane": "✈", "Boat": "⛵",
    "Bicycle": "🚲", "Fire Engine": "🚒", "Tractor": "🚜",
    # sea
    "Whale": "🐋", "Dolphin": "🐬", "Sea Turtle": "🐢", "Octopus": "🐙", "Jellyfish": "🪼", "Crab": "🦀", "Lobster": "🦞",
    "Clownfish": "🐠", "Pufferfish": "🐡", "Seal": "🦭", "Coral": "🪸", "Shrimp": "🦐", "Squid": "🦑", "Sea Otter": "🦦",
    "Angelfish": "🐠", "Oyster and Pearl": "🦪",
    # places
    "Coral Reef": "🐠", "Beach": "🏖", "Park": "🌳", "Garden": "🌻", "Farm": "🚜", "Zoo": "🦁", "Market": "🛒", "Masjid Garden": "🕌",
    "Kitchen": "🍳", "Picnic": "🧺", "Snow Day": "⛄", "Desert": "🐪", "Mountain": "⛰", "River": "🏞", "Night Sky": "🌌",
    "Bakery": "🥐", "Library": "📚", "Fruit Orchard": "🍊", "Bus Ride": "🚌",
    # count objects
    "Stars": "⭐", "Bubbles": "🫧", "Fish": "🐟", "Balloons": "🎈", "Ducks": "🦆", "Shells": "🐚", "Cars": "🚗", "Lanterns": "🏮",
    "Books": "📚", "Cats": "🐈", "Clouds": "☁", "Butterflies": "🦋",
}
SERIES_EMOJI = {"Islamic Basics & Surahs": "🕌", "Ramadan with Deeni": "🌙", "Hajj & Eid al-Adha": "🕋", "Eid Specials": "🎁",
                "Bedtime Lullabies": "🌙", "Arabic for Little Ones": "🔤", "Under the Sea with Deeni": "🐠", "Deeni & Bubbly Adventures": "🎒"}
BASICS_EMOJI = {"Fajr": "🌅", "Dhuhr": "☀", "Asr": "🌤", "Maghrib": "🌇", "Isha": "🌙", "Wudu": "💧", "Quran": "📖", "Kaaba": "🕋",
                "Zakat": "💰", "Fasting": "🌙", "Hajj": "🕋", "Qibla": "🧭", "Friday": "🛁", "Month": "🌙", "Dua": "🤲", "Charity": "💰"}
