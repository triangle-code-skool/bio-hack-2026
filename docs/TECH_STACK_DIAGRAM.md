# UltraViab — Technical Architecture

> Real-time organ viability assessment powered by ultrasound analytics and machine learning

---

## System Architecture

```mermaid
flowchart TB
    %% ───────────────────────────────────────────────
    %% CLIENT LAYER
    %% ───────────────────────────────────────────────
    subgraph CLIENTS["CLIENT LAYER — Cross-Platform Reach"]
        direction LR

        subgraph MOBILE["MOBILE APP"]
            direction TB
            RN["React Native 0.81\n+ Expo SDK 54"]
            TS_M["TypeScript 5.9\nStrict Type Safety"]
            ROUTER["Expo Router 6\nFile-Based Navigation"]
            REANIMATE["Reanimated 4\nNative Animations"]
            RN --> TS_M
            TS_M --> ROUTER
            ROUTER --> REANIMATE
        end

        subgraph WEB["WEB DASHBOARD"]
            direction TB
            ST["Streamlit 1.42\nRapid Analytics UI"]
            PLOTLY["Plotly 5.24\nInteractive Charts"]
            SHADCN["shadcn/ui\nPremium Components"]
            PANDAS["Pandas + NumPy\nData Processing"]
            ST --> PLOTLY
            PLOTLY --> SHADCN
            SHADCN --> PANDAS
        end
    end

    %% ───────────────────────────────────────────────
    %% API LAYER
    %% ───────────────────────────────────────────────
    subgraph API_LAYER["SERVICE LAYER — Clean Architecture"]
        direction TB

        subgraph GATEWAY["API GATEWAY"]
            FASTAPI["FastAPI + Uvicorn\nAsync ASGI Server"]
            PYDANTIC["Pydantic Schemas\nRuntime Validation"]
            CORS["CORS Middleware\nSecure Cross-Origin"]
            SWAGGER["OpenAPI / Swagger\nAuto-Generated Docs"]
        end

        subgraph SERVICES["BUSINESS LOGIC"]
            direction TB
            CTRL["Controllers\nHTTP Endpoint Routing"]
            SVC["Services\nDomain Logic Layer"]
            DI["Dependency Injection\nTestable & Modular"]
            CTRL --> SVC
            SVC --> DI
        end
    end

    %% ───────────────────────────────────────────────
    %% INTELLIGENCE LAYER
    %% ───────────────────────────────────────────────
    subgraph ML_LAYER["INTELLIGENCE LAYER — Predictive Engine"]
        direction LR

        subgraph SCORING["VIABILITY SCORING"]
            PREDICT["Prediction Service\nWeighted Feature Analysis"]
            RISK["Risk Factor Detection\nThreshold-Based Alerts"]
            CLASS["Classification Engine\nAccept | Marginal | Decline"]
        end

        subgraph ML_FUTURE["ML PIPELINE — Future"]
            SKLEARN["scikit-learn\nGradient Boosting"]
            TRAIN["Model Training\nSynthetic + Clinical Data"]
            INTERPRET["Feature Importance\nClinical Interpretability"]
        end
    end

    %% ───────────────────────────────────────────────
    %% DATA LAYER
    %% ───────────────────────────────────────────────
    subgraph DATA_LAYER["DATA LAYER — Managed Infrastructure"]
        direction LR

        subgraph SUPABASE["SUPABASE PLATFORM"]
            PG["PostgreSQL 17\nRelational Database"]
            AUTH["Supabase Auth\nJWT + Refresh Tokens"]
            REALTIME["Realtime Engine\nLive Subscriptions"]
            S3["S3 Storage\nFile & Image Uploads"]
        end
    end

    %% ───────────────────────────────────────────────
    %% CONNECTIONS
    %% ───────────────────────────────────────────────
    MOBILE -->|"REST / JSON"| FASTAPI
    WEB -->|"HTTP Client"| FASTAPI
    FASTAPI --> PYDANTIC
    PYDANTIC --> CTRL
    FASTAPI --> CORS
    FASTAPI --> SWAGGER
    SVC --> PREDICT
    PREDICT --> RISK
    PREDICT --> CLASS
    PREDICT -.->|"Future Integration"| SKLEARN
    SKLEARN --> TRAIN
    TRAIN --> INTERPRET
    DI --> PG
    DI --> AUTH
    PG --> REALTIME
    PG --> S3

    %% ───────────────────────────────────────────────
    %% STYLES
    %% ───────────────────────────────────────────────
    classDef clientBox fill:#1e3a5f,stroke:#3b82f6,stroke-width:2px,color:#e2e8f0
    classDef mobileNode fill:#1e40af,stroke:#60a5fa,stroke-width:1px,color:#dbeafe
    classDef webNode fill:#064e3b,stroke:#34d399,stroke-width:1px,color:#d1fae5
    classDef apiNode fill:#7c2d12,stroke:#fb923c,stroke-width:1px,color:#fed7aa
    classDef serviceNode fill:#78350f,stroke:#fbbf24,stroke-width:1px,color:#fef3c7
    classDef mlNode fill:#581c87,stroke:#a78bfa,stroke-width:1px,color:#ede9fe
    classDef futureNode fill:#3b0764,stroke:#7c3aed,stroke-width:1px,color:#c4b5fd,stroke-dasharray: 5 5
    classDef dataNode fill:#0f172a,stroke:#22d3ee,stroke-width:1px,color:#cffafe
    classDef layerLabel fill:none,stroke:none,color:#94a3b8

    class RN,TS_M,ROUTER,REANIMATE mobileNode
    class ST,PLOTLY,SHADCN,PANDAS webNode
    class FASTAPI,PYDANTIC,CORS,SWAGGER apiNode
    class CTRL,SVC,DI serviceNode
    class PREDICT,RISK,CLASS mlNode
    class SKLEARN,TRAIN,INTERPRET futureNode
    class PG,AUTH,REALTIME,S3 dataNode
```

