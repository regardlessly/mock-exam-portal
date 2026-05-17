"""Sec 1 (G3) Lower Secondary Geography curriculum — MOE syllabus aligned.

Topic IDs use the 301+ range so they never clash with Mathematics (1–14),
Science (101–114) or Chinese (201–212). Each topic mirrors the existing
structure: meta + subtopics + MCQ bank. Plain English text — no KaTeX / no `$`.
"""

# (id, semester, title, description, [subtopics])
GEOGRAPHY_TOPICS = [
    (301, 1, "Geographical Skills: Maps & Map Reading",
     "Grid references, scale, distance, direction, conventional symbols",
     ["Conventional Symbols", "Four & Six-Figure Grid References",
      "Scale & Measuring Distance", "Direction & Bearings"]),

    (302, 1, "Geographical Skills: Relief, Photographs & GIS",
     "Contours and relief, cross-sections, photographs, GIS basics",
     ["Contours & Relief", "Cross-Sections", "Interpreting Photographs",
      "Geographical Information Systems (GIS)"]),

    (303, 1, "Weather & Climate: Elements & Instruments",
     "Elements of weather, weather instruments, the Stevenson screen",
     ["Elements of Weather", "Weather Instruments",
      "The Stevenson Screen", "Recording & Reading Weather Data"]),

    (304, 1, "Factors Affecting Temperature & Rainfall",
     "Latitude, altitude, distance from sea, types of rainfall",
     ["Factors Affecting Temperature", "Altitude & Continentality",
      "Convectional & Relief Rainfall", "Frontal Rainfall"]),

    (305, 1, "Climate Graphs & Data Interpretation",
     "Reading and interpreting climate graphs, data and tables",
     ["Reading Climate Graphs", "Describing Temperature Patterns",
      "Describing Rainfall Patterns", "Interpreting Data Tables"]),

    (306, 1, "The Water Cycle & Drainage Basins",
     "Hydrological cycle, drainage basin components, key terms",
     ["The Water Cycle", "Drainage Basin Components",
      "Infiltration & Surface Runoff", "Drainage Basin Terms"]),

    (307, 2, "Rivers & River Landforms",
     "River processes, the long profile, erosional & depositional landforms",
     ["River Processes", "Upper Course Landforms",
      "Middle & Lower Course Landforms", "Floodplains & Deltas"]),

    (308, 2, "Water Resources & Management",
     "Water supply, demand, scarcity, and management strategies",
     ["Sources of Water", "Causes of Water Scarcity",
      "Water Management Strategies", "Singapore's Four National Taps"]),

    (309, 2, "Tropical Rainforest Ecosystems",
     "Structure, climate, adaptations, and value of tropical rainforests",
     ["Rainforest Climate", "Rainforest Structure & Layers",
      "Plant & Animal Adaptations", "Value & Deforestation"]),

    (310, 2, "Variable Weather & Climate Change",
     "Hazards from variable weather, climate change causes and impacts",
     ["Variable Weather Hazards", "Causes of Climate Change",
      "Impacts of Climate Change", "Responses & Mitigation"]),

    (311, 2, "Natural Vegetation & Biomes",
     "World biomes, vegetation belts and their characteristics",
     ["Major World Biomes", "Vegetation & Climate Links",
      "Hot Desert Vegetation", "Mangrove & Coastal Vegetation"]),

    (312, 2, "Tourism & Sustainable Development",
     "Tourism growth, impacts, and sustainable / responsible tourism",
     ["Growth of Tourism", "Economic & Social Impacts",
      "Environmental Impacts", "Sustainable Tourism"]),
]
