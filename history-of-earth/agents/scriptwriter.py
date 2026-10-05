"""
Scriptwriter Agent for History of Earth (Cinematic YouTube Screenplay Engine).
Produces high-retention, 7-scene episodic movie screenplays with dramatic hooks,
continuous pacing, and a high-stakes mysterious cliffhanger ending.
"""

from typing import Dict, List, Any, Optional

CINEMATIC_SCENES = [
    {
        "scene_id": 1,
        "title": "THE DEATH OF A SISTER WORLD",
        "scene_type": "theia_impact",
        "scene_asset": "assets/scenes/theia_impact.jpg",
        "camera_style": "rapid_impact_zoom_with_shake",
        "narration": (
            "Look at the ground beneath your feet. It feels solid. Permanent. Safe.\n\n"
            "Four and a half billion years ago, there was no ground. There was only fire, poison, and a sky that wanted to kill you.\n\n"
            "In the blackness of the newborn solar system, a rogue planet named Theia—the size of Mars—is screaming through the dark at twenty-five thousand miles per hour. "
            "It is locked on a direct collision course with the infant Earth.\n\n"
            "The impact does not merely crack the crust. It obliterates it. Trillions of tons of vaporized mantle detonate into space, lighting up the void with a blinding kinetic supernova."
        )
    },
    {
        "scene_id": 2,
        "title": "A WORLD OF LIQUID ROCK",
        "scene_type": "magma_ocean",
        "scene_asset": "assets/scenes/magma_ocean.jpg",
        "camera_style": "panoramic_lava_tracking_sweep",
        "narration": (
            "From the ashes of that planetary collision rises a nightmare: an unbroken ocean of boiling magma, one thousand kilometers deep.\n\n"
            "Tides of liquid basalt surge across the burning horizon, pulled by a newborn Moon orbiting terrifyingly close—dominating half the blood-red sky.\n\n"
            "For tens of millions of years, the inferno refuses to sleep. Heavy molten iron plunges through liquid rock toward the center, forging the planet’s magnetic shield. "
            "Earth is hammering out its heart inside a planetary furnace."
        )
    },
    {
        "scene_id": 3,
        "title": "THE GREAT CONDENSATION",
        "scene_type": "torrential_rain",
        "scene_asset": "assets/scenes/torrential_rain.jpg",
        "camera_style": "vertical_lightning_deluge_tilt",
        "narration": (
            "Above the magma waves, the atmosphere is a crushing vault of supercritical steam and sulfur, with pressure fierce enough to pulverize steel.\n\n"
            "Then, temperature physics hits an irreversible tipping point. The planet drops below three hundred degrees Celsius... and the sky shatters.\n\n"
            "Rain falls continuously for centuries. Torrential, boiling, acidic downpours crash onto cooling basalt rocks. "
            "Steam geysers roar into the emerald clouds, only to fall again, pooling into Earth’s very first ocean: scalding, emerald-green, and saturated with dissolved iron."
        )
    },
    {
        "scene_id": 4,
        "title": "THE IMPOSSIBLE WITNESS",
        "scene_type": "jack_hills_zircon",
        "scene_asset": "assets/scenes/jack_hills_zircon.jpg",
        "camera_style": "macro_luminescence_dolly",
        "narration": (
            "For decades, science taught that the Hadean was an unlivable wasteland—a hell with no memory.\n\n"
            "They were wrong.\n\n"
            "In the ancient red dirt of Western Australia's Jack Hills, geologists extracted a microscopic crystal no thicker than a human hair: a zircon grain, dated to 4.404 billion years old.\n\n"
            "Trapped inside its atomic lattice was an impossible secret: oxygen isotope signatures proving that cool liquid water and granitic continents existed almost immediately after the magma sea froze."
        )
    },
    {
        "scene_id": 5,
        "title": "THE FINAL BOMBARDMENT",
        "scene_type": "late_bombardment",
        "scene_asset": "assets/scenes/late_bombardment.jpg",
        "camera_style": "crane_pullback_meteor_shockwaves",
        "narration": (
            "Yet just as the crust began to heal, the universe launched a final, cataclysmic assault: the Late Heavy Bombardment.\n\n"
            "Asteroids the size of entire mountain ranges rained down from the sky, detonating like thermonuclear warheads across the boiling oceans.\n\n"
            "Yet against all astronomical odds, Earth held. Every drop of water in your cells, every mineral in your bones, and the ground beneath your feet was forged in this dawn of fire."
        )
    },
    {
        "scene_id": 6,
        "title": "INTO THE BLACK ABYSS",
        "scene_type": "hydrothermal_vent",
        "scene_asset": "assets/scenes/hydrothermal_vent.jpg",
        "camera_style": "deep_abyssal_descent",
        "narration": (
            "The firestorms above eventually faded. But the real story wasn't happening on the surface.\n\n"
            "Four miles beneath the boiling green waves, in total and suffocating blackness, the sea floor opened up.\n\n"
            "Towering mineral chimneys—black smokers—began spewing superheated chemical soups into the dark. Heat, pressure, and volcanic sulfur met for the first time in an abyssal cauldron."
        )
    },
    {
        "scene_id": 7,
        "title": "THE MYSTERIOUS AWAKENING (CLIFFHANGER)",
        "scene_type": "life_spark_cliffhanger",
        "scene_asset": "assets/scenes/life_spark_cliffhanger.jpg",
        "camera_style": "mysterious_macro_spark_drift",
        "narration": (
            "And here, in the pitch-black depths of this volcanic grave... something impossible began to stir.\n\n"
            "Microscopic organic molecules were locking together on metallic crystals, forming the first self-replicating chains.\n\n"
            "Chemistry was crossing the forbidden threshold into code. Dead rock was learning to breathe.\n\n"
            "How did poisonous chemical dust spark into life? And what looming planetary catastrophe almost snuffed it out before it could even begin?\n\n"
            "Next time, on History of Earth: The Archean Dawn — The Secret of the Black Smokers.\n\n"
            "Hit subscribe, and ring the bell. Because Earth's darkest mystery... has only just begun."
        )
    }
]


