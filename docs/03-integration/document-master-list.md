# Table 1: Document Master List

**Status:** Working draft  
**Owner:** Product Management  
**Audience:** AI Architect, PM



## 🎨 Color Legend

🟦 **Static/Baseline** (Very Infrequent)
🟨 **Dynamic** (Continuous/PMS)
🟢 **SRS** (Central Hub)
🔴 **High Impact** (Mandatory)

## 📋 Document Characteristics

| Document                        | 🧑‍💼 Owner       | 📜 Standards            | ✅ Baseline?  | ⏱️ Frequency          | 🔄 Drivers   | ➡️ SRS          | SRS ➡️          |
| ------------------------------- | ------------------ | ----------------------- | ------------- | ----------------------- | ------------ | ----------------- | ----------------- |
| **🟦 Intended Use**       | Regulatory Lead    | MDR Annex I/II, FDA 801 | ✅ Strategic  | Very Infrequent         | Strategy     | ✅                | ✅                |
| **🟦 Classification**     | Regulatory Lead    | MDR Rule 11             | ✅ Strategic  | Very Infrequent         | Scope        | ✅                | ✅                |
| **🟨 Risk File**          | Risk/Safety Eng    | **ISO 14971**     | Partial       | **🔴 Continuous** | Design/PMS   | **🔴 ✅**   | **🔴 ✅**   |
| **🟨 Usability File**     | UX/Human Factors   | **IEC 62366-1**   | Partial       | Per UI + PMS            | UX Redesign  | ✅                | **🔴 ✅**   |
| **🟨 Cybersecurity File** | Cyber Eng          | **IEC 81001-5-1** | Partial       | Per Release + CVEs      | Interfaces   | **🔴 ✅**   | **🔴 ✅**   |
| **🟨 AI/ML Docs**         | AI/ML Eng          | FDA GMLP, EU AI Act     | Per Model     | Per Retraining          | Model Rules  | ✅                | **🔴 ✅**   |
| **🟨 Clinical Eval**      | Clinical/Reg       | MDR Annex XIV           | Periodic      | Yearly + PMS            | Claims       | ✅                | **🔴 ✅**   |
| **🟢 SRS**                | Software Eng       | **IEC 62304**     | Continuous    | **🔴 Per Sprint** | All Upstream | **Central** | **Central** |
| Architecture                    | Software Architect | IEC 62304               | Per Major SRS | Per Major Release       | SRS Changes  | ❌                | ✅                |
| V&V Plans                       | QA/Test Eng        | IEC 62304               | Per SRS       | **🔴 Per SRS**    | Req Changes  | ❌                | **🔴 ✅**   |
| IFU/Labeling                    | Reg Writer         | MDR Labeling            | Per Safety/UI | Per User Change         | Warnings     | ❌                | **🔴 ✅**   |
| Tech Doc                        | Quality/Reg        | MDR Annex II/III        | Container     | Per Milestone           | Upstream     | ❌                | ✅                |
