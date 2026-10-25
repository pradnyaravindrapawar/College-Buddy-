"""Script to parse and generate all 224 verified FAQs for B.K. Birla College of Arts, Science & Commerce, Kalyan."""

import csv
import re
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAQS_CSV = os.path.join(PROJECT_ROOT, "data", "faqs.csv")

RAW_TEXT = """
## A. About the College

**1. What is the full name of the college?**
B. K. Birla College of Arts, Science & Commerce, Kalyan.

**2. Where is it located?**
In Kalyan, Maharashtra. Address and phone details are on the Contact Us page (bkbck.edu.in/contact-us/).

**3. When was the college established?**
In 1972.

**4. Which university is it affiliated with?**
The University of Mumbai.

**5. Is the college autonomous?**
Yes. It has Autonomous Status for 2023–2033.

**6. What NAAC grade does it hold?**
NAAC 'A++'.

**7. Does it have ISO certification?**
Yes, ISO 9001:2015.

**8. How big is the campus?**
About 20 acres, described as a green campus.

**9. How many programs does it offer?**
33 undergraduate, 34 postgraduate and 9 Ph.D. programs, plus vocational, diploma and skill-based courses.

**10. What is the college's motto or tagline?**
"Engaging, Nurturing, Transforming."

**11. Does the college have a Junior College?**
Yes, in Arts, Commerce and Science.

**12. Is the college government, aided or unaided?**
It has both. The site marks some programs as "Unaided" (for example, all Technology programs), and the faculty recruitment notice is for Assistant Professor (Unaided).

**13. Who is the college's revered patron?**
Pujya Syt. B. K. Birla Ji. The college posted a tribute on his 104th birth anniversary.

**14. What are the "B. K. Birla Institutes"?**
It's a section linked from the top of the website. I haven't read its contents, so check bkbck.edu.in/birla_institutes/.

**15. Is there a virtual campus tour?**
Yes, a 360° interactive tour at bkbck.netlify.app. It offers virtual tour, campus exploration, immersive views and free navigation.

**16. What is the official website?**
https://bkbck.edu.in/

**17. Does the college have an alumni network?**
Yes, there's an Alumni page for staying connected with the college.

**18. Which social media pages does it have?**
Facebook, YouTube, Instagram and LinkedIn.

**19. Does the college publish a blog, news and events?**
Yes. The site has Blog, News, Events, Notices and Achievements sections.

**20. What is Mpower?**
It's the college's online portal. Students and faculty log in through it (via the MastersoftERP/CIMS system).

**21. Where can students log in?**
Through the "Student" link on the site (cimsstudentnewui.mastersofterp.in). Faculty use a separate "Faculty" login.

**22. Does the college have a photo and video gallery?**
Yes, there's a Gallery page with photos and videos.

## B. Accreditation, Rankings and Recognition

**23. What is the IQAC?**
The Internal Quality Assurance Cell. The site has pages for About IQAC, member list, minutes reports and annual reports.

**24. Where can I find NAAC documents?**
Under the IQAC & NAAC menu: About NAAC, IIQA undertaking, IQAC criteria, AQAR best practices and the SSR best practices.

**25. Does the college publish AQARs?**
Yes. There's an AQAR Lists page, and the 2023–24 Best Practices I and II PDFs.

**26. Is the college ranked under NIRF?**
The site has NIRF Overall, NIRF College and NIRF feedback pages. The rank itself is on those pages.

**27. Is the college AICTE approved?**
For its AICTE-regulated programs, yes. The site publishes the AICTE Letter of Approval, Letter of Extension, Mandatory Disclosures, Brochure, Syllabus and Admission Notice.

**28. Which courses are AICTE-linked?**
The notices mention F.Y.B.C.A. (BCA) and F.Y.B.M.S. as "AICTE (NEP)" courses.

**29. What is "Institutional Distinctiveness"?**
It's a page under IQAC & NAAC describing what makes the college distinctive.

**30. What is the "College of Excellence"?**
A "Proud Moments" page showing the college's College of Excellence recognition.

**31. Is the college a DBT Star College?**
Yes. The site has a DBT Star College section, with reports from the Department of Zoology.

**32. What is FIST?**
Fund for Improvement of S&T Infrastructure. The college has a FIST page.

**33. Has the college won any security award?**
Yes, the Payment Security Excellence Award 2025 from the PCI Security Standards Council, supported by DSCI, the Cyber Security Association of India and ISACA Mumbai Chapter.

**34. Does the college have a patents cell?**
Yes. Dr. Narayan Totewad of Microbiology was also congratulated for a UK Design Patent.

**35. Are there rules about public disclosure?**
The site publishes the "Guidelines on Public Self-Disclosure by Higher Education Institutions" PDF.

**36. Does the college follow RTI?**
Yes, there's a Right To Information page.

## C. Programs Overview

**37. What streams does the Degree College offer?**
Arts, Commerce, Science, Technology, Management and New Age Programs.

**38. What are "New Age Programs"?**
A separate category on the site. I haven't read its contents; see bkbck.edu.in/new-age-programs/.

**39. Does the college offer Ph.D. programs?**
Yes (9 in total). Examples: Economics, Hindi, History, Biotechnology, Botany, Chemistry, Physics.

**40. Where is the list of Ph.D. guides?**
A "List of Ph.D. Guides" PDF is under Knowledge Hub → Research.

**41. Does the college follow NEP 2020?**
Yes. It has an NEP 2020 booklet, an NEP Cell and an Examination Manual under NEP 2020.

**42. What is the OBE Manual?**
The Outcome-Based Education manual, published on the site, with an OBE Committee.

**43. What is the Standard Operating Procedure document?**
A PDF listed under Academics that sets out the college's procedures.

**44. What certificate and short courses are available?**
Examples: Spoken English, Sugam Marathi, Travel and Tourism, Digital Skills with Microsoft 365, Civil Services Aptitude Test, History in Competitive Exams, AI for Leaders, Data Analytics Using Python, Robotics, Astronomy and Nanotechnology.

**45. Does the college offer diplomas?**
Yes, for example Diploma in Sports Management, Diploma in Event Management & PR, and Post Graduate Diplomas in Sports Management and Event Management & PR.

**46. Does the college offer vocational degrees?**
Yes, B.Voc. in Financial Market & Trading Operations, Cyber Security & Forensics, and Medical Laboratory Technology.

## D. Arts Programs

**47. Which B.A. subjects are offered?**
Economics, English, Geography, Hindi, History, Marathi, Philosophy and Political Science.

**48. Is B.A.M.M.C. available?**
Yes, Bachelor of Arts in Multimedia and Mass Communication.

**49. What sports management programs are offered?**
Bachelor (BSM), Diploma (DSM), Post Graduate Diploma (PGDSM) and Master (MSM) of Sports Management.

**50. Which M.A. programs are offered?**
History, Business Economics, Hindi, Marathi and Political Science.

**51. Which Ph.D. programs are in Arts?**
Economics, Hindi and History.

**52. Is there a course for civil services aspirants?**
Yes, the Civil Services Aptitude Test course.

**53. Is there a course for History in competitive exams?**
Yes, "History in Competitive Exams."

**54. Is there a Spoken English course?**
Yes, listed under Arts.

**55. What is Sugam Marathi?**
A Marathi language course under Arts. See its page for details.

**56. Is a Travel and Tourism course available?**
Yes, under Arts.

**57. What is "Digital Skills with Microsoft 365"?**
A skill course under Arts that covers Microsoft 365 tools.

**58. What are the eligibility rules for B.A.?**
Pass HSC (12th) or an equivalent exam. There's no fixed minimum percentage, but admission is merit-based.

**59. What are the eligibility rules for B.A.M.M.C.?**
Pass Class XII (Maharashtra State Board or equivalent) in Arts, Science or Commerce.

## E. Commerce and Management Programs

**60. Which Commerce programs are offered?**
B.Com, Bachelor of Banking and Insurance, B.Com (Management Studies), B.Com (Management Studies) Logistics, B.Voc. in Financial Market & Trading Operations, and Masters in Business Management.

**61. Which Management programs are offered?**
Bachelor of Accounting and Finance, Bachelor of Business Management and Entrepreneurial Development, B.Com Retail Management, M.Com (Business Management), M.Sc. Finance, Masters in Accounting and Finance, and Masters in E-Commerce.

**62. Is BMS offered?**
Yes, as B.Com (Management Studies), also called B.M.S.

**63. Is there a Logistics specialization?**
Yes, Bachelor of Commerce (Management Studies) Logistics.

**64. Is there a Retail Management program?**
Yes, Bachelor of Commerce in Retail Management.

**65. Is there an entrepreneurship-related degree?**
Yes, the Bachelor of Business Management and Entrepreneurial Development. The college also has an Entrepreneurship Cell.

**66. Which postgraduate Commerce programs are offered?**
M.Com (Business Management), Masters in Accounting and Finance, Masters in E-Commerce, and M.Sc. Finance.

**67. What is the eligibility for B.Com (Management Studies)?**
Pass Class XII in one sitting (or a 2–3 year engineering diploma after SSC), with at least 45% (Open) or 40% (Reserved).

**68. What is the eligibility for B.Com (Accounting & Finance)?**
Pass Class XII with at least 45% aggregate (40% Reserved) in one sitting.

**69. What is the eligibility for B.Com (Banking & Insurance)?**
Pass Class XII with at least 45% aggregate (40% Reserved) in one sitting.

**70. What is the eligibility for B.Com (Financial Management)?**
The same: Class XII with at least 45% aggregate (40% Reserved) in one sitting.

**71. Can diploma holders join B.Com (Management Studies)?**
Yes, those with a 2- or 3-year engineering diploma from the Maharashtra Board of Technical Education after SSC, meeting the marks requirement.

**72. Does "one sitting" mean anything specific?**
Yes. The required marks must be obtained in a single attempt of the Class XII exam.

**73. Are BMS and BCA admissions advertised separately?**
Yes. The site posted an "Advertisement for BCA & BMS" notice and AICTE-related notices.

**74. Which postgraduate admissions are merit-based?**
M.A., M.Com., M.Com. (E-Commerce) and most M.Sc. programs, as per University norms.

## F. Science Programs

**75. Which science departments exist?**
Bioanalytical Sciences, Biotechnology, Botany, Chemistry, Computer Science & IT, Environmental Science, Event Management & PR, Food Science & Nutraceuticals, Mathematics, Microbiology, Physics and Zoology.

**76. Which B.Sc. programs are offered under Science?**
Biotechnology, Botany, Chemistry, Mathematics, Microbiology, Physics, Zoology, and Event Management & PR. Computer Science and IT-related degrees are listed under Technology.

**77. Are there Honours programs?**
Yes: B.Sc. (Honours) in Integrative Nutrition and Dietetics, and B.Sc. (Honours) in Interior Design.

**78. Is BCA offered?**
Yes, the Bachelor of Computer Applications is under the Department of Computer Science & IT.

**79. What B.Voc. programs does Science include?**
B.Voc. Cyber Security & Forensics and B.Voc. Medical Laboratory Technology.

**80. Which M.Sc. programs are offered in Science?**
Bioanalytical Sciences, Biotechnology, Industrial Biotechnology, Botany, Analytical Chemistry, Organic Chemistry, Environmental Sciences, Food Science, Microbiology, Physics (Electronics), Zoology, and Event Management & PR.

**81. Which Ph.D. programs are in Science?**
Biotechnology, Botany, Chemistry and Physics.

**82. Which certificate courses does the Physics department offer?**
Certificate Courses in Astronomy and in Robotics.

**83. What certificate courses does Chemistry offer?**
Industrial Methods of Chemical Analysis and Nanotechnology.

**84. What short courses does Environmental Science offer?**
Environmental Monitoring, Environmental Nanotechnology, and Heavy Metal Analysis of Environmental Samples.

**85. What does Bioanalytical Sciences offer beyond the M.Sc.?**
Analytical Instrumentation, Clinical Research, and an EHS (Environment, Health & Safety in analytical labs) course.

**86. Is Event Management a full degree path?**
Yes. B.Sc., M.Sc., Diploma (DEM) and PG Diploma (PGDEM) in Event Management & Public Relations.

**87. What is the eligibility for B.Sc. Biotechnology?**
Pass Class XII with Mathematics as one of the subjects.

**88. Which M.Sc. programs require an entrance exam?**
M.Sc. Environmental Science and M.Sc. Bioanalytical Science.

**89. How are other M.Sc. admissions decided?**
On merit, as per University norms (Physics, Chemistry, Botany, Zoology, Microbiology, Biotechnology, Computer Science, IT).

**90. Is the Zoology department notable?**
It is linked with the DBT Star College scheme, with published reports.

## G. Technology Programs

**91. Which undergraduate Technology programs are offered?**
B.Sc. Computer Science, B.Sc. IT, B.Sc. Data Science, B.Sc. Cyber Security, and B.Sc. AI, Robotics & Automation.

**92. How long are these undergraduate programs?**
3 years. B.Sc. AI, Robotics & Automation is listed as 3 or 4 years.

**93. What are the programme codes?**
B.Sc. CS: BUS203. B.Sc. IT: BUS202. B.Sc. Data Science: BUS211. B.Sc. Cyber Security: BUS212.

**94. Which postgraduate Technology programs are offered?**
M.Sc. Computer Science, M.Sc. IT (Cloud Computing), M.Sc. Data Science & Big Data Analytics, M.Sc. Artificial Intelligence, and M.Sc. Cyber Security.

**95. How long are the M.Sc. programs?**
2 years.

**96. What are the M.Sc. programme codes?**
Computer Science: BPSCS207. IT (Cloud Computing): BPSCC221. Data Science & Big Data: BPSBDA211. AI: BPSAI212. Cyber Security: none listed.

**97. Are the Technology programs aided or unaided?**
They are listed as unaided.

**98. Which certificate courses are in Technology?**
AI for Leaders (3 months), Robotics, Data Analytics Using Python, Game Development Using Scratch, and Computer Hardware & Maintenance.

**99. How long is "AI for Leaders"?**
3 months.

**100. Who heads the IT department?**
Ms. Esmita Gupta, who is also Senior Vice-Principal (Unit II) and Chief Technology Officer.

**101. How big is the CS & IT faculty?**
About 30 faculty members are listed.

**102. Does the department publish a newsletter?**
Yes, "TantrashAstra," published monthly (June, July and August 2026 issues are online).

**103. What does the B.Sc. IT program cover?**
Programming, networking, databases, web development, cybersecurity, data analytics, and emerging areas such as AI and IoT.

**104. What is the eligibility for B.Sc. IT?**
Class XII (Maharashtra Board or equivalent) with Mathematics, and at least 45% (Open) or 40% (Reserved) at first attempt.

**105. What is the eligibility for B.Sc. Computer Science?**
Class XII with Mathematics and Statistics as one of the subjects.

**106. What does Semester I of B.Sc. IT include?**
Database Management System, Computer Oriented Architecture, Mathematical Foundations of Information Science, Introduction to Programming (C++), Understanding e-Services, Effective Business Communication-I and Indian Science and Technology.

**107. How many credits is Semester I of B.Sc. IT?**
22 credits.

**108. What does Semester II of B.Sc. IT include?**
Computer Network, Operating System, Numerical Analysis with C++, Python Programming, Embedded System, Effective Business Communication-II, Environmental Science-II and a SWAYAM yoga course.

**109. Which programming languages appear in the first-year B.Sc. IT?**
C++ in Semester I and Python in Semester II.

**110. Does B.Sc. IT include a yoga or wellness course?**
Yes, "Yoga & Positive Psychology for managing career & life" through SWAYAM.

**111. What kinds of paper categories appear in the syllabus?**
Major, Minor, VSC, SEC, AEC, VEC, IKS and CC, which follow the NEP 2020 credit framework.

**112. Does the B.Sc. IT syllabus include Indian Knowledge Systems?**
Yes, "Indian Science and Technology" is an IKS paper in Semester I.

**113. Does the program include community engagement?**
Yes, a CEP Community Engagement Services course appears among the course outcomes.

**114. Does the IT course mention IoT?**
Yes. One course outcome covers designing and programming IoT devices.

**115. Where can I read the full IT syllabus?**
On the B.Sc. IT page: bkbck.edu.in/science/department-of-computer-science-and-it/it/

**116. Are course outcomes published?**
Yes, along with program outcomes (PO) on the course pages.

**117. Is there a separate B.Sc. Computer Science syllabus PDF?**
An older syllabus PDF is online (on the www.bkbck.edu.in file server). It lists courses like Digital Systems & Architecture and Python programming.

## H. Eligibility and Qualifying Exams

**118. What is the Junior College (XI/XII/Vocational) eligibility?**
Pass Class X (Maharashtra State Board or equivalent).

**119. Is a minimum percentage required for B.A.?**
No fixed minimum, but admission is merit-based.

**120. Do Reserved Category students get lower cut-offs?**
Yes, on programs that specify them: 40% instead of 45% for BMS, B.Com variants and B.Sc. IT.

**121. Which programs require Mathematics in Class XII?**
B.Sc. IT, B.Sc. Biotechnology and B.Sc. Computer Science (with Statistics).

**122. Can students from other boards apply?**
Yes, where the page says "or an equivalent" board or examination.

**123. Can Commerce students apply to B.A.M.M.C.?**
Yes. Arts, Science and Commerce graduates of Class XII are eligible.

**124. Is B.Sc. IT open to Commerce students?**
Only if they studied Mathematics in Class XII and meet the percentage requirement.

**125. Can diploma holders join B.Sc. programs?**
The site only mentions the diploma route for B.Com (Management Studies).

**126. What about eligibility for Ph.D.?**
The site tells you to refer to the University website.

**127. What does "first attempt" mean for B.Sc. IT?**
The required marks must be earned in your first attempt at the qualifying exam.

## I. Admission Process

**128. How do I apply for Degree College admission?**
Register online at enrollonline.co.in/registration/apply/bkbc.

**129. How do I apply to Junior College?**
Through the Junior College Admission Registration page on the site.

**130. Is there a detailed admission process document?**
Yes, an "Admission Process" PDF (not readable in my tools), so open it from the Admission menu.

**131. Is there an "Apply Now" button?**
Yes, on the site header and pages.

**132. Is there an Enquire Now form?**
Yes, a floating "Enquire Now" form on the site.

**133. Does the college publish merit lists?**
Yes. It has posted CAP Round Merit List III and Institute Quota Merit List 3.

**134. What is the CAP round?**
The Centralized Admission Process used for some courses. The college uses it for certain programs and also has an Institute Quota.

**135. Is there an Institute Quota?**
Yes, merit lists for it are published.

**136. Are admissions merit-based?**
Mostly. A few programs (M.Sc. Environmental Science, Bioanalytical Science) use entrance exams.

**137. Where are admission notices posted?**
Under Admission → Admission Notice, and in the Notices section.

**138. Are there fee waivers for some categories?**
The site has a Scholarships & Endowment Prizes page. Check it for current schemes.

**139. Does the college mention committees for SC/ST, OBC and minorities?**
Yes: Committee for SC/ST, OBC Cell and Minority Cell.

**140. Where do I read the admission cancellation rules?**
Admission → Rules & Regulations for Cancellation.

**141. Is there an Anti-Ragging Cell?**
Yes, under Committees and Cells.

## J. Fees, Refunds and Cancellation

**142. Where is the official fee structure?**
In the "Fees Structure" PDF under Academics (bkbck.edu.in/wp-content/uploads/2026/06/Fees-Structure.pdf).

**143. What are the total fees for each course?**
I couldn't read the PDF, so I can't state them. Please check the PDF or the admission office.

**144. Are fees the same for aided and unaided programs?**
No. Third-party sources show wide ranges, and the official PDF is the source of truth.

**145. What do third-party sites say about B.Sc. fees?**
One site lists a range of about ₹25,000 to ₹1.05 lakh in total. This is unofficial and can mix up similarly named colleges.

**146. What are cancellation deductions before the term starts?**
₹500 lump sum.

**147. What is deducted up to 20 days after the term starts?**
20% of total fees.

**148. What about days 21 to 50?**
30% of total fees.

**149. What about days 51 to 80 (or Aug 31, whichever is earlier)?**
50% of total fees.

**150. What if I cancel between September 1 and 30?**
60% of total fees.

**151. What if I cancel after September 30?**
100% of fees are retained (no refund).

**152. When is the refund paid?**
On or before the 30th day after the cancellation date.

**153. How do I request cancellation?**
In writing, applying for cancellation of admission.

**154. Which university rule governs refunds?**
University of Mumbai Circular No. UG/412 of 2008.

**155. Which fees are non-refundable?**
Group insurance, and University-share items already paid (exam fee, enrollment fee, sports and cultural fee, e-charge, disaster management fund, Vice-Chancellor fund).

**156. Are ID card and library card fees refundable?**
Not after the academic term begins. The same goes for admission form and prospectus fees.

**157. Are lab or library deposits refunded?**
Yes, refundable deposits such as laboratory, caution money and library are fully returned on cancellation.

**158. Do different rules apply for centralized admissions?**
Yes. If another authority sets refund rules for the centralized process, those apply to first-year admissions.

**159. What applies to subsequent-year cancellations?**
The "0.2859 rule" applies.

**160. Does the college offer EMI or installment plans?**
Not mentioned on the pages I read. Ask the accounts office.

## K. Examinations

**161. Does the college conduct its own exams?**
Yes, as an autonomous college it conducts exams on its own syllabus.

**162. Where do I find exam timetables?**
Examination → Exam Timetable.

**163. Where are admit cards issued?**
Examination → Admit Card.

**164. Where can I check results?**
Examination → Results – Degree College.

**165. Is there an examination manual?**
Yes, the "Examination Manual (NEP 2020)."

**166. What is the Board of Examination page for?**
It lists the exam governing board.

**167. Are circulars posted?**
Yes, under Circular Notifications.

**168. When do Winter Session 2026 exams start?**
Commencement notices for UG FY Sem-I and SY Sem-III (NEP) and PG Part-I Sem-I and Part-II Sem-III were posted on September 24, 2026. See the notices for exact dates.

**169. Are ATKT (backlog) exams offered?**
Yes, for both UG and PG, with exam form and fee notices (the PG deadline was extended in September 2026).

**170. How does PG exam structure work?**
Notices refer to Part-I Semester I/II and Part-II Semester III/IV, under both NEP and Old patterns.

**171. Are there UG ATKT notices for BCA/BMS?**
Yes, a notice for F.Y.B.C.A./F.Y.B.M.S. Semester II (AICTE, NEP) ATKT forms, posted September 8, 2026.

**172. Where are exam rules published?**
Examination → Rules & Regulations.

**173. Is there an academic calendar?**
Yes, under IQAC & NAAC → Academic Calendars.

## L. Student Life and Support

**174. Does the college have an NCC unit?**
Yes.

**175. Does it have an NSS unit?**
Yes, National Service Scheme.

**176. Does it support sports?**
Yes. There's a Sports page and a Gymkhana Committee. Students have won national-level honors (see Q 202–203).

**177. Is there a Yoga centre?**
Yes, the Centre for Yoga & Philosophy.

**178. Is there a Rotaract Club?**
Yes (rcbkbirla.com).

**179. Does the college have a Student Council?**
Yes, with a council list and an annual report.

**180. What is the Mentor–Mentee Handbook?**
A PDF explaining the mentoring system between faculty and students.

**181. Is there a student satisfaction survey?**
Yes, "Student Satisfaction Analysis."

**182. Are there student achievers pages?**
Yes, "Student Achievers."

**183. Where are student rules published?**
Student Corner → Rules and Regulations, and a Code of Conduct PDF.

**184. What associations exist?**
Arts Circle, Commerce Association, Science Association and Social Sciences Association.

**185. Is there a canteen committee?**
Yes.

**186. Is there a magazine committee?**
Yes.

**187. Is there a grievance cell?**
Yes, the Grievance Redressal Cell.

**188. How does the college handle harassment complaints?**
Through the Internal Complaints Committee and the POSH Committee.

**189. Is there a safety committee?**
Yes.

**190. Is there an attendance committee?**
Yes, and a Monitoring Committee.

**191. Does the college have a hostel?**
The pages I read don't confirm this. Third-party sites are inconsistent, so ask the college directly.

## M. Library, Research and Learning Resources

**192. Does the college have a library?**
Yes, a Central Library with infrastructure and institutional-membership pages.

**193. Are library timings published?**
Yes, on the Library Timings page.

**194. Is there a library membership guideline?**
Yes, "Guidelines for Membership."

**195. What research resources are listed?**
Projects, Publications, Department-Wise Research Data and the Ph.D. guides list.

**196. Does the college use online learning tools?**
Yes, MS Teams under "E-ABHYAS," plus a Netiquette Guide for Online Learning.

**197. Can students take SWAYAM/NPTEL courses?**
Yes. The site lists certificate details, active SPOC certificates and a local chapter.

**198. Does the college offer IIT Bombay Spoken Tutorials?**
Yes, with a course list and a list of students who completed them.

**199. Which open resources does it point to?**
Shodhganga, the National Digital Library of India and a list of open-access resources.

**200. Does the college offer extension services?**
Yes, plus a Department of Lifelong Learning and Extension.

## N. Scholarships, Placements and Achievements

**201. Does the college offer scholarships?**
Yes. See Student Corner → Scholarships & Endowment Prizes.

**202. Is there an industry scholarship?**
Yes. An Industry Skill Scholarship Partner was recognized for 2025–26 and 2026–27 with a total commitment of ₹20,25,000 for students.

**203. Has the college produced sports achievers?**
Yes: Isha Bhagat won silver at the Under-20 National Triathlon Championship, and Pratiksha Bhoir (FYBA) took second place at the Junior National Rugby 7s Championship 2026.

**204. Do alumni get into civil services?**
One example: Shivkumar Jadhav (M.A. Business Economics, 2023–24 batch) was appointed Dy. CEO/Block Development Officer through MPSC Civil Service Exam 2024–25.

**205. Have students won research competitions?**
Yes. Vivek Das (TYBMS Marketing) won 1st prize in research paper presentation at the 2nd Asia Pacific International Conference, and Ms. Saroj Iyengar and Dr. Suraj Agarwala won Best Research Paper at D. G. Ruparel College (April 2025).

**206. Is there a Placement Cell?**
Yes: bkbck.edu.in/placement-cell/

**207. Which companies recruit?**
I couldn't verify this on the official site. Third-party pages mention Wipro, L&T and Capgemini, so check the Placement Cell page.

**208. What do students say about placements?**
Student reviews on third-party sites say placements are average, with some internships offered.

**209. Are there corporate events on campus?**
Yes, for example "Pantaloons comes to B.K. Birla College" (July 2025) and an Entrepreneurship & Start-up Clinic session.

**210. Are there tech events?**
Yes, such as a Robotics and 3D-Printing Workshop (July 2025) and "Test your tech IQ" (August 2025).

## O. Junior College, International and Value-Based Programs

**211. Which streams does the Junior College offer?**
Arts, Commerce and Science (XI and XII), plus vocational courses.

**212. Where do I register for Junior College?**
bkbck.edu.in/junior-college-admission-registration/

**213. What is the Global Master's Program?**
An international program with Vistula University (Poland), promoted as "Study in Europe." See its page for details.

**214. What is the Global Education Program?**
A program (PGDGE, teacher training) offered through a partner site (abea.in). The college links to it.

**215. What are the Value Based Education centres?**
The Gandhian Studies Centre, Dr. Ambedkar Studies Centre and Women Studies Centre.

**216. Does the college have an Indian Knowledge Systems centre?**
Yes. News mentions a Center for IKS that held an Ayurveda Day pledge.

**217. Are there environmental initiatives?**
Yes, the Eco Sensitive Campus page, and the Environmental Sciences department celebrated World Ozone Day.

## P. Governance and Contact

**218. Where can I see the governing body?**
About Us → Governing Structure & Quality Policy (Governing Council Members, Governing Body).

**219. Is there a Quality Policy?**
Yes.

**220. Where are the college policies?**
In the Policy Manual PDF and the Organization Charts (2020–21 to 2024–25).

**221. Who leads the college academically?**
See "Academic Leadership" and "Leadership Speaks" on the About Us menu.

**222. Is faculty hiring posted online?**
Yes. A Careers page and a notice for Assistant Professor (Unaided), dated August 19, 2026.

**223. Where can I find contact details?**
https://bkbck.edu.in/contact-us/

**224. Why should I double-check fees and dates?**
Because the fee tables, admission process PDF and seat numbers weren't readable to me, and notices change often. Always verify on the official site or with the admission office.
"""