CINEMATIC_SCENES_HADEAN_MAP = [
    {
        "scene_id": 1,
        "title": "THE UNBROKEN PRISON",
        "scene_type": "stagnant_lid_sphere",
        "scene_asset": "pipeline/cinematic_animator.py:1",
        "camera_style": "3d_orbital_scan_with_detective_hud",
        "mood": "cosmic_mystery",
        "narration": (
            "Open any geology textbook in the world, and you will find a map of plates. "
            "Fifteen colossal jigsaw pieces sliding, colliding, and recycling the surface of the Earth.\n\n"
            "Continental drift is the master engine of our world. But rewind the clock four point four billion years... and that engine did not exist.\n\n"
            "In the dawn of the Hadean eon, our planet was trapped in a single, unbroken rocky cage. "
            "No Pacific plate. No Atlantic rift. No subduction trenches. Just one monolithic, rigid basalt shell capping a churning planetary mantle.\n\n"
            "Geophysicists call this the Stagnant Lid. And for five hundred million years, Earth was a world with no plates."
        )
    },
    {
        "scene_id": 2,
        "title": "THE HEAT-PIPE FURNACE",
        "scene_type": "heat_pipe_furnace",
        "scene_asset": "pipeline/cinematic_animator.py:2",
        "camera_style": "mantle_cross_section_convection_loops",
        "mood": "internal_furnace",
        "narration": (
            "Underneath this unbroken crust, a monstrous engine was trapped.\n\n"
            "Primordial radioactivity was three times hotter than today. "
            "Billions of tons of molten rock churned violently against the ceiling of the shell with nowhere to go.\n\n"
            "Without plate tectonics to pull cool crust down, how did Earth keep from detonating?\n\n"
            "It survived through an alien mechanism: volcanic heat pipes. "
            "Towering conduits pierced straight through the shell, pumping torrential flood basalts across the surface—cooling the interior through continuous, apocalyptic eruption. "
            "Earth did not drift. It boiled in place."
        )
    },
    {
        "scene_id": 3,
        "title": "THE 500-MILLION-YEAR CRIME SCENE",
        "scene_type": "vanished_world_timeline",
        "scene_asset": "pipeline/cinematic_animator.py:3",
        "camera_style": "geological_column_laser_disintegration",
        "mood": "forensic_investigation",
        "narration": (
            "Here is the detective mystery that kept geologists awake for a century.\n\n"
            "If Earth was locked in a stagnant lid... where did all the evidence go?\n\n"
            "Every square mile of modern oceanic crust is recycled within two hundred million years. "
            "And of the ancient Hadean rock that formed this planetary shell? Exactly zero percent survives intact. Not a single cliff. Not a single boulder.\n\n"
            "Five hundred million years of planetary history... erased from the geologic record.\n\n"
            "How do we know the stagnant lid existed? And what clues could possibly survive a half-billion-year forensic void?"
        )
    },
    {
        "scene_id": 4,
        "title": "THE ATOMIC WITNESS",
        "scene_type": "zircon_mass_spectrometry",
        "scene_asset": "pipeline/cinematic_animator.py:4",
        "camera_style": "laser_ablation_mass_spectrometry",
        "mood": "atomic_discovery",
        "narration": (
            "The answer was hiding inside a microscopic time capsule.\n\n"
            "In the ancient red dirt of Western Australia's Jack Hills, scientists discovered tiny, indestructible mineral crystals: detrital zircons, dated to 4.404 billion years ago.\n\n"
            "When geochemists fired secondary ion mass spectrometers and atom-probe tomography beams into their crystal lattice, they uncovered an impossible chemical signature.\n\n"
            "The titanium-in-zircon thermometer revealed crystallization temperatures of just six hundred and eighty degrees Celsius.\n\n"
            "Dry basalt under a stagnant lid melts at eleven hundred degrees. "
            "Six hundred and eighty degrees can only mean one thing: granite forming in the presence of water. The stagnant shell had an invisible fracture."
        )
    },
    {
        "scene_id": 5,
        "title": "THE GREAT RUPTURE",
        "scene_type": "great_rupture_subduction",
        "scene_asset": "pipeline/cinematic_animator.py:5",
        "camera_style": "lithospheric_fracture_subduction_descent",
        "mood": "tectonic_rupture",
        "narration": (
            "Over hundreds of millions of years, the cold basalt shell grew thicker and heavier, until gravitational instability reached a catastrophic tipping point.\n\n"
            "The rigid shell began to buckle under its own immense weight.\n\n"
            "Then, across thousands of miles of primordial ocean... the lid cracked.\n\n"
            "Cold, dense oceanic crust broke free and plunged downward into the incandescent mantle. The very first subduction zone on Earth was born.\n\n"
            "Frictional shear heating lit up the fault plane with blinding energy, unleashing planet-shattering megaquakes as mobile plate tectonics awakened for the very first time."
        )
    },
    {
        "scene_id": 6,
        "title": "FORGING THE ANCESTORS",
        "scene_type": "birth_of_cratons",
        "scene_asset": "pipeline/cinematic_animator.py:6",
        "camera_style": "island_arc_collision_cratonic_keel",
        "mood": "continental_majesty",
        "narration": (
            "As the hydrated oceanic slab plunged into the mantle, it triggered a miracle of chemistry.\n\n"
            "Water lowered the melting point of rock, creating buoyant, silica-rich granitic magmas that bubbled toward the surface.\n\n"
            "Volcanic island arcs drifted together on conveyor belts of rock, crashing and fusing into the first stable, buoyant landmasses: cratons.\n\n"
            "The Pilbara Craton in Australia. The Kaapvaal Craton in Africa. Light enough to float on the mantle, and strong enough to endure four billion years of planetary violence.\n\n"
            "These were not just rocks. They were the ancient great-grandfathers of Pangaea—and the bedrock of the continents we walk on today."
        )
    },
    {
        "scene_id": 7,
        "title": "THE DEGASSING INFERNO (CLIFFHANGER)",
        "scene_type": "degassing_crisis_cliffhanger",
        "scene_asset": "pipeline/cinematic_animator.py:7",
        "camera_style": "supervolcanic_outgassing_greenhouse_surge",
        "mood": "cliffhanger_suspense",
        "narration": (
            "The birth of moving plates saved Earth from a dead stagnant fate. But it ignited a brand new planetary catastrophe.\n\n"
            "As billions of tons of water-soaked crust plunged into the deep mantle, the planet exhaled.\n\n"
            "Monstrous volcanic arcs exploded across the globe, pumping gigatons of steam, carbon dioxide, and poisonous sulfur into the sky.\n\n"
            "Atmospheric pressure soared to nearly one hundred atmospheres. The skies choked into a suffocating, boiling green vault of acid and darkness.\n\n"
            "How did Earth survive a runaway greenhouse inferno? And what triggered the deluge of boiling rain that forged the world's first ocean?\n\n"
            "Next time, on History of Earth: The Sky Was Poison and the Rain Never Stopped.\n\n"
            "Subscribe, ring the bell, and join us... as the clouds begin to fall."
        )
    }
]


