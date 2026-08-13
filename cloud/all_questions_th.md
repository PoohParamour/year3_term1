# คลังข้อสอบ AWS Academy Cloud Foundations (ภาษาไทย)

> **หมายเหตุการจัดทำ:**
> - แปลจากไฟล์ `all_questions.md` ต้นฉบับ (ภาษาอังกฤษ) เป็นภาษาไทย โดยคงศัพท์เฉพาะ/ชื่อบริการของ AWS ไว้เป็นภาษาอังกฤษตามเดิม (เช่น Amazon S3, IAM, EC2, VPC ฯลฯ)
> - คำตอบที่ถูกต้องจะมีข้อความ **(ถูกต้อง)** กำกับไว้ท้ายตัวเลือก
> - แต่ละ Module มีข้อสอบเดิม 10 ข้อ (ข้อ 1–10) ตามด้วยข้อสอบที่เพิ่มเติมใหม่ ซึ่งจะมีป้ายกำกับ **[ข้อใหม่]** ต่อท้ายหมายเลขข้อ — ข้อใหม่เหล่านี้เขียนขึ้นโดยอิงเนื้อหาจากสไลด์ประกอบการสอนของแต่ละ Module และมีสไตล์คำถาม (เลือกคำตอบที่ดีที่สุด / เลือกหลายข้อ / ถูก-ผิด) เหมือนข้อสอบเดิม เพื่อให้นำไปใช้เป็นข้อมูลตั้งต้น (mock data) ได้ทันที
> - รวมทั้งหมด **120 ข้อ** (ของเดิมที่แปลแล้ว 90 ข้อ + ข้อใหม่ 30 ข้อ กระจายเท่าๆ กันในทุก Module)
> - แนะนำให้ตรวจทานอีกครั้งก่อนนำไปใช้งานจริง เนื่องจากข้อสอบใหม่เป็นเนื้อหาที่สร้างขึ้นเพื่อการฝึกฝน ไม่ใช่ข้อสอบจริงจากทาง AWS Academy

---

## Module 1

1. cloud computing มีข้อได้เปรียบเหนือกว่าการทำงานแบบ on-premises อย่างไร? (เลือกคำตอบที่ดีที่สุด)
- หลีกเลี่ยงการลงทุนซื้อสินทรัพย์ก้อนใหญ่ (Avoid large capital purchases)
- ใช้ capacity แบบ on-demand
- ขยายธุรกิจสู่ระดับโลกได้ในไม่กี่นาที (Go global in minutes)
- เพิ่มความเร็วและความคล่องตัวในการทำงาน
- ถูกทุกข้อ (ถูกต้อง)

2. รูปแบบการคิดราคาแบบใดที่ทำให้ลูกค้า AWS จ่ายเงินตามการใช้ resource ที่ต้องการจริง? (เลือกคำตอบที่ดีที่สุด)
- Pay as you decommission
- Pay as you go (ถูกต้อง)
- Pay as you buy
- Pay as you reserve

3. ข้อใดต่อไปนี้ "ไม่ใช่" cloud computing model? (เลือกคำตอบที่ดีที่สุด)
- Platform as a service
- Infrastructure as a service
- System administration as a service (ถูกต้อง)
- Software as a service

4. ถูกหรือผิด? AWS เป็นเจ้าของและดูแลรักษา hardware ที่เชื่อมต่อกับเครือข่ายซึ่งจำเป็นสำหรับ application services ในขณะที่คุณเป็นผู้ provision และใช้งานตามที่ต้องการ
- ถูก (ถูกต้อง)
- ผิด

5. ข้อใดต่อไปนี้ "ไม่ใช่" ประโยชน์ของ cloud computing เมื่อเทียบกับ on-premises computing? (เลือกคำตอบที่ดีที่สุด)
- เพิ่มความเร็วและความคล่องตัว
- จ่ายเงินสำหรับการติดตั้ง (racking), จัดวาง (stacking) และจ่ายไฟให้เซิร์ฟเวอร์ (ถูกต้อง)
- ไม่ต้องคาดเดาความต้องการด้าน capacity ของโครงสร้างพื้นฐาน
- แปลง capital expense ให้เป็น variable expense
- ได้รับประโยชน์จาก economies of scale ขนาดใหญ่

6. ข้อใดต่อไปนี้ "ไม่ใช่" ประโยชน์ของ AWS Cloud computing? (เลือก 2 ข้อ)
- Multiple procurement cycles (ถูกต้อง)
- High availability
- High latency (ถูกต้อง)
- resource ชั่วคราวที่ใช้แล้วทิ้งได้ (Temporary and disposable resources)
- database ที่ทนทานต่อความผิดพลาด (Fault-tolerant databases)

7. ข้อใดต่อไปนี้เป็น compute service? (เลือกคำตอบที่ดีที่สุด)
- Amazon VPC
- Amazon S3
- Amazon EC2 (ถูกต้อง)
- Amazon CloudFront
- Amazon Redshift

8. ถูกหรือผิด? cloud computing เป็นวิธีง่ายๆ ในการเข้าถึง servers, storage, databases และชุด application services ที่หลากหลายผ่านทางอินเทอร์เน็ต โดยคุณเป็นเจ้าของ hardware ที่เชื่อมต่อกับเครือข่ายซึ่งจำเป็นสำหรับ services เหล่านี้ และ Amazon Web Services เป็นผู้ provision สิ่งที่คุณต้องการ
- ถูก
- ผิด (ถูกต้อง)

9. Economies of scale เกิดจาก ______ (เลือกคำตอบที่ดีที่สุด)
- การมี cloud provider ที่หลากหลายจำนวนมาก
- การมีลูกค้าหลายแสนรายรวมตัวกันอยู่บน cloud (ถูกต้อง)
- การมี cloud service หลายร้อยตัวให้ใช้งานผ่านอินเทอร์เน็ต
- การต้องลงทุนอย่างหนักใน data center และ server

10. ข้อใดต่อไปนี้เป็นวิธีเข้าถึง AWS core services? (เลือก 3 ข้อ)
- การโทรขอความช่วยเหลือด้าน technical support
- AWS Marketplace
- AWS Management Console (ถูกต้อง)
- AWS Command Line Interface (AWS CLI) (ถูกต้อง)
- Software Development Kits (SDKs) (ถูกต้อง)

11. [ข้อใหม่] AWS Cloud Adoption Framework (AWS CAF) แบ่งออกเป็นกี่ perspective? (เลือกคำตอบที่ดีที่สุด)
- 3 perspective
- 4 perspective
- 6 perspective (ถูกต้อง)
- 8 perspective

