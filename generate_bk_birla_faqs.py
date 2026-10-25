"""Script to generate verified FAQs for B.K. Birla College of Arts, Science & Commerce, Kalyan."""

import csv
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAQS_CSV = os.path.join(PROJECT_ROOT, "data", "faqs.csv")

FAQS = [
    {
        "id": 1,
        "category": "About College",
        "question": "Tell me about B.K. Birla College, Kalyan, its establishment, affiliation, and autonomous status.",
        "answer": "B.K. Birla College of Arts, Science & Commerce, Kalyan, was established in 1972 and is affiliated with the University of Mumbai. It holds NAAC 'A++' accreditation, ISO 9001:2015 certification, and has been granted Autonomous status for 2023–2033. The college features a lush, green 20-acre campus offering 33 undergraduate, 34 postgraduate, and 9 Ph.D. programs, along with vocational, diploma, and skill-based courses, as well as a Junior College (Class XI & XII).",
        "paraphrases": "What is B.K. Birla College?|Tell me about BK Birla College Kalyan|When was BK Birla College established?|Is BK Birla College autonomous and NAAC accredited?",
        "keywords": "bk birla college|kalyan|established 1972|mumbai university|naac a++|autonomous|iso 9001|20 acres|overview|about",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 2,
        "category": "Campus",
        "question": "What is the campus size and virtual tour facility of B.K. Birla College?",
        "answer": "B.K. Birla College spans a 20-acre lush green campus in Kalyan, Maharashtra, featuring modern classrooms, advanced science and computer labs, a Central Library, and recreational grounds. A 360° virtual campus tour is accessible online at https://bkbck.netlify.app/.",
        "paraphrases": "How big is the college campus?|Is there a virtual tour of BK Birla College?|What is the campus environment like?",
        "keywords": "campus|20 acres|green campus|virtual tour|bkbck netlify|kalyan|infrastructure",
        "source_url": "https://bkbck.netlify.app/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 3,
        "category": "Programs",
        "question": "What programs are offered in Junior College (Class 11 and 12)?",
        "answer": "The Junior College at B.K. Birla College offers Class XI and Class XII education across Arts, Commerce, and Science streams, as well as vocational courses. Candidates who have passed Class X (SSC) from the Maharashtra State Board or an equivalent recognized board are eligible.",
        "paraphrases": "Does BK Birla College have 11th and 12th?|What streams are in Junior College?|Junior college admission at BK Birla",
        "keywords": "junior college|class 11|class 12|xi|xii|arts|commerce|science|vocational|ssc",
        "source_url": "https://bkbck.edu.in/junior-college-admission-registration/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 4,
        "category": "Programs",
        "question": "What undergraduate Arts programs are available at B.K. Birla College?",
        "answer": "Undergraduate Arts offerings include B.A. in Economics, English, Geography, Hindi, History, Marathi, Philosophy, and Political Science. The college also offers B.A.M.M.C. (Bachelor of Arts in Multimedia & Mass Communication) and Bachelor of Sports Management.",
        "paraphrases": "What BA specializations are available?|Can I do BAMMC at BK Birla College?|What degree courses are in Arts?",
        "keywords": "arts|ba|bammc|multimedia|mass communication|sports management|economics|history|political science|english|marathi|hindi|geography|philosophy",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 5,
        "category": "Programs",
        "question": "What M.A. and Ph.D. programs are offered in Arts?",
        "answer": "In Arts, B.K. Birla College provides M.A. programs in History, Business Economics, Hindi, Marathi, and Political Science, alongside Master, Diploma, and Post Graduate Diploma in Sports Management. Ph.D. programs are available in Economics, Hindi, and History.",
        "paraphrases": "What master courses are in Arts?|Can I do MA or PhD in Arts at BK Birla?|Is Sports Management offered at postgraduate level?",
        "keywords": "ma|arts masters|phd arts|history|business economics|hindi|marathi|political science|sports management",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 6,
        "category": "Programs",
        "question": "What short-term and skill-based courses are offered in Arts?",
        "answer": "Short courses in Arts include Civil Services Aptitude Test (CSAT), Digital Skills with Microsoft 365, History in Competitive Exams, Spoken English, Sugam Marathi, and Travel and Tourism.",
        "paraphrases": "Are there certificate courses in Arts?|Does the college offer spoken english or civil services preparation?|What short courses can I take in Arts?",
        "keywords": "short courses|arts|csat|civil services|microsoft 365|spoken english|sugam marathi|travel and tourism",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 7,
        "category": "Programs",
        "question": "What undergraduate Commerce and Management courses are offered?",
        "answer": "Commerce and Management undergraduate programs include Bachelor of Commerce (B.Com), Bachelor of Banking and Insurance (BBI), Bachelor of Commerce in Management Studies / BMS (including a Logistics variant), B.Voc. in Financial Market & Trading Operations, Bachelor of Accounting and Finance (BAF), Bachelor of Business Management and Entrepreneurial Development (BBMED), and B.Com in Retail Management.",
        "paraphrases": "What courses are in Commerce?|Does the college offer BAF BBI and BMS?|What management degrees are offered at undergraduate level?",
        "keywords": "commerce|bcom|bbi|bms|management studies|baf|accounting and finance|banking insurance|logistics|financial market|bbmed|retail management",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 8,
        "category": "Programs",
        "question": "What postgraduate Commerce and Finance programs are available?",
        "answer": "Postgraduate offerings in Commerce and Management include Masters in Business Management, Masters in Accounting and Finance, Masters in E-Commerce, and M.Sc. in Finance.",
        "paraphrases": "What M.Com or finance master programs exist?|Can I do M.Sc. Finance or M.Com at BK Birla?|What postgraduate commerce degrees are offered?",
        "keywords": "postgraduate commerce|mcom|business management|accounting and finance|e-commerce|msc finance|masters",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 9,
        "category": "Programs",
        "question": "What Science departments and academic subjects are at B.K. Birla College?",
        "answer": "Science departments include Bioanalytical Sciences, Biotechnology, Botany, Chemistry, Computer Science & IT, Environmental Science, Event Management & PR, Food Science & Nutraceuticals, Mathematics, Microbiology, Physics, and Zoology.",
        "paraphrases": "What science branches exist?|Which science departments are in BK Birla College?|What subjects are taught in science?",
        "keywords": "science departments|biotechnology|botany|chemistry|microbiology|physics|zoology|environmental science|food science|maths",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 10,
        "category": "Programs",
        "question": "What specialized B.Sc., vocational, and BCA programs are available in Science?",
        "answer": "Specialized programs include B.Sc. (Honours) in Integrative Nutrition & Dietetics, B.Sc. (Honours) in Interior Design, B.Sc. in Event Management & PR (plus Diploma and PG Diploma), B.Voc. in Cyber Security & Forensics, B.Voc. in Medical Laboratory Technology (MLT), and BCA (Bachelor of Computer Applications).",
        "paraphrases": "Does BK Birla offer BCA?|Is there nutrition dietetics or interior design B.Sc.?|What vocational courses are in science?",
        "keywords": "bca|nutrition dietetics|interior design|event management|cyber security|medical laboratory technology|mlt|bvoc|science",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 11,
        "category": "Programs",
        "question": "What M.Sc. and Ph.D. programs are offered in Science disciplines?",
        "answer": "M.Sc. programs are offered in Bioanalytical Sciences, Biotechnology, Industrial Biotechnology, Botany, Analytical Chemistry, Organic Chemistry, Environmental Sciences, Food Science, Microbiology, Physics (Electronics), Zoology, and Event Management & PR. Ph.D. degrees are offered in Biotechnology, Botany, Chemistry, and Physics.",
        "paraphrases": "What MSc courses are in science?|Can I do PhD in Chemistry or Biotechnology?|What are the postgraduate science degrees?",
        "keywords": "msc|science masters|phd science|biotechnology|botany|chemistry|organic chemistry|analytical chemistry|physics|zoology|microbiology|environmental science",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 12,
        "category": "Programs",
        "question": "What certificate courses are available in Science and Technology?",
        "answer": "Science certificate courses include Astronomy, Robotics, Nanotechnology, Industrial Methods of Chemical Analysis, Environmental Monitoring, and Clinical Research.",
        "paraphrases": "What short term certificate courses are in science?|Can I learn astronomy robotics or clinical research?|What are the science certificate courses?",
        "keywords": "certificate courses|astronomy|robotics|nanotechnology|chemical analysis|environmental monitoring|clinical research",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 13,
        "category": "Programs",
        "question": "What Technology, Computer Science, IT, and AI programs are offered?",
        "answer": "Undergraduate technology degrees (unaided) include B.Sc. in Computer Science (BUS203), B.Sc. in Information Technology (BUS202), B.Sc. in Data Science (BUS211), B.Sc. in Cyber Security (BUS212), and B.Sc. in AI, Robotics & Automation (3 or 4 years). Postgraduate degrees (unaided, 2 years) include M.Sc. in Computer Science (BPSCS207), M.Sc. in IT - Cloud Computing (BPSCC221), M.Sc. in Data Science & Big Data Analytics (BPSBDA211), M.Sc. in Artificial Intelligence (BPSAI212), and M.Sc. in Cyber Security.",
        "paraphrases": "Does BK Birla offer AI and Data Science?|What courses are in Computer Science and IT?|Can I do M.Sc. in Artificial Intelligence or Cyber Security?",
        "keywords": "technology|bsc cs|bsc it|data science|cyber security|artificial intelligence|ai robotics|msc ai|cloud computing|big data|bus202|bus203",
        "source_url": "https://bkbck.edu.in/technology/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 14,
        "category": "Programs",
        "question": "What short courses in Technology and Computer Science are offered?",
        "answer": "Short-term courses in technology include AI for Leaders (duration: 3 months), Data Analytics Using Python, Game Development Using Scratch, Computer Hardware & Maintenance, and Robotics.",
        "paraphrases": "Are there python or game development courses?|What IT short courses are available?|Does the college offer AI for leaders or robotics certificate?",
        "keywords": "short courses tech|python|data analytics|game development|scratch|hardware|robotics|ai for leaders|3 months",
        "source_url": "https://bkbck.edu.in/technology/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 15,
        "category": "Programs",
        "question": "What international collaborations and value-based centres exist at B.K. Birla College?",
        "answer": "The college runs international programs including a Global Master's Program in partnership with Vistula University (Poland) and a Global Education Program. It also houses dedicated value-based education centres: Gandhian Studies, Dr. Ambedkar Studies, and Women Studies.",
        "paraphrases": "Does the college have international degree partnerships?|What is the Vistula University Poland collaboration?|What value based study centres are on campus?",
        "keywords": "international programs|vistula university|poland|global master|gandhian studies|ambedkar studies|women studies",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 16,
        "category": "Eligibility",
        "question": "What is the eligibility criteria for Junior College (Class XI and XII)?",
        "answer": "Admission to Class XI (Arts, Commerce, Science, or vocational) requires having passed Class X (SSC) from the Maharashtra State Board of Secondary and Higher Secondary Education or any recognized equivalent board.",
        "paraphrases": "How can I join 11th grade at BK Birla College?|What is the qualification for junior college?|Who is eligible for FYJC admission?",
        "keywords": "junior college eligibility|class 10|ssc|fyjc|11th admission|maharashtra board",
        "source_url": "https://bkbck.edu.in/junior-college-admission-registration/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 17,
        "category": "Eligibility",
        "question": "What is the eligibility criteria for B.A. and B.A.M.M.C. programs?",
        "answer": "For B.A. programs, applicants must have passed HSC (Class 12th) or equivalent from a recognized board; there is no fixed minimum cutoff percentage, and admission is based strictly on merit. For B.A.M.M.C. (Multimedia & Mass Communication), students must have passed Class XII in Arts, Science, or Commerce stream.",
        "paraphrases": "What marks are required for BA admission?|Who is eligible for BAMMC?|What is the minimum percentage for BA?",
        "keywords": "ba eligibility|bammc eligibility|12th marks|hsc|arts cutoff|mass media eligibility|merit",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 18,
        "category": "Eligibility",
        "question": "What are the eligibility requirements for BMS / B.Com (Management Studies)?",
        "answer": "Candidates must have passed Class XII (HSC) in one single sitting, or hold a 2–3 year engineering diploma post-SSC recognized by MSBTE. The candidate must have secured a minimum of 45% aggregate marks for the General/Open category, or 40% aggregate marks for Reserved categories.",
        "paraphrases": "What is the eligibility for BMS?|Can diploma students apply for B.Com Management Studies?|What percentage is needed for BMS?",
        "keywords": "bms eligibility|management studies|45 percent|open category|reserved category|diploma post ssc|single sitting",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 19,
        "category": "Eligibility",
        "question": "What is the eligibility for BAF, BBI, and Financial Management programs?",
        "answer": "For B.Com (Accounting & Finance - BAF), B.Com (Banking & Insurance - BBI), and Financial Management: Applicants must have passed Class XII (HSC) in one single attempt with a minimum of 45% aggregate marks for Open category, or 40% aggregate marks for Reserved categories.",
        "paraphrases": "What is the qualification for BAF?|What are the marks required for BBI?|Who is eligible for Accounting and Finance?",
        "keywords": "baf eligibility|bbi eligibility|accounting and finance|banking insurance|45 percent|single attempt|hsc",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 20,
        "category": "Eligibility",
        "question": "What are the eligibility criteria for B.Sc. Computer Science and B.Sc. IT?",
        "answer": "For B.Sc. Computer Science: Candidates must have passed Class XII with Mathematics and Statistics as compulsory subjects. For B.Sc. Information Technology (IT): Candidates must have passed Class XII with Mathematics, securing at least 45% aggregate marks (Open category) or 40% aggregate marks (Reserved category) in their first attempt.",
        "paraphrases": "What is the criteria for B.Sc. CS and B.Sc. IT?|Is maths compulsory for B.Sc. Computer Science?|What marks are needed for B.Sc. IT admission?",
        "keywords": "bsc cs eligibility|bsc it eligibility|computer science|information technology|mathematics compulsory|statistics|45 percent",
        "source_url": "https://bkbck.edu.in/technology/bachelor-of-science-in-information-technology/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 21,
        "category": "Eligibility",
        "question": "What is the eligibility requirement for B.Sc. Biotechnology?",
        "answer": "Applicants seeking admission to B.Sc. Biotechnology must have passed Class XII (HSC) in the Science stream with Mathematics as one of the subjects.",
        "paraphrases": "Can I get into Biotechnology without maths?|What is the eligibility for B.Sc. Biotechnology?|Who can apply for biotechnology?",
        "keywords": "biotechnology eligibility|bsc biotechnology|science stream|mathematics subject|hsc",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 22,
        "category": "Eligibility",
        "question": "What is the eligibility and selection process for Master's programs (M.A., M.Com, M.Sc.)?",
        "answer": "Admissions to M.A., M.Com., M.Com. (E-Commerce), and most M.Sc. programs are merit-based following University of Mumbai norms. However, admissions to M.Sc. Environmental Science and M.Sc. Bioanalytical Science require qualifying a college entrance examination.",
        "paraphrases": "How are postgraduate students selected?|Is there an entrance exam for M.Sc.?|What is the selection process for MA and MCom?",
        "keywords": "postgraduate eligibility|msc entrance exam|environmental science entrance|bioanalytical entrance|mcom eligibility|ma eligibility|merit",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 23,
        "category": "Eligibility",
        "question": "What is the admission procedure and eligibility for Ph.D. programs?",
        "answer": "Ph.D. admissions at B.K. Birla College are conducted in accordance with University of Mumbai guidelines. Candidates must qualify the Ph.D. Entrance Test (PET) or possess valid UGC-NET/SET/GATE exemptions, followed by personal interviews and research proposal defence before the Research Recognition Committee.",
        "paraphrases": "How do I apply for PhD at BK Birla College?|What is the qualification for doctorate programs?|Is PET exam required for PhD?",
        "keywords": "phd eligibility|doctorate|pet exam|mumbai university|ugc net|set|gate|research guides",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 24,
        "category": "Fees & Refund",
        "question": "What are the rules and deductions for admission cancellation and fee refund?",
        "answer": "Admission cancellation and refunds follow University of Mumbai Circular UG/412 of 2008 based on when you cancel: (1) Prior to term start: flat ₹500 deduction; (2) Up to 20 days after term starts: 20% of total fees deducted; (3) Day 21 to Day 50: 30% deducted; (4) Day 51 to Day 80 (or Aug 31 if earlier): 50% deducted; (5) Sept 1 to Sept 30: 60% deducted; (6) After Sept 30: 100% deduction (No refund). Caution, laboratory, and library deposits are 100% refundable.",
        "paraphrases": "What is the refund policy on admission cancellation?|How much fee is deducted if I cancel admission?|Can I get a fee refund after term starts?",
        "keywords": "fee refund|cancellation policy|circular ug 412 2008|deduction|500 rs|20 percent|50 percent|no refund after sept 30|refundable deposits",
        "source_url": "https://bkbck.edu.in/wp-content/uploads/2026/06/Fees-Structure.pdf",
        "last_updated": "2026-10-25"
    },
    {
        "id": 25,
        "category": "Fees & Refund",
        "question": "Which fee components are non-refundable upon admission cancellation?",
        "answer": "Non-refundable charges include group insurance, University share of fees (examination, enrollment, e-charges), ID card fee, library card fee, and admission form fee once the academic term commences. For courses admitted via Centralized Admission Processes (CAP), the governing authority's refund rules apply to first-year admissions.",
        "paraphrases": "What fees will not be refunded if I cancel?|Is exam fee or ID card fee refundable?|What are non refundable charges?",
        "keywords": "non-refundable fees|group insurance|university share|id card fee|library card fee|admission form|centralized admissions|cap round",
        "source_url": "https://bkbck.edu.in/wp-content/uploads/2026/06/Fees-Structure.pdf",
        "last_updated": "2026-10-25"
    },
    {
        "id": 26,
        "category": "Fees & Refund",
        "question": "Where can I find the official fee structure for courses at B.K. Birla College?",
        "answer": "The official course-wise fee structure for undergraduate and postgraduate courses is published in the Fees Structure document available at https://bkbck.edu.in/wp-content/uploads/2026/06/Fees-Structure.pdf.",
        "paraphrases": "What is the fee for each course?|Where can I download the fees structure PDF?|How much are the college fees?",
        "keywords": "fee structure|fees pdf|tuition fee|charges|course fee|bkbck fees structure",
        "source_url": "https://bkbck.edu.in/wp-content/uploads/2026/06/Fees-Structure.pdf",
        "last_updated": "2026-10-25"
    },
    {
        "id": 27,
        "category": "Admissions",
        "question": "How do I register for Degree College and Junior College admission?",
        "answer": "Degree College online admission registration is submitted at https://enrollonline.co.in/registration/apply/bkbc. Junior College registration is available at https://bkbck.edu.in/junior-college-admission-registration/. A detailed step-by-step admission process PDF can be accessed at https://bkbck.edu.in/wp-content/uploads/2026/04/Admission_Process.pdf.",
        "paraphrases": "Where is the admission registration portal?|How to apply for degree college admission?|What is the link to register for admission?",
        "keywords": "admission process|registration link|enrollonline|junior college registration|apply online|degree college admission",
        "source_url": "https://bkbck.edu.in/wp-content/uploads/2026/04/Admission_Process.pdf",
        "last_updated": "2026-10-25"
    },
    {
        "id": 28,
        "category": "Admissions",
        "question": "Are admissions for BCA and BMS conducted through CAP rounds?",
        "answer": "Yes, B.K. Birla College publishes CAP Round merit lists and notifications for AICTE-approved BCA (Bachelor of Computer Applications) and BMS (Bachelor of Management Studies) admissions on the college website and notice boards.",
        "paraphrases": "Is there a CAP round for BCA and BMS?|Where are the merit lists posted?|How to get admission in BCA and BMS?",
        "keywords": "cap round|bca admission|bms admission|merit list|aicte approval|counseling",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 29,
        "category": "Exams & Notices",
        "question": "What are the latest exam dates, NEP schedules, and ATKT deadlines?",
        "answer": "For Winter Session 2026, exam commencement notices have been announced for UG FY Sem-I and SY Sem-III (NEP) and PG Part-I Sem-I and Part-II Sem-III, along with deadlines for ATKT exam form submissions. Notices were posted on 24 September 2026 on the college portal.",
        "paraphrases": "When do Winter 2026 semester exams start?|What are the ATKT form submission dates?|What is the NEP exam schedule?",
        "keywords": "winter session 2026|exam dates|ug fy sem 1|sy sem 3|nep|pg sem 1|atkt form deadlines|september 2026",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 30,
        "category": "Exams & Notices",
        "question": "Are there any current faculty recruitment or hiring notices at B.K. Birla College?",
        "answer": "B.K. Birla College published an Assistant Professor (Unaided) recruitment advertisement on 19 August 2026. Interested candidates should review the notices section on the college website for eligibility and application procedures.",
        "paraphrases": "Is BK Birla College hiring teachers?|Are there assistant professor job openings?|What recruitment notices are published?",
        "keywords": "recruitment|hiring|assistant professor unaided|job vacancy|careers|august 2026",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 31,
        "category": "Facilities & Library",
        "question": "What library facilities and digital learning platforms are provided to students?",
        "answer": "The Central Library offers extensive print collections, reference sections, institutional memberships, and lending facilities. Students also receive access to premier digital platforms including Microsoft Teams, SWAYAM/NPTEL, IIT Bombay Spoken Tutorial, Shodhganga, and the National Digital Library of India (NDLI).",
        "paraphrases": "What library resources exist?|Can students use SWAYAM NPTEL and MS Teams?|Does the college have digital library access?",
        "keywords": "central library|books|swayam|nptel|ms teams|spoken tutorial|shodhganga|national digital library|ndli|digital resources",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 32,
        "category": "Campus",
        "question": "What co-curricular, sports, NCC, and student activities are available?",
        "answer": "The college hosts vibrant student activities including NCC (National Cadet Corps), NSS (National Service Scheme), sports grounds and competitions, the Centre for Yoga & Philosophy, Rotaract Club, and an active Student Council.",
        "paraphrases": "Does BK Birla College have NCC and NSS?|What clubs and sports are on campus?|Is there a Rotaract club and student council?",
        "keywords": "ncc|nss|sports|yoga and philosophy|rotaract club|student council|extracurricular|activities",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 33,
        "category": "Scholarships",
        "question": "What scholarships and financial assistance are offered to students?",
        "answer": "The college maintains a Scholarships & Endowment Prizes program, facilitating government reservation and merit scholarships. Furthermore, an industry partner has committed ₹20,25,000 specifically in skill scholarships for the academic years 2025–26 and 2026–27.",
        "paraphrases": "Are scholarships available at BK Birla College?|Can I get a fee concession or endowment prize?|What is the 20 lakh skill scholarship?",
        "keywords": "scholarships|endowment prizes|skill scholarships|2025000|government scholarship|financial aid|fee concession",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 34,
        "category": "Placements & Research",
        "question": "Does B.K. Birla College have a Placement Cell and campus recruitment support?",
        "answer": "Yes, B.K. Birla College operates a dedicated Placement Cell that coordinates with corporate recruiters, conducts campus recruitment drives, soft skills training, and facilitates student internships. Details can be found at https://bkbck.edu.in/placement-cell/.",
        "paraphrases": "How are the placements at BK Birla College?|Is there a placement cell?|Does the college provide campus placements and internships?",
        "keywords": "placement cell|campus placements|jobs|recruitment|internships|companies|career",
        "source_url": "https://bkbck.edu.in/placement-cell/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 35,
        "category": "Placements & Research",
        "question": "What research recognitions, DBT Star status, and FIST grants does the college hold?",
        "answer": "B.K. Birla College holds DBT Star College status and DST-FIST funding support. The institution actively engages in funded research projects, publications, houses a Patents Cell, and has recognized Ph.D. research guides across 9 disciplines.",
        "paraphrases": "Does the college have research grants?|What is DBT Star College and FIST status?|Is there a patents cell at BK Birla College?",
        "keywords": "research|dbt star college|dst fist funding|patents cell|phd guides|publications|projects",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 36,
        "category": "Campus",
        "question": "What student welfare, anti-ragging, and grievance committees are established?",
        "answer": "The college maintains essential statutory committees for student safety: Anti-Ragging Committee, Internal Complaints Committee (ICC), Students Grievance Redressal Cell, Prevention of Sexual Harassment (POSH) Committee, and an Entrepreneurship Cell (E-Cell).",
        "paraphrases": "Is there an anti ragging committee?|How to register a grievance or complaint?|What student safety committees exist?",
        "keywords": "anti ragging|grievance redressal|internal complaints|icc|posh|entrepreneurship cell|student safety|committees",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 37,
        "category": "About College",
        "question": "What are the institutional rankings and regulatory approvals of B.K. Birla College?",
        "answer": "B.K. Birla College participates in the National Institutional Ranking Framework (NIRF) with official ranking data published online. Its professional courses, including BCA (Bachelor of Computer Applications) and BMS (Bachelor of Management Studies), are officially approved by AICTE.",
        "paraphrases": "What is the NIRF ranking of BK Birla College?|Are BCA and BMS courses AICTE approved?|What accreditations does the college have?",
        "keywords": "nirf ranking|aicte approval|bca aicte|bms aicte|accreditations|approvals",
        "source_url": "https://bkbck.edu.in/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 38,
        "category": "Programs",
        "question": "What are the programme codes and durations for undergraduate Technology programs?",
        "answer": "Undergraduate Technology programs (unaided, 3 years unless noted) and their official programme codes are: (1) B.Sc. Computer Science (3 years) - Code: BUS203; (2) B.Sc. Information Technology (3 years) - Code: BUS202; (3) B.Sc. Data Science (3 years) - Code: BUS211; (4) B.Sc. Cyber Security (3 years) - Code: BUS212; and (5) B.Sc. AI, Robotics & Automation (3 or 4 years).",
        "paraphrases": "What is the programme code for B.Sc. IT and Computer Science?|What are the course codes for tech degrees?|What is BUS202 and BUS203?",
        "keywords": "programme code|bus202|bus203|bus211|bus212|bsc it code|bsc cs code|data science code|cyber security code|unaided",
        "source_url": "https://bkbck.edu.in/technology/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 39,
        "category": "Programs",
        "question": "What are the programme codes for postgraduate Technology programs?",
        "answer": "Postgraduate Technology programs (unaided, 2 years) and their official programme codes are: (1) M.Sc. Computer Science - Code: BPSCS207; (2) M.Sc. IT (Cloud Computing) - Code: BPSCC221; (3) M.Sc. Data Science & Big Data Analytics - Code: BPSBDA211; (4) M.Sc. Artificial Intelligence - Code: BPSAI212; and (5) M.Sc. Cyber Security (2 years).",
        "paraphrases": "What is the course code for M.Sc. AI or Computer Science?|What are the PG technology programme codes?|What is BPSAI212 and BPSCS207?",
        "keywords": "postgraduate codes|bpscs207|bpscc221|bpsbda211|bpsai212|msc ai code|msc cs code|cloud computing code|msc it",
        "source_url": "https://bkbck.edu.in/technology/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 40,
        "category": "About College",
        "question": "Who are the faculty and leadership of the IT and Computer Science department?",
        "answer": "The Department of Computer Science and IT has approximately 30 dedicated faculty members. Ms. Esmita Gupta serves as Senior Vice-Principal (Unit II), Chief Technology Officer (CTO), and Head of IT. The department also publishes a monthly technical newsletter titled 'TantrashAstra'.",
        "paraphrases": "Who is the Head of IT at BK Birla College?|Who is Esmita Gupta?|What is the TantrashAstra newsletter?|How many faculty are in computer science and IT?",
        "keywords": "esmita gupta|head of it|cto|senior vice principal|tantrashastra|newsletter|it faculty|computer science department|30 faculty",
        "source_url": "https://bkbck.edu.in/science/department-of-computer-science-and-it/it/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 41,
        "category": "Programs",
        "question": "What is the detailed syllabus and semester structure of B.Sc. Information Technology?",
        "answer": "B.Sc. IT follows the NEP 2020 credit framework with courses categorized as Major, Minor, VSC, SEC, AEC, VEC, IKS, and CC. As an autonomous institution, B.K. Birla College designs its own syllabus and examinations. Semester I (22 credits) includes Database Management System (DBMS), Computer Oriented Architecture, Mathematical Foundations of Information Science, Introduction to Programming (C++), Understanding e-Services, Effective Business Communication-I, and Indian Science and Technology. Semester II includes Computer Network, Operating System, Numerical Analysis with C++, Python Programming, Embedded System, Effective Business Communication-II, Environmental Science-II, and a SWAYAM course on yoga and positive psychology. Semesters III–VI tables, program outcomes, and course outcomes are available at https://bkbck.edu.in/science/department-of-computer-science-and-it/it/.",
        "paraphrases": "What subjects are taught in B.Sc. IT Semester 1 and 2?|What is the curriculum for B.Sc. Information Technology?|What courses are in first year B.Sc. IT?|Does B.Sc. IT follow NEP 2020?",
        "keywords": "bsc it syllabus|semester 1|semester 2|dbms|c++|python|embedded system|computer network|operating system|nep 2020|22 credits|swayam",
        "source_url": "https://bkbck.edu.in/science/department-of-computer-science-and-it/it/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 42,
        "category": "Programs",
        "question": "What are the certificate courses and durations in Technology and AI?",
        "answer": "The technology department offers certificate courses including: (1) AI for Leaders (duration: 3 months); (2) Robotics; (3) Data Analytics Using Python; (4) Game Development Using Scratch; and (5) Computer Hardware & Maintenance.",
        "paraphrases": "How long is the AI for Leaders certificate course?|What certificate courses does the tech department offer?|Is there python or scratch game development certificate?",
        "keywords": "ai for leaders|3 months|robotics|data analytics python|game development scratch|computer hardware|technology certificate",
        "source_url": "https://bkbck.edu.in/technology/",
        "last_updated": "2026-10-25"
    },
    {
        "id": 43,
        "category": "Fees & Refund",
        "question": "What are the estimated fees for B.Sc., M.Sc., and B.Com programs and how do aided vs. unaided courses differ?",
        "answer": "Fees differ significantly between government-aided and self-financed / unaided programs. The official source of truth is the college's official Fees Structure PDF at https://bkbck.edu.in/wp-content/uploads/2026/06/Fees-Structure.pdf. For general orientation, third-party aggregators (such as Careers360) estimate total 3-year fees for B.Sc. ranging from ₹25,000 up to ₹1.05 lakh (e.g., self-financed B.Sc. Computer Science is around ₹1.05 lakh), M.Sc. from ₹85,000 to ₹1.85 lakh, and B.Com from ₹22,000 to ₹62,000. Note: Ensure you consult B.K. Birla College in Kalyan, as some third-party platforms confuse it with Birla College in Thane.",
        "paraphrases": "How much does B.Sc. Computer Science cost?|What are the aided vs unaided fees?|What are the fee ranges for BSc MSc and BCom?|Is B.Sc. CS self financed?",
        "keywords": "estimated fees|aided vs unaided|bsc fees|msc fees|bcom fees|1.05 lakh|careers360|self financed|fees structure pdf|kalyan not thane",
        "source_url": "https://bkbck.edu.in/wp-content/uploads/2026/06/Fees-Structure.pdf",
        "last_updated": "2026-10-25"
    },
    {
        "id": 44,
        "category": "Placements & Research",
        "question": "What is the seat intake capacity and placement track record for Technology and general courses?",
        "answer": "Seat intake cohorts vary across programs (common intake sizes include 180, 60, 40, 30, and 25 seats). Student reviews describe campus placements as average, with visiting companies offering internships and recruitment drives. Third-party sources list recruiters such as Wipro, L&T, and Capgemini. Official placement updates and recruitment drives are managed by the Placement Cell at https://bkbck.edu.in/placement-cell/.",
        "paraphrases": "What companies recruit from BK Birla College?|Do Wipro and L&T recruit?|What are the seat intakes for courses?|How are placements according to student reviews?",
        "keywords": "seat intake|180|60|40|30|25|wipro|l&t|capgemini|student reviews|placements|internships|placement cell",
        "source_url": "https://bkbck.edu.in/placement-cell/",
        "last_updated": "2026-10-25"
    }
]


def write_faqs():
    fieldnames = [
        "id", "category", "question", "answer", "paraphrases", "keywords", "source_url", "last_updated"
    ]
    with open(FAQS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for faq in FAQS:
            writer.writerow(faq)
    print(f"Successfully wrote {len(FAQS)} verified FAQs to {FAQS_CSV}")


if __name__ == "__main__":
    write_faqs()