CINEMATIC_SCENES_HADEAN_AIR_OCEAN = [
    {
        "scene_id": 1,
        "title": "THE PRESSURE VAULT",
        "scene_type": "supercritical_steam_vault",
        "scene_asset": "assets/scenes/supercritical_steam_vault.jpg",
        "camera_style": "downward_pressure_push_with_haze",
        "mood": "internal_furnace",
        "narration": (
            "Take a breath. Feel the cool, clean air filling your lungs.\n\n"
            "Four point four billion years ago, a single breath would have dissolved your lungs and crushed your body with the force of an industrial hydraulic press.\n\n"
            "In the aftermath of the planetary magma ocean, infant Earth was sealed inside an impenetrable atmospheric vault. "
            "One hundred to two hundred atmospheres of supercritical steam, dense carbon dioxide, and choking sulfur gas pulverized the black basalt below.\n\n"
            "The sky was not blue. It was an ominous, suffocating amber vault of acid, pressure, and perpetual darkness.\n\n"
            "How could a liquid ocean ever form inside this planetary pressure furnace?"
        )
    },
    {
        "scene_id": 2,
        "title": "THE FAINT YOUNG SUN PARADOX",
        "scene_type": "faint_young_sun_haze",
        "scene_asset": "assets/scenes/faint_young_sun_haze.jpg",
        "camera_style": "solar_haze_telemetry_scan",
        "mood": "cosmic_mystery",
        "narration": (
            "Peer through this toxic sulfur veil into deep space, and astrophysics reveals an impossible paradox.\n\n"
            "Four billion years ago, our newborn Sun was weak—burning twenty-five to thirty percent fainter than it does today.\n\n"
            "By all laws of stellar physics, infant Earth should have frozen solid into a lifeless, dead snowball of cosmic ice.\n\n"
            "So why did the world stay liquid?\n\n"
            "Because the poisonous sky was a colossal greenhouse trap. "
            "Gigatons of volcanic carbon dioxide and methane formed an impenetrable thermal blanket, capturing every single watt of internal heat.\n\n"
            "Earth did not freeze. It simmered at the boiling edge of planetary physics."
        )
    },
    {
        "scene_id": 3,
        "title": "THE THERMAL TIPPING POINT",
        "scene_type": "atmospheric_condensation_shatter",
        "scene_asset": "assets/scenes/atmospheric_condensation_shatter.jpg",
        "camera_style": "vertical_deluge_lightning_tilt",
        "mood": "tectonic_rupture",
        "narration": (
            "For tens of millions of years, the inferno refused to surrender.\n\n"
            "Water could not condense. The basalt ground was too scorching, and the atmospheric steam was trapped in a supercritical vapor shroud.\n\n"
            "Then... planetary thermodynamics crossed an irreversible tipping point.\n\n"
            "As primordial radioactive decay slowed, surface temperatures dropped below three hundred and fifty degrees Celsius.\n\n"
            "In a geological heartbeat, the physics of water flipped.\n\n"
            "High within the cooling sulfur clouds... the sky broke."
        )
    },
    {
        "scene_id": 4,
        "title": "THE THOUSAND-YEAR DELUGE",
        "scene_type": "torrential_rain",
        "scene_asset": "assets/scenes/torrential_rain.jpg",
        "camera_style": "horizontal_storm_tracking_sweep",
        "mood": "tectonic_rupture",
        "narration": (
            "What followed has never occurred again in the history of the solar system.\n\n"
            "Rain began to fall.\n\n"
            "Not gentle showers, but catastrophic, boiling, acidic downpours crashing day and night, century after century, without stopping for a single second.\n\n"
            "A thousand years of unbroken deluge slamming into glowing basalt rock.\n\n"
            "Explosive steam plumes erupted miles into the sky as superheated water boiled, condensed, and fell again.\n\n"
            "An entire planetary atmosphere of steam was collapsing onto the crust of the Earth."
        )
    },
    {
        "scene_id": 5,
        "title": "THE EMERALD SEA",
        "scene_type": "emerald_ocean_iron",
        "scene_asset": "assets/scenes/emerald_ocean_iron.jpg",
        "camera_style": "panoramic_green_ocean_sweep",
        "mood": "continental_majesty",
        "narration": (
            "When the centuries of scalding rain finally gathered in the lowlands, they pooled into Earth’s very first global ocean.\n\n"
            "It bore zero resemblance to the blue waters we know.\n\n"
            "Under an overcast orange sky, the primordial sea was scalding hot, corrosive, and heavily saturated with dissolved ferrous iron.\n\n"
            "The ocean was an alien, murky emerald green.\n\n"
            "No white sand beaches. No coral reefs. No fish.\n\n"
            "Just hundreds of millions of square miles of boiling, iron-rich acid churning beneath continuous atmospheric lightning storms."
        )
    },
    {
        "scene_id": 6,
        "title": "THE ATOMIC CHRONOMETER",
        "scene_type": "jack_hills_zircon",
        "scene_asset": "assets/scenes/jack_hills_zircon.jpg",
        "camera_style": "macro_luminescence_dolly",
        "mood": "atomic_discovery",
        "narration": (
            "For decades, science textbooks taught that this primordial ocean was a myth—that early Earth was a dry, desiccated wasteland until billions of years later.\n\n"
            "Once again, the ancient rocks proved consensus wrong.\n\n"
            "In the red dirt of Western Australia's Jack Hills, microscopic zircon crystals dated to four point four billion years ago preserved an undeniable atomic fingerprint:\n\n"
            "Heavy oxygen-eighteen isotope ratios that could only be forged in the presence of cool, standing liquid water.\n\n"
            "Within one hundred and fifty million years of planet formation, the impossible ocean was already here."
        )
    },
    {
        "scene_id": 7,
        "title": "THE PREBIOTIC CRUCIBLE (CLIFFHANGER)",
        "scene_type": "hydrothermal_vent",
        "scene_asset": "assets/scenes/hydrothermal_vent.jpg",
        "camera_style": "deep_abyssal_descent",
        "mood": "cliffhanger_suspense",
        "narration": (
            "The sky was still toxic. The green ocean was boiling and acidic.\n\n"
            "Yet four miles beneath the churning waves, where crushing pressure met volcanic heat, black smoker chimneys began spewing chemical riches into the total dark.\n\n"
            "In these abyssal volcanic cauldrons, dead inorganic chemistry was about to cross the final threshold into code.\n\n"
            "How did poisonous minerals spark the first self-replicating breath of life? "
            "And what astronomical catastrophe almost snuffed it out before it could even begin?\n\n"
            "Next time, on History of Earth: The Planet Before Life.\n\n"
            "Subscribe, ring the bell, and journey with us... into the abyss."
        )
    }
]