12. [ข้อใหม่] ข้อใดต่อไปนี้ "ไม่ใช่" perspective ใน AWS CAF? (เลือกคำตอบที่ดีที่สุด)
- Business perspective
- People perspective
- Marketing perspective (ถูกต้อง)
- Governance perspective

13. [ข้อใหม่] cloud deployment model มีทั้งหมดกี่แบบ และมีอะไรบ้าง? (เลือกคำตอบที่ดีที่สุด)
- 2 แบบ: Public และ Private
- 3 แบบ: Cloud, Hybrid, On-premises (private cloud) (ถูกต้อง)
- 4 แบบ: IaaS, PaaS, SaaS, FaaS
- 3 แบบ: IaaS, PaaS, SaaS

## Module 2

1. สำหรับบริการบางประเภท เช่น Amazon EC2 และ Amazon RDS คุณสามารถลงทุนใน reserved capacity ได้ ตัวเลือกใดบ้างที่มีให้สำหรับ Reserved Instances? (เลือก 3 ข้อ)
- AURI (ถูกต้อง)
- MURI
- NURI (ถูกต้อง)
- PURI (ถูกต้อง)
- DURI

2. ลูกค้าสามารถไปดูรายละเอียดเพิ่มเติมเกี่ยวกับกิจกรรมการเรียกเก็บเงิน (billing) ของ Amazon EC2 ที่เกิดขึ้นเมื่อ 3 เดือนก่อนได้ที่ไหน? (เลือกคำตอบที่ดีที่สุด)
- Amazon EC2 dashboard
- AWS Cost Explorer (ถูกต้อง)
- AWS Trusted Advisor dashboard
- AWS CloudTrail logs ที่เก็บไว้ใน Amazon S3

3. ถูกหรือผิด? การจะได้รับส่วนลดราคาของ Reserved Instances คุณจำเป็นต้องจ่ายเงินเต็มจำนวนล่วงหน้า (full upfront) ตลอดระยะเวลาของสัญญาเท่านั้น
- ถูก
- ผิด (ถูกต้อง)

4. ข้อความใดต่อไปนี้ถูกต้องเกี่ยวกับ pricing model ของ AWS? (เลือกคำตอบที่ดีที่สุด)
- โดยส่วนใหญ่จะมีค่าใช้จ่ายต่อ gigabyte สำหรับการโอนข้อมูลขาเข้า (inbound data transfer)
- โดยทั่วไป storage จะคิดค่าใช้จ่ายต่อ gigabyte (ถูกต้อง)
- โดยทั่วไป compute จะคิดค่าใช้จ่ายเป็นรายเดือนตาม instance type
- ค่าใช้จ่ายขาออก (outbound) ฟรีจนถึง limit ต่อบัญชี

5. AWS Support มี support plan ทั้งหมด 4 แบบ ได้แก่อะไรบ้าง? (เลือกคำตอบที่ดีที่สุด)
- Basic, Developer, Business, Enterprise (ถูกต้อง)
- Basic, Startup, Business, Enterprise
- Free, Bronze, Silver, Gold
- support ทั้งหมดฟรี

6. เครื่องมือใดของ AWS ที่ช่วยให้คุณสำรวจ AWS services และสร้างประมาณการค่าใช้จ่ายสำหรับ use case ของคุณบน AWS ได้? (เลือกคำตอบที่ดีที่สุด)
- AWS Pricing Calculator (ถูกต้อง)
- AWS Budgets
- AWS Cost and Usage Report
- AWS Billing Dashboard

7. เมื่อ AWS เติบโตขึ้น ต้นทุนในการดำเนินธุรกิจจะลดลง และการประหยัดต้นทุนนี้จะถูกส่งต่อกลับไปยังลูกค้าในรูปแบบราคาที่ถูกลง การ optimize แบบนี้เรียกว่าอะไร? (เลือกคำตอบที่ดีที่สุด)
- Expenditure awareness
- Economies of scale (ถูกต้อง)
- Matching supply and demand
- EC2 Right Sizing

8. ถูกหรือผิด? AWS ให้บริการบางอย่างโดยไม่คิดค่าใช้จ่าย เช่น Amazon Virtual Private Cloud, AWS Identity and Access Management, Consolidated Billing, AWS Elastic Beanstalk, automatic scaling, AWS OpsWorks และ AWS CloudFormation แต่คุณอาจถูกเรียกเก็บเงินสำหรับ AWS services อื่นที่ใช้งานร่วมกับบริการเหล่านี้
- ถูก (ถูกต้อง)
- ผิด

9. ประโยชน์ของการใช้ AWS Organizations คืออะไร? (เลือก 2 ข้อ)
- แทนที่ IAM policies เดิมด้วย service control policies (SCPs) ซึ่งจัดการง่ายกว่า
- สามารถสร้างกลุ่มของบัญชี (account) แล้วแนบ policy เข้ากับกลุ่มนั้นได้ (ถูกต้อง)
- สามารถสร้าง nested organizational units (OUs) ได้ไม่จำกัดจำนวนตามโครงสร้างที่ต้องการ
- ช่วยให้การสร้างและจัดการบัญชีเป็นไปโดยอัตโนมัติผ่าน API ได้ง่ายขึ้น (ถูกต้อง)
- ป้องกันไม่ให้มีการจำกัดสิทธิ์ใดๆ กับ root user ของบัญชีหลักใน organization

10. ถูกหรือผิด? AWS Free Tier มอบบริการแบบไม่จำกัด (unlimited) ให้กับลูกค้าใหม่ของ AWS เป็นเวลา 12 เดือนหลังจากวันที่สมัครใช้งาน
- ถูก
- ผิด (ถูกต้อง)

11. [ข้อใหม่] Service control policies (SCPs) ใน AWS Organizations ทำหน้าที่อะไร? (เลือกคำตอบที่ดีที่สุด)
- ให้สิทธิ์ (grant) การเข้าถึง resource แก่ user โดยตรง
- กำหนดขอบเขตสิทธิ์สูงสุด (maximum permissions) ที่บัญชีในองค์กรสามารถมีได้ (ถูกต้อง)
- แทนที่ IAM policy ทั้งหมด
- ใช้เข้ารหัสข้อมูลใน S3 bucket

12. [ข้อใหม่] ข้อใดอธิบาย AWS Organizations ได้ถูกต้อง? (เลือกคำตอบที่ดีที่สุด)
- ใช้สำหรับตรวจสอบ compliance เท่านั้น
- ช่วยรวมศูนย์การจัดการหลายบัญชี AWS ผ่าน consolidated billing และ organizational units (OUs) (ถูกต้อง)
- เป็นบริการสำหรับสร้าง VPC หลายตัว
- ใช้แทน AWS IAM ทั้งหมด

