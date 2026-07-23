# 🧰 AWS Academy Learner Lab — Service List & ข้อจำกัด

> อัปเดตล่าสุดจาก Readme: 2025-06-24 | จำกัดใช้งานแค่ region **us-east-1** และ **us-west-2** เท่านั้น

---

## ⚠️ กฎเหล็กที่ต้องรู้ก่อน (งบ/บัญชีหาย)
- เกินงบ (budget) ที่กำหนด → **บัญชีถูกปิดทันที** และรีซอร์สทั้งหมดหาย
- รัน EC2 (นับรวมทุกบริการที่สร้าง EC2 เช่น EMR, Elastic Beanstalk) **พร้อมกันเกิน 9 instance** หรือ **เกิน 20 instance ไม่ว่าขนาดไหน** → บัญชีถูกปิดทันที
- vCPU รวมของ instance ที่รันพร้อมกัน ห้ามเกิน **32 vCPU**
- ปิด/ลบ resource ที่ไม่ใช้แล้วเสมอ เพื่อประหยัดงบ (โดยเฉพาะ EC2, RDS, NAT Gateway, SageMaker, EMR/ECS/EKS, Elastic Beanstalk)

---

## 💻 Compute

**Amazon EC2**
- ใช้ LabRole ได้
- Instance type รองรับ: `nano` `micro` `small` `medium` `large` เท่านั้น (On-Demand เท่านั้น)
- AMI: เฉพาะ AMI ใน region us-east-1/us-west-2 (Quick Start / My AMIs / Community) — **AWS Marketplace AMI ใช้ไม่ได้**
- จำกัดสูงสุด **9 instance รันพร้อมกัน** และ **32 vCPU รวม**
- EBS volume สูงสุด 100GB, รองรับ gp2/gp3/sc1/standard เท่านั้น (ไม่รองรับ PIOPS)
- Key pair: ใช้ `vockey` ได้เฉพาะใน us-east-1 (region อื่นต้องสร้าง key pair เอง)
- EC2 Fleet **ใช้ไม่ได้**

**EC2 Auto Scaling**
- ใช้ LabRole ได้ | รองรับ instance type: nano/micro/small/medium/large

**AWS Elastic Beanstalk**
- ใช้ LabRole ได้ (ต้องตั้ง Service role = LabRole, IAM instance profile = LabInstanceProfile เอง)
- รองรับ instance nano–large เท่านั้น ใหญ่กว่านี้จะถูก terminate อัตโนมัติ

**AWS Cloud9**
- รองรับ instance: nano/micro/small/medium/large/c4.xlarge (ไม่ใช่ทุก AZ รองรับทุกไซส์)

**Amazon Lightsail**
- เลือก spec สูงเกินไป (เช่น 8 vCPU/32GB) จะถูก terminate — ใช้ไซส์เล็กเท่านั้น

---

## 🗄️ Database

**Amazon RDS**
- Engine รองรับ: Aurora (Provisioned), Oracle, SQL Server, MySQL, PostgreSQL, MariaDB
- Instance type: nano/micro/small/medium เท่านั้น (On-Demand เท่านั้น)
- Storage: EBS gp2 สูงสุด 100GB (ไม่รองรับ PIOPS)
- **ต้องปิด Enhanced Monitoring เอง** (ไม่งั้น error)
- ⚠️ หยุด (stop) RDS แล้วปล่อยไว้เกิน 7 วัน AWS จะ auto-start ให้เอง (เสียงบเพิ่ม)

**Amazon Aurora / DynamoDB**
- ใช้ LabRole ได้ ไม่มีข้อจำกัดพิเศษเพิ่มเติมที่ระบุ

**Amazon Redshift** 🎯 (data warehouse)
- ใช้ LabRole ได้
- Instance type รองรับแค่ `ra3.large`
- คลัสเตอร์สูงสุด **2 instance**

---

## 📦 Storage

**Amazon S3 / S3 Glacier**
- ใช้ได้ปกติ | S3 Glacier: สร้าง vault lock ไม่ได้

**Amazon EBS**
- Volume สูงสุด 100GB | ไม่รองรับ PIOPS

**Amazon EFS**
- ใช้ LabRole ได้ ไม่มีข้อจำกัดพิเศษเพิ่มเติม

---

## 🔄 Data / Analytics (ETL, Big Data)

**AWS Glue**
- ใช้ LabRole ได้
- Worker type รองรับ: `G.1X`, `Standard` เท่านั้น
- Worker สูงสุด **10 คน**, Concurrency สูงสุด **1**

**AWS Glue DataBrew**
- ใช้ LabRole ได้ ไม่มีข้อจำกัดพิเศษเพิ่มเติมที่ระบุ

**Amazon Athena**
- ใช้ LabRole ได้ ไม่มีข้อจำกัดพิเศษเพิ่มเติมที่ระบุ