CINEMATIC_SCENES_HADEAN_LIFE_THEN = [
    {
        "scene_id": 1,
        "title": "THE SILENT CRADLE",
        "scene_type": "hadean_earth_genesis_orbit",
        "scene_asset": "assets/scenes/hadean_earth_genesis_orbit.jpg",
        "camera_style": "orbital_descent_with_telemetry",
        "mood": "cosmic_mystery",
        "narration": (
            "Look at your hands. Feel the pulse in your wrist.\n\n"
            "Inside your body, thirty-seven trillion living cells are burning fuel, copying code, and keeping you alive.\n\n"
            "Every animal, every blade of grass, every microscopic bacterium on this planet shares this exact same operating system.\n\n"
            "Now rewind the clock four point two billion years.\n\n"
            "Earth is an alien graveyard of fire and water. "
            "A churning, scalding emerald-green ocean covers the planet, wrapped in an impenetrable sky of toxic amber smog.\n\n"
            "Zero oxygen. Lethal cosmic radiation. Not a single cell, spore, or strand of DNA exists in the universe.\n\n"
            "Earth is completely, utterly dead.\n\n"
            "So how did raw, poisonous rock learn to breathe?"
        )
    },
    {
        "scene_id": 2,
        "title": "THE 4,000-METER ABYSS",
        "scene_type": "abyssal_descent_darkness",
        "scene_asset": "assets/scenes/hadean_alkaline_vent_towers.jpg",
        "camera_style": "deep_abyssal_sonar_dive",
        "mood": "internal_furnace",
        "narration": (
            "For decades, science believed life began on the surface—in a sunny tide pool or a warm volcanic pond.\n\n"
            "Modern physics shattered that dream.\n\n"
            "Without an ozone layer, the Hadean surface was a planetary radiation chamber. "
            "Solar ultraviolet rays disintegrated organic molecules in seconds. "
            "Torrential acid storms and screaming asteroid impacts vaporized shallow coastlines.\n\n"
            "The surface was a death sentence.\n\n"
            "If life was going to begin, it had to hide.\n\n"
            "Four miles beneath the boiling green waves, in total and suffocating blackness, lies the abyssal floor.\n\n"
            "Here, under four hundred atmospheres of crushing pressure, the violent surface disappears.\n\n"
            "And here, in the cold dark depths, the ocean floor was about to ignite."
        )
    },
    {
        "scene_id": 3,
        "title": "TOWERS OF SERPENTINIZATION",
        "scene_type": "alkaline_vent_towers",
        "scene_asset": "assets/scenes/hadean_alkaline_vent_towers.jpg",
        "camera_style": "colossal_spire_cinematic_dolly",
        "mood": "tectonic_rupture",
        "narration": (
            "Piercing the abyssal darkness rise colossal mineral monuments: shimmering white and gray towers, fifty meters tall, glowing like phantom cathedrals on the seabed.\n\n"
            "These are not volcanic black smokers spewing volcanic acid.\n\n"
            "These are alkaline hydrothermal vents—the ancient ancestors of the Lost City.\n\n"
            "Deep within the seabed, raw olivine rock from Earth's mantle was reacting directly with circulating seawater—a planetary reaction called serpentinization.\n\n"
            "This reaction generated immense heat, swelling the rocks and exhaling warm, mineral-rich alkaline fluids saturated with hydrogen gas and methane.\n\n"
            "Day and night, for millions of years, these colossal mineral towers pumped endless chemical energy into the dark ocean."
        )
    },
    {
        "scene_id": 4,
        "title": "THE NATURAL PROTON BATTERY",
        "scene_type": "proton_gradient_battery",
        "scene_asset": "assets/scenes/hadean_mineral_nanopores_cell.jpg",
        "camera_style": "chemiosmotic_voltage_zoom",
        "mood": "atomic_discovery",
        "narration": (
            "Look closer at the boundary where these vent fluids met the ancient sea.\n\n"
            "The surrounding Hadean ocean was acidic—choked with dissolved carbon dioxide at a pH of five point five.\n\n"
            "The vent fluids emerging through the rock were deeply alkaline—at a pH of ten.\n\n"
            "Separating these two vast chemical worlds was nothing more than a razor-thin membrane of iron and sulfur minerals.\n\n"
            "And that microscopic difference created an astonishing geological miracle.\n\n"
            "A continuous electrical potential of two hundred millivolts across the mineral wall—a natural proton-motive force.\n\n"
            "Earth had accidentally built a planetary battery.\n\n"
            "And remarkably... that exact same electrical voltage powers every single mitochondrion inside your body right now."
        )
    },
    {
        "scene_id": 5,
        "title": "THE ROCK THAT LEARNED TO CODE",
        "scene_type": "mineral_catalytic_nanopores",
        "scene_asset": "assets/scenes/hadean_mineral_nanopores_cell.jpg",
        "camera_style": "microscopic_pore_labyrinth_dive",
        "mood": "atomic_discovery",
        "narration": (
            "Zoom in millions of times into the rock itself.\n\n"
            "The chimney is not solid stone. It is a labyrinth of microscopic mineral honeycomb cavities—tiny chambers no wider than a fraction of a human hair.\n\n"
            "The walls of these pores are made of mackinawite: catalytic clusters of iron, nickel, and sulfur.\n\n"
            "Driven by thermal currents and proton flows, simple organic molecules became trapped inside these micro-chambers.\n\n"
            "The metallic walls acted as inorganic enzymes, forcing carbon dioxide and hydrogen together.\n\n"
            "Amino acids formed. Lipids coated the rock cavities.\n\n"
            "And within these natural stone incubators, nucleotides began linking into the first self-replicating chains of RNA.\n\n"
            "Dead rock was functioning as the universe's first computer hardware."
        )
    },
    {
        "scene_id": 6,
        "title": "THE PROTO-CELL AWAKENING",
        "scene_type": "first_autonomous_protocell",
        "scene_asset": "assets/scenes/hadean_first_protocell.jpg",
        "camera_style": "macro_protocell_birth_drift",
        "mood": "continental_majesty",
        "narration": (
            "For millions of years, proto-life was enslaved to the rock. It could not leave the vent.\n\n"
            "Then came the evolutionary leap that changed the history of the universe.\n\n"
            "Fatty acid molecules lining the stone pores began self-assembling into double-layered spherical membranes.\n\n"
            "They pinched closed—trapping RNA code, metallic catalytic clusters, and an internal proton gradient inside.\n\n"
            "A microscopic bubble broke free from the chimney wall.\n\n"
            "It did not collapse. It did not dissolve.\n\n"
            "It was the world's very first autonomous protocell: the direct ancestor of the Last Universal Common Ancestor—LUCA.\n\n"
            "Life was no longer mineral. Life had become alive."
        )
    },
    {
        "scene_id": 7,
        "title": "THE COMING CATACLYSM (CLIFFHANGER)",
        "scene_type": "late_bombardment_cliffhanger",
        "scene_asset": "assets/scenes/hadean_asteroid_bombardment_ocean.jpg",
        "camera_style": "asteroid_impact_supernova_sweep",
        "mood": "cliffhanger_suspense",
        "narration": (
            "The spark had caught. Life was replicating in the deep dark cradle of the sea floor.\n\n"
            "Yet high above the waves... a cosmic nightmare was hurtling toward Earth.\n\n"
            "The orbits of Jupiter and Saturn shifted, destabilizing the solar system and hurling a storm of mountain-sized asteroids directly into our world: The Late Heavy Bombardment.\n\n"
            "Impact fireballs detonated with the force of billions of megatons, boiling oceans and threatening to sterilize the planet to its core.\n\n"
            "Did Earth's infant biology survive buried inside the crust? "
            "And what microscopic crystals survived to tell the story?\n\n"
            "Next time, on History of Earth: When Rocks Learned to Cool — The Zircon Code.\n\n"
            "Hit subscribe, ring the bell, and journey with us... into the trial of fire."
        )
    }
]