13. [ข้อใหม่] ขั้นตอนใดเป็นลำดับที่ถูกต้องในการตั้งค่า AWS Organizations? (เลือกคำตอบที่ดีที่สุด)
- สร้าง SCP > สร้าง organization > สร้าง OU > ทดสอบข้อจำกัด
- สร้าง organization > สร้าง organizational units > สร้าง service control policies > ทดสอบข้อจำกัด (ถูกต้อง)
- สร้าง OU > ทดสอบข้อจำกัด > สร้าง organization
- สร้าง billing account ก่อนเสมอ

## Module 3

1. Amazon CloudFront ใช้ component ใดของ AWS Global Infrastructure เพื่อรับประกันการส่งข้อมูลแบบ low-latency? (เลือกคำตอบที่ดีที่สุด)
- AWS Regions
- AWS edge locations (ถูกต้อง)
- AWS Availability Zones
- Amazon Virtual Private Cloud (Amazon VPC)

2. คุณสามารถรัน application และ workload จาก Region ที่อยู่ใกล้กับผู้ใช้งานปลายทางมากขึ้น เพื่อ _____ latency
- เพิ่ม (increase)
- ลด (decrease) (ถูกต้อง)

3. ถูกหรือผิด? Networking, storage, compute และ databases เป็นตัวอย่างของ service category ที่ AWS มีให้บริการ
- ถูก (ถูกต้อง)
- ผิด

4. ข้อใดต่อไปนี้เป็นพื้นที่ทางภูมิศาสตร์ที่มี Availability Zone ตั้งแต่ 2 แห่งขึ้นไป? (เลือกคำตอบที่ดีที่สุด)
- AWS Origins
- AWS Regions (ถูกต้อง)
- Compute zones
- Edge locations

5. ______ หมายถึงโครงสร้างพื้นฐานมี component redundancy อยู่ในตัว และ ______ หมายถึง resource ที่ปรับเปลี่ยนขนาดแบบไดนามิกตามความต้องการ capacity ที่เพิ่มขึ้นหรือลดลง (เลือกคำตอบที่ดีที่สุด)
- No human intervention, fault tolerant
- Elastic and scalable, no human intervention
- Fault tolerant, elastic and scalable (ถูกต้อง)
- Fault tolerant, no human intervention
- Elastic and scalable, fault tolerant

6. ถูกหรือผิด? Availability Zone ต่างๆ ภายใน Region เดียวกันเชื่อมต่อกันผ่าน low-latency links
- ถูก (ถูกต้อง)
- ผิด

7. ข้อความใดต่อไปนี้เกี่ยวกับ Availability Zones "ไม่ถูกต้อง"? (เลือกคำตอบที่ดีที่สุด)
- Availability Zones ถูกออกแบบมาเพื่อ fault isolation
- Availability Zones ประกอบด้วย data center หนึ่งแห่งหรือมากกว่า
- data center หนึ่งแห่งสามารถใช้เป็นส่วนหนึ่งของ Availability Zone ได้มากกว่าหนึ่งแห่ง (ถูกต้อง)
- Availability Zones เชื่อมต่อกันด้วย high-speed private links

8. ข้อใดต่อไปนี้เป็นจริงเกี่ยวกับ Region? (เลือก 2 ข้อ)
- ทุก Region ตั้งอยู่ในพื้นที่ทางภูมิศาสตร์เดียวกัน
- แต่ละ Region ตั้งอยู่ในพื้นที่ทางภูมิศาสตร์ที่แยกจากกัน (ถูกต้อง)
- Region คือตำแหน่งทางกายภาพของลูกค้าของคุณ
- Region คือสถานที่ทางกายภาพที่มี Availability Zone หลายแห่งอยู่ภายใน (ถูกต้อง)

9. AWS แนะนำอย่างยิ่งให้ provision compute resource ของคุณกระจายอยู่บน Availability Zone ______ (เลือกคำตอบที่ดีที่สุด)
- หลายแห่ง (multiple) (ถูกต้อง)
- ไม่มีเลย
- แห่งเดียว (single)
- ทุกแห่ง (all)

10. ถูกหรือผิด? Edge locations ตั้งอยู่เฉพาะในพื้นที่เดียวกันกับ Region เท่านั้น
- ถูก
- ผิด (ถูกต้อง)

11. [ข้อใหม่] ข้อใดคือคำนิยามที่ถูกต้องของ AWS Availability Zone? (เลือกคำตอบที่ดีที่สุด)
- กลุ่มของ Region ที่อยู่ใกล้กัน
- data center หนึ่งแห่งหรือกลุ่ม data center ที่แยกจากกันทางกายภาพภายใน Region เดียวกัน (ถูกต้อง)
- ตำแหน่งที่ตั้งของลูกค้าปลายทาง
- ศูนย์ให้บริการเฉพาะสำหรับ CloudFront เท่านั้น

12. [ข้อใหม่] เหตุใดการกระจายทรัพยากรไปยังหลาย Availability Zone จึงเป็น best practice? (เลือกคำตอบที่ดีที่สุด)
- เพื่อลดค่าใช้จ่ายด้าน storage
- เพื่อเพิ่ม fault tolerance และความพร้อมใช้งานของ application (ถูกต้อง)
- เพื่อให้ IP address ไม่ซ้ำกัน
- เพื่อให้ผ่านมาตรฐาน compliance เท่านั้น

13. [ข้อใหม่] Amazon CloudFront เป็นบริการประเภทใด? (เลือกคำตอบที่ดีที่สุด)
- Content Delivery Network (CDN) ที่ช่วยส่งข้อมูลไปยังผู้ใช้ด้วย latency ต่ำผ่าน edge location (ถูกต้อง)
- บริการ compute แบบ serverless
- บริการจัดเก็บฐานข้อมูลเชิงสัมพันธ์
- บริการสำหรับสร้าง VPC

## Module 3 (เพิ่มเติม - Well-Architected & Security)

1. ข้อความใดสะท้อนถึงหลักการออกแบบ (design principle) ของ security pillar ใน Well-Architected Framework? (เลือกคำตอบที่ดีที่สุด)
- อย่า deploy solution ขึ้น production จนกว่าจะมั่นใจว่าไม่มีความเสี่ยงด้านความปลอดภัยเลย
- กระจายอำนาจการจัดการสิทธิ์ (decentralize privilege management)
- ให้พนักงานคอยเฝ้าติดตามความเสี่ยงที่อาจเกิดขึ้นด้วยตนเองตลอดเวลา
- ใช้มาตรการด้านความปลอดภัยในทุกชั้น (layer) ของสถาปัตยกรรม (ถูกต้อง)

