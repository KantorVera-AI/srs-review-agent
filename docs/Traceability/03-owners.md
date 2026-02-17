# Table 3: Owner Responsibilities

## 🎨 Role Legend

🟦 **Static Owners** (Strategic/Baseline)
🟨 **Dynamic Owners** (Technical/Continuous)
🟢 **SRS Central**
🔴 **High Priority Actions**

## 👥 Responsibilities

| Owner Role                     | Documents Owned                    | Monitoring                    | Receives SRS Findings         | Triggers SRS Review          |
| ------------------------------ | ---------------------------------- | ----------------------------- | ----------------------------- | ---------------------------- |
| **🟦 Regulatory Lead**   | Intended Use, Class, IFU, Tech Doc | Strategic baselines           | Clinical/UI changes           | **🔴 ✅ Baselines**    |
| **🟨 Risk/Safety Eng**   | Risk Management File               | **🔴 Continuous + PMS** | **🔴 Safety changes**   | **🔴 ✅ Hazards**      |
| **🟨 UX/Human Factors**  | Usability File                     | Per UI release + PMS          | **🔴 UI changes**       | ✅ Use errors                |
| **🟨 Cybersecurity Eng** | Cyber/Threat Model                 | Per vuln + release            | **🔴 Security changes** | **🔴 ✅ Threats**      |
| **🟨 AI/ML Engineer**    | AI Docs, PCCP                      | Per model version             | **🔴 AI changes**       | **🔴 ✅ Perf targets** |
| **🟨 Clinical/Reg**      | Clinical Eval                      | Yearly + PMS                  | **🔴 Clinical claims**  | ✅ Endpoints                 |
| **🟢 Software Engineer** | **🔴 SRS**                   | **🔴 Continuous**       | N/A                           | N/A                          |
| QA/Test Eng                    | V&V Plans                          | Per SRS version               | All testable changes          | Testability feedback         |
| Software Architect             | Architecture                       | Per major SRS                 | Non-functional                | Feasibility constraints      |
