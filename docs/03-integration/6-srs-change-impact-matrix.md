# Table 2: SRS Change Impact Matrix

**Status:** Working draft  
**Owner:** Product Management  
**Audience:** AI Architect, PM

## 🎨 Impact Legend

🔴 **H** = High (Mandatory owner review)
🟡 **M** = Medium (Check references)
🟢 **L** = Low (Monitor)
🟣 **Reclassification** = IMDRF category or software item safety class change detected — routes to RA/PRRC and Software Architect

## 📊 Matrix

| SRS Change Type           | Intended Use   | Risk File      | UX File        | Cyber File     | AI Docs        | Clinical       | V&V Plans      | IFU            |
| ------------------------- | -------------- | -------------- | -------------- | -------------- | -------------- | -------------- | -------------- | -------------- |
| **Clinical Claims** | **🔴 H** | 🟡 M           | 🟢 L           | 🟢 L           | **🔴 H** | **🔴 H** | 🟡 M           | **🔴 H** |
| **Risk/Safety**     | 🟢 L           | **🔴 H** | 🟡 M           | 🟡 M           | 🟡 M           | 🟡 M           | **🔴 H** | **🔴 H** |
| **UI/Workflow**     | 🟢 L           | 🟡 M           | **🔴 H** | 🟢 L           | 🟢 L           | 🟢 L           | **🔴 H** | **🔴 H** |
| **Security Flows**  | 🟢 L           | 🟡 M           | 🟢 L           | **🔴 H** | 🟡 M           | 🟢 L           | **🔴 H** | 🟡 M           |
| **AI/ML Behavior**  | **🔴 H** | **🔴 H** | 🟡 M           | 🟡 M           | **🔴 H** | **🔴 H** | **🔴 H** | 🟡 M           |
| 🟣 **Reclassification trigger** | 🔴 H | 🔴 H | 🟢 L | 🟢 L | 🟡 M | 🟡 M | 🟡 M | 🟢 L |
| **Non-Functional**  | 🟢 L           | 🟡 M           | 🟢 L           | 🟢 L           | 🟡 M           | 🟢 L           | **🔴 H** | 🟢 L           |

**Reverse Flow**: All Baseline docs → SRS suggestions (**🔴 High**)