2. ข้อความใดต่อไปนี้ถูกต้องเกี่ยวกับความรับผิดชอบตาม AWS shared responsibility model? (เลือก 2 ข้อ)
- AWS รับผิดชอบการตั้งค่า host-based firewall
- ลูกค้ารับผิดชอบการจัดการข้อมูลผู้ใช้ (user data) ของตนเอง (ถูกต้อง)
- ลูกค้ารับผิดชอบการติดตั้ง บำรุงรักษา และปลดระวาง hardware ที่ใช้งานใน AWS data center
- AWS รับผิดชอบการตั้งค่า security group
- AWS รับผิดชอบความปลอดภัยทางกายภาพ (physical security) ของ data center (ถูกต้อง)

3. ข้อใดเป็นลักษณะของหลักการ principle of least privilege? (เลือก 2 ข้อ)
- ใช้การเข้ารหัสข้อมูล (encryption)
- ให้สิทธิ์การเข้าถึงเท่าที่จำเป็นเท่านั้น (ถูกต้อง)
- ตรวจติดตาม action และการเปลี่ยนแปลงต่างๆ
- สร้าง security policy ที่จำกัดการเข้าถึงเฉพาะงานที่กำหนด (ถูกต้อง)
- ใช้ group เสมอ

4. ข้อความใดเกี่ยวกับ AWS Identity and Access Management (IAM) ถูกต้อง? (เลือกคำตอบที่ดีที่สุด)
- IAM ให้ audit trail ว่าใครเป็นผู้ทำ action อะไร และทำเมื่อใด
- IAM เพิ่มชั้นความปลอดภัยพิเศษด้วยการตรวจจับความผิดปกติ (anomaly detection) บน resource
- ด้วย IAM คุณสามารถจัดการ encryption สำหรับข้อมูลที่ต้องเข้ารหัสแบบ at rest ได้
- ด้วย IAM คุณสามารถให้สิทธิ์การเข้าถึง resource แก่ principal ได้อย่างละเอียด (granular) (ถูกต้อง)

5. ข้อความใดอธิบายเกี่ยวกับ IAM roles ได้ถูกต้อง? (เลือก 2 ข้อ)
- ผูกกับบุคคลใดบุคคลหนึ่งโดยเฉพาะ
- ให้ security credential แบบถาวร
- บุคคล, application และ service สามารถ assume role ได้ (ถูกต้อง)
- ใช้ได้เฉพาะกับบัญชีที่เกี่ยวข้องกับผู้สร้าง role เท่านั้น
- ให้ security credential แบบชั่วคราว (temporary) (ถูกต้อง)

6. ข้อความใดสะท้อนถึง best practice สำหรับ root user ของบัญชี AWS? (เลือกคำตอบที่ดีที่สุด)
- เพื่อป้องกันไม่ให้ถูกล็อกออกจากบัญชี ไม่ควรเปิดใช้งาน MFA บน root account
- สร้าง admin user แล้วใช้ user นี้ทำงานด้าน admin ส่วนใหญ่แทนการใช้ root user (ถูกต้อง)
- สร้าง root user สองบัญชีที่มี credential แยกกัน แล้วแจกจ่ายให้คนสองคน
- ลบสิทธิ์ที่ไม่จำเป็นออกจากบัญชี root user

7. IAM ประเมิน (evaluate) policy อย่างไร? (เลือกคำตอบที่ดีที่สุด)
- explicit deny statement จะไม่ override explicit allow statement
- ตรวจสอบ explicit allow statement ก่อน explicit deny statement
- ตรวจสอบ explicit deny statement ก่อน explicit allow statement (ถูกต้อง)
- หาก policy ไม่มี explicit deny หรือ explicit allow เลย ผู้ใช้จะได้รับสิทธิ์เข้าถึงโดย default

8. ข้อความใดเกี่ยวกับ IAM policy ถูกต้อง? (เลือกคำตอบที่ดีที่สุด)
- resource-based policy อนุญาตการเข้าถึงโดย default
- identity-based policy ถูกแนบเข้ากับ user, group หรือ role (ถูกต้อง)
- identity-based policy สามารถแนบกับ entity ได้เพียงหนึ่งเดียวเท่านั้น
- resource-based policy ถูกแนบเข้ากับ user, group หรือ role

9. IAM policy element ใดที่ระบุว่าจะ allow หรือ deny request? (เลือกคำตอบที่ดีที่สุด)
- Condition
- Principal
- Effect (ถูกต้อง)
- Action

10. ข้อใดอธิบาย statement element ใน IAM policy ได้ถูกต้อง? (เลือกคำตอบที่ดีที่สุด)
- statement element เป็นส่วนที่ไม่บังคับ (optional) ของ IAM policy
- policy หนึ่งตัวมี statement element ได้เพียงหนึ่งเดียวเท่านั้น
- statement element ไม่สามารถใช้กับ identity-based policy ได้
- statement element ประกอบด้วย element อื่นๆ ที่รวมกันกำหนดว่าอะไรถูก allow หรือ deny (ถูกต้อง)

11. [ข้อใหม่] AWS Well-Architected Framework ประกอบด้วยกี่ pillar ในปัจจุบัน? (เลือกคำตอบที่ดีที่สุด)
- 4 pillar
- 5 pillar
- 6 pillar (ถูกต้อง)
- 8 pillar

12. [ข้อใหม่] โปรแกรม compliance ของ AWS สามารถแบ่งออกเป็นกลุ่มใหญ่ๆ ได้กี่ประเภท? (เลือกคำตอบที่ดีที่สุด)
- 2 ประเภท
- 3 ประเภท ได้แก่ certifications and attestations, laws/regulations/privacy และ alignments and frameworks (ถูกต้อง)
- 4 ประเภท
- ไม่มีการแบ่งประเภท

13. [ข้อใหม่] ถูกหรือผิด? Service control policy (SCP) สามารถใช้ "grant" (ให้) สิทธิ์การเข้าถึงแก่ user ได้โดยตรง
- ถูก
- ผิด (ถูกต้อง)

## Module 4

1. ใน shared responsibility model, AWS รับผิดชอบด้านใด? (เลือกคำตอบที่ดีที่สุด)
- Security "of" the cloud (ความปลอดภัยของตัว cloud เอง) (ถูกต้อง)
- Security "to" the cloud
- Security "for" the cloud
- Security "in" the cloud

2. ใน shared responsibility model ข้อใดเป็นตัวอย่างของ "security in the cloud"? (เลือก 2 ข้อ)
- การปฏิบัติตามมาตรฐานและกฎระเบียบด้าน compute security
- ความปลอดภัยทางกายภาพของสถานที่ที่ให้บริการ
- การตั้งค่า security group (ถูกต้อง)
- การเข้ารหัสข้อมูลทั้งแบบ at rest และ in transit (ถูกต้อง)
- การปกป้อง global infrastructure

