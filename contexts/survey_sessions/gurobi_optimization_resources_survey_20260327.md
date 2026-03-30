# Gurobi Industry-Level Optimization Learning Resources

## Core Recommendation: The Definitive Modern Python Optimization Book

If there is only **one** resource you use to learn modern, industry-level mathematical optimization with Python, it should be:

### **"Hands-On Mathematical Optimization with Python" (2025)**
- **Authors:** Krzysztof Postek, Alessandro Zocca, Joaquim Gromicho, Jeffrey Kantor
- **Publisher:** Cambridge University Press (Early 2025)
- **Why it's the gold standard:** This book is specifically designed to bridge the gap between theoretical math and practical, hands-on Python coding for real-world scenarios. 
- **What it covers:** Linear and network optimization, convex optimization, and optimizations under uncertainty. It tackles real-life challenges like production planning, portfolio optimization, scheduling, and traveling salesman problems.
- **Companion Resources:** The true value of this book is its companion GitHub repository containing over 50 Jupyter notebooks. You can interact with the code at [mobook.github.io/MO-book](https://mobook.github.io/MO-book/intro.html).

---

## Free Official Gurobi Training Paths

Since Gurobi is the industry standard, their official learning paths are surprisingly excellent and completely free (though you do have to register).

### 1. The "Intro to Optimization" Udemy Course
- **Created by:** Gurobi in partnership with Dr. Joel Sokol (Georgia Tech).
- **Focus:** Teaching optimization decision-making through the lens of data science. This is a highly recommended starting point for understanding the "why" and "how" before deep-diving into code.
- **Link:** [Gurobi's Free Educational Resources](https://www.gurobi.com/learn)

### 2. Gurobi Academy: "From Zero To Hero"
- **Focus:** Designed for people with little-to-no optimization experience, teaching how to identify when to apply optimization and develop simple models.
- **Link:** [Gurobi Learning Paths](https://gurobi.com/lp/academics/learning-path)

### 3. Gurobi Python API Tutorials & Modeling Examples
- **Focus:** Once you understand the concepts, this is where you learn the syntax. Gurobi provides an extensive library of Jupyter Notebooks demonstrating their Python API (`gurobipy`).
- **Topics Covered:** Facility location, airline planning, battery scheduling, adding decision variables, building linear expressions, and handling constraints.
- **Link:** [Gurobi Modeling Examples](https://gurobi.github.io/modeling-examples/)

---

## Advanced & Practical Implementations (GitHub)

To see how real companies build optimization models, exploring high-quality open-source projects is crucial.

### 1. Gurobi OptiMods
- **Repository:** [Gurobi/gurobi-optimods](https://github.com/Gurobi/gurobi-optimods)
- **What it is:** An open-source Python library offering data-driven APIs for common optimization tasks. It shows how to build robust, reusable optimization modules using `pandas`, `numpy`, and `gurobipy`.

### 2. Gurobi Machine Learning
- **Repository:** [Gurobi/gurobi-machinelearning](https://github.com/Gurobi/gurobi-machinelearning)
- **What it is:** For advanced use cases, this repo shows how to embed trained machine learning models (like scikit-learn predictors or PyTorch neural networks) directly into Gurobi optimization models.

---

## A Classic Foundational Text (If you need deeper theory)

### **"Model Building in Mathematical Programming" (5th Edition)**
- **Author:** H.P. Williams
- **Why it's useful:** This is considered the bible for formulating optimization models. It doesn't teach you Python, but it teaches you *how to think* about complex constraints and objectives. 
- **Practical Application:** Gurobi explicitly bases several of its official Jupyter Notebook tutorials on the examples from this book. You can find unofficial Python implementations of the book's exercises on GitHub (e.g., [ash7erix/model_building_assignments](https://github.com/ash7erix/model_building_assignments)).

---

## Alternative Open-Source Solvers (For Practice)

While Gurobi is the gold standard, its commercial licenses are notoriously expensive. If you ever need to build a model without a Gurobi license, it's worth knowing the open-source alternatives:

### **Pyomo — Optimization Modeling in Python**
- **What it is:** A comprehensive book (Springer, 3rd Edition, 2021) covering Pyomo, an open-source Python optimization modeling framework.
- **Why it matters:** Pyomo allows you to write the model once and solve it with *any* solver (including Gurobi, CPLEX, or free solvers like GLPK/CBC). It's a very common framework in industry when companies don't want vendor lock-in with a specific solver.