CINEMATIC_SCENES_HADEAN_LEAP = [
    {
        "scene_id": 1,
        "title": "THE FORGOTTEN EON",
        "scene_type": "vanished_hadean_crust",
        "scene_asset": "assets/scenes/hadean_earth_genesis_orbit.jpg",
        "camera_style": "orbital_descent_with_telemetry",
        "mood": "cosmic_mystery",
        "narration": (
            "Pick up a handful of sand. Look at every grain.\n\n"
            "Almost every rock, mountain, and canyon you have ever seen was formed in the last geological blink of an eye.\n\n"
            "The first five hundred million years of Earth's history... are completely gone. A forensic black hole.\n\n"
            "No mountains. No cliffs. No ocean floors survive.\n\n"
            "Over ninety-nine point nine percent of Earth's birth crust was swallowed by the churning mantle or pulverized by cosmic collisions.\n\n"
            "For two centuries, geologists taught that Earth's first half-billion years was an unlivable hell of boiling magma with zero physical record.\n\n"
            "They were wrong.\n\n"
            "Hiding in the ancient desert of Western Australia was a single microscopic grain that refused to die."
        )
    },
    {
        "scene_id": 2,
        "title": "EXPEDITION TO THE JACK HILLS",
        "scene_type": "jack_hills_outback",
        "scene_asset": "assets/scenes/jack_hills_outback_red.jpg",
        "camera_style": "panoramic_outback_geological_scan",
        "mood": "forensic_investigation",
        "narration": (
            "Five hundred miles north of Perth, in the scorching expanse of the Australian Outback, lies the Jack Hills.\n\n"
            "An ancient, weather-beaten ridge of red sandstone and conglomerate rock that has stood undisturbed for three billion years.\n\n"
            "In the late 1990s, geologists arrived not looking for gold or iron, but for something far rarer.\n\n"
            "They crushed tons of ancient quartz rock, washing away the sand through magnetic separators and heavy liquid baths.\n\n"
            "And there, floating in the residue, were tiny microscopic crystals no thicker than a single human hair.\n\n"
            "Zircon grains: time capsules forged in the dawn of time."
        )
    },
    {
        "scene_id": 3,
        "title": "THE INDESTRUCTIBLE VAULT",
        "scene_type": "zircon_crystal_macro",
        "scene_asset": "assets/scenes/jack_hills_zircon.jpg",
        "camera_style": "macro_luminescence_dolly",
        "mood": "atomic_discovery",
        "narration": (
            "To understand why this microscopic crystal matters, look at its atomic architecture: zirconium silicate.\n\n"
            "In the mineral kingdom, zircon is virtually indestructible.\n\n"
            "Harder than steel. Resistant to weathering, crushing tectonic pressures, and chemical acid baths.\n\n"
            "A zircon crystal can withstand temperatures above two thousand degrees Celsius—surviving intact when the volcanic rocks around it melt back into liquid lava.\n\n"
            "As the crystal grows from cooling magma, its tight atomic lattice traps uranium atoms, but violently rejects lead.\n\n"
            "It locks its chemical vault shut at the exact millisecond of crystallization.\n\n"
            "An imperishable atomic clock."
        )
    },
    {
        "scene_id": 4,
        "title": "THE ATOMIC TICK",
        "scene_type": "shrimp_mass_spectrometry",
        "scene_asset": "assets/scenes/zircon_mass_spectrometer.jpg",
        "camera_style": "laser_ablation_mass_spectrometry",
        "mood": "atomic_discovery",
        "narration": (
            "Inside that locked atomic vault, a radioactive countdown began four and a half billion years ago.\n\n"
            "Trapped Uranium-238 steadily decays into Lead-206 with an unshakeable half-life of four point four seven billion years.\n\n"
            "In 2001, geochemists fired the SHRIMP ion microprobe beam into a tiny zircon grain named W74/2-36.\n\n"
            "When the mass spectrometer counted the ratio of uranium to lead, the numbers sent shockwaves through the scientific world.\n\n"
            "The crystal was four point four zero four billion years old.\n\n"
            "The oldest confirmed piece of planet Earth ever discovered.\n\n"
            "And in 2014, atom-probe tomography mapped individual lead atoms inside the crystal nanoclusters—proving the atomic clock had never reset."
        )
    },
    {
        "scene_id": 5,
        "title": "THE IMPOSSIBLE OCEAN",
        "scene_type": "oxygen_isotope_breakthrough",
        "scene_asset": "assets/scenes/hadean_emerald_sea_surface.jpg",
        "camera_style": "ocean_surface_isotope_scan",
        "mood": "atomic_discovery",
        "narration": (
            "Dating the crystal was only the beginning of the shock.\n\n"
            "When scientists probed the oxygen isotopes inside the 4.4-billion-year-old zircon lattice, they discovered something textbooks claimed was impossible.\n\n"
            "The crystal was enriched with heavy Oxygen-18 isotopes, with delta-18-O values soaring up to seven point four per mil.\n\n"
            "In planetary geochemistry, high oxygen-18 ratios have only one fingerprint: granite magma melting in the presence of cool, standing liquid water.\n\n"
            "For fifty years, science taught that Earth was a boiling, magma-choked hell for five hundred million years.\n\n"
            "This microscopic crystal proved consensus dead wrong.\n\n"
            "Just one hundred and fifty million years after planet formation, Earth already had cool liquid oceans."
        )
    },
    {
        "scene_id": 6,
        "title": "CONTINENTS IN THE MIST",
        "scene_type": "granitic_protocontinent",
        "scene_asset": "assets/scenes/granite_protocontinent.jpg",
        "camera_style": "island_arc_collision_cratonic_keel",
        "mood": "continental_majesty",
        "narration": (
            "Next came the titanium-in-zircon thermometer.\n\n"
            "The level of titanium trapped inside the crystal revealed its crystallization temperature: a shockingly cool six hundred and eighty degrees Celsius.\n\n"
            "Basalt from dry mantle plumes crystallizes at eleven hundred degrees.\n\n"
            "Six hundred and eighty degrees is the unmistakable signature of granitic magma—the buoyant, silica-rich rock that makes up modern continental crust.\n\n"
            "This single grain of zircon proved that primitive continents were already rising above the primordial waves four point four billion years ago.\n\n"
            "Earth wasn't just cooling. It was forging the ancestors of the continents we walk on today."
        )
    },
    {
        "scene_id": 7,
        "title": "THE EXTINCTION STORM (CLIFFHANGER)",
        "scene_type": "late_heavy_bombardment_arrival",
        "scene_asset": "assets/scenes/hadean_asteroid_bombardment_ocean.jpg",
        "camera_style": "asteroid_impact_supernova_sweep",
        "mood": "cliffhanger_suspense",
        "narration": (
            "The zircon grains settled into the ancient river sands, carrying the memory of Earth's first oceans and newborn continents.\n\n"
            "Yet peace on infant Earth never lasts.\n\n"
            "High above the atmosphere, the giant outer planets shifted orbits.\n\n"
            "A cataclysmic gravitational resonance uncoiled across the solar system, hurling a colossal storm of mountain-sized asteroids straight into the inner planets: The Late Heavy Bombardment.\n\n"
            "Impact fireballs detonated across the globe, vaporizing oceans and testing Earth's fragile newborn crust to the brink of total annihilation.\n\n"
            "Did Earth's infant oceans survive? And how did our planet reset the clock?\n\n"
            "Next time, on History of Earth: The Bombardment That Almost Reset the Clock.\n\n"
            "Hit subscribe, ring the bell, and journey with us... into the trial of fire."
        )
    }
]