3. ข้อใดเป็นความรับผิดชอบของ AWS ภายใต้ shared responsibility model? (เลือกคำตอบที่ดีที่สุด)
- การตั้งค่า third-party application
- การดูแลรักษา physical hardware (ถูกต้อง)
- การรักษาความปลอดภัยของ application access และข้อมูล
- การจัดการ custom Amazon Machine Images (AMIs)

4. เมื่อสร้าง IAM policy การเข้าถึงแบบใดบ้างที่สามารถให้สิทธิ์แก่ user ได้? (เลือก 2 ข้อ)
- Institutional access
- Authorized access
- Programmatic access (ถูกต้อง)
- AWS Management Console access (ถูกต้อง)
- Administrative root access

5. ถูกหรือผิด? AWS Organizations ช่วยให้คุณรวม (consolidate) บัญชี AWS หลายบัญชีเพื่อจัดการแบบรวมศูนย์ได้
- ถูก (ถูกต้อง)
- ผิด

6. ข้อใดเป็น best practice ในการรักษาความปลอดภัยบัญชีของคุณโดยใช้ IAM? (เลือก 2 ข้อ)
- ให้สิทธิ์ระดับ administrator แก่ user ทุกคนเป็นค่าเริ่มต้น
- ปล่อย user และ credential ที่ไม่ได้ใช้งานทิ้งไว้
- จัดการการเข้าถึง AWS resource อย่างเหมาะสม (ถูกต้อง)
- หลีกเลี่ยงการใช้ IAM group เพื่อให้สิทธิ์เดียวกันแก่ user หลายคน
- กำหนดสิทธิ์การเข้าถึงแบบละเอียด (fine-grained) (ถูกต้อง)

7. ข้อใดควรทำโดย AWS account root user? (เลือกคำตอบที่ดีที่สุด)
- รักษาความปลอดภัยการเข้าถึงสำหรับ application
- เชื่อมต่อกับ AWS service อื่นๆ
- เปลี่ยนสิทธิ์แบบละเอียด (granular permissions)
- เปลี่ยน AWS support plan (ถูกต้อง)

8. หลังจาก login ครั้งแรก AWS แนะนำ best practice ใดสำหรับ root user? (เลือกคำตอบที่ดีที่สุด)
- ลบบัญชี root user ทิ้ง
- เพิกถอนสิทธิ์ทั้งหมดของ root user
- จำกัดสิทธิ์ของ root user
- ลบ access key ของ root user ทิ้ง (ถูกต้อง)

9. ผู้ดูแลระบบจะเพิ่มความปลอดภัยอีกชั้นให้กับการ login เข้า AWS Management Console ของ user ได้อย่างไร? (เลือกคำตอบที่ดีที่สุด)
- ใช้ Amazon Cloud Directory
- ตรวจสอบ (audit) IAM roles
- เปิดใช้งาน multi-factor authentication (MFA) (ถูกต้อง)
- เปิดใช้งาน AWS CloudTrail

10. ถูกหรือผิด? AWS Key Management Service (AWS KMS) ช่วยให้คุณประเมิน ตรวจสอบ (audit) และวิเคราะห์การตั้งค่า configuration ของ AWS resource ได้
- ถูก
- ผิด (ถูกต้อง)

11. [ข้อใหม่] AWS Shield Standard ให้การป้องกันประเภทใดโดยไม่มีค่าใช้จ่ายเพิ่มเติม? (เลือกคำตอบที่ดีที่สุด)
- การป้องกันมัลแวร์
- การป้องกัน Distributed Denial of Service (DDoS) (ถูกต้อง)
- การเข้ารหัสข้อมูล
- การสแกนช่องโหว่ (vulnerability scanning)

12. [ข้อใหม่] AWS Key Management Service (AWS KMS) ใช้สำหรับอะไร? (เลือกคำตอบที่ดีที่สุด)
- สร้างและจัดการ encryption key เพื่อควบคุมการเข้ารหัสข้อมูลใน AWS service และ application (ถูกต้อง)
- ตรวจจับ DDoS attack
- จัดการบัญชี AWS หลายบัญชี
- สร้าง VPC

13. [ข้อใหม่] ถูกหรือผิด? Service control policy (SCP) มีไวยากรณ์ (syntax) คล้ายกับ IAM permission policy แต่ SCP ไม่สามารถให้สิทธิ์ (grant) ได้โดยตรง
- ถูก (ถูกต้อง)
- ผิด

14. [ข้อใหม่] โปรแกรม compliance ประเภท "Laws, regulations, and privacy" ของ AWS มีตัวอย่างเช่นอะไรบ้าง? (เลือกคำตอบที่ดีที่สุด)
- ISO 27001
- GDPR และ HIPAA (ถูกต้อง)
- CIS benchmark
- SOC 2 เท่านั้น

## Module 5

1. ด้วย Amazon Virtual Private Cloud (Amazon VPC) subnet ที่มีขนาดเล็กที่สุดที่คุณสามารถมีได้ใน VPC คือขนาดใด? (เลือกคำตอบที่ดีที่สุด)
- /26
- /28 (ถูกต้อง)
- /30
- /24

2. ด้วย Amazon Virtual Private Cloud (Amazon VPC) ช่วง IP address ที่ใหญ่ที่สุดที่คุณสามารถมีได้ใน VPC คือขนาดใด? (เลือกคำตอบที่ดีที่สุด)
- /16 (ถูกต้อง)
- /24
- /30
- /28

3. คุณต้องการให้ resource ใน private subnet เข้าถึงอินเทอร์เน็ตได้ ต้องมีสิ่งใดต่อไปนี้เพื่อเปิดใช้งานการเข้าถึงนี้? (เลือกคำตอบที่ดีที่สุด)
- NAT gateway (ถูกต้อง)
- Network access control lists
- Security groups
- Route tables

4. AWS networking service ใดที่ช่วยให้บริษัทสามารถสร้าง virtual network ภายใน AWS ได้? (เลือกคำตอบที่ดีที่สุด)
- Amazon Virtual Private Cloud (Amazon VPC) (ถูกต้อง)
- AWS Direct Connect
- Amazon Route 53
- AWS Config

5. ถูกหรือผิด? private subnet มีการเข้าถึงอินเทอร์เน็ตโดยตรง
- ถูก
- ผิด (ถูกต้อง)

