---

# **EosNet: Predicting Superconducting Properties of Type-I Metal-B-C Clathrates**  

EosNet is a powerful tool for predicting the properties of structures. In this project, I focus on generating **Type-I Metal-B-C Clathrates** and predicting their **superconducting transition temperature (Tc)** using EosNet.  

---

## **🔹 Workflow Overview**  

### **1️⃣ Prepare Training Data**  
- Collect a **CSV file** containing structures and their corresponding **superconducting temperatures (Tc)**.  
- Place the **CSV file** in the same folder as the related structure files.  
- Train a **multi-layer perceptron (MLP)** model using **EOSNet**.  
- Example data can be found in the **`superconductor/`** folder.  

📌 **Example CSV format:**  
| Structure | Tc (K) |
|-----------|--------|
| structure_1 | 12.5 |
| structure_2 | 8.9 |

---

### **2️⃣ Generate Type-I Metal-B-C Clathrates**  
- The dataset **`type1_clathrate.zip`** contains **~4000 clathrate structures**.  
- Use **`modify.py`** to **customize** the generated Type-I Metal-B-C clathrate structures. In modify.py you can change different metal atoms in different positions. 
- (optional) To **refine and optimize** the generated structures, use `opt.py` along with **MatterSim** for efficient structure relaxation.  


---

## **📂 Project Files**  

```
📦 EosNet_Clathrate_Project
 ┣ 📂 superconductor/       # Example dataset for training EOSNet
 ┣ 📂 type1_clathrate/      # Generated Type-I Metal-B-C clathrate structures
 ┣ 📜 modify.py             # Script to modify clathrate structures
 ┣ 📜 opt.py                # Optimization script using MatterSim
 ┗ 📜 README.md             # This documentation
```

---

