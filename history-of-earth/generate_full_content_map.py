"""
Generates the Master 100-Episode Content Map for 'History of Earth'.
Chronological journey from 4.54 Ga to Present Day (Hadean to Anthropocene).
Implements exponential resolution scaling:
- Precambrian (Hadean, Archean, Proterozoic): Macro planetary geodynamics & origin of life (26 episodes).
- Paleozoic (Cambrian to Permian): First land ecosystems, giant insects, and mass extinctions (20 episodes).
- Mesozoic (Triassic, Jurassic, Cretaceous): Continental-scale breakdown across North America, South America, Europe, Asia, Africa, Australia, and oceans (29 episodes).
- Cenozoic (Paleocene to Pleistocene & Anthropocene): Mammalian evolution, Ice Ages, megafauna, and human planetary impact (25 episodes).
"""

import csv
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_CSV = os.path.join(PROJECT_ROOT, "content_map.csv")

EPISODES = [
 # ==========================================================================================
 # 1. HADEAN EON (4.54 - 4.0 Ga) [The Primordial Crucible] (6 Episodes)
 # ==========================================================================================
 {
 "era": "Hadean",
 "pillar": "Landscape",
 "working_title": "A World of Fire and Rain",
 "hook": "Earth had no solid ground for 500 million years - here's what 'no ground' actually looked like",
 "runtime_target": "9 min",
 "originality_note": "Cold open: reverse-chronology from ISS view of modern Earth dissolving backward into a magma ocean"
 },
 {
 "era": "Hadean",
 "pillar": "Map",
 "working_title": "The Planet With No Plates - Before Continents Were Born",
 "hook": "Before continents, there was one churning shell - this is what came before Pangaea's ancestors",
 "runtime_target": "8 min",
 "originality_note": "Structured as a 'detective' narration - what evidence tells us this, not just what happened"
 },
 {
 "era": "Hadean",
 "pillar": "Air & Ocean",
 "working_title": "The Sky Was Poison and the Rain Never Stopped",
 "hook": "Steam, sulfur, and a 100+ atmosphere of pressure - how Earth's first boiling emerald ocean formed",
 "runtime_target": "8 min",
 "originality_note": "Data-overlay visual style vs. narrative style; chemical phase transition modeling"
 },
 {
 "era": "Hadean",
 "pillar": "Life Then",
 "working_title": "The Planet Before Life - Genesis in the Abyss",
 "hook": "Nothing lived here - but inside deep-sea hydrothermal cauldrons, dead rocks were learning to code",
 "runtime_target": "7 min",
 "originality_note": "First-person 'if you stood here' framing; microscopic mineral catalytic pore focus"
 },
 {
 "era": "Hadean",
 "pillar": "Leap",
 "working_title": "When Rocks Learned to Cool - The Zircon Code",
 "hook": "Microscopic crystals from the Australian Outback are the only surviving witnesses to Earth's birth",
 "runtime_target": "9 min",
 "originality_note": "Object-biography structure following one 4.404-billion-year-old zircon grain under ion mass spectrometer"
 },
 {
 "era": "Hadean",
 "pillar": "Ending",
 "working_title": "The Bombardment That Almost Reset the Clock",
 "hook": "A storm of mountain-sized asteroids hammered the infant Earth - did it sterilize the crust or spark biology?",
 "runtime_target": "8 min",
 "originality_note": "Explicitly flags scientific uncertainty and crater-dating debates between lunar Apollo samples and dynamic models"
 },

 # ==========================================================================================
 # 2. ARCHEAN EON (4.0 - 2.5 Ga) [The Dawn of Continents & First Life] (8 Episodes)
 # ==========================================================================================
 {
 "era": "Archean: Eoarchean",
 "pillar": "Landscape",
 "working_title": "The First Solid Rock - The 4-Billion-Year-Old Acasta Gneiss",
 "hook": "In Canada's Northwest Territories lies the oldest intact piece of continental crust on Earth",
 "runtime_target": "8 min",
 "originality_note": "Field geology investigation tracking the tonalite-trondhjemite-granodiorite (TTG) cratonic roots"
 },
 {
 "era": "Archean: Eoarchean",
 "pillar": "Life Then",
 "working_title": "LUCA: The Single Ancestor of All Living Things",
 "hook": "Every human, tree, shark, and bacterium traces back to one single microscopic cell 3.8 billion years ago",
 "runtime_target": "8 min",
 "originality_note": "Genomic detective retro-synthesis reconstructing LUCA's 355 universal genes and chemoautotrophic lifestyle"
 },
 {
 "era": "Archean: Paleoarchean",
 "pillar": "Map",
 "working_title": "The Ancient Twins - Pilbara and Kaapvaal: Earth's First Cratons",
 "hook": "Australia and South Africa were once tiny sibling islands in a vast global boiling green ocean",
 "runtime_target": "8 min",
 "originality_note": "Reconstructing the world's very first stable continental crustal nuclei and granite-greenstone belts"
 },
 {
 "era": "Archean: Paleoarchean",
 "pillar": "Life Then",
 "working_title": "The Living Towers - The 3.5-Billion-Year-Old Stromatolites",
 "hook": "Before animals, entire coastlines were built by living, breathing bacterial apartment towers",
 "runtime_target": "8 min",
 "originality_note": "Microbial mat cross-sections showing daily sediment trapping and comparing fossil chert with living Shark Bay colonies"
 },
 {
 "era": "Archean: Mesoarchean",
 "pillar": "Air & Ocean",
 "working_title": "The Orange Haze World - When Methane Ruled the Atmosphere",
 "hook": "Earth did not look blue from space - it was wrapped in a dense, glowing hydrocarbon smog like Titan",
 "runtime_target": "8 min",
 "originality_note": "Photochemical haze simulation contrasting methanogen-dominated sky with today's nitrogen-oxygen atmosphere"
 },
 {
 "era": "Archean: Mesoarchean",
 "pillar": "Map",
 "working_title": "Vaalbara - Earth's Very First Supercontinent",
 "hook": "Long before Pangaea, two micro-cratons locked together to form the first landmass in solar system history",
 "runtime_target": "8 min",
 "originality_note": "Paleomagnetic polar wander paths proving Pilbara and Kaapvaal were fused 3.1 billion years ago"
 },
 {
 "era": "Archean: Neoarchean",
 "pillar": "Leap",
 "working_title": "The Sun Drinkers - The Invention of Oxygenic Photosynthesis",
 "hook": "One tiny mutation in a cyanobacterium learned to split water molecules - and changed planetary physics forever",
 "runtime_target": "9 min",
 "originality_note": "Molecular machine animation of Photosystem II releasing free O2 as a toxic waste product"
 },
 {
 "era": "Archean: Neoarchean",
 "pillar": "Ending",
 "working_title": "The Oceans of Rust - When the Sea Turned Blood Red",
 "hook": "Billions of tons of dissolved iron in the ocean reacted with newborn oxygen - raining rust across the seafloor",
 "runtime_target": "8 min",
 "originality_note": "Tracing the genesis of Earth's Banded Iron Formations (BIFs) that supply 90% of modern industrial steel"
 },

 # ==========================================================================================
 # 3. PROTEROZOIC EON (2.5 Ga - 538.8 Ma) [The Oxygen Cataclysm & Snowball Earth] (12 Episodes)
 # ==========================================================================================
 {
 "era": "Proterozoic: Paleoproterozoic",
 "pillar": "Air & Ocean",
 "working_title": "The Great Oxidation Event - History's Deadliest Gas",
 "hook": "Oxygen was not a gift of life - it was a catastrophic biological poison that wiped out 99% of early species",
 "runtime_target": "9 min",
 "originality_note": "Contrasting anaerobic biosphere collapse with the birth of the first ozone layer protective shield"
 },
 {
 "era": "Proterozoic: Paleoproterozoic",
 "pillar": "Landscape",
 "working_title": "The Huronian Snowball - When Earth Froze for 300 Million Years",
 "hook": "When methane collapsed, temperatures plummeted to -50 deg C and equatorial glaciers locked the globe in ice",
 "runtime_target": "9 min",
 "originality_note": "Glaciological ice sheet thickness modeling and glacial dropstones found in ancient Canadian quartzites"
 },
 {
 "era": "Proterozoic: Paleoproterozoic",
 "pillar": "Map",
 "working_title": "Columbia / Nuna - The Supercontinent That Spanned the Equator",
 "hook": "Two billion years ago, North America, Siberia, and Baltica collided into a colossal equatorial continent",
 "runtime_target": "8 min",
 "originality_note": "Tectonic suture tracking along the Trans-Hudson and Nagssugtoqidian mountain belts"
 },
 {
 "era": "Proterozoic: Paleoproterozoic",
 "pillar": "Life Then",
 "working_title": "The Endosymbiosis Miracle - When Two Cells Became One",
 "hook": "An Asgard archaeon swallowed a bacterium without digesting it - and birthed the ancestor of all animals and plants",
 "runtime_target": "9 min",
 "originality_note": "Deep cellular animation of the mitochondrial merger and the birth of the complex eukaryotic cell"
 },
 {
 "era": "Proterozoic: Mesoproterozoic",
 "pillar": "Air & Ocean",
 "working_title": "The 'Boring' Billion That Wasn't - The Anoxic Canfield Ocean",
 "hook": "For a billion years, oxygen stalled, the oceans turned toxic purple with sulfur, and evolution seemed frozen",
 "runtime_target": "8 min",
 "originality_note": "Reframing the Boring Billion through nutrient scarcity, molybdenum drawdown, and steady evolutionary incubation"
 },
 {
 "era": "Proterozoic: Mesoproterozoic",
 "pillar": "Map",
 "working_title": "Rodinia - The Monolithic Heart of Ancient Continents",
 "hook": "One point one billion years ago, every landmass smashed together into the gigantic supercontinent Rodinia",
 "runtime_target": "8 min",
 "originality_note": "Reconstructing the Grenville Orogeny: mountain ranges as tall as the Himalayas stretching across future North America"
 },
 {
 "era": "Proterozoic: Mesoproterozoic",
 "pillar": "Life Then",
 "working_title": "The Birth of Sex - Bangiomorpha and the Clonal Breakdown",
 "hook": "One point two billion years ago in Arctic Canada, a red alga invented sexual reproduction - and supercharged evolution",
 "runtime_target": "8 min",
 "originality_note": "Examining Bangiomorpha pubescens microfossils under polarized light to show differentiated spores and gametes"
 },
 {
 "era": "Proterozoic: Neoproterozoic",
 "pillar": "Landscape",
 "working_title": "The Sturtian Freeze - A Mile of Ice at the Equator",
 "hook": "Rodinia broke apart, triggering basalt weathering that stripped CO2 from the sky and froze the planet to the tropics",
 "runtime_target": "9 min",
 "originality_note": "Albedo runaway climate modeling: how ice reflective feedback plunged Earth into a 55-million-year frozen desert"
 },
 {
 "era": "Proterozoic: Neoproterozoic",
 "pillar": "Air & Ocean",
 "working_title": "The Marinoan Meltdown - From Icehouse to a 50 deg C Acid Ocean",
 "hook": "Volcanoes pumped out centuries of trapped CO2, melting global glaciers in a torrential boiling acid deluge",
 "runtime_target": "8 min",
 "originality_note": "Analysis of massive global 'Cap Carbonate' geological deposits deposited during the hyper-greenhouse recovery"
 },
 {
 "era": "Proterozoic: Neoproterozoic",
 "pillar": "Map",
 "working_title": "Pannotia and the Trans-Gondwanan Mountain Chains",
 "hook": "Before Pangaea, the continents gathered into short-lived Pannotia, shedding mineral nutrients into the seas",
 "runtime_target": "8 min",
 "originality_note": "Connecting tectonic continental erosion and phosphorus surges directly to the explosion of complex animal life"
 },
 {
 "era": "Proterozoic: Neoproterozoic",
 "pillar": "Life Then",
 "working_title": "The Ediacaran Garden - Earth's Forgotten Quilted Animals",
 "hook": "Before jaws, eyes, or skeletons, gentle quilted creatures like Dickinsonia carpeted the ocean floor in total peace",
 "runtime_target": "9 min",
 "originality_note": "Forensic biomolecule analysis of Dickinsonia cholesterol confirming it was an authentic animal, not a plant or fungus"
 },
 {
 "era": "Proterozoic: Neoproterozoic",
 "pillar": "Ending",
 "working_title": "The First Teeth - The End-Ediacaran Revolution",
 "hook": "The first predatory burrowers tunneled through the microbial mats - destroying the Ediacaran world and opening the Cambrian gate",
 "runtime_target": "8 min",
 "originality_note": "Trace fossils (Treptichnus pedum) showing the agronomic revolution: vertical burrowing that aerated the seafloor"
 },

 # ==========================================================================================
 # 4. PALEOZOIC ERA (538.8 - 251.9 Ma) [The Explosion of Complex Life & The Great Dying] (20 Episodes)
 # ==========================================================================================
 {
 "era": "Paleozoic: Cambrian",
 "pillar": "Life Then",
 "working_title": "The Cambrian Explosion - Burgess Shale and Chengjiang",
 "hook": "In a 20-million-year flash, every modern animal body plan appeared in the fossil record with armor and claws",
 "runtime_target": "9 min",
 "originality_note": "3D biomechanical reconstructions of Anomalocaris, Opabinia, and Hallucigenia from Canadian and Chinese shales"
 },
 {
 "era": "Paleozoic: Cambrian",
 "pillar": "Map",
 "working_title": "The Tropical Laurentian Sea - North America on the Equator",
 "hook": "Five hundred million years ago, North America lay sideways across the equator beneath warm, shallow, sunlit coral seas",
 "runtime_target": "8 min",
 "originality_note": "Paleogeographic reconstruction showing Gondwana at the South Pole and Laurentia bathed in shallow tropical epicontinental seas"
 },
 {
 "era": "Paleozoic: Cambrian",
 "pillar": "Leap",
 "working_title": "The Invention of Vision - The Compound Eye Arms Race",
 "hook": "Trilobites were the first creatures to grow calcified compound eyes - sparking the predator-prey evolutionary war",
 "runtime_target": "8 min",
 "originality_note": "Optical physics of calcite crystal lenses in trilobite eyes (Schizochroal vision) and how light drove armor evolution"
 },
 {
 "era": "Paleozoic: Ordovician",
 "pillar": "Life Then",
 "working_title": "The Ordovician Radiation - Giants of the Cephalopod Seas",
 "hook": "Ten-meter-long shelled cephalopods like Cameroceras ruled the oceans as the first apex marine leviathans",
 "runtime_target": "8 min",
 "originality_note": "Great Ordovician Biodiversification Event (GOBE) tracking plankton diversity and marine food web tiering"
 },
 {
 "era": "Paleozoic: Ordovician",
 "pillar": "Landscape",
 "working_title": "Green on Gray - The First Plants Invade the Dry Land",
 "hook": "Four hundred and seventy million years ago, ancient bryophytes and liverworts crept out of the tidepools onto bare rock",
 "runtime_target": "8 min",
 "originality_note": "Fossil cryptospores and weathering chemistry: how primitive mosses dissolved granite and triggered global cooling"
 },
 {
 "era": "Paleozoic: Ordovician",
 "pillar": "Ending",
 "working_title": "The Hirnantian Ice Age & The First Big Mass Extinction",
 "hook": "A sudden ice sheet locked over the South Pole, freezing the tropics and wiping out 85% of all marine species",
 "runtime_target": "9 min",
 "originality_note": "Dual-pulse extinction mechanism: glacio-eustatic sea-level retreat followed by toxic anoxic ocean flooding"
 },
 {
 "era": "Paleozoic: Silurian",
 "pillar": "Life Then",
 "working_title": "The First Air Breathers - Millipedes and the Land Beachhead",
 "hook": "Pneumodesmus newmani, a tiny millipede from Scotland, preserves the oldest breathing spiracles in the fossil record",
 "runtime_target": "8 min",
 "originality_note": "High-magnification microscopic analysis of fossil breathing pores proving terrestrial respiration 428 million years ago"
 },
 {
 "era": "Paleozoic: Silurian",
 "pillar": "Ocean",
 "working_title": "The Eurypterid Emperors & The Dawn of True Jaws",
 "hook": "Eight-foot sea scorpions stalked coastal lagoons, while humble fish evolved the deadliest weapon in nature: jaws",
 "runtime_target": "8 min",
 "originality_note": "Comparative anatomy: how gill arches morphed into predatory hinged jaws in early gnathostomes"
 },
 {
 "era": "Paleozoic: Devonian",
 "pillar": "Ocean",
 "working_title": "Dunkleosteus - The 4-Ton Armored Guillotine of the Seas",
 "hook": "With self-sharpening bony jaw plates snapping shut with the bite force of a T. rex, Dunkleosteus dominated the Devonian",
 "runtime_target": "9 min",
 "originality_note": "Biomechanical jaw linkage modeling showing 5,000 N bite force and 20-millisecond vacuum strike"
 },
 {
 "era": "Paleozoic: Devonian",
 "pillar": "Landscape",
 "working_title": "The First Forests - How Archaeopteris Suffocated the Oceans",
 "hook": "The first true trees grew deep roots that broke rocks, washed nutrients into rivers, and accidentally choked the seas of oxygen",
 "runtime_target": "9 min",
 "originality_note": "Geochemical soil genesis: how the evolution of deep root systems caused marine eutrophication and global black shales"
 },
 {
 "era": "Paleozoic: Devonian",
 "pillar": "Leap",
 "working_title": "Tiktaalik's Pushup - The Tetrapod Leap to Land",
 "hook": "A fish with wrist bones and a flexible neck hauled itself out of a muddy Canadian stream onto the riverbank",
 "runtime_target": "9 min",
 "originality_note": "Detailed limb anatomy comparison from Tiktaalik to Acanthostega and Ichthyostega showing the evolution of 5-digit hands"
 },
 {
 "era": "Paleozoic: Devonian",
 "pillar": "Ending",
 "working_title": "The Kellwasser Catastrophe - The Late Devonian Extinction",
 "hook": "Warm water coral reefs died out completely, armored placoderm fishes disappeared, and oceans turned black and dead",
 "runtime_target": "8 min",
 "originality_note": "Testing multiple extinction triggers: Viluy and Pripyat volcanic traps versus plant-driven ocean anoxia"
 },
 {
 "era": "Paleozoic: Carboniferous",
 "pillar": "Air & Ocean",
 "working_title": "The 35% Oxygen Sky - When Giant Insects Ruled the Air",
 "hook": "Crowbar-sized dragonflies with 2.5-foot wingspans and 8-foot millipedes crawled through forests supercharged by oxygen",
 "runtime_target": "9 min",
 "originality_note": "Respiratory physiology of spiracle diffusion: why high oxygen allowed Meganeura and Arthropleura to grow to titan sizes"
 },
 {
 "era": "Paleozoic: Carboniferous: Euramerica",
 "pillar": "Landscape",
 "working_title": "The Endless Coal Swamps of Euramerica",
 "hook": "Hundreds of miles of scale trees fell into acidic bogs, unable to decay - locking away carbon to forge modern coal basins",
 "runtime_target": "8 min",
 "originality_note": "The lignin paradox: did bacteria lack the enzymes to rot lignin, or did rapid subsidence bury the trees before decay?"
 },
 {
 "era": "Paleozoic: Carboniferous: Gondwana",
 "pillar": "Landscape",
 "working_title": "The Glacial Wastes of Southern Gondwana",
 "hook": "While Euramerica simmered in tropical swamps, South America, Africa, and Australia froze under giant polar ice caps",
 "runtime_target": "8 min",
 "originality_note": "Glossopteris deciduous leaf drop layers proving cold-adapted vegetation surviving continuous polar winter night"
 },
 {
 "era": "Paleozoic: Carboniferous",
 "pillar": "Leap",
 "working_title": "The Amniotic Egg - The Portable Pond That Conquered Land",
 "hook": "By packaging an embryo inside a waterproof shell, primitive reptiles broke free from water and colonized the continents",
 "runtime_target": "8 min",
 "originality_note": "Comparative embryology of Hylonomus and early amniotes versus amphibian jelly eggs"
 },
 {
 "era": "Paleozoic: Permian",
 "pillar": "Map",
 "working_title": "Pangaea United - The Colossal Supercontinent and Megamonsoons",
 "hook": "Every continent collided into one mega-continent stretching from pole to pole, surrounded by a global ocean",
 "runtime_target": "9 min",
 "originality_note": "Climate modeling of the extreme Pangaean central desert and the hyper-monsoons that swept the coasts"
 },
 {
 "era": "Paleozoic: Permian: Euramerica",
 "pillar": "Life Then",
 "working_title": "The Sail-Backed Monarchs - Dimetrodon in the Texas Red Beds",
 "hook": "Dimetrodon was not a dinosaur - it was a mammal-like synapsid with a giant thermoregulatory solar sail on its spine",
 "runtime_target": "8 min",
 "originality_note": "Vascular bone histology showing blood vessel channels running up the neural spines to regulate body temperature"
 },
 {
 "era": "Paleozoic: Permian: Siberia & Urals",
 "pillar": "Life Then",
 "working_title": "The Gorgonopsid Apex - Inostrancevia and the Saber-Tooth Dawn",
 "hook": "In ancient Russia, 10-foot predatory synapsids with 6-inch sabertooth fangs hunted armored pareiasaurs across the plains",
 "runtime_target": "8 min",
 "originality_note": "Sokolki fossil quarry excavations on the Northern Dvina River detailing therapsid carnivore guild structure"
 },
 {
 "era": "Paleozoic: Permian",
 "pillar": "Ending",
 "working_title": "The Great Dying - When 96% of All Life Vanished",
 "hook": "Two million cubic miles of lava erupted in Siberia, cooking coal seams, acidifying oceans, and bringing Earth to the brink of death",
 "runtime_target": "10 min",
 "originality_note": "Multi-tier lethal synergy model: Siberian Traps volcanic outgassing, ozone destruction, oceanic euxinia, and sulfur release"
 },

 # ==========================================================================================
 # 5. MESOZOIC ERA (251.9 - 66.0 Ma) [The Age of Dinosaurs - Detailed Continental Focus] (29 Episodes)
 # ==========================================================================================
 # --- Triassic Period (7 Episodes) ---
 {
 "era": "Mesozoic: Triassic",
 "pillar": "Landscape",
 "working_title": "The Ash Wasteland - The 10-Million-Year Permian Hangover",
 "hook": "After the Great Dying, the world was a scorching desert where one shovel-beaked mammal ancestor made up 95% of land life",
 "runtime_target": "8 min",
 "originality_note": "Lystrosaurus disaster-taxon dominance and burrowing lifestyle as a survival mechanism in hypoxic environments"
 },
 {
 "era": "Mesozoic: Triassic: Pangaea",
 "pillar": "Life Then",
 "working_title": "The Pseudosuchian Lords - When Crocodile Ancestors Ruled the Earth",
 "hook": "Before dinosaurs rose to power, giant armored crocodile cousins walked upright and sat at the top of the food chain",
 "runtime_target": "8 min",
 "originality_note": "Erect limb posture in Postosuchus and Saurosuchus compared to early humble bipedal dinosaurs"
 },
 {
 "era": "Mesozoic: Triassic",
 "pillar": "Air & Ocean",
 "working_title": "The Carnian Pluvial Episode - The 2-Million-Year Rain That Birthed Dinosaurs",
 "hook": "A sudden volcanic pulse triggered two million years of relentless monsoon rains that broke the Triassic drought and unleashed dinosaurs",
 "runtime_target": "9 min",
 "originality_note": "Wrangellia flood basalt eruptions and the sudden floral turnover from conifer scrub to lush humid fern-forests"
 },
 {
 "era": "Mesozoic: Triassic: South America",
 "pillar": "Life Then",
 "working_title": "Ischigualasto: Valley of the Moon - The First True Dinosaurs",
 "hook": "In the red sandstone canyons of Argentina, agile dog-sized predators like Herrerasaurus and Eoraptor started an empire",
 "runtime_target": "9 min",
 "originality_note": "Ischigualasto Formation stratigraphy showing early dinosaurs comprising less than 10% of the fauna before their explosive rise"
 },
 {
 "era": "Mesozoic: Triassic: North America",
 "pillar": "Life Then",
 "working_title": "The Petrified Forest of Chinle - Coelophysis and the Dawn of Packs",
 "hook": "In the painted deserts of Arizona and New Mexico, hundreds of light-boned agile hunters congregated around vanishing waterholes",
 "runtime_target": "8 min",
 "originality_note": "Ghost Ranch bonebed taphonomy: analyzing thousands of Coelophysis skeletons trapped in a sudden flash flood"
 },
 {
 "era": "Mesozoic: Triassic: Oceans",
 "pillar": "Ocean",
 "working_title": "The Leviathans of Panthalassa - Shonisaurus and the Giant Ichthyosaurs",
 "hook": "Seventy-foot sea monsters shaped like giant whales hunted in deep open waters before the first giant sauropod ever walked land",
 "runtime_target": "8 min",
 "originality_note": "Berlin-Ichthyosaur State Park Nevada bonebed analysis proving schooling behavior in 20-meter marine reptiles"
 },
 {
 "era": "Mesozoic: Triassic",
 "pillar": "Ending",
 "working_title": "The Unzipping of Pangaea - The End-Triassic Mass Extinction",
 "hook": "The Central Atlantic Magma Province tore North America away from Africa, wiping out the giant croc-ancestors and handing Earth to dinosaurs",
 "runtime_target": "9 min",
 "originality_note": "CAMP volcanic pulse dating (201.4 Ma) and carbon isotope excursion correlating directly with pseudosuchian extinction"
 },

 # --- Jurassic Period (8 Episodes) ---
 {
 "era": "Mesozoic: Early Jurassic: Europe",
 "pillar": "Life Then",
 "working_title": "Lyme Regis & The Blue Lias - Mary Anning's Marine Dragons",
 "hook": "Along the stormy English cliffs, 12-year-old Mary Anning uncovered giant ichthyosaurs and long-necked plesiosaurs that shocked science",
 "runtime_target": "9 min",
 "originality_note": "Historical forensic paleontology highlighting Anning's discoveries and the biomechanics of Plesiosaurus and Temnodontosaurus"
 },
 {
 "era": "Mesozoic: Early Jurassic: Africa",
 "pillar": "Life Then",
 "working_title": "The Karoo Storms - Massospondylus and the First Long-Necks",
 "hook": "In southern Africa, primitive prosauropods laid eggs in colonial nests, guarding the delicate beginnings of the giant sauropod lineage",
 "runtime_target": "8 min",
 "originality_note": "Golden Gate Highlands National Park fossilized dinosaur nesting site showing clutches of eggs with embryonic skeletons"
 },
 {
 "era": "Mesozoic: Middle Jurassic: Asia",
 "pillar": "Life Then",
 "working_title": "The Shishugou & Daohugou Forests - China's Feathered Jurassic Dawn",
 "hook": "In the volcanic forests of Xinjiang, primitive tyrannosaurs like Guanlong hunted alongside gliding mammal cousins",
 "runtime_target": "9 min",
 "originality_note": "Spectacular Yanliao Biota preservation revealing dinosaur plumage, membranous bat-like dinosaur wings (Yi qi ancestors), and early mammals"
 },
 {
 "era": "Mesozoic: Late Jurassic: North America",
 "pillar": "Life Then",
 "working_title": "The Morrison Kingdom - Allosaurus, Stegosaurus, and the Giant Sauropods",
 "hook": "One hundred and fifty million years ago, western North America was home to the greatest gathering of colossal dinosaurs in Earth history",
 "runtime_target": "10 min",
 "originality_note": "Dinosaur National Monument quarry wall: niche partitioning between Diplodocus, Brachiosaurus, Camarasaurus, and Allosaurus"
 },
 {
 "era": "Mesozoic: Late Jurassic: Europe",
 "pillar": "Life Then",
 "working_title": "The Solnhofen Lagoons - Archaeopteryx and the Pterodactyl Reefs",
 "hook": "In hypersaline Bavarian lagoons, delicate feather impressions, jellyfish, and Archaeopteryx were locked forever in ultra-fine limestone",
 "runtime_target": "9 min",
 "originality_note": "Synchrotron X-ray fluorescence analysis of Archaeopteryx feather shafts confirming asymmetric aerodynamic flight capability"
 },
 {
 "era": "Mesozoic: Late Jurassic: Africa",
 "pillar": "Life Then",
 "working_title": "Tendaguru: The African Giant Plateau - Giraffatitan and Kentrosaurus",
 "hook": "On the coastal plains of Tanzania, 40-foot-tall Giraffatitan browsed tree crowns while spiky Kentrosaurus defended the lower brush",
 "runtime_target": "9 min",
 "originality_note": "The legendary Berlin Tendaguru expeditions: comparing Gondwanan late Jurassic ecosystems directly to the North American Morrison"
 },
 {
 "era": "Mesozoic: Late Jurassic: South America",
 "pillar": "Life Then",
 "working_title": "The Patagonian Jurassic - Piatnitzkysaurus in the Southern Forests",
 "hook": "While North America boomed with Allosaurus, South America evolved its own unique family of megalosauroid hunters and spiny sauropods",
 "runtime_target": "8 min",
 "originality_note": "Canadon Asfalto Basin stratigraphy showing southern hemisphere provincialism during the late Jurassic"
 },
 {
 "era": "Mesozoic: Late Jurassic: Oceans",
 "pillar": "Ocean",
 "working_title": "The Oxford Clay Monsters - Liopleurodon and Leedsichthys",
 "hook": "Beneath the tropical European seas swam 50-foot filter-feeding fish Leedsichthys, hunted by bone-crushing pliosaurs like Liopleurodon",
 "runtime_target": "8 min",
 "originality_note": "Peterborough brick pit taphonomy: tooth-mark bite analysis on plesiosaur paddles proving pliosaur ambush strikes"
 },

 # --- Cretaceous Period (14 Episodes) ---
 {
 "era": "Mesozoic: Early Cretaceous: Asia",
 "pillar": "Life Then",
 "working_title": "The Pompeii of Paleontology - Yixian's Feathered Dragons",
 "hook": "Volcanic ash in Liaoning buried thousands of dinosaurs with pristine feather coats, scales, internal organs, and stomach contents",
 "runtime_target": "9 min",
 "originality_note": "Microscopic melanosome analysis reconstructing true iridescent black and rust-orange plumage colors in Microraptor and Sinosauropteryx"
 },
 {
 "era": "Mesozoic: Early Cretaceous: Europe",
 "pillar": "Life Then",
 "working_title": "The Wealden Deltas - Iguanodon, Baryonyx, and the Fish Hunters",
 "hook": "In the murky coastal deltas of England and Belgium, fish-hunting spinosaurs like Baryonyx used 12-inch hand claws to gaff giant fish",
 "runtime_target": "8 min",
 "originality_note": "Bernissart mine discovery of 30 intact Iguanodon skeletons in Belgium and Baryonyx acid-etched Lepidotes fish scales"
 },
 {
 "era": "Mesozoic: Early Cretaceous: Australia & Antarctica",
 "pillar": "Life Then",
 "working_title": "Dinosaurs of the Polar Night - Surviving the Antarctic Freezes",
 "hook": "At the South Pole, big-eyed dinosaurs like Leaellynasaura lived through six months of continuous sub-zero darkness without losing heat",
 "runtime_target": "9 min",
 "originality_note": "Dinosaur Cove brain endocasts: enlarged optic lobes proving adaptation to continuous polar winter darkness"
 },
 {
 "era": "Mesozoic: Mid-Cretaceous: Africa",
 "pillar": "Life Then",
 "working_title": "The River of Giants - Spinosaurus and the African Carnivore Swamps",
 "hook": "The Kem Kem river system held three rival giant carnivores larger than T. rex, dominated by the aquatic sail-backed Spinosaurus",
 "runtime_target": "10 min",
 "originality_note": "High-density predator trap paradox: isotopic bone calcium tracking proving Spinosaurus fed primarily on 20-foot Onchopristis sawfish"
 },
 {
 "era": "Mesozoic: Mid-Cretaceous: South America",
 "pillar": "Life Then",
 "working_title": "Land of the Colossi - Argentinosaurus and Giganotosaurus in Patagonia",
 "hook": "In prehistoric Argentina, 100-ton titanosaurs shook the ground while 45-foot Giganotosaurus hunted in coordinated packs",
 "runtime_target": "10 min",
 "originality_note": "Biomechanical weight calculations of Argentinosaurus femurs and trackway analysis from the Candeleros Formation"
 },
 {
 "era": "Mesozoic: Mid-Cretaceous",
 "pillar": "Landscape",
 "working_title": "The Cretaceous Thermal Maximum - Crocodiles at the North Pole",
 "hook": "With atmospheric CO2 spiking over 1,000 ppm, there was zero polar ice anywhere on Earth and palm trees flourished in Alaska",
 "runtime_target": "8 min",
 "originality_note": "Axel Heiberg Island fossil redwood stumps and Champsosaurus crocodile bones found above the Arctic Circle"
 },
 {
 "era": "Mesozoic: Mid-Cretaceous",
 "pillar": "Leap",
 "working_title": "The Floral Revolution - When Flowers and Insects Conquered the World",
 "hook": "Angiosperms invented petals, scent, and fruit - sparking an co-evolutionary explosion with bees, butterflies, and herbivorous dinosaurs",
 "runtime_target": "8 min",
 "originality_note": "Fossil amber inclusions from Myanmar showing early Cretaceous flowers and pollen-coated beetles from 100 million years ago"
 },
 {
 "era": "Mesozoic: Late Cretaceous: North America",
 "pillar": "Ocean",
 "working_title": "The Western Interior Seaway - Hell's Aquarium",
 "hook": "A shallow inland sea split North America in two, teeming with 50-foot mosasaurs, giant sea turtles, and 15-foot predatory bulldog-fish",
 "runtime_target": "9 min",
 "originality_note": "Smoky Hill Chalk fossil beds of Kansas: Xiphactinus swallowing a 6-foot Gillicus whole before fossilizing"
 },
 {
 "era": "Mesozoic: Late Cretaceous: North America",
 "pillar": "Life Then",
 "working_title": "The Twilight of the Tyrants - Hell Creek and the Rule of T. rex",
 "hook": "In the lush floodplains of Montana and the Dakotas, Tyrannosaurus rex, Triceratops, and Ankylosaurus clashed in the final chapter of dinosaurs",
 "runtime_target": "10 min",
 "originality_note": "Hell Creek Formation paleobiology: T. rex bone-crushing biomechanics, Triceratops frill battle punctures, and sensory olfactory bulbs"
 },
 {
 "era": "Mesozoic: Late Cretaceous: Asia",
 "pillar": "Life Then",
 "working_title": "The Flaming Cliffs of the Gobi - Velociraptor and the Desert Titans",
 "hook": "Under sweeping sandstorms in Mongolia, Velociraptor and Protoceratops locked in mortal combat were buried alive in a collapsing dune",
 "runtime_target": "9 min",
 "originality_note": "The famous 'Fighting Dinosaurs' fossil specimen preserved mid-strike; Deinocheirus 8-foot giant arms mystery solved"
 },
 {
 "era": "Mesozoic: Late Cretaceous: Europe",
 "pillar": "Life Then",
 "working_title": "The Island of Dwarfs & Flying Giants - Hateg Island and Hatzegopteryx",
 "hook": "In an isolated island in ancient Romania, sauropods shrank to pony-size while giraffe-sized flying azhdarchid pterosaurs became apex land killers",
 "runtime_target": "9 min",
 "originality_note": "Island dwarfism rule (Foster's Rule) in Magyarosaurus vs. extreme gigantism in the heavy-beaked pterosaur Hatzegopteryx"
 },
 {
 "era": "Mesozoic: Late Cretaceous: South America",
 "pillar": "Life Then",
 "working_title": "The Armored Badlands - Baurusuchus and Dreadnoughtus in Gondwana",
 "hook": "While North America bowed to tyrannosaurs, South America remained an isolated continent of giant titanosaurs and galloping terrestrial crocs",
 "runtime_target": "8 min",
 "originality_note": "Bauru Basin crocodylomorph running adaptations (caniniform fangs) and the 65-ton Dreadnoughtus schrani skeleton"
 },
 {
 "era": "Mesozoic: Late Cretaceous: Madagascar & India",
 "pillar": "Life Then",
 "working_title": "The Island of Monsters - Majungasaurus and the Deccan Volcanoes",
 "hook": "Madagascar drifted into total isolation, producing cannibal theropods and dome-headed frogs, while India drifted across a massive volcanic hotspot",
 "runtime_target": "8 min",
 "originality_note": "Cannibalism tooth-mark evidence on Majungasaurus bones and the lethal pre-extinction Deccan Traps eruptions in India"
 },
 {
 "era": "Mesozoic: End Cretaceous",
 "pillar": "Ending",
 "working_title": "Chicxulub: The Day the Mesozoic Died",
 "hook": "A 6-mile-wide asteroid slammed into Mexico at 45,000 mph, unleashing a 300-foot tsunami, global firestorms, and wiping out 75% of species",
 "runtime_target": "11 min",
 "originality_note": "Tanis North Dakota seismite event: freshwater fish gills packed with glass impact spherules from the first 60 minutes after impact"
 },

 # ==========================================================================================
 # 6. CENOZOIC ERA (66.0 Ma - Present) [The Age of Mammals, Ice Ages & Humanity] (25 Episodes)
 # ==========================================================================================
 # --- Paleocene Epoch (3 Episodes) ---
 {
 "era": "Cenozoic: Paleocene",
 "pillar": "Landscape",
 "working_title": "Day Zero After Impact - The Fern Spike and Mammalian Awakening",
 "hook": "With dinosaurs gone and forests burned to cinders, tiny burrowing mammals emerged from the ash into a world covered in ferns",
 "runtime_target": "8 min",
 "originality_note": "Corral Bluffs Colorado discovery tracking the exact 1-million-year recovery timeline of mammal body sizes and brain weights"
 },
 {
 "era": "Cenozoic: Paleocene: South America",
 "pillar": "Life Then",
 "working_title": "Titanoboa and the 100-Foot Steaming Jungles of Cerrejon",
 "hook": "In the sweltering 34 deg C tropical swamps of ancient Colombia, a 42-foot, 1.25-ton super-snake hunted 10-foot giant turtles",
 "runtime_target": "9 min",
 "originality_note": "Poikilotherm metabolic size ceiling: calculating ambient equatorial temperatures from Titanoboa's massive vertebrae"
 },
 {
 "era": "Cenozoic: Paleocene",
 "pillar": "Air & Ocean",
 "working_title": "The PETM Spike - When Temperatures Soared 8 deg C in 20,000 Years",
 "hook": "A massive catastrophic release of methane hydrates turned the Arctic into a subtropical swamp and acidified the oceans",
 "runtime_target": "8 min",
 "originality_note": "Using the Paleocene-Eocene Thermal Maximum (PETM) as the ultimate deep-time geological analogue for modern fossil fuel emissions"
 },

 # --- Eocene Epoch (5 Episodes) ---
 {
 "era": "Cenozoic: Eocene: North America",
 "pillar": "Life Then",
 "working_title": "The Green River Lakes - Eohippus, Bats, and the First Primates",
 "hook": "Around pristine sub-tropical lakes in Wyoming, fox-sized dawn horses grazed and the first echolocating bats filled the skies",
 "runtime_target": "8 min",
 "originality_note": "Fossil Butte oil shale preservation showing stomach contents, wing membranes in Onychonycteris, and dawn primates"
 },
 {
 "era": "Cenozoic: Eocene: Europe",
 "pillar": "Life Then",
 "working_title": "The Messel Pit Oil Vault - Darwinius and the Giant Ants",
 "hook": "Volcanic gas belches in an ancient German crater lake suffocated primates, giant flightless birds, and 6-inch predatory ants",
 "runtime_target": "8 min",
 "originality_note": "Ida fossil (Darwinius masillae): X-ray and CT imaging showing soft-tissue silhouettes and complete digestive gut contents"
 },
 {
 "era": "Cenozoic: Eocene: Egypt & Tethys",
 "pillar": "Ocean",
 "working_title": "When Whales Walked on Land - The Valley of the Whales",
 "hook": "In the Sahara desert of Egypt, skeletons of 60-foot Basilosaurus still bear tiny, vestigial legs from their walking land ancestors",
 "runtime_target": "9 min",
 "originality_note": "Wadi al-Hitan UNESCO site: transitional sequence from terrestrial Pakicetus to paddling Ambulocetus and oceanic Basilosaurus"
 },
 {
 "era": "Cenozoic: Eocene",
 "pillar": "Map",
 "working_title": "The Great Collision - When India Slammed Into Asia",
 "hook": "Fifty million years ago, the Indian tectonic plate crashed into Asia at 6 inches a year, crumpling the seafloor into the Himalayas",
 "runtime_target": "9 min",
 "originality_note": "Tectonic uplift and silicate weathering: how the rising Himalayas sucked CO2 from the atmosphere and started global cooling"
 },
 {
 "era": "Cenozoic: Eocene",
 "pillar": "Ending",
 "working_title": "The Drake Passage Opens - The Freezing of Antarctica",
 "hook": "South America ripped away from Antarctica, unleashing the Antarctic Circumpolar Current and locking the South Pole in perpetual ice",
 "runtime_target": "8 min",
 "originality_note": "Oceanic gateway modeling: how thermal isolation transformed Antarctica from lush green forests into a frozen polar continent"
 },

 # --- Oligocene Epoch (2 Episodes) ---
 {
 "era": "Cenozoic: Oligocene: North America",
 "pillar": "Life Then",
 "working_title": "The White River Badlands - Hell Pigs and False Sabertooths",
 "hook": "As forests retreated into open savannahs, bone-crushing Entelodonts and saber-toothed Nimravids battled on the plains of Dakota",
 "runtime_target": "8 min",
 "originality_note": "Badlands National Park bonebeds: skull pathology showing Entelodont facial bite marks during intra-species dominance battles"
 },
 {
 "era": "Cenozoic: Oligocene: Asia",
 "pillar": "Life Then",
 "working_title": "Paraceratherium - The 20-Ton Giant of the Asian Steppes",
 "hook": "A hornless rhinoceros as tall as a giraffe and weighing as much as four elephants browsed the tree crowns of prehistoric Kazakhstan",
 "runtime_target": "8 min",
 "originality_note": "Biomechanics of the largest terrestrial mammal to ever walk the Earth: vascular heat shedding and limb column loading limits"
 },

 # --- Miocene Epoch (4 Episodes) ---
 {
 "era": "Cenozoic: Miocene: South America",
 "pillar": "Life Then",
 "working_title": "The Terror Bird Bastion - Phorusrhacids and the Amazon Sea",
 "hook": "In an isolated island continent, 10-foot flightless birds with axe-like beaks and 40-foot super-caimans Purussaurus ruled the wetlands",
 "runtime_target": "9 min",
 "originality_note": "Pebas wetland megasystem taphonomy and strike-force modeling of Andalgalornis axe-swing predatory mechanics"
 },
 {
 "era": "Cenozoic: Miocene: Oceans",
 "pillar": "Ocean",
 "working_title": "Megalodon vs Livyatan - The Battle of the 60-Foot Apex Predators",
 "hook": "The greatest shark in history clashed with a sperm whale with 14-inch teeth in the richest, warmest oceans our planet ever saw",
 "runtime_target": "10 min",
 "originality_note": "Dental histology and bite-force comparisons: 180,000 N bite force of Otodus megalodon targeting whale ribcages"
 },
 {
 "era": "Cenozoic: Miocene: Africa",
 "pillar": "Leap",
 "working_title": "The Great Rift Valley Opens - The Bipedal Ape Awakens",
 "hook": "Tectonic faulting tore East Africa apart, drying the rainforests and forcing ancient hominins onto two legs in the savannah",
 "runtime_target": "9 min",
 "originality_note": "Sahelanthropus tchadensis and Ardipithecus ramidus: pelvic restructuring and the foramen magnum shift toward bipedal walking"
 },
 {
 "era": "Cenozoic: Miocene: Mediterranean",
 "pillar": "Landscape",
 "working_title": "The Messinian Salinity Crisis - When the Mediterranean Dried to Dust",
 "hook": "The Strait of Gibraltar slammed shut, turning the Mediterranean into a 2-mile-deep scorching salt canyon before the Atlantic burst back in",
 "runtime_target": "9 min",
 "originality_note": "Seismic reflection profiling of the 1-mile thick salt bed under the Mediterranean and the catastrophic Zanclean megaflood"
 },

 # --- Pliocene Epoch (2 Episodes) ---
 {
 "era": "Cenozoic: Pliocene: The Americas",
 "pillar": "Map",
 "working_title": "The Great American Interchange - When Panama Linked Two Worlds",
 "hook": "The Isthmus of Panama rose from the sea, triggering the greatest animal invasion in history and redirecting the Gulf Stream",
 "runtime_target": "8 min",
 "originality_note": "Tracking the asymmetric collision: why North American cats, dogs, and bears outcompeted South American native marsupials"
 },
 {
 "era": "Cenozoic: Pliocene: Africa",
 "pillar": "Life Then",
 "working_title": "Lucy in the Afar - Australopithecus and the Laetoli Footprints",
 "hook": "Three point two million years ago in Ethiopia, a 3-foot-tall hominin walked upright, leaving footprints preserved in fresh volcanic ash",
 "runtime_target": "9 min",
 "originality_note": "Biomechanical foot pressure analysis of the Laetoli trail: non-divergent big toe and arch formation identical to modern human walking"
 },

 # --- Pleistocene Epoch [The Ice Ages & Megafauna] (6 Episodes) ---
 {
 "era": "Cenozoic: Pleistocene: North America",
 "pillar": "Life Then",
 "working_title": "The Mammoth Steppe of North America - Smilodon and the Tar Pits",
 "hook": "Columbian mammoths, American lions, and dire wolves roamed the grasslands of California, falling into bubbling asphalt seeps",
 "runtime_target": "9 min",
 "originality_note": "La Brea Tar Pits micro-taphonomy: analyzing healed bone fractures and social pack behavior in Smilodon fatalis"
 },
 {
 "era": "Cenozoic: Pleistocene: Eurasia",
 "pillar": "Life Then",
 "working_title": "The Woolly Giants of the Mammoth Steppe - Siberia to Europe",
 "hook": "Across a 10,000-mile unbroken cold prairie, woolly mammoths, woolly rhinos, and cave hyenas lived alongside Neanderthal clans",
 "runtime_target": "9 min",
 "originality_note": "Siberian permafrost mummies (Yuka and Lyuba): intact stomach vegetation, hemoglobin cold-adaptation, and cave art accuracy"
 },
 {
 "era": "Cenozoic: Pleistocene: Australia",
 "pillar": "Life Then",
 "working_title": "The Land of Giant Marsupials - Diprotodon and Megalania",
 "hook": "In prehistoric Australia, 3-ton wombats and 20-foot venomous monitor lizards ruled a land with zero placental mammal competitors",
 "runtime_target": "8 min",
 "originality_note": "Lake Callabonna fossil beds: Diprotodon herds trapped in saline lake muds and the impact of First Nations mosaic burning"
 },
 {
 "era": "Cenozoic: Pleistocene: South America",
 "pillar": "Life Then",
 "working_title": "The Living Tanks of the Pampas - Megatherium and Glyptodon",
 "hook": "Volkswagen-sized armadillos with spiked tail clubs and 20-foot ground sloths with clawed paws dominated the Argentine grasslands",
 "runtime_target": "8 min",
 "originality_note": "Paleoburrows: massive underground tunnels carved into bedrock in Brazil by the claws of giant ground sloths"
 },
 {
 "era": "Cenozoic: Pleistocene: Global",
 "pillar": "Leap",
 "working_title": "Homo sapiens Arrives - The 300,000-Year Global Migration",
 "hook": "From Jebel Irhoud in Morocco, modern humans crossed deserts, coasts, and ice sheets with language, art, and projectile weapons",
 "runtime_target": "10 min",
 "originality_note": "Ancient DNA hybridization mapping showing Neanderthal and Denisovan introgression across human regional populations"
 },
 {
 "era": "Cenozoic: Pleistocene",
 "pillar": "Ending",
 "working_title": "The Quaternary Extinction - The Sudden Collapse of the Giants",
 "hook": "Within a few thousand years, almost every mammal weighing over 100 pounds vanished from North America, South America, and Australia",
 "runtime_target": "9 min",
 "originality_note": "Disentangling the climate change vs. human overkill debate: radiocarbon dating correlation spikes and Sporormiella spore decline"
 },

 # --- Holocene Epoch & The Anthropocene (3 Episodes) ---
 {
 "era": "Holocene: Early to Mid",
 "pillar": "Landscape",
 "working_title": "The Green Sahara & Doggerland - Earth's Changing Shorelines",
 "hook": "Eight thousand years ago, the Sahara was a paradise of lakes and hippos, while Britain was joined to Europe across Doggerland",
 "runtime_target": "9 min",
 "originality_note": "Marine core bathymetry and Storegga Slide tsunami deposits that permanently submerged the inhabited heart of northern Europe"
 },
 {
 "era": "Holocene: Late",
 "pillar": "Life Then",
 "working_title": "The Tamed Planet - Agriculture, Cities, and the Human Force",
 "hook": "In 10,000 years, one single species cleared half the planet's forests, diverted its rivers, and domesticated its megafauna",
 "runtime_target": "9 min",
 "originality_note": "Geomorphological human sediment movement: humans moving more rock and soil annually than all natural rivers combined"
 },
 {
 "era": "Anthropocene: Present & Future",
 "pillar": "Ending",
 "working_title": "The Sixth Epoch - Earth in the Hands of Humanity",
 "hook": "Plastics, concrete, radioactive fallout, and 420 ppm CO2: what the geological stratum of modern civilization will look like in 100 million years",
 "runtime_target": "10 min",
 "originality_note": "Golden Spike stratigraphic candidate analysis (Crawford Lake plutonium signals) and the future of Earth across the next billion years"
 }
]


def main():
 print(f"Generating Master Content Map: {len(EPISODES)} episodes...")
 fieldnames = ["era", "pillar", "working_title", "hook", "runtime_target", "originality_note"]

 with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
 writer = csv.DictWriter(f, fieldnames=fieldnames)
 writer.writeheader()
 for ep in EPISODES:
 writer.writerow(ep)

 print(f"Successfully generated {len(EPISODES)} episodes in {OUTPUT_CSV}!")


if __name__ == "__main__":
 main()