6. Amazon CloudFront ใช้ component ใดของ AWS Global Infrastructure เพื่อรับประกันการส่งข้อมูลแบบ low-latency? (เลือกคำตอบที่ดีที่สุด)
- Amazon Virtual Private Cloud (Amazon VPC)
- AWS edge locations (ถูกต้อง)
- AWS Regions
- AWS Availability Zones

7. ข้อใดเป็น security control แบบเสริม (optional) ที่สามารถใช้ในระดับ subnet ของ VPC ได้? (เลือกคำตอบที่ดีที่สุด)
- Firewall
- Security group
- Network ACL (ถูกต้อง)
- Web application firewall

8. เกิดอะไรขึ้นเมื่อคุณใช้ Amazon Virtual Private Cloud (Amazon VPC) สร้าง VPC ใหม่? (เลือกคำตอบที่ดีที่สุด)
- มีการสร้าง subnet 3 ตัวโดย default ใน Availability Zone เดียว
- มีการสร้าง subnet 3 ตัวโดย default หนึ่งตัวต่อหนึ่ง Availability Zone
- มีการสร้าง internet gateway โดย default
- มีการสร้าง main route table โดย default (ถูกต้อง)

9. ข้อใดสามารถใช้เพื่อปกป้อง Amazon Elastic Compute Cloud (Amazon EC2) instance ที่โฮสต์อยู่บน AWS ได้? (เลือกคำตอบที่ดีที่สุด)
- ถูกทุกข้อ
- Security group (ถูกต้อง)
- AMI
- Internet Gateway

10. คุณเป็น solutions architect ที่ทำงานให้บริษัทค้าปลีกขนาดใหญ่ซึ่งกำลังย้ายโครงสร้างพื้นฐานเดิมมาสู่ AWS คุณแนะนำให้ใช้ custom VPC เมื่อคุณสร้าง VPC คุณกำหนด IPv4 Classless Inter-Domain Routing (CIDR) block เป็น 10.0.1.0/24 (ซึ่งมี IP address ทั้งหมด 256 ตัว) มี IP address ที่ใช้งานได้จริงกี่ตัว? (เลือกคำตอบที่ดีที่สุด)
- 256
- 246
- 250
- 251 (ถูกต้อง)

11. [ข้อใหม่] VPC peering มีข้อจำกัดใดบ้าง? (เลือกคำตอบที่ดีที่สุด)
- รองรับ transitive peering ได้
- ช่วง IP ของทั้งสอง VPC ต้องไม่ทับซ้อนกัน (ถูกต้อง)
- เชื่อมต่อได้เฉพาะภายใน Region เดียวกันเท่านั้น
- เชื่อมต่อ VPC ได้ไม่จำกัดจำนวนคู่ระหว่าง VPC เดียวกัน

12. [ข้อใหม่] route table ทุกตัวใน VPC จะมี route ใดอยู่โดย default เสมอ? (เลือกคำตอบที่ดีที่สุด)
- route ไปยัง internet gateway
- local route สำหรับสื่อสารภายใน VPC (ถูกต้อง)
- route ไปยัง NAT gateway
- route ไปยัง VPN gateway

13. [ข้อใหม่] NAT gateway ควรถูกวางไว้ใน subnet ประเภทใด? (เลือกคำตอบที่ดีที่สุด)
- private subnet
- public subnet (ถูกต้อง)
- VPN subnet
- edge subnet

14. [ข้อใหม่] ถูกหรือผิด? แต่ละ subnet สามารถเชื่อมโยง (associate) กับ route table ได้มากกว่าหนึ่งตัวพร้อมกัน
- ถูก
- ผิด (ถูกต้อง)

## Module 6

1. Amazon Elastic Compute Cloud (Amazon EC2) คือ ______ (เลือกคำตอบที่ดีที่สุด)
- serverless compute service
- platform as a service (PaaS)
- managed database service
- infrastructure as a service (IaaS) (ถูกต้อง)

2. ถูกหรือผิด? serverless compute service หมายความว่าไม่มี server ใดๆ รัน code ของคุณเลย
- ถูก
- ผิด (ถูกต้อง)

3. เมื่อบริษัทสร้าง (spin up) Amazon EC2 instance บริษัทมีความรับผิดชอบด้านใด? (เลือกคำตอบที่ดีที่สุด)
- การ patch host operating system ที่อยู่เบื้องหลัง
- การจัดหาความปลอดภัยทางกายภาพให้ hardware ใน data center
- การดูแลไฟฟ้าให้กับ instance
- การ patch guest operating system (ถูกต้อง)

4. ถูกหรือผิด? ปริมาณ memory ของ Amazon EC2 instance ถูกกำหนดโดย instance type
- ถูก (ถูกต้อง)
- ผิด

5. ข้อความใดเกี่ยวกับการใช้งาน Amazon Machine Images (AMIs) ถูกต้อง? (เลือกคำตอบที่ดีที่สุด)
- คุณต้องสร้าง AMI ก่อนจึงจะ launch Amazon EC2 instance ได้
- คุณสามารถ launch instance ได้เพียงหนึ่งตัวจาก AMI หนึ่งตัวเท่านั้น
- มีเพียงเจ้าของ AMI เท่านั้นที่สามารถ launch EC2 instance จาก AMI นั้นได้
- คุณสามารถ launch instance หลายตัวจาก AMI เดียวได้ (ถูกต้อง)

6. Amazon EC2 pricing option ใดเหมาะสมที่สุดสำหรับ application ที่รันตลอด 24 ชั่วโมง 7 วันต่อสัปดาห์ เป็นเวลา 3 ปี? (เลือกคำตอบที่ดีที่สุด)
- On-Demand Instances
- Reserved Instances (ถูกต้อง)
- Spot Instances
- Dedicated Hosts

7. Amazon EC2 pricing option ใดเหมาะสมที่สุดสำหรับ application ที่มี workload ไม่แน่นอนและเปลี่ยนแปลงตลอดเวลา? (เลือกคำตอบที่ดีที่สุด)
- On-Demand Instances (ถูกต้อง)
- Reserved Instances
- Spot Instances
- Dedicated Hosts

8. AWS service ใดที่สามารถ scale จำนวน Amazon EC2 instance โดยอัตโนมัติตามชุดกฎที่กำหนดได้? (เลือกคำตอบที่ดีที่สุด)
- Amazon Elastic Load Balancing
- AWS Auto Scaling (ถูกต้อง)
- AWS CloudFormation
- Amazon CloudWatch

9. load balancer ประเภทใดเหมาะสมที่สุดสำหรับกระจาย traffic แบบ HTTP และ HTTPS? (เลือกคำตอบที่ดีที่สุด)
- Classic Load Balancer
- Network Load Balancer
- Application Load Balancer (ถูกต้อง)
- UDP Load Balancer