**Amazon EMR**
- Instance type: nano/micro/small/medium/large (ใหญ่กว่านี้ terminate อัตโนมัติ)
- ⚠️ EMR cluster **ไม่รอดข้าม session** — ถ้า session จบ, EC2 ของ EMR จะถูก stop และ EMR ไม่รองรับการ stop คลัสเตอร์ → ต้องเขียนผลลง S3 ก่อนจบ session เสมอ
- Tip: ถ้าสร้าง cluster ไม่ผ่าน ให้ลอง instance type `m4.large`

**Amazon Kinesis**
- ถ้าสร้าง Kinesis Data Analytics Studio notebook → เลือก "Create with custom settings" แล้วใช้ LabRole
- ถ้าสร้าง Delivery Stream → เลือก Advanced settings แล้วใช้ LabRole ที่มีอยู่แล้ว

---

## 🤖 AI / Machine Learning

**Amazon SageMaker**
- ใช้ LabRole ได้
- Instance type รองรับ: `ml.t3.medium` `ml.t3.large` `ml.t3.xlarge` `ml.m5.large` `ml.m5.xlarge` `ml.c5.large` `ml.c5.xlarge`
- Notebook สูงสุด **2 ตัว**, App สูงสุด **2 ตัว**
- SageMaker Studio/Canvas/JumpStart บาง feature ใช้ไม่ได้ (permission ไม่พอ)

**Amazon Rekognition**
- ใช้ LabRole ได้
- จำกัด: Face detect 1,000 ครั้ง, Label detect 1,000 ครั้ง, Inference unit สูงสุด 1

**Amazon Textract**
- ใช้ได้ ไม่มีข้อจำกัดพิเศษเพิ่มเติมที่ระบุ

**Amazon Q Developer**
- ใช้ inline code suggestion ได้ในหลาย IDE (เช่น Lambda code editor)

**Amazon ML (Machine Learning แบบเก่า)**
- ไม่มีข้อจำกัดเพิ่มเติมระบุไว้ (แต่เป็นบริการเก่า)

---

## 🐳 Containers

**Amazon ECS**
- Instance type: nano/micro/small/medium/large
- ถ้าใช้ EC2 (ไม่ใช่ Fargate) → ต้องสร้าง Auto Scaling Group ก่อนแล้วค่อยผูกกับ ECS
- Task definition ต้องตั้ง Task role และ Task execution role = LabRole เอง

**Amazon EKS**
- ใช้ role `LabEksClusterRole` (แยกจาก LabRole ปกติ) สำหรับ Cluster และ Node
- Instance type: nano/micro/small/medium/large

**Amazon ECR**
- LabRole มีสิทธิ์แค่ **read-only** ส่วน console user เขียนได้ปกติ

**AWS Fargate**
- ใช้ LabRole ได้ ไม่มีข้อจำกัดพิเศษเพิ่มเติมที่ระบุ

---

## 🔧 Developer Tools / Integration

**AWS Lambda**
- Concurrent execution สูงสุด **10 instance**

**AWS Step Functions / SNS / SQS / EventBridge / API Gateway / CodeCommit / CodeDeploy / CloudFormation / Batch / Service Catalog**
- ใช้ LabRole ได้ตามปกติ ไม่มีข้อจำกัดพิเศษเพิ่มเติมที่ระบุ

**AWS CloudTrail**
- สร้าง Trail ได้ แต่ **เปิด CloudWatch logging ให้ trail ไม่ได้**

---

## 🔐 Security / IAM

**AWS IAM**
- จำกัดสิทธิ์มาก: สร้าง user/group ไม่ได้, สร้าง role ไม่ได้ (ยกเว้น service-linked role)
- มี Role `LabRole` และ Instance Profile `LabInstanceProfile` เตรียมไว้ให้แล้ว ใช้แนบกับ EC2/Lambda/SageMaker ฯลฯ เพื่อเข้าถึงบริการอื่น

**Amazon Route 53**
- **จดโดเมนใหม่ไม่ได้**

---

## 🚫 อื่น ๆ ที่มีข้อจำกัดเฉพาะ
- **AWS Marketplace Subscriptions** — เข้าถึงได้แบบ read-only เท่านั้น
- **S3 Glacier** — สร้าง vault lock ไม่ได้
- **EC2 Fleet** — ใช้ไม่ได้เลย

---

## ✅ บริการที่ไม่มีข้อจำกัดพิเศษระบุไว้ (ใช้ได้ปกติ)
App Mesh, ACM, AWS Backup, CloudWatch, Config, Cost Explorer/Cost & Usage Report, DeepComposer, DeepLens, DeepRacer, Directory Service, ElastiCache, GuardDuty, IoT Core/1-Click/Greengrass, KMS, Mobile Hub, OpsWorks, Secrets Manager, Security Hub, STS, SAR, SWF, SSM, Trusted Advisor, VPC, WAF, Well-Architected Tool

---
