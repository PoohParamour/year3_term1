# 📝 Homework 1: Customer Segmentation (K-Means)

**Instructor:** Panita Thusaranon  
**Topic:** K-Means Clustering on Credit Card Customer Data

---

## 🎯 Assignment Instruction / โจทย์แบบฝึกหัด

### 🇹🇭 ภาษาไทย
จากข้อมูลที่กำหนดให้ (`CreditCardCustomer.csv`) จงจัดกลุ่มลูกค้าบัตรเครดิต โดยเลือกใช้ Attribute ที่นักศึกษาคิดว่าเหมาะสม และสามารถอธิบายลักษณะพฤติกรรมของลูกค้าในแต่ละ Cluster (กลุ่ม) ได้อย่างสมเหตุสมผล พร้อมแนบรูปภาพกราฟหรือสถิติที่ใช้ในการอธิบายประกอบ

### 🇬🇧 English
Using the provided dataset (`CreditCardCustomer.csv`), perform customer segmentation on credit card users. 
1. Select the attributes (features) that you deem most appropriate for clustering.
2. Formulate and explain the characteristics and behaviors of the customers in each resulting cluster.
3. Support your explanations with relevant visualizations (e.g., scatter plots, bar charts) or descriptive statistics.

---

## 📁 Files in this Folder

| File | Description |
|---|---|
| 📊 [CreditCardCustomer.csv](./CreditCardCustomer.csv) | The main dataset containing credit card customer details and transaction behavior. |
| 📄 [Credit Card Customer Description.pdf](./Credit%20Card%20Customer%20Description.pdf) | Data dictionary explaining the meaning of each column/attribute in the dataset. |

---

## 💡 Suggested Workflow / แนวทางการทำ

1. **Exploratory Data Analysis (EDA):** Understand the distribution of attributes and handle any missing values.
2. **Feature Selection & Preprocessing:** Select relevant features. *Don't forget to scale/standardize your data (e.g., using `StandardScaler`) since K-Means is sensitive to feature scales!*
3. **Finding Optimal K:** Use the Elbow Method or Silhouette Score to justify your choice for the number of clusters.
4. **Clustering:** Fit the `KMeans` model with the chosen $K$.
5. **Profiling & Interpretation:** Analyze the centroids or calculate the mean of each feature per cluster to describe who these customers are (e.g., "High Spenders," "Inactive Users," etc.).
6. **Visualization:** Plot the clusters to clearly show the segmentation.