10. ประโยชน์หลักของการใช้ Amazon Elastic Load Balancing คืออะไร? (เลือกคำตอบที่ดีที่สุด)
- ให้การเชื่อมต่อแบบเฉพาะ (dedicated) ไปยัง AWS
- กระจาย traffic ขาเข้าไปยัง target หลายตัว (ถูกต้อง)
- สร้าง Amazon EC2 instance โดยอัตโนมัติตามความต้องการ
- สำรองข้อมูล (backup) database โดยอัตโนมัติ

11. [ข้อใหม่] EC2 instance type category ใดเหมาะกับงานที่ต้องใช้ high-performance computing (HPC) และ batch processing? (เลือกคำตอบที่ดีที่สุด)
- General purpose
- Compute optimized (ถูกต้อง)
- Storage optimized
- Memory optimized

12. [ข้อใหม่] EC2 instance type category ใดเหมาะกับ workload ประเภท in-memory database และ big data analytics? (เลือกคำตอบที่ดีที่สุด)
- Compute optimized
- Memory optimized (ถูกต้อง)
- Accelerated computing
- General purpose

13. [ข้อใหม่] ข้อใดคือคำแนะนำเมื่อต้องเลือก instance type ตระกูล (family) ใหม่? (เลือกคำตอบที่ดีที่สุด)
- ควรเลือก instance generation ล่าสุดในตระกูลนั้น เพราะมักมี price-to-performance ratio ที่ดีกว่า (ถูกต้อง)
- ควรเลือก instance generation เก่าที่สุดเพื่อความเสถียร
- generation ไม่มีผลต่อราคาหรือประสิทธิภาพ
- ควรเลือกตาม storage เพียงอย่างเดียว

14. [ข้อใหม่] ถูกหรือผิด? EBS-optimized instance ให้การเชื่อมต่อเครือข่ายแบบเฉพาะ (dedicated) ไปยัง EBS volume ที่แนบอยู่ เพื่อเพิ่มประสิทธิภาพ I/O
- ถูก (ถูกต้อง)
- ผิด

## Module 7

1. ถูกหรือผิด? Amazon Simple Storage Service (Amazon S3) เป็น object storage ที่เหมาะสำหรับจัดเก็บ flat file เช่น เอกสาร Microsoft Word, รูปภาพ ฯลฯ
- ถูก (ถูกต้อง)
- ผิด

2. Amazon S3 ทำการ replicate object ทั้งหมด ______ (เลือกคำตอบที่ดีที่สุด)
- บน volume หลายตัวภายใน Availability Zone เดียว
- ไปยัง Availability Zone หลายแห่งภายใน Region เดียวกัน (ถูกต้อง)
- ข้าม Region หลาย Region เพื่อความทนทาน (durability) ที่สูงขึ้น
- บน S3 bucket หลายตัว

3. ข้อใดสามารถใช้เป็น storage class ใน S3 object lifecycle policy ได้? (เลือก 3 ข้อ)
- S3 Standard (ถูกต้อง)
- AWS Storage Gateway
- S3 Standard-Infrequent Access (ถูกต้อง)
- Amazon S3 Glacier (ถูกต้อง)
- S3 Reduced Redundancy Storage
- Amazon DynamoDB

4. ชื่อของ S3 bucket ต้องไม่ซ้ำกัน ______ (เลือกคำตอบที่ดีที่สุด)
- ทั่วโลกในทุกบัญชี AWS (ถูกต้อง)
- ภายใน Region เดียวกัน
- ในทุกบัญชี AWS ของคุณ
- ภายในบัญชี AWS ของคุณเอง

5. คุณสามารถใช้ Amazon Elastic File System (Amazon EFS) เพื่อ: (เลือกคำตอบที่ดีที่สุด)
- จัดเตรียม file storage ที่เรียบง่าย, scalable, elastic สำหรับใช้ภายใน AWS เท่านั้น
- ทำ storage ให้กับ Amazon EC2 instance ที่ virtual machine หลายตัวสามารถเข้าถึงพร้อมกันได้ (ถูกต้อง)
- โฮสต์ CDN ที่แข็งแกร่งเพื่อส่งเว็บไซต์ทั้งหมดพร้อม dynamic, static และ streaming content
- สร้าง content เฉพาะสำหรับผู้ใช้แต่ละคน

6. Amazon Elastic Block Store (Amazon EBS) เหมาะสำหรับข้อมูลที่ ______ และ ______ (เลือก 2 ข้อ)
- ต้องการ storage แบบ object-level
- ต้องเข้าถึงได้อย่างรวดเร็ว และต้องการความคงอยู่ (persistence) ในระยะยาว (ถูกต้อง)
- ต้องการวิธีการเข้ารหัส (encryption) (ถูกต้อง)
- ต้องถูกเก็บไว้ใน Availability Zone ที่ต่างจาก EC2 instance ที่ใช้งาน

7. ถูกหรือผิด? โดย default ข้อมูลทั้งหมดที่จัดเก็บใน Amazon S3 สามารถถูกดูได้โดยสาธารณะ (public)
- ถูก
- ผิด (ถูกต้อง)

8. ในบริบทของ Amazon S3 Glacier, "Vault" คืออะไร? (เลือกคำตอบที่ดีที่สุด)
- กฎที่กำหนดว่าใครสามารถ (หรือไม่สามารถ) เข้าถึง archive ได้
- object (รูปภาพ, วิดีโอ, ไฟล์ หรือเอกสาร)
- container สำหรับจัดเก็บ archive (ถูกต้อง)
- policy ที่ระบุว่าใครสามารถเข้าถึง content ที่เก็บใน Glacier ได้

9. ถูกหรือผิด? เมื่อคุณสร้าง bucket ใน Amazon S3 bucket นั้นจะถูกผูกไว้กับ AWS Region ที่เฉพาะเจาะจง
- ถูก (ถูกต้อง)
- ผิด

10. ข้อใดต่อไปนี้เป็น feature ของ Amazon Elastic Block Store (Amazon EBS)? (เลือก 2 ข้อ)
- ข้อมูลที่เก็บบน Amazon EBS จะถูก replicate โดยอัตโนมัติภายใน Availability Zone เดียวกัน (ถูกต้อง)
- ข้อมูล Amazon EBS จะถูก backup ไปยัง tape โดยอัตโนมัติ
- ข้อมูลบน EBS volume จะหายไปเมื่อ instance ที่แนบอยู่ถูกหยุด (stop)
- EBS volume สามารถถูกเข้ารหัสได้อย่างโปร่งใส (transparently) ต่อ workload บน instance ที่แนบอยู่ (ถูกต้อง)

