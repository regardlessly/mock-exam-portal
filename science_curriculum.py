"""Sec 1 Express (G3) Lower Secondary Science curriculum — MOE syllabus aligned.

Topic IDs use the 101+ range so they never clash with Mathematics (1–14).
Each topic mirrors the math-quest structure: meta + subtopics + MCQ bank.
"""

# (id, semester, title, description, [subtopics])
SCIENCE_TOPICS = [
    (101, 1, "Introduction to Science & the Laboratory",
     "Scientific method, lab apparatus, safety rules, hazard symbols",
     ["Branches of Science", "Scientific Method & Variables", "Laboratory Apparatus",
      "Laboratory Safety & Hazard Symbols", "Bunsen Burner"]),

    (102, 1, "Physical Quantities, Units & Measurement",
     "SI units, length, volume, mass, time, density, measuring instruments",
     ["SI Base Units & Prefixes", "Measuring Length", "Measuring Volume",
      "Measuring Mass & Time", "Density"]),

    (103, 1, "Particulate Nature of Matter",
     "Kinetic particle theory, states of matter, changes of state, diffusion",
     ["States of Matter", "Kinetic Particle Theory", "Changes of State",
      "Diffusion", "Brownian Motion"]),

    (104, 1, "Elements, Compounds & Mixtures",
     "Atoms, molecules, classification of matter, chemical symbols",
     ["Atoms & Molecules", "Elements & Symbols", "Compounds",
      "Mixtures", "Comparing Compounds & Mixtures"]),

    (105, 1, "Separation Techniques",
     "Filtration, evaporation, distillation, chromatography, magnetism",
     ["Filtration & Evaporation", "Distillation", "Chromatography",
      "Using a Separating Funnel", "Choosing a Method"]),

    (106, 1, "Solutions & Solubility",
     "Solute, solvent, solution, suspension, saturation, solubility",
     ["Solute, Solvent & Solution", "Suspensions & Colloids",
      "Saturated Solutions", "Factors Affecting Solubility"]),

    (107, 1, "Cells — The Basic Unit of Life",
     "Plant & animal cells, organelles, microscope, cell organisation",
     ["The Microscope", "Animal Cells", "Plant Cells",
      "Comparing Cells", "Cells, Tissues, Organs & Systems"]),

    (108, 2, "Movement of Substances",
     "Diffusion and osmosis in living systems, surface area to volume",
     ["Diffusion in Cells", "Osmosis", "Surface Area to Volume Ratio"]),

    (109, 2, "Human Digestive System",
     "Nutrients, enzymes, digestive organs, absorption, balanced diet",
     ["Nutrients & Food Tests", "Enzymes in Digestion", "Digestive Organs",
      "Absorption & Assimilation", "Balanced Diet"]),

    (110, 2, "Transport in Living Things",
     "Human circulatory system, transport in plants",
     ["The Heart & Blood Vessels", "Blood", "Transport in Plants"]),

    (111, 2, "Energy",
     "Energy forms, conversions, conservation, energy from food, sources",
     ["Forms of Energy", "Energy Conversions", "Conservation of Energy",
      "Energy from Food", "Energy Sources"]),

    (112, 2, "Forces",
     "Types of forces, effects of forces, friction, weight vs mass",
     ["Types of Forces", "Effects of Forces", "Friction",
      "Mass, Weight & Gravity", "Springs & Hooke's Law"]),

    (113, 2, "Electrical Systems",
     "Electric circuits, current, conductors/insulators, series & parallel",
     ["Electric Circuits & Symbols", "Conductors & Insulators",
      "Series & Parallel Circuits", "Effects of Electric Current",
      "Electrical Safety"]),

    (114, 2, "Ray Model of Light",
     "Light, reflection, refraction, the eye, colour",
     ["Light & Luminous Objects", "Reflection of Light",
      "Refraction of Light", "The Human Eye"]),
]
