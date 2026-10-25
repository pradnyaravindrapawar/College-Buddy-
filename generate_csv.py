import csv

faqs = [
    {
        "id": 1,
        "category": "Admissions",
        "question": "What are the eligibility criteria for B.Tech admission?",
        "answer": "Applicants must have passed 10+2 (Higher Secondary) with Physics and Mathematics as compulsory subjects along with Chemistry/Biotechnology/Computer Science, securing at least 60% aggregate marks (55% for reserved categories). Valid entrance test scores (JEE Main or College Entrance Test CET) are required.",
        "paraphrases": "How can I get admission into BTech?|What is the minimum percentage required for engineering admission?|What qualifications are needed for B.Tech?",
        "keywords": "admission|eligibility|btech|engineering|12th marks|jee main|aggregate",
        "source_url": "https://college.edu/admissions/eligibility",
        "last_updated": "2026-01-15"
    },
    {
        "id": 2,
        "category": "Admissions",
        "question": "What is the admission procedure and how do I apply?",
        "answer": "Applications must be submitted online through the college admissions portal at https://admissions.college.edu. Complete the registration form, upload scanned 10th and 12th marksheets, submit entrance exam rank cards, pay the application fee of $50/Rs.1200, and attend online counseling.",
        "paraphrases": "How do I apply for courses?|Where is the application form?|Steps to apply for admission",
        "keywords": "application|procedure|apply|portal|counseling|registration",
        "source_url": "https://college.edu/admissions/process",
        "last_updated": "2026-01-15"
    },
    {
        "id": 3,
        "category": "Admissions",
        "question": "What is the last date to submit the application form for admission?",
        "answer": "The deadline for submitting online undergraduate applications for the academic year 2026-27 is June 30, 2026. Late submissions with an additional late fee of Rs. 500 are accepted until July 10, 2026.",
        "paraphrases": "When is the application deadline?|Last date for admission form?|What is the cutoff date for applying?",
        "keywords": "deadline|last date|application deadline|cutoff date|late submission",
        "source_url": "https://college.edu/admissions/dates",
        "last_updated": "2026-02-01"
    },
    {
        "id": 4,
        "category": "Fees",
        "question": "What is the annual tuition fee for engineering programs?",
        "answer": "The annual tuition fee for B.Tech programs is Rs. 1,45,000 per year. Additional components include a one-time refundable caution deposit of Rs. 10,000, examination fees of Rs. 6,000 per year, and university development charges of Rs. 8,000.",
        "paraphrases": "How much are the engineering college fees?|What is the fee structure for B.Tech?|What is the annual cost of study?",
        "keywords": "fees|tuition|btech fee|cost|charges|caution deposit",
        "source_url": "https://college.edu/fees/btech",
        "last_updated": "2026-01-10"
    },
    {
        "id": 5,
        "category": "Fees",
        "question": "Can college tuition fees be paid in installments?",
        "answer": "Yes, tuition fees can be paid in two equal semester-wise installments. The first semester installment is due prior to registration in July, and the second installment is due by December 15th.",
        "paraphrases": "Is installment facility available for fees?|Can I pay fees semester wise?|Can I pay half fees now and half later?",
        "keywords": "installments|fee payment|semester fee|due date|payment options",
        "source_url": "https://college.edu/fees/policy",
        "last_updated": "2026-01-10"
    },
    {
        "id": 6,
        "category": "Fees",
        "question": "What is the refund policy if I cancel my admission?",
        "answer": "If admission cancellation is requested at least 15 days before the commencement of classes, 100% of the tuition fee is refunded after deducting a processing charge of Rs. 1,000. For cancellations up to 15 days after classes commence, 50% is refunded. No refund is granted after 30 days.",
        "paraphrases": "Can I get a fee refund if I withdraw?|What is the cancellation and refund policy?|How much fee will be refunded on cancellation?",
        "keywords": "refund|cancellation|withdrawal|money back|policy",
        "source_url": "https://college.edu/fees/refund",
        "last_updated": "2026-01-10"
    },
    {
        "id": 7,
        "category": "Scholarships",
        "question": "Are there merit-based or need-based scholarships available?",
        "answer": "Yes, the college offers Merit Scholarships covering up to 100% tuition fee waiver for top 5% rankers in entrance exams. Need-based financial aid is available for students whose family annual income is below Rs. 3,00,000. Government scholarships (SC/ST/OBC/Minority) are fully facilitated.",
        "paraphrases": "Do you provide scholarships?|Can I get financial aid or fee concession?|What are the criteria for fee waivers?",
        "keywords": "scholarship|merit|financial aid|fee concession|waiver|income",
        "source_url": "https://college.edu/scholarships",
        "last_updated": "2026-01-20"
    },
    {
        "id": 8,
        "category": "Hostel",
        "question": "What hostel facilities are provided and what is the room rent?",
        "answer": "The campus provides separate air-conditioned and non-AC hostels for boys and girls with 24/7 security, Wi-Fi, power backup, study rooms, and gym facilities. Annual hostel rent ranges from Rs. 65,000 for triple sharing (non-AC) to Rs. 1,10,000 for single occupancy (AC).",
        "paraphrases": "What are the hostel charges and room types?|Is hostel accommodation available?|How much does the college hostel cost?",
        "keywords": "hostel|accommodation|dorm|room rent|boys hostel|girls hostel|ac rooms",
        "source_url": "https://college.edu/campus/hostel",
        "last_updated": "2026-01-18"
    },
    {
        "id": 9,
        "category": "Hostel",
        "question": "What are the hostel rules, curfew timings, and leave policy?",
        "answer": "Hostel gates close strictly at 9:30 PM on weekdays and 10:00 PM on weekends. Night outs or weekend home visits require prior written approval and digital leave requests sent through the student ERP portal signed by registered parent/guardian contacts.",
        "paraphrases": "What is the curfew time for hostel students?|Can I stay out overnight from the hostel?|What happens if I come late to hostel?",
        "keywords": "curfew|hostel rules|gate timing|night out|leave permission|discipline",
        "source_url": "https://college.edu/campus/hostel-rules",
        "last_updated": "2026-01-18"
    },
    {
        "id": 10,
        "category": "Hostel",
        "question": "How is the mess food quality and what meal plans are offered?",
        "answer": "The hostel mess serves four nutritious vegetarian and non-vegetarian meals daily (breakfast, lunch, evening snacks, and dinner). The student mess committee inspects kitchen hygiene weekly and reviews monthly rotating menus. Mess charges are Rs. 42,000 per academic year.",
        "paraphrases": "What food is served in the hostel mess?|Is non-veg food available in mess?|What are the mess charges?",
        "keywords": "mess|food|dining|canteen|meals|diet|menu",
        "source_url": "https://college.edu/campus/dining",
        "last_updated": "2026-01-18"
    },
    {
        "id": 11,
        "category": "Exams",
        "question": "What is the grading system and CGPA calculation method?",
        "answer": "The college follows a 10-point relative grading scale: O (Outstanding - 10), A+ (Excellent - 9), A (Very Good - 8), B+ (Good - 7), B (Above Average - 6), C (Average - 5), and F (Fail - 0). Semester Grade Point Average (SGPA) and Cumulative GPA (CGPA) are weighted by course credits.",
        "paraphrases": "How is CGPA calculated?|What is the 10 point grading scale?|What is the passing grade?",
        "keywords": "cgpa|sgpa|grading system|marks|credits|grade scale|gpa",
        "source_url": "https://college.edu/academics/grading",
        "last_updated": "2026-02-05"
    },
    {
        "id": 12,
        "category": "Exams",
        "question": "What is the minimum attendance required to appear for semester exams?",
        "answer": "A minimum attendance of 75% in each enrolled theory and practical course is strictly mandatory to be eligible for end-semester examinations. Medical leave exemptions of up to 10% may be granted by the Dean of Academic Affairs upon submission of valid hospital records.",
        "paraphrases": "Is 75 percent attendance compulsory?|What happens if my attendance is low?|Can medical leave compensate for attendance shortage?",
        "keywords": "attendance|75 percent|exam eligibility|shortage|medical leave|condonation",
        "source_url": "https://college.edu/academics/attendance",
        "last_updated": "2026-02-05"
    },
    {
        "id": 13,
        "category": "Exams",
        "question": "What is the procedure for supplementary or backlog exams?",
        "answer": "Supplementary and backlog examinations are conducted twice a year, typically in January (for even semesters) and July (for odd semesters). Students must register on the examination portal and pay a backlog examination fee of Rs. 800 per subject.",
        "paraphrases": "When are backlog exams held?|How do I register for supplementary exams?|What is the re-exam process for failed subjects?",
        "keywords": "backlog|supplementary|re-exam|arrears|failed subject|exam portal",
        "source_url": "https://college.edu/academics/examinations",
        "last_updated": "2026-02-05"
    },
    {
        "id": 14,
        "category": "Placements",
        "question": "What were the placement statistics and highest package last year?",
        "answer": "In the previous academic year, 92% of eligible graduating students secured placements across 180+ visiting companies. The highest international package was Rs. 48 LPA, highest domestic package was Rs. 38 LPA, and the average salary package across B.Tech branches was Rs. 8.6 LPA.",
        "paraphrases": "What is the average and highest placement package?|How good are the college placements?|Which companies recruit from campus?",
        "keywords": "placements|highest package|average package|campus recruitment|salary|jobs",
        "source_url": "https://college.edu/placements/statistics",
        "last_updated": "2026-02-10"
    },
    {
        "id": 15,
        "category": "Placements",
        "question": "Which top companies visit the campus for recruitment and internships?",
        "answer": "Major recruiters include Google, Microsoft, Amazon, Infosys, TCS, Wipro, Cognizant, Deloitte, Accenture, L&T, Tata Motors, and Goldman Sachs. On-campus summer internship drives start in the 6th semester for 3rd-year engineering students.",
        "paraphrases": "Who are the key recruiting companies?|Do tech companies visit the college?|Is campus internship offered?",
        "keywords": "recruiters|companies|hiring|internships|campus placement|tech giants",
        "source_url": "https://college.edu/placements/recruiters",
        "last_updated": "2026-02-10"
    },
    {
        "id": 16,
        "category": "Placements",
        "question": "What are the eligibility criteria for participating in campus placements?",
        "answer": "To sit for campus placements, students must maintain a minimum CGPA of 6.5 with no active backlogs at the time of company registration. Some premium tier-1 companies mandate a minimum CGPA of 7.5 or 8.0 and no historical backlogs.",
        "paraphrases": "Can students with backlogs sit for placements?|What minimum CGPA is required for campus interviews?|Who is eligible for campus placement drives?",
        "keywords": "placement eligibility|cgpa criteria|active backlogs|campus drive|interview eligibility",
        "source_url": "https://college.edu/placements/policy",
        "last_updated": "2026-02-10"
    },
    {
        "id": 17,
        "category": "Facilities",
        "question": "What are the library timings and borrowing rules?",
        "answer": "The central library is open Monday through Saturday from 8:00 AM to 10:00 PM, and 24 hours during semester examination weeks. Undergraduate students can borrow up to 4 books simultaneously for a duration of 14 days with online renewal options.",
        "paraphrases": "When does the library open and close?|How many books can a student borrow from the library?|Is the library open late at night?",
        "keywords": "library|books|library timings|borrowing|reading room|digital library",
        "source_url": "https://college.edu/facilities/library",
        "last_updated": "2026-01-25"
    },
    {
        "id": 18,
        "category": "Facilities",
        "question": "What sports and recreational facilities are available on campus?",
        "answer": "The campus houses Olympic-standard sports facilities including a football ground, cricket pitch, synthetic basketball and tennis courts, badminton courts, an indoor table tennis hall, and a fully equipped gymnasium with trained physical instructors.",
        "paraphrases": "Does the college have a sports ground and gym?|What games and indoor sports are available?|Are sports coaches provided?",
        "keywords": "sports|gym|ground|football|cricket|basketball|indoor games|athletics",
        "source_url": "https://college.edu/facilities/sports",
        "last_updated": "2026-01-25"
    },
    {
        "id": 19,
        "category": "Facilities",
        "question": "What medical and healthcare facilities are on campus for students?",
        "answer": "A 24/7 health center is located on campus with two resident doctors, nursing staff, and a basic pharmacy providing primary healthcare and first aid free of charge to students. An emergency ambulance is stationed on campus around the clock.",
        "paraphrases": "Is there a doctor or dispensary on campus?|What should I do in case of a medical emergency?|Is there hospital support on campus?",
        "keywords": "medical|health center|doctor|dispensary|emergency|ambulance|pharmacy",
        "source_url": "https://college.edu/facilities/healthcare",
        "last_updated": "2026-01-25"
    },
    {
        "id": 20,
        "category": "Facilities",
        "question": "What Wi-Fi and computing lab facilities are accessible to students?",
        "answer": "High-speed Wi-Fi (1 Gbps leased line) is available across all academic buildings, hostels, and outdoor lawns. The college maintains six advanced computer laboratories with over 500 workstations equipped with Linux and Windows environments for programming and simulations.",
        "paraphrases": "Is there free Wi-Fi on campus?|How fast is the internet in hostels?|What computing labs are available?",
        "keywords": "wifi|internet|computer labs|workstations|bandwidth|network",
        "source_url": "https://college.edu/facilities/computing",
        "last_updated": "2026-01-25"
    }
]

fieldnames = ["id", "category", "question", "answer", "paraphrases", "keywords", "source_url", "last_updated"]

for target in ["data/sample_faqs.csv", "data/faqs.csv"]:
    with open(target, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(faqs)

print("Successfully written properly quoted CSV files.")