11. [ข้อใหม่] S3 storage class ใดเหมาะสำหรับข้อมูลที่เข้าถึงไม่บ่อยแต่ต้องการดึงข้อมูล (retrieve) ได้ทันที? (เลือกคำตอบที่ดีที่สุด)
- S3 Standard
- S3 Standard-IA (ถูกต้อง)
- S3 Glacier Deep Archive
- S3 Glacier Flexible Retrieval

12. [ข้อใหม่] ข้อใดคือระยะเวลาการดึงข้อมูล (retrieval) แบบ Expedited ของ Amazon S3 Glacier? (เลือกคำตอบที่ดีที่สุด)
- 1–5 นาที (ถูกต้อง)
- 3–5 ชั่วโมง
- 5–12 ชั่วโมง
- 24–48 ชั่วโมง

13. [ข้อใหม่] ถูกหรือผิด? S3 lifecycle policy สามารถกำหนดให้ย้าย object จาก S3 Standard ไปยัง S3 Standard-IA แล้วจึงย้ายไปยัง Amazon S3 Glacier โดยอัตโนมัติตามอายุของ object
- ถูก (ถูกต้อง)
- ผิด

## Module 8

1. คุณกำลังออกแบบ ecommerce web application ที่ต้อง scale รองรับผู้ใช้งานพร้อมกันหลายแสนคน database technology ใดเหมาะสมที่สุดสำหรับเก็บ session state ในกรณีนี้? (เลือกคำตอบที่ดีที่สุด)
- Amazon Relational Database Service (Amazon RDS)
- Amazon DynamoDB (ถูกต้อง)
- Amazon Redshift
- Amazon Simple Storage Service (Amazon S3)

2. คุณต้องการค้นหา item ใน Amazon DynamoDB table โดยใช้ attribute อื่นที่ไม่ใช่ primary key ของ item ควรใช้ operation ใด? (เลือกคำตอบที่ดีที่สุด)
- PutItem
- Scan (ถูกต้อง)
- Query
- GetItem

3. ใน Amazon DynamoDB, operation "query" ช่วยให้คุณทำอะไรได้บ้าง? (เลือกคำตอบที่ดีที่สุด)
- query table โดยใช้ partition key และตัวกรอง sort key แบบเสริม
- query secondary index ใดๆ ที่มีอยู่ใน table
- ดึง item จาก table หรือ secondary index ได้อย่างมีประสิทธิภาพ
- ถูกทุกข้อ (ถูกต้อง)

4. AWS Cloud service ใดเหมาะสมที่สุดสำหรับการวิเคราะห์ข้อมูลด้วย standard structured query language (SQL) และเครื่องมือ business intelligence (BI) ที่มีอยู่แล้ว? (เลือกคำตอบที่ดีที่สุด)
- Amazon Relational Database Service (Amazon RDS)
- Amazon Simple Storage Service Glacier
- Amazon DynamoDB
- Amazon Redshift (ถูกต้อง)

5. ใน Amazon DynamoDB, attribute คือ ______ (เลือกคำตอบที่ดีที่สุด)
- fundamental data element (หน่วยข้อมูลพื้นฐาน) (ถูกต้อง)
- กลุ่มของ item
- กลุ่มของ attribute

6. หากคุณกำลังพัฒนา application ที่ต้องการ database ที่มี performance รวดเร็วมาก, scale ได้เร็ว และมีความยืดหยุ่นของ schema ควรพิจารณาใช้บริการใด? (เลือกคำตอบที่ดีที่สุด)
- Amazon Relational Database Service (Amazon RDS)
- Amazon ElastiCache
- Amazon DynamoDB (ถูกต้อง)
- Amazon Redshift

7. use case ใดเหมาะสมกับการใช้งาน Amazon Relational Database Service (Amazon RDS)? (เลือกคำตอบที่ดีที่สุด)
- อัตราการอ่าน/เขียนจำนวนมหาศาล
- คำขอ GET หรือ PUT แบบง่ายๆ
- transaction ที่ซับซ้อน (ถูกต้อง)
- ถูกทุกข้อ

8. บริษัทหนึ่งมี application ที่ประกอบด้วย .NET layer ซึ่งเชื่อมต่อกับ MySQL database ต้องการย้าย application นี้มายัง AWS และใช้ feature อย่าง high availability และ automated backup database ใดต่อไปนี้เหมาะสมที่สุดสำหรับกรณีนี้? (เลือกคำตอบที่ดีที่สุด)
- Amazon DynamoDB
- Amazon Redshift
- Amazon RDS
- Amazon Aurora (ถูกต้อง)

9. ถูกหรือผิด? Amazon RDS ทำการ patch database software โดยอัตโนมัติ และสำรองข้อมูล database ของคุณ โดยเก็บ backup ไว้ตามระยะเวลาที่ user กำหนด และรองรับการทำ point-in-time recovery
- ถูก (ถูกต้อง)
- ผิด

10. คุณควรพิจารณาอะไรบ้างเมื่อเลือกประเภทของ database? (เลือกคำตอบที่ดีที่สุด)
- ขนาดข้อมูล (Data size)
- ช่วงเวลาการเข้าถึงข้อมูล (Data access period)
- ความถี่ในการ query (Query frequency)
- ความพร้อมใช้งานสูง (Highly available)
- ถูกทุกข้อ (ถูกต้อง)

11. [ข้อใหม่] Primary key แบบ composite ของ DynamoDB ประกอบด้วยอะไรบ้าง? (เลือกคำตอบที่ดีที่สุด)
- partition key เพียงอย่างเดียว
- partition key และ sort key (ถูกต้อง)
- sort key เพียงอย่างเดียว
- attribute ทั้งหมดในตาราง

12. [ข้อใหม่] Global Secondary Index (GSI) ใน DynamoDB แตกต่างจาก Local Secondary Index (LSI) อย่างไร? (เลือกคำตอบที่ดีที่สุด)
- GSI สามารถใช้ partition key และ/หรือ sort key ที่ต่างจาก base table ได้ ในขณะที่ LSI ใช้ partition key เดิมแต่เปลี่ยน sort key (ถูกต้อง)
- GSI และ LSI ทำงานเหมือนกันทุกประการ
- LSI ใช้ได้กับทุก table โดยไม่ต้องสร้างตั้งแต่แรก
- GSI ใช้ได้เฉพาะกับ Amazon RDS เท่านั้น

13. [ข้อใหม่] ถูกหรือผิด? Amazon DynamoDB เป็น fully managed, serverless, NoSQL database ที่รองรับทั้ง key-value และ document data model
- ถูก (ถูกต้อง)
- ผิด