CINEMATIC_SCENES_HADEAN_ENDING = [
    {
        "scene_id": 1,
        "title": "THE GATHERING GRAVITATIONAL TSUNAMI",
        "scene_type": "planetary_resonance_chaos",
        "scene_asset": "assets/scenes/solar_system_resonance_instability.jpg",
        "camera_style": "orbital_jupiter_saturn_drift",
        "mood": "gravitational_tension",
        "narration": (
            "Three point nine billion years ago, deep in the frozen outskirts of the newborn solar system, an invisible disaster was unfolding.\n\n"
            "Jupiter and Saturn, swollen with cosmic gas, were spiraling into a deadly gravitational dance.\n\n"
            "As their orbits locked into a catastrophic two-to-one resonance, their combined gravity tore through the outer asteroid belts like a cosmic wrecking ball.\n\n"
            "Millions of frozen planetesimals, comets, and mountain-sized asteroids were ripped from their quiet orbits and hurled directly into the inner solar system.\n\n"
            "Earth, just beginning to heal its cooling crust, stood directly in the crosshairs of an astronomical firing squad."
        )
    },
    {
        "scene_id": 2,
        "title": "THE SCARRED WITNESS: THE LUNAR ARCHIVE",
        "scene_type": "lunar_crater_basin",
        "scene_asset": "assets/scenes/lunar_crater_basin_apollo.jpg",
        "camera_style": "lunar_surface_crater_zoom",
        "mood": "forensic_lunar_mystery",
        "narration": (
            "Earth remembers almost nothing of this nightmare. Tectonic churning, oceans, and weather wiped our ancient crime scene completely clean.\n\n"
            "To see what happened to our planet, look at our closest neighbor: the Moon.\n\n"
            "When Apollo astronauts landed in the lunar highlands and returned with impact melt rocks from the Imbrium and Serenitatis basins, isotope geochemists discovered an astonishing pattern.\n\n"
            "Nearly every single shock-melted rock was dated to exactly the same narrow window: 3.9 billion years ago.\n\n"
            "Scientists called it the Late Heavy Bombardment: a sudden, violent cataclysm that scarred the Moon with craters the size of entire nations.\n\n"
            "And whatever struck the Moon... hit Earth with ten times the fury."
        )
    },
    {
        "scene_id": 3,
        "title": "FIRESTORM ACROSS THE INFERNAL HORIZON",
        "scene_type": "hypersonic_asteroid_impact",
        "scene_asset": "assets/scenes/hadean_asteroid_bombardment_ocean.jpg",
        "camera_style": "supersonic_shockwave_ocean_sweep",
        "mood": "cataclysmic_inferno",
        "narration": (
            "Because Earth has vastly greater mass and gravity than the Moon, it attracted an onslaught of unimaginable proportions.\n\n"
            "Over twenty thousand massive asteroids slammed into the infant planet at thirty kilometers per second—detonating with the kinetic force of millions of hydrogen bombs per second.\n\n"
            "Mountain-sized bolides tore through the thick carbon dioxide sky, igniting hypersonic fireballs that turned the clouds into incandescent plasma.\n\n"
            "Impact shockwaves blasted through entire ocean basins, instantly flash-boiling cubic kilometers of seawater into blinding towers of superheated steam.\n\n"
            "The newborn crust shattered into vast molten impact lakes. It looked like the end of the world."
        )
    },
    {
        "scene_id": 4,
        "title": "THE GREAT DEBATE: CATACLYSM OR SLOW BURN?",
        "scene_type": "geochronology_debate_chamber",
        "scene_asset": "assets/scenes/crater_dating_spectrometer.jpg",
        "camera_style": "analytical_mass_spec_sweep",
        "mood": "academic_detective",
        "narration": (
            "For forty years, science accepted this story as fact: a single, sudden spike of astronomical violence that nearly obliterated the planet.\n\n"
            "But in recent years, a fierce scientific debate has fractured the consensus.\n\n"
            "Geochemists re-analyzing Apollo sample data and ancient terrestrial zircons noticed something troubling.\n\n"
            "Many of the lunar impact ages might have been biased by samples originating from just one gigantic basin: the Imbrium impact, which scattered its melted debris across half the lunar face.\n\n"
            "Dynamic models now suggest the bombardment might not have been a sudden spike at all, but rather an exponentially decaying tail of planet formation stretching over hundreds of millions of years.\n\n"
            "Was it a single, terrifying cataclysm? Or a grueling, half-billion-year gauntlet that infant Earth had to endure?"
        )
    },
    {
        "scene_id": 5,
        "title": "THE SUBTERRANEAN REFUGE",
        "scene_type": "subsurface_hydrothermal_fracture",
        "scene_asset": "assets/scenes/subterranean_hydrothermal_sanctuary.jpg",
        "camera_style": "deep_crustal_fracture_descent",
        "mood": "subterranean_sanctuary",
        "narration": (
            "Whichever theory is correct, the central mystery remains: Did this planetary bombardment sterilize the planet?\n\n"
            "Did it reset Earth's clock back to zero?\n\n"
            "In 2009, geophysicists Oleg Abramov and Stephen Mojzsis ran complex three-dimensional thermal simulations of Earth's crust under the heaviest possible impact flux.\n\n"
            "Their results overturned everything.\n\n"
            "Even during the peak bombardment, less than twenty-five percent of Earth's crust ever melted simultaneously.\n\n"
            "Thousands of meters beneath the boiling seas, in fractured basalt and deep hydrothermal aquifers, temperatures remained cool enough for hyperthermophilic microbes to thrive.\n\n"
            "The surface was hell. But deep underground, Earth's first living organisms were safely insulated inside an indestructible rocky bunker."
        )
    },
    {
        "scene_id": 6,
        "title": "THE SEEDS OF DESTRUCTION... AND CREATION",
        "scene_type": "carbonaceous_chondrite_crucible",
        "scene_asset": "assets/scenes/carbonaceous_chondrite_delivery.jpg",
        "camera_style": "meteorite_macro_organic_drift",
        "mood": "prebiotic_revelation",
        "narration": (
            "And the asteroids did not merely bring devastation. They brought gifts.\n\n"
            "Trapped within carbonaceous chondrites that rained down upon the crust was extraterrestrial water, vital phosphorus, and complex organic compounds, including amino acids and nucleobases.\n\n"
            "The energy of the impacts themselves superheated hydrothermal fracture systems, creating thousands of brand new geothermal crucibles across the seafloor.\n\n"
            "The very catastrophe that threatened to extinguish life... may have supplied the indispensable chemical ingredients to build it.\n\n"
            "Destruction and creation were locked in a cosmic partnership."
        )
    },
    {
        "scene_id": 7,
        "title": "THE THRESHOLD OF DEEP TIME (CLIFFHANGER)",
        "scene_type": "acasta_gneiss_archean_dawn",
        "scene_asset": "assets/scenes/acasta_gneiss_first_rock.jpg",
        "camera_style": "cratonic_shield_dawn_pan",
        "mood": "cliffhanger_suspense",
        "narration": (
            "Four billion years ago, the bombardment finally began to fade.\n\n"
            "The dust settled from the scorched atmosphere. The oceans condensed once more onto a hardened, scarred crust.\n\n"
            "The Hadean eon—the six-hundred-million-year crucible of fire, poison, and astronomical fury—was officially over.\n\n"
            "Ahead lay a new chapter in our planet's biography: the Archean eon.\n\n"
            "For the very first time in planetary history, solid rock would form that survives intact to this very day.\n\n"
            "Where is the oldest piece of solid Earth you can still touch today?\n\n"
            "Next time, on History of Earth: The First Solid Rock — The 4-Billion-Year-Old Acasta Gneiss.\n\n"
            "Hit subscribe, ring the bell, and step with us across the threshold into the deep past."
        )
    }
]