---

## Platform Advantages

```mermaid
flowchart LR
    subgraph MOBILE_ADV["MOBILE ADVANTAGES"]
        direction TB
        M1["Single Codebase\niOS + Android + Web"]
        M2["OTA Updates\nNo App Store Delay"]
        M3["Native Performance\nReanimated + Hermes"]
        M4["Offline Capable\nLocal Fallback Scoring"]
        M5["Bedside Ready\nTouch-Optimized Clinical UI"]
    end

    subgraph WEB_ADV["WEB ADVANTAGES"]
        direction TB
        W1["Zero Install\nBrowser-Based Access"]
        W2["Real-Time Analytics\nLive Data Visualization"]
        W3["Rich Charting\nRadar + Signal + Bar"]
        W4["Dark Mode Clinical UI\nLow-Light Optimized"]
        W5["Multi-User Dashboard\nSimultaneous Access"]
    end

    subgraph SHARED_ADV["SHARED STRENGTHS"]
        direction TB
        S1["Type-Safe End-to-End\nTS + Pydantic Validation"]
        S2["Clean Architecture\nController-Service-Schema"]
        S3["Supabase BaaS\nAuth + DB + Realtime + Storage"]
        S4["Auto-Generated API Docs\nOpenAPI / Swagger"]
        S5["Concurrent Dev Server\nnpm run dev — All Services"]
    end

    MOBILE_ADV ~~~ SHARED_ADV
    SHARED_ADV ~~~ WEB_ADV

    classDef mobileAdv fill:#1e40af,stroke:#60a5fa,stroke-width:1px,color:#dbeafe
    classDef webAdv fill:#064e3b,stroke:#34d399,stroke-width:1px,color:#d1fae5
    classDef sharedAdv fill:#4c1d95,stroke:#a78bfa,stroke-width:1px,color:#ede9fe

    class M1,M2,M3,M4,M5 mobileAdv
    class W1,W2,W3,W4,W5 webAdv
    class S1,S2,S3,S4,S5 sharedAdv
```