def extract_keywords(text: str) -> str:
    """Generate meaningful pipe-separated keywords from question and answer text."""
    # Remove punctuation
    cleaned = re.sub(r"[^\w\s]", " ", text.lower())
    words = [w for w in cleaned.split() if len(w) > 3]
    # Filter common stopwords
    stopwords = {
        "what", "when", "where", "which", "does", "have", "with", "from", "that",
        "this", "they", "there", "their", "about", "some", "only", "also", "college",
        "page", "site", "more", "details", "check", "info", "bkbck", "birla", "kalyan"
    }
    meaningful = []
    seen = set()
    for w in words:
        if w not in stopwords and w not in seen:
            seen.add(w)
            meaningful.append(w)
        if len(meaningful) >= 8:
            break
    return "|".join(meaningful) if meaningful else "college|info"


def parse_and_generate():
    lines = RAW_TEXT.strip().split("\n")
    
    current_category = "General"
    faqs = []
    
    i = 0
    q_pattern = re.compile(r"^\*\*(\d+)\.\s*(.+?)\*\*$")
    cat_pattern = re.compile(r"^##\s*[A-P]\.\s*(.+)$")
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for category header
        cat_match = cat_pattern.match(line)
        if cat_match:
            current_category = cat_match.group(1).strip()
            i += 1
            continue
            
        # Check for Question
        q_match = q_pattern.match(line)
        if q_match:
            faq_num = int(q_match.group(1))
            question = q_match.group(2).strip()
            
            # Collect answer lines until next question or section header
            i += 1
            answer_lines = []
            while i < len(lines) and not q_pattern.match(lines[i].strip()) and not cat_pattern.match(lines[i].strip()):
                if lines[i].strip():
                    answer_lines.append(lines[i].strip())
                i += 1
                
            answer = " ".join(answer_lines).strip()
            
            # Detect source URL if mentioned in answer
            url_match = re.search(r"https?://[^\s\)]+|bkbck\.edu\.in[^\s\)]+|bkbck\.netlify\.app[^\s\)]*", answer)
            source_url = "https://bkbck.edu.in/"
            if url_match:
                found_url = url_match.group(0).rstrip(".,;")
                if not found_url.startswith("http"):
                    found_url = "https://" + found_url
                source_url = found_url
                
            keywords = extract_keywords(f"{question} {answer}")
            
            faqs.append({
                "id": faq_num,
                "category": current_category,
                "question": question,
                "answer": answer,
                "paraphrases": question,
                "keywords": keywords,
                "source_url": source_url,
                "last_updated": "2026-10-26"
            })
            continue
            
        i += 1
        
    print(f"Parsed {len(faqs)} FAQs successfully.")
    
    # Write to CSV
    fieldnames = [
        "id", "category", "question", "answer", "paraphrases", "keywords", "source_url", "last_updated"
    ]
    with open(FAQS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for faq in faqs:
            writer.writerow(faq)
            
    print(f"Successfully wrote {len(faqs)} verified FAQs to {FAQS_CSV}")


if __name__ == "__main__":
    parse_and_generate()