def write_script(
    approved_claims: List[Dict[str, Any]],
    variation_constraints: Optional[Dict[str, Any]] = None,
    pillar: str = "Map"
) -> Dict[str, Any]:
    """
    Assembles the 7-scene cinematic movie screenplay with high-retention pacing,
    theatrical acting cues, and the mysterious cliffhanger ending.
    """
    norm_pillar = pillar.strip().lower()
    if "ending" in norm_pillar or "bombardment" in norm_pillar:
        scenes = CINEMATIC_SCENES_HADEAN_ENDING
        next_hook = "The First Solid Rock: The 4-Billion-Year-Old Acasta Gneiss"
    elif "leap" in norm_pillar or "zircon" in norm_pillar:
        scenes = CINEMATIC_SCENES_HADEAN_LEAP
        next_hook = "The Bombardment That Almost Reset the Clock"
    elif "life" in norm_pillar:
        scenes = CINEMATIC_SCENES_HADEAN_LIFE_THEN
        next_hook = "When Rocks Learned to Cool: The Zircon Code"
    elif "air" in norm_pillar or "ocean" in norm_pillar:
        scenes = CINEMATIC_SCENES_HADEAN_AIR_OCEAN
        next_hook = "The Planet Before Life"
    elif norm_pillar == "map":
        scenes = CINEMATIC_SCENES_HADEAN_MAP
        next_hook = "The Sky Was Poison and the Rain Never Stopped"
    else:
        scenes = CINEMATIC_SCENES
        next_hook = "The Archean Dawn: The Secret of the Black Smokers"

    shot_list = []
    full_script_blocks = []
    current_time_sec = 0.0

    for scene in scenes:
        scene_text = scene["narration"].strip()
        full_script_blocks.append(f"=== SCENE {scene['scene_id']}: {scene['title']} ===\n{scene_text}")

        # Dramatic trailer cadence: ~2.1 words/sec
        words = len(scene_text.split())
        dur = max(20, int(words / 2.1))

        m_start, s_start = divmod(int(current_time_sec), 60)
        current_time_sec += dur
        m_end, s_end = divmod(int(current_time_sec), 60)

        shot_list.append({
            "shot_id": scene["scene_id"],
            "scene_title": scene["title"],
            "scene_type": scene["scene_type"],
            "scene_asset": scene["scene_asset"],
            "camera_move": scene["camera_style"],
            "mood": scene.get("mood", "cosmic_mystery"),
            "narration_segment": scene_text,
            "duration_sec": dur,
            "timestamp_start": f"{m_start:02d}:{s_start:02d}",
            "timestamp_end": f"{m_end:02d}:{s_end:02d}"
        })

    full_script_text = "\n\n".join(full_script_blocks)

    return {
        "script_text": full_script_text,
        "shot_list": shot_list,
        "runtime_estimate_sec": int(current_time_sec),
        "metadata": {
            "total_scenes": len(scenes),
            "cliffhanger_present": True,
            "next_episode_hook": next_hook,
            "word_count": len(full_script_text.split())
        }
    }


if __name__ == "__main__":
    res = write_script([])
    print(f"Generated 7-Scene Screenplay ({res['runtime_estimate_sec']}s):")
    for s in res["shot_list"]:
        print(f"  [{s['timestamp_start']} - {s['timestamp_end']}] {s['scene_title']}")