---

## Future-Proofing Roadmap

```mermaid
flowchart TB
    subgraph NOW["CURRENT — Hackathon MVP"]
        direction LR
        N1["Weighted Scoring\nAlgorithm"]
        N2["Manual Metric Entry\nForm-Based Input"]
        N3["Local Dev\nExpo + Uvicorn"]
        N4["Synthetic Data\nSimulated Datasets"]
    end

    subgraph NEXT["NEXT PHASE — Post-Hackathon"]
        direction LR
        X1["Trained ML Model\nscikit-learn Ensemble"]
        X2["Ultrasound Probe\nDirect Device Input"]
        X3["Cloud Deployment\nContainerized Services"]
        X4["Clinical Dataset\nIRB-Approved Data"]
    end

    subgraph FUTURE["LONG TERM — Clinical Readiness"]
        direction LR
        F1["Deep Learning\nImage-Based Analysis"]
        F2["DICOM Integration\nHospital Systems"]
        F3["HIPAA Compliant\nEnd-to-End Encryption"]
        F4["FDA Pathway\nRegulatory Validation"]
    end

    N1 -->|"Model Training"| X1
    N2 -->|"Hardware API"| X2
    N3 -->|"Docker + K8s"| X3
    N4 -->|"Clinical Trials"| X4

    X1 -->|"CNN / Transformers"| F1
    X2 -->|"DICOM Protocol"| F2
    X3 -->|"SOC 2 + HIPAA"| F3
    X4 -->|"Regulatory Filing"| F4

    classDef nowNode fill:#065f46,stroke:#10b981,stroke-width:2px,color:#d1fae5
    classDef nextNode fill:#1e40af,stroke:#3b82f6,stroke-width:2px,color:#dbeafe
    classDef futureNode fill:#581c87,stroke:#a78bfa,stroke-width:2px,color:#ede9fe

    class N1,N2,N3,N4 nowNode
    class X1,X2,X3,X4 nextNode
    class F1,F2,F3,F4 futureNode
```

---

## Data Flow — Prediction Pipeline

```mermaid
sequenceDiagram
    participant C as Clinician
    participant M as Mobile App
    participant A as FastAPI
    participant P as Prediction Engine
    participant D as Supabase

    C->>M: Enter ultrasound metrics\n+ clinical metadata
    activate M
    M->>M: Local validation\n(TypeScript types)
    M->>A: POST /predict\n(JSON payload)
    activate A
    A->>A: Pydantic schema\nvalidation
    A->>P: Forward validated features
    activate P
    P->>P: Weighted scoring\n(9 feature weights)
    P->>P: Risk factor detection\n(threshold analysis)
    P->>P: Classification\n(Accept | Marginal | Decline)
    P-->>A: Viability result\n(score + risks + confidence)
    deactivate P
    A->>D: Store assessment\n(PostgreSQL)
    A-->>M: JSON response
    deactivate A
    M->>M: Render result\n(clinical theme)
    M-->>C: Display viability score\n+ risk factors
    deactivate M

    Note over C,D: Fallback: If API unreachable,\nmobile runs local simulation
```

---

## Why This Stack

| Principle | Implementation | Benefit |
|-----------|---------------|---------|
| **Lightweight** | Expo managed workflow, Streamlit single-file dashboard, FastAPI minimal footprint | Sub-second cold starts, minimal dependencies, rapid iteration |
| **Robust** | TypeScript + Pydantic dual validation, Supabase managed Postgres, JWT auth | Type-safe from client to database, zero data corruption surface |
| **Future-Proof** | Abstract service interfaces, dependency injection, modular ML pipeline | Swap scoring algorithm for trained model without touching API or UI |
| **Cross-Platform** | React Native (iOS/Android/Web), Streamlit (any browser) | One team covers every deployment surface |
| **Clinically Aware** | Dark/light clinical themes, offline fallback, touch-optimized forms | Built for real-world bedside use, not just demo day |
